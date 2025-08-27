from datetime import datetime
from functools import partial

import msgspec

from betfair_parser.endpoints import SILKS
from betfair_parser.spec.betting.enums import (
    BetDelayModel,
    BetTargetType,
    ExecutionReportErrorCode,
    ExecutionReportStatus,
    InstructionReportErrorCode,
    InstructionReportStatus,
    MarketBettingType,
    MarketStatus,
    MarketTypeCode,
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
    MarketType,
    MatchId,
    OrderStatus,
    OrderType,
    Price,
    SelectionId,
    Set,
    Size,
    TimeRange,
    Venue,
    method_tag,
)


betting_tag = partial(method_tag, "SportsAPING/v1.0/")


class Competition(BaseMessage, frozen=True):
    id: CompetitionId | None = None
    name: str | None = None


class CompetitionResult(BaseMessage, frozen=True):
    competition: Competition | None = None
    market_count: int | None = None  # Count of markets associated with this competition
    competition_region: str | None = None  # Region in which this competition is happening


class Event(BaseMessage, frozen=True):
    id: EventId | None = None  # The unique id for the event
    name: str | None = None  # The name of the event
    country_code: CountryCode | None = None  # The ISO-2 code for the event, defaults to GB
    timezone: str | None = None  # The timezone in which the event is taking place
    venue: str | None = None
    open_date: Date | None = None  # The scheduled start date and time of the event


class EventResult(BaseMessage, frozen=True):
    event: Event | None = None
    market_count: int | None = None  # Count of markets associated with this event


class EventType(BaseMessage, frozen=True):
    id: EventTypeId | None = None
    name: str | None = None


class EventTypeResult(BaseMessage, frozen=True):
    event_type: EventType | None = None  # The ID identifying the Event Type
    market_count: int | None = None  # Count of markets associated with this eventType


class MarketTypeResult(BaseMessage, frozen=True):
    market_type: str | None = None
    market_count: int | None = None  # Count of markets associated with this marketType


class CountryCodeResult(BaseMessage, frozen=True):
    country_code: CountryCode | None = None  # The ISO-2 code for the event
    market_count: int | None = None  # Count of markets associated with this Country Code


class VenueResult(BaseMessage, frozen=True):
    venue: Venue | None = None
    market_count: int | None = None  # Count of markets associated with this Venue


class PriceSize(BaseMessage, frozen=True):
    price: Price  # Available price
    size: Size  # Available stake


class TimeRangeResult(BaseMessage, frozen=True):
    time_range: TimeRange | None = None
    market_count: int | None = None  # Count of markets associated with this TimeRange


class MarketFilter(BaseMessage, frozen=True):
    bsp_only: bool | None = None  # Restrict to bsp markets only if True or non-bsp markets if False
    competition_ids: Set[CompetitionId] | None = None  # Restrict markets by the competitions
    event_ids: Set[EventId] | None = None  # Restrict markets by the event id associated with the market
    event_type_ids: Set[EventTypeId] | None = None  # Restrict markets by event type associated with the market
    exchange_ids: Set[ExchangeId] | None = None  # DEPRECATED

    # Restrict to markets that are currently in play if True or are not currently in play if False
    in_play_only: bool | None = None
    market_betting_types: Set[MarketBettingType] | None = None  # Match the betting type of the market
    market_countries: Set[CountryCode] | None = None  # Match the specified country or countries
    market_ids: Set[MarketId] | None = None  # Restrict markets by the market id associated with the market
    market_start_time: TimeRange | None = None  # Restrict to markets with a market start time range
    market_type_codes: Set[MarketTypeCode] | None = None  # Restrict to markets that match the type of the market
    race_types: Set[str] | None = None  # Restrict by race type
    text_query: str | None = None  # Restrict markets by any text associated with the Event name

    # Restrict to markets that will turn in play if True or will not turn in play if False
    turn_in_play_enabled: bool | None = None
    venues: Set[Venue] | None = None  # Restrict markets by the venue associated with the market
    with_orders: Set[str] | None = None  # Markets that have one or more orders of defined OrderStatus


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

    near_price: float | None = None  # What the starting price would be if the market was reconciled now
    far_price: float | None = None  # What the starting price would be if the market was reconciled now

    # The total amount of back bets matched at the actual Betfair Starting Price
    back_stake_taken: list[PriceSize] | None = None
    lay_liability_taken: list[PriceSize] | None = None  # The lay amount matched at the actual Betfair Starting Price
    actual_sp: float | None = msgspec.field(name="actualSP", default=None)  # The final BSP price for this runner


