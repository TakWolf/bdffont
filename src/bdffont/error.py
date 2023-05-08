
class BdfException(Exception):
    pass


class BdfGlyphExists(BdfException):
    def __init__(self, code_point: int):
        self.code_point = code_point
        super().__init__(f"Glyph '{code_point}' already exists")


class BdfMissingLine(BdfException):
    def __init__(self, word: str):
        self.word = word
        super().__init__(f"Missing line '{word}'")


class BdfValueIncorrect(BdfException):
    def __init__(self, word: str):
        self.word = word
        super().__init__(f"'{word}' value incorrect")


class BdfIllegalBitmap(BdfException):
    pass


class BdfIllegalPropertiesKey(BdfException):
    pass


class BdfIllegalPropertiesValue(BdfException):
    pass
