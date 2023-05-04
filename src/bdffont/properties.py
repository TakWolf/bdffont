from collections import UserDict

from bdffont import common


class BdfProperties(UserDict):
    # Comments.
    comments: list[str] = []

    def __getitem__(self, word: str) -> str | int:
        common.check_word(word)
        return super().__getitem__(word)

    def __setitem__(self, word: str, value: str | int):
        common.check_word(word)
        common.check_properties_value(value)
        super().__setitem__(word, value)

    def get_default_char(self) -> int:
        return self['DEFAULT_CHAR']

    def set_default_char(self, value: int):
        self['DEFAULT_CHAR'] = value

    def get_font_ascent(self) -> int:
        return self['FONT_ASCENT']

    def set_font_ascent(self, value: int):
        self['FONT_ASCENT'] = value

    def get_font_descent(self) -> int:
        return self['FONT_DESCENT']

    def set_font_descent(self, value: int):
        self['FONT_DESCENT'] = value

    def get_cap_height(self) -> int:
        return self['CAP_HEIGHT']

    def set_cap_height(self, value: int):
        self['CAP_HEIGHT'] = value

    def get_x_height(self) -> int:
        return self['X_HEIGHT']

    def set_x_height(self, value: int):
        self['X_HEIGHT'] = value

    def get_point_size(self) -> int:
        return self['POINT_SIZE']

    def set_point_size(self, value: int):
        self['POINT_SIZE'] = value

    def get_resolution_x(self) -> int:
        return self['RESOLUTION_X']

    def set_resolution_x(self, value: int):
        self['RESOLUTION_X'] = value

    def get_resolution_y(self) -> int:
        return self['RESOLUTION_Y']

    def set_resolution_y(self, value: int):
        self['RESOLUTION_Y'] = value

    def get_face_name(self) -> str:
        return self['FACE_NAME']

    def set_face_name(self, value: str):
        self['FACE_NAME'] = value

    def get_font(self) -> str:
        return self['FONT']

    def set_font(self, value: str):
        self['FONT'] = value

    def get_font_version(self) -> str:
        return self['FONT_VERSION']

    def set_font_version(self, value: str):
        self['FONT_VERSION'] = value

    def get_family_name(self) -> str:
        return self['FAMILY_NAME']

    def set_family_name(self, value: str):
        self['FAMILY_NAME'] = value

    def get_slant(self) -> str:
        return self['SLANT']

    def set_slant(self, value: str):
        self['SLANT'] = value

    def get_weight_name(self) -> str:
        return self['WEIGHT_NAME']

    def set_weight_name(self, value: str):
        self['WEIGHT_NAME'] = value

    def get_foundry(self) -> str:
        return self['FOUNDRY']

    def set_foundry(self, value: str):
        self['FOUNDRY'] = value

    def get_copyright(self) -> str:
        return self['COPYRIGHT']

    def set_copyright(self, value: str):
        self['COPYRIGHT'] = value

    def get_notice(self) -> str:
        return self['NOTICE']

    def set_notice(self, value: str):
        self['NOTICE'] = value
