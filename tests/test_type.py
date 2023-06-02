import pytest

from bdffont import BdfFont, BdfProperties, BdfGlyph, xlfd
from bdffont.error import BdfException, BdfGlyphExists, BdfIllegalBitmap, BdfIllegalPropertiesKey, BdfIllegalPropertiesValue, BdfIllegalXlfdFontName


def test_font():
    font = BdfFont()

    font.resolution_xy = 1, 2
    assert font.resolution_xy == (1, 2)
    assert font.resolution_x == 1
    assert font.resolution_y == 2

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

    font = BdfFont()

    font.point_size = 16
    font.resolution_xy = (75, 75)
    font.properties.foundry = 'TakWolf Studio'
    font.properties.family_name = 'Demo Pixel'
    font.properties.add_style_name = xlfd.AddStyleName.SANS_SERIF
    font.properties.pixel_size = 16
    font.properties.point_size = 160
    font.properties.spacing = xlfd.Spacing.PROPORTIONAL
    font.properties.average_width = 80
    font.setup_missing_xlfd_properties()
    assert font.properties.weight_name == 'Medium'
    assert font.properties.slant == 'R'
    assert font.properties.setwidth_name == 'Normal'
    assert font.properties.resolution_x == 75
    assert font.properties.resolution_y == 75
    assert font.properties.charset_registry == 'ISO10646'
    assert font.properties.charset_encoding == '1'
    font.generate_xlfd_font_name()
    assert font.name == '-TakWolf Studio-Demo Pixel-Medium-R-Normal-Sans Serif-16-160-75-75-P-80-ISO10646-1'

    font = BdfFont()

    with pytest.raises(BdfException) as info:
        font.update_by_name_as_xlfd_font_name()
    assert info.value.args[0] == "Missing attribute 'name'"
    font.name = '-Adobe-Times-Medium-R-Normal--14-100-100-100-P-74-ISO8859-1'
    font.update_by_name_as_xlfd_font_name()
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

    font = BdfFont()

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
    glyphs = font.get_glyphs()
    assert glyphs[0] == glyph_a
    assert glyphs[1] == glyph_b

    with pytest.raises(BdfException) as info:
        font.encode()
    assert info.value.args[0] == "Missing attribute 'name'"
    font.name = 'my-font'
    font.encode()


def test_properties():
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

    properties.clear()

    properties.foundry = 'TakWolf Studio'
    assert properties.foundry == 'TakWolf Studio'
    assert properties['FOUNDRY'] == 'TakWolf Studio'

    properties.family_name = 'Demo Pixel'
    assert properties.family_name == 'Demo Pixel'
    assert properties['FAMILY_NAME'] == 'Demo Pixel'

    properties.weight_name = xlfd.WeightName.MEDIUM
    assert properties.weight_name == 'Medium'
    assert properties['WEIGHT_NAME'] == 'Medium'

    properties.slant = xlfd.Slant.ROMAN
    assert properties.slant == 'R'
    assert properties['SLANT'] == 'R'

    properties.setwidth_name = xlfd.SetwidthName.NORMAL
    assert properties.setwidth_name == 'Normal'
    assert properties['SETWIDTH_NAME'] == 'Normal'

    properties.add_style_name = xlfd.AddStyleName.SANS_SERIF
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

    properties.spacing = xlfd.Spacing.MONOSPACED
    assert properties.spacing == 'M'
    assert properties['SPACING'] == 'M'

    properties.average_width = 85
    assert properties.average_width == 85
    assert properties['AVERAGE_WIDTH'] == 85

    properties.charset_registry = xlfd.CharsetRegistry.ISO8859
    assert properties.charset_registry == 'ISO8859'
    assert properties['CHARSET_REGISTRY'] == 'ISO8859'

    properties.charset_encoding = '1'
    assert properties.charset_encoding == '1'
    assert properties['CHARSET_ENCODING'] == '1'

    assert len(properties) == 14

    font_name = '-TakWolf Studio-Demo Pixel-Medium-R-Normal-Sans Serif-16-160-75-240-M-85-ISO8859-1'
    assert properties.to_xlfd_font_name() == font_name

    font_name = '-Bitstream-Charter-Medium-R-Normal--12-120-75-75-P-68-ISO8859-1'
    properties.update_by_xlfd_font_name(font_name)
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
    assert properties.to_xlfd_font_name() == font_name

    font_name = '--------------'
    properties.update_by_xlfd_font_name(font_name)
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
    assert properties.to_xlfd_font_name() == font_name

    font_name = 'Bitstream-Charter-Medium-R-Normal--12-120-75-75-P-68-ISO8859-1'
    with pytest.raises(BdfIllegalXlfdFontName) as info:
        properties.update_by_xlfd_font_name(font_name)
    assert info.value.font_name == font_name
    assert info.value.reason == "not starts with '-'"

    font_name = '-Bitstream-Charter-Medium-R-Normal--12-120-75-75-P-68-ISO8859-1-'
    with pytest.raises(BdfIllegalXlfdFontName) as info:
        properties.update_by_xlfd_font_name(font_name)
    assert info.value.font_name == font_name
    assert info.value.reason == "there could only be 14 '-' in the name"

    properties.clear()

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
    properties.clear()

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
    properties.clear()

    properties['abc'] = 'abc'
    assert properties['ABC'] == 'abc'
    assert properties['abc'] == 'abc'

    with pytest.raises(BdfIllegalPropertiesKey) as info:
        properties['abc-def'] = 'abcdef'
    assert info.value.key == 'ABC-DEF'

    properties['NONE_PARAM'] = None
    assert 'NONE_PARAM' not in properties

    with pytest.raises(BdfIllegalPropertiesValue) as info:
        properties.foundry = 1
    assert info.value.key == 'FOUNDRY'
    assert info.value.value == 1

    with pytest.raises(BdfIllegalPropertiesValue) as info:
        properties.pixel_size = '1'
    assert info.value.key == 'PIXEL_SIZE'
    assert info.value.value == '1'

    with pytest.raises(BdfIllegalPropertiesValue) as info:
        # noinspection PyTypeChecker
        properties['FLOAT_PARAM'] = 1.2
    assert info.value.key == 'FLOAT_PARAM'
    assert info.value.value == 1.2

    with pytest.raises(BdfIllegalPropertiesValue) as info:
        properties.family_name = 'Demo-Pixel'
    assert info.value.key == 'FAMILY_NAME'
    assert info.value.value == 'Demo-Pixel'


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
        bounding_box_size=(5, 10),
        bounding_box_offset=(0, 0),
        bitmap=[
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    glyph.check_bitmap_validity()

    glyph.bitmap.pop()
    with pytest.raises(BdfIllegalBitmap) as info:
        glyph.check_bitmap_validity()
    assert info.value.code_point == glyph.code_point

    glyph.bitmap.append([0, 0, 0, 0, 0, 0])
    with pytest.raises(BdfIllegalBitmap) as info:
        glyph.check_bitmap_validity()
    assert info.value.code_point == glyph.code_point

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
    assert offset_y == 8
