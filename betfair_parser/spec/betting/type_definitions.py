from typing import Optional

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
)


class Competition(BaseMessage, frozen=True):
    id: Optional[CompetitionId] = None
    name: Optional[str] = None


class CompetitionResult(BaseMessage, frozen=True):
    competition: Optional[Competition] = None
    marketCount: Optional[int] = None  # Count of markets associated with this competition
    competitionRegion: Optional[str] = None  # Region in which this competition is happening


class Event(BaseMessage, frozen=True):
    id: Optional[EventId] = None  # The unique id for the event
    name: Optional[str] = None  # The name of the event
    countryCode: Optional[CountryCode] = None  # The ISO-2 code for the event, defaults to GB
    timezone: Optional[str] = None  # The timezone in which the event is taking place
    venue: Optional[str] = None
    openDate: Optional[Date] = None  # The scheduled start date and time of the event


class EventResult(BaseMessage, frozen=True):
    event: Optional[Event] = None
    marketCount: Optional[int] = None  # Count of markets associated with this event


class EventType(BaseMessage, frozen=True):
    id: Optional[EventTypeId] = None
    name: Optional[str] = None


class EventTypeResult(BaseMessage, frozen=True):
    eventType: Optional[EventType] = None  # The ID identifying the Event Type
    marketCount: Optional[int] = None  # Count of markets associated with this eventType


class MarketTypeResult(BaseMessage, frozen=True):
    marketType: Optional[str] = None
    marketCount: Optional[int] = None  # Count of markets associated with this marketType


class CountryCodeResult(BaseMessage, frozen=True):
    countryCode: Optional[CountryCode] = None  # The ISO-2 code for the event
    marketCount: Optional[int] = None  # Count of markets associated with this Country Code


class VenueResult(BaseMessage, frozen=True):
    venue: Optional[Venue] = None
    marketCount: Optional[int] = None  # Count of markets associated with this Venue


class PriceSize(BaseMessage, frozen=True):
    price: Price  # Available price
    size: Size  # Available stake


class TimeRangeResult(BaseMessage, frozen=True):
    timeRange: Optional[TimeRange] = None
    marketCount: Optional[int] = None  # Count of markets associated with this TimeRange


class MarketFilter(BaseMessage, frozen=True):
    textQuery: Optional[str] = None  # Restrict markets by any text associated with the Event name
    exchangeIds: Optional[set[ExchangeId]] = None  # DEPRECATED
    eventTypeIds: Optional[set[EventTypeId]] = None  # Restrict markets by event type associated with the market
    eventIds: Optional[set[EventId]] = None  # Restrict markets by the event id associated with the market
    competitionIds: Optional[
        set[CompetitionId]
    ] = None  # Restrict markets by the competitions associated with the market
    marketIds: Optional[set[MarketId]] = None  # Restrict markets by the market id associated with the market
    venues: Optional[set[Venue]] = None  # Restrict markets by the venue associated with the market
    bspOnly: Optional[bool] = None  # Restrict to bsp markets only if True or non-bsp markets if False

    # Restrict to markets that will turn in play if True or will not turn in play if False
    turnInPlayEnabled: Optional[bool] = None

    # Restrict to markets that are currently in play if True or are not currently in play if False
    inPlayOnly: Optional[bool] = None
    marketBettingTypes: Optional[
        set[MarketBettingType]
    ] = None  # Restrict to markets that match the betting type of the market
    marketCountries: Optional[
        set[CountryCode]
    ] = None  # Restrict to markets that are in the specified country or countries
    marketTypeCodes: Optional[set[str]] = None  # Restrict to markets that match the type of the market
    marketStartTime: Optional[TimeRange] = None  # Restrict to markets with a market start time range
    withOrders: Optional[set[str]] = None  # Restrict to markets that I have one or more orders in these status
    raceTypes: Optional[set[str]] = None  # Restrict by race type


class MarketLineRangeInfo(BaseMessage, frozen=True):
    """Market Line and Range Info"""

    maxUnitValue: float  # Maximum value for the outcome, in market units
    minUnitValue: float  # Minimum value for the outcome, in market units
    interval: float  # The odds ladder increment interval
    marketUnit: str  # The type of unit the lines are incremented in


class PriceLadderDescription(BaseMessage, frozen=True):
    """Description of the price ladder type and any related data"""

    type: PriceLadderType


