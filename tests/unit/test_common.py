"""Tests for field documentation metadata and its usage in validation error messages."""

import json
import re
from typing import Annotated

import msgspec
import msgspec.inspect
import pytest

from betfair_parser.exceptions import JSONError, StreamError
from betfair_parser.spec.accounts.operations import GetAccountFunds
from betfair_parser.spec.betting.orders import UpdateOrders
from betfair_parser.spec.common import (
    Request,
    Response,
    decode,
    doc,
    enriched_validation_error,
)
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
    with pytest.raises(JSONError, match=r"got `123` \(marketId: The market id these orders are to be placed on\)"):
        decode(raw, type=UpdateOrders)


def test_decode_error_value_truncated_to_limit():
    raw = b'{"jsonrpc": "2.0", "id": 1, "params": {"marketId": ["' + b"x" * 120 + b'"], "instructions": []}}'
    with pytest.raises(JSONError) as exc_info:
        decode(raw, type=UpdateOrders)
    match = re.search(r": got `([^`]*)`", str(exc_info.value))
    assert match
    assert len(match.group(1)) == 100
    assert match.group(1).endswith("...")


def test_decode_error_masked_key_without_value():
    """Masked dict keys `...]` have no specific value, only the labeled description is added."""

    class T(msgspec.Struct, frozen=True, rename="camel"):
        m: Annotated[dict[str, Annotated[int, doc("the map value")]], doc("the map")] = {}

    raw = b'{"m": {"a.b": "x"}}'
    with pytest.raises(JSONError) as exc_info:
        decode(raw, type=T)
    message = str(exc_info.value)
    assert ": got `" not in message
    assert "(m: the map value)" in message


def test_decode_error_nested_description():
    raw = b'{"jsonrpc": "2.0", "id": 1, "params": {"marketId": "1.23", "instructions": [{"unknown": 1}]}}'
    with pytest.raises(JSONError, match=r"\(instructions: The limit of update instructions per request is 60\)"):
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
    assert (
        enriched_validation_error(error, A | B)
        == "Expected `int`, got `str` - at `$.value` (value: agreed description)"
    )


def test_enriched_validation_error_tuple_index():
    """Tuple descriptions are picked by the position from the error path index."""

    class T(msgspec.Struct, frozen=True, tag_field="op", tag="t"):
        pair: Annotated[
            tuple[Annotated[int, doc("first element")], Annotated[str, doc("second element")]],
            doc("a pair"),
        ] = None

    error = msgspec.ValidationError("Expected `str`, got `int` - at `$.pair[1]`")
    assert "(pair: second element)" in enriched_validation_error(error, T)


def test_enriched_validation_error_masked_dict_key():
    """msgspec masks dict keys as ``[...]``; the value type description is the most specific one."""

    class T(msgspec.Struct, frozen=True, tag_field="op", tag="t"):
        m: Annotated[dict[str, Annotated[int, doc("the map value")]], doc("the map")] = {}

    error = msgspec.ValidationError("Expected `int`, got `object` - at `$.m[...]`")
    assert "(m: the map value)" in enriched_validation_error(error, T)


def test_enriched_validation_error_nested_masked_dict_key():
    """Dict keys masked as ``[...]`` must survive the path splitting, even nested within lists."""

    class T(msgspec.Struct, frozen=True, tag_field="op", tag="t"):
        items: Annotated[list[dict[str, Annotated[int, doc("the inner value")]]], doc("the items")] = []

    error = msgspec.ValidationError("Expected `int`, got `object` - at `$.items[0][...]`")
    assert "(items: the inner value)" in enriched_validation_error(error, T)


def test_enriched_validation_error_non_struct_root():
    """List roots carry their index directly at the root marker ``$`` and walking continues below."""

    class T(msgspec.Struct, frozen=True, tag_field="op", tag="t"):
        value: Annotated[int, doc("the value")] = 0

    error = msgspec.ValidationError("Expected `int`, got `object` - at `$[1].value`")
    assert "(value: the value)" in enriched_validation_error(error, list[T])


