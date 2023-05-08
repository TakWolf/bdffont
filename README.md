# BdfFont

[![PyPI](https://img.shields.io/pypi/v/bdffont)](https://pypi.org/project/bdffont/)

BdfFont is a library for manipulating [`.bdf` format fonts](https://en.wikipedia.org/wiki/Glyph_Bitmap_Distribution_Format), written in Python.

## Installation

```commandline
pip install bdffont
```

## Usage

```python
import os

from bdffont import BdfFont, BdfProperties, BdfGlyph
from examples import outputs_dir


def main():
    font = BdfFont(
        name='my-font',
        point_size=16,
        dpi_xy=(75, 75),
        bounding_box_size=(16, 16),
        bounding_box_offset=(0, -2),
        properties=BdfProperties({
            'PARAM_1': 1,
            'PARAM_2': '2',
        }),
        comments=[
            'This is a comment.',
            'This is a comment, too.',
        ],
    )
    font.properties.font_version = '1.0.0'
    font.properties.font_ascent = 7
    font.properties.font_descent = 2
    font.properties.x_height = 5
    font.properties.cap_height = 7
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
    font.save(os.path.join(outputs_dir, 'my-font.bdf'), optimize_bitmap=True)


if __name__ == '__main__':
    main()
```

## References

- [X11 - Bitmap Distribution Format - Version 2.1](https://www.x.org/docs/BDF/bdf.pdf)
- [Adobe - Glyph Bitmap Distribution Format (BDF) Specification - Version 2.2](https://adobe-type-tools.github.io/font-tech-notes/pdfs/5005.BDF_Spec.pdf)

## License

Under the [MIT license](LICENSE).
