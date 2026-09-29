from typing import Annotated, Literal

import msgspec

from betfair_parser.spec.betting.enums import (
    BetDelayModel,
    MarketBettingType,
    MarketStatus,
    MarketTypeCode,
    PriceLadderType,
    RunnerStatus,
)
from betfair_parser.spec.common import (
    BaseMessage,
    BetId,
    CompetitionId,
    Date,
    EventId,
    EventTypeId,
    EventTypeIdCode,
    Handicap,
    MarketId,
    Price,
    RegulatorCode,
    SelectionId,
    Set,
    Size,
    Venue,
    doc,
)
from betfair_parser.spec.streaming.enums import LapseStatusReasonCode, MarketDataFilterFields


type StreamRef = int | str

# Request objects


class MarketFilter(BaseMessage, frozen=True):
    bet_delay_models: Annotated[
        Set[BetDelayModel] | None,
        doc("Indicates which bet delay models are applied to a market"),
    ] = None
    betting_types: Annotated[Set[MarketBettingType] | None, doc("Match the betting type of the market")] = None
    bsp_market: Annotated[
        bool | None,
        doc("If set, restrict to BSP or non-BSP markets only. If unset, return both"),
    ] = None
    country_codes: Annotated[
        Set[str] | None,
        doc("Restrict to specified country or countries. Defaults to 'GB' on error"),
    ] = None
    event_ids: Annotated[Set[EventId] | None, doc("Restrict markets by the event id associated with the market")] = None
    event_type_ids: Annotated[
        Set[EventTypeId] | None,
        doc("Restrict markets by event type associated with the market"),
    ] = None
    market_ids: Annotated[
        Set[MarketId] | None,
        doc("If no marketIds passed user will be subscribed to all markets"),
    ] = None
    market_types: Annotated[
        Set[MarketTypeCode] | None,
        doc("Restrict to markets that match the type of the market"),
    ] = None
    race_types: Annotated[
        Set[str] | None,
        doc("Harness, Flat, Hurdle, Chase, Bumper, NH Flat, Steeple or NO_VALUE"),
    ] = None
    turn_in_play_enabled: Annotated[
        bool | None,
        doc("If set, restrict to turn-inplay or non-inplay markets. Both if unset"),
    ] = None
    venues: Annotated[
        Set[Venue] | None,
        doc("Restrict by the venue associated with the market. Only for horse racing"),
    ] = None


class MarketDataFilter(BaseMessage, frozen=True):
    fields: Set[MarketDataFilterFields] | None = None
    ladder_levels: int | None = None


class OrderFilter(BaseMessage, frozen=True):
    include_overall_position: Annotated[
        bool,
        doc("Return overall position (See: OrderRunnerChange.mb / OrderRunnerChange.ml)"),
    ] = True
    customer_strategy_refs: Annotated[Set[str] | None, doc("Restricts to specified customerStrategyRefs")] = None

    partition_matched_by_strategy_ref: Annotated[
        bool,
        doc(
            "Returns strategy positions (See: OrderRunnerChange.smc=Map<customerStrategyRef, StrategyMatchChange>) "
            "these are sent in delta format as per overall position"
        ),
    ] = False

    account_ids: Annotated[
        Set[int] | None,
        doc(
            "Internal use only & should not be set on your filter (your subscription is already locked to your "
            "account). If set subscription will fail."
        ),
    ] = None


# Response objects


class RunnerDefinition(BaseMessage, frozen=True):
    sort_priority: int
    id: SelectionId
    hc: Handicap | None = None
    name: str | None = None
    status: RunnerStatus | None = None
    adjustment_factor: float | None = None
    bsp: float | None = None
    removal_date: Date | None = None

    @property
    def selection_id(self):
        return self.id

    @property
    def handicap(self):
        """The handicap of the runner (selection) (None if not applicable)"""
        return self.hc


class KeyLineSelection(BaseMessage, frozen=True):
    id: SelectionId
    hc: Handicap

    @property
    def selection_id(self):
        return self.id

    @property
    def handicap(self):
        """The handicap of the runner (selection) (None if not applicable)"""
        return self.hc


class KeyLineDefinition(BaseMessage, frozen=True):
    kl: list[KeyLineSelection]


class PriceLadderDefinition(BaseMessage, frozen=True):
    type: PriceLadderType


