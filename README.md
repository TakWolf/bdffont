# BdfFont

[![PyPI](https://img.shields.io/pypi/v/bdffont)](https://pypi.org/project/bdffont/)

BdfFont is a library for manipulating [`.bdf` format fonts](https://en.wikipedia.org/wiki/Glyph_Bitmap_Distribution_Format), written in Python.

## Installation

```commandline
pip install bdffont
```

## Usage

```python
import bdffont
from bdffont import BdfGlyph

font = bdffont.load_bdf('assets/example.bdf')
font.properties.set_font_version('1.0.0')
font.properties.set_font_ascent(7)
font.properties.set_font_descent(2)
font.properties.set_x_height(5)
font.properties.set_cap_height(7)
font.add_glyph(BdfGlyph(
    name='A',
    code_point=ord('A'),
    s_width=(500, 0),
    d_width=(8, 0),
    bbx=(8, 16, 0, -2),
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
font.save('build/example.bdf')
```

## References

- [X11 - Bitmap Distribution Format - Version 2.1](https://www.x.org/docs/BDF/bdf.pdf)
- [Adobe - Glyph Bitmap Distribution Format (BDF) Specification - Version 2.2](https://adobe-type-tools.github.io/font-tech-notes/pdfs/5005.BDF_Spec.pdf)

## License

Under the [MIT license](LICENSE).
