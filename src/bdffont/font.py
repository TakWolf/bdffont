import os

from bdffont.properties import BdfProperties
from bdffont.glyph import BdfGlyph
from bdffont.error import BdfGlyphExists


class BdfFont:
    # The BDF Specification version.
    spec_version: str

    # Either the 'X logical font description' or some private font name.
    # https://en.wikipedia.org/wiki/X_logical_font_description
    # Example: -Adobe-Helvetica-Bold-R-Normal--24-240-75-75-P-65-ISO8859-1
    name: str

    # The point size of the characters, the x resolution, and the y resolution of the device for which these characters were intended.
    # Names: point_size, x_dpi, y_dpi
    size: tuple[int, int, int]

    # The width in x, height in y, and the x and y displacement of the lower left corner from the origin of the character.
    # Names: bounding_box_width, bounding_box_height, bounding_box_origin_x, bounding_box_origin_y
    bounding_box: tuple[int, int, int, int]

    # Some optional extended properties.
    properties: BdfProperties

    # Glyph objects using code point indexing.
    code_point_to_glyph: dict[int, BdfGlyph]

    # Comments.
    comments: list[str]

    def __init__(
            self,
            name: str,
            size: tuple[int, int, int],
            bounding_box: tuple[int, int, int, int],
            properties: BdfProperties = None,
            glyphs: list[BdfGlyph] = None,
            comments: list[str] = None,
    ):
        self.spec_version = '2.1'
        self.name = name
        self.size = size
        self.bounding_box = bounding_box
        if properties is None:
            self.properties = BdfProperties()
        else:
            self.properties = properties
        if glyphs is None:
            self.code_point_to_glyph = {}
        else:
            self.code_point_to_glyph = {glyph.code_point: glyph for glyph in glyphs}
        if comments is None:
            self.comments = []
        else:
            self.comments = comments

    @property
    def point_size(self) -> int:
        return self.size[0]

    @point_size.setter
    def point_size(self, value: int):
        self.size = (value, self.size[1], self.size[2])

    @property
    def xy_dpi(self) -> tuple[int, int]:
        return self.size[1], self.size[2]

    @xy_dpi.setter
    def xy_dpi(self, value: tuple[int, int]):
        self.size = (self.size[0], value[0], value[1])

    @property
    def x_dpi(self) -> int:
        return self.size[1]

    @x_dpi.setter
    def x_dpi(self, value: int):
        self.size = (self.size[0], value, self.size[2])

    @property
    def y_dpi(self) -> int:
        return self.size[2]

    @y_dpi.setter
    def y_dpi(self, value: int):
        self.size = (self.size[0], self.size[1], value)

    @property
    def bounding_box_size(self) -> tuple[int, int]:
        return self.bounding_box[0], self.bounding_box[1]

    @bounding_box_size.setter
    def bounding_box_size(self, value: tuple[int, int]):
        self.bounding_box = (value[0], value[1], self.bounding_box[2], self.bounding_box[3])

    @property
    def bounding_box_width(self) -> int:
        return self.bounding_box[0]

    @bounding_box_width.setter
    def bounding_box_width(self, value: int):
        self.bounding_box = (value, self.bounding_box[1], self.bounding_box[2], self.bounding_box[3])

    @property
    def bounding_box_height(self) -> int:
        return self.bounding_box[1]

    @bounding_box_height.setter
    def bounding_box_height(self, value: int):
        self.bounding_box = (self.bounding_box[0], value, self.bounding_box[2], self.bounding_box[3])

    @property
    def bounding_box_origin(self) -> tuple[int, int]:
        return self.bounding_box[2], self.bounding_box[3]

    @bounding_box_origin.setter
    def bounding_box_origin(self, value: tuple[int, int]):
        self.bounding_box = (self.bounding_box[0], self.bounding_box[1], value[0], value[1])

    @property
    def bounding_box_origin_x(self) -> int:
        return self.bounding_box[2]

    @bounding_box_origin_x.setter
    def bounding_box_origin_x(self, value: int):
        self.bounding_box = (self.bounding_box[0], self.bounding_box[1], value, self.bounding_box[3])

    @property
    def bounding_box_origin_y(self) -> int:
        return self.bounding_box[3]

    @bounding_box_origin_y.setter
    def bounding_box_origin_y(self, value: int):
        self.bounding_box = (self.bounding_box[0], self.bounding_box[1], self.bounding_box[2], value)

    def get_glyph(self, code_point: int) -> BdfGlyph | None:
        return self.code_point_to_glyph.get(code_point, None)

    def add_glyph(self, glyph: BdfGlyph):
        if glyph.code_point in self.code_point_to_glyph:
            raise BdfGlyphExists(glyph.code_point)
        self.code_point_to_glyph[glyph.code_point] = glyph

    def set_glyph(self, glyph: BdfGlyph):
        self.code_point_to_glyph[glyph.code_point] = glyph

    def remove_glyph(self, code_point: int) -> BdfGlyph | None:
        return self.code_point_to_glyph.pop(code_point, None)

    def encode(self) -> list[str]:
        lines = [
            f'STARTFONT {self.spec_version}',
        ]
        for comment in self.comments:
            lines.append(f'COMMENT {comment}')
        lines.append(f'FONT {self.name}')
        lines.append(f'SIZE {self.size[0]} {self.size[1]} {self.size[2]}')
        lines.append(f'FONTBOUNDINGBOX {self.bounding_box[0]} {self.bounding_box[1]} {self.bounding_box[2]} {self.bounding_box[3]}')

        lines.append(f'STARTPROPERTIES {len(self.properties)}')
        for comment in self.properties.comments:
            lines.append(f'COMMENT {comment}')
        for word, value in self.properties.items():
            if isinstance(value, str):
                value = f'"{value}"'
            lines.append(f'{word} {value}')
        lines.append('ENDPROPERTIES')

        alphabet = list(self.code_point_to_glyph.items())
        alphabet.sort()
        lines.append(f'CHARS {len(alphabet)}')
        for code_point, glyph in alphabet:
            lines.append(f'STARTCHAR {glyph.name}')
            for comment in glyph.comments:
                lines.append(f'COMMENT {comment}')
            lines.append(f'ENCODING {code_point}')
            lines.append(f'SWIDTH {glyph.scalable_width[0]} {glyph.scalable_width[1]}')
            lines.append(f'DWIDTH {glyph.device_width[0]} {glyph.device_width[1]}')
            lines.append(f'BBX {glyph.bounding_box[0]} {glyph.bounding_box[1]} {glyph.bounding_box[2]} {glyph.bounding_box[3]}')
            lines.append('BITMAP')
            for bitmap_row in glyph.get_padding_bitmap():
                hex_format = '{:0' + str(len(bitmap_row) // 4) + 'X}'
                lines.append(hex_format.format(int(''.join(map(str, bitmap_row)), 2)))
            lines.append('ENDCHAR')

        lines.append('ENDFONT')
        lines.append('')
        return lines

    def encode_str(self) -> str:
        return '\n'.join(self.encode())

    def save(self, file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.encode_str())
