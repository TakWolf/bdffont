from pathlib import Path

import pytest

from bdffont import BdfFont
from bdffont.error import BdfParseError, BdfMissingLineError, BdfIllegalWordError, BdfCountError


def test_not_a_bdf(assets_dir: Path):
    with pytest.raises(BdfMissingLineError) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'not_a_bdf.bdf'))
    assert info.value.word == 'STARTFONT'


def test_not_support_version(assets_dir: Path):
    with pytest.raises(BdfParseError):
        BdfFont.load(assets_dir.joinpath('damaged', 'not_support_version.bdf'))


def test_no_line_font(assets_dir: Path):
    with pytest.raises(BdfMissingLineError) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_font.bdf'))
    assert info.value.word == 'FONT'


def test_no_line_size(assets_dir: Path):
    with pytest.raises(BdfMissingLineError) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_size.bdf'))
    assert info.value.word == 'SIZE'


def test_no_line_fontboundingbox(assets_dir: Path):
    with pytest.raises(BdfMissingLineError) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_fontboundingbox.bdf'))
    assert info.value.word == 'FONTBOUNDINGBOX'


def test_no_line_end_properties(assets_dir: Path):
    with pytest.raises(Exception):
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_end_properties.bdf'))


def test_no_line_chars(assets_dir: Path):
    with pytest.raises(BdfMissingLineError) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_chars.bdf'))
    assert info.value.word == 'CHARS'


def test_no_line_encoding(assets_dir: Path):
    with pytest.raises(BdfMissingLineError) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_encoding.bdf'))
    assert info.value.word == 'ENCODING'


def test_no_line_swidth(assets_dir: Path):
    with pytest.raises(BdfMissingLineError) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_swidth.bdf'))
    assert info.value.word == 'SWIDTH'


def test_no_line_dwidth(assets_dir: Path):
    with pytest.raises(BdfMissingLineError) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_dwidth.bdf'))
    assert info.value.word == 'DWIDTH'


def test_no_line_bbx(assets_dir: Path):
    with pytest.raises(BdfMissingLineError) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_bbx.bdf'))
    assert info.value.word == 'BBX'


def test_no_line_end_char(assets_dir: Path):
    with pytest.raises(Exception):
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_end_char.bdf'))


def test_no_line_end_font(assets_dir: Path):
    with pytest.raises(BdfMissingLineError) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_end_font.bdf'))
    assert info.value.word == 'ENDFONT'


def test_illegal_word_in_font(assets_dir: Path):
    with pytest.raises(BdfIllegalWordError) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'illegal_word_in_font.bdf'))
    assert info.value.word == 'ABC'


def test_illegal_word_in_char(assets_dir: Path):
    with pytest.raises(BdfIllegalWordError) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'illegal_word_in_char.bdf'))
    assert info.value.word == 'DEF'


def test_incorrect_properties_count(assets_dir: Path):
    with pytest.raises(BdfCountError) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'incorrect_properties_count.bdf'))
    assert info.value.word == 'STARTPROPERTIES'


def test_incorrect_chars_count(assets_dir: Path):
    with pytest.raises(BdfCountError) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'incorrect_chars_count.bdf'))
    assert info.value.word == 'CHARS'
