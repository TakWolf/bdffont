import pytest

from bdffont import BdfProperties
from bdffont.error import BdfXlfdError


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

    with pytest.raises(BdfXlfdError) as info:
        properties.update_by_xlfd('Bitstream-Charter-Medium-R-Normal--12-120-75-75-P-68-ISO8859-1')
    assert info.value.args[0] == "not starts with '-'"

    with pytest.raises(BdfXlfdError) as info:
        properties.update_by_xlfd('-Bitstream-Charter-Medium-R-Normal--12-120-75-75-P-68-ISO8859-1-')
    assert info.value.args[0] == "must be 14 '-'"


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

    with pytest.raises(KeyError) as info:
        properties['abc-def'] = 'abcdef'
    assert info.value.args[0] == 'contains illegal characters'

    properties['NONE_PARAM'] = None
    assert 'NONE_PARAM' not in properties

    with pytest.raises(ValueError) as info:
        properties.foundry = 1
    assert info.value.args[0] == "expected type 'str', got 'int' instead"

    with pytest.raises(ValueError) as info:
        properties.pixel_size = '1'
    assert info.value.args[0] == "expected type 'int', got 'str' instead"

    with pytest.raises(ValueError) as info:
        properties['FLOAT_PARAM'] = 1.2
    assert info.value.args[0] == "expected type 'str | int', got 'float' instead"

    with pytest.raises(ValueError) as info:
        properties.family_name = 'Demo-Pixel'
    assert info.value.args[0] == "contains illegal characters '-'"