class ExchangePrices(BaseMessage, frozen=True):
    available_to_back: list[PriceSize] | None = None
    available_to_lay: list[PriceSize] | None = None
    traded_volume: list[PriceSize] | None = None


class Order(BaseMessage, frozen=True):
    bet_id: BetId
    order_type: OrderType
    status: OrderStatus
    persistence_type: PersistenceType
    side: Side  # Side (BACK or LAY)
    price: Price
    size: Size
    bsp_liability: Size  # Liability of a given BSP bet
    placed_date: Date  # Date and time the bet was placed
    avg_price_matched: Price | None = None  # Average price matched at
    size_matched: Size | None = None  # Current amount of this bet that was matched
    size_remaining: Size | None = None  # Current amount of this bet that is unmatched
    size_lapsed: Size | None = None  # Current amount of this bet that was lapsed
    size_cancelled: Size | None = None  # Current amount of this bet that was cancelled
    size_voided: Size | None = None  # Current amount of this bet that was voided
    customer_order_ref: CustomerOrderRef | None = None  # Customer Order Reference
    customer_strategy_ref: CustomerStrategyRef | None = None  # Customer Strategy Reference


class Match(BaseMessage, kw_only=True, frozen=True):
    """An individual bet Match, or rollup by price or avg price.

    Rollup depends on the requested MatchProjection.
    """

    bet_id: BetId | None = None  # Bet ID (present if no rollup)
    match_id: MatchId | None = None  # Match ID (present if no rollup)
    side: Side  # Side (BACK or LAY)
    price: Price  # Match price
    size: Size  # Size matched at
    match_date: Date | None = None  # Match date (present if no rollup)


class MarketVersion(BaseMessage, frozen=True):
    version: int | None = None  # A non-monotonically increasing number indicating market changes


class MarketRates(BaseMessage, frozen=True):
    market_base_rate: float  # Market base rate
    discount_allowed: bool  # Indicates whether discount is allowed on this market


class MarketLicence(BaseMessage, frozen=True):
    wallet: str  # Wallet from which funds will be taken when betting on this market
    rules: str | None = None
    rules_has_date: bool | None = None  # Markets start date and time are relevant to the rules
    clarifications: str | None = None  # Clarifications to the rules for the market


class MarketDescription(BaseMessage, kw_only=True, frozen=True):
    betting_type: MarketBettingType
    bsp_market: bool  # Indicates if the market supports Betfair SP betting
    clarifications: str | None = None  # Additional information regarding the market
    discount_allowed: bool  # Indicates whether user's discount rate is taken into account on this
    each_way_divisor: float | None = None  # Divisor for EACH_WAY market type
    line_range_info: MarketLineRangeInfo | None = None  # Line range info for line markets
    market_base_rate: float  # Commission rate applicable to the market
    market_time: Date  # Scheduled start time of the market
    market_type: str  # Market base type
    persistence_enabled: bool  # Indicates if the market supports 'Keep' bets if turned in-play
    price_ladder_description: PriceLadderDescription | None = None  # Details about the price ladder in use
    race_type: str | None = None  # External identifier of a race type
    regulator: str  # Market regulator
    rules: str | None = None  # The market rules
    rules_has_date: bool | None = None  # Indicates whether rules have a date included
    settle_time: Date | None = None
    suspend_time: Date  # Next time the market will be suspended for betting, usually just marketTime
    turn_in_play_enabled: bool  # Indicates if the market is set to turn in-play
    wallet: str | None = None  # The wallet to which the market belongs


# TODO: Some fields in the meta data should be country codes. Unfortunately, sometimes they contain
#       erroneous data that fails verification. This should be switched to CountryCode as soon as there is
#       some more fine-grained error handling possible in msgspec. Related issue:
#       https://github.com/jcrist/msgspec/issues/420
_MetaCountryCode = str  # CountryCode


