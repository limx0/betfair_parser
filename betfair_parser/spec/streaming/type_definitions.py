from typing import Annotated, Literal, Optional, Union

import msgspec

from betfair_parser.spec.betting.enums import MarketBettingType, MarketStatus, MarketTypeCode, RunnerStatus
from betfair_parser.spec.common import (
    BaseMessage,
    BetId,
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


class MarketFilter(BaseMessage, frozen=True):
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


class MarketDataFilter(BaseMessage, frozen=True):
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


class RunnerDefinition(BaseMessage, frozen=True):
    sort_priority: int
    id: SelectionId
    name: Optional[str] = None  # Undefined, but present
    hc: Optional[Handicap] = None
    status: Optional[RunnerStatus] = None
    adjustment_factor: Optional[float] = None
    bsp: Optional[float] = None
    removal_date: Optional[Date] = None

    @property
    def handicap(self) -> str:
        return str(self.hc or 0.0)

    @property
    def runner_id(self) -> int:
        return self.id


class KeyLineSelection(BaseMessage, frozen=True):
    id: int
    hc: float


class KeyLineDefinition(BaseMessage, frozen=True):
    kl: list[KeyLineSelection]


class PriceLadderDefinition(BaseMessage, frozen=True):
    type: PriceLadderDefinitionType


class MarketDefinition(BaseMessage, kw_only=True, frozen=True):
    bet_delay: int
    betting_type: MarketBettingType
    bsp_market: bool
    bsp_reconciled: bool
    competition_id: Optional[str] = ""
    competition_name: Optional[str] = ""
    complete: bool
    country_code: Optional[str] = None
    cross_matching: bool
    discount_allowed: Optional[bool] = None
    each_way_divisor: Optional[float] = None
    event_id: str
    event_name: Optional[str] = ""
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
    market_id: Optional[str] = ""
    market_name: Optional[str] = ""
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
        return EventTypeIdCode(int(self.event_type_id)).name


class _PriceVolume(BaseMessage, array_like=True, frozen=True):
    price: Price
    volume: Size


class _LevelPriceVolume(BaseMessage, array_like=True, frozen=True):
    level: int
    price: Price
    volume: Size


AvailableToBack = Annotated[_PriceVolume, msgspec.Meta(title="AvailableToBack")]
AvailableToLay = Annotated[_PriceVolume, msgspec.Meta(title="AvailableToLay")]
BestAvailableToBack = Annotated[_LevelPriceVolume, msgspec.Meta(title="BestAvailableToBack")]
BestAvailableToLay = Annotated[_LevelPriceVolume, msgspec.Meta(title="BestAvailableToLay")]
BestDisplayAvailableToBack = Annotated[_LevelPriceVolume, msgspec.Meta(title="BestDisplayAvailableToBack")]
BestDisplayAvailableToLay = Annotated[_LevelPriceVolume, msgspec.Meta(title="BestDisplayAvailableToLay")]
StartingPriceBack = Annotated[_PriceVolume, msgspec.Meta(title="StartingPriceBack")]
StartingPriceLay = Annotated[_PriceVolume, msgspec.Meta(title="StartingPriceLay")]
Trade = Annotated[_PriceVolume, msgspec.Meta(title="Trade")]


class RunnerChange(BaseMessage, frozen=True):
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
    trd: Optional[list[Trade]] = None
    ltp: Optional[float] = None
    tv: Optional[float] = None  # The total amount matched. This value is truncated at 2dp.
    hc: Optional[Handicap] = None


class MarketChange(BaseMessage, kw_only=True, frozen=True):
    id: MarketId
    rc: Optional[list[RunnerChange]] = None  # not presend if market_definition is sent
    con: Optional[bool] = None  # Conflated - have more than a single change been combined (or null if not conflated)
    img: bool = False  # Image - replace existing prices / data with the data supplied: it is not a delta
    market_definition: Optional[MarketDefinition] = None
    tv: Optional[float] = None  # Total amount matched across the market. Null if un-changed


class Order(BaseMessage, frozen=True):
    id: BetId
    # Price - the original placed price of the order. Line markets operate at even-money odds of 2.0.
    # However, price for these markets refers to the line positions available as defined by the markets
    # min-max range and interval steps
    p: float
    # Size - the original placed size of the order
    s: float
    # Side of the order. For Line markets a 'B' bet refers to a SELL line and an 'L' bet refers to a BUY line.
    side: Literal["B", "L"]
    # Status of the order (E = EXECUTABLE, EC = EXECUTION_COMPLETE)
    status: Literal["E", "EC"]
    # Persistence Type - if the order will persist at in play or not (L=LAPSE, P=PERSIST, MOC=Market On Close)
    pt: Literal["L", "P", "MOC"]
    # Order Type - the type of the order (L = LIMIT, MOC = MARKET_ON_CLOSE, LOC = LIMIT_ON_CLOSE)
    ot: Literal["L", "MOC", "LOC"]  # codespell-ignore
    # Placed Date - the date the order was placed (in millis since epoch) that the changes were generated
    pd: int
    # BSP Liability - the BSP liability of the order (null if the order is not a BSP order)
    bsp: Optional[float] = None
    # Order Reference - the customer's order reference for this order (empty string if one was not set)
    rfo: Optional[str] = None
    # Strategy Reference - the customer's strategy reference for this order (empty string if one was not set)
    rfs: Optional[str] = None
    rc: Optional[str] = None  # Regulator Code - the regulator of the order
    rac: Optional[str] = None  # Regulator Auth Code - the auth code returned by the regulator
    # TODO: format int for dates??
    md: Optional[int] = None  # Matched Date - the date the order was matched (null if the order is not matched)
    cd: Optional[int] = None  # Cancelled Date - the date the order was cancelled (null if the order is not cancelled)
    ld: Optional[int] = None  # Lapsed Date - the date the order was lapsed (null if the order is not lapsed)

    # Average Price Matched - the average price the order was matched at (null if the order is not matched).
    # This value is not meaningful for activity on Line markets and is not guaranteed to be returned or
    # maintained for these markets.
    avp: Optional[float] = None
    sm: Optional[float] = None  # Size Matched - the amount of the order that has been matched
    sr: Optional[float] = None  # Size Remaining - the amount of the order that is remaining unmatched
    sl: Optional[float] = None  # Size Lapsed - the amount of the order that has been lapsed
    sc: Optional[float] = None  # Size Cancelled - the amount of the order that has been cancelled
    sv: Optional[float] = None  # Size Voided - the amount of the order that has been voided
    lsrc: Optional[LapseStatusReasonCode] = None


class MatchedOrder(BaseMessage, array_like=True, frozen=True):
    price: Price
    size: Size


class StrategyMatchChange(BaseMessage, frozen=True):
    mb: Optional[list[MatchedOrder]] = None
    ml: Optional[list[MatchedOrder]] = None


class OrderRunnerChange(BaseMessage, frozen=True):
    id: SelectionId
    full_image: Optional[bool] = False
    hc: Optional[Handicap] = None
    mb: Optional[list[MatchedOrder]] = None
    ml: Optional[list[MatchedOrder]] = None
    smc: Optional[dict[str, StrategyMatchChange]] = None
    uo: Optional[list[Order]] = None


class OrderMarketChange(BaseMessage, kw_only=True, frozen=True):
    id: MarketId
    account_id: Optional[int] = None
    closed: Optional[bool] = None
    full_image: Optional[bool] = False
    orc: Optional[list[OrderRunnerChange]] = None