class StartingPrices(BaseMessage, frozen=True):
    """Information about the Betfair Starting Price. Only available in BSP markets"""

    nearPrice: Optional[float] = None  # What the starting price would be if the market was reconciled now
    farPrice: Optional[float] = None  # What the starting price would be if the market was reconciled now

    # The total amount of back bets matched at the actual Betfair Starting Price
    backStakeTaken: Optional[list[PriceSize]] = None
    layLiabilityTaken: Optional[list[PriceSize]] = None  # The lay amount matched at the actual Betfair Starting Price
    actualSP: Optional[float] = None  # The final BSP price for this runner


class ExchangePrices(BaseMessage, frozen=True):
    availableToBack: Optional[list[PriceSize]] = None
    availableToLay: Optional[list[PriceSize]] = None
    tradedVolume: Optional[list[PriceSize]] = None


class Order(BaseMessage, frozen=True):
    betId: BetId
    orderType: OrderType
    status: OrderStatus
    persistenceType: PersistenceType
    side: Side  # Side (BACK or LAY)
    price: Price
    size: Size
    bspLiability: Size  # Liability of a given BSP bet
    placedDate: Date  # Date and time the bet was placed
    avgPriceMatched: Optional[Price] = None  # Average price matched at
    sizeMatched: Optional[Size] = None  # Current amount of this bet that was matched
    sizeRemaining: Optional[Size] = None  # Current amount of this bet that is unmatched
    sizeLapsed: Optional[Size] = None  # Current amount of this bet that was lapsed
    sizeCancelled: Optional[Size] = None  # Current amount of this bet that was cancelled
    sizeVoided: Optional[Size] = None  # Current amount of this bet that was voided
    customerOrderRef: Optional[CustomerOrderRef] = None  # Customer Order Reference
    customerStrategyRef: Optional[CustomerStrategyRef] = None  # Customer Strategy Reference


class Match(BaseMessage, kw_only=True, frozen=True):
    """An individual bet Match, or rollup by price or avg price. Rollup depends on
    the requested MatchProjection.
    """

    betId: Optional[BetId] = None  # Bet ID (present if no rollup)
    matchId: Optional[MatchId] = None  # Match ID (present if no rollup)
    side: Side  # Side (BACK or LAY)
    price: Price  # Match price
    size: Size  # Size matched at
    matchDate: Optional[Date] = None  # Match date (present if no rollup)


class MarketVersion(BaseMessage, frozen=True):
    version: Optional[int] = None  # A non-monotonically increasing number indicating market changes


class MarketRates(BaseMessage, frozen=True):
    marketBaseRate: float  # Market base rate
    discountAllowed: bool  # Indicates whether discount is allowed on this market


class MarketLicence(BaseMessage, frozen=True):
    wallet: str  # Wallet from which funds will be taken when betting on this market
    rules: Optional[str] = None
    rulesHasDate: Optional[bool] = None  # Indicates whether the market's start date and time are relevant to the rules
    clarifications: Optional[str] = None  # Clarifications to the rules for the market


class MarketDescription(BaseMessage, kw_only=True, frozen=True):
    persistenceEnabled: bool  # Indicates if the market supports 'Keep' bets if turned in-play
    bspMarket: bool  # Indicates if the market supports Betfair SP betting
    marketTime: Date  # Scheduled start time of the market
    suspendTime: Date  # Next time the market will be suspended for betting, usually just marketTime
    settleTime: Optional[Date] = None
    bettingType: MarketBettingType
    turnInPlayEnabled: bool  # Indicates if the market is set to turn in-play
    marketType: str  # Market base type
    regulator: str  # Market regulator
    marketBaseRate: float  # Commission rate applicable to the market
    discountAllowed: bool  # Indicates whether user's discount rate is taken into account on this
    wallet: Optional[str] = None  # The wallet to which the market belongs
    rules: Optional[str] = None  # The wallet to which the market belongs
    rulesHasDate: Optional[bool] = None  # Indicates whether rules have a date included
    eachWayDivisor: Optional[float] = None  # Divisor for EACH_WAY market type
    clarifications: Optional[str] = None  # Additional information regarding the market
    lineRangeInfo: Optional[MarketLineRangeInfo] = None  # Line range info for line markets
    raceType: Optional[str] = None  # External identifier of a race type
    priceLadderDescription: Optional[PriceLadderDescription] = None  # Details about the price ladder in use


