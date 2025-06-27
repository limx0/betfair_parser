"""
Exchange stream cache for market and order data.

This cache implementation tries to be efficient and minimalistic by using the following principles:
- Use builtin data structures whenever possible
- Minimize creation and allocation of new objects
- Avoid any kind of sorting

Though, there is probably quite some room for further optimizations.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Generic, NamedTuple, TypeAlias, TypeVar

from betfair_parser.spec.streaming import (
    LPV,
    MCM,
    OCM,
    PV,
    ChangeType,
    MarketDefinition,
    MatchedOrder,
    Order,
    OrderRunnerChange,
    RunnerChange,
    SegmentType,
)


class RunnerChangeKey(NamedTuple):
    selection_id: int
    handicap: float


def rc_key(runner_change: RunnerChange | OrderRunnerChange) -> RunnerChangeKey:
    """Asian handicap markets use a combined key to represent all selections in a market."""
    return RunnerChangeKey(runner_change.id, runner_change.hc or 0.0)


V = TypeVar("V")
RunnerChangeKeyTypes: TypeAlias = int | tuple[int, float] | RunnerChangeKey


class SelectionHandicapDict(defaultdict[RunnerChangeKey, V], Generic[V]):
    """
    A defaultdict whose real key type is RunnerChangeKey,
    but which also lets you do d[5] or d[(5,1.0)].
    """

    default_factory: type[V]

    def __init__(self) -> None:
        super().__init__(self.default_factory)

    @staticmethod
    def _normalize(key: RunnerChangeKeyTypes) -> RunnerChangeKey:
        if isinstance(key, RunnerChangeKey):
            return key
        if isinstance(key, tuple):
            return RunnerChangeKey(*key)
        if isinstance(key, int):
            return RunnerChangeKey(key, 0.0)
        raise TypeError(f"Invalid key type: {type(key).__name__}")

    def __getitem__(self, key: RunnerChangeKeyTypes) -> V:
        return super().__getitem__(self._normalize(key))

    def __contains__(self, key: RunnerChangeKeyTypes) -> bool:  # type: ignore[override]
        return super().__contains__(self._normalize(key))

    def __setitem__(self, key: RunnerChangeKeyTypes, value: V) -> None:
        return super().__setitem__(self._normalize(key), value)

    def __delitem__(self, key: RunnerChangeKeyTypes) -> None:
        return super().__delitem__(self._normalize(key))

    def get(self, key: RunnerChangeKeyTypes, default: V | None = None) -> V | None:  # type: ignore[override]
        return super().get(self._normalize(key), default)


PriceVolumeMap: TypeAlias = dict[float, float]
LadderPriceVolumeMap: TypeAlias = dict[int, LPV]


def ladder_update_lpv(ladder: LadderPriceVolumeMap, lpvs: list[LPV]) -> None:
    for lpv in lpvs:
        if not lpv.volume:
            ladder.pop(lpv.level, None)
        else:
            ladder[lpv.level] = lpv


def ladder_update_pv(ladder: PriceVolumeMap, pvs: list[PV]) -> None:
    for pv in pvs:
        if not pv.volume:
            ladder.pop(pv.price, None)
        else:
            ladder[pv.price] = pv.volume


def ladder_update_mo(ladder: PriceVolumeMap, mos: list[MatchedOrder]) -> None:
    for mo in mos:
        if not mo.size:
            ladder.pop(mo.price, None)
        else:
            ladder[mo.price] = mo.size


class BestPriceVolume(NamedTuple):
    back_price: float
    back_volume: float
    lay_price: float
    lay_volume: float


_NO_PRICE = 0.0  # should this be None?
_NO_PRICE_LPV = LPV(0, _NO_PRICE, 0.0)


@dataclass(slots=True)
class RunnerOrderBook:
    """Order book for a runner with all relevant price and volume levels."""

    available_to_back: PriceVolumeMap = field(default_factory=dict)
    available_to_lay: PriceVolumeMap = field(default_factory=dict)

    best_available_to_back: LadderPriceVolumeMap = field(default_factory=dict)
    best_available_to_lay: LadderPriceVolumeMap = field(default_factory=dict)

    best_display_available_to_back: LadderPriceVolumeMap = field(default_factory=dict)
    best_display_available_to_lay: LadderPriceVolumeMap = field(default_factory=dict)

    starting_price_back: PriceVolumeMap = field(default_factory=dict)
    starting_price_lay: PriceVolumeMap = field(default_factory=dict)

    starting_price_near: float | None = None
    starting_price_far: float | None = None

    traded: PriceVolumeMap = field(default_factory=dict)
    last_traded_price: float | None = None
    total_volume: float | None = None

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

    def best_prices(self) -> BestPriceVolume:
        """Extract the best available prices."""

        if self.available_to_back or self.available_to_lay:
            back_price = max(self.available_to_back) if self.available_to_back else _NO_PRICE
            back_volume = self.available_to_back[back_price] if back_price else 0.0
            lay_price = min(self.available_to_lay) if self.available_to_lay else _NO_PRICE
            lay_volume = self.available_to_lay[lay_price] if lay_price else 0.0
            return BestPriceVolume(back_price, back_volume, lay_price, lay_volume)

        if self.best_available_to_back or self.best_available_to_lay:
            blpv = self.best_available_to_back.get(0, _NO_PRICE_LPV)
            llpv = self.best_available_to_lay.get(0, _NO_PRICE_LPV)
            return BestPriceVolume(blpv.price, blpv.volume, llpv.price, llpv.volume)

        if self.best_display_available_to_back or self.best_display_available_to_lay:
            blpv = self.best_display_available_to_back.get(0, _NO_PRICE_LPV)
            llpv = self.best_display_available_to_lay.get(0, _NO_PRICE_LPV)
            return BestPriceVolume(blpv.price, blpv.volume, llpv.price, llpv.volume)

        return BestPriceVolume(_NO_PRICE, 0.0, _NO_PRICE, 0.0)

    def __repr__(self) -> str:
        data: dict[str, str] = {}
        for key in self.__dataclass_fields__:
            val = getattr(self, key)
            if not val:
                continue

            if isinstance(val, dict):
                if key in ("available_to_back", "available_to_lay"):
                    formatted = ", ".join(f"{price:.4g}:{volume:.2f}" for price, volume in sorted(val.items()))
                else:
                    formatted = ", ".join(f"{lpv.price:.4g}:{lpv.volume:.2f}" for _, lpv in sorted(val.items()))
                val_str = f"[{formatted}]"
            elif isinstance(val, float):
                val_str = f"{val:.2f}"
            else:
                val_str = str(val)

            data[key] = val_str

        fields_str = ", ".join(f"{k}={v}" for k, v in sorted(data.items()))
        space = " " if fields_str else ""
        return f"<{type(self).__name__}{space}{fields_str}>"


class ChangeCache:
    clk: str | None = None
    initial_clk: str | None = None
    publish_time: int | None = None
    stream_unreliable: bool | None = False
    conflate_ms: int | None = None

    def update_meta(self, msg: MCM | OCM) -> None:
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
        raise NotImplementedError()


class MarketOrderBook(SelectionHandicapDict[RunnerOrderBook]):
    """Order book for a single market, collecting a bunch of RunnerOrderBooks."""

    default_factory: type = RunnerOrderBook


class MarketSubscriptionCache(ChangeCache):
    """
    Orderbook for all markets of a market change stream.

    Market subscriptions are always in the underlying exchange currency - GBP. The default roll-up for GBP
    is £1 for batb / batl and bdatb / bdatl, This means that stakes of less than £1 (or currency
    equivalent) are rolled up to the next available price on the odds ladder. For atb / atl there is
    no roll-up. Available volume is displayed at all prices including those with less than £2 available.
    """

    def __init__(self):
        self.order_book: defaultdict[str, MarketOrderBook] = defaultdict(MarketOrderBook)
        self.definitions: dict[str, MarketDefinition] = {}

    def clear(self) -> None:
        self.order_book.clear()
        self.definitions.clear()

    def update(self, mcm: MCM) -> None:
        self.update_meta(mcm)
        if mcm.is_heartbeat:
            return
        if not mcm.mc:
            return

        for mc in mcm.mc:
            if mc.img:
                self.order_book.pop(mc.id, None)
            if mc.market_definition:
                self.definitions[mc.id] = mc.market_definition
            if not mc.rc:
                continue
            for rc in mc.rc:
                self.order_book[mc.id][rc_key(rc)].update(rc)


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

    def update(self, orc: OrderRunnerChange) -> None:
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
            ladder_update_mo(self.matched_lays, orc.ml)


class MarketOrders(SelectionHandicapDict[RunnerOrders]):
    """All orders for a single market, collecting a bunch of RunnerOrders."""

    default_factory: type = RunnerOrders


class OrderSubscriptionCache(ChangeCache):
    """
    Order subscriptions are provided in the currency of the account that the orders are placed in.
    """

    def __init__(self):
        self.orders: defaultdict[str, MarketOrders] = defaultdict(MarketOrders)

    def clear(self) -> None:
        self.orders.clear()

    def update(self, ocm: OCM) -> None:
        self.update_meta(ocm)
        if ocm.is_heartbeat:
            return
        if not ocm.oc:
            return

        for oc in ocm.oc:
            if oc.full_image:
                self.orders.pop(oc.id, None)
            if oc.closed:
                self.orders.pop(oc.id, None)
            if not oc.orc:
                # on closed markets
                continue
            for orc in oc.orc:
                orc_key = rc_key(orc)
                if orc.full_image:
                    self.orders[oc.id].pop(orc_key, None)
                self.orders[oc.id][orc_key].update(orc)
