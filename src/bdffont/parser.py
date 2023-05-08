import os
import re
from typing import Iterator

from bdffont.font import BdfFont
from bdffont.properties import BdfProperties
from bdffont.glyph import BdfGlyph
from bdffont.error import BdfMissingLine, BdfValueIncorrect


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
        value = tail.removeprefix('"').removesuffix('"')
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
                raise BdfValueIncorrect('STARTPROPERTIES')
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


def _decode_font_segment(lines: Iterator[str], strict_mode: bool) -> BdfFont:
    name = None
    point_size = None
    dpi_xy = None
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
            dpi_xy = tokens[1], tokens[2]
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
            if point_size is None or dpi_xy is None:
                raise BdfMissingLine('SIZE')
            if bounding_box_size is None or bounding_box_offset is None:
                raise BdfMissingLine('FONTBOUNDINGBOX')
            if glyphs_count is None:
                raise BdfMissingLine('CHARS')
            if strict_mode and glyphs_count != len(glyphs):
                raise BdfValueIncorrect('CHARS')
            font = BdfFont(
                name,
                point_size,
                dpi_xy,
                bounding_box_size,
                bounding_box_offset,
                properties,
                comments,
            )
            font.add_glyphs(glyphs)
            return font
    raise BdfMissingLine('ENDFONT')


def decode_bdf(lines: Iterator[str], strict_mode: bool = False) -> BdfFont:
    while line_params := _next_word_line(lines):
        word, tail = line_params
        if word == 'STARTFONT':
            font = _decode_font_segment(lines, strict_mode)
            font.spec_version = tail
            return font
    raise BdfMissingLine('STARTFONT')


def decode_bdf_str(text: str, strict_mode: bool = False) -> BdfFont:
    return decode_bdf(iter(text.split('\n')), strict_mode)


def load_bdf(
        file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        strict_mode: bool = False,
) -> BdfFont:
    with open(file_path, 'r', encoding='utf-8') as file:
        return decode_bdf(iter(file.readlines()), strict_mode)
