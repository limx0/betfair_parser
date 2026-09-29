from datetime import datetime
from functools import partial
from typing import Annotated

import msgspec
from msgspec.structs import force_setattr

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
    doc,
    method_tag,
)


betting_tag = partial(method_tag, "SportsAPING/v1.0/")


class Competition(BaseMessage, frozen=True):
    id: CompetitionId | None = None
    name: str | None = None


class CompetitionResult(BaseMessage, frozen=True):
    competition: Competition | None = None
    market_count: Annotated[int | None, doc("Count of markets associated with this competition")] = None
    competition_region: Annotated[str | None, doc("Region in which this competition is happening")] = None


class Event(BaseMessage, frozen=True):
    id: Annotated[EventId | None, doc("The unique id for the event")] = None
    name: Annotated[str | None, doc("The name of the event")] = None
    country_code: Annotated[CountryCode | None, doc("The ISO-2 code for the event, defaults to GB")] = None
    timezone: Annotated[str | None, doc("The timezone in which the event is taking place")] = None
    venue: str | None = None
    open_date: Annotated[Date | None, doc("The scheduled start date and time of the event")] = None


class EventResult(BaseMessage, frozen=True):
    event: Event | None = None
    market_count: Annotated[int | None, doc("Count of markets associated with this event")] = None


class EventType(BaseMessage, frozen=True):
    id: EventTypeId | None = None
    name: str | None = None


class EventTypeResult(BaseMessage, frozen=True):
    event_type: Annotated[EventType | None, doc("The ID identifying the Event Type")] = None
    market_count: Annotated[int | None, doc("Count of markets associated with this eventType")] = None


class MarketTypeResult(BaseMessage, frozen=True):
    market_type: str | None = None
    market_count: Annotated[int | None, doc("Count of markets associated with this marketType")] = None


class CountryCodeResult(BaseMessage, frozen=True):
    country_code: Annotated[CountryCode | None, doc("The ISO-2 code for the event")] = None
    market_count: Annotated[int | None, doc("Count of markets associated with this Country Code")] = None


class VenueResult(BaseMessage, frozen=True):
    venue: Venue | None = None
    market_count: Annotated[int | None, doc("Count of markets associated with this Venue")] = None


class PriceSize(BaseMessage, frozen=True):
    price: Annotated[Price, doc("Available price")]
    size: Annotated[Size, doc("Available stake")]


class TimeRangeResult(BaseMessage, frozen=True):
    time_range: TimeRange | None = None
    market_count: Annotated[int | None, doc("Count of markets associated with this TimeRange")] = None


class MarketFilter(BaseMessage, frozen=True):
    bet_delay_models: Annotated[
        Set[BetDelayModel] | None,
        doc("Indicates which bet delay models are applied to a market"),
    ] = None
    bsp_only: Annotated[bool | None, doc("Restrict to bsp markets only if True or non-bsp markets if False")] = None
    competition_ids: Annotated[Set[CompetitionId] | None, doc("Restrict markets by the competitions")] = None
    event_ids: Annotated[Set[EventId] | None, doc("Restrict markets by the event id associated with the market")] = None
    event_type_ids: Annotated[
        Set[EventTypeId] | None,
        doc("Restrict markets by event type associated with the market"),
    ] = None
    exchange_ids: Annotated[
        Set[ExchangeId] | None,
        doc(
            "Restrict markets by the Exchange where the market operates. Note: This is not currently in use and only "
            "entities for the current exchange will be returned"
        ),
    ] = None

    in_play_only: Annotated[
        bool | None,
        doc("Restrict to markets that are currently in play if True or are not currently in play if False"),
    ] = None
    market_betting_types: Annotated[Set[MarketBettingType] | None, doc("Match the betting type of the market")] = None
    market_countries: Annotated[Set[CountryCode] | None, doc("Match the specified country or countries")] = None
    market_ids: Annotated[
        Set[MarketId] | None,
        doc("Restrict markets by the market id associated with the market"),
    ] = None
    market_start_time: Annotated[TimeRange | None, doc("Restrict to markets with a market start time range")] = None
    market_type_codes: Annotated[
        Set[MarketTypeCode] | None,
        doc("Restrict to markets that match the type of the market"),
    ] = None
    race_types: Annotated[Set[str] | None, doc("Restrict by race type")] = None
    text_query: Annotated[str | None, doc("Restrict markets by any text associated with the Event name")] = None

    turn_in_play_enabled: Annotated[
        bool | None,
        doc("Restrict to markets that will turn in play if True or will not turn in play if False"),
    ] = None
    venues: Annotated[Set[Venue] | None, doc("Restrict markets by the venue associated with the market")] = None
    with_orders: Annotated[Set[str] | None, doc("Markets that have one or more orders of defined OrderStatus")] = None


