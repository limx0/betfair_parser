from datetime import datetime
from functools import partial
from typing import Optional

import msgspec

from betfair_parser.endpoints import SILKS
from betfair_parser.spec.betting.enums import (
    BetTargetType,
    ExecutionReportErrorCode,
    ExecutionReportStatus,
    InstructionReportErrorCode,
    InstructionReportStatus,
    MarketBettingType,
    MarketStatus,
    PersistenceType,
    PriceData,
    PriceLadderType,
    RollupModel,
    RunnerStatus,
    Side,
    TimeInForce,
)
from betfair_parser.spec.common import (
    BaseMessage,
    BetId,
    CompetitionId,
    CountryCode,
    CustomerOrderRef,
    CustomerRef,
    CustomerStrategyRef,
    Date,
    EventId,
    EventTypeId,
    ExchangeId,
    Handicap,
    MarketId,
    MatchId,
    OrderStatus,
    OrderType,
    Price,
    SelectionId,
    Size,
    TimeRange,
    Venue,
    method_tag,
)


betting_tag = partial(method_tag, "SportsAPING/v1.0/")


class Competition(BaseMessage, frozen=True):
    id: Optional[CompetitionId] = None
    name: Optional[str] = None


class CompetitionResult(BaseMessage, frozen=True):
    competition: Optional[Competition] = None
    market_count: Optional[int] = None  # Count of markets associated with this competition
    competition_region: Optional[str] = None  # Region in which this competition is happening


class Event(BaseMessage, frozen=True):
    id: Optional[EventId] = None  # The unique id for the event
    name: Optional[str] = None  # The name of the event
    country_code: Optional[CountryCode] = None  # The ISO-2 code for the event, defaults to GB
    timezone: Optional[str] = None  # The timezone in which the event is taking place
    venue: Optional[str] = None
    open_date: Optional[Date] = None  # The scheduled start date and time of the event


class EventResult(BaseMessage, frozen=True):
    event: Optional[Event] = None
    market_count: Optional[int] = None  # Count of markets associated with this event


class EventType(BaseMessage, frozen=True):
    id: Optional[EventTypeId] = None
    name: Optional[str] = None


class EventTypeResult(BaseMessage, frozen=True):
    event_type: Optional[EventType] = None  # The ID identifying the Event Type
    market_count: Optional[int] = None  # Count of markets associated with this eventType


class MarketTypeResult(BaseMessage, frozen=True):
    market_type: Optional[str] = None
    market_count: Optional[int] = None  # Count of markets associated with this marketType


class CountryCodeResult(BaseMessage, frozen=True):
    country_code: Optional[CountryCode] = None  # The ISO-2 code for the event
    market_count: Optional[int] = None  # Count of markets associated with this Country Code


class VenueResult(BaseMessage, frozen=True):
    venue: Optional[Venue] = None
    market_count: Optional[int] = None  # Count of markets associated with this Venue


class PriceSize(BaseMessage, frozen=True):
    price: Price  # Available price
    size: Size  # Available stake


class TimeRangeResult(BaseMessage, frozen=True):
    time_range: Optional[TimeRange] = None
    market_count: Optional[int] = None  # Count of markets associated with this TimeRange


