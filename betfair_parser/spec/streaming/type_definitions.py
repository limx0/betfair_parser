from typing import Annotated, Literal, Optional, Union

import msgspec

from betfair_parser.spec.betting.enums import MarketBettingType, MarketStatus, MarketTypeCode, RunnerStatus
from betfair_parser.spec.common import (
    BaseMessage,
    BetId,
    CompetitionId,
    Date,
    EventId,
    EventTypeIdCode,
    Handicap,
    MarketId,
    Price,
    RegulatorCode,
    SelectionId,
    Size,
    Venue,
)
from betfair_parser.spec.streaming.enums import LapseStatusReasonCode, MarketDataFilterFields, PriceLadderDefinitionType


# Request objects


class MarketFilter(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    betting_types: Optional[list[MarketBettingType]] = None  # Match the betting type of the market
    bsp_market: Optional[bool] = None  # If set, restrict to BSP or non-BSP markets only. If unset, return both
    country_codes: Optional[list[str]] = None  # Restrict to specified country or countries. Defaults to 'GB' on error
    event_ids: Optional[list[EventId]] = None  # Restrict markets by the event id associated with the market
    event_type_ids: Optional[list[EventTypeIdCode]] = None  # Restrict markets by event type associated with the market
    market_ids: Optional[list[MarketId]] = None  # If no marketIds passed user will be subscribed to all markets
    market_types: Optional[list[MarketTypeCode]] = None  # Restrict to markets that match the type of the market
    race_types: Optional[list[str]] = None  # Harness, Flat, Hurdle, Chase, Bumper, NH Flat, Steeple or NO_VALUE
    turn_in_play_enabled: Optional[bool] = None  # If set, restrict to turn-inplay or non-inplay markets. Both if unset
    venues: Optional[list[Venue]] = None  # Restrict by the venue associated with the market. Only for horse racing


class MarketDataFilter(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    fields: Optional[list[MarketDataFilterFields]] = None
    ladder_levels: Optional[int] = None


class OrderFilter(BaseMessage, frozen=True):
    include_overall_position: bool = True  # Return overall position (See: OrderRunnerChange.mb / OrderRunnerChange.ml)
    customer_strategy_refs: Optional[list[str]] = None  # Restricts to specified customerStrategyRefs

    # Returns strategy positions (See: OrderRunnerChange.smc=Map<customerStrategyRef, StrategyMatchChange>)
    # these are sent in delta format as per overall position
    partition_matched_by_strategy_ref: bool = False

    # Internal use only & should not be set on your filter (your subscription is already locked to your account).
    # If set subscription will fail.
    account_ids: Optional[list[int]] = None


# Response objects


class RunnerDefinition(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    sort_priority: int
    id: SelectionId
    name: Optional[str] = None  # Undefined, but partly present
    hc: Optional[Handicap] = None
    status: Optional[RunnerStatus] = None
    adjustment_factor: Optional[float] = None
    bsp: Optional[float] = None
    removal_date: Optional[Date] = None

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
    type: PriceLadderDefinitionType


class MarketDefinition(BaseMessage, kw_only=True, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    bet_delay: int
    betting_type: MarketBettingType
    bsp_market: bool
    bsp_reconciled: bool
    competition_id: Optional[CompetitionId] = None
    competition_name: Optional[str] = None
    complete: bool
    country_code: Optional[str] = None
    cross_matching: bool
    discount_allowed: Optional[bool] = None
    each_way_divisor: Optional[float] = None
    event_id: EventId
    event_name: Optional[str] = None
    event_type_id: EventTypeIdCode
    in_play: bool
    key_line_definition: Optional[KeyLineDefinition] = None

    # For Handicap and Line markets, the lines available on this market will be between the range of
    # lineMinUnit and lineMaxUnit, in increments of the lineInterval value. e.g. If unit is runs,
    # lineMinUnit=10, lineMaxUnit=20 and lineInterval=0.5, then valid lines include 10, 10.5, 11, 11.5 up to 20 runs.
    line_interval: Optional[float] = None
    # For Handicap and Line markets, the maximum value for the outcome, in market units for this market (eg 100 runs).
    line_max_unit: Optional[float] = None
    # For Handicap and Line markets, the minimum value for the outcome, in market units for this market (eg 0 runs).
    line_min_unit: Optional[float] = None

    market_base_rate: Optional[float]
    market_id: Optional[MarketId] = None
    market_name: Optional[str] = None
    market_time: Date
    market_type: str
    name: Optional[str] = None
    number_of_active_runners: int
    number_of_winners: int
    open_date: Optional[Date] = None
    persistence_enabled: bool
    price_ladder_definition: Optional[Union[PriceLadderDefinition, PriceLadderDefinitionType]] = None
    race_type: Optional[str] = None
    regulators: list[RegulatorCode]
    runners: list[RunnerDefinition]
    runners_voidable: bool
    settled_time: Optional[Date] = None
    status: MarketStatus
    suspend_time: Date
    timezone: Optional[str] = None
    turn_in_play_enabled: bool
    venue: Optional[str] = None
    version: Optional[int] = None

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


class RunnerChange(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    id: SelectionId
    atb: Optional[list[AvailableToBack]] = None
    atl: Optional[list[AvailableToLay]] = None
    batb: Optional[list[BestAvailableToBack]] = None
    batl: Optional[list[BestAvailableToLay]] = None
    bdatb: Optional[list[BestDisplayAvailableToBack]] = None
    bdatl: Optional[list[BestDisplayAvailableToLay]] = None
    spb: Optional[list[StartingPriceBack]] = None  # Starting Price (Available To) Back
    spl: Optional[list[StartingPriceLay]] = None  # Starting Price (Available To) Lay
    spn: Optional[float] = None  # Starting Price Near
    spf: Optional[float] = None  # Starting Price Far
    trd: Optional[list[Trade]] = None  # Traded
    ltp: Optional[float] = None  # Last Traded Price
    tv: Optional[float] = None  # Total Volume
    hc: Optional[Handicap] = None

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


class MarketChange(BaseMessage, kw_only=True, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    id: MarketId
    rc: Optional[list[RunnerChange]] = None  # Runner Changes
    con: Optional[bool] = None  # Conflated
    img: bool = False  # Image
    market_definition: Optional[MarketDefinition] = None
    tv: Optional[float] = None  # Traded Volume

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


class Order(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    id: BetId
    p: float  # Price
    s: float  # Size
    # Side of the order. For Line markets a 'B' bet refers to a SELL line and an 'L' bet refers to a BUY line.
    side: Literal["B", "L"]
    status: Literal["E", "EC"]  # Status of the order (E = EXECUTABLE, EC = EXECUTION_COMPLETE)
    pt: Literal["L", "P", "MOC"]  # Persistence Type
    ot: Literal["L", "MOC", "LOC"]  # Order Type - codespell-ignore
    pd: int  # Placed Date
    bsp: Optional[float] = None  # BSP Liability
    rfo: Optional[str] = None  # Order Reference
    rfs: Optional[str] = None  # Strategy Reference
    rc: Optional[str] = None  # Regulator Code
    rac: Optional[str] = None  # Regulator Auth Code
    # TODO: convert int(ms) into datetime for dates??
    md: Optional[int] = None  # Matched Date
    cd: Optional[int] = None  # Cancelled Date
    ld: Optional[int] = None  # Lapsed Date
    avp: Optional[float] = None  # Average Price Matched
    sm: Optional[float] = None  # Size Matched
    sr: Optional[float] = None  # Size Remaining
    sl: Optional[float] = None  # Size Lapsed
    sc: Optional[float] = None  # Size Cancelled
    sv: Optional[float] = None  # Size Voided
    lsrc: Optional[LapseStatusReasonCode] = None

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
    def order_reference(self):
        """The customer's order reference for this order (None if one was not set)"""
        return self.rfo

    @property
    def strategy_reference(self):
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


class MatchedOrder(BaseMessage, array_like=True, frozen=True):
    price: Price
    size: Size


class StrategyMatchChange(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    mb: Optional[list[MatchedOrder]] = None  # Matched Backs
    ml: Optional[list[MatchedOrder]] = None  # Matched Lays

    @property
    def matched_backs(self):
        """Matched amounts by distinct matched price on the Back side for this strategy"""
        return self.mb

    @property
    def matched_lays(self):
        """Matched amounts by distinct matched price on the Lay side for this strategy"""
        return self.ml


class OrderRunnerChange(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    id: SelectionId
    full_image: Optional[bool] = False
    hc: Optional[Handicap] = None
    mb: Optional[list[MatchedOrder]] = None  # Matched Backs
    ml: Optional[list[MatchedOrder]] = None  # Matched Lays
    smc: Optional[dict[str, StrategyMatchChange]] = None  # Strategy Matches
    uo: Optional[list[Order]] = None  # Unmatched Orders

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


class OrderMarketChange(BaseMessage, kw_only=True, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    id: MarketId
    account_id: Optional[int] = None
    closed: Optional[bool] = None
    full_image: Optional[bool] = False
    orc: Optional[list[OrderRunnerChange]] = None

    @property
    def order_runner_changes(self):
        """A list of changes to orders on a selection"""
        return self.orc
