from enum import Enum, _auto_null, auto  # noqa
from functools import total_ordering
from typing import Any


class StrEnum(str, Enum):
    """Allow the `auto()` syntax to use the defined enum key as value.

    Unlike in python 3.11 StrEnum, the fieldnames are not lowered.

    >>> class MyEnum(StrEnum):
    ...     FIELD = auto()
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


@total_ordering
class DocumentedEnum(Enum):
    """Enum with documentation strings.

    Members compare, hash and sort like their values, no matter if these
    are strings or numbers:

    >>> class DocEnum(DocumentedEnum):
    ...     FIELD = doc("This is a docstring")
    ...     FIELD2 = auto()
    >>> DocEnum.FIELD == "FIELD"
    True
    >>> DocEnum.FIELD == DocEnum.FIELD2
    False
    >>> DocEnum.FIELD in ("FIELD", "OTHER")
    True
    >>> hash(DocEnum.FIELD) == hash("FIELD")
    True
    >>> DocEnum.FIELD.__doc__
    'This is a docstring'
    >>> DocEnum.FIELD2.value
    'FIELD2'
    >>> str(DocEnum.FIELD)
    'FIELD: This is a docstring'
    >>> repr(DocEnum.FIELD)
    'DocEnum.FIELD'
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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DocumentedEnum):
            return self.value == other.value
        if isinstance(other, type(self.value)):
            return self.value == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.value)

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, DocumentedEnum):
            return self.value < other.value
        if isinstance(other, type(self.value)):
            return self.value < other
        return NotImplemented
