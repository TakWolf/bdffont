import os

import bdffont
from examples import path_define


def main():
    font = bdffont.load_bdf(os.path.join(path_define.assets_dir, 'unifont-15.0.01.bdf'))
    for code_point, glyph in font.code_point_to_glyph.items():
        print(f"---> {chr(code_point)} {code_point:04X}")
        for bitmap_row in glyph.bitmap:
            print(''.join(map(str, bitmap_row)).replace('0', '  ').replace('1', '##'))


if __name__ == '__main__':
    main()
