from betfair_parser.cache import LPV, MarketCache, OrderCache, depth_ladder_update_lpv
from betfair_parser.spec.common import decode, encode
from betfair_parser.spec.streaming import stream_decode
from tests.resources import RESOURCES_DIR


def test_runner_order_book_repr():
    mcm = stream_decode((RESOURCES_DIR / "responses/streaming/mcm_sub_image_no_market_def.json").read_bytes())
    cache = MarketCache()
    cache.update(mcm)
    rc = cache.order_book["1.180737193"][25327214]
    repr_str = repr(rc)
    assert repr_str.startswith("<RunnerOrderBook best_display_available_to_back=[")
    assert repr_str.endswith("], traded_volume=0.02>")


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
    depth_ladder_update_lpv(ladder, decode(encode(upd0), type=list[LPV]))
    assert ladder[0] == LPV(level=0, price=1.4, volume=2)
    assert len(ladder) == 1

    # Placed a second bet that didn't disturb the first bet's position
    upd1 = [[1, 1.5, 2]]
    depth_ladder_update_lpv(ladder, decode(encode(upd1), type=list[LPV]))
    assert ladder[1] == LPV(level=1, price=1.5, volume=2)
    assert len(ladder) == 2

    # Placed a third bet that bumped the previous two down the ladder
    upd2 = [[2, 1.5, 2], [1, 1.4, 2], [0, 1.3, 2]]
    depth_ladder_update_lpv(ladder, decode(encode(upd2), type=list[LPV]))
    assert ladder[2] == LPV(level=2, price=1.5, volume=2)
    assert ladder[1] == LPV(level=1, price=1.4, volume=2)
    assert ladder[0] == LPV(level=0, price=1.3, volume=2)
    assert len(ladder) == 3

    # Cancelled the top position causing the other positions to move up (and the bottom position to become empty)
    upd3 = [[2, 0, 0], [1, 1.5, 2], [0, 1.4, 2]]
    depth_ladder_update_lpv(ladder, decode(encode(upd3), type=list[LPV]))
    assert 2 not in ladder
    assert ladder[1] == LPV(level=1, price=1.5, volume=2)
    assert ladder[0] == LPV(level=0, price=1.4, volume=2)
    assert len(ladder) == 2

    # Cancelled by market to remove the remaining 2 positions in one go
    upd4 = [[1, 0, 0], [0, 0, 0]]
    depth_ladder_update_lpv(ladder, decode(encode(upd4), type=list[LPV]))
    assert not ladder


OCMS_SAMPLE = [
    """{"op":"ocm","id":2,"clk":"AK0CAPsBALEC","pt":1467219304831,"oc":[{"id":"1.102151675","orc":[{"fullImage":true,"id":6113662,"uo":[{"id":"10822867886","p":12,"s":2,"side":"B","status":"E","pt":"L","ot":"L","pd":1467219304000,"sm":0,"sr":2,"sl":0,"sc":0,"sv":0,"rac":"","rc":"REG_GGC"}]}]}]}""",  # noqa codespell-ignore
    """{"op":"ocm","id":2,"clk":"AK0CAPsBALMC","pt":1467219316709,"oc":[{"id":"1.102151675","orc":[{"id":6113662,"uo":[{"id":"10822867886","p":12,"s":2,"side":"B","status":"EC","pt":"L","ot":"L","pd":1467219304000,"md":1467219316000,"avp":12,"sm":2,"sr":0,"sl":0,"sc":0,"sv":0}],"mb":[[12,2]]}]}]}""",  # noqa codespell-ignore
    """{"op":"ocm","id":2,"clk":"AK0CAJACALsC","pt":1467219376611,"oc":[{"id":"1.102151675","orc":[{"id":6113662,"uo":[{"id":"10822867886","p":12,"s":2,"side":"B","status":"EC","pt":"L","ot":"L","pd":1467219304000,"md":1467219316000,"avp":9.47,"sm":2,"sr":0,"sl":0,"sc":0,"sv":0}],"mb":[[9.47,2],[12,0]]}]}]}""",  # noqa codespell-ignore
]


def test_order_cache_runner_removal():
    """OrderCache example including reduction factor from the documentation."""
    cache = OrderCache()

    # bet gets placed
    cache.update(stream_decode(OCMS_SAMPLE[0]))
    assert len(cache.orders) == 1
    assert len(cache.orders["1.102151675"]) == 1
    assert len(cache.orders["1.102151675"][6113662].unmatched_orders) == 1
    assert not cache.orders["1.102151675"][6113662].matched_backs
    assert not cache.orders["1.102151675"][6113662].matched_lays

    order = cache.orders["1.102151675"][6113662].unmatched_orders[10822867886]
    assert order.price == 12
    assert order.side == "B"
    assert not order.execution_complete
    assert not order.average_price_matched
    size_requested = order.size_remaining
    assert not cache.orders["1.102151675"][6113662].matched_backs

    # bet matched
    cache.update(stream_decode(OCMS_SAMPLE[1]))
    order = cache.orders["1.102151675"][6113662].executed_orders[10822867886]
    assert order.execution_complete
    assert order.matched_date
    assert order.size_matched == size_requested
    assert order.size_remaining == 0
    assert order.average_price_matched == 12
    assert cache.orders["1.102151675"][6113662].matched_backs[12] == 2

    # another runner was removed and the reduction factor was applied to the order
    cache.update(stream_decode(OCMS_SAMPLE[2]))
    order = cache.orders["1.102151675"][6113662].executed_orders[10822867886]
    assert order.average_price_matched == 9.47
    assert cache.orders["1.102151675"][6113662].matched_backs[9.47] == 2
    assert len(cache.orders["1.102151675"][6113662].matched_backs) == 1
