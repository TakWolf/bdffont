import os

import bdffont
from examples import assets_dir


def main():
    font = bdffont.load_bdf(os.path.join(assets_dir, 'unifont-15.0.01.bdf'))
    alphabet = list(font.code_point_to_glyph.items())
    alphabet.sort()
    for code_point, glyph in alphabet:
        print(f'--> {code_point} {glyph.bounding_box}')
        for bitmap_row in glyph.bitmap:
            print(''.join(map(str, bitmap_row)).replace('0', '__').replace('1', '##'))
        print()


if __name__ == '__main__':
    main()
