# BdfFont

[![Python](https://img.shields.io/badge/python-3.10-brightgreen)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/bdffont)](https://pypi.org/project/bdffont/)

BdfFont is a library for manipulating [Glyph Bitmap Distribution Format (BDF) Fonts](https://en.wikipedia.org/wiki/Glyph_Bitmap_Distribution_Format).

## Installation

```shell
pip install bdffont
```

## Usage

### Create

```python
import shutil

from bdffont import BdfFont, BdfGlyph
from examples import build_dir


def main():
    outputs_dir = build_dir.joinpath('create')
    if outputs_dir.exists():
        shutil.rmtree(outputs_dir)
    outputs_dir.mkdir(parents=True)

    font = BdfFont(
        point_size=16,
        resolution=(75, 75),
        bounding_box=(16, 16, 0, -2),
    )

    font.glyphs.append(BdfGlyph(
        name='A',
        encoding=65,
        scalable_width=(500, 0),
        device_width=(8, 0),
        bounding_box=(8, 16, 0, -2),
        bitmap=[
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
    ))

    font.properties.foundry = 'Pixel Font Studio'
    font.properties.family_name = 'My Font'
    font.properties.weight_name = 'Medium'
    font.properties.slant = 'R'
    font.properties.setwidth_name = 'Normal'
    font.properties.add_style_name = 'Sans Serif'
    font.properties.pixel_size = font.point_size
    font.properties.point_size = font.point_size * 10
    font.properties.resolution_x = font.resolution_x
    font.properties.resolution_y = font.resolution_y
    font.properties.spacing = 'P'
    font.properties.average_width = round(sum([glyph.device_width_x * 10 for glyph in font.glyphs]) / len(font.glyphs))
    font.properties.charset_registry = 'ISO10646'
    font.properties.charset_encoding = '1'
    font.generate_name_as_xlfd()

    font.properties.default_char = -1
    font.properties.font_ascent = 14
    font.properties.font_descent = 2
    font.properties.x_height = 7
    font.properties.cap_height = 10

    font.properties.font_version = '1.0.0'
    font.properties.copyright = 'Copyright (c) TakWolf'

    font.save(outputs_dir.joinpath('my-font.bdf'))


if __name__ == '__main__':
    main()
```

### Load

```python
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
        print(f'offset: {glyph.offset}')
        for bitmap_row in glyph.bitmap:
            text = ''.join('  ' if color == 0 else '██' for color in bitmap_row)
            print(f'{text}*')
        print()
    font.save(outputs_dir.joinpath('unifont-16.0.02.bdf'))


if __name__ == '__main__':
    main()
```

## Test Fonts

- [GNU Unifont Glyphs](https://unifoundry.com/unifont/index.html)
- [美咲フォント / Misaki](https://littlelimit.net/misaki.htm)

## References

- [X11 - Bitmap Distribution Format - Version 2.1](https://www.x.org/docs/BDF/bdf.pdf)
- [Adobe - Glyph Bitmap Distribution Format (BDF) Specification - Version 2.2](https://adobe-type-tools.github.io/font-tech-notes/pdfs/5005.BDF_Spec.pdf)
- [X Logical Font Description Conventions - X Consortium Standard](https://www.x.org/releases/current/doc/xorg-docs/xlfd/xlfd.html)

## License

[MIT License](LICENSE)
