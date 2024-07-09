from typing import Any


class BdfError(Exception):
    pass


class BdfParseError(BdfError):
    line_num: int
    reason: str

    def __init__(self, line_num: int, reason: str):
        self.line_num = line_num
        self.reason = reason

    def __str__(self) -> str:
        return f'[line {self.line_num}] {self.reason}'


class BdfMissingLineError(BdfError):
    line_num: int
    word: str

    def __init__(self, line_num: int, word: str):
        self.line_num = line_num
        self.word = word

    def __str__(self) -> str:
        return f'[line {self.line_num}] missing line: {repr(self.word)}'


class BdfIllegalWordError(BdfError):
    line_num: int
    word: str

    def __init__(self, line_num: int, word: str):
        self.line_num = line_num
        self.word = word

    def __str__(self) -> str:
        return f'[line {self.line_num}] illegal word: {repr(self.word)}'


class BdfCountError(BdfError):
    line_num: int
    word: str
    expected: int
    actual: int

    def __init__(self, line_num: int, word: str, expected: int, actual: int):
        self.line_num = line_num
        self.word = word
        self.expected = expected
        self.actual = actual

    def __str__(self) -> str:
        return f'[line {self.line_num}] {repr(self.word)} expected to be {self.expected} but actually {self.actual}'


class BdfPropKeyError(BdfError):
    key: Any
    reason: str

    def __init__(self, key: Any, reason: str):
        self.key = key
        self.reason = reason

    def __str__(self) -> str:
        return f'{self.reason}: key = {repr(self.key)}'


class BdfPropValueError(BdfError):
    key: str
    value: Any
    reason: str

    def __init__(self, key: str, value: Any, reason: str):
        self.key = key
        self.value = value
        self.reason = reason

    def __str__(self) -> str:
        return f'{self.reason}: key = {repr(self.key)}, value = {repr(self.value)}'


class BdfXlfdError(BdfError):
    font_name: str
    reason: str

    def __init__(self, font_name: str, reason: str):
        self.font_name = font_name
        self.reason = reason

    def __str__(self) -> str:
        return f'{self.reason}: {self.font_name}'
