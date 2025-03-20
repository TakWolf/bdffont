import math
import re
from collections.abc import Iterator
from io import StringIO
from os import PathLike
from typing import Any, TextIO

from bdffont.error import BdfParseError, BdfMissingLineError, BdfIllegalWordError, BdfCountError
from bdffont.glyph import BdfGlyph
from bdffont.properties import BdfProperties

_SPEC_VERSION = '2.1'

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


def _iter_as_lines(stream: TextIO) -> Iterator[tuple[int, str, str | None]]:
    for i, line in enumerate(stream):
        line = line.strip()
        if line == '':
            continue
        line_num = i + 1
        tokens = re.split(r' +', line, 1)
        word = tokens[0]
        if len(tokens) < 2:
            tail = None
        else:
            tail = tokens[1]
        yield line_num, word, tail


def _convert_tail_to_ints(tail: str) -> list[int]:
    tokens = re.split(r' +', tail)
    values = [int(token) for token in tokens]
    return values


def _convert_tail_to_properties_value(tail: str) -> str | int:
    if tail.startswith('"') and tail.endswith('"'):
        value = tail.removeprefix('"').removesuffix('"').replace('""', '"')
    else:
        try:
            value = int(tail)
        except ValueError:
            value = tail
    return value


def _parse_properties_segment(
        lines: Iterator[tuple[int, str, str | None]],
        start_line_num: int,
        count: int,
) -> BdfProperties:
    properties = BdfProperties()
    for _line_num, word, tail in lines:
        if word == _WORD_ENDPROPERTIES:
            if len(properties) != count:
                raise BdfCountError(start_line_num, _WORD_STARTPROPERTIES, count, len(properties))
            return properties
        elif word == _WORD_COMMENT:
            properties.comments.append(tail)
        else:
            properties[word] = _convert_tail_to_properties_value(tail)
    raise BdfMissingLineError(start_line_num, _WORD_ENDPROPERTIES)


def _parse_bitmap_segment(
        lines: Iterator[tuple[int, str, str | None]],
        start_line_num: int,
) -> tuple[list[list[int]], list[str]]:
    bitmap = []
    comments = []
    for _line_num, word, tail in lines:
        if word == _WORD_ENDCHAR:
            return bitmap, comments
        elif word == _WORD_COMMENT:
            comments.append(tail)
        else:
            bin_format = '{:0' + str(len(word) * 4) + 'b}'
            bin_string = bin_format.format(int(word, 16))
            bitmap_row = [int(c) for c in bin_string]
            bitmap.append(bitmap_row)
    raise BdfMissingLineError(start_line_num, _WORD_ENDCHAR)


def _parse_glyph_segment(
        lines: Iterator[tuple[int, str, str | None]],
        start_line_num: int,
        name: str,
) -> BdfGlyph:
    encoding = None
    scalable_width = None
    device_width = None
    bounding_box = None
    bitmap = None
    comments = []
    for line_num, word, tail in lines:
        if word == _WORD_ENCODING:
            encoding = int(tail)
        elif word == _WORD_SWIDTH:
            values = _convert_tail_to_ints(tail)
            scalable_width = values[0], values[1]
        elif word == _WORD_DWIDTH:
            values = _convert_tail_to_ints(tail)
            device_width = values[0], values[1]
        elif word == _WORD_BBX:
            values = _convert_tail_to_ints(tail)
            bounding_box = values[0], values[1], values[2], values[3]
        elif word == _WORD_COMMENT:
            comments.append(tail)
        elif word == _WORD_BITMAP or word == _WORD_ENDCHAR:
            if word == _WORD_BITMAP:
                bitmap, bitmap_comments = _parse_bitmap_segment(lines, line_num)
                comments.extend(bitmap_comments)
            if encoding is None:
                raise BdfMissingLineError(start_line_num, _WORD_ENCODING)
            if scalable_width is None:
                raise BdfMissingLineError(start_line_num, _WORD_SWIDTH)
            if device_width is None:
                raise BdfMissingLineError(start_line_num, _WORD_DWIDTH)
            if bounding_box is None:
                raise BdfMissingLineError(start_line_num, _WORD_BBX)
            bitmap = [bitmap_row[:bounding_box[0]] for bitmap_row in bitmap]
            return BdfGlyph(
                name,
                encoding,
                scalable_width,
                device_width,
                bounding_box,
                bitmap,
                comments,
            )
        else:
            raise BdfIllegalWordError(line_num, word)
    raise BdfMissingLineError(start_line_num, _WORD_ENDCHAR)


