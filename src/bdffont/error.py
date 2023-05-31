
class BdfException(Exception):
    pass


class BdfMissingLine(BdfException):
    def __init__(self, word: str):
        self.word = word
        super().__init__(f"Missing line '{word}'")


class BdfCountIncorrect(BdfException):
    def __init__(self, word: str, defined: int, actual: int):
        self.word = word
        self.defined = defined
        self.actual = actual
        super().__init__(f"'{word}' count incorrect: defined as {defined} but actually {actual}")


class BdfIllegalPropertiesKey(BdfException):
    def __init__(self, key: str, reason: str):
        self.key = key
        self.reason = reason
        super().__init__(f"Illegal properties key '{key}': {reason}")


class BdfIllegalPropertiesValue(BdfException):
    def __init__(self, key: str, value: any, reason: str):
        self.key = key
        self.value = value
        self.reason = reason
        super().__init__(f"Illegal properties value of key '{key}': {reason}")


class BdfIllegalXlfdFontName(BdfException):
    def __init__(self, font_name: str, reason: str):
        self.font_name = font_name
        self.reason = reason
        super().__init__(f'Illegal xlfd font name: {reason}')


class BdfGlyphExists(BdfException):
    def __init__(self, code_point: int):
        self.code_point = code_point
        super().__init__(f"Glyph '{code_point}' already exists")


class BdfIllegalBitmap(BdfException):
    def __init__(self, code_point: int, reason: str):
        self.code_point = code_point
        super().__init__(f"Glyph '{code_point}': {reason}")
