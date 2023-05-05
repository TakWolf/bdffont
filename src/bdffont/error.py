
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


class BdfWordNotClosed(BdfException):
    start_word: str
    end_word: str

    def __init__(self, start_word: str, end_word: str):
        self.start_word = start_word
        self.end_word = end_word
        super().__init__(f"'{start_word}' not closed with '{end_word}'")


class BdfValueIncorrect(BdfException):
    word: str

    def __init__(self, word: str):
        self.word = word
        super().__init__(f"'{word}' value incorrect")


class BdfPropertiesIllegalKey(BdfException):
    pass


class BdfPropertiesIllegalValue(BdfException):
    pass