class RunnerCatalog(BaseMessage, frozen=True):
    """Information about the Runners (selections) in a market"""

    selectionId: int  # The unique id for the selection
    runnerName: str  # The name of the runner

    # The handicap applies to market with the MarketBettingType ASIAN_HANDICAP_SINGLE_LINE
    # & ASIAN_HANDICAP_DOUBLE_LINE only
    handicap: float
    sortPriority: Optional[int] = None  # This is marked as REQUIRED in the API doc, but omitted sometimes
    metadata: Optional[dict[str, Optional[str]]] = None  # Metadata associated with the runner

    @property
    def runner_name(self):
        # TODO: This should be gone, as soon all fields are renamed
        return self.runnerName

    @property
    def runner_id(self):
        # TODO: Careful, selectionId is simply a number for a certain string. It's not
        #       uniquely identifying a team or a certain horse.
        if self.selectionId:
            return self.selectionId
        elif self.metadata.get("runnerId"):
            return int(self.metadata.get("runnerId"))
        return None


class Runner(BaseMessage, frozen=True):
    """The dynamic data about runners in a market"""

    selectionId: int  # The unique id of the runner (selection)
    handicap: float  # The handicap
    status: RunnerStatus  # The status of the selection
    adjustmentFactor: Optional[float] = None  # The adjustment factor applied if the selection is removed
    lastPriceTraded: Optional[float] = None  # The price of the most recent bet matched on this selection
    totalMatched: Optional[float] = None  # The total amount matched on this runner
    removalDate: Optional[Date] = None  # If date and time the runner was removed
    sp: Optional[StartingPrices] = None  # The BSP related prices for this runner
    ex: Optional[ExchangePrices] = None  # The Exchange prices available for this runner
    orders: Optional[list[Order]] = None  # List of orders in the market
    matches: Optional[list[Match]] = None  # List of matches (i.e., orders that have been fully or partially executed)
    matchesByStrategy: Optional[dict[str, Match]] = None  # List of matches for each strategy, ordered by matched data


class MarketCatalogue(BaseMessage, frozen=True):
    marketId: MarketId  # The unique identifier for the market
    marketName: str  # The name of the market
    marketStartTime: Optional[Date] = None  # Only returned when the MARKET_START_TIME enum is requested
    description: Optional[MarketDescription] = None  # Details about the market
    totalMatched: Optional[float] = None  # The total amount of money matched on the market
    runners: Optional[list[RunnerCatalog]] = None  # The runners (selections) contained in the market
    eventType: Optional[EventType] = None  # The Event Type the market is contained within
    competition: Optional[Competition] = None  # The competition the market is contained within
    event: Optional[Event] = None  # The event the market is contained within


class KeyLineSelection(BaseMessage, frozen=True):
    """Description of a market's key line selection"""

    selectionId: SelectionId  # Selection ID of the runner in the key line handicap
    handicap: Handicap  # Handicap value of the key line


class KeyLineDescription(BaseMessage, frozen=True):
    """A list of KeyLineSelection objects describing the key line for the market"""

    keyLine: list[KeyLineSelection]  # A list of KeyLineSelection objects


class MarketBook(BaseMessage, frozen=True):
    """The dynamic data in a market"""

    marketId: MarketId  # The unique identifier for the market
    isMarketDataDelayed: bool  # True if the data returned by listMarketBook will be delayed
    status: Optional[MarketStatus] = None  # The status of the market
    betDelay: Optional[int] = None  # The number of seconds an order is held until it is submitted into the market
    bspReconciled: Optional[bool] = None  # True if the market starting price has been reconciled
    complete: Optional[bool] = None  # If false, runners may be added to the market
    inplay: Optional[bool] = None  # True if the market is currently in play
    numberOfWinners: Optional[int] = None  # The number of selections that could be settled as winners
    numberOfRunners: Optional[int] = None  # The number of runners in the market
    numberOfActiveRunners: Optional[int] = None  # The number of runners that are currently active
    lastMatchTime: Optional[Date] = None  # The most recent time an order was executed
    totalMatched: Optional[float] = None  # The total amount matched on the market
    totalAvailable: Optional[float] = None  # The total amount of orders that remain unmatched
    crossMatching: Optional[bool] = None  # True if cross matching is enabled for this market
    runnersVoidable: Optional[bool] = None  # True if runners in the market can be voided
    version: Optional[int] = None  # The version of the market
    runners: Optional[list[Runner]] = None  # Information about the runners (selections) in the market
    keyLineDescription: Optional[KeyLineDescription] = None  # Description of a market's key line


