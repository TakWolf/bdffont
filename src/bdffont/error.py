from typing import Any


class BdfError(Exception):
    pass


class BdfParseError(BdfError):
    pass


class BdfMissingWordError(BdfError):
    word: str

    def __init__(self, word: str):
        self.word = word

    def __str__(self) -> str:
        return f'missing word: {repr(self.word)}'


class BdfIllegalWordError(BdfError):
    word: str

    def __init__(self, word: str):
        self.word = word

    def __str__(self) -> str:
        return f'illegal word: {repr(self.word)}'


class BdfCountError(BdfError):
    word: str
    expected: int
    actual: int

    def __init__(self, word: str, expected: int, actual: int):
        self.word = word
        self.expected = expected
        self.actual = actual

    def __str__(self) -> str:
        return f'{repr(self.word)} expected to be {self.expected} but actually {self.actual}'


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
    pass
