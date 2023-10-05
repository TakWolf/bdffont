import os
import re
from collections.abc import Iterable, Iterator

from bdffont import xlfd
from bdffont.properties import BdfProperties
from bdffont.glyph import BdfGlyph
from bdffont.error import BdfException, BdfMissingLine, BdfCountIncorrect, BdfGlyphExists

_WORD_STARTFONT = 'STARTFONT'
_WORD_ENDFONT = 'ENDFONT'
_WORD_COMMENT = 'COMMENT'
_WORD_FONT = 'FONT'
_WORD_SIZE = 'SIZE'
_WORD_FONTBOUNDINGBOX = 'FONTBOUNDINGBOX'
_WORD_STARTPROPERTIES = 'STARTPROPERTIES'
_WORD_ENDPROPERTIES = 'ENDPROPERTIES'
_WORD_CHARS = 'CHARS'
_WORD_STARTCHAR = 'STARTCHAR'
_WORD_ENDCHAR = 'ENDCHAR'
_WORD_ENCODING = 'ENCODING'
_WORD_SWIDTH = 'SWIDTH'
_WORD_DWIDTH = 'DWIDTH'
_WORD_BBX = 'BBX'
_WORD_BITMAP = 'BITMAP'


def _iter_word_lines(lines: Iterable[str]) -> Iterator[tuple[str, str | None]]:
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        tokens = re.split(r' +', line, 1)
        word = tokens[0]
        if len(tokens) < 2:
            tail = None
        else:
            tail = tokens[1]
        yield word, tail


def _convert_tail_to_ints(tail: str) -> list[int]:
    tokens = re.split(r' +', tail)
    ints = [int(token) for token in tokens]
    return ints


def _convert_tail_to_properties_value(tail: str) -> str | int:
    if tail.startswith('"') and tail.endswith('"'):
        value = tail.removeprefix('"').removesuffix('"').replace('""', '"')
    else:
        try:
            value = int(tail)
        except ValueError:
            value = tail
    return value


def _decode_properties_segment(word_lines: Iterator[tuple[str, str | None]], count: int, strict_mode: bool) -> BdfProperties:
    properties = BdfProperties()
    for word, tail in word_lines:
        if word == _WORD_ENDPROPERTIES:
            if strict_mode and count != len(properties):
                raise BdfCountIncorrect(_WORD_STARTPROPERTIES, count, len(properties))
            return properties
        elif word == _WORD_COMMENT:
            properties.comments.append(tail)
        else:
            properties[word] = _convert_tail_to_properties_value(tail)
    raise BdfMissingLine(_WORD_ENDPROPERTIES)


def _decode_bitmap_segment(word_lines: Iterator[tuple[str, str | None]]) -> list[list[int]]:
    bitmap = []
    for word, tail in word_lines:
        if word == _WORD_ENDCHAR:
            return bitmap
        else:
            bin_format = '{:0' + str(len(word) * 4) + 'b}'
            bitmap.append([int(c) for c in bin_format.format(int(word, 16))])
    raise BdfMissingLine(_WORD_ENDCHAR)


def _decode_glyph_segment(word_lines: Iterator[tuple[str, str | None]], name: str) -> BdfGlyph:
    code_point = None
    scalable_width = None
    device_width = None
    bounding_box_size = None
    bounding_box_offset = None
    bitmap = None
    comments = []
    for word, tail in word_lines:
        if word == _WORD_ENCODING:
            code_point = int(tail)
        elif word == _WORD_SWIDTH:
            tokens = _convert_tail_to_ints(tail)
            scalable_width = tokens[0], tokens[1]
        elif word == _WORD_DWIDTH:
            tokens = _convert_tail_to_ints(tail)
            device_width = tokens[0], tokens[1]
        elif word == _WORD_BBX:
            tokens = _convert_tail_to_ints(tail)
            bounding_box_size = tokens[0], tokens[1]
            bounding_box_offset = tokens[2], tokens[3]
        elif word == _WORD_COMMENT:
            comments.append(tail)
        elif word == _WORD_BITMAP or word == _WORD_ENDCHAR:
            if word == _WORD_BITMAP:
                bitmap = _decode_bitmap_segment(word_lines)
            if code_point is None:
                raise BdfMissingLine(_WORD_ENCODING)
            if scalable_width is None:
                raise BdfMissingLine(_WORD_SWIDTH)
            if device_width is None:
                raise BdfMissingLine(_WORD_DWIDTH)
            if bounding_box_size is None or bounding_box_offset is None:
                raise BdfMissingLine(_WORD_BBX)
            for bitmap_row in bitmap:
                while len(bitmap_row) > bounding_box_size[0]:
                    bitmap_row.pop()
            return BdfGlyph(
                name,
                code_point,
                scalable_width,
                device_width,
                bounding_box_size,
                bounding_box_offset,
                bitmap,
                comments,
            )
    raise BdfMissingLine(_WORD_ENDCHAR)


