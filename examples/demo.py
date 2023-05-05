import os

import bdffont
from examples import assets_dir, build_dir


def main():
    font = bdffont.load_bdf(os.path.join(assets_dir, 'unifont-15.0.01.bdf'))
    alphabet = list(font.code_point_to_glyph.items())
    alphabet.sort()
    for code_point, glyph in alphabet:
        print(f"---> {chr(code_point)} {code_point:04X}")
        for bitmap_row in glyph.bitmap:
            print(''.join(map(str, bitmap_row)).replace('0', '  ').replace('1', '##'))
    font.save(os.path.join(build_dir, 'unifont-output.bdf'))


if __name__ == '__main__':
    main()
