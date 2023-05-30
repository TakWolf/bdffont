import os
import re
from typing import Iterable, Iterator

from bdffont.properties import BdfProperties
from bdffont.glyph import BdfGlyph
from bdffont.error import BdfMissingLine, BdfCountIncorrect, BdfGlyphExists


def _next_word_line(lines: Iterator[str]) -> tuple[str, str | None] | None:
    while True:
        try:
            line = next(lines)
        except StopIteration:
            return None
        line = line.strip()
        if line == '':
            continue
        tokens = re.split(r' +', line, 1)
        word = tokens[0]
        if len(tokens) < 2:
            tail = None
        else:
            tail = tokens[1]
        return word, tail


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


def _decode_properties_segment(lines: Iterator[str], count: int, strict_mode: bool) -> BdfProperties:
    properties = BdfProperties()
    while line_params := _next_word_line(lines):
        word, tail = line_params
        if word == 'ENDPROPERTIES':
            if strict_mode and count != len(properties):
                raise BdfCountIncorrect('STARTPROPERTIES', count, len(properties))
            return properties
        elif word == 'COMMENT':
            properties.comments.append(tail)
        else:
            properties[word] = _convert_tail_to_properties_value(tail)
    raise BdfMissingLine('ENDPROPERTIES')


def _decode_bitmap_segment(lines: Iterator[str]) -> list[list[int]]:
    bitmap = []
    while line_params := _next_word_line(lines):
        word, tail = line_params
        if word == 'ENDCHAR':
            return bitmap
        else:
            bin_format = '{:0' + str(len(word) * 4) + 'b}'
            bitmap.append([int(c) for c in bin_format.format(int(word, 16))])
    raise BdfMissingLine('ENDCHAR')


def _decode_glyph_segment(lines: Iterator[str], name: str) -> BdfGlyph:
    code_point = None
    scalable_width = None
    device_width = None
    bounding_box_size = None
    bounding_box_offset = None
    bitmap = None
    comments = []
    while line_params := _next_word_line(lines):
        word, tail = line_params
        if word == 'ENCODING':
            code_point = int(tail)
        elif word == 'SWIDTH':
            tokens = _convert_tail_to_ints(tail)
            scalable_width = tokens[0], tokens[1]
        elif word == 'DWIDTH':
            tokens = _convert_tail_to_ints(tail)
            device_width = tokens[0], tokens[1]
        elif word == 'BBX':
            tokens = _convert_tail_to_ints(tail)
            bounding_box_size = tokens[0], tokens[1]
            bounding_box_offset = tokens[2], tokens[3]
        elif word == 'COMMENT':
            comments.append(tail)
        elif word == 'BITMAP' or word == 'ENDCHAR':
            if word == 'BITMAP':
                bitmap = _decode_bitmap_segment(lines)
            if code_point is None:
                raise BdfMissingLine('ENCODING')
            if scalable_width is None:
                raise BdfMissingLine('SWIDTH')
            if device_width is None:
                raise BdfMissingLine('DWIDTH')
            if bounding_box_size is None or bounding_box_offset is None:
                raise BdfMissingLine('BBX')
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
    raise BdfMissingLine('ENDCHAR')


def _decode_font_segment(lines: Iterator[str], strict_mode: bool) -> 'BdfFont':
    name = None
    point_size = None
    resolution_xy = None
    bounding_box_size = None
    bounding_box_offset = None
    properties = None
    glyphs_count = None
    glyphs = []
    comments = []
    while line_params := _next_word_line(lines):
        word, tail = line_params
        if word == 'FONT':
            name = tail
        elif word == 'SIZE':
            tokens = _convert_tail_to_ints(tail)
            point_size = tokens[0]
            resolution_xy = tokens[1], tokens[2]
        elif word == 'FONTBOUNDINGBOX':
            tokens = _convert_tail_to_ints(tail)
            bounding_box_size = tokens[0], tokens[1]
            bounding_box_offset = tokens[2], tokens[3]
        elif word == 'STARTPROPERTIES':
            properties = _decode_properties_segment(lines, int(tail), strict_mode)
        elif word == 'CHARS':
            glyphs_count = int(tail)
        elif word == 'STARTCHAR':
            glyphs.append(_decode_glyph_segment(lines, tail))
        elif word == 'COMMENT':
            comments.append(tail)
        elif word == 'ENDFONT':
            if name is None:
                raise BdfMissingLine('FONT')
            if point_size is None or resolution_xy is None:
                raise BdfMissingLine('SIZE')
            if bounding_box_size is None or bounding_box_offset is None:
                raise BdfMissingLine('FONTBOUNDINGBOX')
            if glyphs_count is None:
                raise BdfMissingLine('CHARS')
            if strict_mode and glyphs_count != len(glyphs):
                raise BdfCountIncorrect('CHARS', glyphs_count, len(glyphs))
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
    raise BdfMissingLine('ENDFONT')