class MarketDefinition(BaseMessage, kw_only=True, frozen=True):
    bet_delay: int
    bet_delay_models: Annotated[
        list[BetDelayModel] | None,
        doc("Indicates which bet delay models are applied to a market"),
    ] = None
    betting_type: MarketBettingType
    bsp_market: bool
    bsp_reconciled: bool
    competition_id: CompetitionId | None = None
    competition_name: str | None = None
    complete: bool
    country_code: str | None = None
    cross_matching: bool
    discount_allowed: bool | None = None
    each_way_divisor: float | None = None
    event_id: EventId
    event_name: str | None = None
    event_type_id: EventTypeIdCode
    in_play: bool
    key_line_definition: KeyLineDefinition | None = None

    line_interval: Annotated[
        float | None,
        doc(
            "For Handicap and Line markets, the lines available on this market will be between the range of "
            "lineMinUnit and lineMaxUnit, in increments of the lineInterval value. e.g. If unit is runs, "
            "lineMinUnit=10, lineMaxUnit=20 and lineInterval=0.5, then valid lines include 10, 10.5, 11, 11.5 up to 20 "
            "runs."
        ),
    ] = None
    line_max_unit: Annotated[
        float | None,
        doc(
            "For Handicap and Line markets, the maximum value for the outcome, in market units for this market (eg 100 "
            "runs)."
        ),
    ] = None
    line_min_unit: Annotated[
        float | None,
        doc(
            "For Handicap and Line markets, the minimum value for the outcome, in market units for this market (eg 0 "
            "runs)."
        ),
    ] = None

    market_base_rate: float | None = None
    market_id: Annotated[MarketId | None, doc("Undocumented, but occasionally present")] = None
    market_name: str | None = None
    market_time: Date
    market_type: str
    name: str | None = None
    number_of_active_runners: int
    number_of_winners: int
    open_date: Date | None = None
    persistence_enabled: bool
    price_ladder_definition: PriceLadderDefinition | PriceLadderType | None = None
    race_type: str | None = None
    regulators: list[RegulatorCode]
    runners: list[RunnerDefinition]
    runners_voidable: bool
    settled_time: Date | None = None
    status: MarketStatus
    suspend_time: Date
    suspend_reason: str | None = None
    timezone: str | None = None
    turn_in_play_enabled: bool
    venue: str | None = None
    version: int | None = None

    @property
    def event_type_name(self) -> str:
        return self.event_type_id.name


class PV(BaseMessage, array_like=True, frozen=True):
    """Price-Volume pair"""

    price: Price
    volume: Size


class LPV(BaseMessage, array_like=True, frozen=True):
    """Level-Price-Volume triple"""

    level: int
    price: Price
    volume: Size


AvailableToBack = Annotated[PV, msgspec.Meta(title="AvailableToBack")]
AvailableToLay = Annotated[PV, msgspec.Meta(title="AvailableToLay")]
BestAvailableToBack = Annotated[LPV, msgspec.Meta(title="BestAvailableToBack")]
BestAvailableToLay = Annotated[LPV, msgspec.Meta(title="BestAvailableToLay")]
BestDisplayAvailableToBack = Annotated[LPV, msgspec.Meta(title="BestDisplayAvailableToBack")]
BestDisplayAvailableToLay = Annotated[LPV, msgspec.Meta(title="BestDisplayAvailableToLay")]
StartingPriceBack = Annotated[PV, msgspec.Meta(title="StartingPriceBack")]
StartingPriceLay = Annotated[PV, msgspec.Meta(title="StartingPriceLay")]
Trade = Annotated[PV, msgspec.Meta(title="Trade")]