class MarketLineRangeInfo(BaseMessage, frozen=True):
    """Market Line and Range Info"""

    max_unit_value: Annotated[float, doc("Maximum value for the outcome, in market units")]
    min_unit_value: Annotated[float, doc("Minimum value for the outcome, in market units")]
    interval: Annotated[float, doc("The odds ladder increment interval")]
    market_unit: Annotated[str, doc("The type of unit the lines are incremented in")]


class PriceLadderDescription(BaseMessage, frozen=True):
    """Description of the price ladder type and any related data"""

    type: PriceLadderType


class StartingPrices(BaseMessage, frozen=True):
    """Information about the Betfair Starting Price. Only available in BSP markets"""

    near_price: Annotated[float | None, doc("What the starting price would be if the market was reconciled now")] = None
    far_price: Annotated[float | None, doc("What the starting price would be if the market was reconciled now")] = None

    back_stake_taken: Annotated[
        list[PriceSize] | None,
        doc("The total amount of back bets matched at the actual Betfair Starting Price"),
    ] = None
    lay_liability_taken: Annotated[
        list[PriceSize] | None,
        doc("The lay amount matched at the actual Betfair Starting Price"),
    ] = None
    actual_sp: Annotated[
        float | None,
        doc("The final BSP price for this runner"),
    ] = msgspec.field(name="actualSP", default=None)


class ExchangePrices(BaseMessage, frozen=True):
    available_to_back: list[PriceSize] | None = None
    available_to_lay: list[PriceSize] | None = None
    traded_volume: list[PriceSize] | None = None


class Order(BaseMessage, frozen=True):
    bet_id: BetId
    order_type: OrderType
    status: OrderStatus
    persistence_type: PersistenceType
    side: Annotated[Side, doc("Side (BACK or LAY)")]
    price: Price
    size: Size
    bsp_liability: Annotated[Size, doc("Liability of a given BSP bet")]
    placed_date: Annotated[Date, doc("Date and time the bet was placed")]
    avg_price_matched: Annotated[Price | None, doc("Average price matched at")] = None
    size_matched: Annotated[Size | None, doc("Current amount of this bet that was matched")] = None
    size_remaining: Annotated[Size | None, doc("Current amount of this bet that is unmatched")] = None
    size_lapsed: Annotated[Size | None, doc("Current amount of this bet that was lapsed")] = None
    size_cancelled: Annotated[Size | None, doc("Current amount of this bet that was cancelled")] = None
    size_voided: Annotated[Size | None, doc("Current amount of this bet that was voided")] = None
    customer_order_ref: Annotated[CustomerOrderRef | None, doc("Customer Order Reference")] = None
    customer_strategy_ref: Annotated[CustomerStrategyRef | None, doc("Customer Strategy Reference")] = None


class Match(BaseMessage, kw_only=True, frozen=True):
    """An individual bet Match, or rollup by price or avg price.

    Rollup depends on the requested MatchProjection.
    """

    bet_id: Annotated[BetId | None, doc("Bet ID (present if no rollup)")] = None
    match_id: Annotated[MatchId | None, doc("Match ID (present if no rollup)")] = None
    side: Annotated[Side, doc("Side (BACK or LAY)")]
    price: Annotated[Price, doc("Match price")]
    size: Annotated[Size, doc("Size matched at")]
    match_date: Annotated[Date | None, doc("Match date (present if no rollup)")] = None


class MarketVersion(BaseMessage, frozen=True):
    version: Annotated[int | None, doc("A non-monotonically increasing number indicating market changes")] = None


class MarketRates(BaseMessage, frozen=True):
    market_base_rate: Annotated[float, doc("Market base rate")]
    discount_allowed: Annotated[bool, doc("Indicates whether discount is allowed on this market")]


class MarketLicence(BaseMessage, frozen=True):
    wallet: Annotated[str, doc("Wallet from which funds will be taken when betting on this market")]
    rules: str | None = None
    rules_has_date: Annotated[bool | None, doc("Markets start date and time are relevant to the rules")] = None
    clarifications: Annotated[str | None, doc("Clarifications to the rules for the market")] = None


