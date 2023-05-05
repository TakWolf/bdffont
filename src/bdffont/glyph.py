
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
    scalable_width: tuple[int, int]

    # The width in x and y of the character in device units. Like the s_width, this width information is a vector
    # indicating the position of the next character’s origin relative to the origin of this character. Note that
    # the d_width of a given "hand-tuned" WYSIWYG glyph may deviate slightly from its ideal device-independent width
    # given by s_width in order to improve its typographic characteristics on a display. The d_width y value should
    # always be zero for a standard X font.
    device_width: tuple[int, int]

    # The width in x, height in y, and the x and y displacement of the lower left corner from the origin of the character.
    bounding_box: tuple[int, int, int, int]

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
            bounding_box: tuple[int, int, int, int],
            bitmap: list[list[int]] = None,
            comments: list[str] = None,
    ):
        self.name = name
        self.code_point = code_point
        self.scalable_width = scalable_width
        self.device_width = device_width
        self.bounding_box = bounding_box
        if bitmap is None:
            self.bitmap = []
        else:
            self.bitmap = bitmap
        if comments is None:
            self.comments = []
        else:
            self.comments = comments

    @property
    def scalable_width_x(self) -> int:
        return self.scalable_width[0]

    @scalable_width_x.setter
    def scalable_width_x(self, value: int):
        self.scalable_width = (value, self.scalable_width[1])

    @property
    def scalable_width_y(self) -> int:
        return self.scalable_width[1]

    @scalable_width_y.setter
    def scalable_width_y(self, value: int):
        self.scalable_width = (self.scalable_width[0], value)

    @property
    def device_width_x(self) -> int:
        return self.device_width[0]

    @device_width_x.setter
    def device_width_x(self, value: int):
        self.device_width = (value, self.device_width[1])

    @property
    def device_width_y(self) -> int:
        return self.device_width[1]

    @device_width_y.setter
    def device_width_y(self, value: int):
        self.device_width = (self.device_width[0], value)

    @property
    def bounding_box_size(self) -> tuple[int, int]:
        return self.bounding_box[0], self.bounding_box[1]

    @bounding_box_size.setter
    def bounding_box_size(self, value: tuple[int, int]):
        self.bounding_box = (value[0], value[1], self.bounding_box[2], self.bounding_box[3])

    @property
    def bounding_box_width(self) -> int:
        return self.bounding_box[0]

    @bounding_box_width.setter
    def bounding_box_width(self, value: int):
        self.bounding_box = (value, self.bounding_box[1], self.bounding_box[2], self.bounding_box[3])

    @property
    def bounding_box_height(self) -> int:
        return self.bounding_box[1]

    @bounding_box_height.setter
    def bounding_box_height(self, value: int):
        self.bounding_box = (self.bounding_box[0], value, self.bounding_box[2], self.bounding_box[3])

    @property
    def bounding_box_origin(self) -> tuple[int, int]:
        return self.bounding_box[2], self.bounding_box[3]

    @bounding_box_origin.setter
    def bounding_box_origin(self, value: tuple[int, int]):
        self.bounding_box = (self.bounding_box[0], self.bounding_box[1], value[0], value[1])

    @property
    def bounding_box_origin_x(self) -> int:
        return self.bounding_box[2]

    @bounding_box_origin_x.setter
    def bounding_box_origin_x(self, value: int):
        self.bounding_box = (self.bounding_box[0], self.bounding_box[1], value, self.bounding_box[3])

    @property
    def bounding_box_origin_y(self) -> int:
        return self.bounding_box[3]

    @bounding_box_origin_y.setter
    def bounding_box_origin_y(self, value: int):
        self.bounding_box = (self.bounding_box[0], self.bounding_box[1], self.bounding_box[2], value)

    def get_padding_bitmap(self) -> list[list[int]]:
        padding_bitmap = []
        for bitmap_row in self.bitmap:
            padding_bitmap_row = []
            for alpha in bitmap_row:
                if alpha == 0:
                    padding_bitmap_row.append(0)
                else:
                    padding_bitmap_row.append(1)
            remainder = len(bitmap_row) % 8
            if remainder > 0:
                for _ in range(8 - remainder):
                    padding_bitmap_row.append(0)
            padding_bitmap.append(padding_bitmap_row)
        return padding_bitmap
