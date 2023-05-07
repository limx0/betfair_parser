import msgspec.json
import pytest

from betfair_parser.spec.api.betting import (
    PlaceResultResponse,
    cancelOrders,
    placeOrders,
    replaceOrders,
)
from tests.resources import read_test_file, id_from_path


@pytest.mark.parametrize(
    "path",
    [
        "requests/betting_place_order.json",
        "requests/betting_place_order_bsp.json",
        "requests/betting_place_order_handicap.json",
    ],
    ids=id_from_path,
)
def test_place_order(path):
    raw = read_test_file(path)
    message = msgspec.json.decode(raw, type=placeOrders)
    assert message.validate()


@pytest.mark.parametrize(
    "path",
    [
        "requests/betting_cancel_order.json",
    ],
    ids=id_from_path,
)
def test_cancel_order(path):
    raw = read_test_file(path)
    message = msgspec.json.decode(raw, type=cancelOrders)
    assert message.validate()


@pytest.mark.parametrize(
    "path",
    [
        "requests/betting_replace_order.json",
    ],
    ids=id_from_path,
)
def test_replace_order(path):
    raw = read_test_file(path)
    message = msgspec.json.decode(raw, type=replaceOrders)
    assert message.validate()


@pytest.mark.parametrize(
    "path",
    [
        "responses/betting_place_order_error.json",
        "responses/betting_place_order_success.json",
    ],
    ids=id_from_path,
)
def test_place_order_response(path):
    raw = read_test_file(path)
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
