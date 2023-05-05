import os

import bdffont
from tests import assets_dir, outputs_dir


def load_bdf(bdf_file_name):
    bdf_file_path = os.path.join(assets_dir, bdf_file_name)
    with open(bdf_file_path, 'r', encoding='utf-8') as file:
        bdf_text = file.read()
    font = bdffont.decode_bdf_str(bdf_text)
    return font, bdf_text


def test_example():
    font, bdf_text = load_bdf('example.bdf')
    assert font.encode_str() == bdf_text
    assert font.name == '-Adobe-Helvetica-Bold-R-Normal--24-240-75-75-P-65-ISO8859-1'
    assert font.size == (24, 75, 75)
    assert font.bounding_box == (9, 24, -2, -6)
    assert len(font.properties) == 19
    assert font.properties.get_font_ascent() == 21
    assert font.properties.get_font_descent() == 7
    assert font.properties.get_copyright() == 'Copyright (c) 1987 Adobe Systems, Inc.'
    assert font.properties.get_notice() == 'Helvetica is a registered trademark of Linotype Inc.'
    assert len(font.code_point_to_glyph) == 2
    glyph = font.get_glyph(39)
    assert glyph.name == 'quoteright'
    assert glyph.code_point == 39
    assert glyph.s_width == (223, 0)
    assert glyph.d_width == (5, 0)
    assert glyph.bbx == (4, 6, 2, 12)
    assert len(glyph.bitmap) == 6
    font.save(os.path.join(outputs_dir, 'example-output.bdf'))


def test_unifont():
    font = load_bdf('unifont-15.0.01.bdf')[0]
    font = bdffont.decode_bdf(iter(font.encode()))
    font.save(os.path.join(outputs_dir, 'unifont-output.bdf'))
