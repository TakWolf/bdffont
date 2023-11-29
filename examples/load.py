import os
import shutil

from bdffont import BdfFont
from examples import assets_dir, build_dir


def main():
    outputs_dir = os.path.join(build_dir, 'load')
    if os.path.exists(outputs_dir):
        shutil.rmtree(outputs_dir)
    os.makedirs(outputs_dir)

    font = BdfFont.load(os.path.join(assets_dir, 'unifont', 'unifont-15.0.01.bdf'))
    print(f'name: {font.name}')
    print(f'size: {font.point_size}')
    print(f'ascent: {font.properties.font_ascent}')
    print(f'descent: {font.properties.font_descent}')
    for glyph in font.get_glyphs():
        print(f'glyph: {glyph.name} - {glyph.code_point:04X}')
    font.save(os.path.join(outputs_dir, 'unifont-15.0.01.bdf'), optimize_bitmap=True)


if __name__ == '__main__':
    main()
