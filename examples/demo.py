import os

from bdffont import BdfFont, BdfProperties, BdfGlyph
from examples import outputs_dir


def main():
    font = BdfFont(
        name='my-font',
        point_size=16,
        dpi_xy=(75, 75),
        bounding_box_size=(16, 16),
        bounding_box_offset=(0, -2),
        properties=BdfProperties({
            'PARAM_1': 1,
            'PARAM_2': '2',
        }),
        comments=[
            'This is a comment.',
            'This is a comment, too.',
        ],
    )
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
    font.save(os.path.join(outputs_dir, 'my-font.bdf'))


if __name__ == '__main__':
    main()