class RunnerMetaData(BaseMessage, frozen=True, rename="upper"):
    # Yes, this is the only type definition, that has (mostly) upper-case key names
    """
    Runner metadata as defined in the API as additional information.
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Additional+Information
    """

    adjusted_rating: int | None = None  # Race-specific ratings that reflect weights allocated in the race
    age: int | None = None  # The age of the horse
    bred: _MetaCountryCode | None = None  # The country in which the horse was born
    cloth_number: int | None = None  # The number on the saddle-cloth
    cloth_number_alpha: str | None = None  # The number on the saddle cloth for US paired runners, e.g. "1A"
    colour_type: str | None = None  # The colour of the horse
    colours_description: str | None = None  # The textual description of the jockey silk
    colours_filename: str | None = None  # Image representing the jockey silk
    dam_bred: _MetaCountryCode | None = None  # The country where the horse's mother was born
    dam_name: str | None = None  # The name of the horse's mother
    dam_year_born: int | None = None  # The year the horse’s mother's birth
    damsire_bred: _MetaCountryCode | None = None  # The country where the horse's grandfather was born
    damsire_name: str | None = None  # The name of the horse's grandfather
    damsire_year_born: int | None = None  # Year in which the horse's grandfather was born on its mother's side
    days_since_last_run: int | None = None  # The number of days since the horse last ran
    forecastprice_denominator: int | None = None  # The forecast price denominator
    forecastprice_numerator: int | None = None  # The forecast price numerator
    form: str | None = None  # The horses recent form
    jockey_claim: int | None = None  # Reduction in the weight that the horse carries for a particular jockey
    jockey_name: str | None = None  # Name of the jockey. This field will contain 'Reserve' if it's a reserve runner
    official_rating: int | None = None  # The horses official rating
    owner_name: str | None = None  # The owner of the horse
    runner_id: int | None = msgspec.field(name="runnerId", default=None)  # The runnerId for the horse
    sex_type: str | None = None  # The sex of the horse
    sire_bred: _MetaCountryCode | None = None  # The country where the horse's father was bred
    sire_name: str | None = None  # The name of the horse's father
    sire_year_born: int | None = None  # The year the horse's father was born
    stall_draw: int | None = None  # The stall number the horse is starting from
    trainer_name: str | None = None  # The name of the horse's trainer
    wearing: str | None = None  # Any extra equipment the horse is wearing
    weight_units: str | None = None  # The unit of weight used.
    weight_value: float | None = None  # The weight of the horse

    def __post_init__(self):
        force_setattr = msgspec.structs.force_setattr
        cur_year = datetime.now().year
        if self.weight_value is not None and self.weight_value <= 0:
            force_setattr(self, "weight_value", None)
        if self.stall_draw is not None and not 0 < self.stall_draw < 50:
            force_setattr(self, "stall_draw", None)
        if self.sire_year_born is not None and not cur_year - 40 < self.sire_year_born < cur_year:
            force_setattr(self, "sire_year_born", None)
        if self.dam_year_born is not None and not cur_year - 40 < self.dam_year_born < cur_year:
            force_setattr(self, "dam_year_born", None)
        if self.damsire_year_born is not None and not cur_year - 60 < self.damsire_year_born < cur_year:
            force_setattr(self, "damsire_year_born", None)
        if self.cloth_number is not None and not 0 < self.cloth_number < 50:
            force_setattr(self, "cloth_number", None)
        if self.age is not None and not 1 < self.age < 30:
            force_setattr(self, "age", None)

    @property
    def colours_url(self):
        if not self.colours_filename:
            return None
        return SILKS + self.colours_filename

    @property
    def forecastprice_decimal(self):
        if not self.forecastprice_numerator or not self.forecastprice_denominator:
            return None
        return self.forecastprice_numerator / self.forecastprice_denominator + 1


