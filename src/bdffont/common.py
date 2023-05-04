
def check_word(word: str):
    if not word.isupper():
        raise Exception(f'Word must be upper: {word}')
    if not word.replace('_', '').isalpha():
        raise Exception(f'Word illegal: {word}')


def check_properties_value(value: str | int):
    if not isinstance(value, str) and not isinstance(value, int):
        raise Exception("Properties value can only be a 'str' or 'int'")


def raise_glyph_already_exists_exception(code_point: int):
    raise Exception(f"Glyph '{chr(code_point)} ({code_point})' already exists")


def raise_missing_word_line_exception(word: str):
    raise Exception(f"Missing word line '{word}'")


def raise_word_value_incorrect_exception(word: str):
    raise Exception(f"'{word}' value incorrect")


def raise_word_line_not_closeed(start_word: str, end_word: str):
    raise Exception(f"'{start_word}' not closed with '{end_word}'")
