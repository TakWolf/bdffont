from bdffont import BdfFont

_spec_version = "2.1"


def decode_bdf(text):
    # TODO
    return BdfFont()


def load_bdf(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return decode_bdf(file.read())


def encode_bdf(font: BdfFont):
    text = ""
    # TODO
    return text


def save_bdf(font: BdfFont, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(encode_bdf(font))
