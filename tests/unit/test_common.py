"""Tests for field documentation metadata and its usage in validation error messages."""

from typing import Annotated

import msgspec
import msgspec.inspect
import pytest

from betfair_parser.exceptions import JSONError, StreamError
from betfair_parser.spec.betting.orders import UpdateOrders
from betfair_parser.spec.common import decode, doc, enriched_validation_error
from betfair_parser.spec.streaming import stream_decode


def test_doc_metadata():
    meta = doc("some description")
    assert isinstance(meta, msgspec.Meta)
    assert meta.description == "some description"


def test_field_description_available():
    params_cls = UpdateOrders.params_cls
    info = msgspec.inspect.type_info(params_cls)
    assert isinstance(info, msgspec.inspect.StructType)
    fields = {f.name: f.type for f in info.fields}
    expected = {
        "market_id": "The market id these orders are to be placed on",
        "instructions": "The limit of update instructions per request is 60",
    }
    for name, description in expected.items():
        meta = fields[name]
        assert isinstance(meta, msgspec.inspect.Metadata)
        assert meta.extra_json_schema["description"] == description


def test_decode_error_with_description():
    raw = b'{"jsonrpc": "2.0", "id": 1, "params": {"marketId": 123, "instructions": []}}'
    with pytest.raises(JSONError, match=r"\(The market id these orders are to be placed on\)"):
        decode(raw, type=UpdateOrders)


def test_decode_error_nested_description():
    raw = b'{"jsonrpc": "2.0", "id": 1, "params": {"marketId": "1.23", "instructions": [{"unknown": 1}]}}'
    with pytest.raises(JSONError, match=r"\(The limit of update instructions per request is 60\)"):
        decode(raw, type=UpdateOrders)


def test_decode_error_without_description_unchanged():
    raw = b'{"jsonrpc": "2.0", "id": 1, "params": {"marketId": "1.23", "unknown": true}}'
    with pytest.raises(JSONError, match="unknown field") as exc_info:
        decode(raw, type=UpdateOrders)
    assert "The market id" not in str(exc_info.value)


def test_enriched_validation_error_undocumented_type():
    error = msgspec.ValidationError("Expected `str`, got `int` - at `$.id`")
    assert enriched_validation_error(error, int) == "Expected `str`, got `int` - at `$.id`"


def test_enriched_validation_error_ambiguous_union():
    """Unions with a differing field of the same name must not guess a description."""

    class A(msgspec.Struct, frozen=True, tag_field="op", tag="a"):
        value: Annotated[int, doc("description A")] = 0

    class B(msgspec.Struct, frozen=True, tag_field="op", tag="b"):
        value: Annotated[int, doc("description B")] = 0

    error = msgspec.ValidationError("Expected `int`, got `str` - at `$.value`")
    assert enriched_validation_error(error, A | B) == "Expected `int`, got `str` - at `$.value`"


def test_enriched_validation_error_consistent_union():
    """Unions, where all members agree on a field description, may use it."""

    class A(msgspec.Struct, frozen=True, tag_field="op", tag="a"):
        value: Annotated[int, doc("agreed description")] = 0

    class B(msgspec.Struct, frozen=True, tag_field="op", tag="b"):
        value: Annotated[int, doc("agreed description")] = 0

    error = msgspec.ValidationError("Expected `int`, got `str` - at `$.value`")
    assert enriched_validation_error(error, A | B) == "Expected `int`, got `str` - at `$.value` (agreed description)"


def test_enriched_validation_error_tuple_index():
    """Tuple descriptions are picked by the position from the error path index."""

    class T(msgspec.Struct, frozen=True, tag_field="op", tag="t"):
        pair: Annotated[
            tuple[Annotated[int, doc("first element")], Annotated[str, doc("second element")]],
            doc("a pair"),
        ] = None

    error = msgspec.ValidationError("Expected `str`, got `int` - at `$.pair[1]`")
    assert "(second element)" in enriched_validation_error(error, T)


def test_enriched_validation_error_masked_dict_key():
    """msgspec masks dict keys as ``[...]``; the value type description is the most specific one."""

    class T(msgspec.Struct, frozen=True, tag_field="op", tag="t"):
        m: Annotated[dict[str, Annotated[int, doc("the map value")]], doc("the map")] = {}

    error = msgspec.ValidationError("Expected `int`, got `object` - at `$.m[...]`")
    assert "(the map value)" in enriched_validation_error(error, T)


def test_enriched_validation_error_nested_masked_dict_key():
    """Dict keys masked as ``[...]`` must survive the path splitting, even nested within lists."""

    class T(msgspec.Struct, frozen=True, tag_field="op", tag="t"):
        items: Annotated[list[dict[str, Annotated[int, doc("the inner value")]]], doc("the items")] = []

    error = msgspec.ValidationError("Expected `int`, got `object` - at `$.items[0][...]`")
    assert "(the inner value)" in enriched_validation_error(error, T)


def test_enriched_validation_error_non_struct_root():
    """List roots carry their index directly at the root marker ``$`` and walking continues below."""

    class T(msgspec.Struct, frozen=True, tag_field="op", tag="t"):
        value: Annotated[int, doc("the value")] = 0

    error = msgspec.ValidationError("Expected `int`, got `object` - at `$[1].value`")
    assert "(the value)" in enriched_validation_error(error, list[T])


def test_stream_decode_error_with_description():
    raw = b'{"op": "status", "id": 1, "connectionsAvailable": "many"}'
    with pytest.raises(StreamError, match=r"\(The number of connections available for this account at this moment\)"):
        stream_decode(raw)


def test_json_schema_contains_description():
    params_cls = UpdateOrders.params_cls
    schema = msgspec.json.schema(params_cls)
    assert schema["$defs"]["_UpdateOrdersParams"]["properties"]["marketId"]["description"] == (
        "The market id these orders are to be placed on"
    )