class RunnerChange(BaseMessage, frozen=True):
    id: SelectionId
    hc: Handicap | None = None
    atb: list[AvailableToBack] | None = None
    atl: list[AvailableToLay] | None = None
    batb: list[BestAvailableToBack] | None = None
    batl: list[BestAvailableToLay] | None = None
    bdatb: list[BestDisplayAvailableToBack] | None = None
    bdatl: list[BestDisplayAvailableToLay] | None = None
    spb: Annotated[list[StartingPriceBack] | None, doc("Starting Price (Available To) Back")] = None
    spl: Annotated[list[StartingPriceLay] | None, doc("Starting Price (Available To) Lay")] = None
    spn: Annotated[float | None, doc("Starting Price Near")] = None
    spf: Annotated[float | None, doc("Starting Price Far")] = None
    trd: Annotated[list[Trade] | None, doc("Traded")] = None
    ltp: Annotated[float | None, doc("Last Traded Price")] = None
    tv: Annotated[float | None, doc("Total Volume")] = None

    @property
    def selection_id(self):
        return self.id

    @property
    def handicap(self):
        """The handicap of the runner (selection) (None if not applicable)"""
        return self.hc

    @property
    def available_to_back(self):
        """PriceVol tuple delta of price changes (0 vol is remove)"""
        return self.atb

    @property
    def available_to_lay(self):
        """PriceVol tuple delta of price changes (0 vol is remove)"""
        return self.atl

    @property
    def best_available_to_back(self):
        """LevelPriceVol triple delta of price changes, keyed by level (0 vol is remove)"""
        return self.batb

    @property
    def best_available_to_lay(self):
        """LevelPriceVol triple delta of price changes, keyed by level (0 vol is remove)"""
        return self.batl

    @property
    def best_display_available_to_back(self):
        """LevelPriceVol triple delta of price changes, keyed by level (0 vol is remove) (includes virtual prices)"""
        return self.bdatb

    @property
    def best_display_available_to_lay(self):
        """LevelPriceVol triple delta of price changes, keyed by level (0 vol is remove) (includes virtual prices)"""
        return self.bdatl

    @property
    def starting_price_back(self):
        """PriceVol tuple delta of price changes (0 vol is remove)"""
        return self.spb

    @property
    def starting_price_lay(self):
        """PriceVol tuple delta of price changes (0 vol is remove)"""
        return self.spl

    @property
    def starting_price_near(self):
        """The near starting price (or None if un-changed)"""
        return self.spn

    @property
    def starting_price_far(self):
        """The far starting price (or None if un-changed)"""
        return self.spf

    @property
    def traded(self):
        """PriceVol tuple delta of price changes (0 vol is remove)"""
        return self.trd

    @property
    def last_traded_price(self):
        """The last traded price (or None if un-changed)"""
        return self.ltp

    @property
    def total_volume(self):
        """The total amount matched. This value is truncated at 2dp."""
        return self.tv


class MarketChange(BaseMessage, kw_only=True, frozen=True):
    id: MarketId
    rc: Annotated[list[RunnerChange] | None, doc("Runner Changes")] = None
    con: Annotated[bool | None, doc("Conflated")] = None
    img: Annotated[bool, doc("Image")] = False
    market_definition: MarketDefinition | None = None
    tv: Annotated[float | None, doc("Traded Volume")] = None

    @property
    def runner_changes(self):
        """Not present if market_definition is sent"""
        return self.rc

    @property
    def conflated(self):
        """Have more than a single change been combined (or None if not conflated)"""
        return self.con

    @property
    def image(self):
        """Replace existing prices / data with the data supplied: it is not a delta"""
        return self.img

    @property
    def traded_volume(self):
        """Total amount matched across the market. None if un-changed"""
        return self.tv