class RunnerCatalog(BaseMessage, frozen=True):
    """Information about the Runners (selections) in a market"""

    selection_id: SelectionId  # The unique id for the selection
    runner_name: str  # The name of the runner

    # The handicap applies to market with the MarketBettingType ASIAN_HANDICAP_SINGLE_LINE
    # & ASIAN_HANDICAP_DOUBLE_LINE only
    handicap: Handicap
    sort_priority: int | None = None  # This is marked as REQUIRED in the API doc, but omitted sometimes
    metadata: RunnerMetaData | None = None  # Metadata associated with the runner

    @property
    def name(self):
        return self.runner_name


class Runner(BaseMessage, frozen=True):
    """The dynamic data about runners in a market"""

    selection_id: SelectionId  # The unique id of the runner (selection)
    handicap: Handicap
    status: RunnerStatus  # The status of the selection
    adjustment_factor: float | None = None  # The adjustment factor applied if the selection is removed
    last_price_traded: float | None = None  # The price of the most recent bet matched on this selection
    total_matched: float | None = None  # The total amount matched on this runner
    removal_date: Date | None = None  # If date and time the runner was removed
    sp: StartingPrices | None = None  # The BSP related prices for this runner
    ex: ExchangePrices | None = None  # The Exchange prices available for this runner
    orders: list[Order] | None = None  # List of orders in the market
    matches: list[Match] | None = None  # List of matches (i.e., orders that have been fully or partially executed)
    matches_by_strategy: dict[str, list[Match]] | None = None  # All matches for each strategy, sort by matched data


class MarketCatalogue(BaseMessage, frozen=True):
    market_id: MarketId  # The unique identifier for the market
    market_name: str  # The name of the market
    market_start_time: Date | None = None  # Only returned when the MARKET_START_TIME enum is requested
    total_matched: float | None = None  # The total amount of money matched on the market
    event_type: EventType | None = None  # The Event Type the market is contained within
    competition: Competition | None = None  # The competition the market is contained within
    description: MarketDescription | None = None  # Details about the market
    event: Event | None = None  # The event the market is contained within
    runners: list[RunnerCatalog] | None = None  # The runners (selections) contained in the market


class KeyLineSelection(BaseMessage, frozen=True):
    """Description of a market's key line selection"""

    selection_id: SelectionId  # Selection ID of the runner in the key line handicap
    handicap: Handicap  # Handicap value of the key line


class KeyLineDescription(BaseMessage, frozen=True):
    """A list of KeyLineSelection objects describing the key line for the market"""

    key_line: list[KeyLineSelection]  # A list of KeyLineSelection objects


class MarketBook(BaseMessage, frozen=True):
    """The dynamic data in a market"""

    market_id: MarketId  # The unique identifier for the market
    is_market_data_delayed: bool  # True if the data returned by listMarketBook will be delayed
    bet_delay: int | None = None  # The number of seconds an order is held until it is submitted into the market
    bsp_reconciled: bool | None = None  # True if the market starting price has been reconciled
    complete: bool | None = None  # If false, runners may be added to the market
    cross_matching: bool | None = None  # True if cross-matching is enabled for this market
    inplay: bool | None = None  # True if the market is currently in play
    key_line_description: KeyLineDescription | None = None  # Description of a market's key line
    last_match_time: Date | None = None  # The most recent time an order was executed
    number_of_active_runners: int | None = None  # The number of runners that are currently active
    number_of_runners: int | None = None  # The number of runners in the market
    number_of_winners: int | None = None  # The number of selections that could be settled as winners
    runners_voidable: bool | None = None  # True if runners in the market can be voided
    status: MarketStatus | None = None  # The status of the market
    total_available: float | None = None  # The total amount of orders that remain unmatched
    total_matched: float | None = None  # The total amount matched on the market
    version: int | None = None  # The version of the market
    runners: list[Runner] | None = None  # Information about the runners (selections) in the market
    bet_delay_models: list[BetDelayModel] | None = None  # Indicates which bet delay models are applied to a market