class MarketDescription(BaseMessage, kw_only=True, frozen=True):
    bet_delay_models: Annotated[
        list[BetDelayModel] | None,
        doc("Indicates which bet delay models are applied to a market"),
    ] = None
    betting_type: MarketBettingType
    bsp_market: Annotated[bool, doc("Indicates if the market supports Betfair SP betting")]
    clarifications: Annotated[str | None, doc("Additional information regarding the market")] = None
    discount_allowed: Annotated[bool, doc("Indicates whether user's discount rate is taken into account on this")]
    each_way_divisor: Annotated[float | None, doc("Each Way Divisor for E/W markets")] = None
    line_range_info: Annotated[MarketLineRangeInfo | None, doc("Line range info for line markets")] = None
    market_base_rate: Annotated[float, doc("Commission rate applicable to the market")]
    market_time: Annotated[Date, doc("Scheduled start time of the market")]
    market_type: Annotated[str, doc("Market base type")]
    persistence_enabled: Annotated[bool, doc("Indicates if the market supports 'Keep' bets if turned in-play")]
    price_ladder_description: Annotated[
        PriceLadderDescription | None,
        doc("Details about the price ladder in use"),
    ] = None
    race_type: Annotated[str | None, doc("External identifier of a race type")] = None
    regulator: Annotated[str, doc("Market regulator")]
    rules: Annotated[str | None, doc("The market rules")] = None
    rules_has_date: Annotated[bool | None, doc("Indicates whether rules have a date included")] = None
    settle_time: Date | None = None
    suspend_time: Annotated[Date, doc("Next time the market will be suspended for betting, usually just marketTime")]
    turn_in_play_enabled: Annotated[bool, doc("Indicates if the market is set to turn in-play")]
    wallet: Annotated[str | None, doc("The wallet to which the market belongs")] = None


# TODO: Some fields in the meta data should be country codes. Unfortunately, sometimes they contain
#       erroneous data that fails verification. This should be switched to CountryCode as soon as there is
#       some more fine-grained error handling possible in msgspec. Related issue:
#       https://github.com/jcrist/msgspec/issues/420
_MetaCountryCode = str  # CountryCode


class RunnerMetaData(BaseMessage, frozen=True, rename="upper"):
    # Yes, this is the only type definition, that has (mostly) upper-case key names
    """
    Runner metadata as defined in the API as additional information.
    https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2686993/Additional+Information#AdditionalInformation-RunnerMetadataDescription
    """

    adjusted_rating: Annotated[
        int | None,
        doc("Race-specific ratings that reflect weights allocated in the race"),
    ] = None
    age: Annotated[int | None, doc("The age of the horse")] = None
    bred: Annotated[_MetaCountryCode | None, doc("The country in which the horse was born")] = None
    cloth_number: Annotated[int | str | None, doc("The number on the saddle-cloth")] = None
    cloth_number_alpha: Annotated[
        str | None,
        doc('The number on the saddle cloth for US paired runners, e.g. "1A"'),
    ] = None
    colour_type: Annotated[str | None, doc("The colour of the horse")] = None
    colours_description: Annotated[str | None, doc("The textual description of the jockey silk")] = None
    colours_filename: Annotated[str | None, doc("Image representing the jockey silk")] = None
    colours_filename_url: Annotated[
        str | None,
        doc("The full URL to an image file corresponding to the jockey silk"),
    ] = None
    dam_bred: Annotated[_MetaCountryCode | None, doc("The country where the horse's mother was born")] = None
    dam_name: Annotated[str | None, doc("The name of the horse's mother")] = None
    dam_year_born: Annotated[int | None, doc("The year the horse’s mother's birth")] = None
    damsire_bred: Annotated[_MetaCountryCode | None, doc("The country where the horse's grandfather was born")] = None
    damsire_name: Annotated[str | None, doc("The name of the horse's grandfather")] = None
    damsire_year_born: Annotated[
        int | None,
        doc("Year in which the horse's grandfather was born on its mother's side"),
    ] = None
    days_since_last_run: Annotated[int | None, doc("The number of days since the horse last ran")] = None
    forecastprice_denominator: Annotated[int | None, doc("The forecast price denominator")] = None
    forecastprice_numerator: Annotated[int | None, doc("The forecast price numerator")] = None
    form: Annotated[str | None, doc("The horses recent form")] = None
    jockey_claim: Annotated[
        int | None,
        doc("Reduction in the weight that the horse carries for a particular jockey"),
    ] = None
    jockey_name: Annotated[
        str | None,
        doc("Name of the jockey. This field will contain 'Reserve' if it's a reserve runner"),
    ] = None
    official_rating: Annotated[int | None, doc("The horses official rating")] = None
    owner_name: Annotated[str | None, doc("The owner of the horse")] = None
    runner_id: Annotated[int | None, doc("The runnerId for the horse")] = msgspec.field(name="runnerId", default=None)
    sex_type: Annotated[str | None, doc("The sex of the horse")] = None
    sire_bred: Annotated[_MetaCountryCode | None, doc("The country where the horse's father was bred")] = None
    sire_name: Annotated[str | None, doc("The name of the horse's father")] = None
    sire_year_born: Annotated[int | None, doc("The year the horse's father was born")] = None
    stall_draw: Annotated[int | None, doc("The stall number the horse is starting from")] = None
    trainer_name: Annotated[str | None, doc("The name of the horse's trainer")] = None
    wearing: Annotated[str | None, doc("Any extra equipment the horse is wearing")] = None
    weight_units: Annotated[str | None, doc("The unit of weight used.")] = None
    weight_value: Annotated[float | None, doc("The weight of the horse")] = None

    def __post_init__(self):
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
        if self.age is not None and not 1 < self.age < 30:
            force_setattr(self, "age", None)
        if isinstance(self.cloth_number, str):
            try:
                cloth_number = int("".join(filter(str.isdigit, self.cloth_number)))
            except ValueError:
                cloth_number = None
            force_setattr(self, "cloth_number", cloth_number)
        if self.cloth_number is not None and not 0 < self.cloth_number < 50:  # type: ignore[operator]
            force_setattr(self, "cloth_number", None)

    @property
    def colours_url(self):
        return self.colours_filename_url

    @property
    def forecastprice_decimal(self):
        if not self.forecastprice_numerator or not self.forecastprice_denominator:
            return None
        return self.forecastprice_numerator / self.forecastprice_denominator + 1


