import msgspec.json
import pytest

from betfair_parser.spec.api.betting import (
    PlaceResultResponse,
    cancelOrders,
    placeOrders,
    replaceOrders,
)
from tests.resources import read_test_file


@pytest.mark.parametrize(
    "raw",
    [
        read_test_file("requests/betting_place_order.json"),
        read_test_file("requests/betting_place_order_bsp.json"),
        read_test_file("requests/betting_place_order_handicap.json"),
    ],
)
def test_place_order(raw):
    message = msgspec.json.decode(raw, type=placeOrders)
    assert message.validate()


@pytest.mark.parametrize(
    "raw",
    [
        read_test_file("requests/betting_cancel_order.json"),
    ],
)
def test_cancel_order(raw):
    message = msgspec.json.decode(raw, type=cancelOrders)
    assert message.validate()


@pytest.mark.parametrize(
    "raw",
    [
        read_test_file("requests/betting_replace_order.json"),
    ],
)
def test_replace_order(raw):
    message = msgspec.json.decode(raw, type=replaceOrders)
    assert message.validate()


@pytest.mark.parametrize(
    "raw",
    [
        read_test_file("responses/betting_place_order_error.json"),
        read_test_file("responses/betting_place_order_success.json"),
    ],
)
def test_place_order_response(raw):
    message = msgspec.json.decode(raw, type=PlaceResultResponse)
    assert message.validate()


# @pytest.mark.parametrize(
#     "raw",
#     [
#        read_test_file("responses/betting_replace_orders_success.json"),
#        read_test_file("responses/betting_replace_orders_success_multi.json"),
#     ],
# )
# def test_replace_order_response(raw):
#     message = msgspec.json.decode(raw, type=ReplaceResultResponse)
#     assert message.validate()