class ItemDescription(BaseMessage, frozen=True):
    """
    This object contains some text which may be useful to render a betting history view.
    It offers no long-term warranty as to the correctness of the text.
    """

    event_type_desc: str | None = None  # The event type name translated into the requested locale
    event_desc: str | None = None  # The event name or openDate + venue translated into the requested locale
    market_desc: str | None = None  # The market name or racing market type translated into the requested locale
    market_type: MarketType | None = None  # The market type e.g. MATCH_ODDS, PLACE, WIN etc.
    market_start_time: Date | None = None  # The start time of the market in ISO-8601 format, not translated
    runner_desc: str | None = None  # The runner name translated into the requested locale
    number_of_winners: int | None = None  # The number of winners on a market
    each_way_divisor: float | None = None  # The divisor for the EACH_WAY market type


class ClearedOrderSummary(BaseMessage, frozen=True):
    """Summary of a cleared order"""

    event_type_id: EventTypeId | None = None  # The id of the event type bet on
    event_id: EventId | None = None  # The id of the event bet on
    market_id: MarketId | None = None  # The id of the market bet on
    selection_id: SelectionId | None = None  # The id of the selection bet on
    handicap: Handicap | None = None  # The handicap value for Asian handicap markets
    bet_id: BetId | None = None  # The id of the bet
    placed_date: Date | None = None  # The date the bet order was placed by the customer
    persistence_type: PersistenceType | None = None  # The turn in play persistence state of the order
    order_type: OrderType | None = None
    side: Side | None = None  # Whether the bet was a back or lay bet
    item_description: ItemDescription | None = None  # Container for ancillary data and localized text
    bet_outcome: str | None = None  # The settlement outcome of the bet
    price_requested: Price | None = None  # The average requested price across all settled bet orders under this item
    settled_date: Date | None = None  # The date and time the bet order was settled by Betfair
    last_matched_date: Date | None = None  # The date and time the last bet order was matched by Betfair
    bet_count: int | None = None  # The number of actual bets within this grouping
    commission: Size | None = None  # Cumulative commission paid by the customer across all bets under this item
    price_matched: Price | None = None  # The average matched price across all settled bets or bet fragments
    price_reduced: bool | None = None  # Indicates if the matched price was affected by a reduction factor
    size_settled: Size | None = None  # The cumulative bet size that was settled as matched or voided under this item
    profit: float | None = None  # The profit or loss gained on this line
    size_cancelled: Size | None = None  # The amount of the bet that was cancelled
    customer_order_ref: CustomerOrderRef | None = None  # Defined by the customer for the bet order
    customer_strategy_ref: CustomerStrategyRef | None = None  # Defined by the customer for the bet order


class ClearedOrderSummaryReport(BaseMessage, frozen=True):
    """A container representing search results"""

    cleared_orders: list[ClearedOrderSummary]  # The list of cleared orders returned by the query
    more_available: bool  # Indicates whether there are further result items beyond this page


class RunnerId(BaseMessage, frozen=True):
    """Unique identifier for a runner"""

    market_id: MarketId  # The id of the market bet on
    selection_id: SelectionId  # The id of the selection bet on
    handicap: Handicap | None = None  # The handicap associated with the runner in case of Asian handicap markets


class CurrentItemDescription(BaseMessage, frozen=True):
    """This object contains ancillary information about the item"""

    market_version: MarketVersion  # The relevant version of the market for this item


class CurrentOrderSummary(BaseMessage, frozen=True):
    """Summary of a current order"""

    bet_id: BetId  # The bet ID of the original place order
    market_id: MarketId  # The market ID the order is for
    selection_id: SelectionId  # The selection ID the order is for
    handicap: Handicap  # The handicap associated with the runner in case of Asian handicap markets
    price_size: PriceSize  # The price and size of the bet
    bsp_liability: Size  # The liability of a given BSP bet
    side: Side  # BACK/LAY
    status: OrderStatus  # The status of the order
    persistence_type: PersistenceType  # What to do with the order at turn-in-play
    order_type: OrderType  # BSP Order type
    placed_date: Date  # The date the bet was placed

    # Date of the last matched bet fragment.
    # Mandatory according to documentation, but optional in reality
    matched_date: Date | None = None
    average_price_matched: Price | None = None  # The average price matched at
    size_matched: Size | None = None
    size_remaining: Size | None = None
    size_lapsed: Size | None = None
    size_cancelled: Size | None = None
    size_voided: Size | None = None
    regulator_auth_code: str | None = None
    regulator_code: str | None = None
    customer_order_ref: str | None = None  # The order reference defined by the customer for this bet
    customer_strategy_ref: str | None = None  # The strategy reference defined by the customer for this bet
    current_item_description: CurrentItemDescription | None = None  # Container for ancillary data for this item