def test_stream_decode_error_with_description():
    raw = b'{"op": "status", "id": 1, "connectionsAvailable": "many"}'
    with pytest.raises(
        StreamError,
        match=r"got `'many'` \(connectionsAvailable: The number of connections available for this account at this moment\)",
    ):
        stream_decode(raw)


def test_json_schema_contains_description():
    params_cls = UpdateOrders.params_cls
    schema = msgspec.json.schema(params_cls)
    assert schema["$defs"]["_UpdateOrdersParams"]["properties"]["marketId"]["description"] == (
        "The market id these orders are to be placed on"
    )


def test_rpc_error_str_without_data():
    raw = b'{"jsonrpc": "2.0", "id": 1, "error": {"code": -32700, "message": "oops"}}'
    response = decode(raw, type=Response[int])
    assert response.is_error
    assert str(response.error).startswith("INVALID_JSON")


def test_request_params_cls_fallbacks():
    class OptionalOtherParams(Request, frozen=True):
        params: int | None = None  # type: ignore[assignment]

    class NoParams(Request, frozen=True):
        params: None = None

    assert OptionalOtherParams.params_cls is dict
    assert NoParams.params_cls is dict


def test_parse_response_error_without_raise():
    request = GetAccountFunds.with_params()
    error = {"jsonrpc": "2.0", "id": request.id, "error": {"code": -32602, "message": "DSC-0018"}}
    error_response = request.parse_response(json.dumps(error).encode(), raise_errors=False)
    assert error_response.exception_code.name == "INVALID_PARAMETERS"


def test_decode_error_invalid_json():
    with pytest.raises(JSONError, match="malformed"):
        decode(b"nope", type=int)


class _TagA(msgspec.Struct, frozen=True, tag_field="op", tag="a"):
    value: int = 0


class _TagB(msgspec.Struct, frozen=True, tag_field="op", tag="b"):
    other: int = 0


class _TaggedUnion(msgspec.Struct, frozen=True, tag_field="op", tag="t"):
    u: _TagA | _TagB = _TagA()


@pytest.mark.parametrize(
    ["error_message", "type"],
    [
        ("Expected `str`, got `int`", int),  # no path in the message
        ("Expected `str`, got `int` - at `$[0]`", int),  # index into a non-sequence root
        ("Expected `str`, got `int` - at `$.u.nope`", _TaggedUnion),  # union without a matching field
        ("Expected `str`, got `int` - at `$.a`", "not a type"),  # unusable type, must never mask the error
    ],
)
def test_enriched_validation_error_unresolvable_path(error_message, type):
    """Errors, whose paths can't be resolved into a documented field, keep the message unchanged."""
    error = msgspec.ValidationError(error_message)
    assert enriched_validation_error(error, type) == error_message


def test_enriched_validation_error_bracket_descent_fails_keeps_field_description():
    """A failing bracket descent keeps the field description, but drops bracket descriptions."""

    class T(msgspec.Struct, frozen=True, tag_field="op", tag="t"):
        values: Annotated[list[Annotated[int, doc("the list value")]], doc("the values")] = []

    error = msgspec.ValidationError("Expected `str`, got `int` - at `$.values[0][1]`")
    assert "(values: the values)" in enriched_validation_error(error, T)


def test_enriched_validation_error_tuple_field_without_index():
    """A tuple field reached without an index falls back to its first element type."""

    class Item(msgspec.Struct, frozen=True):
        x: Annotated[int, doc("the x value")] = 0

    class T(msgspec.Struct, frozen=True, tag_field="op", tag="t"):
        pair: Annotated[tuple[Item, Item], doc("a pair")] = (Item(), Item())

    error = msgspec.ValidationError("Expected `str`, got `int` - at `$.pair.x`")
    assert "(x: the x value)" in enriched_validation_error(error, T)


def test_enriched_validation_error_dict_field_without_key():
    """A dict field reached without a key falls back to its value type description."""

    class T(msgspec.Struct, frozen=True, tag_field="op", tag="t"):
        m: Annotated[dict[str, Annotated[int, doc("the map value")]], doc("the map")] = {}

    error = msgspec.ValidationError("Expected `str`, got `int` - at `$.m.x`")
    assert "(m: the map)" in enriched_validation_error(error, T)
