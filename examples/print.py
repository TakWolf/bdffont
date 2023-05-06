import os

import bdffont
from examples import assets_dir


def print_bdf(file_name: str):
    font = bdffont.load_bdf(os.path.join(assets_dir, file_name))
    alphabet = list(font.code_point_to_glyph.items())
    alphabet.sort()
    print(f'##### {file_name}')
    for code_point, glyph in alphabet:
        print(f'-> {code_point} {glyph.bounding_box}')
        for bitmap_row in glyph.bitmap:
            print(''.join(map(str, bitmap_row)).replace('0', '__').replace('1', '**'))
        print()


def main():
    print_bdf('unifont-15.0.01.bdf')
    print_bdf('galmuri9.bdf')


if __name__ == '__main__':
    main()
