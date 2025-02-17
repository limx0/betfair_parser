from enum import Enum, _auto_null, auto  # noqa


class StrEnum(str, Enum):
    """Allow the `auto()` syntax to use the defined enum key as value.

    Unlike in python 3.11 StrEnum, the fieldnames are not lowered.

    class MyEnum(BaseEnum):
        FIELD = auto()

    >>> MyEnum.FIELD.value == "FIELD"
    True
    """

    def _generate_next_value_(key, start, count, last_values):  # type: ignore[override]
        return key

    def __repr__(self):
        return f"{type(self).__name__}.{self.name}"


class LowerStrEnum(StrEnum):
    """Like StrEnum, but have lowered values."""

    def _generate_next_value_(key, start, count, last_values):  # type: ignore[override]
        return key.lower()


class doc(auto):
    """Auto-generated enum field with docstring

    doc("docstring") replaces auto() for DocumentedEnums. A value
    can be set using doc(value=..., docstring=...), otherwise the
    same value as for auto() is calculated.

    This mechanism only works in combination with
    DocumentedEnum and messes up the values of an Enum otherwise.
    """

    def __init__(self, docstring=None, value=None):
        self._value = value
        self.__doc__ = docstring

    @property
    def value(self):
        # When value is accessed the first time by the enum internals, it
        # needs to return auto.value, in order to trigger the auto-generation
        # mechanism.
        if self._value is None:
            return _auto_null
        return self

    @value.setter
    def value(self, val):
        # value is set by the enum auto-generation mechanism
        self._value = val


class DocumentedEnum(Enum):
    """Enum with documentation strings.

    class DocEnum(DocumentedEnum):
        FIELD = doc("This is a docstring")
        FIELD2 = auto()

    >>> DocEnum.FIELD == "FIELD"
    True
    >>> DocEnum.FIELD.__doc__
    "This is a docstring"
    """

    def __new__(cls, val):
        member = object.__new__(cls)
        if isinstance(val, doc):
            member._value_ = val._value
            member.__doc__ = val.__doc__
        else:
            # also handle ordinary or auto() values
            member._value = val  # type: ignore[attr-defined]
            member.__doc__ = None
        return member

    def _generate_next_value_(key, start, count, last_values):  # type: ignore[override]
        return key

    def __str__(self):
        if self.__doc__:
            return f"{self.name}: {self.__doc__}"
        return self.name

    def __repr__(self):
        return f"{type(self).__name__}.{self.name}"
