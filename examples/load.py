import shutil

from bdffont import BdfFont
from examples import assets_dir, build_dir


def main():
    outputs_dir = build_dir.joinpath('load')
    if outputs_dir.exists():
        shutil.rmtree(outputs_dir)
    outputs_dir.mkdir(parents=True)

    font = BdfFont.load(assets_dir.joinpath('unifont', 'unifont-16.0.02.bdf'))
    print(f'name: {font.name}')
    print(f'size: {font.point_size}')
    print(f'ascent: {font.properties.font_ascent}')
    print(f'descent: {font.properties.font_descent}')
    print()
    for glyph in font.glyphs:
        print(f'char: {chr(glyph.encoding)} ({glyph.encoding:04X})')
        print(f'glyph_name: {glyph.name}')
        print(f'advance_width: {glyph.device_width_x}')
        print(f'dimensions: {glyph.dimensions}')
        print(f'origin: {glyph.origin}')
        for bitmap_row in glyph.bitmap:
            text = ''.join('  ' if alpha == 0 else '██' for alpha in bitmap_row)
            print(f'{text}*')
        print()
    font.save(outputs_dir.joinpath('unifont-16.0.02.bdf'))


if __name__ == '__main__':
    main()
