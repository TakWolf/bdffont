# BdfFont

[![Python](https://img.shields.io/badge/python-3.11-brightgreen)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/bdffont)](https://pypi.org/project/bdffont/)

BdfFont is a library for manipulating [`.bdf` format fonts](https://en.wikipedia.org/wiki/Glyph_Bitmap_Distribution_Format).

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

    font = BdfFont.load(os.path.join(assets_dir, 'unifont', 'unifont-15.0.01.bdf'))
    print(f'name: {font.name}')
    print(f'size: {font.point_size}')
    print(f'ascent: {font.properties.font_ascent}')
    print(f'descent: {font.properties.font_descent}')
    for glyph in font.get_glyphs():
        print(f'glyph: {glyph.name} - {glyph.code_point:04X}')
    font.save(os.path.join(outputs_dir, 'unifont-15.0.01.bdf'), optimize_bitmap=True)


if __name__ == '__main__':
    main()
```

### Create

```python
import os
import shutil

from bdffont import BdfFont, BdfGlyph, xlfd
from examples import build_dir


def main():
    outputs_dir = os.path.join(build_dir, 'create')
    if os.path.exists(outputs_dir):
        shutil.rmtree(outputs_dir)
    os.makedirs(outputs_dir)

    font = BdfFont(
        point_size=16,
        resolution_xy=(75, 75),
        bounding_box_size=(16, 16),
        bounding_box_offset=(0, -2),
    )

    font.add_glyph(BdfGlyph(
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
    font.properties.add_style_name = xlfd.AddStyleName.SANS_SERIF
    font.properties.pixel_size = 16
    font.properties.point_size = 160
    font.properties.spacing = xlfd.Spacing.PROPORTIONAL
    font.properties.average_width = round(sum([glyph.device_width_x * 10 for glyph in font.code_point_to_glyph.values()]) / font.get_glyphs_count())
    font.setup_missing_xlfd_properties()

    font.properties.default_char = -1
    font.properties.font_ascent = 14
    font.properties.font_descent = 2
    font.properties.x_height = 5
    font.properties.cap_height = 7

    font.properties.font_version = '1.0.0'
    font.properties.copyright = 'Copyright (c) TakWolf'

    font.generate_xlfd_font_name()

    font.save(os.path.join(outputs_dir, 'my-font.bdf'), optimize_bitmap=True)


if __name__ == '__main__':
    main()
```

## References

- [X11 - Bitmap Distribution Format - Version 2.1](https://www.x.org/docs/BDF/bdf.pdf)
- [Adobe - Glyph Bitmap Distribution Format (BDF) Specification - Version 2.2](https://adobe-type-tools.github.io/font-tech-notes/pdfs/5005.BDF_Spec.pdf)
- [X Logical Font Description Conventions - X Consortium Standard](https://www.x.org/releases/X11R7.6/doc/xorg-docs/specs/XLFD/xlfd.html)
- [ArchWiki - X Logical Font Description](https://wiki.archlinux.org/title/X_Logical_Font_Description)

## License

Under the [MIT license](LICENSE).