class RunnerCatalog(BaseMessage, frozen=True):
    """Information about the Runners (selections) in a market"""

    selection_id: Annotated[SelectionId, doc("The unique id for the selection")]
    runner_name: Annotated[str, doc("The name of the runner")]

    handicap: Annotated[
        Handicap,
        doc(
            "The handicap applies to market with the MarketBettingType ASIAN_HANDICAP_SINGLE_LINE & "
            "ASIAN_HANDICAP_DOUBLE_LINE only"
        ),
    ]
    sort_priority: Annotated[int | None, doc("This is marked as REQUIRED in the API doc, but omitted sometimes")] = None
    metadata: Annotated[RunnerMetaData | None, doc("Metadata associated with the runner")] = None

    @property
    def name(self):
        return self.runner_name


class Runner(BaseMessage, frozen=True):
    """The dynamic data about runners in a market"""

    selection_id: Annotated[SelectionId, doc("The unique id of the runner (selection)")]
    handicap: Handicap
    status: Annotated[RunnerStatus, doc("The status of the selection")]
    adjustment_factor: Annotated[float | None, doc("The adjustment factor applied if the selection is removed")] = None
    last_price_traded: Annotated[float | None, doc("The price of the most recent bet matched on this selection")] = None
    total_matched: Annotated[float | None, doc("The total amount matched on this runner")] = None
    removal_date: Annotated[Date | None, doc("If date and time the runner was removed")] = None
    sp: Annotated[StartingPrices | None, doc("The BSP related prices for this runner")] = None
    ex: Annotated[ExchangePrices | None, doc("The Exchange prices available for this runner")] = None
    orders: Annotated[list[Order] | None, doc("List of orders in the market")] = None
    matches: Annotated[
        list[Match] | None,
        doc("List of matches (i.e., orders that have been fully or partially executed)"),
    ] = None
    matches_by_strategy: Annotated[
        dict[str, list[Match]] | None,
        doc("List of matches keyed by strategy, ordered by matched data"),
    ] = None


class MarketCatalogue(BaseMessage, frozen=True):
    market_id: Annotated[MarketId, doc("The unique identifier for the market")]
    market_name: Annotated[str, doc("The name of the market")]
    market_start_time: Annotated[Date | None, doc("Only returned when the MARKET_START_TIME enum is requested")] = None
    total_matched: Annotated[float | None, doc("The total amount of money matched on the market")] = None
    event_type: Annotated[EventType | None, doc("The Event Type the market is contained within")] = None
    competition: Annotated[Competition | None, doc("The competition the market is contained within")] = None
    description: Annotated[MarketDescription | None, doc("Details about the market")] = None
    event: Annotated[Event | None, doc("The event the market is contained within")] = None
    runners: Annotated[list[RunnerCatalog] | None, doc("The runners (selections) contained in the market")] = None


