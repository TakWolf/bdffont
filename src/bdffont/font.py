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

    # The point size of the characters.
    point_size: int

    # The x resolution, and the y resolution of the device for which these characters were intended.
    dpi_x: int
    dpi_y: int

    # The width in x, height in y, and the x and y displacement of the lower left corner from the origin
    # of the character.
    bounding_box_width: int
    bounding_box_height: int
    bounding_box_offset_x: int
    bounding_box_offset_y: int

    # Some optional extended properties.
    properties: BdfProperties

    # Glyph objects using code point indexing.
    code_point_to_glyph: dict[int, BdfGlyph]

    # Comments.
    comments: list[str]

    def __init__(
            self,
            name: str,
            point_size: int,
            dpi_xy: tuple[int, int],
            bounding_box_size: tuple[int, int],
            bounding_box_offset: tuple[int, int],
            properties: BdfProperties = None,
            glyphs: list[BdfGlyph] = None,
            comments: list[str] = None,
    ):
        self.spec_version = '2.1'
        self.name = name
        self.point_size = point_size
        self.dpi_x, self.dpi_y = dpi_xy
        self.bounding_box_width, self.bounding_box_height = bounding_box_size
        self.bounding_box_offset_x, self.bounding_box_offset_y = bounding_box_offset
        if properties is None:
            properties = BdfProperties()
        self.properties = properties
        if glyphs is None:
            glyphs = []
        self.code_point_to_glyph = {glyph.code_point: glyph for glyph in glyphs}
        if comments is None:
            comments = []
        self.comments = comments

    @property
    def dpi_xy(self) -> tuple[int, int]:
        return self.dpi_x, self.dpi_y

    @dpi_xy.setter
    def dpi_xy(self, value: tuple[int, int]):
        self.dpi_x, self.dpi_y = value

    @property
    def bounding_box_size(self) -> tuple[int, int]:
        return self.bounding_box_width, self.bounding_box_height

    @bounding_box_size.setter
    def bounding_box_size(self, value: tuple[int, int]):
        self.bounding_box_width, self.bounding_box_height = value

    @property
    def bounding_box_offset(self) -> tuple[int, int]:
        return self.bounding_box_offset_x, self.bounding_box_offset_y

    @bounding_box_offset.setter
    def bounding_box_offset(self, value: tuple[int, int]):
        self.bounding_box_offset_x, self.bounding_box_offset_y = value

    @property
    def bounding_box(self) -> tuple[int, int, int, int]:
        return self.bounding_box_width, self.bounding_box_height, self.bounding_box_offset_x, self.bounding_box_offset_y

    @bounding_box.setter
    def bounding_box(self, value: tuple[int, int, int, int]):
        self.bounding_box_width, self.bounding_box_height, self.bounding_box_offset_x, self.bounding_box_offset_y = value

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
        lines.append(f'SIZE {self.point_size} {self.dpi_x} {self.dpi_y}')
        lines.append(f'FONTBOUNDINGBOX {self.bounding_box_width} {self.bounding_box_height} {self.bounding_box_offset_x} {self.bounding_box_offset_y}')

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
            lines.append(f'SWIDTH {glyph.scalable_width_x} {glyph.scalable_width_y}')
            lines.append(f'DWIDTH {glyph.device_width_x} {glyph.device_width_y}')
            lines.append(f'BBX {glyph.bounding_box_width} {glyph.bounding_box_height} {glyph.bounding_box_offset_x} {glyph.bounding_box_offset_y}')
            lines.append('BITMAP')
            for bitmap_row in glyph.get_padded_bitmap():
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
