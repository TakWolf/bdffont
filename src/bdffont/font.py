import math
import re
from collections.abc import Iterator
from io import StringIO
from os import PathLike
from typing import Any, TextIO

from bdffont.error import BdfParseError, BdfMissingWordError, BdfIllegalWordError, BdfCountError, BdfDumpError
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


def _create_lines_iterator(stream: TextIO) -> Iterator[tuple[str, str]]:
    for line in stream:
        line = line.strip()
        if line == '':
            continue
        tokens = re.split(r' +', line, 1)
        word = tokens[0]
        tail = tokens[1] if len(tokens) >= 2 else ''
        yield word, tail


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


def _parse_properties_segment(lines: Iterator[tuple[str, str]], count: int) -> BdfProperties:
    properties = BdfProperties()
    for word, tail in lines:
        if word == _WORD_ENDPROPERTIES:
            if len(properties) != count:
                raise BdfCountError(_WORD_STARTPROPERTIES, count, len(properties))
            return properties
        elif word == _WORD_COMMENT:
            properties.comments.append(tail)
        else:
            properties[word] = _convert_tail_to_properties_value(tail)
    raise BdfMissingWordError(_WORD_ENDPROPERTIES)


def _parse_bitmap_segment(lines: Iterator[tuple[str, str]]) -> list[list[int]]:
    bitmap = []
    for word, _ in lines:
        if word == _WORD_ENDCHAR:
            return bitmap
        else:
            bin_format = '{:0' + str(len(word) * 4) + 'b}'
            bin_string = bin_format.format(int(word, 16))
            bitmap_row = [int(c) for c in bin_string]
            bitmap.append(bitmap_row)
    raise BdfMissingWordError(_WORD_ENDCHAR)


def _parse_glyph_segment(lines: Iterator[tuple[str, str]], name: str) -> BdfGlyph:
    encoding = None
    scalable_width = None
    device_width = None
    bounding_box = None
    bitmap = None
    comments = []
    for word, tail in lines:
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
                bitmap = _parse_bitmap_segment(lines)
            if encoding is None:
                raise BdfMissingWordError(_WORD_ENCODING)
            if scalable_width is None:
                raise BdfMissingWordError(_WORD_SWIDTH)
            if device_width is None:
                raise BdfMissingWordError(_WORD_DWIDTH)
            if bounding_box is None:
                raise BdfMissingWordError(_WORD_BBX)
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
            raise BdfIllegalWordError(word)
    raise BdfMissingWordError(_WORD_ENDCHAR)


def _parse_font_segment(lines: Iterator[tuple[str, str]]) -> 'BdfFont':
    name = None
    point_size = None
    resolution = None
    bounding_box = None
    properties = None
    glyphs_count = None
    glyphs = []
    comments = []
    for word, tail in lines:
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
            properties = _parse_properties_segment(lines, int(tail))
        elif word == _WORD_CHARS:
            glyphs_count = int(tail)
        elif word == _WORD_STARTCHAR:
            glyphs.append(_parse_glyph_segment(lines, tail))
        elif word == _WORD_COMMENT:
            comments.append(tail)
        elif word == _WORD_ENDFONT:
            if name is None:
                raise BdfMissingWordError(_WORD_FONT)
            if point_size is None or resolution is None:
                raise BdfMissingWordError(_WORD_SIZE)
            if bounding_box is None:
                raise BdfMissingWordError(_WORD_FONTBOUNDINGBOX)
            if glyphs_count is None:
                raise BdfMissingWordError(_WORD_CHARS)
            if len(glyphs) != glyphs_count:
                raise BdfCountError(_WORD_CHARS, glyphs_count, len(glyphs))
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
            raise BdfIllegalWordError(word)
    raise BdfMissingWordError(_WORD_ENDFONT)


def _parse_stream(stream: TextIO) -> 'BdfFont':
    lines = _create_lines_iterator(stream)
    for word, tail in lines:
        if word == _WORD_STARTFONT:
            if tail != _SPEC_VERSION:
                raise BdfParseError(f'spec version not support: {tail}')
            return _parse_font_segment(lines)
    raise BdfMissingWordError(_WORD_STARTFONT)


def _dump_word_str_line(stream: TextIO, word: str, tail: str | None = None):
    stream.write(word)
    if tail is not None:
        tail = tail.strip()
        if tail != '':
            if len(tail.splitlines()) > 1:
                raise BdfDumpError('tail cannot be multi-line string')
            stream.write(f' {tail}')
    stream.write('\n')


def _dump_word_ints_line(stream: TextIO, word: str, *values: int):
    stream.write(word)
    for value in values:
        stream.write(f' {value}')
    stream.write('\n')


def _dump_properties_line(stream: TextIO, key: str, value: str | int):
    if isinstance(value, str):
        value = value.replace('"', '""')
        value = f'"{value}"'
        if len(value.splitlines()) > 1:
            raise BdfDumpError('properties value cannot be multi-line string')
    stream.write(f'{key} {value}\n')


class BdfFont:
    @staticmethod
    def parse(stream: str | TextIO) -> 'BdfFont':
        if isinstance(stream, str):
            stream = StringIO(stream)
        return _parse_stream(stream)

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
        _dump_word_str_line(stream, _WORD_STARTFONT, _SPEC_VERSION)
        for comment in self.comments:
            _dump_word_str_line(stream, _WORD_COMMENT, comment)
        _dump_word_str_line(stream, _WORD_FONT, self.name)
        _dump_word_ints_line(stream, _WORD_SIZE, self.point_size, self.resolution_x, self.resolution_y)
        _dump_word_ints_line(stream, _WORD_FONTBOUNDINGBOX, self.width, self.height, self.offset_x, self.offset_y)

        _dump_word_ints_line(stream, _WORD_STARTPROPERTIES, len(self.properties))
        for comment in self.properties.comments:
            _dump_word_str_line(stream, _WORD_COMMENT, comment)
        for key, value in self.properties.items():
            _dump_properties_line(stream, key, value)
        _dump_word_str_line(stream, _WORD_ENDPROPERTIES)

        _dump_word_ints_line(stream, _WORD_CHARS, len(self.glyphs))
        for glyph in self.glyphs:
            _dump_word_str_line(stream, _WORD_STARTCHAR, glyph.name)
            for comment in glyph.comments:
                _dump_word_str_line(stream, _WORD_COMMENT, comment)
            _dump_word_ints_line(stream, _WORD_ENCODING, glyph.encoding)
            _dump_word_ints_line(stream, _WORD_SWIDTH, glyph.scalable_width_x, glyph.scalable_width_y)
            _dump_word_ints_line(stream, _WORD_DWIDTH, glyph.device_width_x, glyph.device_width_y)
            _dump_word_ints_line(stream, _WORD_BBX, glyph.width, glyph.height, glyph.offset_x, glyph.offset_y)
            _dump_word_str_line(stream, _WORD_BITMAP)
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
            _dump_word_str_line(stream, _WORD_ENDCHAR)

        _dump_word_str_line(stream, _WORD_ENDFONT)

    def dump_to_string(self) -> str:
        stream = StringIO()
        self.dump(stream)
        return stream.getvalue()

    def save(self, file_path: str | PathLike[str]):
        with open(file_path, 'w', encoding='utf-8') as file:
            self.dump(file)