class KeyLineSelection(BaseMessage, frozen=True):
    """Description of a market's key line selection"""

    selection_id: Annotated[SelectionId, doc("Selection ID of the runner in the key line handicap")]
    handicap: Annotated[Handicap, doc("Handicap value of the key line")]


class KeyLineDescription(BaseMessage, frozen=True):
    """A list of KeyLineSelection objects describing the key line for the market"""

    key_line: Annotated[list[KeyLineSelection], doc("A list of KeyLineSelection objects")]


class MarketBook(BaseMessage, frozen=True):
    """The dynamic data in a market"""

    market_id: Annotated[MarketId, doc("The unique identifier for the market")]
    is_market_data_delayed: Annotated[bool, doc("True if the data returned by listMarketBook will be delayed")]
    bet_delay: Annotated[
        int | None,
        doc("The number of seconds an order is held until it is submitted into the market"),
    ] = None
    bsp_reconciled: Annotated[bool | None, doc("True if the market starting price has been reconciled")] = None
    complete: Annotated[bool | None, doc("If false, runners may be added to the market")] = None
    cross_matching: Annotated[bool | None, doc("True if cross-matching is enabled for this market")] = None
    inplay: Annotated[bool | None, doc("True if the market is currently in play")] = None
    key_line_description: Annotated[KeyLineDescription | None, doc("Description of a market's key line")] = None
    last_match_time: Annotated[Date | None, doc("The most recent time an order was executed")] = None
    number_of_active_runners: Annotated[int | None, doc("The number of runners that are currently active")] = None
    number_of_runners: Annotated[int | None, doc("The number of runners in the market")] = None
    number_of_winners: Annotated[int | None, doc("The number of selections that could be settled as winners")] = None
    runners_voidable: Annotated[bool | None, doc("True if runners in the market can be voided")] = None
    status: Annotated[MarketStatus | None, doc("The status of the market")] = None
    total_available: Annotated[float | None, doc("The total amount of orders that remain unmatched")] = None
    total_matched: Annotated[float | None, doc("The total amount matched on the market")] = None
    version: Annotated[int | None, doc("The version of the market")] = None
    runners: Annotated[list[Runner] | None, doc("Information about the runners (selections) in the market")] = None
    bet_delay_models: Annotated[
        list[BetDelayModel] | None,
        doc("Indicates which bet delay models are applied to a market"),
    ] = None


class ItemDescription(BaseMessage, frozen=True):
    """
    This object contains some text which may be useful to render a betting history view.
    It offers no long-term warranty as to the correctness of the text.
    """

    event_type_desc: Annotated[str | None, doc("The event type name translated into the requested locale")] = None
    event_desc: Annotated[
        str | None,
        doc("The event name or openDate + venue translated into the requested locale"),
    ] = None
    market_desc: Annotated[
        str | None,
        doc("The market name or racing market type translated into the requested locale"),
    ] = None
    market_type: Annotated[MarketType | None, doc("The market type e.g. MATCH_ODDS, PLACE, WIN etc.")] = None
    market_start_time: Annotated[
        Date | None,
        doc("The start time of the market in ISO-8601 format, not translated"),
    ] = None
    runner_desc: Annotated[str | None, doc("The runner name translated into the requested locale")] = None
    number_of_winners: Annotated[int | None, doc("The number of winners on a market. Available at BET groupBy")] = None
    each_way_divisor: Annotated[float | None, doc("The odds divisor applicable to EachWay markets")] = None