class Order(BaseMessage, frozen=True):
    id: BetId
    p: Price
    s: Size
    side: Annotated[
        Literal["B", "L"],
        doc("Side of the order. For Line markets a 'B' bet refers to a SELL line and an 'L' bet refers to a BUY line."),
    ]
    status: Annotated[Literal["E", "EC"], doc("Status of the order (E = EXECUTABLE, EC = EXECUTION_COMPLETE)")]
    pt: Annotated[Literal["L", "P", "MOC"], doc("Persistence Type")]
    ot: Annotated[Literal["L", "MOC", "LOC"], doc("Order Type")]  # codespell-ignore
    pd: Annotated[int, doc("Placed Date")]
    bsp: Annotated[float | None, doc("BSP Liability")] = None
    rfo: Annotated[str | None, doc("Order Reference")] = None
    rfs: Annotated[str | None, doc("Strategy Reference")] = None
    rc: Annotated[str | None, doc("Regulator Code")] = None
    rac: Annotated[str | None, doc("Regulator Auth Code")] = None
    # TODO: convert int(ms) into datetime for dates??
    md: Annotated[int | None, doc("Matched Date")] = None
    cd: Annotated[int | None, doc("Cancelled Date")] = None
    ld: Annotated[int | None, doc("Lapsed Date")] = None
    avp: Annotated[Price | None, doc("Average Price Matched")] = None
    sm: Annotated[Size | None, doc("Size Matched")] = None
    sr: Annotated[Size | None, doc("Size Remaining")] = None
    sl: Annotated[Size | None, doc("Size Lapsed")] = None
    sc: Annotated[Size | None, doc("Size Cancelled")] = None
    sv: Annotated[Size | None, doc("Size Voided")] = None
    lsrc: LapseStatusReasonCode | None = None

    @property
    def bet_id(self):
        # interchangeability with betting.Order
        return self.id

    @property
    def execution_complete(self) -> bool:
        return self.status == "EC"

    @property
    def price(self):
        """
        The original placed price of the order. Line markets operate at even-money odds of 2.0.
        However, price for these markets refers to the line positions available as defined by the markets
        min-max range and interval steps
        """
        return self.p

    @property
    def size(self):
        """The original placed size of the order"""
        return self.s

    @property
    def persistence_type(self):
        """If the order will persist at in play or not (L=LAPSE, P=PERSIST, MOC=Market On Close)"""
        return self.pt

    @property
    def order_type(self):
        """The type of the order (L = LIMIT, MOC = MARKET_ON_CLOSE, LOC = LIMIT_ON_CLOSE)"""
        return self.ot  # codespell-ignore

    @property
    def placed_date(self):
        """The date the order was placed (in millis since epoch) that the changes were generated"""
        return self.pd

    @property
    def bsp_liability(self):
        """The BSP liability of the order (None if the order is not a BSP order)"""
        return self.bsp

    @property
    def customer_order_ref(self):
        """The customer's order reference for this order (None if one was not set)"""
        return self.rfo

    @property
    def customer_strategy_ref(self):
        """The customer's strategy reference for this order (empty string if one was not set)"""
        return self.rfs

    @property
    def regulator_code(self):
        """The regulator of the order"""
        return self.rc

    @property
    def regulator_auth_code(self):
        """The auth code returned by the regulator"""
        return self.rac

    @property
    def matched_date(self):
        """The date the order was matched (None if the order is not matched)"""
        return self.md

    @property
    def cancelled_date(self):
        """The date the order was cancelled (None if the order is not cancelled)"""
        return self.cd

    @property
    def lapsed_date(self):
        """The date the order was lapsed (None if the order is not lapsed)"""
        return self.ld

    @property
    def average_price_matched(self):
        """
        The average price the order was matched at (None if the order is not matched). This value
        is not meaningful for activity on Line markets and is not guaranteed to be returned or
        maintained for these markets.
        """
        return self.avp

    avg_price_matched = average_price_matched  # interchangeability with betting.Order

    @property
    def size_matched(self):
        """The amount of the order that has been matched"""
        return self.sm

    @property
    def size_remaining(self):
        """The amount of the order that is remaining unmatched"""
        return self.sr

    @property
    def size_lapsed(self):
        """The amount of the order that has been lapsed"""
        return self.sl

    @property
    def size_cancelled(self):
        """The amount of the order that has been cancelled"""
        return self.sc

    @property
    def size_voided(self):
        """The amount of the order that has been voided"""
        return self.sv

    @property
    def lapse_status_reason_code(self):
        """The reason that some or all of this order has been lapsed (None if no portion of the order is lapsed"""
        return self.lsrc


class MatchedOrder(BaseMessage, array_like=True, frozen=True):
    price: Price
    size: Size


class StrategyMatchChange(BaseMessage, frozen=True):
    mb: Annotated[list[MatchedOrder] | None, doc("Matched Backs")] = None
    ml: Annotated[list[MatchedOrder] | None, doc("Matched Lays")] = None

    @property
    def matched_backs(self):
        """Matched amounts by distinct matched price on the Back side for this strategy"""
        return self.mb

    @property
    def matched_lays(self):
        """Matched amounts by distinct matched price on the Lay side for this strategy"""
        return self.ml


class OrderRunnerChange(BaseMessage, frozen=True):
    id: SelectionId
    full_image: bool | None = False
    hc: Handicap | None = None
    mb: Annotated[list[MatchedOrder] | None, doc("Matched Backs")] = None
    ml: Annotated[list[MatchedOrder] | None, doc("Matched Lays")] = None
    smc: Annotated[dict[str, StrategyMatchChange] | None, doc("Strategy Matches")] = None
    uo: Annotated[list[Order] | None, doc("Unmatched Orders")] = None

    @property
    def selection_id(self):
        return self.id

    @property
    def handicap(self):
        """The handicap of the runner (selection) (None if not applicable)"""
        return self.hc

    @property
    def matched_backs(self):
        """Matched amounts by distinct matched price on the Back side for this runner (selection)"""
        return self.mb

    @property
    def matched_lays(self):
        """Matched amounts by distinct matched price on the Lay side for this runner (selection)"""
        return self.ml

    @property
    def strategy_matches(self):
        """Matched Backs and Matched Lays grouped by strategy reference"""
        return self.smc

    @property
    def unmatched_orders(self):
        """Orders on this runner (selection) that are not fully matched"""
        return self.uo


class OrderMarketChange(BaseMessage, kw_only=True, frozen=True):
    id: MarketId
    account_id: int | None = None
    closed: bool | None = None
    full_image: bool | None = False
    orc: list[OrderRunnerChange] | None = None

    @property
    def order_runner_changes(self):
        """A list of changes to orders on a selection"""
        return self.orc