def _parse_font_segment(
        lines: Iterator[tuple[int, str, str | None]],
        start_line_num: int,
) -> 'BdfFont':
    name = None
    point_size = None
    resolution = None
    bounding_box = None
    properties = None
    chars_line_num = None
    glyphs_count = None
    glyphs = []
    comments = []
    for line_num, word, tail in lines:
        if word == _WORD_FONT:
            name = tail
        elif word == _WORD_SIZE:
            values = _convert_tail_to_ints(tail)
            point_size = values[0]
            resolution = values[1], values[2]
        elif word == _WORD_FONTBOUNDINGBOX:
            values = _convert_tail_to_ints(tail)
            bounding_box = values[0], values[1], values[2], values[3]
        elif word == _WORD_STARTPROPERTIES:
            properties = _parse_properties_segment(lines, line_num, int(tail))
        elif word == _WORD_CHARS:
            chars_line_num = line_num
            glyphs_count = int(tail)
        elif word == _WORD_STARTCHAR:
            glyphs.append(_parse_glyph_segment(lines, line_num, tail))
        elif word == _WORD_COMMENT:
            comments.append(tail)
        elif word == _WORD_ENDFONT:
            if name is None:
                raise BdfMissingLineError(start_line_num, _WORD_FONT)
            if point_size is None or resolution is None:
                raise BdfMissingLineError(start_line_num, _WORD_SIZE)
            if bounding_box is None:
                raise BdfMissingLineError(start_line_num, _WORD_FONTBOUNDINGBOX)
            if glyphs_count is None:
                raise BdfMissingLineError(start_line_num, _WORD_CHARS)
            if len(glyphs) != glyphs_count:
                raise BdfCountError(chars_line_num, _WORD_CHARS, glyphs_count, len(glyphs))
            return BdfFont(
                name,
                point_size,
                resolution,
                bounding_box,
                properties,
                glyphs,
                comments,
            )
        else:
            raise BdfIllegalWordError(line_num, word)
    raise BdfMissingLineError(start_line_num, _WORD_ENDFONT)


