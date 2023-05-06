import pytest

from bdffont import BdfFont, BdfProperties, BdfGlyph
from bdffont.error import BdfIllegalPropertiesKey, BdfIllegalPropertiesValue


def test_font():
    font = BdfFont(
        name='',
        point_size=0,
        dpi_xy=(0, 0),
        bounding_box_size=(0, 0),
        bounding_box_offset=(0, 0),
    )

    font.dpi_xy = 1, 2
    assert font.dpi_xy == (1, 2)
    assert font.dpi_x == 1
    assert font.dpi_y == 2

    font.bounding_box_size = 3, 4
    assert font.bounding_box_size == (3, 4)
    assert font.bounding_box_width == 3
    assert font.bounding_box_height == 4

    font.bounding_box_offset = 5, 6
    assert font.bounding_box_offset == (5, 6)
    assert font.bounding_box_offset_x == 5
    assert font.bounding_box_offset_y == 6

    assert font.bounding_box == (3, 4, 5, 6)
    font.bounding_box = 7, 8, 9, 10
    assert font.bounding_box == (7, 8, 9, 10)
    assert font.bounding_box_width == 7
    assert font.bounding_box_height == 8
    assert font.bounding_box_offset_x == 9
    assert font.bounding_box_offset_y == 10


def test_properties():
    properties = BdfProperties()

    assert properties.default_char is None
    properties.default_char = 1
    assert properties.default_char == 1
    assert 'DEFAULT_CHAR' in properties

    assert properties.font_ascent is None
    properties.font_ascent = 2
    assert properties.font_ascent == 2
    assert 'FONT_ASCENT' in properties

    assert properties.font_descent is None
    properties.font_descent = 3
    assert properties.font_descent == 3
    assert 'FONT_DESCENT' in properties

    assert properties.cap_height is None
    properties.cap_height = 4
    assert properties.cap_height == 4
    assert 'CAP_HEIGHT' in properties

    assert properties.x_height is None
    properties.x_height = 5
    assert properties.x_height == 5
    assert 'X_HEIGHT' in properties

    assert properties.point_size is None
    properties.point_size = 6
    assert properties.point_size == 6
    assert 'POINT_SIZE' in properties

    assert properties.resolution_x is None
    properties.resolution_x = 7
    assert properties.resolution_x == 7
    assert 'RESOLUTION_X' in properties

    assert properties.resolution_y is None
    properties.resolution_y = 8
    assert properties.resolution_y == 8
    assert 'RESOLUTION_Y' in properties

    assert properties.face_name is None
    properties.face_name = 'A'
    assert properties.face_name == 'A'
    assert 'FACE_NAME' in properties

    assert properties.font is None
    properties.font = 'B'
    assert properties.font == 'B'
    assert 'FONT' in properties

    assert properties.font_version is None
    properties.font_version = '1.2.3'
    assert properties.font_version == '1.2.3'
    assert 'FONT_VERSION' in properties

    assert properties.family_name is None
    properties.family_name = 'C'
    assert properties.family_name == 'C'
    assert 'FAMILY_NAME' in properties

    assert properties.slant is None
    properties.slant = 'D'
    assert properties.slant == 'D'
    assert 'SLANT' in properties

    assert properties.weight_name is None
    properties.weight_name = 'E'
    assert properties.weight_name == 'E'
    assert 'WEIGHT_NAME' in properties

    assert properties.foundry is None
    properties.foundry = 'F'
    assert properties.foundry == 'F'
    assert 'FOUNDRY' in properties

    assert properties.copyright is None
    properties.copyright = 'G'
    assert properties.copyright == 'G'
    assert 'COPYRIGHT' in properties

    assert properties.notice is None
    properties.notice = 'H'
    assert properties.notice == 'H'
    assert 'NOTICE' in properties

    assert len(properties) == 17

    with pytest.raises(Exception) as info:
        properties['abc'] = 'def'
    assert info.type == BdfIllegalPropertiesKey

    with pytest.raises(Exception) as info:
        properties['TEST_KEY'] = float(1.2)
    assert info.type == BdfIllegalPropertiesValue


def test_glyph():
    glyph = BdfGlyph(
        name='A',
        code_point=ord('A'),
        scalable_width=(0, 0),
        device_width=(0, 0),
        bounding_box_size=(0, 0),
        bounding_box_offset=(0, 0),
    )

    glyph.scalable_width = 1, 2
    assert glyph.scalable_width == (1, 2)
    assert glyph.scalable_width_x == 1
    assert glyph.scalable_width_y == 2

    glyph.device_width = 3, 4
    assert glyph.device_width == (3, 4)
    assert glyph.device_width_x == 3
    assert glyph.device_width_y == 4

    glyph.bounding_box_size = 5, 6
    assert glyph.bounding_box_size == (5, 6)
    assert glyph.bounding_box_width == 5
    assert glyph.bounding_box_height == 6

    glyph.bounding_box_offset = 7, 8
    assert glyph.bounding_box_offset == (7, 8)
    assert glyph.bounding_box_offset_x == 7
    assert glyph.bounding_box_offset_y == 8

    assert glyph.bounding_box == (5, 6, 7, 8)
    glyph.bounding_box = 9, 10, 11, 12
    assert glyph.bounding_box == (9, 10, 11, 12)
    assert glyph.bounding_box_width == 9
    assert glyph.bounding_box_height == 10
    assert glyph.bounding_box_offset_x == 11
    assert glyph.bounding_box_offset_y == 12