class ItemDescription(BaseMessage, frozen=True):
    """
    This object contains some text which may be useful to render a betting history view.
    It offers no long-term warranty as to the correctness of the text.
    """

    eventTypeDesc: Optional[str] = None  # The event type name translated into the requested locale
    eventDesc: Optional[str] = None  # The event name or openDate + venue translated into the requested locale
    marketDesc: Optional[str] = None  # The market name or racing market type translated into the requested locale
    marketType: Optional[str] = None  # The market type e.g. MATCH_ODDS, PLACE, WIN etc.
    marketStartTime: Optional[Date] = None  # The start time of the market in ISO-8601 format, not translated
    runnerDesc: Optional[str] = None  # The runner name translated into the requested locale
    numberOfWinners: Optional[int] = None  # The number of winners on a market
    eachWayDivisor: Optional[float] = None  # The divisor for the EACH_WAY market type


class ClearedOrderSummary(BaseMessage, frozen=True):
    """Summary of a cleared order"""

    eventTypeId: Optional[EventTypeId] = None  # The id of the event type bet on
    eventId: Optional[EventId] = None  # The id of the event bet on
    marketId: Optional[MarketId] = None  # The id of the market bet on
    selectionId: Optional[int] = None  # The id of the selection bet on
    handicap: Optional[float] = None  # The handicap value for Asian handicap markets
    betId: Optional[BetId] = None  # The id of the bet
    placedDate: Optional[Date] = None  # The date the bet order was placed by the customer
    persistenceType: Optional[PersistenceType] = None  # The turn in play persistence state of the order
    orderType: Optional[OrderType] = None
    side: Optional[Side] = None  # Whether the bet was a back or lay bet
    itemDescription: Optional[ItemDescription] = None  # Container for ancillary data and localized text
    betOutcome: Optional[str] = None  # The settlement outcome of the bet
    priceRequested: Optional[Price] = None  # The average requested price across all settled bet orders under this item
    settledDate: Optional[Date] = None  # The date and time the bet order was settled by Betfair
    lastMatchedDate: Optional[Date] = None  # The date and time the last bet order was matched by Betfair
    betCount: Optional[int] = None  # The number of actual bets within this grouping

    # The cumulative amount of commission paid by the customer across all bets under this item
    commission: Optional[Size] = None
    priceMatched: Optional[Price] = None  # The average matched price across all settled bets or bet fragments
    priceReduced: Optional[bool] = None  # Indicates if the matched price was affected by a reduction factor
    sizeSettled: Optional[Size] = None  # The cumulative bet size that was settled as matched or voided under this item
    profit: Optional[Size] = None  # The profit or loss gained on this line
    sizeCancelled: Optional[Size] = None  # The amount of the bet that was cancelled
    customerOrderRef: Optional[CustomerOrderRef] = None  # The order reference defined by the customer for the bet order
    customerStrategyRef: Optional[
        CustomerStrategyRef
    ] = None  # The strategy reference defined by the customer for the bet order


class ClearedOrderSummaryReport(BaseMessage, frozen=True):
    """A container representing search results"""

    clearedOrders: list[ClearedOrderSummary]  # The list of cleared orders returned by the query
    moreAvailable: bool  # Indicates whether there are further result items beyond this page


class RunnerId(BaseMessage, frozen=True):
    """Unique identifier for a runner"""

    marketId: MarketId  # The id of the market bet on
    selectionId: int  # The id of the selection bet on
    handicap: Optional[float] = None  # The handicap associated with the runner in case of Asian handicap markets


class CurrentItemDescription(BaseMessage, frozen=True):
    """This object contains ancillary information about the item"""

    marketVersion: MarketVersion  # The relevant version of the market for this item


class CurrentOrderSummary(BaseMessage, frozen=True):
    """Summary of a current order"""

    betId: BetId  # The bet ID of the original place order
    marketId: MarketId  # The market ID the order is for
    selectionId: int  # The selection ID the order is for
    handicap: float  # The handicap associated with the runner in case of Asian handicap markets
    priceSize: PriceSize  # The price and size of the bet
    bspLiability: Size  # The liability of a given BSP bet
    side: Side  # BACK/LAY
    status: OrderStatus  # The status of the order
    persistenceType: PersistenceType  # What to do with the order at turn-in-play
    orderType: OrderType  # BSP Order type
    placedDate: Date  # The date the bet was placed
    matchedDate: Date  # The date of the last matched bet fragment
    averagePriceMatched: Optional[Price] = None  # The average price matched at
    sizeMatched: Optional[Size] = None
    sizeRemaining: Optional[Size] = None
    sizeLapsed: Optional[Size] = None
    sizeCancelled: Optional[Size] = None
    sizeVoided: Optional[Size] = None
    regulatorAuthCode: Optional[str] = None
    regulatorCode: Optional[str] = None
    customerOrderRef: Optional[str] = None  # The order reference defined by the customer for this bet
    customerStrategyRef: Optional[str] = None  # The strategy reference defined by the customer for this bet
    currentItemDescription: Optional[CurrentItemDescription] = None  # Container for ancillary data for this item


