from collections import UserDict

from bdffont.error import BdfPropertiesIllegalKey, BdfPropertiesIllegalValue


def _check_key(key: str):
    if not key.isupper():
        raise BdfPropertiesIllegalKey(f'Properties key must be upper')
    if not key.replace('_', '').isalpha():
        raise BdfPropertiesIllegalKey(f"Illegal properties key '{key}'")


def _check_value(value: str | int):
    if not isinstance(value, str) and not isinstance(value, int):
        raise BdfPropertiesIllegalValue("Properties value must be 'str' or 'int'")


class BdfProperties(UserDict):
    # Comments.
    comments: list[str] = []

    def __getitem__(self, key: str) -> str | int:
        _check_key(key)
        return super().__getitem__(key)

    def __setitem__(self, key: str, value: str | int):
        _check_key(key)
        _check_value(value)
        super().__setitem__(key, value)

    @property
    def default_char(self) -> int:
        return self['DEFAULT_CHAR']

    @default_char.setter
    def default_char(self, value: int):
        self['DEFAULT_CHAR'] = value

    @property
    def font_ascent(self) -> int:
        return self['FONT_ASCENT']

    @font_ascent.setter
    def font_ascent(self, value: int):
        self['FONT_ASCENT'] = value

    @property
    def font_descent(self) -> int:
        return self['FONT_DESCENT']

    @font_descent.setter
    def font_descent(self, value: int):
        self['FONT_DESCENT'] = value

    @property
    def cap_height(self) -> int:
        return self['CAP_HEIGHT']

    @cap_height.setter
    def cap_height(self, value: int):
        self['CAP_HEIGHT'] = value

    @property
    def x_height(self) -> int:
        return self['X_HEIGHT']

    @x_height.setter
    def x_height(self, value: int):
        self['X_HEIGHT'] = value

    @property
    def point_size(self) -> int:
        return self['POINT_SIZE']

    @point_size.setter
    def point_size(self, value: int):
        self['POINT_SIZE'] = value

    @property
    def resolution_x(self) -> int:
        return self['RESOLUTION_X']

    @resolution_x.setter
    def resolution_x(self, value: int):
        self['RESOLUTION_X'] = value

    @property
    def resolution_y(self) -> int:
        return self['RESOLUTION_Y']

    @resolution_y.setter
    def resolution_y(self, value: int):
        self['RESOLUTION_Y'] = value

    @property
    def face_name(self) -> str:
        return self['FACE_NAME']

    @face_name.setter
    def face_name(self, value: str):
        self['FACE_NAME'] = value

    @property
    def font(self) -> str:
        return self['FONT']

    @font.setter
    def font(self, value: str):
        self['FONT'] = value

    @property
    def font_version(self) -> str:
        return self['FONT_VERSION']

    @font_version.setter
    def font_version(self, value: str):
        self['FONT_VERSION'] = value

    @property
    def family_name(self) -> str:
        return self['FAMILY_NAME']

    @family_name.setter
    def family_name(self, value: str):
        self['FAMILY_NAME'] = value

    @property
    def slant(self) -> str:
        return self['SLANT']

    @slant.setter
    def slant(self, value: str):
        self['SLANT'] = value

    @property
    def weight_name(self) -> str:
        return self['WEIGHT_NAME']

    @weight_name.setter
    def weight_name(self, value: str):
        self['WEIGHT_NAME'] = value

    @property
    def foundry(self) -> str:
        return self['FOUNDRY']

    @foundry.setter
    def foundry(self, value: str):
        self['FOUNDRY'] = value

    @property
    def copyright(self) -> str:
        return self['COPYRIGHT']

    @copyright.setter
    def copyright(self, value: str):
        self['COPYRIGHT'] = value

    @property
    def notice(self) -> str:
        return self['NOTICE']

    @notice.setter
    def notice(self, value: str):
        self['NOTICE'] = value