class BdfFont:
    @staticmethod
    def decode(lines: Iterable[str], strict_mode: bool = False) -> 'BdfFont':
        lines = iter(lines)
        while line_params := _next_word_line(lines):
            word, tail = line_params
            if word == 'STARTFONT':
                font = _decode_font_segment(lines, strict_mode)
                font.spec_version = tail
                return font
        raise BdfMissingLine('STARTFONT')

    @staticmethod
    def decode_str(text: str, strict_mode: bool = False) -> 'BdfFont':
        return BdfFont.decode(text.split('\n'), strict_mode)

    @staticmethod
    def load(
            file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
            strict_mode: bool = False,
    ) -> 'BdfFont':
        with open(file_path, 'r', encoding='utf-8') as file:
            return BdfFont.decode(file.readlines(), strict_mode)

    def __init__(
            self,
            name: str,
            point_size: int,
            resolution_xy: tuple[int, int],
            bounding_box_size: tuple[int, int],
            bounding_box_offset: tuple[int, int],
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
        self.code_point_to_glyph = {}

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

    def get_glyphs_count(self) -> int:
        return len(self.code_point_to_glyph)

    def get_glyph(self, code_point: int) -> BdfGlyph | None:
        return self.code_point_to_glyph.get(code_point, None)

    def get_orderly_glyphs(self) -> list[BdfGlyph]:
        glyphs = list(self.code_point_to_glyph.values())
        glyphs.sort(key=lambda glyph: glyph.code_point)
        return glyphs

    def add_glyph(self, glyph: BdfGlyph):
        if glyph.code_point in self.code_point_to_glyph:
            raise BdfGlyphExists(glyph.code_point)
        self.code_point_to_glyph[glyph.code_point] = glyph

    def add_glyphs(self, glyphs: list[BdfGlyph]):
        for glyph in glyphs:
            self.add_glyph(glyph)

    def set_glyph(self, glyph: BdfGlyph):
        self.code_point_to_glyph[glyph.code_point] = glyph

    def remove_glyph(self, code_point: int) -> BdfGlyph | None:
        return self.code_point_to_glyph.pop(code_point, None)

    def encode(self, optimize_bitmap: bool = False) -> list[str]:
        lines = [
            f'STARTFONT {self.spec_version}',
        ]
        for comment in self.comments:
            lines.append(f'COMMENT {comment}')
        lines.append(f'FONT {self.name}')
        lines.append(f'SIZE {self.point_size} {self.resolution_x} {self.resolution_y}')
        lines.append(f'FONTBOUNDINGBOX {self.bounding_box_width} {self.bounding_box_height} {self.bounding_box_offset_x} {self.bounding_box_offset_y}')

        if len(self.properties) > 0 or len(self.properties.comments) > 0:
            lines.append(f'STARTPROPERTIES {len(self.properties)}')
            for comment in self.properties.comments:
                lines.append(f'COMMENT {comment}')
            for word, value in self.properties.items():
                if isinstance(value, str):
                    value = value.replace('"', '""')
                    value = f'"{value}"'
                lines.append(f'{word} {value}')
            lines.append('ENDPROPERTIES')

        lines.append(f'CHARS {self.get_glyphs_count()}')
        for glyph in self.get_orderly_glyphs():
            lines.append(f'STARTCHAR {glyph.name}')
            for comment in glyph.comments:
                lines.append(f'COMMENT {comment}')
            lines.append(f'ENCODING {glyph.code_point}')
            lines.append(f'SWIDTH {glyph.scalable_width_x} {glyph.scalable_width_y}')
            lines.append(f'DWIDTH {glyph.device_width_x} {glyph.device_width_y}')
            (bounding_box_width, bounding_box_height), (bounding_box_offset_x, bounding_box_offset_y), bitmap = glyph.get_8bit_aligned_bitmap(optimize_bitmap)
            lines.append(f'BBX {bounding_box_width} {bounding_box_height} {bounding_box_offset_x} {bounding_box_offset_y}')
            lines.append('BITMAP')
            for bitmap_row in bitmap:
                hex_format = '{:0' + str(len(bitmap_row) // 4) + 'X}'
                lines.append(hex_format.format(int(''.join(map(str, bitmap_row)), 2)))
            lines.append('ENDCHAR')

        lines.append('ENDFONT')
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