class ClearedOrderSummary(BaseMessage, frozen=True):
    """Summary of a cleared order"""

    event_type_id: Annotated[EventTypeId | None, doc("The id of the event type bet on")] = None
    event_id: Annotated[EventId | None, doc("The id of the event bet on")] = None
    market_id: Annotated[MarketId | None, doc("The id of the market bet on")] = None
    selection_id: Annotated[SelectionId | None, doc("The id of the selection bet on")] = None
    handicap: Annotated[Handicap | None, doc("The handicap value for Asian handicap markets")] = None
    bet_id: Annotated[BetId | None, doc("The id of the bet")] = None
    placed_date: Annotated[Date | None, doc("The date the bet order was placed by the customer")] = None
    persistence_type: Annotated[PersistenceType | None, doc("The turn in play persistence state of the order")] = None
    order_type: OrderType | None = None
    side: Annotated[Side | None, doc("Whether the bet was a back or lay bet")] = None
    item_description: Annotated[
        ItemDescription | None, doc("A container for all the ancillary data and localised text valid for this Item")
    ] = None
    bet_outcome: Annotated[str | None, doc("The settlement outcome of the bet")] = None
    price_requested: Annotated[
        Price | None,
        doc("The average requested price across all settled bet orders under this item"),
    ] = None
    settled_date: Annotated[Date | None, doc("The date and time the bet order was settled by Betfair")] = None
    last_matched_date: Annotated[Date | None, doc("The date and time the last bet order was matched by Betfair")] = None
    bet_count: Annotated[int | None, doc("The number of actual bets within this grouping")] = None
    commission: Annotated[
        Size | None,
        doc("Cumulative commission paid by the customer across all bets under this item"),
    ] = None
    price_matched: Annotated[
        Price | None,
        doc("The average matched price across all settled bets or bet fragments"),
    ] = None
    price_reduced: Annotated[
        bool | None,
        doc("Indicates if the matched price was affected by a reduction factor"),
    ] = None
    size_settled: Annotated[
        Size | None,
        doc("The cumulative bet size that was settled as matched or voided under this item"),
    ] = None
    profit: Annotated[float | None, doc("The profit or loss gained on this line")] = None
    size_cancelled: Annotated[Size | None, doc("The amount of the bet that was cancelled")] = None
    customer_order_ref: Annotated[CustomerOrderRef | None, doc("Defined by the customer for the bet order")] = None
    customer_strategy_ref: Annotated[
        CustomerStrategyRef | None,
        doc("Defined by the customer for the bet order"),
    ] = None


class ClearedOrderSummaryReport(BaseMessage, frozen=True):
    """A container representing search results"""

    cleared_orders: Annotated[list[ClearedOrderSummary], doc("The list of cleared orders returned by the query")]
    more_available: Annotated[bool, doc("Indicates whether there are further result items beyond this page")]


class RunnerId(BaseMessage, frozen=True):
    """Unique identifier for a runner"""

    market_id: Annotated[MarketId, doc("The id of the market bet on")]
    selection_id: Annotated[SelectionId, doc("The id of the selection bet on")]
    handicap: Annotated[
        Handicap | None,
        doc("The handicap associated with the runner in case of Asian handicap markets"),
    ] = None


class CurrentItemDescription(BaseMessage, frozen=True):
    """This object contains ancillary information about the item"""

    market_version: Annotated[MarketVersion, doc("The relevant version of the market for this item")]


class CurrentOrderSummary(BaseMessage, frozen=True):
    """Summary of a current order"""

    bet_id: Annotated[BetId, doc("The bet ID of the original place order")]
    market_id: Annotated[MarketId, doc("The market ID the order is for")]
    selection_id: Annotated[SelectionId, doc("The selection ID the order is for")]
    handicap: Annotated[Handicap, doc("The handicap of the bet")]
    price_size: Annotated[PriceSize, doc("The price and size of the bet")]
    bsp_liability: Annotated[Size, doc("The liability of a given BSP bet")]
    side: Annotated[Side, doc("BACK/LAY")]
    status: Annotated[
        OrderStatus,
        doc("Either EXECUTABLE (an unmatched amount remains) or EXECUTION_COMPLETE (no unmatched amount remains)"),
    ]
    persistence_type: Annotated[PersistenceType, doc("What to do with the order at turn-in-play")]
    order_type: Annotated[OrderType, doc("BSP Order type")]
    placed_date: Annotated[Date, doc("The date the bet was placed")]

    matched_date: Annotated[
        Date | None,
        doc("Date of the last matched bet fragment. Mandatory according to documentation, but optional in reality"),
    ] = None
    average_price_matched: Annotated[Price | None, doc("The average price matched at")] = None
    size_matched: Size | None = None
    size_remaining: Size | None = None
    size_lapsed: Size | None = None
    size_cancelled: Size | None = None
    size_voided: Size | None = None
    regulator_auth_code: str | None = None
    regulator_code: str | None = None
    customer_order_ref: Annotated[str | None, doc("The order reference defined by the customer for this bet")] = None
    customer_strategy_ref: Annotated[
        str | None,
        doc("The strategy reference defined by the customer for this bet"),
    ] = None
    current_item_description: Annotated[
        CurrentItemDescription | None,
        doc("Container for ancillary data for this item"),
    ] = None


