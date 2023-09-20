import pytest

from betfair_parser.spec.betting.orders import CancelOrders, PlaceOrders, ReplaceOrders
from betfair_parser.spec.common import decode
from tests.resources import RESOURCES_DIR, id_from_path


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
    raw = RESOURCES_DIR.joinpath(path).read_bytes()
    message = decode(raw, type=PlaceOrders)
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
    raw = RESOURCES_DIR.joinpath(path).read_bytes()
    message = decode(raw, type=CancelOrders)
    assert message.validate()


@pytest.mark.parametrize(
    "path",
    [
        "requests/betting/replace_orders.json",
    ],
    ids=id_from_path,
)
def test_replace_order(path):
    raw = RESOURCES_DIR.joinpath(path).read_bytes()
    message = decode(raw, type=ReplaceOrders)
    assert message.validate()


@pytest.mark.parametrize(
    "path",
    [
        "responses/betting/place_orders_lapse.json",
        "responses/betting/place_orders_success.json",
        "responses/betting/place_orders_failure.json",
        "responses/betting/place_orders_no_persistence.json",
    ],
    ids=id_from_path,
)
def test_place_order_response(path):
    raw = RESOURCES_DIR.joinpath(path).read_bytes()
    message = decode(raw, type=PlaceOrders.return_type)
    assert message.validate()


@pytest.mark.parametrize(
    "path",
    [
        "responses/betting/cancel_orders_success.json",
        "responses/betting/cancel_orders_partly.json",
        "responses/betting/cancel_orders_failure.json",
    ],
    ids=id_from_path,
)
def test_cancel_order_response(path):
    raw = RESOURCES_DIR.joinpath(path).read_bytes()
    message = decode(raw, type=CancelOrders.return_type)
    assert message.validate()


@pytest.mark.parametrize(
    "path",
    [
        "responses/betting/replace_orders_success.json",
    ],
    ids=id_from_path,
)
def test_replace_order_response(path):
    raw = RESOURCES_DIR.joinpath(path).read_bytes()
    message = decode(raw, type=ReplaceOrders.return_type)
    assert message.validate()
