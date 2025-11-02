import weakref

import pytest

from betfair_parser.cache import (
    LPV,
    MarketOrderBook,
    MarketOrders,
    MarketSubscriptionCache,
    OrderSubscriptionCache,
    SelectionKey,
    get_selection_key,
    get_selection_key_streaming,
    ladder_update_lpv,
)
from betfair_parser.spec.common import decode, encode
from betfair_parser.spec.streaming import MCM, OCM, stream_decode
from tests.resources import RESOURCES_DIR


def test_runner_order_book_repr():
    raw = (RESOURCES_DIR / "responses" / "streaming" / "mcm_sub_image_no_market_def.json").read_bytes()
    mcm: MCM = stream_decode(raw)  # type: ignore[assignment]
    cache = MarketSubscriptionCache()
    cache.update(mcm)
    rob = cache.order_book["1.180737193"][25327214]
    repr_str = repr(rob)
    assert repr_str.startswith("<RunnerOrderBook best_display_available_to_back=[")
    assert repr_str.endswith("], total_volume=0.02>")


def test_batb_cache():
    """MarketCache example from the documentation."""
    ladder: dict[int, LPV] = {}

    # Seeing [position,0,0] means that there’s nothing at that position anymore
    # (and hence [0,0,0] means there’s nothing in the entire ladder anymore)
    # Placed the first bet on a selection
    upd0 = [
        [0, 1.4, 2],
        [1, 0, 0],
        [2, 0, 0],
        [3, 0, 0],
        [4, 0, 0],
        [5, 0, 0],
        [6, 0, 0],
        [7, 0, 0],
        [8, 0, 0],
        [9, 0, 0],
    ]
    ladder_update_lpv(ladder, decode(encode(upd0), type=list[LPV]))
    assert ladder[0] == LPV(level=0, price=1.4, volume=2)
    assert len(ladder) == 1

    # Placed a second bet that didn't disturb the first bet's position
    upd1 = [[1, 1.5, 2]]
    ladder_update_lpv(ladder, decode(encode(upd1), type=list[LPV]))
    assert ladder[1] == LPV(level=1, price=1.5, volume=2)
    assert len(ladder) == 2

    # Placed a third bet that bumped the previous two down the ladder
    upd2 = [[2, 1.5, 2], [1, 1.4, 2], [0, 1.3, 2]]
    ladder_update_lpv(ladder, decode(encode(upd2), type=list[LPV]))
    assert ladder[2] == LPV(level=2, price=1.5, volume=2)
    assert ladder[1] == LPV(level=1, price=1.4, volume=2)
    assert ladder[0] == LPV(level=0, price=1.3, volume=2)
    assert len(ladder) == 3

    # Cancelled the top position causing the other positions to move up (and the bottom position to become empty)
    upd3 = [[2, 0, 0], [1, 1.5, 2], [0, 1.4, 2]]
    ladder_update_lpv(ladder, decode(encode(upd3), type=list[LPV]))
    assert 2 not in ladder
    assert ladder[1] == LPV(level=1, price=1.5, volume=2)
    assert ladder[0] == LPV(level=0, price=1.4, volume=2)
    assert len(ladder) == 2

    # Cancelled by market to remove the remaining 2 positions in one go
    upd4 = [[1, 0, 0], [0, 0, 0]]
    ladder_update_lpv(ladder, decode(encode(upd4), type=list[LPV]))
    assert not ladder


OCMS_SAMPLE = [
    """{"op":"ocm","id":2,"clk":"AK0CAPsBALEC","pt":1467219304831,"oc":[{"id":"1.102151675","orc":[{"fullImage":true,"id":6113662,"uo":[{"id":"10822867886","p":12,"s":2,"side":"B","status":"E","pt":"L","ot":"L","pd":1467219304000,"sm":0,"sr":2,"sl":0,"sc":0,"sv":0,"rac":"","rc":"REG_GGC"}]}]}]}""",  # noqa codespell-ignore
    """{"op":"ocm","id":2,"clk":"AK0CAPsBALMC","pt":1467219316709,"oc":[{"id":"1.102151675","orc":[{"id":6113662,"uo":[{"id":"10822867886","p":12,"s":2,"side":"B","status":"EC","pt":"L","ot":"L","pd":1467219304000,"md":1467219316000,"avp":12,"sm":2,"sr":0,"sl":0,"sc":0,"sv":0}],"mb":[[12,2]]}]}]}""",  # noqa codespell-ignore
    """{"op":"ocm","id":2,"clk":"AK0CAJACALsC","pt":1467219376611,"oc":[{"id":"1.102151675","orc":[{"id":6113662,"uo":[{"id":"10822867886","p":12,"s":2,"side":"B","status":"EC","pt":"L","ot":"L","pd":1467219304000,"md":1467219316000,"avp":9.47,"sm":2,"sr":0,"sl":0,"sc":0,"sv":0}],"mb":[[9.47,2],[12,0]]}]}]}""",  # noqa codespell-ignore
]


