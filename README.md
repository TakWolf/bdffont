# BdfFont

[![Python](https://img.shields.io/badge/python-3.10-brightgreen)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/bdffont)](https://pypi.org/project/bdffont/)

BdfFont is a library for manipulating [Glyph Bitmap Distribution Format (BDF) Fonts](https://en.wikipedia.org/wiki/Glyph_Bitmap_Distribution_Format).

## Installation

```shell
pip install bdffont
```

## Usage

### Load

```python
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
```

### Create

```python
import os
import shutil

from bdffont import BdfFont, BdfGlyph
from examples import build_dir


def main():
    outputs_dir = os.path.join(build_dir, 'create')
    if os.path.exists(outputs_dir):
        shutil.rmtree(outputs_dir)
    os.makedirs(outputs_dir)

    font = BdfFont()

    font.point_size = 16
    font.resolution_xy = 75, 75
    font.bounding_box_size = 16, 16
    font.bounding_box_offset = 0, -2

    font.glyphs.append(BdfGlyph(
        name='A',
        code_point=ord('A'),
        scalable_width=(500, 0),
        device_width=(8, 0),
        bounding_box_size=(8, 16),
        bounding_box_offset=(0, -2),
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
    font.properties.family_name = 'Demo Pixel'
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
    font.properties.x_height = 5
    font.properties.cap_height = 7

    font.properties.font_version = '1.0.0'
    font.properties.copyright = 'Copyright (c) TakWolf'

    font.save(os.path.join(outputs_dir, 'my-font.bdf'))


if __name__ == '__main__':
    main()
```

## Test Fonts

- [GNU Unifont Glyphs](https://unifoundry.com/unifont/index.html)
- [Galmuri](https://github.com/quiple/galmuri)
- [美咲フォント / Misaki](https://littlelimit.net/misaki.htm)

## References

- [X11 - Bitmap Distribution Format - Version 2.1](https://www.x.org/docs/BDF/bdf.pdf)
- [Adobe - Glyph Bitmap Distribution Format (BDF) Specification - Version 2.2](https://adobe-type-tools.github.io/font-tech-notes/pdfs/5005.BDF_Spec.pdf)
- [X Logical Font Description Conventions - X Consortium Standard](https://www.x.org/releases/current/doc/xorg-docs/xlfd/xlfd.html)

## License

Under the [MIT license](LICENSE).
