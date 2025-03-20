from pathlib import Path

import pytest

from bdffont import BdfFont, BdfProperties, BdfGlyph
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
    font.resolution = (75, 75)

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

    with pytest.raises(BdfXlfdError):
        font.update_by_name_as_xlfd()

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


def test_properties_1():
    properties = BdfProperties({
        'PARAM_1': 1,
        'param_2': '2',
        'PARAM_3': None,
    }, comments=[
        'This is a comment.',
        'This is a comment, too.',
    ])

    assert len(properties) == 2
    assert properties['param_1'] == 1
    assert properties['PARAM_2'] == '2'
    assert len(properties.comments) == 2
    assert properties.comments[0] == 'This is a comment.'
    assert properties.comments[1] == 'This is a comment, too.'


def test_properties_2():
    properties = BdfProperties()

    properties.foundry = 'TakWolf Studio'
    assert properties.foundry == 'TakWolf Studio'
    assert properties['FOUNDRY'] == 'TakWolf Studio'

    properties.family_name = 'Demo Pixel'
    assert properties.family_name == 'Demo Pixel'
    assert properties['FAMILY_NAME'] == 'Demo Pixel'

    properties.weight_name = 'Medium'
    assert properties.weight_name == 'Medium'
    assert properties['WEIGHT_NAME'] == 'Medium'

    properties.slant = 'R'
    assert properties.slant == 'R'
    assert properties['SLANT'] == 'R'

    properties.setwidth_name = 'Normal'
    assert properties.setwidth_name == 'Normal'
    assert properties['SETWIDTH_NAME'] == 'Normal'

    properties.add_style_name = 'Sans Serif'
    assert properties.add_style_name == 'Sans Serif'
    assert properties['ADD_STYLE_NAME'] == 'Sans Serif'

    properties.pixel_size = 16
    assert properties.pixel_size == 16
    assert properties['PIXEL_SIZE'] == 16

    properties.point_size = 160
    assert properties.point_size == 160
    assert properties['POINT_SIZE'] == 160

    properties.resolution_x = 75
    assert properties.resolution_x == 75
    assert properties['RESOLUTION_X'] == 75

    properties.resolution_y = 240
    assert properties.resolution_y == 240
    assert properties['RESOLUTION_Y'] == 240

    properties.spacing = 'M'
    assert properties.spacing == 'M'
    assert properties['SPACING'] == 'M'

    properties.average_width = 85
    assert properties.average_width == 85
    assert properties['AVERAGE_WIDTH'] == 85

    properties.charset_registry = 'ISO8859'
    assert properties.charset_registry == 'ISO8859'
    assert properties['CHARSET_REGISTRY'] == 'ISO8859'

    properties.charset_encoding = '1'
    assert properties.charset_encoding == '1'
    assert properties['CHARSET_ENCODING'] == '1'

    assert len(properties) == 14
    assert properties.to_xlfd() == '-TakWolf Studio-Demo Pixel-Medium-R-Normal-Sans Serif-16-160-75-240-M-85-ISO8859-1'


def test_properties_3():
    properties = BdfProperties()

    font_name = '-Bitstream-Charter-Medium-R-Normal--12-120-75-75-P-68-ISO8859-1'
    properties.update_by_xlfd(font_name)
    assert properties.foundry == 'Bitstream'
    assert properties.family_name == 'Charter'
    assert properties.weight_name == 'Medium'
    assert properties.slant == 'R'
    assert properties.setwidth_name == 'Normal'
    assert properties.add_style_name is None
    assert properties.pixel_size == 12
    assert properties.point_size == 120
    assert properties.resolution_x == 75
    assert properties.resolution_y == 75
    assert properties.spacing == 'P'
    assert properties.average_width == 68
    assert properties.charset_registry == 'ISO8859'
    assert properties.charset_encoding == '1'
    assert properties.to_xlfd() == font_name

    font_name = '--------------'
    properties.update_by_xlfd(font_name)
    assert properties.foundry is None
    assert properties.family_name is None
    assert properties.weight_name is None
    assert properties.slant is None
    assert properties.setwidth_name is None
    assert properties.add_style_name is None
    assert properties.pixel_size is None
    assert properties.point_size is None
    assert properties.resolution_x is None
    assert properties.resolution_y is None
    assert properties.spacing is None
    assert properties.average_width is None
    assert properties.charset_registry is None
    assert properties.charset_encoding is None
    assert properties.to_xlfd() == font_name


