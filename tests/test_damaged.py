import os

import pytest

from bdffont import BdfFont
from bdffont.error import BdfParseError, BdfMissingLineError, BdfIllegalWordError, BdfCountError

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _load_damaged_bdf(file_name: str, strict_level: int = 1):
    file_path = os.path.join(project_root_dir, 'assets', 'damaged', file_name)
    BdfFont.load(file_path, strict_level)


def test_not_a_bdf():
    with pytest.raises(BdfMissingLineError) as info:
        _load_damaged_bdf('not_a_bdf.bdf')
    assert info.value.line_num == 1
    assert info.value.word == 'STARTFONT'


def test_not_support_version():
    with pytest.raises(BdfParseError) as info:
        _load_damaged_bdf('not_support_version.bdf')
    assert info.value.line_num == 1


def test_no_line_font():
    with pytest.raises(BdfMissingLineError) as info:
        _load_damaged_bdf('no_line_font.bdf')
    assert info.value.line_num == 1
    assert info.value.word == 'FONT'


def test_no_line_size():
    with pytest.raises(BdfMissingLineError) as info:
        _load_damaged_bdf('no_line_size.bdf')
    assert info.value.line_num == 1
    assert info.value.word == 'SIZE'


def test_no_line_fontboundingbox():
    with pytest.raises(BdfMissingLineError) as info:
        _load_damaged_bdf('no_line_fontboundingbox.bdf')
    assert info.value.line_num == 1
    assert info.value.word == 'FONTBOUNDINGBOX'


def test_no_line_end_properties():
    with pytest.raises(Exception):
        _load_damaged_bdf('no_line_end_properties.bdf')


def test_no_line_chars():
    with pytest.raises(BdfMissingLineError) as info:
        _load_damaged_bdf('no_line_chars.bdf')
    assert info.value.line_num == 1
    assert info.value.word == 'CHARS'


def test_no_line_encoding():
    with pytest.raises(BdfMissingLineError) as info:
        _load_damaged_bdf('no_line_encoding.bdf')
    assert info.value.line_num == 29
    assert info.value.word == 'ENCODING'


def test_no_line_swidth():
    with pytest.raises(BdfMissingLineError) as info:
        _load_damaged_bdf('no_line_swidth.bdf')
    assert info.value.line_num == 29
    assert info.value.word == 'SWIDTH'


def test_no_line_dwidth():
    with pytest.raises(BdfMissingLineError) as info:
        _load_damaged_bdf('no_line_dwidth.bdf')
    assert info.value.line_num == 29
    assert info.value.word == 'DWIDTH'


def test_no_line_bbx():
    with pytest.raises(BdfMissingLineError) as info:
        _load_damaged_bdf('no_line_bbx.bdf')
    assert info.value.line_num == 29
    assert info.value.word == 'BBX'


def test_no_line_end_char():
    with pytest.raises(Exception):
        _load_damaged_bdf('no_line_end_char.bdf')


def test_no_line_end_font():
    with pytest.raises(BdfMissingLineError) as info:
        _load_damaged_bdf('no_line_end_font.bdf')
    assert info.value.line_num == 1
    assert info.value.word == 'ENDFONT'


def test_illegal_word_in_font():
    with pytest.raises(BdfIllegalWordError) as info:
        _load_damaged_bdf('illegal_word_in_font.bdf', strict_level=2)
    assert info.value.line_num == 2
    assert info.value.word == 'ABC'


def test_illegal_word_in_char():
    with pytest.raises(BdfIllegalWordError) as info:
        _load_damaged_bdf('illegal_word_in_char.bdf', strict_level=2)
    assert info.value.line_num == 30
    assert info.value.word == 'DEF'


def test_incorrect_properties_count():
    _load_damaged_bdf('incorrect_properties_count.bdf')
    with pytest.raises(BdfCountError) as info:
        _load_damaged_bdf('incorrect_properties_count.bdf', strict_level=2)
    assert info.value.line_num == 6
    assert info.value.word == 'STARTPROPERTIES'


def test_incorrect_chars_count():
    _load_damaged_bdf('incorrect_chars_count.bdf')
    with pytest.raises(BdfCountError) as info:
        _load_damaged_bdf('incorrect_chars_count.bdf', strict_level=2)
    assert info.value.line_num == 28
    assert info.value.word == 'CHARS'
