from pathlib import Path

from bdffont import BdfFont


def test_demo(assets_dir: Path):
    data = assets_dir.joinpath('demo.bdf').read_text('utf-8')
    font = BdfFont.parse(data)
    assert font.dump_to_string() == data
    assert font.spec_version == '2.1'
    assert font.name == '-Adobe-Helvetica-Bold-R-Normal--24-240-75-75-P-65-ISO8859-1'
    assert font.point_size == 24
    assert font.resolution_x == 75
    assert font.resolution_y == 75
    assert font.resolution == (75, 75)
    assert font.width == 9
    assert font.height == 24
    assert font.dimensions == (9, 24)
    assert font.offset_x == -2
    assert font.offset_y == -6
    assert font.offset == (-2, -6)
    assert font.bounding_box == (9, 24, -2, -6)
    assert len(font.properties) == 19
    assert font.properties.foundry == 'Adobe'
    assert font.properties.family_name == 'Helvetica'
    assert font.properties.weight_name == 'Bold'
    assert font.properties.slant == 'R'
    assert font.properties.setwidth_name == 'Normal'
    assert font.properties.add_style_name == ''
    assert font.properties.pixel_size == 24
    assert font.properties.point_size == 240
    assert font.properties.resolution_x == 75
    assert font.properties.resolution_y == 75
    assert font.properties.spacing == 'P'
    assert font.properties.average_width == 65
    assert font.properties.charset_registry == 'ISO8859'
    assert font.properties.charset_encoding == '1'
    assert font.properties['MIN_SPACE'] == 4
    assert font.properties.font_ascent == 21
    assert font.properties.font_descent == 7
    assert font.properties.copyright == 'Copyright (c) 1987 Adobe Systems, Inc.'
    assert font.properties.notice == 'Helvetica is a registered trademark of Linotype Inc.'
    assert len(font.glyphs) == 2
    glyph = {glyph.encoding: glyph for glyph in font.glyphs}[39]
    assert glyph.name == 'quoteright'
    assert glyph.encoding == 39
    assert glyph.scalable_width_x == 223
    assert glyph.scalable_width_y == 0
    assert glyph.scalable_width == (223, 0)
    assert glyph.device_width_x == 5
    assert glyph.device_width_y == 0
    assert glyph.device_width == (5, 0)
    assert glyph.width == 4
    assert glyph.height == 6
    assert glyph.dimensions == (4, 6)
    assert glyph.offset_x == 2
    assert glyph.offset_y == 12
    assert glyph.offset == (2, 12)
    assert glyph.bounding_box == (4, 6, 2, 12)
    assert len(glyph.bitmap) == 6
    glyph_bitmap = [
        [0, 1, 1, 1],
        [0, 1, 1, 1],
        [0, 1, 1, 1],
        [0, 1, 1, 0],
        [1, 1, 1, 0],
        [1, 1, 0, 0],
    ]
    assert glyph.bitmap == glyph_bitmap
