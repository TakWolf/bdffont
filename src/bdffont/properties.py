from collections import UserDict

from bdffont.error import BdfIllegalPropertiesKey, BdfIllegalPropertiesValue


def _check_key(key: str):
    if not key.isupper():
        raise BdfIllegalPropertiesKey(f'Properties key must be upper')
    if not key.replace('_', '').isalnum():
        raise BdfIllegalPropertiesKey(f"Illegal properties key '{key}'")


def _check_value(value: str | int):
    if not isinstance(value, str) and not isinstance(value, int):
        raise BdfIllegalPropertiesValue("Properties value must be 'str' or 'int'")


class BdfProperties(UserDict):
    def __init__(
            self,
            kvs: dict[str, str | int] = None,
            comments: list[str] = None,
    ):
        """
        :param kvs:
            Keys and values used for initialization.
        :param comments:
            The comments.
        """
        super().__init__()
        if kvs is not None:
            for key, value in kvs.items():
                self[key] = value
        if comments is None:
            comments = []
        self.comments = comments

    def __getitem__(self, key: str) -> str | int:
        _check_key(key)
        return super().__getitem__(key)

    def __setitem__(self, key: str, value: str | int):
        _check_key(key)
        _check_value(value)
        super().__setitem__(key, value)

    @property
    def default_char(self) -> int | None:
        return self.get('DEFAULT_CHAR', None)

    @default_char.setter
    def default_char(self, value: int):
        self['DEFAULT_CHAR'] = value

    @property
    def font_ascent(self) -> int | None:
        return self.get('FONT_ASCENT', None)

    @font_ascent.setter
    def font_ascent(self, value: int):
        self['FONT_ASCENT'] = value

    @property
    def font_descent(self) -> int | None:
        return self.get('FONT_DESCENT', None)

    @font_descent.setter
    def font_descent(self, value: int):
        self['FONT_DESCENT'] = value

    @property
    def cap_height(self) -> int | None:
        return self.get('CAP_HEIGHT', None)

    @cap_height.setter
    def cap_height(self, value: int):
        self['CAP_HEIGHT'] = value

    @property
    def x_height(self) -> int | None:
        return self.get('X_HEIGHT', None)

    @x_height.setter
    def x_height(self, value: int):
        self['X_HEIGHT'] = value

    @property
    def point_size(self) -> int | None:
        return self.get('POINT_SIZE', None)

    @point_size.setter
    def point_size(self, value: int):
        self['POINT_SIZE'] = value

    @property
    def resolution_x(self) -> int | None:
        return self.get('RESOLUTION_X', None)

    @resolution_x.setter
    def resolution_x(self, value: int):
        self['RESOLUTION_X'] = value

    @property
    def resolution_y(self) -> int | None:
        return self.get('RESOLUTION_Y', None)

    @resolution_y.setter
    def resolution_y(self, value: int):
        self['RESOLUTION_Y'] = value

    @property
    def face_name(self) -> str | None:
        return self.get('FACE_NAME', None)

    @face_name.setter
    def face_name(self, value: str):
        self['FACE_NAME'] = value

    @property
    def font(self) -> str | None:
        return self.get('FONT', None)

    @font.setter
    def font(self, value: str):
        self['FONT'] = value

    @property
    def font_version(self) -> str | None:
        return self.get('FONT_VERSION', None)

    @font_version.setter
    def font_version(self, value: str):
        self['FONT_VERSION'] = value

    @property
    def family_name(self) -> str | None:
        return self.get('FAMILY_NAME', None)

    @family_name.setter
    def family_name(self, value: str):
        self['FAMILY_NAME'] = value

    @property
    def slant(self) -> str | None:
        return self.get('SLANT', None)

    @slant.setter
    def slant(self, value: str):
        self['SLANT'] = value

    @property
    def weight_name(self) -> str | None:
        return self.get('WEIGHT_NAME', None)

    @weight_name.setter
    def weight_name(self, value: str):
        self['WEIGHT_NAME'] = value

    @property
    def foundry(self) -> str | None:
        return self.get('FOUNDRY', None)

    @foundry.setter
    def foundry(self, value: str):
        self['FOUNDRY'] = value

    @property
    def copyright(self) -> str | None:
        return self.get('COPYRIGHT', None)

    @copyright.setter
    def copyright(self, value: str):
        self['COPYRIGHT'] = value

    @property
    def notice(self) -> str | None:
        return self.get('NOTICE', None)

    @notice.setter
    def notice(self, value: str):
        self['NOTICE'] = value
