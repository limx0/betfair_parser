"""Check a broad selection of common API requests and responses for correct parsing."""

import bz2

import pytest

from betfair_parser.cache import MarketSubscriptionCache, RunnerOrderBook, SelectionKey
from betfair_parser.spec import accounts, betting
from betfair_parser.spec.common import decode
from betfair_parser.spec.streaming import MCM, StreamRequestType, StreamResponseType, stream_decode
from tests.resources import RESOURCES_DIR, id_from_path


def _name_parts(name):
    # There are some file names, that have special remarks in the end, so we can't just mangle the name:
    # list_cleared_orders_empty etc.
    if name.startswith(("get_", "list_")):
        return 3
    if name.startswith(("cancel_", "place_", "replace_")):
        return 2
    raise ValueError(f"Filename {name} not yet covered by integration tests")


def op_cls_from_path(path):
    snake_op_name = path.name.split(".")[0]
    no_parts = _name_parts(snake_op_name)
    cls_name = "".join(pt.capitalize() for pt in snake_op_name.split("_")[:no_parts])
    mod = {"betting": betting.operations, "accounts": accounts.operations}[path.parent.name]
    return getattr(mod, cls_name)


@pytest.mark.parametrize("path", sorted((RESOURCES_DIR / "requests").glob("*/*.json")), ids=id_from_path)
def test_requests(path):
    raw = path.read_bytes()
    if "streaming" in str(path):
        data = stream_decode(raw)
        assert isinstance(data, StreamRequestType)
        return

    request_type = op_cls_from_path(path)
    assert request_type
    parsed = request_type.parse(raw)
    assert isinstance(parsed, request_type)
    assert parsed.id
    assert parsed.params
    assert parsed.validate()


@pytest.mark.parametrize("path", sorted((RESOURCES_DIR / "responses").glob("*/*.json")), ids=id_from_path)
def test_responses(path):
    raw = path.read_bytes()
    if "streaming" in str(path):
        data = stream_decode(raw)
        if isinstance(data, list):
            for msg in data:
                assert isinstance(msg, StreamResponseType)
        else:
            assert isinstance(data, StreamResponseType)
        return

    parse_type = op_cls_from_path(path).return_type
    resp = decode(raw, type=parse_type)
    assert resp
    if "error" in str(path):
        assert resp.is_error
        assert resp.error
        assert isinstance(resp.error.code, int)
        assert resp.error.exception_code
        assert not resp.result
    else:
        assert not resp.is_error
        assert not resp.error
        assert resp.result


LINE_COUNT = {
    "1.164917629.bz2": 298,
    "1.185781277.bz2": 7600,
    "1.205822330.bz2": 5654,
    "27312315.bz2": 50854,
}


@pytest.mark.parametrize("path", sorted((RESOURCES_DIR / "data").glob("**/*.bz2")), ids=id_from_path)
def test_archive(path):
    mc = MarketSubscriptionCache()
    i = 0
    with bz2.open(path) as f:
        for i, line in enumerate(f, start=1):
            msg = stream_decode(line)
            assert isinstance(msg, MCM)
            mc.update(msg)

    required_count = LINE_COUNT.get(path.name)
    if required_count:
        assert i == required_count
    else:
        # for any other archive file with not explicitly listed line count
        assert i > 100

    assert len(mc.order_book)
    for mkt_id, mkt_order_book in mc.order_book.items():
        mkt_def = mc.definitions[mkt_id]
        betting_type = mkt_def.betting_type
        is_handicap_betting = betting_type in (
            betting.MarketBettingType.ASIAN_HANDICAP_DOUBLE_LINE,
            betting.MarketBettingType.ASIAN_HANDICAP_SINGLE_LINE,
        )
        assert len(mkt_order_book)
        for selection_key, runner_order_book in mkt_order_book.items():
            assert isinstance(runner_order_book, RunnerOrderBook)
            assert isinstance(selection_key, SelectionKey)
            assert isinstance(selection_key.selection_id, int)
            assert isinstance(selection_key.handicap, float)
            if not is_handicap_betting:
                assert selection_key.handicap == 0.0

            best_prices = runner_order_book.best_prices()
            if not best_prices.back_price:
                assert best_prices.back_volume == 0
            else:
                assert 1 < best_prices.back_price < 1001
                assert best_prices.back_volume > 0
            if not best_prices.lay_price:
                assert best_prices.lay_volume == 0
            else:
                assert 1 < best_prices.lay_price < 1001
                assert best_prices.lay_volume > 0

            if best_prices.back_price and best_prices.lay_price and not mkt_def.complete:
                assert best_prices.back_price < best_prices.lay_price, "Back price must be smaller than lay price"