class CurrentOrderSummaryReport(BaseMessage, frozen=True):
    """A container representing search results"""

    current_orders: list[CurrentOrderSummary]  # The list of current orders returned by the query
    more_available: bool  # Indicates whether there are further result items beyond this page


class LimitOrder(BaseMessage, frozen=True):
    """Place a new LIMIT order (simple exchange bet for immediate execution)"""

    size: Size
    price: Price
    persistence_type: PersistenceType | None = None
    time_in_force: TimeInForce | None = None
    min_fill_size: Size | None = None
    bet_target_type: BetTargetType | None = None
    bet_target_size: Size | None = None


class LimitOnCloseOrder(BaseMessage, frozen=True):
    liability: Size
    price: Price


class MarketOnCloseOrder(BaseMessage, frozen=True):
    liability: Size


class PlaceInstruction(BaseMessage, kw_only=True, frozen=True):
    """Instruction to place a new order"""

    order_type: OrderType  # The order type
    selection_id: SelectionId  # The selection ID
    handicap: Handicap | None = None  # The handicap associated with the runner in case of Asian handicap markets
    side: Side  # Back or Lay
    limit_order: LimitOrder | None = None  # A simple exchange bet for immediate execution

    # Bets matched if the returned starting price is better than a specified price
    limit_on_close_order: LimitOnCloseOrder | None = None

    # Bets matched and settled at a price representative of the market at the point it turns in-play
    market_on_close_order: MarketOnCloseOrder | None = None
    customer_order_ref: str | None = None  # An optional reference to identify instructions


class PlaceInstructionReport(BaseMessage, kw_only=True, frozen=True):
    """Report for a place instruction"""

    status: InstructionReportStatus  # The instruction report status
    error_code: InstructionReportErrorCode | None = None
    order_status: OrderStatus | None = None
    instruction: PlaceInstruction  # The place instruction
    bet_id: BetId | None = None  # The bet ID of the placed order, if successful
    placed_date: Date | None = None  # The date and time the bet was placed, if successful
    average_price_matched: Price | None = None  # The average price matched at, if successful
    size_matched: Size | None = None  # The current amount of the bet that was matched, if successful


class PlaceExecutionReport(BaseMessage, kw_only=True, frozen=True):
    customer_ref: CustomerRef | None = None  # Echo of the customer reference if passed
    status: ExecutionReportStatus  # The execution report status
    error_code: ExecutionReportErrorCode | None = None  # The execution report error code
    market_id: MarketId | None = None  # Echo of the market ID passed
    instruction_reports: list[PlaceInstructionReport] | None = None  # The list of place instruction reports


class CancelInstruction(BaseMessage, frozen=True):
    """Instruction to fully or partially cancel an order (only applies to LIMIT orders)"""

    bet_id: BetId
    # If supplied then this is a partial cancel. Should be set to 'null' if no size
    # reduction is required.
    size_reduction: Size | None = None


class ReplaceInstruction(BaseMessage, frozen=True):
    """Instruction to replace a LIMIT or LIMIT_ON_CLOSE order at a new price."""

    bet_id: BetId  # Unique identifier for the bet
    new_price: Price  # The price to replace the bet at


class CancelInstructionReport(BaseMessage, kw_only=True, frozen=True):
    status: InstructionReportStatus  # Whether the command succeeded or failed
    error_code: InstructionReportErrorCode | None = None  # Cause of failure, or null if command succeeds
    instruction: CancelInstruction | None = None  # The instruction that was requested
    size_cancelled: float | None = None  # The API states, that this is mandatory, but it's skipped in case of error
    cancelled_date: Date | None = None  # The API states, that this is mandatory, but it's skipped in case of error


