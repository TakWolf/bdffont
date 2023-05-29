
class BdfException(Exception):
    pass


class BdfMissingLine(BdfException):
    def __init__(self, word: str):
        self.word = word
        super().__init__(f"Missing line '{word}'")


class BdfValueIncorrect(BdfException):
    def __init__(self, word: str):
        self.word = word
        super().__init__(f"'{word}' value incorrect")


class BdfIllegalPropertiesKey(BdfException):
    pass


class BdfIllegalPropertiesValue(BdfException):
    pass


class BdfGlyphExists(BdfException):
    def __init__(self, code_point: int):
        self.code_point = code_point
        super().__init__(f"Glyph '{code_point}' already exists")


class BdfIllegalBitmap(BdfException):
    def __init__(self, code_point: int, reason: str):
        self.code_point = code_point
        super().__init__(f"Glyph '{code_point}': {reason}")
