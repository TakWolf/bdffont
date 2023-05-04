import re

from bdffont import common
from bdffont.font import BdfFont
from bdffont.properties import BdfProperties
from bdffont.glyph import BdfGlyph


def _decode_word_line(line: str) -> (str, str):
    tokens = re.split(r" +", line, 1)
    word = tokens[0]
    if len(tokens) >= 2:
        tail = tokens[1]
    else:
        tail = None
    return word, tail


def _decode_tail_to_ints(tail: str) -> list[int]:
    tokens = re.split(r" +", tail)
    ints = [int(token) for token in tokens]
    return ints


def _decode_properties_value(tail: str) -> str | int:
    if tail.startswith('"') and tail.endswith('"'):
        value = tail.removeprefix('"').removesuffix('"')
    else:
        value = int(tail)
    return value


def _decode_properties_segment(lines, count: int) -> BdfProperties:
    properties = BdfProperties()
    while (line := next(lines, None).strip()) is not None:
        word, tail = _decode_word_line(line)
        if word == 'ENDPROPERTIES':
            if count != len(properties):
                common.raise_word_value_incorrect_exception('STARTPROPERTIES')
            return properties
        elif word == 'COMMENT':
            properties.comments.append(tail)
        else:
            properties[word] = _decode_properties_value(tail)
    common.raise_word_line_not_closeed('STARTPROPERTIES', 'ENDPROPERTIES')


def _decode_bitmap_segment(lines, comments) -> list[list[int]]:
    bitmap = []
    while (line := next(lines, None).strip()) is not None:
        word, tail = _decode_word_line(line)
        if word == 'ENDCHAR':
            return bitmap
        elif word == 'COMMENT':
            comments.append(tail)
        elif word != '':
            bitmap.append([int(c) for c in bin(int('1' + line, 16))[3:]])
    common.raise_word_line_not_closeed('STARTCHAR', 'ENDCHAR')


def _decode_glyph_segment(lines, name: str) -> BdfGlyph:
    code_point = None
    s_width = None
    d_width = None
    bbx = None
    bitmap = None
    comments = []
    while (line := next(lines, None).strip()) is not None:
        word, tail = _decode_word_line(line)
        if word == 'ENCODING':
            code_point = int(tail)
        elif word == 'SWIDTH':
            tokens = _decode_tail_to_ints(tail)
            s_width = tokens[0], tokens[1]
        elif word == 'DWIDTH':
            tokens = _decode_tail_to_ints(tail)
            d_width = tokens[0], tokens[1]
        elif word == 'BBX':
            tokens = _decode_tail_to_ints(tail)
            bbx = tokens[0], tokens[1], tokens[2], tokens[3]
        elif word == 'COMMENT':
            comments.append(tail)
        elif word == 'BITMAP' or word == 'ENDCHAR':
            if word == 'BITMAP':
                bitmap = _decode_bitmap_segment(lines, comments)
            if code_point is None:
                common.raise_missing_word_line_exception('ENCODING')
            if s_width is None:
                common.raise_missing_word_line_exception('SWIDTH')
            if d_width is None:
                common.raise_missing_word_line_exception('DWIDTH')
            if bbx is None:
                common.raise_missing_word_line_exception('BBX')
            return BdfGlyph(name, code_point, s_width, d_width, bbx, bitmap, comments)
    common.raise_word_line_not_closeed('STARTCHAR', 'ENDCHAR')


def _decode_font_segment(lines) -> BdfFont:
    name = None
    size = None
    bounding_box = None
    properties = None
    glyph_count = None
    glyphs = []
    alphabet = set()
    comments = []
    while (line := next(lines, None).strip()) is not None:
        word, tail = _decode_word_line(line)
        if word == 'FONT':
            name = tail
        elif word == 'SIZE':
            tokens = _decode_tail_to_ints(tail)
            size = tokens[0], tokens[1], tokens[2]
        elif word == 'FONTBOUNDINGBOX':
            tokens = _decode_tail_to_ints(tail)
            bounding_box = tokens[0], tokens[1], tokens[2], tokens[3]
        elif word == 'STARTPROPERTIES':
            properties = _decode_properties_segment(lines, int(tail))
        elif word == 'CHARS':
            glyph_count = int(tail)
        elif word == 'STARTCHAR':
            glyph = _decode_glyph_segment(lines, tail)
            if glyph.code_point in alphabet:
                common.raise_glyph_already_exists_exception(glyph.code_point)
            glyphs.append(glyph)
            alphabet.add(glyph.code_point)
        elif word == 'COMMENT':
            comments.append(tail)
        elif word == 'ENDFONT':
            if name is None:
                common.raise_missing_word_line_exception('FONT')
            if size is None:
                common.raise_missing_word_line_exception('SIZE')
            if bounding_box is None:
                common.raise_missing_word_line_exception('FONTBOUNDINGBOX')
            if glyph_count is None:
                common.raise_missing_word_line_exception('CHARS')
            if glyph_count != len(glyphs) or glyph_count != len(alphabet):
                common.raise_word_value_incorrect_exception('CHARS')
            return BdfFont(name, size, bounding_box, properties, glyphs, comments)
    common.raise_word_line_not_closeed('STARTFONT', 'ENDFONT')


def decode_bdf(text) -> BdfFont:
    lines = iter(text.split('\n'))
    while (line := next(lines, None).strip()) is not None:
        word, tail = _decode_word_line(line)
        if word == 'STARTFONT':
            font = _decode_font_segment(lines)
            font.spec_version = tail
            return font
    common.raise_missing_word_line_exception('STARTFONT')


def load_bdf(file_path) -> BdfFont:
    with open(file_path, 'r', encoding='utf-8') as file:
        return decode_bdf(file.read())
