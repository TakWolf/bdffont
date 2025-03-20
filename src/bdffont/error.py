
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
        return f'the count of {repr(self.word)} is incorrect: {self.expected} -> {self.actual}'


class BdfXlfdError(BdfError):
    pass