class CurrentOrderSummaryReport(BaseMessage, frozen=True):
    """A container representing search results"""

    current_orders: Annotated[list[CurrentOrderSummary], doc("The list of current orders returned by the query")]
    more_available: Annotated[bool, doc("Indicates whether there are further result items beyond this page")]


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

    order_type: Annotated[OrderType, doc("The order type")]
    selection_id: Annotated[SelectionId, doc("The selection ID")]
    handicap: Annotated[
        Handicap | None,
        doc("The handicap applied to the selection, if on an asian-style market"),
    ] = None
    side: Annotated[Side, doc("Back or Lay")]
    limit_order: Annotated[LimitOrder | None, doc("A simple exchange bet for immediate execution")] = None

    limit_on_close_order: Annotated[
        LimitOnCloseOrder | None,
        doc("Bets matched if the returned starting price is better than a specified price"),
    ] = None

    market_on_close_order: Annotated[
        MarketOnCloseOrder | None,
        doc("Bets matched and settled at a price representative of the market at the point it turns in-play"),
    ] = None
    customer_order_ref: Annotated[str | None, doc("An optional reference to identify instructions")] = None


class PlaceInstructionReport(BaseMessage, kw_only=True, frozen=True):
    """Report for a place instruction"""

    status: Annotated[InstructionReportStatus, doc("Whether the command succeeded or failed")]
    error_code: InstructionReportErrorCode | None = None
    order_status: OrderStatus | None = None
    instruction: Annotated[PlaceInstruction, doc("The instruction that was requested")]
    bet_id: Annotated[BetId | None, doc("The bet ID of the placed order, if successful")] = None
    placed_date: Annotated[Date | None, doc("Will be null if order was placed asynchronously")] = None
    average_price_matched: Annotated[
        Price | None,
        doc(
            "Will be null if order was placed asynchronously. This value is not meaningful for activity on LINE "
            "markets and is not guaranteed to be returned or maintained for these markets"
        ),
    ] = None
    size_matched: Annotated[Size | None, doc("Will be null if order was placed asynchronously")] = None


class PlaceExecutionReport(BaseMessage, kw_only=True, frozen=True):
    customer_ref: Annotated[CustomerRef | None, doc("Echo of the customerRef if passed")] = None
    status: Annotated[ExecutionReportStatus, doc("The execution report status")]
    error_code: Annotated[ExecutionReportErrorCode | None, doc("The execution report error code")] = None
    market_id: Annotated[MarketId | None, doc("Echo of marketId passed")] = None
    instruction_reports: Annotated[
        list[PlaceInstructionReport] | None,
        doc("The list of place instruction reports"),
    ] = None


class CancelInstruction(BaseMessage, frozen=True):
    """Instruction to fully or partially cancel an order (only applies to LIMIT orders)"""

    bet_id: BetId
    size_reduction: Annotated[
        Size | None,
        doc("If supplied then this is a partial cancel. Should be set to 'null' if no size reduction is required."),
    ] = None


class ReplaceInstruction(BaseMessage, frozen=True):
    """Instruction to replace a LIMIT or LIMIT_ON_CLOSE order at a new price."""

    bet_id: Annotated[BetId, doc("Unique identifier for the bet")]
    new_price: Annotated[Price, doc("The price to replace the bet at")]


class CancelInstructionReport(BaseMessage, kw_only=True, frozen=True):
    status: Annotated[InstructionReportStatus, doc("Whether the command succeeded or failed")]
    error_code: Annotated[
        InstructionReportErrorCode | None,
        doc("Cause of failure, or null if command succeeds"),
    ] = None
    instruction: Annotated[CancelInstruction | None, doc("The instruction that was requested")] = None
    size_cancelled: Annotated[
        float | None,
        doc("The API states, that this is mandatory, but it's skipped in case of error"),
    ] = None
    cancelled_date: Annotated[
        Date | None,
        doc("The API states, that this is mandatory, but it's skipped in case of error"),
    ] = None


class CancelExecutionReport(BaseMessage, kw_only=True, frozen=True):
    customer_ref: Annotated[CustomerRef | None, doc("Echo of the customerRef if passed")] = None
    status: ExecutionReportStatus
    error_code: ExecutionReportErrorCode | None = None
    market_id: Annotated[MarketId | None, doc("Echo of marketId passed")] = None
    instruction_reports: list[CancelInstructionReport] | None = None


