"""
Exchange stream cache for market and order data.

This cache implementation tries to be efficient and minimalistic by using the following principles:
- Use builtin data structures whenever possible
- Minimize creation and allocation of new objects
- Avoid any kind of sorting

Though, there is probably quite some room for further optimizations.
"""

from collections import defaultdict
from typing import Optional, Union

from betfair_parser.spec.streaming import (
    LPV,
    MCM,
    OCM,
    PV,
    ChangeType,
    MatchedOrder,
    Order,
    OrderRunnerChange,
    RunnerChange,
    SegmentType,
)


def ladder_update_lpv(ladder: dict[int, LPV], lpvs: list[LPV]) -> None:
    for lpv in lpvs:
        if not lpv.volume:
            ladder.pop(lpv.level, None)
        else:
            ladder[lpv.level] = lpv


def ladder_update_pv(ladder: dict[float, float], pvs: list[PV]) -> None:
    for pv in pvs:
        if not pv.volume:
            ladder.pop(pv.price, None)
        else:
            ladder[pv.price] = pv.volume


def ladder_update_mo(ladder: dict[float, float], mos: list[MatchedOrder]) -> None:
    for mo in mos:
        if not mo.size:
            ladder.pop(mo.price, None)
        else:
            ladder[mo.price] = mo.size


class RunnerOrderBook:
    __slots__ = (
        "available_to_back",
        "available_to_lay",
        "best_available_to_back",
        "best_available_to_lay",
        "best_display_available_to_back",
        "best_display_available_to_lay",
        "starting_price_back",
        "starting_price_lay",
        "starting_price_near",
        "starting_price_far",
        "traded",
        "last_traded_price",
        "total_volume",
        "handicap",
    )

    def __init__(self) -> None:
        self.available_to_back: dict[float, float] = {}
        self.available_to_lay: dict[float, float] = {}
        self.best_available_to_back: dict[int, LPV] = {}
        self.best_available_to_lay: dict[int, LPV] = {}
        self.best_display_available_to_back: dict[int, LPV] = {}
        self.best_display_available_to_lay: dict[int, LPV] = {}
        self.starting_price_back: dict[float, float] = {}
        self.starting_price_lay: dict[float, float] = {}
        self.starting_price_near: Optional[float] = None
        self.starting_price_far: Optional[float] = None
        self.traded: dict[float, float] = {}
        self.last_traded_price: Optional[float] = None
        self.total_volume: Optional[float] = None
        self.handicap: Optional[float] = None

    def update(self, rc: RunnerChange) -> None:
        if rc.atb:
            ladder_update_pv(self.available_to_back, rc.atb)
        if rc.atl:
            ladder_update_pv(self.available_to_lay, rc.atl)
        if rc.batb:
            ladder_update_lpv(self.best_available_to_back, rc.batb)
        if rc.batl:
            ladder_update_lpv(self.best_available_to_lay, rc.batl)
        if rc.bdatb:
            ladder_update_lpv(self.best_display_available_to_back, rc.bdatb)
        if rc.bdatl:
            ladder_update_lpv(self.best_display_available_to_lay, rc.bdatl)
        if rc.spb:
            ladder_update_pv(self.starting_price_back, rc.spb)
        if rc.spl:
            ladder_update_pv(self.starting_price_lay, rc.spl)
        if rc.spn:
            self.starting_price_near = rc.spn
        if rc.spf:
            self.starting_price_far = rc.spf
        if rc.trd:
            ladder_update_pv(self.traded, rc.trd)
        if rc.ltp:
            self.last_traded_price = rc.ltp
        if rc.tv:
            self.total_volume = rc.tv
        if rc.hc:
            self.handicap = rc.hc

    def __repr__(self) -> str:
        data = {}
        for key in self.__slots__:
            val = getattr(self, key, None)
            if not val:
                continue
            if isinstance(val, dict):
                if key in ("available_to_back", "available_to_lay"):
                    val = "[" + ", ".join(f"{price:.4g}:{volume:.2f}" for price, volume in sorted(val.items())) + "]"
                else:
                    val = "[" + ", ".join(f"{lpv.price:.4g}:{lpv.volume:.2f}" for _, lpv in sorted(val.items())) + "]"
            elif isinstance(val, float):
                val = f"{val:.2f}"
            else:
                val = str(val)
            data[key] = val
        fields = ", ".join(f"{key}={val}" for key, val in sorted(data.items()))
        return f"<{type(self).__name__}{' ' if fields else ''}{fields}>"