def test_order_cache_runner_removal():
    """OrderSubscriptionCache example including reduction factor from the documentation."""
    cache = OrderSubscriptionCache()

    # bet gets placed
    cache.update(stream_decode(OCMS_SAMPLE[0]))  # type: ignore[arg-type]
    assert len(cache.orders) == 1
    assert len(cache.orders["1.102151675"]) == 1
    ro = cache.orders["1.102151675"][6113662]
    assert len(ro.unmatched_orders) == 1
    assert not ro.matched_backs
    assert not ro.matched_lays

    order = ro.unmatched_orders[10822867886]
    assert order.price == 12
    assert order.side == "B"
    assert not order.execution_complete
    assert not order.average_price_matched
    size_requested = order.size_remaining
    assert not ro.matched_backs

    # bet matched
    cache.update(stream_decode(OCMS_SAMPLE[1]))  # type: ignore[arg-type]
    order = ro.executed_orders[10822867886]
    assert order.execution_complete
    assert order.matched_date
    assert order.size_matched == size_requested
    assert order.size_remaining == 0
    assert order.average_price_matched == 12
    assert ro.matched_backs[12] == 2

    # another runner was removed and the reduction factor was applied to the order
    cache.update(stream_decode(OCMS_SAMPLE[2]))  # type: ignore[arg-type]
    order = ro.executed_orders[10822867886]  # previous order was replaced
    assert order.average_price_matched == 9.47
    assert ro.matched_backs[9.47] == 2
    assert len(ro.matched_backs) == 1


@pytest.mark.parametrize("dict_type", (MarketOrders, MarketOrderBook))
def test_selection_dict(dict_type):
    cache = dict_type()
    runner_cache = cache[123]
    assert runner_cache == cache[(123, 0)]
    assert runner_cache == cache.get((123, 0.0))

    assert (123, 1.0) not in cache
    assert cache.get((123, 1.0)) is None

    assert len(cache) == 1
    assert list(cache.keys()) == [(123, 0.0)]

    assert list(cache.keys())[0].selection_id == 123
    assert list(cache.keys())[0].handicap == 0.0

    _ = cache[321], cache[456, 0.0]
    assert len(cache) == 3
    assert 321 in cache
    assert (456, 0.0) in cache

    assert cache.get(555) is None
    assert 555 not in cache
    assert len(cache) == 3

    del cache[321]
    del cache[456, 0.0]
    assert len(cache) == 1

    r = weakref.ref(cache)
    assert type(runner_cache).__name__ == type(cache).__name__.replace("Market", "Runner")
    assert r() is cache
    del runner_cache
    del cache
    assert r() is None


def test_selection_key():
    assert str(SelectionKey(123, 0)) == "123+0.0"
    assert str(SelectionKey(123, -0.5)) == "123-0.5"
    assert str(SelectionKey(123, 1.5)) == "123+1.5"


def test_get_selection_key():
    raw = (RESOURCES_DIR / "responses" / "streaming" / "mcm_sub_image_no_market_def.json").read_bytes()
    mcm: MCM = stream_decode(raw)  # type: ignore[assignment]
    for mc in mcm.market_changes:
        for rc in mc.runner_changes:
            selection_key = get_selection_key(rc)
            assert selection_key == get_selection_key_streaming(rc)
            assert selection_key.selection_id in (25327214, 10727442, 41364, 41365, 6393482, 6393483)
            assert selection_key.handicap == 0.0
    for ocm_sample in OCMS_SAMPLE:
        ocm: OCM = stream_decode(ocm_sample)  # type: ignore[assignment]
        for omc in ocm.order_market_changes:
            for orc in omc.order_runner_changes:
                selection_key = get_selection_key(orc)
                assert selection_key == get_selection_key_streaming(orc)
                assert selection_key.selection_id == 6113662
                assert selection_key.handicap == 0.0
