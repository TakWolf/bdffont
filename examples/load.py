import os
import shutil

from bdffont import BdfFont
from examples import assets_dir, build_dir


def main():
    outputs_dir = os.path.join(build_dir, 'load')
    if os.path.exists(outputs_dir):
        shutil.rmtree(outputs_dir)
    os.makedirs(outputs_dir)

    font = BdfFont.load(os.path.join(assets_dir, 'unifont', 'unifont-15.1.05.bdf'))
    print(f'name: {font.name}')
    print(f'size: {font.point_size}')
    print(f'ascent: {font.properties.font_ascent}')
    print(f'descent: {font.properties.font_descent}')
    print()
    for glyph in font.glyphs:
        print(f'char: {chr(glyph.code_point)} ({glyph.code_point:04X})')
        print(f'glyph_name: {glyph.name}')
        print(f'advance_width: {glyph.device_width_x}')
        print(f'offset: {glyph.bounding_box_offset}')
        for bitmap_row in glyph.bitmap:
            text = ''.join(map(str, bitmap_row)).replace('0', '  ').replace('1', '██')
            print(f'{text}*')
        print()
    font.save(os.path.join(outputs_dir, 'unifont-15.0.01.bdf'))


if __name__ == '__main__':
    main()
