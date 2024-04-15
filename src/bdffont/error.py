
class BdfError(Exception):
    pass


class BdfParseError(BdfError):
    pass


class BdfAttrError(BdfError):
    pass


class BdfMissingLineError(BdfError):
    def __init__(self, word: str):
        self.word = word
        super().__init__(f"Word unclosed: '{word}'")


class BdfCountError(BdfError):
    def __init__(self, word: str, expected: int, actual: int):
        self.word = word
        self.expected = expected
        self.actual = actual
        super().__init__(f"'{word}' expected to be {expected} but actually {actual}")


class BdfPropKeyError(BdfError):
    def __init__(self, key: str, reason: str):
        self.key = key
        self.reason = reason
        super().__init__(f"'{key}': {reason}")


class BdfPropValueError(BdfError):
    def __init__(self, key: str, value: object, reason: str):
        self.key = key
        self.value = value
        self.reason = reason
        super().__init__(f"'{key}': '{value}': {reason}")


class BdfXlfdError(BdfError):
    def __init__(self, font_name: str, reason: str):
        self.font_name = font_name
        self.reason = reason
        super().__init__(f"'{font_name}': {reason}")
