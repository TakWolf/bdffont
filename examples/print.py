import os

from bdffont import BdfFont
from examples import assets_dir


def _print_bdf(file_name: str):
    font = BdfFont.load(os.path.join(assets_dir, file_name))
    print(f'##### {file_name}')
    for glyph in font.get_glyphs():
        print(f'-> U+{glyph.code_point:04X} {chr(glyph.code_point)} {glyph.bounding_box}')
        for bitmap_row in glyph.bitmap:
            print(''.join(map(str, bitmap_row)).replace('0', '__').replace('1', '**'))
        print()


def main():
    _print_bdf('unifont/unifont-15.0.01.bdf')
    _print_bdf('galmuri/galmuri9.bdf')
    _print_bdf('misaki/misaki_gothic.bdf')
    _print_bdf('misaki/misaki_gothic_2nd.bdf')
    _print_bdf('misaki/misaki_mincho.bdf')


if __name__ == '__main__':
    main()
