import pytest

from bdffont import BdfFont, BdfProperties, BdfGlyph
from bdffont.error import BdfPropertiesIllegalKey, BdfPropertiesIllegalValue


def test_font():
    font = BdfFont(
        name='',
        size=(0, 0, 0),
        bounding_box=(0, 0, 0, 0),
    )

    font.point_size = 1
    assert font.point_size == 1
    assert font.size == (1, 0, 0)
    font.xy_dpi = (2, 3)
    assert font.xy_dpi == (2, 3)
    assert font.size == (1, 2, 3)
    font.x_dpi = 4
    assert font.x_dpi == 4
    assert font.size == (1, 4, 3)
    font.y_dpi = 5
    assert font.y_dpi == 5
    assert font.size == (1, 4, 5)

    font.bounding_box_size = (6, 7)
    assert font.bounding_box_size == (6, 7)
    assert font.bounding_box == (6, 7, 0, 0)
    font.bounding_box_width = 8
    assert font.bounding_box_width == 8
    assert font.bounding_box == (8, 7, 0, 0)
    font.bounding_box_height = 9
    assert font.bounding_box_height == 9
    assert font.bounding_box == (8, 9, 0, 0)
    font.bounding_box_origin = (10, 11)
    assert font.bounding_box_origin == (10, 11)
    assert font.bounding_box == (8, 9, 10, 11)
    font.bounding_box_origin_x = 12
    assert font.bounding_box_origin_x == 12
    assert font.bounding_box == (8, 9, 12, 11)
    font.bounding_box_origin_y = 13
    assert font.bounding_box_origin_y == 13
    assert font.bounding_box == (8, 9, 12, 13)


def test_properties():
    properties = BdfProperties()

    properties.default_char = 1
    assert properties.default_char == 1
    assert 'DEFAULT_CHAR' in properties

    properties.font_ascent = 2
    assert properties.font_ascent == 2
    assert 'FONT_ASCENT' in properties

    properties.font_descent = 3
    assert properties.font_descent == 3
    assert 'FONT_DESCENT' in properties

    properties.cap_height = 4
    assert properties.cap_height == 4
    assert 'CAP_HEIGHT' in properties

    properties.x_height = 5
    assert properties.x_height == 5
    assert 'X_HEIGHT' in properties

    properties.point_size = 6
    assert properties.point_size == 6
    assert 'POINT_SIZE' in properties

    properties.resolution_x = 7
    assert properties.resolution_x == 7
    assert 'RESOLUTION_X' in properties

    properties.resolution_y = 8
    assert properties.resolution_y == 8
    assert 'RESOLUTION_Y' in properties

    properties.face_name = 'A'
    assert properties.face_name == 'A'
    assert 'FACE_NAME' in properties

    properties.font = 'B'
    assert properties.font == 'B'
    assert 'FONT' in properties

    properties.font_version = '1.2.3'
    assert properties.font_version == '1.2.3'
    assert 'FONT_VERSION' in properties

    properties.family_name = 'C'
    assert properties.family_name == 'C'
    assert 'FAMILY_NAME' in properties

    properties.slant = 'D'
    assert properties.slant == 'D'
    assert 'SLANT' in properties

    properties.weight_name = 'E'
    assert properties.weight_name == 'E'
    assert 'WEIGHT_NAME' in properties

    properties.foundry = 'F'
    assert properties.foundry == 'F'
    assert 'FOUNDRY' in properties

    properties.copyright = 'G'
    assert properties.copyright == 'G'
    assert 'COPYRIGHT' in properties

    properties.notice = 'H'
    assert properties.notice == 'H'
    assert 'NOTICE' in properties

    assert len(properties) == 17

    with pytest.raises(Exception) as info:
        properties['abc'] = 'def'
    assert info.type == BdfPropertiesIllegalKey

    with pytest.raises(Exception) as info:
        properties['TEST_KEY'] = float(1.2)
    assert info.type == BdfPropertiesIllegalValue


def test_glyph():
    glyph = BdfGlyph(
        name='A',
        code_point=ord('A'),
        scalable_width=(0, 0),
        device_width=(0, 0),
        bounding_box=(0, 0, 0, 0),
    )

    glyph.scalable_width_x = 1
    assert glyph.scalable_width_x == 1
    assert glyph.scalable_width == (1, 0)
    glyph.scalable_width_y = 2
    assert glyph.scalable_width_y == 2
    assert glyph.scalable_width == (1, 2)

    glyph.device_width_x = 3
    assert glyph.device_width_x == 3
    assert glyph.device_width == (3, 0)
    glyph.device_width_y = 4
    assert glyph.device_width_y == 4
    assert glyph.device_width == (3, 4)

    glyph.bounding_box_size = (5, 6)
    assert glyph.bounding_box_size == (5, 6)
    assert glyph.bounding_box == (5, 6, 0, 0)
    glyph.bounding_box_width = 7
    assert glyph.bounding_box_width == 7
    assert glyph.bounding_box == (7, 6, 0, 0)
    glyph.bounding_box_height = 8
    assert glyph.bounding_box_height == 8
    assert glyph.bounding_box == (7, 8, 0, 0)
    glyph.bounding_box_origin = (9, 10)
    assert glyph.bounding_box_origin == (9, 10)
    assert glyph.bounding_box == (7, 8, 9, 10)
    glyph.bounding_box_origin_x = 11
    assert glyph.bounding_box_origin_x == 11
    assert glyph.bounding_box == (7, 8, 11, 10)
    glyph.bounding_box_origin_y = 12
    assert glyph.bounding_box_origin_y == 12
    assert glyph.bounding_box == (7, 8, 11, 12)
