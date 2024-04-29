
class BdfError(Exception):
    pass


class BdfParseError(BdfError):
    def __init__(self, line_num: int, message: str):
        super().__init__(f'[line {line_num}] {message}')
        self.line_num = line_num


class BdfMissingLineError(BdfError):
    def __init__(self, line_num: int, word: str):
        super().__init__(f"[line {line_num}] Missing line: '{word}'")
        self.line_num = line_num
        self.word = word


class BdfIllegalWordError(BdfError):
    def __init__(self, line_num: int, word: str):
        super().__init__(f"[line {line_num}] Illegal word: '{word}'")
        self.line_num = line_num
        self.word = word


class BdfCountError(BdfError):
    def __init__(self, line_num: int, word: str, expected: int, actual: int):
        super().__init__(f"[line {line_num}] '{word}' expected to be {expected} but actually {actual}")
        self.line_num = line_num
        self.word = word
        self.expected = expected
        self.actual = actual


class BdfPropKeyError(BdfError):
    def __init__(self, key: str, reason: str):
        super().__init__(f"'{key}': {reason}")
        self.key = key
        self.reason = reason


class BdfPropValueError(BdfError):
    def __init__(self, key: str, value: object, reason: str):
        super().__init__(f"'{key}': '{value}': {reason}")
        self.key = key
        self.value = value
        self.reason = reason


class BdfXlfdError(BdfError):
    def __init__(self, font_name: str, reason: str):
        super().__init__(f"'{font_name}': {reason}")
        self.font_name = font_name
        self.reason = reason