def test_properties_4():
    properties = BdfProperties()

    with pytest.raises(BdfXlfdError):
        properties.update_by_xlfd('Bitstream-Charter-Medium-R-Normal--12-120-75-75-P-68-ISO8859-1')

    with pytest.raises(BdfXlfdError):
        properties.update_by_xlfd('-Bitstream-Charter-Medium-R-Normal--12-120-75-75-P-68-ISO8859-1-')


def test_properties_5():
    properties = BdfProperties()

    properties.default_char = -1
    assert properties.default_char == -1
    assert properties['DEFAULT_CHAR'] == -1

    properties.font_ascent = 14
    assert properties.font_ascent == 14
    assert properties['FONT_ASCENT'] == 14

    properties.font_descent = 2
    assert properties.font_descent == 2
    assert properties['FONT_DESCENT'] == 2

    properties.x_height = 5
    assert properties.x_height == 5
    assert properties['X_HEIGHT'] == 5

    properties.cap_height = 8
    assert properties.cap_height == 8
    assert properties['CAP_HEIGHT'] == 8

    assert len(properties) == 5


def test_properties_6():
    properties = BdfProperties()

    properties.font_version = '1.0.0'
    assert properties.font_version == '1.0.0'
    assert properties['FONT_VERSION'] == '1.0.0'

    properties.copyright = 'Copyright (c) TakWolf'
    assert properties.copyright == 'Copyright (c) TakWolf'
    assert properties['COPYRIGHT'] == 'Copyright (c) TakWolf'

    properties.notice = 'This is a notice.'
    assert properties.notice == 'This is a notice.'
    assert properties['NOTICE'] == 'This is a notice.'

    assert len(properties) == 3


def test_properties_7():
    properties = BdfProperties()

    properties['abc'] = 'abc'
    assert properties['ABC'] == 'abc'
    assert properties['abc'] == 'abc'

    with pytest.raises(KeyError):
        properties['abc-def'] = 'abcdef'

    properties['NONE_PARAM'] = None
    assert 'NONE_PARAM' not in properties

    with pytest.raises(ValueError):
        properties.foundry = 1

    with pytest.raises(ValueError):
        properties.pixel_size = '1'

    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        properties['FLOAT_PARAM'] = 1.2

    with pytest.raises(ValueError):
        properties.family_name = 'Demo-Pixel'

    with pytest.raises(ValueError):
        properties['MULTI_LINE'] = 'This is a line.\nThis is another line.'


def test_glyph():
    glyph = BdfGlyph(
        name='A',
        encoding=ord('A'),
        scalable_width=(0, 0),
        device_width=(0, 0),
        bounding_box=(0, 0, 0, 0),
    )

    glyph.scalable_width = 1, 2
    assert glyph.scalable_width == (1, 2)
    assert glyph.scalable_width_x == 1
    assert glyph.scalable_width_y == 2

    glyph.device_width = 3, 4
    assert glyph.device_width == (3, 4)
    assert glyph.device_width_x == 3
    assert glyph.device_width_y == 4

    glyph.dimensions = 5, 6
    assert glyph.dimensions == (5, 6)
    assert glyph.width == 5
    assert glyph.height == 6

    glyph.offset = 7, 8
    assert glyph.offset == (7, 8)
    assert glyph.offset_x == 7
    assert glyph.offset_y == 8

    assert glyph.bounding_box == (5, 6, 7, 8)
    glyph.bounding_box = 9, 10, 11, 12
    assert glyph.bounding_box == (9, 10, 11, 12)
    assert glyph.width == 9
    assert glyph.height == 10
    assert glyph.offset_x == 11
    assert glyph.offset_y == 12


def test_eq(assets_dir: Path):
    file_path = assets_dir.joinpath('demo.bdf')
    font_1 = BdfFont.load(file_path)
    font_2 = BdfFont.load(file_path)
    assert font_1 == font_2