class CancelExecutionReport(BaseMessage, kw_only=True, frozen=True):
    customer_ref: CustomerRef | None = None  # Echo of the customerRef if passed
    status: ExecutionReportStatus
    error_code: ExecutionReportErrorCode | None = None
    market_id: MarketId | None = None  # Echo of marketId passed
    instruction_reports: list[CancelInstructionReport] | None = None


class ReplaceInstructionReport(BaseMessage, frozen=True):
    status: InstructionReportStatus  # Whether the command succeeded or failed
    error_code: InstructionReportErrorCode | None = None  # Cause of failure, or null if command succeeds
    cancel_instruction_report: CancelInstructionReport | None = None  # Cancellation report for the original order
    place_instruction_report: PlaceInstructionReport | None = None  # Placement report for the new order


class ReplaceExecutionReport(BaseMessage, kw_only=True, frozen=True):
    customer_ref: CustomerRef | None = None  # Echo of the customerRef if passed.
    status: ExecutionReportStatus
    error_code: ExecutionReportErrorCode | None = None
    market_id: MarketId | None = None  # Echo of marketId passed
    instruction_reports: list[ReplaceInstructionReport] | None = None


class UpdateInstruction(BaseMessage, frozen=True):
    """Instruction to update LIMIT bet's persistence of an order that do not affect exposure"""

    bet_id: BetId  # Unique identifier for the bet
    new_persistence_type: PersistenceType  # The new persistence type to update this bet to


class UpdateInstructionReport(BaseMessage, kw_only=True, frozen=True):
    status: InstructionReportStatus  # Whether the command succeeded or failed
    error_code: InstructionReportErrorCode | None = None  # Cause of failure, or null if command succeeds
    instruction: UpdateInstruction  # The instruction that was requested


class UpdateExecutionReport(BaseMessage, frozen=True):
    customer_ref: CustomerRef | None  # Echo of the customerRef if passed.
    status: ExecutionReportStatus
    error_code: ExecutionReportErrorCode | None
    market_id: MarketId | None  # Echo of marketId passed
    instruction_reports: list[UpdateInstructionReport] | None


class ExBestOffersOverrides(BaseMessage, frozen=True):
    """Options to alter the default representation of best offer prices"""

    best_prices_depth: int | None = None  # The maximum number of prices to return on each side for each runner
    rollup_model: RollupModel | None = None  # The model to use when rolling up available sizes
    rollup_limit: int | None = None  # The volume limit to use when rolling up returned sizes
    rollup_liability_threshold: float | None = None  # Only applicable when rollupModel is MANAGED_LIABILITY
    rollup_liability_factor: int | None = None  # Only applicable when rollupModel is MANAGED_LIABILITY


class PriceProjection(BaseMessage, frozen=True):
    """Selection criteria of the returning price data"""

    price_data: Set[PriceData] | None = None  # The basic price data you want to receive in the response

    # Options to alter the default representation of best offer prices
    ex_best_offers_overrides: ExBestOffersOverrides | None = None
    virtualise: bool | None = None  # Indicates if the returned prices should include virtual prices

    # Indicates if the volume returned at each price point should be the absolute value or a
    # cumulative sum of volumes available at the price and all better prices. If unspecified
    # defaults to false. Applicable to EX_BEST_OFFERS and EX_ALL_OFFERS price projections.
    # Not supported as yet.
    rollover_stakes: bool | None = None


class RunnerProfitAndLoss(BaseMessage, frozen=True):
    """Profit and loss if selection wins or loses"""

    selection_id: SelectionId | None = None  # The unique identifier for the selection
    if_win: float | None = None  # Profit or loss for the market if this selection is the winner
    if_lose: float | None = None  # Profit or loss for the market if this selection is the loser

    # Profit or loss for the market if this selection is placed (applies to marketType EACH_WAY only)
    if_place: float | None = None


class MarketProfitAndLoss(BaseMessage, frozen=True):
    """Profit and loss in a market"""

    market_id: MarketId | None = None  # The unique identifier for the market
    commission_applied: float | None = None  # The commission rate applied to P&L values
    profit_and_losses: list[RunnerProfitAndLoss] | None = None  # Calculated profit and loss data
