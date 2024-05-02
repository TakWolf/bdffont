import os
import re
from collections.abc import Iterator
from io import StringIO

from bdffont.error import BdfParseError, BdfMissingLineError, BdfIllegalWordError, BdfCountError, BdfPropKeyError, BdfPropValueError
from bdffont.glyph import BdfGlyph
from bdffont.properties import BdfProperties

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


def _iter_as_lines(text: str) -> Iterator[tuple[int, str, str | None]]:
    for i, line in enumerate(text.splitlines()):
        line_num = i + 1
        line = line.strip()
        if line == '':
            continue
        tokens = re.split(r' +', line, 1)
        word = tokens[0]
        if len(tokens) < 2:
            tail = None
        else:
            tail = tokens[1]
        yield line_num, word, tail


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


def _parse_properties_segment(
        lines: Iterator[tuple[int, str, str | None]],
        start_line_num: int,
        count: int,
        strict_level: int,
) -> BdfProperties:
    properties = BdfProperties()
    for _line_num, word, tail in lines:
        if word == _WORD_ENDPROPERTIES:
            if strict_level >= 2 and len(properties) != count:
                raise BdfCountError(start_line_num, _WORD_STARTPROPERTIES, count, len(properties))
            return properties
        elif word == _WORD_COMMENT:
            properties.comments.append(tail)
        else:
            try:
                properties[word] = _convert_tail_to_properties_value(tail)
            except (BdfPropKeyError, BdfPropValueError) as e:
                if strict_level >= 1:
                    raise e
    raise BdfMissingLineError(start_line_num, _WORD_ENDPROPERTIES)


def _parse_bitmap_segment(
        lines: Iterator[tuple[int, str, str | None]],
        start_line_num: int,
        _strict_level: int,
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
        strict_level: int,
) -> BdfGlyph:
    code_point = None
    scalable_width = None
    device_width = None
    bounding_box_size = None
    bounding_box_offset = None
    bitmap = None
    comments = []
    for line_num, word, tail in lines:
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
                bitmap, bitmap_comments = _parse_bitmap_segment(lines, line_num, strict_level)
                comments.extend(bitmap_comments)
            if code_point is None:
                raise BdfMissingLineError(start_line_num, _WORD_ENCODING)
            if scalable_width is None:
                raise BdfMissingLineError(start_line_num, _WORD_SWIDTH)
            if device_width is None:
                raise BdfMissingLineError(start_line_num, _WORD_DWIDTH)
            if bounding_box_size is None or bounding_box_offset is None:
                raise BdfMissingLineError(start_line_num, _WORD_BBX)
            bitmap = [bitmap_row[:bounding_box_size[0]] for bitmap_row in bitmap]
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
        else:
            if strict_level >= 2:
                raise BdfIllegalWordError(line_num, word)
    raise BdfMissingLineError(start_line_num, _WORD_ENDCHAR)


def _parse_font_segment(
        lines: Iterator[tuple[int, str, str | None]],
        start_line_num: int,
        strict_level: int,
) -> 'BdfFont':
    name = None
    point_size = None
    resolution_xy = None
    bounding_box_size = None
    bounding_box_offset = None
    properties = None
    chars_line_num = None
    glyphs_count = None
    glyphs = []
    comments = []
    for line_num, word, tail in lines:
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
            properties = _parse_properties_segment(lines, line_num, int(tail), strict_level)
        elif word == _WORD_CHARS:
            chars_line_num = line_num
            glyphs_count = int(tail)
        elif word == _WORD_STARTCHAR:
            glyphs.append(_parse_glyph_segment(lines, line_num, tail, strict_level))
        elif word == _WORD_COMMENT:
            comments.append(tail)
        elif word == _WORD_ENDFONT:
            if name is None:
                raise BdfMissingLineError(start_line_num, _WORD_FONT)
            if point_size is None or resolution_xy is None:
                raise BdfMissingLineError(start_line_num, _WORD_SIZE)
            if bounding_box_size is None or bounding_box_offset is None:
                raise BdfMissingLineError(start_line_num, _WORD_FONTBOUNDINGBOX)
            if glyphs_count is None:
                raise BdfMissingLineError(start_line_num, _WORD_CHARS)
            if strict_level >= 2 and len(glyphs) != glyphs_count:
                raise BdfCountError(chars_line_num, _WORD_CHARS, glyphs_count, len(glyphs))
            return BdfFont(
                name,
                point_size,
                resolution_xy,
                bounding_box_size,
                bounding_box_offset,
                properties,
                glyphs,
                comments,
            )
        else:
            if strict_level >= 2:
                raise BdfIllegalWordError(line_num, word)
    raise BdfMissingLineError(start_line_num, _WORD_ENDFONT)


