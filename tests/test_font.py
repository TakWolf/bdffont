from pathlib import Path

import pytest

from bdffont import BdfFont
from bdffont.error import BdfXlfdError


def test_font_1():
    font = BdfFont()

    font.resolution = 1, 2
    assert font.resolution == (1, 2)
    assert font.resolution_x == 1
    assert font.resolution_y == 2

    font.dimensions = 3, 4
    assert font.dimensions == (3, 4)
    assert font.width == 3
    assert font.height == 4

    font.offset = 5, 6
    assert font.offset == (5, 6)
    assert font.offset_x == 5
    assert font.offset_y == 6
    assert font.bounding_box == (3, 4, 5, 6)

    font.bounding_box = 7, 8, 9, 10
    assert font.bounding_box == (7, 8, 9, 10)
    assert font.width == 7
    assert font.height == 8
    assert font.offset_x == 9
    assert font.offset_y == 10


def test_font_2():
    font = BdfFont()

    font.point_size = 16
    font.resolution = 75, 75

    font.properties.foundry = 'TakWolf Studio'
    font.properties.family_name = 'Demo Pixel'
    font.properties.weight_name = 'Medium'
    font.properties.slant = 'R'
    font.properties.setwidth_name = 'Normal'
    font.properties.add_style_name = 'Sans Serif'
    font.properties.pixel_size = font.point_size
    font.properties.point_size = font.point_size * 10
    font.properties.resolution_x = font.resolution_x
    font.properties.resolution_y = font.resolution_y
    font.properties.spacing = 'P'
    font.properties.average_width = 80
    font.properties.charset_registry = 'ISO10646'
    font.properties.charset_encoding = '1'

    font.generate_name_as_xlfd()
    assert font.name == '-TakWolf Studio-Demo Pixel-Medium-R-Normal-Sans Serif-16-160-75-75-P-80-ISO10646-1'


def test_font_3():
    font = BdfFont()

    with pytest.raises(BdfXlfdError) as info:
        font.update_by_name_as_xlfd()
    assert info.value.args[0] == "not starts with '-'"

    font.name = '--------------'
    font.update_by_name_as_xlfd()
    assert font.resolution_x == 0
    assert font.resolution_y == 0
    assert len(font.properties) == 0

    font.name = '-Adobe-Times-Medium-R-Normal--14-100-100-100-P-74-ISO8859-1'
    font.update_by_name_as_xlfd()
    assert font.resolution_x == 100
    assert font.resolution_y == 100
    assert font.properties.foundry == 'Adobe'
    assert font.properties.family_name == 'Times'
    assert font.properties.weight_name == 'Medium'
    assert font.properties.slant == 'R'
    assert font.properties.setwidth_name == 'Normal'
    assert font.properties.add_style_name is None
    assert font.properties.pixel_size == 14
    assert font.properties.point_size == 100
    assert font.properties.resolution_x == 100
    assert font.properties.resolution_y == 100
    assert font.properties.spacing == 'P'
    assert font.properties.average_width == 74
    assert font.properties.charset_registry == 'ISO8859'
    assert font.properties.charset_encoding == '1'


def test_eq(assets_dir: Path):
    file_path = assets_dir.joinpath('demo.bdf')
    font_1 = BdfFont.load(file_path)
    font_2 = BdfFont.load(file_path)
    assert font_1 == font_2
