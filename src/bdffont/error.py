
class BdfException(Exception):
    pass


class BdfGlyphExists(BdfException):
    code_point: int

    def __init__(self, code_point: int):
        self.code_point = code_point
        super().__init__(f"Glyph '{code_point}' already exists")


class BdfMissingLine(BdfException):
    word: str

    def __init__(self, word: str):
        self.word = word
        super().__init__(f"Missing line '{word}'")


class BdfValueIncorrect(BdfException):
    word: str

    def __init__(self, word: str):
        self.word = word
        super().__init__(f"'{word}' value incorrect")


class BdfPropertiesIllegalKey(BdfException):
    pass


class BdfPropertiesIllegalValue(BdfException):
    pass
