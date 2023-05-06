import os

import bdffont
from bdffont import BdfGlyph
from examples import assets_dir, outputs_dir


def main():
    font = bdffont.load_bdf(os.path.join(assets_dir, 'example.bdf'))
    font.name = 'my-new-font'
    font.bounding_box_size = 16, 16
    font.bounding_box_offset = 0, -2
    font.properties.font_version = '1.0.0'
    font.properties.font_ascent = 7
    font.properties.font_descent = 2
    font.properties.x_height = 5
    font.properties.cap_height = 7
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
    font.save(os.path.join(outputs_dir, 'example-output.bdf'))


if __name__ == '__main__':
    main()
