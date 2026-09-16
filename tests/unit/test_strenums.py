import msgspec

from betfair_parser.strenums import DocumentedEnum, StrEnum, auto, doc


def test_strenum():
    class SE(StrEnum):
        FIELD1 = auto()
        FIELD2 = "xyz"

    assert SE.FIELD1 == "FIELD1"
    assert SE.FIELD2 == "xyz"
    assert repr(SE.FIELD2) == "SE.FIELD2"


def test_documented_enum():
    class DE(DocumentedEnum):
        FIELD_AUTO = auto()
        FIELD_DOC = doc("This is a docstring")
        FIELD_DOC_VALUE = doc(value="doc_val", docstring="This is another docstring")
        FIELD_VAL = "SOME_VALUE"

    assert DE.FIELD_AUTO.value == "FIELD_AUTO"
    assert DE.FIELD_AUTO.__doc__ is None
    assert repr(DE.FIELD_AUTO) == "DE.FIELD_AUTO"
    assert DE.FIELD_DOC.value == "FIELD_DOC"
    assert DE.FIELD_DOC.__doc__ == "This is a docstring"
    assert DE.FIELD_DOC_VALUE.value == "doc_val"
    assert DE.FIELD_DOC_VALUE.__doc__ == "This is another docstring"
    assert repr(DE.FIELD_DOC) == "DE.FIELD_DOC"
    assert DE.FIELD_VAL.value == "SOME_VALUE"
    assert DE.FIELD_VAL.__doc__ is None
    assert repr(DE.FIELD_VAL) == "DE.FIELD_VAL"

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


def test_documented_enum_comparison():
    class ErrorA(DocumentedEnum):
        CODE = doc("Some error code")

    class ErrorB(DocumentedEnum):
        CODE = doc("The same error code from a different enum")

    assert ErrorA.CODE == ErrorB.CODE
    assert ErrorA.CODE == "CODE"
    assert ErrorA.CODE in ("CODE", "OTHER")
    assert ErrorA.CODE in {ErrorB.CODE}
    assert hash(ErrorA.CODE) == hash(ErrorB.CODE)
    assert hash(ErrorA.CODE) == hash("CODE")
    assert sorted([ErrorA.CODE, "AAA"]) == ["AAA", ErrorA.CODE]  # type: ignore[type-var]
    assert "CODE" == ErrorA.CODE
    assert ErrorA.CODE != "OTHER"


def test_documented_enum_int_comparison():
    class IE(DocumentedEnum):
        FIELD1 = doc(value=1, docstring="Some docstring")
        FIELD2 = doc(value=10, docstring="Another docstring")

    assert IE.FIELD1 == 1
    assert IE(10) == IE.FIELD2
    assert IE.FIELD1 in (1, 2)
    assert IE.FIELD1 in {IE.FIELD1, IE.FIELD2}
    assert sorted([IE.FIELD2, IE.FIELD1]) == [IE.FIELD1, IE.FIELD2]
    assert IE.FIELD1 < IE.FIELD2
    assert IE.FIELD1 < 5
    assert IE.FIELD2 > 5
    # str() and repr() behaviour is unchanged, client code relies on it
    assert str(IE.FIELD1) == "FIELD1: Some docstring"
    assert repr(IE.FIELD1) == "IE.FIELD1"
    assert msgspec.json.decode(msgspec.json.encode(IE.FIELD1), type=IE) == IE.FIELD1
