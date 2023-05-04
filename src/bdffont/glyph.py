
class BdfGlyph:
    # Up to 14 characters (no blanks) of descriptive name of the glyph.
    # Example: quoteright
    name: str

    # Code point in Unicode.
    # Example: 39
    code_point: int

    # The scalable width in x and y of character.
    # Scalable widths are in units of 1/1000th of the size of the character.
    # If the size of the character is p points, the width information must be scaled by p/1000 to get
    # the width of the character in printer’s points.
    # This width information should be considered as a vector indicating the position of the next
    # character’s origin relative to the origin of this character.
    # To convert the scalable width to the width in device pixels, multiply s_width times p/1000 times r/72,
    # where r is the device resolution in pixels per inch.
    # The result is a real number giving the ideal print width in device pixels.
    # The actual device width must of course be an integral number of device pixels and is given in the next entry.
    # The s_width y value should always be zero for a standard X font.
    s_width: (int, int)

    # The width in x and y of the character in device units.
    # Like the s_width, this width information is a vector indicating the position of the next character’s origin
    # relative to the origin of this character.
    # Note that the d_width of a given "hand-tuned" WYSIWYG glyph may deviate slightly from its ideal
    # device-independent width given by s_width in order to improve its typographic characteristics
    # on a display.
    # The d_width y value should always be zero for a standard X font.
    d_width: (int, int)

    # The width in x (BBw), height in y (BBh), and x and y displacement (BBox, BBoy) of the lower left corner
    # from the origin of the character.
    bbx: (int, int, int, int)

    # The bitmap object.
    bitmap: list[list[int]]

    # Comments.
    comments: list[str]

    def __init__(
            self,
            name: str,
            code_point: int,
            s_width: (int, int),
            d_width: (int, int),
            bbx: (int, int, int, int),
            bitmap: list[list[int]] = None,
            comments: list[str] = None,
    ):
        self.name = name
        self.code_point = code_point
        self.s_width = s_width
        self.d_width = d_width
        self.bbx = bbx
        if bitmap is None:
            self.bitmap = []
        else:
            self.bitmap = bitmap
        if comments is None:
            self.comments = []
        else:
            self.comments = comments
