
class BdfGlyph:
    def __init__(
            self,
            name: str,
            code_point: int,
            scalable_width: tuple[int, int] = (0, 0),
            device_width: tuple[int, int] = (0, 0),
            bounding_box_size: tuple[int, int] = (0, 0),
            bounding_box_offset: tuple[int, int] = (0, 0),
            bitmap: list[list[int]] = None,
            comments: list[str] = None,
    ):
        """
        :param name:
            The name for the glyph, limited to a string of 14 characters. In base fonts, this should correspond to
            the name in the PostScript language outline font's encoding vector. In a Composite font (Type 0), the
            value may be a numeric offset or glyph ID.
        :param code_point:
            The code point in Unicode. Could set -1 and optionally by another integer specifying the glyph index
            for the non-standard encoding.
        :param scalable_width:
            The scalable width in x and y of the glyph. The scalable width are in units of 1/1000th of the size of
            the glyph and correspond to the width found in AFM files (for outline fonts). If the size of the glyph
            is p points, the width information must be scaled by p/1000 to get the width of the glyph in printer's
            points. This width information should be regarded as a vector indicating the position of the next glyph's
            origin relative to the origin of this glyph.
            To convert the scalable width to the width in device pixels, multiply scalable width times p/1000 times
            r/72, where r is the device resolution in pixels per inch. The result is a real number giving the ideal
            width in device pixels. The actual device width must be an integral number of device pixels and is given
            by the device width entry.
            The scalable width y value should always be zero for a standard X font.
        :param device_width:
            The width in x and y of the glyph in device pixels. Like the scalable width, this width information is a
            vector indicating the position of the next glyph's origin relative to the origin of this glyph.
            The device width y value should always be zero for a standard X font.
        :param bounding_box_size:
            The width in x and height in y of the bitmap in integer pixel values.
        :param bounding_box_offset:
            The x and y displacement of the lower left corner from origin 0 of the bitmap in integer pixel values.
        :param bitmap:
            The bitmap of the glyph.
        :param comments:
            The comments.
        """
        self.name = name
        self.code_point = code_point
        self.scalable_width_x, self.scalable_width_y = scalable_width
        self.device_width_x, self.device_width_y = device_width
        self.bounding_box_width, self.bounding_box_height = bounding_box_size
        self.bounding_box_offset_x, self.bounding_box_offset_y = bounding_box_offset
        if bitmap is None:
            bitmap = []
        self.bitmap = bitmap
        if comments is None:
            comments = []
        self.comments = comments

    @property
    def scalable_width(self) -> tuple[int, int]:
        return self.scalable_width_x, self.scalable_width_y

    @scalable_width.setter
    def scalable_width(self, value: tuple[int, int]):
        self.scalable_width_x, self.scalable_width_y = value

    @property
    def device_width(self) -> tuple[int, int]:
        return self.device_width_x, self.device_width_y

    @device_width.setter
    def device_width(self, value: tuple[int, int]):
        self.device_width_x, self.device_width_y = value

    @property
    def bounding_box_size(self) -> tuple[int, int]:
        return self.bounding_box_width, self.bounding_box_height

    @bounding_box_size.setter
    def bounding_box_size(self, value: tuple[int, int]):
        self.bounding_box_width, self.bounding_box_height = value

    @property
    def bounding_box_offset(self) -> tuple[int, int]:
        return self.bounding_box_offset_x, self.bounding_box_offset_y

    @bounding_box_offset.setter
    def bounding_box_offset(self, value: tuple[int, int]):
        self.bounding_box_offset_x, self.bounding_box_offset_y = value

    @property
    def bounding_box(self) -> tuple[int, int, int, int]:
        return self.bounding_box_width, self.bounding_box_height, self.bounding_box_offset_x, self.bounding_box_offset_y

    @bounding_box.setter
    def bounding_box(self, value: tuple[int, int, int, int]):
        self.bounding_box_width, self.bounding_box_height, self.bounding_box_offset_x, self.bounding_box_offset_y = value