class BdfFont:
    @staticmethod
    def parse(stream: str | TextIO) -> 'BdfFont':
        if isinstance(stream, str):
            stream = StringIO(stream)
        lines = _iter_as_lines(stream)

        for line_num, word, tail in lines:
            if word == _WORD_STARTFONT:
                if tail != _SPEC_VERSION:
                    raise BdfParseError(line_num, f'spec version not support: {tail}')
                return _parse_font_segment(lines, line_num)
        raise BdfMissingLineError(1, _WORD_STARTFONT)

    @staticmethod
    def load(file_path: str | PathLike[str]) -> 'BdfFont':
        with open(file_path, 'r', encoding='utf-8') as file:
            return BdfFont.parse(file)

    name: str
    point_size: int
    resolution_x: int
    resolution_y: int
    width: int
    height: int
    offset_x: int
    offset_y: int
    properties: BdfProperties
    glyphs: list[BdfGlyph]
    comments: list[str]

    def __init__(
            self,
            name: str = '',
            point_size: int = 0,
            resolution: tuple[int, int] = (0, 0),
            bounding_box: tuple[int, int, int, int] = (0, 0, 0, 0),
            properties: BdfProperties | None = None,
            glyphs: list[BdfGlyph] | None = None,
            comments: list[str] | None = None,
    ):
        """
        :param name:
            The font name. Should match the PostScript language FontName in the corresponding outline font program,
            or match the 'X logical font description (https://en.wikipedia.org/wiki/X_logical_font_description)'.
        :param point_size:
            The point size of the glyphs.
        :param resolution:
            The x and y resolutions of the device for which the font is intended.
        :param bounding_box:
            The width in x and height in y of the glyphs in integer pixel values.
            The x and y displacement of the lower left corner from origin of the glyphs in integer pixel values.
        :param properties:
            The optional extended properties.
        :param glyphs:
            The glyphs.
        :param comments:
            The comments.
        """
        self.name = name
        self.point_size = point_size
        self.resolution_x, self.resolution_y = resolution
        self.width, self.height, self.offset_x, self.offset_y = bounding_box
        self.properties = BdfProperties() if properties is None else properties
        self.glyphs = [] if glyphs is None else glyphs
        self.comments = [] if comments is None else comments

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BdfFont):
            return False
        return (self.name == other.name and
                self.point_size == other.point_size and
                self.resolution_x == other.resolution_x and
                self.resolution_y == other.resolution_y and
                self.width == other.width and
                self.height == other.height and
                self.offset_x == other.offset_x and
                self.offset_y == other.offset_y and
                self.properties == other.properties and
                self.glyphs == other.glyphs and
                self.comments == other.comments)

    @property
    def resolution(self) -> tuple[int, int]:
        return self.resolution_x, self.resolution_y

    @resolution.setter
    def resolution(self, value: tuple[int, int]):
        self.resolution_x, self.resolution_y = value

    @property
    def dimensions(self) -> tuple[int, int]:
        return self.width, self.height

    @dimensions.setter
    def dimensions(self, value: tuple[int, int]):
        self.width, self.height = value

    @property
    def offset(self) -> tuple[int, int]:
        return self.offset_x, self.offset_y

    @offset.setter
    def offset(self, value: tuple[int, int]):
        self.offset_x, self.offset_y = value

    @property
    def bounding_box(self) -> tuple[int, int, int, int]:
        return self.width, self.height, self.offset_x, self.offset_y

    @bounding_box.setter
    def bounding_box(self, value: tuple[int, int, int, int]):
        self.width, self.height, self.offset_x, self.offset_y = value

    def generate_name_as_xlfd(self):
        self.name = self.properties.to_xlfd()

    def update_by_name_as_xlfd(self):
        self.properties.update_by_xlfd(self.name)
        self.resolution_x = self.properties.resolution_x or 0
        self.resolution_y = self.properties.resolution_y or 0

    def dump(self, stream: TextIO):
        stream.write(f'{_WORD_STARTFONT} {_SPEC_VERSION}\n')
        for comment in self.comments:
            stream.write(f'{_WORD_COMMENT} {comment}\n')
        stream.write(f'{_WORD_FONT} {self.name}\n')
        stream.write(f'{_WORD_SIZE} {self.point_size} {self.resolution_x} {self.resolution_y}\n')
        stream.write(f'{_WORD_FONTBOUNDINGBOX} {self.width} {self.height} {self.offset_x} {self.offset_y}\n')

        stream.write(f'{_WORD_STARTPROPERTIES} {len(self.properties)}\n')
        for comment in self.properties.comments:
            stream.write(f'{_WORD_COMMENT} {comment}\n')
        for key, value in self.properties.items():
            if isinstance(value, str):
                value = value.replace('"', '""')
                value = f'"{value}"'
            stream.write(f'{key} {value}\n')
        stream.write(f'{_WORD_ENDPROPERTIES}\n')

        stream.write(f'{_WORD_CHARS} {len(self.glyphs)}\n')
        for glyph in self.glyphs:
            stream.write(f'{_WORD_STARTCHAR} {glyph.name}\n')
            for comment in glyph.comments:
                stream.write(f'{_WORD_COMMENT} {comment}\n')
            stream.write(f'{_WORD_ENCODING} {glyph.encoding}\n')
            stream.write(f'{_WORD_SWIDTH} {glyph.scalable_width_x} {glyph.scalable_width_y}\n')
            stream.write(f'{_WORD_DWIDTH} {glyph.device_width_x} {glyph.device_width_y}\n')
            stream.write(f'{_WORD_BBX} {glyph.width} {glyph.height} {glyph.offset_x} {glyph.offset_y}\n')
            stream.write(f'{_WORD_BITMAP}\n')
            bitmap_row_width = math.ceil(glyph.width / 8) * 8
            for bitmap_row in glyph.bitmap:
                if len(bitmap_row) < bitmap_row_width:
                    bitmap_row = bitmap_row + [0] * (bitmap_row_width - len(bitmap_row))
                elif len(bitmap_row) > bitmap_row_width:
                    bitmap_row = bitmap_row[:bitmap_row_width]
                bin_string = ''.join(map(str, bitmap_row))
                hex_format = '{:0' + str(len(bitmap_row) // 4) + 'X}'
                hex_value = hex_format.format(int(bin_string, 2))
                stream.write(f'{hex_value}\n')
            stream.write(f'{_WORD_ENDCHAR}\n')

        stream.write(f'{_WORD_ENDFONT}\n')

    def dump_to_string(self) -> str:
        stream = StringIO()
        self.dump(stream)
        return stream.getvalue()

    def save(self, file_path: str | PathLike[str]):
        with open(file_path, 'w', encoding='utf-8') as file:
            self.dump(file)
