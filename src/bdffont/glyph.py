from bdffont.error import BdfIllegalBitmap


class BdfGlyph:
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
        """
        :param name:
            Up to 14 characters (no blanks) of descriptive name of the glyph.
        :param code_point:
            Code point in Unicode.
        :param scalable_width:
            The scalable width in x and y of character. Scalable widths are in units of 1/1000th of the size of the
            character. If the size of the character is p points, the width information must be scaled by p/1000 to
            get the width of the character in printer’s points. This width information should be considered as a vector
            indicating the position of the next character’s origin relative to the origin of this character.
            To convert the scalable width to the width in device pixels, multiply scalable_width times p/1000 times
            r/72, where r is the device resolution in pixels per inch. The result is a real number giving the ideal
            print width in device pixels. The actual device width must of course be an integral number of device pixels
            and is given in the next entry. The scalable_width y value should always be zero for a standard X font.
        :param device_width:
            The width in x and y of the character in device units. Like the scalable_width, this width information is
            a vector indicating the position of the next character’s origin relative to the origin of this character.
            Note that the device_width of a given "hand-tuned" WYSIWYG glyph may deviate slightly from its ideal
            device-independent width given by scalable_width in order to improve its typographic characteristics on a
            display. The device_width y value should always be zero for a standard X font.
        :param bounding_box_size:
            The width in x, height in y of the character.
        :param bounding_box_offset:
            The x and y displacement of the lower left corner from the origin of the character.
        :param bitmap:
            The bitmap object.
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

    def check_bitmap_validity(self):
        if len(self.bitmap) != self.bounding_box_height:
            raise BdfIllegalBitmap("Glyph bitmap height not equals 'bounding_box_height'")
        for bitmap_row in self.bitmap:
            if len(bitmap_row) != self.bounding_box_width:
                raise BdfIllegalBitmap("Glyph bitmap width not equals 'bounding_box_width'")

    def get_8bit_aligned_bitmap(self, optimize_bitmap: bool = False) -> tuple[tuple[int, int], tuple[int, int], list[list[int]]]:
        self.check_bitmap_validity()
        bounding_box_width = self.bounding_box_width
        bounding_box_height = self.bounding_box_height
        bounding_box_offset_x = self.bounding_box_offset_x
        bounding_box_offset_y = self.bounding_box_offset_y
        bitmap = [[color for color in bitmap_row] for bitmap_row in self.bitmap]

        if optimize_bitmap:
            # Top
            while bounding_box_height > 0:
                for color in bitmap[0]:
                    if color != 0:
                        break
                else:
                    bitmap.pop(0)
                    bounding_box_height -= 1
                    continue
                break
            # Bottom
            while bounding_box_height > 0:
                for color in bitmap[-1]:
                    if color != 0:
                        break
                else:
                    bitmap.pop()
                    bounding_box_height -= 1
                    bounding_box_offset_y += 1
                    continue
                break
            # Left
            while bounding_box_width > 0:
                for bitmap_row in bitmap:
                    color = bitmap_row[0]
                    if color != 0:
                        break
                else:
                    for bitmap_row in bitmap:
                        bitmap_row.pop(0)
                    bounding_box_width -= 1
                    bounding_box_offset_x += 1
                    continue
                break
            # Right
            while bounding_box_width > 0:
                for bitmap_row in bitmap:
                    color = bitmap_row[-1]
                    if color != 0:
                        break
                else:
                    for bitmap_row in bitmap:
                        bitmap_row.pop()
                    bounding_box_width -= 1
                    continue
                break

        remainder = bounding_box_width % 8
        if remainder > 0:
            for bitmap_row in bitmap:
                for _ in range(8 - remainder):
                    bitmap_row.append(0)

        return (bounding_box_width, bounding_box_height), (bounding_box_offset_x, bounding_box_offset_y), bitmap
