import os

import bdffont
from bdffont import BdfFont
from tests import assets_dir, outputs_dir


def load_bdf(file_name: str) -> tuple[BdfFont, str]:
    file_path = os.path.join(assets_dir, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        bdf_text = file.read()
    font = bdffont.decode_bdf_str(bdf_text)
    return font, bdf_text


def test_example():
    font, bdf_text = load_bdf('example.bdf')
    assert font.encode_str() == bdf_text
    assert font.encode_str(optimize_bitmap=True) == bdf_text
    assert font.spec_version == '2.1'
    assert font.name == '-Adobe-Helvetica-Bold-R-Normal--24-240-75-75-P-65-ISO8859-1'
    assert font.point_size == 24
    assert font.dpi_x == 75
    assert font.dpi_y == 75
    assert font.dpi_xy == (75, 75)
    assert font.bounding_box_width == 9
    assert font.bounding_box_height == 24
    assert font.bounding_box_size == (9, 24)
    assert font.bounding_box_offset_x == -2
    assert font.bounding_box_offset_y == -6
    assert font.bounding_box_offset == (-2, -6)
    assert font.bounding_box == (9, 24, -2, -6)
    assert len(font.properties) == 19
    assert font.properties.foundry == 'Adobe'
    assert font.properties['FAMILY'] == 'Helvetica'
    assert font.properties.weight_name == 'Bold'
    assert font.properties.slant == 'R'
    assert font.properties['SETWIDTH_NAME'] == 'Normal'
    assert font.properties['ADD_STYLE_NAME'] == ''
    assert font.properties['PIXEL_SIZE'] == 24
    assert font.properties.point_size == 240
    assert font.properties.resolution_x == 75
    assert font.properties.resolution_y == 75
    assert font.properties['SPACING'] == 'P'
    assert font.properties['AVERAGE_WIDTH'] == 65
    assert font.properties['CHARSET_REGISTRY'] == 'ISO8859'
    assert font.properties['CHARSET_ENCODING'] == '1'
    assert font.properties['MIN_SPACE'] == 4
    assert font.properties.font_ascent == 21
    assert font.properties.font_descent == 7
    assert font.properties.copyright == 'Copyright (c) 1987 Adobe Systems, Inc.'
    assert font.properties.notice == 'Helvetica is a registered trademark of Linotype Inc.'
    assert font.get_glyphs_count() == 2
    glyph = font.get_glyph(39)
    assert glyph.name == 'quoteright'
    assert glyph.code_point == 39
    assert glyph.scalable_width_x == 223
    assert glyph.scalable_width_y == 0
    assert glyph.scalable_width == (223, 0)
    assert glyph.device_width_x == 5
    assert glyph.device_width_y == 0
    assert glyph.device_width == (5, 0)
    assert glyph.bounding_box_width == 4
    assert glyph.bounding_box_height == 6
    assert glyph.bounding_box_size == (4, 6)
    assert glyph.bounding_box_offset_x == 2
    assert glyph.bounding_box_offset_y == 12
    assert glyph.bounding_box_offset == (2, 12)
    assert glyph.bounding_box == (4, 6, 2, 12)
    assert len(glyph.bitmap) == 6
    glyph_data = [
        '_###',
        '_###',
        '_###',
        '_##_',
        '###_',
        '##__',
    ]
    for i, bitmap_row in enumerate(glyph.bitmap):
        assert ''.join(map(str, bitmap_row)).replace('0', '_').replace('1', '#') == glyph_data[i]
    font.save(os.path.join(outputs_dir, 'example-output.bdf'), optimize_bitmap=True)


def test_unifont():
    font = load_bdf('unifont-15.0.01.bdf')[0]
    font.save(os.path.join(outputs_dir, 'unifont-output.bdf'), optimize_bitmap=True)


def test_galmuri9():
    font = load_bdf('galmuri9.bdf')[0]
    font.save(os.path.join(outputs_dir, 'galmuri9-output.bdf'), optimize_bitmap=True)