class ReplaceInstructionReport(BaseMessage, frozen=True):
    status: Annotated[InstructionReportStatus, doc("Whether the command succeeded or failed")]
    error_code: Annotated[
        InstructionReportErrorCode | None,
        doc("Cause of failure, or null if command succeeds"),
    ] = None
    cancel_instruction_report: Annotated[
        CancelInstructionReport | None,
        doc("Cancellation report for the original order"),
    ] = None
    place_instruction_report: Annotated[PlaceInstructionReport | None, doc("Placement report for the new order")] = None


class ReplaceExecutionReport(BaseMessage, kw_only=True, frozen=True):
    customer_ref: Annotated[CustomerRef | None, doc("Echo of the customerRef if passed.")] = None
    status: ExecutionReportStatus
    error_code: ExecutionReportErrorCode | None = None
    market_id: Annotated[MarketId | None, doc("Echo of marketId passed")] = None
    instruction_reports: list[ReplaceInstructionReport] | None = None


class UpdateInstruction(BaseMessage, frozen=True):
    """Instruction to update LIMIT bet's persistence of an order that do not affect exposure"""

    bet_id: Annotated[BetId, doc("Unique identifier for the bet")]
    new_persistence_type: Annotated[PersistenceType, doc("The new persistence type to update this bet to")]


class UpdateInstructionReport(BaseMessage, kw_only=True, frozen=True):
    status: Annotated[InstructionReportStatus, doc("Whether the command succeeded or failed")]
    error_code: Annotated[
        InstructionReportErrorCode | None,
        doc("Cause of failure, or null if command succeeds"),
    ] = None
    instruction: Annotated[UpdateInstruction, doc("The instruction that was requested")]


class UpdateExecutionReport(BaseMessage, frozen=True):
    customer_ref: Annotated[CustomerRef | None, doc("Echo of the customerRef if passed.")]
    status: ExecutionReportStatus
    error_code: ExecutionReportErrorCode | None
    market_id: Annotated[MarketId | None, doc("Echo of marketId passed")]
    instruction_reports: list[UpdateInstructionReport] | None


class ExBestOffersOverrides(BaseMessage, frozen=True):
    """Options to alter the default representation of best offer prices"""

    best_prices_depth: Annotated[
        int | None,
        doc("The maximum number of prices to return on each side for each runner"),
    ] = None
    rollup_model: Annotated[RollupModel | None, doc("The model to use when rolling up available sizes")] = None
    rollup_limit: Annotated[int | None, doc("The volume limit to use when rolling up returned sizes")] = None
    rollup_liability_threshold: Annotated[
        float | None,
        doc("Only applicable when rollupModel is MANAGED_LIABILITY"),
    ] = None
    rollup_liability_factor: Annotated[int | None, doc("Only applicable when rollupModel is MANAGED_LIABILITY")] = None


class PriceProjection(BaseMessage, frozen=True):
    """Selection criteria of the returning price data"""

    price_data: Annotated[Set[PriceData] | None, doc("The basic price data you want to receive in the response")] = None

    ex_best_offers_overrides: Annotated[
        ExBestOffersOverrides | None,
        doc("Options to alter the default representation of best offer prices"),
    ] = None
    virtualise: Annotated[bool | None, doc("Indicates if the returned prices should include virtual prices")] = None

    rollover_stakes: Annotated[
        bool | None,
        doc(
            "Indicates if the volume returned at each price point should be the absolute value or a cumulative sum of "
            "volumes available at the price and all better prices. If unspecified defaults to false. Applicable to "
            "EX_BEST_OFFERS and EX_ALL_OFFERS price projections. Not supported as yet."
        ),
    ] = None


class RunnerProfitAndLoss(BaseMessage, frozen=True):
    """Profit and loss if selection wins or loses"""

    selection_id: Annotated[SelectionId | None, doc("The unique identifier for the selection")] = None
    if_win: Annotated[float | None, doc("Profit or loss for the market if this selection is the winner")] = None
    if_lose: Annotated[float | None, doc("Profit or loss for the market if this selection is the loser")] = None

    if_place: Annotated[
        float | None,
        doc("Profit or loss for the market if this selection is placed (applies to marketType EACH_WAY only)"),
    ] = None


class MarketProfitAndLoss(BaseMessage, frozen=True):
    """Profit and loss in a market"""

    market_id: Annotated[MarketId | None, doc("The unique identifier for the market")] = None
    commission_applied: Annotated[float | None, doc("The commission rate applied to P&L values")] = None
    profit_and_losses: Annotated[list[RunnerProfitAndLoss] | None, doc("Calculated profit and loss data")] = None