class CurrentOrderSummaryReport(BaseMessage, frozen=True):
    """A container representing search results"""

    currentOrders: list[CurrentOrderSummary]  # The list of current orders returned by the query
    moreAvailable: bool  # Indicates whether there are further result items beyond this page


class LimitOrder(BaseMessage, frozen=True):
    """Place a new LIMIT order (simple exchange bet for immediate execution)"""

    size: Size
    price: Price
    persistenceType: PersistenceType
    timeInForce: Optional[TimeInForce] = None
    minFillSize: Optional[Size] = None
    betTargetType: Optional[BetTargetType] = None
    betTargetSize: Optional[Size] = None


class LimitOnCloseOrder(BaseMessage, frozen=True):
    liability: Size
    price: Price


class MarketOnCloseOrder(BaseMessage, frozen=True):
    liability: Size


class PlaceInstruction(BaseMessage, kw_only=True, frozen=True):
    """Instruction to place a new order"""

    orderType: OrderType  # The order type
    selectionId: SelectionId  # The selection ID
    handicap: Optional[Handicap] = None  # The handicap associated with the runner in case of Asian handicap markets
    side: Side  # Back or Lay
    limitOrder: Optional[LimitOrder] = None  # A simple exchange bet for immediate execution

    # Bets matched if the returned starting price is better than a specified price
    limitOnCloseOrder: Optional[LimitOnCloseOrder] = None

    # Bets matched and settled at a price representative of the market at the point it turns in-play
    marketOnCloseOrder: Optional[MarketOnCloseOrder] = None
    customerOrderRef: Optional[str] = None  # An optional reference to identify instructions


class PlaceInstructionReport(BaseMessage, kw_only=True, frozen=True):
    """Report for a place instruction"""

    status: InstructionReportStatus  # The instruction report status
    errorCode: Optional[InstructionReportErrorCode] = None
    orderStatus: Optional[OrderStatus] = None
    instruction: PlaceInstruction  # The place instruction
    betId: Optional[BetId] = None  # The bet ID of the placed order, if successful
    placedDate: Optional[Date] = None  # The date and time the bet was placed, if successful
    averagePriceMatched: Optional[Price] = None  # The average price matched at, if successful
    sizeMatched: Optional[Size] = None  # The current amount of the bet that was matched, if successful


class PlaceExecutionReport(BaseMessage, kw_only=True, frozen=True):
    customerRef: Optional[CustomerRef] = None  # Echo of the customer reference if passed
    status: ExecutionReportStatus  # The execution report status
    errorCode: Optional[ExecutionReportErrorCode] = None  # The execution report error code
    marketId: Optional[MarketId] = None  # Echo of the market ID passed
    instructionReports: Optional[list[PlaceInstructionReport]] = None  # The list of place instruction reports


class CancelInstruction(BaseMessage, frozen=True):
    """Instruction to fully or partially cancel an order (only applies to LIMIT orders)"""

    betId: BetId
    # If supplied then this is a partial cancel. Should be set to 'null' if no size
    # reduction is required.
    sizeReduction: Optional[Size] = None


class ReplaceInstruction(BaseMessage, frozen=True):
    """Instruction to replace a LIMIT or LIMIT_ON_CLOSE order at a new price."""

    betId: BetId  # Unique identifier for the bet
    newPrice: Price  # The price to replace the bet at


class CancelInstructionReport(BaseMessage, kw_only=True, frozen=True):
    status: InstructionReportStatus  # Whether the command succeeded or failed
    errorCode: Optional[InstructionReportErrorCode] = None  # Cause of failure, or null if command succeeds
    instruction: Optional[CancelInstruction] = None  # The instruction that was requested
    sizeCancelled: Optional[float] = None  # The API states, that this is mandatory, but it's skipped in case of error
    cancelledDate: Optional[Date] = None


