
class BdfGlyph:
    # Up to 14 characters (no blanks) of descriptive name of the glyph.
    name: str

    # Code point in Unicode.
    code_point: int

    # The scalable width in x and y of character. Scalable widths are in units of 1/1000th of the size of
    # the character. If the size of the character is p points, the width information must be scaled by p/1000
    # to get the width of the character in printer’s points. This width information should be considered as a
    # vector indicating the position of the next character’s origin relative to the origin of this character.
    # To convert the scalable width to the width in device pixels, multiply s_width times p/1000 times r/72,
    # where r is the device resolution in pixels per inch. The result is a real number giving the ideal print
    # width in device pixels. The actual device width must of course be an integral number of device pixels and
    # is given in the next entry. The s_width y value should always be zero for a standard X font.
    scalable_width_x: int
    scalable_width_y: int

    # The width in x and y of the character in device units. Like the s_width, this width information is a vector
    # indicating the position of the next character’s origin relative to the origin of this character. Note that
    # the d_width of a given "hand-tuned" WYSIWYG glyph may deviate slightly from its ideal device-independent width
    # given by s_width in order to improve its typographic characteristics on a display. The d_width y value should
    # always be zero for a standard X font.
    device_width_x: int
    device_width_y: int

    # The width in x, height in y, and the x and y displacement of the lower left corner from the origin
    # of the character.
    bounding_box_width: int
    bounding_box_height: int
    bounding_box_offset_x: int
    bounding_box_offset_y: int

    # The bitmap object.
    bitmap: list[list[int]]

    # Comments.
    comments: list[str]

    def __init__(
            self,
            name: str,
            code_point: int,
            scalable_width: tuple[int, int],
            device_width: tuple[int, int],
            bounding_box_size: tuple[int, int],
            bounding_box_offset: tuple[int, int],
            bitmap: list[list[int]] = None,
            comments: list[str] = None,
    ):
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

    def get_padded_bitmap(self) -> list[list[int]]:
        padded_bitmap = []
        for bitmap_row in self.bitmap:
            padded_bitmap_row = []
            for alpha in bitmap_row:
                if alpha == 0:
                    padded_bitmap_row.append(0)
                else:
                    padded_bitmap_row.append(1)
            remainder = len(bitmap_row) % 8
            if remainder > 0:
                for _ in range(8 - remainder):
                    padded_bitmap_row.append(0)
            padded_bitmap.append(padded_bitmap_row)
        return padded_bitmap
