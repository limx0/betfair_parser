"""Serialization behavior of `BaseMessage` request objects across all API areas.

`BaseMessage` is configured with `omit_defaults=True`, `repr_omit_defaults=True`,
`frozen=True` and `rename="camel"`, so neither the encoded JSON nor the repr may
contain `None` default values, instances are immutable and encoded keys are camelCase.
"""

import json

import pytest

from betfair_parser.spec.accounts.operations import (
    GetAccountDetails,
    GetAccountFunds,
    GetAccountStatement,
    ListCurrencyRates,
)
from betfair_parser.spec.betting import (
    CancelOrders,
    OrderType,
    PlaceInstruction,
    PlaceOrders,
    ReplaceOrders,
    RunnerMetaData,
    Side,
)
from betfair_parser.spec.betting.orders import UpdateOrders
from betfair_parser.spec.common import BaseResponse, Request, decode, encode


REQUEST_OBJECTS = [
    GetAccountDetails.with_params(),
    GetAccountFunds.with_params(),
    GetAccountStatement.with_params(),
    ListCurrencyRates.with_params(),
    CancelOrders.with_params(market_id="10"),
    PlaceOrders.with_params(
        market_id="123", instructions=[PlaceInstruction(order_type=OrderType.LIMIT, selection_id=123123, side=Side.BACK)]
    ),
    ReplaceOrders.with_params(market_id="456", instructions=[]),
    RunnerMetaData(),
]


@pytest.mark.parametrize(
    "obj",
    REQUEST_OBJECTS,
    ids=lambda obj: type(obj).__name__,
)
def test_omit_defaults(obj):
    assert b"None" not in encode(obj)


@pytest.mark.parametrize(
    "obj",
    REQUEST_OBJECTS,
    ids=lambda obj: type(obj).__name__,
)
def test_repr_omit_default(obj):
    assert "None" not in repr(obj)


@pytest.mark.parametrize(
    "obj",
    REQUEST_OBJECTS,
    ids=lambda obj: type(obj).__name__,
)
def test_frozen(obj):
    with pytest.raises(AttributeError):
        setattr(obj, obj.__struct_fields__[0], None)


@pytest.mark.parametrize(
    "obj",
    REQUEST_OBJECTS,
    ids=lambda obj: type(obj).__name__,
)
def test_roundtrip_equality(obj):
    """Encoding and decoding are inverse operations for all request objects."""
    assert decode(encode(obj), type=type(obj)) == obj


@pytest.mark.parametrize(
    "obj",
    REQUEST_OBJECTS,
    ids=lambda obj: type(obj).__name__,
)
def test_camel_case_keys(obj):
    """The `rename="camel"` config applies to all encoded keys, also nested ones."""

    def walk_keys(value):
        if isinstance(value, dict):
            for key, item in value.items():
                yield key
                yield from walk_keys(item)
        elif isinstance(value, list):
            for item in value:
                yield from walk_keys(item)

    assert all("_" not in key for key in walk_keys(json.loads(encode(obj))))


@pytest.mark.parametrize(
    "obj",
    [obj for obj in REQUEST_OBJECTS if isinstance(obj, Request)],
    ids=lambda obj: type(obj).__name__,
)
def test_rpc_envelope(obj):
    """RPC requests encode with a jsonrpc 2.0 envelope, a positive request id and their method tag."""
    data = json.loads(encode(obj))
    assert data["jsonrpc"] == "2.0"
    assert isinstance(data["id"], int) and data["id"] > 0
    assert data["method"] == obj.method


@pytest.mark.parametrize(
    "obj",
    REQUEST_OBJECTS,
    ids=lambda obj: type(obj).__name__,
)
def test_to_dict(obj):
    """`to_dict` returns a dict containing all struct fields."""
    as_dict = obj.to_dict()
    assert set(as_dict) == set(obj.__struct_fields__)


@pytest.mark.parametrize(
    "obj",
    REQUEST_OBJECTS,
    ids=lambda obj: type(obj).__name__,
)
def test_replace_without_changes(obj):
    """`replace` without changes returns an equal object."""
    assert obj.replace() == obj


def test_replace_changes_field():
    request = UpdateOrders.with_params(market_id="1.2", instructions=[])
    replaced = request.replace(id=request.id + 1)
    assert replaced.id == request.id + 1
    assert replaced.params == request.params


def test_base_response_is_error_default_false():
    class BareResponse(BaseResponse, frozen=True):
        pass

    assert BareResponse().is_error is False
