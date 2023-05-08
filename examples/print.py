import os

import bdffont
from examples import assets_dir


def print_bdf(file_name: str):
    font = bdffont.load_bdf(os.path.join(assets_dir, file_name))
    print(f'##### {file_name}')
    for glyph in font.get_glyphs():
        print(f'-> U+{glyph.code_point:04X} {chr(glyph.code_point)} {glyph.bounding_box}')
        for bitmap_row in glyph.bitmap:
            print(''.join(map(str, bitmap_row)).replace('0', '__').replace('1', '**'))
        print()


def main():
    print_bdf('unifont-15.0.01.bdf')
    print_bdf('galmuri9.bdf')


if __name__ == '__main__':
    main()
