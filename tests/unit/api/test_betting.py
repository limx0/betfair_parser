import pytest

from betfair_parser.spec.betting.orders import cancelOrders, placeOrders, replaceOrders
from betfair_parser.spec.common import decode
from tests.resources import id_from_path, read_test_file


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
    message = decode(raw, type=placeOrders)
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
    message = decode(raw, type=cancelOrders)
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
    message = decode(raw, type=replaceOrders)
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
    message = decode(raw, type=placeOrders.return_type)
    assert message.validate()


@pytest.mark.parametrize(
    "path",
    [
        "responses/betting_replace_orders_success.json",
    ],
    ids=id_from_path,
)
def test_replace_order_response(path):
    raw = read_test_file(path)
    message = decode(raw, type=replaceOrders.return_type)
    assert message.validate()