class CancelExecutionReport(BaseMessage, kw_only=True, frozen=True):
    customerRef: Optional[CustomerRef] = None  # Echo of the customerRef if passed
    status: ExecutionReportStatus
    errorCode: Optional[ExecutionReportErrorCode] = None
    marketId: Optional[MarketId] = None  # Echo of marketId passed
    instructionReports: Optional[list[CancelInstructionReport]] = None


class ReplaceInstructionReport(BaseMessage, frozen=True):
    status: InstructionReportStatus  # Whether the command succeeded or failed
    errorCode: Optional[InstructionReportErrorCode] = None  # Cause of failure, or null if command succeeds
    cancelInstructionReport: Optional[CancelInstructionReport] = None  # Cancellation report for the original order
    placeInstructionReport: Optional[PlaceInstructionReport] = None  # Placement report for the new order


class ReplaceExecutionReport(BaseMessage, kw_only=True, frozen=True):
    customerRef: Optional[CustomerRef] = None  # Echo of the customerRef if passed.
    status: ExecutionReportStatus
    errorCode: Optional[ExecutionReportErrorCode] = None
    marketId: Optional[MarketId] = None  # Echo of marketId passed
    instructionReports: Optional[list[ReplaceInstructionReport]] = None


class UpdateInstruction(BaseMessage, frozen=True):
    """Instruction to update LIMIT bet's persistence of an order that do not affect exposure"""

    betId: BetId  # Unique identifier for the bet
    newPersistenceType: PersistenceType  # The new persistence type to update this bet to


class UpdateInstructionReport(BaseMessage, kw_only=True, frozen=True):
    status: InstructionReportStatus  # Whether the command succeeded or failed
    errorCode: Optional[InstructionReportErrorCode] = None  # Cause of failure, or null if command succeeds
    instruction: UpdateInstruction  # The instruction that was requested


class UpdateExecutionReport(BaseMessage, frozen=True):
    customerRef: Optional[CustomerRef]  # Echo of the customerRef if passed.
    status: ExecutionReportStatus
    errorCode: Optional[ExecutionReportErrorCode]
    marketId: Optional[MarketId]  # Echo of marketId passed
    instructionReports: Optional[list[UpdateInstructionReport]]


class ExBestOffersOverrides(BaseMessage, frozen=True):
    """Options to alter the default representation of best offer prices"""

    bestPricesDepth: Optional[int] = None  # The maximum number of prices to return on each side for each runner
    rollupModel: Optional[RollupModel] = None  # The model to use when rolling up available sizes
    rollupLimit: Optional[int] = None  # The volume limit to use when rolling up returned sizes
    rollupLiabilityThreshold: Optional[float] = None  # Only applicable when rollupModel is MANAGED_LIABILITY
    rollupLiabilityFactor: Optional[int] = None  # Only applicable when rollupModel is MANAGED_LIABILITY


class PriceProjection(BaseMessage, frozen=True):
    """Selection criteria of the returning price data"""

    priceData: Optional[set[PriceData]] = None  # The basic price data you want to receive in the response

    # Options to alter the default representation of best offer prices
    exBestOffersOverrides: Optional[ExBestOffersOverrides] = None
    virtualise: Optional[bool] = None  # Indicates if the returned prices should include virtual prices

    # Indicates if the volume returned at each price point should be the absolute value or a
    # cumulative sum of volumes available at the price and all better prices. If unspecified
    # defaults to false. Applicable to EX_BEST_OFFERS and EX_ALL_OFFERS price projections.
    # Not supported as yet.
    rolloverStakes: Optional[bool] = None


class RunnerProfitAndLoss(BaseMessage, frozen=True):
    """Profit and loss if selection wins or loses"""

    selectionId: Optional[SelectionId] = None  # The unique identifier for the selection
    ifWin: Optional[float] = None  # Profit or loss for the market if this selection is the winner
    ifLose: Optional[float] = None  # Profit or loss for the market if this selection is the loser

    # Profit or loss for the market if this selection is placed (applies to marketType EACH_WAY only)
    ifPlace: Optional[float] = None


class MarketProfitAndLoss(BaseMessage, frozen=True):
    """Profit and loss in a market"""

    marketId: Optional[MarketId] = None  # The unique identifier for the market
    commissionApplied: Optional[float] = None  # The commission rate applied to P&L values
    profitAndLosses: Optional[list[RunnerProfitAndLoss]] = None  # Calculated profit and loss data
