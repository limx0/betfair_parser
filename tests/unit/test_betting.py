import pytest

from betfair_parser.spec.betting import CancelOrders, PlaceOrders, ReplaceOrders
from betfair_parser.spec.common import decode
from tests.resources import RESOURCES_DIR, id_from_path


@pytest.mark.parametrize(
    "filename",
    [
        "place_orders_persist.json",
        "place_orders_lapse.json",
        "place_orders_bsp.json",
        "place_orders_handicap.json",
    ],
    ids=id_from_path,
)
def test_place_order(filename):
    raw = (RESOURCES_DIR / "requests" / "betting" / filename).read_bytes()
    message = decode(raw, type=PlaceOrders)
    assert message.validate()


@pytest.mark.parametrize(
    "filename",
    [
        "cancel_orders.json",
        "cancel_orders_partly.json",
    ],
    ids=id_from_path,
)
def test_cancel_order(filename):
    raw = (RESOURCES_DIR / "requests" / "betting" / filename).read_bytes()
    message = decode(raw, type=CancelOrders)
    assert message.validate()


@pytest.mark.parametrize(
    "filename",
    [
        "replace_orders.json",
    ],
    ids=id_from_path,
)
def test_replace_order(filename):
    raw = (RESOURCES_DIR / "requests" / "betting" / filename).read_bytes()
    message = decode(raw, type=ReplaceOrders)
    assert message.validate()


@pytest.mark.parametrize(
    "filename",
    [
        "place_orders_lapse.json",
        "place_orders_success.json",
        "place_orders_failure.json",
        "place_orders_no_persistence.json",
    ],
    ids=id_from_path,
)
def test_place_order_response(filename):
    raw = (RESOURCES_DIR / "responses" / "betting" / filename).read_bytes()
    message = decode(raw, type=PlaceOrders.return_type)
    assert message.validate()


@pytest.mark.parametrize(
    "filename",
    [
        "cancel_orders_success.json",
        "cancel_orders_partly.json",
        "cancel_orders_failure.json",
    ],
    ids=id_from_path,
)
def test_cancel_order_response(filename):
    raw = (RESOURCES_DIR / "responses" / "betting" / filename).read_bytes()
    message = decode(raw, type=CancelOrders.return_type)
    assert message.validate()


@pytest.mark.parametrize(
    "filename",
    [
        "replace_orders_success.json",
    ],
    ids=id_from_path,
)
def test_replace_order_response(filename):
    raw = (RESOURCES_DIR / "responses" / "betting" / filename).read_bytes()
    message = decode(raw, type=ReplaceOrders.return_type)
    assert message.validate()
