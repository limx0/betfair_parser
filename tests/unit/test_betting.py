import pytest

from betfair_parser.spec.betting.orders import cancelOrders, placeOrders, replaceOrders
from betfair_parser.spec.common import decode
from tests.resources import id_from_path, read_test_file


@pytest.mark.parametrize(
    "path",
    [
        "requests/betting/place_orders_persist.json",
        "requests/betting/place_orders_lapse.json",
        "requests/betting/place_orders_bsp.json",
        "requests/betting/place_orders_handicap.json",
    ],
    ids=id_from_path,
)
def test_place_order(path):
    raw = read_test_file(path)
    message = decode(raw, type=placeOrders)
    assert message.validate()


@pytest.mark.parametrize(
    "path",
    [
        "requests/betting/cancel_orders.json",
        "requests/betting/cancel_orders_partly.json",
    ],
    ids=id_from_path,
)
def test_cancel_order(path):
    raw = read_test_file(path)
    message = decode(raw, type=cancelOrders)
    assert message.validate()


@pytest.mark.parametrize(
    "path",
    [
        "requests/betting/replace_orders.json",
    ],
    ids=id_from_path,
)
def test_replace_order(path):
    raw = read_test_file(path)
    message = decode(raw, type=replaceOrders)
    assert message.validate()


@pytest.mark.parametrize(
    "path",
    [
        "responses/betting/place_orders_lapse.json",
        "responses/betting/place_orders_error.json",
        "responses/betting/place_orders_success.json",
    ],
    ids=id_from_path,
)
def test_place_order_response(path):
    raw = read_test_file(path)
    message = decode(raw, type=placeOrders.return_type)
    assert message.validate()


@pytest.mark.parametrize(
    "path",
    [
        "responses/betting/cancel_orders_error.json",
        "responses/betting/cancel_orders_success.json",
        "responses/betting/cancel_orders_partly.json",
    ],
    ids=id_from_path,
)
def test_cancel_order_response(path):
    raw = read_test_file(path)
    message = decode(raw, type=cancelOrders.return_type)
    assert message.validate()


@pytest.mark.parametrize(
    "path",
    [
        "responses/betting/replace_orders_success.json",
    ],
    ids=id_from_path,
)
def test_replace_order_response(path):
    raw = read_test_file(path)
    message = decode(raw, type=replaceOrders.return_type)
    assert message.validate()