def _decode_font_segment(word_lines: Iterator[tuple[str, str | None]], strict_mode: bool) -> 'BdfFont':
    name = None
    point_size = None
    resolution_xy = None
    bounding_box_size = None
    bounding_box_offset = None
    properties = None
    glyphs_count = None
    glyphs = []
    comments = []
    for word, tail in word_lines:
        if word == _WORD_FONT:
            name = tail
        elif word == _WORD_SIZE:
            tokens = _convert_tail_to_ints(tail)
            point_size = tokens[0]
            resolution_xy = tokens[1], tokens[2]
        elif word == _WORD_FONTBOUNDINGBOX:
            tokens = _convert_tail_to_ints(tail)
            bounding_box_size = tokens[0], tokens[1]
            bounding_box_offset = tokens[2], tokens[3]
        elif word == _WORD_STARTPROPERTIES:
            properties = _decode_properties_segment(word_lines, int(tail), strict_mode)
        elif word == _WORD_CHARS:
            glyphs_count = int(tail)
        elif word == _WORD_STARTCHAR:
            glyphs.append(_decode_glyph_segment(word_lines, tail))
        elif word == _WORD_COMMENT:
            comments.append(tail)
        elif word == _WORD_ENDFONT:
            if name is None:
                raise BdfMissingLine(_WORD_FONT)
            if point_size is None or resolution_xy is None:
                raise BdfMissingLine(_WORD_SIZE)
            if bounding_box_size is None or bounding_box_offset is None:
                raise BdfMissingLine(_WORD_FONTBOUNDINGBOX)
            if glyphs_count is None:
                raise BdfMissingLine(_WORD_CHARS)
            if strict_mode and glyphs_count != len(glyphs):
                raise BdfCountIncorrect(_WORD_CHARS, glyphs_count, len(glyphs))
            font = BdfFont(
                name,
                point_size,
                resolution_xy,
                bounding_box_size,
                bounding_box_offset,
                properties,
                comments,
            )
            font.add_glyphs(glyphs)
            return font
    raise BdfMissingLine(_WORD_ENDFONT)


