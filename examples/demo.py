import os

import bdffont
from bdffont import BdfGlyph
from examples import assets_dir, outputs_dir


def main():
    font = bdffont.load_bdf(os.path.join(assets_dir, 'example.bdf'))
    font.properties.set_font_version('1.0.0')
    font.properties.set_font_ascent(7)
    font.properties.set_font_descent(2)
    font.properties.set_x_height(5)
    font.properties.set_cap_height(7)
    font.add_glyph(BdfGlyph(
        name='A',
        code_point=ord('A'),
        s_width=(500, 0),
        d_width=(8, 0),
        bbx=(8, 16, 0, -2),
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