class ChangeCache:
    clk: Optional[str] = None
    initial_clk: Optional[str] = None
    publish_time: Optional[int] = None
    stream_unreliable: Optional[bool] = False
    conflate_ms: Optional[int] = None

    def update_meta(self, msg: Union[MCM, OCM]) -> None:
        if msg.initial_clk:
            self.initial_clk = msg.initial_clk
        if msg.clk:
            self.clk = msg.clk
        if msg.conflate_ms:
            self.conflate_ms = msg.conflate_ms
        self.publish_time = msg.pt
        self.stream_unreliable = msg.stream_unreliable
        if msg.ct == ChangeType.SUB_IMAGE and not msg.segment_type or msg.segment_type == SegmentType.SEG_START:
            self.clear()

    def clear(self) -> None:
        return


class MarketCache(ChangeCache):
    """
    Market subscriptions are always in the underlying exchange currency - GBP. The default roll-up for GBP
    is £1 for batb / batl and bdatb / bdatl, This means that stakes of less than £1 (or currency
    equivalent) are rolled up to the next available price on the odds ladder. For atb / atl there is
    no roll-up. Available volume is displayed at all prices including those with less than £2 available.
    """

    def __init__(self):
        self.order_book: defaultdict[str, defaultdict] = defaultdict(lambda: defaultdict(RunnerOrderBook))
        self.market_definitions = {}

    def clear(self) -> None:
        self.order_book.clear()
        self.market_definitions.clear()

    def update(self, mcm: MCM) -> None:
        self.update_meta(mcm)
        if mcm.is_heartbeat:
            return
        for mc in mcm.mc:
            if mc.img:
                self.order_book.pop(mc.id, None)
            if mc.market_definition:
                self.market_definitions[mc.id] = mc.market_definition
            if not mc.rc:
                continue
            for rc in mc.rc:
                self.order_book[mc.id][rc.id].update(rc)


class RunnerOrders:
    """
    New subscriptions: Will receive an initial image with only E - Executable orders (unmatched).
    Live subscriptions: Will receive a transient of the order to EC - Execution Complete as the
    order transits into that state (allowing you to remove the order from your cache).

    Please note: EXECUTION_COMPLETE (fully matched) orders are only returned when transitioning from
    EXECUTABLE to EXECUTION_COMPLETE. The full details of EXECUTION_COMPLETE orders can only be viewed
    using listCurrentOrders/listMarketBook using orderProjections.
    """

    __slots__ = (
        "matched_backs",
        "matched_lays",
        "unmatched_orders",
        "executed_orders",
        "handicap",
    )

    def __init__(self) -> None:
        self.matched_backs: dict[float, float] = {}
        self.matched_lays: dict[float, float] = {}
        self.unmatched_orders: dict[int, Order] = {}
        self.executed_orders: dict[int, Order] = {}  # Does only contain recently completed orders
        self.handicap: Optional[float] = None

    def update(self, orc: OrderRunnerChange) -> None:
        if orc.hc:
            self.handicap = orc.hc
        if orc.uo:
            for uo in orc.uo:
                if uo.execution_complete:
                    self.unmatched_orders.pop(uo.id, None)
                    self.executed_orders[uo.id] = uo
                else:
                    self.unmatched_orders[uo.id] = uo
        if orc.mb:
            ladder_update_mo(self.matched_backs, orc.mb)
        if orc.ml:
            ladder_update_mo(self.matched_backs, orc.ml)


class OrderCache(ChangeCache):
    """
    Order subscriptions are provided in the currency of the account that the orders are placed in.
    """

    def __init__(self):
        self.orders: defaultdict[str, defaultdict] = defaultdict(lambda: defaultdict(RunnerOrders))

    def clear(self) -> None:
        self.orders.clear()

    def update(self, ocm: OCM) -> None:
        self.update_meta(ocm)
        if ocm.is_heartbeat:
            return

        for oc in ocm.oc:
            if oc.full_image:
                self.orders.pop(oc.id, None)
            if oc.closed:
                # TODO: Call some hooks?
                self.orders.pop(oc.id, None)
            for orc in oc.orc:
                if orc.full_image:
                    self.orders[oc.id].pop(orc.id, None)
                self.orders[oc.id][orc.id].update(orc)
