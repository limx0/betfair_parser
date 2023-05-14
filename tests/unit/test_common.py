from enum import auto

import msgspec

from betfair_parser.spec.common import DocumentedEnum, StrEnum, doc


def test_strenum():
    class SE(StrEnum):
        FIELD1 = auto()
        FIELD2 = "xyz"

    assert SE.FIELD1 == "FIELD1"
    assert SE.FIELD2 == "xyz"


def test_documented_enum():
    class DE(DocumentedEnum):
        FIELD_AUTO = auto()
        FIELD_DOC = doc("This is a docstring")
        FIELD_DOC_VALUE = doc(value="doc_val", docstring="This is another docstring")
        FIELD_VAL = "SOME_VALUE"

    assert DE.FIELD_AUTO.value == "FIELD_AUTO"
    assert DE.FIELD_AUTO.__doc__ is None
    assert DE.FIELD_DOC.value == "FIELD_DOC"
    assert DE.FIELD_DOC.__doc__ == "This is a docstring"
    assert DE.FIELD_DOC_VALUE.value == "doc_val"
    assert DE.FIELD_DOC_VALUE.__doc__ == "This is another docstring"
    assert DE.FIELD_VAL.value == "SOME_VALUE"
    assert DE.FIELD_VAL.__doc__ is None

    assert DE("FIELD_AUTO") == DE.FIELD_AUTO
    assert set(DE._value2member_map_.keys()) == {"FIELD_AUTO", "FIELD_DOC", "doc_val", "SOME_VALUE"}
    assert msgspec.json.decode(msgspec.json.encode(DE.FIELD_DOC_VALUE), type=DE) == DE.FIELD_DOC_VALUE


def test_documented_enum_int():
    class IE(DocumentedEnum):
        FIELD1 = doc(value=1, docstring="Some docstring")
        FIELD2 = doc(value=10, docstring="Another docstring")

    assert IE.FIELD1.value == 1
    assert IE.FIELD1.__doc__ == "Some docstring"
    assert IE.FIELD2.value == 10
    assert IE.FIELD2.__doc__ == "Another docstring"
    assert msgspec.json.decode(msgspec.json.encode(IE.FIELD1), type=IE) == IE.FIELD1
