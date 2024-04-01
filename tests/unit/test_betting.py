from datetime import datetime

import msgspec
import msgspec.json
import pytest

from betfair_parser.spec.betting import (
    CancelOrders,
    OrderType,
    PlaceInstruction,
    PlaceOrders,
    ReplaceOrders,
    RunnerMetaData,
    Side,
)
from betfair_parser.spec.common import decode, encode
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


def test_runner_metadata_validation_pass():
    metadata = dict(
        weight_value=100,
        stall_draw=10,
        sire_year_born=1990,
        dam_year_born=2000,
        damsire_year_born=1990,
        cloth_number=13,
        age=3,
    )
    for rmd in (
        RunnerMetaData(**metadata),  # type: ignore
        RunnerMetaData.parse(msgspec.json.encode({k.upper(): v for k, v in metadata.items()})),
    ):
        assert rmd.weight_value == 100
        assert rmd.stall_draw == 10
        assert rmd.sire_year_born == 1990
        assert rmd.dam_year_born == 2000
        assert rmd.cloth_number == 13
        assert rmd.age == 3


def test_runner_metadata_validation_fail():
    cur_year = datetime.now().year
    metadata = dict(
        weight_value=-1,
        stall_draw=100,
        sire_year_born=cur_year + 1,
        dam_year_born=1950,
        damsire_year_born=1930,
        cloth_number=-1,
        age=35,
    )
    for rmd in (
        RunnerMetaData(**metadata),  # type: ignore
        RunnerMetaData.parse(msgspec.json.encode({k.upper(): v for k, v in metadata.items()})),
    ):
        for field in RunnerMetaData.__struct_fields__:
            # all fields should have failed __post_init__ validation
            assert getattr(rmd, field) is None


REQUEST_OBJECTS = [
    CancelOrders.with_params(market_id=10),
    PlaceOrders.with_params(
        market_id=123, instructions=[PlaceInstruction(order_type=OrderType.LIMIT, selection_id=123123, side=Side.BACK)]
    ),
    ReplaceOrders.with_params(market_id=456, instructions=[]),
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
