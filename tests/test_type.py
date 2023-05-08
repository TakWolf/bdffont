import pytest

from bdffont import BdfFont, BdfProperties, BdfGlyph
from bdffont.error import BdfGlyphExists, BdfIllegalBitmap, BdfIllegalPropertiesKey, BdfIllegalPropertiesValue


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

    glyph_a = BdfGlyph(
        name='A',
        code_point=ord('A'),
        scalable_width=(500, 0),
        device_width=(3, 0),
        bounding_box_size=(2, 2),
        bounding_box_offset=(0, 0),
        bitmap=[
            [0, 1],
            [1, 0],
        ],
    )
    glyph_b = BdfGlyph(
        name='B',
        code_point=ord('B'),
        scalable_width=(500, 0),
        device_width=(3, 0),
        bounding_box_size=(2, 2),
        bounding_box_offset=(0, 0),
        bitmap=[
            [1, 0],
            [0, 1],
        ],
    )
    font.add_glyph(glyph_a)
    assert font.get_glyphs_count() == 1
    assert font.get_glyph(ord('A')) == glyph_a
    font.add_glyph(glyph_b)
    assert font.get_glyphs_count() == 2
    assert font.get_glyph(ord('B')) == glyph_b

    with pytest.raises(BdfGlyphExists) as info:
        font.add_glyph(glyph_a)
    assert info.value.code_point == ord('A')

    with pytest.raises(BdfGlyphExists) as info:
        font.add_glyphs([glyph_a, glyph_b])
    assert info.value.code_point == ord('A')

    font.set_glyph(glyph_a)
    assert font.get_glyphs_count() == 2
    font.remove_glyph(ord('A'))
    assert font.get_glyphs_count() == 1
    font.remove_glyph(ord('B'))
    assert font.get_glyphs_count() == 0

    font.add_glyph(glyph_b)
    font.add_glyph(glyph_a)
    glyphs = font.get_orderly_glyphs()
    assert glyphs[0] == glyph_a
    assert glyphs[1] == glyph_b


def test_properties():
    properties = BdfProperties({
        'PARAM_1': 1,
        'PARAM_2': '2',
    }, comments=[
        'This is a comment.',
        'This is a comment, too.',
    ])
    assert len(properties) == 2
    assert properties['PARAM_1'] == 1
    assert properties['PARAM_2'] == '2'
    assert len(properties.comments) == 2
    assert properties.comments[0] == 'This is a comment.'
    assert properties.comments[1] == 'This is a comment, too.'

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

    assert len(properties) == 19

    with pytest.raises(BdfIllegalPropertiesKey):
        properties['abc'] = 'abc'

    with pytest.raises(BdfIllegalPropertiesKey):
        properties['ABC-DEF'] = 'abcdef'

    with pytest.raises(BdfIllegalPropertiesValue):
        properties['TEST_KEY'] = float(1.2)


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


def test_bitmap():
    glyph = BdfGlyph(
        name='A',
        code_point=ord('A'),
        scalable_width=(0, 0),
        device_width=(0, 0),
        bounding_box_size=(5, 5),
        bounding_box_offset=(0, 0),
        bitmap=[
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    glyph.check_bitmap_validity()

    glyph.bitmap.pop()
    with pytest.raises(BdfIllegalBitmap):
        glyph.check_bitmap_validity()

    glyph.bitmap.append([0, 0, 0, 0, 0, 0])
    with pytest.raises(BdfIllegalBitmap):
        glyph.check_bitmap_validity()

    glyph.bitmap[-1].pop()
    glyph.check_bitmap_validity()

    (width, height), (offset_x, offset_y), bitmap = glyph.get_8bit_aligned_bitmap()
    assert len(bitmap) == height == glyph.bounding_box_height
    for bitmap_row in bitmap:
        assert width == glyph.bounding_box_width
        assert len(bitmap_row) == 8
    assert offset_x == glyph.bounding_box_offset_x
    assert offset_y == glyph.bounding_box_offset_y

    (width, height), (offset_x, offset_y), bitmap = glyph.get_8bit_aligned_bitmap(optimize_bitmap=True)
    assert len(bitmap) == height == 2
    for bitmap_row in bitmap:
        assert width == 3
        assert len(bitmap_row) == 8
    assert offset_x == 1
    assert offset_y == 3
