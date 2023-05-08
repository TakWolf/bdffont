import os

import pytest

import bdffont
from bdffont.error import BdfMissingLine, BdfValueIncorrect
from tests import assets_dir


def load_damaged_bdf(file_name: str, strict_mode: bool = False):
    file_path = os.path.join(assets_dir, 'damaged', file_name)
    bdffont.load_bdf(file_path, strict_mode=strict_mode)


def test_not_a_bdf():
    with pytest.raises(BdfMissingLine) as info:
        load_damaged_bdf('not_a_bdf.bdf')
    assert info.value.word == 'STARTFONT'


def test_no_line_font():
    with pytest.raises(BdfMissingLine) as info:
        load_damaged_bdf('no_line_font.bdf')
    assert info.value.word == 'FONT'


def test_no_line_size():
    with pytest.raises(BdfMissingLine) as info:
        load_damaged_bdf('no_line_size.bdf')
    assert info.value.word == 'SIZE'


def test_no_line_fontboundingbox():
    with pytest.raises(BdfMissingLine) as info:
        load_damaged_bdf('no_line_fontboundingbox.bdf')
    assert info.value.word == 'FONTBOUNDINGBOX'


def test_no_line_end_properties():
    with pytest.raises(Exception):
        load_damaged_bdf('no_line_end_properties.bdf')


def test_no_line_chars():
    with pytest.raises(BdfMissingLine) as info:
        load_damaged_bdf('no_line_chars.bdf')
    assert info.value.word == 'CHARS'


def test_no_line_encoding():
    with pytest.raises(BdfMissingLine) as info:
        load_damaged_bdf('no_line_encoding.bdf')
    assert info.value.word == 'ENCODING'


def test_no_line_swidth():
    with pytest.raises(BdfMissingLine) as info:
        load_damaged_bdf('no_line_swidth.bdf')
    assert info.value.word == 'SWIDTH'


def test_no_line_dwidth():
    with pytest.raises(BdfMissingLine) as info:
        load_damaged_bdf('no_line_dwidth.bdf')
    assert info.value.word == 'DWIDTH'


def test_no_line_bbx():
    with pytest.raises(BdfMissingLine) as info:
        load_damaged_bdf('no_line_bbx.bdf')
    assert info.value.word == 'BBX'


def test_no_line_end_char():
    with pytest.raises(Exception):
        load_damaged_bdf('no_line_end_char.bdf')


def test_no_line_end_font():
    with pytest.raises(BdfMissingLine) as info:
        load_damaged_bdf('no_line_end_font.bdf')
    assert info.value.word == 'ENDFONT'


def test_incorrect_properties_count():
    load_damaged_bdf('incorrect_properties_count.bdf')
    with pytest.raises(BdfValueIncorrect) as info:
        load_damaged_bdf('incorrect_properties_count.bdf', strict_mode=True)
    assert info.value.word == 'STARTPROPERTIES'


def test_incorrect_chars_count():
    load_damaged_bdf('incorrect_chars_count.bdf')
    with pytest.raises(BdfValueIncorrect) as info:
        load_damaged_bdf('incorrect_chars_count.bdf', strict_mode=True)
    assert info.value.word == 'CHARS'