class BdfFont:
    @staticmethod
    def parse(text: str, strict_level: int = 1) -> 'BdfFont':
        lines = _iter_as_lines(text)
        for line_num, word, tail in lines:
            if word == _WORD_STARTFONT:
                if strict_level >= 1 and tail != '2.1':
                    raise BdfParseError(line_num, f'BDF version not supported: {tail}')
                font = _parse_font_segment(lines, line_num, strict_level)
                font.spec_version = tail
                return font
        raise BdfMissingLineError(1, _WORD_STARTFONT)

    @staticmethod
    def load(
            file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
            strict_level: int = 1,
    ) -> 'BdfFont':
        with open(file_path, 'r', encoding='utf-8') as file:
            return BdfFont.parse(file.read(), strict_level)

    def __init__(
            self,
            name: str = '',
            point_size: int = 0,
            resolution_xy: tuple[int, int] = (0, 0),
            bounding_box_size: tuple[int, int] = (0, 0),
            bounding_box_offset: tuple[int, int] = (0, 0),
            properties: BdfProperties = None,
            glyphs: list[BdfGlyph] = None,
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
        :param glyphs:
            The glyphs.
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
        if glyphs is None:
            glyphs = []
        self.glyphs = glyphs
        if comments is None:
            comments = []
        self.comments = comments

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

    def generate_name_as_xlfd(self):
        self.name = self.properties.to_xlfd()

    def update_by_name_as_xlfd(self):
        self.properties.update_by_xlfd(self.name)
        self.resolution_x = self.properties.resolution_x or 0
        self.resolution_y = self.properties.resolution_y or 0

    def dump(self) -> str:
        output = StringIO()
        output.write(f'{_WORD_STARTFONT} {self.spec_version}\n')
        for comment in self.comments:
            output.write(f'{_WORD_COMMENT} {comment}\n')
        output.write(f'{_WORD_FONT} {self.name}\n')
        output.write(f'{_WORD_SIZE} {self.point_size} {self.resolution_x} {self.resolution_y}\n')
        output.write(f'{_WORD_FONTBOUNDINGBOX} {self.bounding_box_width} {self.bounding_box_height} {self.bounding_box_offset_x} {self.bounding_box_offset_y}\n')

        output.write(f'{_WORD_STARTPROPERTIES} {len(self.properties)}\n')
        for comment in self.properties.comments:
            output.write(f'{_WORD_COMMENT} {comment}\n')
        for word, value in self.properties.items():
            if isinstance(value, str):
                value = value.replace('"', '""')
                value = f'"{value}"'
            output.write(f'{word} {value}\n')
        output.write(f'{_WORD_ENDPROPERTIES}\n')

        output.write(f'{_WORD_CHARS} {len(self.glyphs)}\n')
        for glyph in self.glyphs:
            output.write(f'{_WORD_STARTCHAR} {glyph.name}\n')
            for comment in glyph.comments:
                output.write(f'{_WORD_COMMENT} {comment}\n')
            output.write(f'{_WORD_ENCODING} {glyph.code_point}\n')
            output.write(f'{_WORD_SWIDTH} {glyph.scalable_width_x} {glyph.scalable_width_y}\n')
            output.write(f'{_WORD_DWIDTH} {glyph.device_width_x} {glyph.device_width_y}\n')
            output.write(f'{_WORD_BBX} {glyph.bounding_box_width} {glyph.bounding_box_height} {glyph.bounding_box_offset_x} {glyph.bounding_box_offset_y}\n')
            output.write(f'{_WORD_BITMAP}\n')
            for bitmap_row in glyph.bitmap:
                if len(bitmap_row) % 8 > 0:
                    bitmap_row = bitmap_row + [0] * (8 - len(bitmap_row) % 8)
                bin_string = ''.join(map(str, bitmap_row))
                hex_format = '{:0' + str(len(bitmap_row) // 4) + 'X}'
                hex_value = hex_format.format(int(bin_string, 2))
                output.write(f'{hex_value}\n')
            output.write(f'{_WORD_ENDCHAR}\n')

        output.write(f'{_WORD_ENDFONT}\n')
        return output.getvalue()

    def save(self, file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.dump())
