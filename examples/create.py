import os
import shutil

from bdffont import BdfFont, BdfGlyph, xlfd
from examples import build_dir


def main():
    outputs_dir = os.path.join(build_dir, 'create')
    if os.path.exists(outputs_dir):
        shutil.rmtree(outputs_dir)
    os.makedirs(outputs_dir)

    font = BdfFont(
        point_size=16,
        resolution_xy=(75, 75),
        bounding_box_size=(16, 16),
        bounding_box_offset=(0, -2),
    )

    font.add_glyph(BdfGlyph(
        name='A',
        code_point=ord('A'),
        scalable_width=(500, 0),
        device_width=(8, 0),
        bounding_box_size=(8, 16),
        bounding_box_offset=(0, -2),
        bitmap=[
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
    ))

    font.properties.foundry = 'Pixel Font Studio'
    font.properties.family_name = 'Demo Pixel'
    font.properties.add_style_name = xlfd.AddStyleName.SANS_SERIF
    font.properties.pixel_size = 16
    font.properties.point_size = 160
    font.properties.spacing = xlfd.Spacing.PROPORTIONAL
    font.properties.average_width = round(sum([glyph.device_width_x * 10 for glyph in font.code_point_to_glyph.values()]) / font.get_glyphs_count())
    font.setup_missing_xlfd_properties()

    font.properties.default_char = -1
    font.properties.font_ascent = 14
    font.properties.font_descent = 2
    font.properties.x_height = 5
    font.properties.cap_height = 7

    font.properties.font_version = '1.0.0'
    font.properties.copyright = 'Copyright (c) TakWolf'

    font.generate_xlfd_font_name()

    font.save(os.path.join(outputs_dir, 'my-font.bdf'), optimize_bitmap=True)


if __name__ == '__main__':
    main()
