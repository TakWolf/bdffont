import os.path

import pytest

import bdffont
from bdffont.error import BdfMissingLine, BdfValueIncorrect
from tests import assets_dir


def load_damaged_bdf(bdf_file_name):
    bdf_file_path = os.path.join(assets_dir, 'damaged', bdf_file_name)
    bdffont.load_bdf(bdf_file_path)


def test_not_a_bdf():
    with pytest.raises(Exception) as info:
        load_damaged_bdf('not_a_bdf.bdf')
    assert info.type == BdfMissingLine
    assert info.value.word == 'STARTFONT'


def test_no_line_font():
    with pytest.raises(Exception) as info:
        load_damaged_bdf('no_line_font.bdf')
    assert info.type == BdfMissingLine
    assert info.value.word == 'FONT'


def test_no_line_size():
    with pytest.raises(Exception) as info:
        load_damaged_bdf('no_line_size.bdf')
    assert info.type == BdfMissingLine
    assert info.value.word == 'SIZE'


def test_no_line_fontboundingbox():
    with pytest.raises(Exception) as info:
        load_damaged_bdf('no_line_fontboundingbox.bdf')
    assert info.type == BdfMissingLine
    assert info.value.word == 'FONTBOUNDINGBOX'


def test_no_line_end_properties():
    with pytest.raises(Exception):
        load_damaged_bdf('no_line_end_properties.bdf')


def test_no_line_end_char():
    with pytest.raises(Exception):
        load_damaged_bdf('no_line_end_char.bdf')


def test_no_line_end_font():
    with pytest.raises(Exception) as info:
        load_damaged_bdf('no_line_end_font.bdf')
    assert info.type == BdfMissingLine
    assert info.value.word == 'ENDFONT'


def test_incorrect_properties_count():
    with pytest.raises(Exception) as info:
        load_damaged_bdf('incorrect_properties_count.bdf')
    assert info.type == BdfValueIncorrect
    assert info.value.word == 'STARTPROPERTIES'


def test_incorrect_chars_count():
    with pytest.raises(Exception) as info:
        load_damaged_bdf('incorrect_chars_count.bdf')
    assert info.type == BdfValueIncorrect
    assert info.value.word == 'CHARS'
