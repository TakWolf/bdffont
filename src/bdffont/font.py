from bdffont import common
from bdffont.properties import BdfProperties
from bdffont.glyph import BdfGlyph


class BdfFont:
    # The BDF Specification version.
    spec_version: str

    # Either the 'X logical font description' or some private font name.
    # https://en.wikipedia.org/wiki/X_logical_font_description
    # Example: -Adobe-Helvetica-Bold-R-Normal--24-240-75-75-P-65-ISO8859-1
    name: str

    # The point size of the characters, the x resolution, and the y resolution of the device for which these characters were intended.
    # Names: point_size, x_dpi, y_dpi
    # Example: 16 75 75
    size: (int, int, int)

    # The width in x, height in y, and the x and y displacement of the lower left corner from the origin. (In pixels.)
    # Names: bounding_box_width, bounding_box_height, bounding_box_origin_x, bounding_box_origin_y
    # Example: 16 16 0 -2
    bounding_box: (int, int, int, int)

    # Some optional extended properties.
    properties: BdfProperties

    # Glyph objects using code point indexing.
    code_point_to_glyph: dict[int, BdfGlyph]

    def __init__(
            self,
            name: str,
            size: (int, int, int),
            bounding_box: (int, int, int, int),
            properties: BdfProperties = None,
            glyphs: list[BdfGlyph] = None,
    ):
        self.spec_version = '2.1'
        self.name = name
        self.size = size
        self.bounding_box = bounding_box
        if properties is None:
            self.properties = BdfProperties()
        else:
            self.properties = properties
        if glyphs is None:
            self.code_point_to_glyph = {}
        else:
            self.code_point_to_glyph = {glyph.code_point: glyph for glyph in glyphs}

    def get_point_size(self) -> int:
        return self.size[0]

    def set_point_size(self, point_size: int):
        self.size[0] = point_size

    def get_xy_dpi(self) -> (int, int):
        return self.size[1], self.size[2]

    def set_xy_dpi(self, x_dpi: int, y_dpi: int):
        self.size[1] = x_dpi
        self.size[2] = y_dpi

    def get_x_dpi(self) -> int:
        return self.size[1]

    def set_x_dpi(self, x_dpi: int):
        self.size[1] = x_dpi

    def get_y_dpi(self) -> int:
        return self.size[2]

    def set_y_dpi(self, y_dpi: int):
        self.size[2] = y_dpi

    def get_bounding_box_size(self) -> (int, int):
        return self.size[0], self.size[1]

    def set_bounding_box_size(self, width: int, height: int):
        self.size[0] = width
        self.size[1] = height

    def get_bounding_box_width(self) -> int:
        return self.size[0]

    def set_bounding_box_width(self, width: int):
        self.size[0] = width

    def get_bounding_box_height(self) -> int:
        return self.size[1]

    def set_bounding_box_height(self, height: int):
        self.size[1] = height

    def get_bounding_box_origin(self) -> (int, int):
        return self.size[2], self.size[3]

    def set_bounding_box_origin(self, x: int, y: int):
        self.size[2] = x
        self.size[3] = y

    def get_bounding_box_origin_x(self) -> int:
        return self.size[2]

    def set_bounding_box_origin_x(self, x: int):
        self.size[2] = x

    def get_bounding_box_origin_y(self) -> int:
        return self.size[3]

    def set_bounding_box_origin_y(self, y: int):
        self.size[3] = y

    def get_glyph(self, code_point: int) -> BdfGlyph:
        return self.code_point_to_glyph.get(code_point, None)

    def add_glyph(self, glyph: BdfGlyph):
        if glyph.code_point in self.code_point_to_glyph:
            common.raise_glyph_already_exists_exception(glyph.code_point)
        self.code_point_to_glyph[glyph.code_point] = glyph

    def set_glyph(self, glyph: BdfGlyph):
        self.code_point_to_glyph[glyph.code_point] = glyph

    def remove_glyph(self, code_point: int) -> BdfGlyph:
        return self.code_point_to_glyph.pop(code_point, None)
