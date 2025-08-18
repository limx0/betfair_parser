from typing import Annotated, Literal

import msgspec

from betfair_parser.spec.betting.enums import (
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
)
from betfair_parser.spec.streaming.enums import LapseStatusReasonCode, MarketDataFilterFields


StreamRef = int | str

# Request objects


class MarketFilter(BaseMessage, frozen=True):
    betting_types: Set[MarketBettingType] | None = None  # Match the betting type of the market
    bsp_market: bool | None = None  # If set, restrict to BSP or non-BSP markets only. If unset, return both
    country_codes: Set[str] | None = None  # Restrict to specified country or countries. Defaults to 'GB' on error
    event_ids: Set[EventId] | None = None  # Restrict markets by the event id associated with the market
    event_type_ids: Set[EventTypeId] | None = None  # Restrict markets by event type associated with the market
    market_ids: Set[MarketId] | None = None  # If no marketIds passed user will be subscribed to all markets
    market_types: Set[MarketTypeCode] | None = None  # Restrict to markets that match the type of the market
    race_types: Set[str] | None = None  # Harness, Flat, Hurdle, Chase, Bumper, NH Flat, Steeple or NO_VALUE
    turn_in_play_enabled: bool | None = None  # If set, restrict to turn-inplay or non-inplay markets. Both if unset
    venues: Set[Venue] | None = None  # Restrict by the venue associated with the market. Only for horse racing


class MarketDataFilter(BaseMessage, frozen=True):
    fields: Set[MarketDataFilterFields] | None = None
    ladder_levels: int | None = None


class OrderFilter(BaseMessage, frozen=True):
    include_overall_position: bool = True  # Return overall position (See: OrderRunnerChange.mb / OrderRunnerChange.ml)
    customer_strategy_refs: Set[str] | None = None  # Restricts to specified customerStrategyRefs

    # Returns strategy positions (See: OrderRunnerChange.smc=Map<customerStrategyRef, StrategyMatchChange>)
    # these are sent in delta format as per overall position
    partition_matched_by_strategy_ref: bool = False

    # Internal use only & should not be set on your filter (your subscription is already locked to your account).
    # If set subscription will fail.
    account_ids: Set[int] | None = None


# Response objects


class RunnerDefinition(BaseMessage, frozen=True):
    sort_priority: int
    id: SelectionId
    name: str | None = None
    hc: Handicap | None = None
    status: RunnerStatus | None = None
    adjustment_factor: float | None = None
    bsp: float | None = None
    removal_date: Date | None = None

    @property
    def handicap(self):
        """The handicap of the runner (selection) (None if not applicable)"""
        return self.hc


class KeyLineSelection(BaseMessage, frozen=True):
    id: int
    hc: float


class KeyLineDefinition(BaseMessage, frozen=True):
    kl: list[KeyLineSelection]


class PriceLadderDefinition(BaseMessage, frozen=True):
    type: PriceLadderType


class MarketDefinition(BaseMessage, kw_only=True, frozen=True):
    bet_delay: int
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

    # For Handicap and Line markets, the lines available on this market will be between the range of
    # lineMinUnit and lineMaxUnit, in increments of the lineInterval value. e.g. If unit is runs,
    # lineMinUnit=10, lineMaxUnit=20 and lineInterval=0.5, then valid lines include 10, 10.5, 11, 11.5 up to 20 runs.
    line_interval: float | None = None
    # For Handicap and Line markets, the maximum value for the outcome, in market units for this market (eg 100 runs).
    line_max_unit: float | None = None
    # For Handicap and Line markets, the minimum value for the outcome, in market units for this market (eg 0 runs).
    line_min_unit: float | None = None

    market_base_rate: float | None = None
    market_id: MarketId | None = None  # Undocumented, but occasionally present
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
    atb: list[AvailableToBack] | None = None
    atl: list[AvailableToLay] | None = None
    batb: list[BestAvailableToBack] | None = None
    batl: list[BestAvailableToLay] | None = None
    bdatb: list[BestDisplayAvailableToBack] | None = None
    bdatl: list[BestDisplayAvailableToLay] | None = None
    spb: list[StartingPriceBack] | None = None  # Starting Price (Available To) Back
    spl: list[StartingPriceLay] | None = None  # Starting Price (Available To) Lay
    spn: float | None = None  # Starting Price Near
    spf: float | None = None  # Starting Price Far
    trd: list[Trade] | None = None  # Traded
    ltp: float | None = None  # Last Traded Price
    tv: float | None = None  # Total Volume
    hc: Handicap | None = None

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

    @property
    def handicap(self):
        """The handicap of the runner (selection) (None if not applicable)"""
        return self.hc


class MarketChange(BaseMessage, kw_only=True, frozen=True):
    id: MarketId
    rc: list[RunnerChange] | None = None  # Runner Changes
    con: bool | None = None  # Conflated
    img: bool = False  # Image
    market_definition: MarketDefinition | None = None
    tv: float | None = None  # Traded Volume

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
    p: float  # Price
    s: float  # Size
    # Side of the order. For Line markets a 'B' bet refers to a SELL line and an 'L' bet refers to a BUY line.
    side: Literal["B", "L"]
    status: Literal["E", "EC"]  # Status of the order (E = EXECUTABLE, EC = EXECUTION_COMPLETE)
    pt: Literal["L", "P", "MOC"]  # Persistence Type
    ot: Literal["L", "MOC", "LOC"]  # Order Type - codespell-ignore
    pd: int  # Placed Date
    bsp: float | None = None  # BSP Liability
    rfo: str | None = None  # Order Reference
    rfs: str | None = None  # Strategy Reference
    rc: str | None = None  # Regulator Code
    rac: str | None = None  # Regulator Auth Code
    # TODO: convert int(ms) into datetime for dates??
    md: int | None = None  # Matched Date
    cd: int | None = None  # Cancelled Date
    ld: int | None = None  # Lapsed Date
    avp: float | None = None  # Average Price Matched
    sm: float | None = None  # Size Matched
    sr: float | None = None  # Size Remaining
    sl: float | None = None  # Size Lapsed
    sc: float | None = None  # Size Cancelled
    sv: float | None = None  # Size Voided
    lsrc: LapseStatusReasonCode | None = None

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

    @property
    def bet_id(self):
        # interchangeability with betting.Order
        return self.id

    avg_price_matched = average_price_matched  # interchangeability with betting.Order


class MatchedOrder(BaseMessage, array_like=True, frozen=True):
    price: Price
    size: Size


class StrategyMatchChange(BaseMessage, frozen=True):
    mb: list[MatchedOrder] | None = None  # Matched Backs
    ml: list[MatchedOrder] | None = None  # Matched Lays

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
    mb: list[MatchedOrder] | None = None  # Matched Backs
    ml: list[MatchedOrder] | None = None  # Matched Lays
    smc: dict[str, StrategyMatchChange] | None = None  # Strategy Matches
    uo: list[Order] | None = None  # Unmatched Orders

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
