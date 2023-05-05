import os
import re
from typing import Iterator

from bdffont.font import BdfFont
from bdffont.properties import BdfProperties
from bdffont.glyph import BdfGlyph
from bdffont.error import BdfGlyphExists, BdfMissingLine, BdfValueIncorrect


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


def _decode_properties_segment(lines: Iterator[str], count: int) -> BdfProperties:
    properties = BdfProperties()
    while line_params := _next_word_line(lines):
        word, tail = line_params
        if word == 'ENDPROPERTIES':
            if count != len(properties):
                raise BdfValueIncorrect('STARTPROPERTIES')
            return properties
        elif word == 'COMMENT':
            properties.comments.append(tail)
        else:
            properties[word] = _convert_tail_to_properties_value(tail)
    raise BdfMissingLine('ENDPROPERTIES')


def _decode_bitmap_segment(lines: Iterator[str], comments: list[str]) -> list[list[int]]:
    bitmap = []
    while line_params := _next_word_line(lines):
        word, tail = line_params
        if word == 'ENDCHAR':
            return bitmap
        elif word == 'COMMENT':
            comments.append(tail)
        elif word != '':
            bin_format = '{:0' + str(len(word) * 4) + 'b}'
            bitmap.append([int(c) for c in bin_format.format(int(word, 16))])
    raise BdfMissingLine('ENDCHAR')


def _decode_glyph_segment(lines: Iterator[str], name: str) -> BdfGlyph:
    code_point = None
    scalable_width = None
    device_width = None
    bounding_box = None
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
            bounding_box = tokens[0], tokens[1], tokens[2], tokens[3]
        elif word == 'COMMENT':
            comments.append(tail)
        elif word == 'BITMAP' or word == 'ENDCHAR':
            if word == 'BITMAP':
                bitmap = _decode_bitmap_segment(lines, comments)
            if code_point is None:
                raise BdfMissingLine('ENCODING')
            if scalable_width is None:
                raise BdfMissingLine('SWIDTH')
            if device_width is None:
                raise BdfMissingLine('DWIDTH')
            if bounding_box is None:
                raise BdfMissingLine('BBX')
            return BdfGlyph(name, code_point, scalable_width, device_width, bounding_box, bitmap, comments)
    raise BdfMissingLine('ENDCHAR')


def _decode_font_segment(lines: Iterator[str]) -> BdfFont:
    name = None
    size = None
    bounding_box = None
    properties = None
    glyph_count = None
    glyphs = []
    alphabet = set()
    comments = []
    while line_params := _next_word_line(lines):
        word, tail = line_params
        if word == 'FONT':
            name = tail
        elif word == 'SIZE':
            tokens = _convert_tail_to_ints(tail)
            size = tokens[0], tokens[1], tokens[2]
        elif word == 'FONTBOUNDINGBOX':
            tokens = _convert_tail_to_ints(tail)
            bounding_box = tokens[0], tokens[1], tokens[2], tokens[3]
        elif word == 'STARTPROPERTIES':
            properties = _decode_properties_segment(lines, int(tail))
        elif word == 'CHARS':
            glyph_count = int(tail)
        elif word == 'STARTCHAR':
            glyph = _decode_glyph_segment(lines, tail)
            if glyph.code_point in alphabet:
                raise BdfGlyphExists(glyph.code_point)
            glyphs.append(glyph)
            alphabet.add(glyph.code_point)
        elif word == 'COMMENT':
            comments.append(tail)
        elif word == 'ENDFONT':
            if name is None:
                raise BdfMissingLine('FONT')
            if size is None:
                raise BdfMissingLine('SIZE')
            if bounding_box is None:
                raise BdfMissingLine('FONTBOUNDINGBOX')
            if glyph_count is None:
                raise BdfMissingLine('CHARS')
            if glyph_count != len(glyphs) or glyph_count != len(alphabet):
                raise BdfValueIncorrect('CHARS')
            return BdfFont(name, size, bounding_box, properties, glyphs, comments)
    raise BdfMissingLine('ENDFONT')


def decode_bdf(lines: Iterator[str]) -> BdfFont:
    while line_params := _next_word_line(lines):
        word, tail = line_params
        if word == 'STARTFONT':
            font = _decode_font_segment(lines)
            font.spec_version = tail
            return font
    raise BdfMissingLine('STARTFONT')


def decode_bdf_str(text: str) -> BdfFont:
    return decode_bdf(iter(text.split('\n')))


def load_bdf(file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> BdfFont:
    with open(file_path, 'r', encoding='utf-8') as file:
        return decode_bdf(iter(file.readlines()))
