import os
import shutil

import bdffont
from examples import path_define


def main():
    if os.path.exists(path_define.build_dir):
        shutil.rmtree(path_define.build_dir)
    os.makedirs(path_define.build_dir)

    font = bdffont.load_bdf(os.path.join(path_define.assets_dir, 'unifont-15.0.01.bdf'))
    alphabet = list(font.code_point_to_glyph.items())
    alphabet.sort()
    for code_point, glyph in alphabet:
        print(f"---> {chr(code_point)} {code_point:04X}")
        for bitmap_row in glyph.bitmap:
            print(''.join(map(str, bitmap_row)).replace('0', '  ').replace('1', '##'))
    font.save(os.path.join(path_define.build_dir, 'unifont-output.bdf'))


if __name__ == '__main__':
    main()