class BdfFont:
    @staticmethod
    def decode(lines: Iterable[str], strict_mode: bool = False) -> 'BdfFont':
        word_lines = _iter_word_lines(lines)
        for word, tail in word_lines:
            if word == _WORD_STARTFONT:
                font = _decode_font_segment(word_lines, strict_mode)
                font.spec_version = tail
                return font
        raise BdfMissingLine(_WORD_STARTFONT)

    @staticmethod
    def decode_str(text: str, strict_mode: bool = False) -> 'BdfFont':
        return BdfFont.decode(re.split(r'\r\n|\r|\n', text), strict_mode)

    @staticmethod
    def load(
            file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
            strict_mode: bool = False,
    ) -> 'BdfFont':
        with open(file_path, 'r', encoding='utf-8') as file:
            return BdfFont.decode_str(file.read(), strict_mode)

    def __init__(
            self,
            name: str = None,
            point_size: int = 0,
            resolution_xy: tuple[int, int] = (0, 0),
            bounding_box_size: tuple[int, int] = (0, 0),
            bounding_box_offset: tuple[int, int] = (0, 0),
            properties: BdfProperties = None,
            comments: list[str] = None,
    ):
        """
        :param name:
            The font name. Should match the PostScript language FontName in the corresponding outline font program,
            or match the 'X logical font description (https://en.wikipedia.org/wiki/X_logical_font_description)'.
        :param point_size:
            The point size of the glyphs.
        :param resolution_xy:
            The x and y resolutions of the device for which the font is intended.
        :param bounding_box_size:
            The width in x and height in y of the glyphs in integer pixel values.
        :param bounding_box_offset:
            The x and y displacement of the lower left corner from origin 0 of the glyphs in integer pixel values.
        :param properties:
            The optional extended properties.
        :param comments:
            The comments.
        """
        self.spec_version = '2.1'
        self.name = name
        self.point_size = point_size
        self.resolution_x, self.resolution_y = resolution_xy
        self.bounding_box_width, self.bounding_box_height = bounding_box_size
        self.bounding_box_offset_x, self.bounding_box_offset_y = bounding_box_offset
        if properties is None:
            properties = BdfProperties()
        self.properties = properties
        if comments is None:
            comments = []
        self.comments = comments
        self.code_point_to_glyph: dict[int, BdfGlyph] = {}

    @property
    def resolution_xy(self) -> tuple[int, int]:
        return self.resolution_x, self.resolution_y

    @resolution_xy.setter
    def resolution_xy(self, value: tuple[int, int]):
        self.resolution_x, self.resolution_y = value

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

    def get_glyphs(self) -> list[BdfGlyph]:
        glyphs = list(self.code_point_to_glyph.values())
        glyphs.sort(key=lambda glyph: glyph.code_point)
        return glyphs

    def get_glyphs_count(self) -> int:
        return len(self.code_point_to_glyph)

    def set_glyph(self, glyph: BdfGlyph):
        self.code_point_to_glyph[glyph.code_point] = glyph

    def add_glyph(self, glyph: BdfGlyph):
        if glyph.code_point in self.code_point_to_glyph:
            raise BdfGlyphExists(glyph.code_point)
        self.code_point_to_glyph[glyph.code_point] = glyph

    def add_glyphs(self, glyphs: list[BdfGlyph]):
        for glyph in glyphs:
            self.add_glyph(glyph)

    def remove_glyph(self, code_point: int) -> BdfGlyph | None:
        return self.code_point_to_glyph.pop(code_point, None)

    def setup_missing_xlfd_properties(self):
        if self.properties.weight_name is None:
            self.properties.weight_name = xlfd.WeightName.MEDIUM
        if self.properties.slant is None:
            self.properties.slant = xlfd.Slant.ROMAN
        if self.properties.setwidth_name is None:
            self.properties.setwidth_name = xlfd.SetwidthName.NORMAL
        if self.properties.resolution_x is None:
            self.properties.resolution_x = self.resolution_x
        if self.properties.resolution_y is None:
            self.properties.resolution_y = self.resolution_y
        if self.properties.charset_registry is None and self.properties.charset_encoding is None:
            self.properties.charset_registry = xlfd.CharsetRegistry.ISO10646
            self.properties.charset_encoding = '1'

    def generate_xlfd_font_name(self):
        self.name = self.properties.to_xlfd_font_name()

    def update_by_name_as_xlfd_font_name(self):
        if self.name is None:
            raise BdfException("Missing attribute 'name'")

        self.properties.update_by_xlfd_font_name(self.name)
        self.resolution_x = self.properties.resolution_x
        self.resolution_y = self.properties.resolution_y

    def encode(self, optimize_bitmap: bool = False) -> list[str]:
        if self.name is None:
            raise BdfException("Missing attribute 'name'")

        lines = [
            f'{_WORD_STARTFONT} {self.spec_version}',
        ]
        for comment in self.comments:
            lines.append(f'{_WORD_COMMENT} {comment}')
        lines.append(f'{_WORD_FONT} {self.name}')
        lines.append(f'{_WORD_SIZE} {self.point_size} {self.resolution_x} {self.resolution_y}')
        lines.append(f'{_WORD_FONTBOUNDINGBOX} {self.bounding_box_width} {self.bounding_box_height} {self.bounding_box_offset_x} {self.bounding_box_offset_y}')

        if len(self.properties) > 0 or len(self.properties.comments) > 0:
            lines.append(f'{_WORD_STARTPROPERTIES} {len(self.properties)}')
            for comment in self.properties.comments:
                lines.append(f'{_WORD_COMMENT} {comment}')
            for word, value in self.properties.items():
                if isinstance(value, str):
                    value = value.replace('"', '""')
                    value = f'"{value}"'
                lines.append(f'{word} {value}')
            lines.append(_WORD_ENDPROPERTIES)

        lines.append(f'{_WORD_CHARS} {self.get_glyphs_count()}')
        for glyph in self.get_glyphs():
            lines.append(f'{_WORD_STARTCHAR} {glyph.name}')
            for comment in glyph.comments:
                lines.append(f'{_WORD_COMMENT} {comment}')
            lines.append(f'{_WORD_ENCODING} {glyph.code_point}')
            lines.append(f'{_WORD_SWIDTH} {glyph.scalable_width_x} {glyph.scalable_width_y}')
            lines.append(f'{_WORD_DWIDTH} {glyph.device_width_x} {glyph.device_width_y}')
            (bounding_box_width, bounding_box_height), (bounding_box_offset_x, bounding_box_offset_y), bitmap = glyph.get_8bit_aligned_bitmap(optimize_bitmap)
            lines.append(f'{_WORD_BBX} {bounding_box_width} {bounding_box_height} {bounding_box_offset_x} {bounding_box_offset_y}')
            lines.append(_WORD_BITMAP)
            for bitmap_row in bitmap:
                hex_format = '{:0' + str(len(bitmap_row) // 4) + 'X}'
                lines.append(hex_format.format(int(''.join(map(str, bitmap_row)), 2)))
            lines.append(_WORD_ENDCHAR)

        lines.append(_WORD_ENDFONT)
        lines.append('')
        return lines

    def encode_str(self, optimize_bitmap: bool = False) -> str:
        return '\n'.join(self.encode(optimize_bitmap))

    def save(
            self,
            file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
            optimize_bitmap: bool = False,
    ):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.encode_str(optimize_bitmap))