class MarketFilter(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    text_query: Optional[str] = None  # Restrict markets by any text associated with the Event name
    exchange_ids: Optional[set[ExchangeId]] = None  # DEPRECATED
    event_type_ids: Optional[set[EventTypeId]] = None  # Restrict markets by event type associated with the market
    event_ids: Optional[set[EventId]] = None  # Restrict markets by the event id associated with the market
    competition_ids: Optional[set[CompetitionId]] = None  # Restrict markets by the competitions
    market_ids: Optional[set[MarketId]] = None  # Restrict markets by the market id associated with the market
    venues: Optional[set[Venue]] = None  # Restrict markets by the venue associated with the market
    bsp_only: Optional[bool] = None  # Restrict to bsp markets only if True or non-bsp markets if False

    # Restrict to markets that will turn in play if True or will not turn in play if False
    turn_in_play_enabled: Optional[bool] = None

    # Restrict to markets that are currently in play if True or are not currently in play if False
    in_play_only: Optional[bool] = None
    market_betting_types: Optional[set[MarketBettingType]] = None  # Match the betting type of the market
    market_countries: Optional[set[CountryCode]] = None  # Match the specified country or countries
    market_type_codes: Optional[set[str]] = None  # Restrict to markets that match the type of the market
    market_start_time: Optional[TimeRange] = None  # Restrict to markets with a market start time range
    with_orders: Optional[set[str]] = None  # Markets that have one or more orders of defined OrderStatus
    race_types: Optional[set[str]] = None  # Restrict by race type


class MarketLineRangeInfo(BaseMessage, frozen=True):
    """Market Line and Range Info"""

    max_unit_value: float  # Maximum value for the outcome, in market units
    min_unit_value: float  # Minimum value for the outcome, in market units
    interval: float  # The odds ladder increment interval
    market_unit: str  # The type of unit the lines are incremented in


class PriceLadderDescription(BaseMessage, frozen=True):
    """Description of the price ladder type and any related data"""

    type: PriceLadderType


class StartingPrices(BaseMessage, frozen=True):
    """Information about the Betfair Starting Price. Only available in BSP markets"""

    near_price: Optional[float] = None  # What the starting price would be if the market was reconciled now
    far_price: Optional[float] = None  # What the starting price would be if the market was reconciled now

    # The total amount of back bets matched at the actual Betfair Starting Price
    back_stake_taken: Optional[list[PriceSize]] = None
    lay_liability_taken: Optional[list[PriceSize]] = None  # The lay amount matched at the actual Betfair Starting Price
    actual_sp: Optional[float] = msgspec.field(name="actualSP", default=None)  # The final BSP price for this runner


class ExchangePrices(BaseMessage, frozen=True):
    available_to_back: Optional[list[PriceSize]] = None
    available_to_lay: Optional[list[PriceSize]] = None
    traded_volume: Optional[list[PriceSize]] = None


class Order(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    bet_id: BetId
    order_type: OrderType
    status: OrderStatus
    persistence_type: PersistenceType
    side: Side  # Side (BACK or LAY)
    price: Price
    size: Size
    bsp_liability: Size  # Liability of a given BSP bet
    placed_date: Date  # Date and time the bet was placed
    avg_price_matched: Optional[Price] = None  # Average price matched at
    size_matched: Optional[Size] = None  # Current amount of this bet that was matched
    size_remaining: Optional[Size] = None  # Current amount of this bet that is unmatched
    size_lapsed: Optional[Size] = None  # Current amount of this bet that was lapsed
    size_cancelled: Optional[Size] = None  # Current amount of this bet that was cancelled
    size_voided: Optional[Size] = None  # Current amount of this bet that was voided
    customer_order_ref: Optional[CustomerOrderRef] = None  # Customer Order Reference
    customer_strategy_ref: Optional[CustomerStrategyRef] = None  # Customer Strategy Reference


class Match(BaseMessage, kw_only=True, frozen=True):
    """An individual bet Match, or rollup by price or avg price.

    Rollup depends on the requested MatchProjection.
    """

    bet_id: Optional[BetId] = None  # Bet ID (present if no rollup)
    match_id: Optional[MatchId] = None  # Match ID (present if no rollup)
    side: Side  # Side (BACK or LAY)
    price: Price  # Match price
    size: Size  # Size matched at
    match_date: Optional[Date] = None  # Match date (present if no rollup)


class MarketVersion(BaseMessage, frozen=True):
    version: Optional[int] = None  # A non-monotonically increasing number indicating market changes


class MarketRates(BaseMessage, frozen=True):
    market_base_rate: float  # Market base rate
    discount_allowed: bool  # Indicates whether discount is allowed on this market


class MarketLicence(BaseMessage, frozen=True):
    wallet: str  # Wallet from which funds will be taken when betting on this market
    rules: Optional[str] = None
    rules_has_date: Optional[bool] = None  # Markets start date and time are relevant to the rules
    clarifications: Optional[str] = None  # Clarifications to the rules for the market


class MarketDescription(BaseMessage, kw_only=True, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    persistence_enabled: bool  # Indicates if the market supports 'Keep' bets if turned in-play
    bsp_market: bool  # Indicates if the market supports Betfair SP betting
    market_time: Date  # Scheduled start time of the market
    suspend_time: Date  # Next time the market will be suspended for betting, usually just marketTime
    settle_time: Optional[Date] = None
    betting_type: MarketBettingType
    turn_in_play_enabled: bool  # Indicates if the market is set to turn in-play
    market_type: str  # Market base type
    regulator: str  # Market regulator
    market_base_rate: float  # Commission rate applicable to the market
    discount_allowed: bool  # Indicates whether user's discount rate is taken into account on this
    wallet: Optional[str] = None  # The wallet to which the market belongs
    rules: Optional[str] = None  # The wallet to which the market belongs
    rules_has_date: Optional[bool] = None  # Indicates whether rules have a date included
    each_way_divisor: Optional[float] = None  # Divisor for EACH_WAY market type
    clarifications: Optional[str] = None  # Additional information regarding the market
    line_range_info: Optional[MarketLineRangeInfo] = None  # Line range info for line markets
    race_type: Optional[str] = None  # External identifier of a race type
    price_ladder_description: Optional[PriceLadderDescription] = None  # Details about the price ladder in use


# TODO: Some fields in the meta data should be country codes. Unfortunately, sometimes they contain
#       erroneous data that fails verification. This should be switched to CountryCode as soon as there is
#       some more fine-grained error handling possible in msgspec. Related issue:
#       https://github.com/jcrist/msgspec/issues/420
_MetaCountryCode = str  # CountryCode


class RunnerMetaData(BaseMessage, frozen=True, omit_defaults=True, repr_omit_defaults=True, rename="upper"):
    # Yes, this is the only type definition, that has (mostly) uppered key names
    """
    Runner metadata as defined in the API as additional information.
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Additional+Information
    """

    weight_units: Optional[str] = None  # The unit of weight used.
    adjusted_rating: Optional[int] = None  # Race-specific ratings that reflect weights allocated in the race
    dam_year_born: Optional[int] = None  # The year the horse’s mother's birth
    days_since_last_run: Optional[int] = None  # The number of days since the horse last ran
    wearing: Optional[str] = None  # Any extra equipment the horse is wearing
    damsire_year_born: Optional[int] = None  # Year in which the horse's grandfather was born on its mother's side
    sire_bred: Optional[_MetaCountryCode] = None  # The country where the horse's father was bred
    trainer_name: Optional[str] = None  # The name of the horse's trainer
    stall_draw: Optional[int] = None  # The stall number the horse is starting from
    sex_type: Optional[str] = None  # The sex of the horse
    owner_name: Optional[str] = None  # The owner of the horse
    sire_name: Optional[str] = None  # The name of the horse's father
    forecastprice_numerator: Optional[int] = None  # The forecast price numerator
    forecastprice_denominator: Optional[int] = None  # The forecast price denominator
    jockey_claim: Optional[int] = None  # Reduction in the weight that the horse carries for a particular jockey
    weight_value: Optional[float] = None  # The weight of the horse
    dam_name: Optional[str] = None  # The name of the horse's mother
    age: Optional[int] = None  # The age of the horse
    colour_type: Optional[str] = None  # The colour of the horse
    damsire_bred: Optional[_MetaCountryCode] = None  # The country where the horse's grandfather was born
    damsire_name: Optional[str] = None  # The name of the horse's grandfather
    sire_year_born: Optional[int] = None  # The year the horse's father was born
    official_rating: Optional[int] = None  # The horses official rating
    form: Optional[str] = None  # The horses recent form
    bred: Optional[_MetaCountryCode] = None  # The country in which the horse was born
    runner_id: Optional[int] = msgspec.field(name="runnerId", default=None)  # The runnerId for the horse
    jockey_name: Optional[str] = None  # Name of the jockey. This field will contain 'Reserve' if its a reserve runner
    dam_bred: Optional[_MetaCountryCode] = None  # The country where the horse's mother was born
    colours_description: Optional[str] = None  # The textual description of the jockey silk
    colours_filename: Optional[str] = None  # Image representing the jockey silk
    cloth_number: Optional[int] = None  # The number on the saddle-cloth
    cloth_number_alpha: Optional[str] = None  # The number on the saddle cloth for US paired runners, e.g. "1A"

    def __post_init__(self):
        force_setattr = msgspec.structs.force_setattr
        cur_year = datetime.now().year
        if self.weight_value is not None and self.weight_value <= 0:
            force_setattr(self, "weight_value", None)
        if self.stall_draw is not None and not 0 < self.stall_draw < 50:
            force_setattr(self, "stall_draw", None)
        if self.sire_year_born is not None and not 1980 < self.sire_year_born < cur_year:
            force_setattr(self, "sire_year_born", None)
        if self.dam_year_born is not None and not 1980 < self.dam_year_born < cur_year:
            force_setattr(self, "dam_year_born", None)
        if self.damsire_year_born is not None and not 1960 < self.damsire_year_born < cur_year:
            force_setattr(self, "damsire_year_born", None)
        if self.cloth_number is not None and not 0 < self.cloth_number < 50:
            force_setattr(self, "cloth_number", None)
        if self.age is not None and not 1 < self.age < 30:
            force_setattr(self, "age", None)

    @property
    def colours_url(self):
        if self.colours_filename:
            return SILKS + self.colours_filename

    @property
    def forecastprice_decimal(self):
        if not self.forecastprice_numerator or not self.forecastprice_denominator:
            return
        return self.forecastprice_numerator / self.forecastprice_denominator + 1


class RunnerCatalog(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Information about the Runners (selections) in a market"""

    selection_id: int  # The unique id for the selection
    runner_name: str  # The name of the runner

    # The handicap applies to market with the MarketBettingType ASIAN_HANDICAP_SINGLE_LINE
    # & ASIAN_HANDICAP_DOUBLE_LINE only
    handicap: Handicap
    sort_priority: Optional[int] = None  # This is marked as REQUIRED in the API doc, but omitted sometimes
    metadata: Optional[RunnerMetaData] = None  # Metadata associated with the runner

    @property
    def name(self):
        return self.runner_name


class Runner(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """The dynamic data about runners in a market"""

    selection_id: int  # The unique id of the runner (selection)
    handicap: Handicap
    status: RunnerStatus  # The status of the selection
    adjustment_factor: Optional[float] = None  # The adjustment factor applied if the selection is removed
    last_price_traded: Optional[float] = None  # The price of the most recent bet matched on this selection
    total_matched: Optional[float] = None  # The total amount matched on this runner
    removal_date: Optional[Date] = None  # If date and time the runner was removed
    sp: Optional[StartingPrices] = None  # The BSP related prices for this runner
    ex: Optional[ExchangePrices] = None  # The Exchange prices available for this runner
    orders: Optional[list[Order]] = None  # List of orders in the market
    matches: Optional[list[Match]] = None  # List of matches (i.e., orders that have been fully or partially executed)
    matches_by_strategy: Optional[dict[str, list[Match]]] = None  # All matches for each strategy, sort by matched data


class MarketCatalogue(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    market_id: MarketId  # The unique identifier for the market
    market_name: str  # The name of the market
    market_start_time: Optional[Date] = None  # Only returned when the MARKET_START_TIME enum is requested
    description: Optional[MarketDescription] = None  # Details about the market
    total_matched: Optional[float] = None  # The total amount of money matched on the market
    runners: Optional[list[RunnerCatalog]] = None  # The runners (selections) contained in the market
    event_type: Optional[EventType] = None  # The Event Type the market is contained within
    competition: Optional[Competition] = None  # The competition the market is contained within
    event: Optional[Event] = None  # The event the market is contained within


class KeyLineSelection(BaseMessage, frozen=True):
    """Description of a market's key line selection"""

    selection_id: SelectionId  # Selection ID of the runner in the key line handicap
    handicap: Handicap  # Handicap value of the key line


class KeyLineDescription(BaseMessage, frozen=True):
    """A list of KeyLineSelection objects describing the key line for the market"""

    key_line: list[KeyLineSelection]  # A list of KeyLineSelection objects


class MarketBook(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """The dynamic data in a market"""

    market_id: MarketId  # The unique identifier for the market
    is_market_data_delayed: bool  # True if the data returned by listMarketBook will be delayed
    status: Optional[MarketStatus] = None  # The status of the market
    bet_delay: Optional[int] = None  # The number of seconds an order is held until it is submitted into the market
    bsp_reconciled: Optional[bool] = None  # True if the market starting price has been reconciled
    complete: Optional[bool] = None  # If false, runners may be added to the market
    inplay: Optional[bool] = None  # True if the market is currently in play
    number_of_winners: Optional[int] = None  # The number of selections that could be settled as winners
    number_of_runners: Optional[int] = None  # The number of runners in the market
    number_of_active_runners: Optional[int] = None  # The number of runners that are currently active
    last_match_time: Optional[Date] = None  # The most recent time an order was executed
    total_matched: Optional[float] = None  # The total amount matched on the market
    total_available: Optional[float] = None  # The total amount of orders that remain unmatched
    cross_matching: Optional[bool] = None  # True if cross matching is enabled for this market
    runners_voidable: Optional[bool] = None  # True if runners in the market can be voided
    version: Optional[int] = None  # The version of the market
    runners: Optional[list[Runner]] = None  # Information about the runners (selections) in the market
    key_line_description: Optional[KeyLineDescription] = None  # Description of a market's key line


class ItemDescription(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """
    This object contains some text which may be useful to render a betting history view.
    It offers no long-term warranty as to the correctness of the text.
    """

    event_type_desc: Optional[str] = None  # The event type name translated into the requested locale
    event_desc: Optional[str] = None  # The event name or openDate + venue translated into the requested locale
    market_desc: Optional[str] = None  # The market name or racing market type translated into the requested locale
    market_type: Optional[str] = None  # The market type e.g. MATCH_ODDS, PLACE, WIN etc.
    market_start_time: Optional[Date] = None  # The start time of the market in ISO-8601 format, not translated
    runner_desc: Optional[str] = None  # The runner name translated into the requested locale
    number_of_winners: Optional[int] = None  # The number of winners on a market
    each_way_divisor: Optional[float] = None  # The divisor for the EACH_WAY market type


class ClearedOrderSummary(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Summary of a cleared order"""

    event_type_id: Optional[EventTypeId] = None  # The id of the event type bet on
    event_id: Optional[EventId] = None  # The id of the event bet on
    market_id: Optional[MarketId] = None  # The id of the market bet on
    selection_id: Optional[int] = None  # The id of the selection bet on
    handicap: Optional[Handicap] = None  # The handicap value for Asian handicap markets
    bet_id: Optional[BetId] = None  # The id of the bet
    placed_date: Optional[Date] = None  # The date the bet order was placed by the customer
    persistence_type: Optional[PersistenceType] = None  # The turn in play persistence state of the order
    order_type: Optional[OrderType] = None
    side: Optional[Side] = None  # Whether the bet was a back or lay bet
    item_description: Optional[ItemDescription] = None  # Container for ancillary data and localized text
    bet_outcome: Optional[str] = None  # The settlement outcome of the bet
    price_requested: Optional[Price] = None  # The average requested price across all settled bet orders under this item
    settled_date: Optional[Date] = None  # The date and time the bet order was settled by Betfair
    last_matched_date: Optional[Date] = None  # The date and time the last bet order was matched by Betfair
    bet_count: Optional[int] = None  # The number of actual bets within this grouping

    # The cumulative amount of commission paid by the customer across all bets under this item
    commission: Optional[Size] = None
    price_matched: Optional[Price] = None  # The average matched price across all settled bets or bet fragments
    price_reduced: Optional[bool] = None  # Indicates if the matched price was affected by a reduction factor
    size_settled: Optional[Size] = None  # The cumulative bet size that was settled as matched or voided under this item
    profit: Optional[float] = None  # The profit or loss gained on this line
    size_cancelled: Optional[Size] = None  # The amount of the bet that was cancelled
    customer_order_ref: Optional[CustomerOrderRef] = None  # Defined by the customer for the bet order
    customer_strategy_ref: Optional[CustomerStrategyRef] = None  # Defined by the customer for the bet order


class ClearedOrderSummaryReport(BaseMessage, frozen=True):
    """A container representing search results"""

    cleared_orders: list[ClearedOrderSummary]  # The list of cleared orders returned by the query
    more_available: bool  # Indicates whether there are further result items beyond this page


class RunnerId(BaseMessage, frozen=True):
    """Unique identifier for a runner"""

    market_id: MarketId  # The id of the market bet on
    selection_id: int  # The id of the selection bet on
    handicap: Optional[Handicap] = None  # The handicap associated with the runner in case of Asian handicap markets


class CurrentItemDescription(BaseMessage, frozen=True):
    """This object contains ancillary information about the item"""

    market_version: MarketVersion  # The relevant version of the market for this item


class CurrentOrderSummary(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Summary of a current order"""

    bet_id: BetId  # The bet ID of the original place order
    market_id: MarketId  # The market ID the order is for
    selection_id: int  # The selection ID the order is for
    handicap: Handicap  # The handicap associated with the runner in case of Asian handicap markets
    price_size: PriceSize  # The price and size of the bet
    bsp_liability: Size  # The liability of a given BSP bet
    side: Side  # BACK/LAY
    status: OrderStatus  # The status of the order
    persistence_type: PersistenceType  # What to do with the order at turn-in-play
    order_type: OrderType  # BSP Order type
    placed_date: Date  # The date the bet was placed

    # The date of the last matched bet fragment.
    # Mandatory according to documentation, but optional in reality
    matched_date: Optional[Date] = None
    average_price_matched: Optional[Price] = None  # The average price matched at
    size_matched: Optional[Size] = None
    size_remaining: Optional[Size] = None
    size_lapsed: Optional[Size] = None
    size_cancelled: Optional[Size] = None
    size_voided: Optional[Size] = None
    regulator_auth_code: Optional[str] = None
    regulator_code: Optional[str] = None
    customer_order_ref: Optional[str] = None  # The order reference defined by the customer for this bet
    customer_strategy_ref: Optional[str] = None  # The strategy reference defined by the customer for this bet
    current_item_description: Optional[CurrentItemDescription] = None  # Container for ancillary data for this item


class CurrentOrderSummaryReport(BaseMessage, frozen=True):
    """A container representing search results"""

    current_orders: list[CurrentOrderSummary]  # The list of current orders returned by the query
    more_available: bool  # Indicates whether there are further result items beyond this page


class LimitOrder(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Place a new LIMIT order (simple exchange bet for immediate execution)"""

    size: Size
    price: Price
    persistence_type: Optional[PersistenceType] = None
    time_in_force: Optional[TimeInForce] = None
    min_fill_size: Optional[Size] = None
    bet_target_type: Optional[BetTargetType] = None
    bet_target_size: Optional[Size] = None


class LimitOnCloseOrder(BaseMessage, frozen=True):
    liability: Size
    price: Price


class MarketOnCloseOrder(BaseMessage, frozen=True):
    liability: Size


class PlaceInstruction(BaseMessage, kw_only=True, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Instruction to place a new order"""

    order_type: OrderType  # The order type
    selection_id: SelectionId  # The selection ID
    handicap: Optional[Handicap] = None  # The handicap associated with the runner in case of Asian handicap markets
    side: Side  # Back or Lay
    limit_order: Optional[LimitOrder] = None  # A simple exchange bet for immediate execution

    # Bets matched if the returned starting price is better than a specified price
    limit_on_close_order: Optional[LimitOnCloseOrder] = None

    # Bets matched and settled at a price representative of the market at the point it turns in-play
    market_on_close_order: Optional[MarketOnCloseOrder] = None
    customer_order_ref: Optional[str] = None  # An optional reference to identify instructions


class PlaceInstructionReport(BaseMessage, kw_only=True, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Report for a place instruction"""

    status: InstructionReportStatus  # The instruction report status
    error_code: Optional[InstructionReportErrorCode] = None
    order_status: Optional[OrderStatus] = None
    instruction: PlaceInstruction  # The place instruction
    bet_id: Optional[BetId] = None  # The bet ID of the placed order, if successful
    placed_date: Optional[Date] = None  # The date and time the bet was placed, if successful
    average_price_matched: Optional[Price] = None  # The average price matched at, if successful
    size_matched: Optional[Size] = None  # The current amount of the bet that was matched, if successful


class PlaceExecutionReport(BaseMessage, kw_only=True, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    customer_ref: Optional[CustomerRef] = None  # Echo of the customer reference if passed
    status: ExecutionReportStatus  # The execution report status
    error_code: Optional[ExecutionReportErrorCode] = None  # The execution report error code
    market_id: Optional[MarketId] = None  # Echo of the market ID passed
    instruction_reports: Optional[list[PlaceInstructionReport]] = None  # The list of place instruction reports


class CancelInstruction(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Instruction to fully or partially cancel an order (only applies to LIMIT orders)"""

    bet_id: BetId
    # If supplied then this is a partial cancel. Should be set to 'null' if no size
    # reduction is required.
    size_reduction: Optional[Size] = None


class ReplaceInstruction(BaseMessage, frozen=True):
    """Instruction to replace a LIMIT or LIMIT_ON_CLOSE order at a new price."""

    bet_id: BetId  # Unique identifier for the bet
    new_price: Price  # The price to replace the bet at


class CancelInstructionReport(BaseMessage, kw_only=True, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    status: InstructionReportStatus  # Whether the command succeeded or failed
    error_code: Optional[InstructionReportErrorCode] = None  # Cause of failure, or null if command succeeds
    instruction: Optional[CancelInstruction] = None  # The instruction that was requested
    size_cancelled: Optional[float] = None  # The API states, that this is mandatory, but it's skipped in case of error
    cancelled_date: Optional[Date] = None  # The API states, that this is mandatory, but it's skipped in case of error


class CancelExecutionReport(BaseMessage, kw_only=True, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    customer_ref: Optional[CustomerRef] = None  # Echo of the customerRef if passed
    status: ExecutionReportStatus
    error_code: Optional[ExecutionReportErrorCode] = None
    market_id: Optional[MarketId] = None  # Echo of marketId passed
    instruction_reports: Optional[list[CancelInstructionReport]] = None


class ReplaceInstructionReport(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    status: InstructionReportStatus  # Whether the command succeeded or failed
    error_code: Optional[InstructionReportErrorCode] = None  # Cause of failure, or null if command succeeds
    cancel_instruction_report: Optional[CancelInstructionReport] = None  # Cancellation report for the original order
    place_instruction_report: Optional[PlaceInstructionReport] = None  # Placement report for the new order


class ReplaceExecutionReport(BaseMessage, kw_only=True, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    customer_ref: Optional[CustomerRef] = None  # Echo of the customerRef if passed.
    status: ExecutionReportStatus
    error_code: Optional[ExecutionReportErrorCode] = None
    market_id: Optional[MarketId] = None  # Echo of marketId passed
    instruction_reports: Optional[list[ReplaceInstructionReport]] = None


class UpdateInstruction(BaseMessage, frozen=True):
    """Instruction to update LIMIT bet's persistence of an order that do not affect exposure"""

    bet_id: BetId  # Unique identifier for the bet
    new_persistence_type: PersistenceType  # The new persistence type to update this bet to


class UpdateInstructionReport(BaseMessage, kw_only=True, frozen=True):
    status: InstructionReportStatus  # Whether the command succeeded or failed
    error_code: Optional[InstructionReportErrorCode] = None  # Cause of failure, or null if command succeeds
    instruction: UpdateInstruction  # The instruction that was requested


class UpdateExecutionReport(BaseMessage, frozen=True):
    customer_ref: Optional[CustomerRef]  # Echo of the customerRef if passed.
    status: ExecutionReportStatus
    error_code: Optional[ExecutionReportErrorCode]
    market_id: Optional[MarketId]  # Echo of marketId passed
    instruction_reports: Optional[list[UpdateInstructionReport]]


class ExBestOffersOverrides(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Options to alter the default representation of best offer prices"""

    best_prices_depth: Optional[int] = None  # The maximum number of prices to return on each side for each runner
    rollup_model: Optional[RollupModel] = None  # The model to use when rolling up available sizes
    rollup_limit: Optional[int] = None  # The volume limit to use when rolling up returned sizes
    rollup_liability_threshold: Optional[float] = None  # Only applicable when rollupModel is MANAGED_LIABILITY
    rollup_liability_factor: Optional[int] = None  # Only applicable when rollupModel is MANAGED_LIABILITY


class PriceProjection(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Selection criteria of the returning price data"""

    price_data: Optional[set[PriceData]] = None  # The basic price data you want to receive in the response

    # Options to alter the default representation of best offer prices
    ex_best_offers_overrides: Optional[ExBestOffersOverrides] = None
    virtualise: Optional[bool] = None  # Indicates if the returned prices should include virtual prices

    # Indicates if the volume returned at each price point should be the absolute value or a
    # cumulative sum of volumes available at the price and all better prices. If unspecified
    # defaults to false. Applicable to EX_BEST_OFFERS and EX_ALL_OFFERS price projections.
    # Not supported as yet.
    rollover_stakes: Optional[bool] = None


class RunnerProfitAndLoss(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Profit and loss if selection wins or loses"""

    selection_id: Optional[SelectionId] = None  # The unique identifier for the selection
    if_win: Optional[float] = None  # Profit or loss for the market if this selection is the winner
    if_lose: Optional[float] = None  # Profit or loss for the market if this selection is the loser

    # Profit or loss for the market if this selection is placed (applies to marketType EACH_WAY only)
    if_place: Optional[float] = None


class MarketProfitAndLoss(BaseMessage, omit_defaults=True, repr_omit_defaults=True, frozen=True):
    """Profit and loss in a market"""

    market_id: Optional[MarketId] = None  # The unique identifier for the market
    commission_applied: Optional[float] = None  # The commission rate applied to P&L values
    profit_and_losses: Optional[list[RunnerProfitAndLoss]] = None  # Calculated profit and loss data
