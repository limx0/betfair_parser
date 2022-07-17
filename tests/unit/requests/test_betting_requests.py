import msgspec.json
import pytest

from betfair_parser.spec.api.betting import cancelOrders, placeOrders, replaceOrders
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
    place = msgspec.json.decode(raw, type=placeOrders)
    assert place.validate()


@pytest.mark.parametrize(
    "raw",
    [
        read_test_file("requests/betting_cancel_order.json"),
    ],
)
def test_cancel_order(raw):
    place = msgspec.json.decode(raw, type=cancelOrders)
    assert place.validate()


@pytest.mark.parametrize(
    "raw",
    [
        read_test_file("requests/betting_replace_order.json"),
    ],
)
def test_replace_order(raw):
    place = msgspec.json.decode(raw, type=replaceOrders)
    assert place.validate()
