from betfair_parser.strenums import DocumentedEnum, StrEnum, auto, doc


class MarketProjection(DocumentedEnum):
    COMPETITION = doc("If not selected then the competition will not be returned with marketCatalogue")
    EVENT = doc("If not selected then the event will not be returned with marketCatalogue")
    EVENT_TYPE = doc("If not selected then the eventType will not be returned with marketCatalogue")
    MARKET_START_TIME = doc("If not selected then the start time will not be returned with marketCatalogue")
    MARKET_DESCRIPTION = doc("If not selected then the description will not be returned with marketCatalogue")
    RUNNER_DESCRIPTION = doc("If not selected then the runners will not be returned with marketCatalogue")
    RUNNER_METADATA = doc(
        "If not selected then the runner metadata will not be returned with marketCatalogue. If selected "
        "then RUNNER_DESCRIPTION will also be returned regardless of whether it is included as a market "
        "projection."
    )


class PriceData(DocumentedEnum):
    SP_AVAILABLE = doc("Amount available for the BSP auction.")
    SP_TRADED = doc("Amount traded in the BSP auction.")
    EX_BEST_OFFERS = doc("Only the best prices available for each runner, to requested price depth.")
    EX_ALL_OFFERS = doc("EX_ALL_OFFERS trumps EX_BEST_OFFERS if both settings are present")
    EX_TRADED = doc("Amount traded on the exchange.")


class MatchProjection(DocumentedEnum):
    NO_ROLLUP = doc("No rollup, return raw fragments")
    ROLLED_UP_BY_PRICE = doc("Rollup matched amounts by distinct matched prices per side.")
    ROLLED_UP_BY_AVG_PRICE = doc("Rollup matched amounts by average matched price per side")


class OrderProjection(DocumentedEnum):
    ALL = doc("EXECUTABLE and EXECUTION_COMPLETE orders")
    EXECUTABLE = doc(
        "An order that has a remaining unmatched portion. This is either a fully unmatched "
        "or partially matched bet (order)"
    )
    EXECUTION_COMPLETE = doc(
        "An order that does not have any remaining unmatched portion. This is a fully matched bet (order)."
    )


class MarketStatus(DocumentedEnum):
    INACTIVE = doc("The market has been created but isn't yet available.")
    OPEN = doc("The market is open for betting.")
    SUSPENDED = doc("The market is suspended and not available for betting.")
    CLOSED = doc("The market has been settled and is no longer available for betting.")


class RunnerStatus(DocumentedEnum):
    ACTIVE = auto()
    WINNER = auto()
    LOSER = auto()
    PLACED = doc("The runner was placed, applies to EACH_WAY marketTypes only.")
    REMOVED_VACANT = doc(
        "REMOVED_VACANT applies to Greyhounds. Greyhound markets always return a fixed number of "
        "runners (traps). If a dog has been removed, the trap is shown as vacant."
    )
    REMOVED = auto()
    HIDDEN = doc(
        "The selection is hidden from the market. This occurs in Horse Racing markets were runners "
        "is hidden when it is doesn't hold an official entry following an entry stage. This could be "
        "because the horse was never entered or because they have been scratched from a race at a "
        "declaration stage. All matched customer bet prices are set to 1.0 even if there are later "
        "supplementary stages. Should it appear likely that a specific runner may actually be supplemented "
        "into the race this runner will be reinstated with all matched customer bets set back to "
        "the original prices."
    )


class TimeGranularity(StrEnum):
    DAYS = auto()
    HOURS = auto()
    MINUTES = auto()


class Side(DocumentedEnum):
    BACK = doc(
        "To back a team, horse or outcome is to bet on the selection to win. For LINE markets a Back bet "
        "refers to a SELL line. A SELL line will win if the outcome is LESS THAN the taken line (price)."
    )
    LAY = doc(
        "To lay a team, horse, or outcome is to bet on the selection to lose. For LINE markets a Lay bet "
        "refers to a BUY line. A BUY line will win if the outcome is MORE THAN the taken line (price)."
    )


class OrderBy(DocumentedEnum):
    BY_BET = doc("@Deprecated Use BY_PLACE_TIME instead. Order by placed time, then bet id.")
    BY_MARKET = doc("Order by market id, then placed time, then bet id.")
    BY_MATCH_TIME = doc(
        "Order by time of last matched fragment (if any), then placed time, then bet id. Filters "
        "out orders which have no matched date. The dateRange filter (if specified) is applied to "
        "the matched date."
    )
    BY_PLACE_TIME = doc(
        "Order by placed time, then bet id. This is an alias of to be deprecated BY_BET. The "
        "dateRange filter (if specified) is applied to the placed date."
    )
    BY_SETTLED_TIME = doc(
        "Order by time of last settled fragment (if any due to partial market settlement), then by "
        "last match time, then placed time, then bet id. Filters out orders which have not been settled. "
        "The dateRange filter (if specified) is applied to the settled date."
    )
    BY_VOID_TIME = doc(
        "Order by time of last voided fragment (if any), then by last match time, then placed time, then "
        "bet id. Filters out orders which have not been voided. The dateRange filter (if specified) is "
        "applied to the voided date."
    )


class SortDir(DocumentedEnum):
    EARLIEST_TO_LATEST = doc("Order from earliest value to latest e.g. lowest betId is first in the results.")
    LATEST_TO_EARLIEST = doc("Order from the latest value to the earliest e.g. highest betId is first in the results.")


class MarketSort(DocumentedEnum):
    MINIMUM_TRADED = doc("Minimum traded volume")
    MAXIMUM_TRADED = doc("Maximum traded volume")
    MINIMUM_AVAILABLE = doc("Minimum available to match")
    MAXIMUM_AVAILABLE = doc("Maximum available to match")
    FIRST_TO_START = doc("The closest markets based on their expected start time")
    LAST_TO_START = doc("The most distant markets based on their expected start time")


class MarketBettingType(DocumentedEnum):
    ODDS = doc("Odds Market - Any market that doesn't fit any any of the below categories.")
    LINE = doc(
        "Line Market - LINE markets operate at even-money odds of 2.0. However, price for these markets "
        "refers to the line positions available as defined by the markets min-max range and interval steps. "
        "Customers either Buy a line (LAY bet, winning if outcome is greater than the taken line (price)) or "
        "Sell a line (BACK bet, winning if outcome is less than the taken line (price)). If settled outcome "
        "equals the taken line, stake is returned."
    )
    RANGE = doc("Range Market - Now Deprecated")
    ASIAN_HANDICAP_DOUBLE_LINE = doc(
        "Asian Handicap Market - A traditional Asian handicap market. Can be identified by marketType ASIAN_HANDICAP"
    )
    ASIAN_HANDICAP_SINGLE_LINE = doc(
        "Asian Single Line Market - A market in which there can be 0 or multiple winners. e.g. marketType TOTAL_GOALS"
    )
    FIXED_ODDS = doc(
        "Sportsbook Odds Market. This type is deprecated and will be removed in future releases, when "
        "Sportsbook markets will be represented as ODDS market but with a different product type."
    )


class ExecutionReportStatus(DocumentedEnum):
    SUCCESS = doc("Order processed successfully")
    FAILURE = doc("Order failed.")
    PROCESSED_WITH_ERRORS = doc(
        "The order itself has been accepted, but at least one (possibly all) actions have generated errors. "
        "This error only occurs for replaceOrders, cancelOrders and updateOrders operations. In normal "
        "circumstances the placeOrders operation will not return PROCESSED_WITH_ERRORS status as it is an "
        "atomic operation.  PLEASE NOTE: if the 'Best Execution' features is switched off, placeOrders can "
        "return ‘PROCESSED_WITH_ERRORS’ meaning that some bets can be rejected and other placed when "
        "submitted in the same PlaceInstruction"
    )
    TIMEOUT = doc(
        "The order timed out & the status of the bet is unknown. If a TIMEOUT error occurs on a "
        "placeOrders/replaceOrders request, you should check listCurrentOrders to verify the status of your "
        "bets before placing further orders. Please Note: Timeouts will occur after 5 seconds of attempting "
        "to process the bet but please allow up to 15 seconds for a timed out order to appear. After this "
        "time any unprocessed bets will automatically be Lapsed and no longer be available on the Exchange."
    )


class ExecutionReportErrorCode(DocumentedEnum):
    ERROR_IN_MATCHER = doc(
        "The matcher is not healthy. Please note: The error will also be returned if you attempt concurrent "
        "'cancel all' bets requests using cancelOrders which isn't permitted."
    )
    PROCESSED_WITH_ERRORS = doc(
        "The order itself has been accepted, but at least one (possibly all) actions have generated errors."
    )
    BET_ACTION_ERROR = doc(
        "There is an error with an action that has caused the entire order to be rejected. Check the "
        "instructionReports errorCode for the reason for the rejection of the order."
    )
    INVALID_ACCOUNT_STATE = doc("Order rejected due to the account's status (suspended, inactive, dup cards)")
    INVALID_WALLET_STATUS = doc("Order rejected due to the account's wallet's status")
    INSUFFICIENT_FUNDS = doc("Account has exceeded its exposure limit or available to bet limit")
    LOSS_LIMIT_EXCEEDED = doc("The account has exceed the self imposed loss limit")
    MARKET_SUSPENDED = doc("Market is suspended")
    MARKET_NOT_OPEN_FOR_BETTING = doc(
        "Market is not open for betting. It is either not yet active, suspended or closed awaiting settlement."
    )
    DUPLICATE_TRANSACTION = doc(
        "Duplicate customer reference data submitted - Please note: There is a time window associated with "
        "the de-duplication of duplicate submissions which is 60 second"
    )
    INVALID_ORDER = doc(
        "Order cannot be accepted by the matcher due to the combination of actions. For example, bets being "
        "edited are not on the same market, or order includes both edits and placement"
    )
    INVALID_MARKET_ID = doc("Market doesn't exist")
    PERMISSION_DENIED = doc(
        "Business rules do not allow order to be placed. You are either attempting to place the order using "
        "a Delayed Application Key or from a restricted jurisdiction (i.e. USA)"
    )
    DUPLICATE_BETIDS = doc(
        "Duplicate bet ids found. For example, you've included the same betId more than once in a single "
        "cancelOrders request."
    )
    NO_ACTION_REQUIRED = doc("Order hasn't been passed to matcher as system detected there will be no state change")
    SERVICE_UNAVAILABLE = doc("The requested service is unavailable")
    REJECTED_BY_REGULATOR = doc(
        "The regulator rejected the order. On the Italian Exchange this error will occur if more than 50 "
        "bets are sent in a single placeOrders request."
    )
    NO_CHASING = doc(
        "A specific error code that relates to Spanish Exchange markets only which indicates that the bet "
        "placed contravenes the Spanish regulatory rules relating to loss chasing."
    )
    REGULATOR_IS_NOT_AVAILABLE = doc("The underlying regulator service is not available.")
    TOO_MANY_INSTRUCTIONS = doc("The amount of orders exceeded the maximum amount allowed to be executed")
    INVALID_MARKET_VERSION = doc("The supplied market version is invalid. Max length allowed for market version is 12.")
    INVALID_PROFIT_RATIO = doc("The order falls outside the permitted price and size combination.")
    EVENT_EXPOSURE_LIMIT_EXCEEDED = doc("@Deprecated Defined in XML specification but not in API doc")
    EVENT_MATCHED_EXPOSURE_LIMIT_EXCEEDED = doc("@Deprecated Defined in XML specification but not in API doc")
    EVENT_BLOCKED = doc("@Deprecated Defined in XML specification but not in API doc")


class PersistenceType(DocumentedEnum):
    LAPSE = doc("Lapse (cancel) the order automatically when the market is turned in play if the bet is unmatched")
    PERSIST = doc(
        "Persist the unmatched order to in-play. The bet will be placed automatically into the in-play "
        "market at the start of the event. Once in play, the bet won't be cancelled by Betfair if a "
        "material event takes place and will be available until matched or cancelled by the user."
    )
    MARKET_ON_CLOSE = doc("Put the order into the auction (SP) at turn-in-play")


class InstructionReportStatus(DocumentedEnum):
    SUCCESS = doc("The instruction was successful.")
    FAILURE = doc("The instruction failed.")
    TIMEOUT = doc(
        "The order timed out & the status of the bet is unknown. If a TIMEOUT error occurs on a "
        "placeOrders/replaceOrders request, you should check listCurrentOrders to verify the status "
        "of your bets before placing further orders. Please Note: Timeouts will occur after 5 seconds "
        "of attempting to process the bet but please allow up to 15 seconds for a timed out order to "
        "appear. After this time any unprocessed bets will automatically be Lapsed and no longer be "
        "available on the Exchange."
    )


class InstructionReportErrorCode(DocumentedEnum):
    INVALID_BET_SIZE = doc("bet size is invalid for your currency or your regulator")
    INVALID_RUNNER = doc("Runner does not exist, includes vacant traps in greyhound racing")
    BET_TAKEN_OR_LAPSED = doc(
        "Bet cannot be cancelled or modified as it has already been taken or has been cancelled/lapsed "
        "Includes attempts to cancel/modify market on close BSP bets and cancelling limit on close BSP bets. "
        "The error may be returned on placeOrders request if for example a bet is placed at the point when "
        "a market admin event takes place (i.e. market is turned in-play). The error will also be returned "
        "if a market version is submitted and a material change has taken place since the bet was submitted "
        "causing the bet to be rejected."
    )
    BET_IN_PROGRESS = doc("No result was received from the matcher in a timeout configured for the system")
    RUNNER_REMOVED = doc("Runner has been removed from the event")
    MARKET_NOT_OPEN_FOR_BETTING = doc("Attempt to edit a bet on a market that has closed.")
    LOSS_LIMIT_EXCEEDED = doc("The action has caused the account to exceed the self imposed loss limit")
    MARKET_NOT_OPEN_FOR_BSP_BETTING = doc("Market now closed to bsp betting. Turned in-play or has been reconciled")
    INVALID_PRICE_EDIT = doc(
        "Attempt to edit down the price of a bsp limit on close lay bet, or edit up the price of a limit on "
        "close back bet"
    )
    INVALID_ODDS = doc("Odds not on price ladder - either edit or placement")
    INSUFFICIENT_FUNDS = doc(
        "Insufficient funds available to cover the bet action. Either the exposure limit or available to bet "
        "limit would be exceeded."
    )
    INVALID_PERSISTENCE_TYPE = doc("Invalid persistence type for this market, e.g. KEEP for a non in-play market.")
    ERROR_IN_MATCHER = doc("A problem with the matcher prevented this action completing successfully")
    INVALID_BACK_LAY_COMBINATION = doc(
        "The order contains a back and a lay for the same runner at overlapping prices. This would guarantee "
        "a self match. This also applies to BSP limit on close bets."
    )
    ERROR_IN_ORDER = doc("The action failed because the parent order failed")
    INVALID_BID_TYPE = doc("Bid type is mandatory")
    INVALID_BET_ID = doc("Bet for id supplied has not been found")
    CANCELLED_NOT_PLACED = doc("Bet cancelled but replacement bet was not placed")
    RELATED_ACTION_FAILED = doc("Action failed due to the failure of a action on which this action is dependent")
    NO_ACTION_REQUIRED = doc(
        "the action does not result in any state change. eg changing a persistence to it's current value"
    )
    TIME_IN_FORCE_CONFLICT = doc(
        "You may only specify a time in force on either the place request OR on individual limit order "
        "instructions (not both), since the implied behaviors are incompatible."
    )
    UNEXPECTED_PERSISTENCE_TYPE = doc(
        "You have specified a persistence type for a FILL_OR_KILL order, which is nonsensical because no "
        "umatched portion can remain after the order has been placed."
    )
    INVALID_ORDER_TYPE = doc(
        "You have specified a time in force of FILL_OR_KILL, but have included a non-LIMIT order type."
    )
    UNEXPECTED_MIN_FILL_SIZE = doc(
        "You have specified a minFillSize on a limit order, where the limit order's time in force is not "
        "FILL_OR_KILL. Using minFillSize is not supported where the time in force of the request (as "
        "opposed to an order) is FILL_OR_KILL."
    )
    INVALID_CUSTOMER_ORDER_REF = doc("The supplied customer order reference is too long.")
    INVALID_MIN_FILL_SIZE = doc(
        "The minFillSize must be greater than zero and less than or equal to the order's size. The "
        "minFillSize cannot be less than the minimum bet size for your currency."
    )
    BET_LAPSED_PRICE_IMPROVEMENT_TOO_LARGE = doc(
        "Your bet is lapsed. There is better odds than requested available in the market, but your "
        "preferences don't allow the system to match your bet against better odds. Change your betting "
        "preferences to accept better odds if you don't want to receive this error."
    )
    INVALID_CUSTOMER_STRATEGY_REF = doc("@Deprecated Defined in XML specification but not in API doc")
    INVALID_PROFIT_RATIO = doc("The order falls outside the permitted price and size combination.")


class RollupModel(DocumentedEnum):
    STAKE = doc("The volumes will be rolled up to the minimum value which is >= rollupLimit.")
    PAYOUT = doc(
        "The volumes will be rolled up to the minimum value where the payout( price * volume ) "
        "is >= rollupLimit. On a LINE market, volumes will be rolled up where payout( 2.0 * volume ) "
        "is >= rollupLimit"
    )
    MANAGED_LIABILITY = doc(
        "The volumes will be rolled up to the minimum value which is >= rollupLimit, until a lay price "
        "threshold. Thereafter, the volumes will be rolled up to the minimum value such that the liability "
        ">= a minimum liability. Not supported as yet."
    )
    NONE = doc(
        "No rollup will be applied. However, the volumes will be filtered by currency specific minimum "
        "stake unless overridden specifically for the channel."
    )


class GroupBy(DocumentedEnum):
    EVENT_TYPE = doc("A roll up of settled P&L, commission paid and number of bet orders, on a specified event type")
    EVENT = doc("A roll up of settled P&L, commission paid and number of bet orders, on a specified event")
    MARKET = doc("A roll up of settled P&L, commission paid and number of bet orders, on a specified market")
    SIDE = doc(
        "An averaged roll up of settled P&L, and number of bets, on the specified side of a specified "
        "selection within a specified market, that are either settled or voided"
    )
    BET = doc("The P&L, side and regulatory information etc, about each individual bet order.")
    RUNNER = doc("@Deprecated Defined in XML specification but not in API doc")
    STRATEGY = doc("@Deprecated Defined in XML specification but not in API doc")


class BetStatus(DocumentedEnum):
    SETTLED = doc("A matched bet that was settled normally")
    VOIDED = doc("A matched bet that was subsequently voided by Betfair, before, during or after settlement")
    LAPSED = doc("Unmatched bet that was cancelled by Betfair (for example at turn in play).")
    CANCELLED = doc("Unmatched bet that was cancelled by an explicit customer action.")


class TimeInForce(DocumentedEnum):
    FILL_OR_KILL = doc(
        "Execute the transaction immediately and completely (filled to size or between minFillSize and size) "
        "or not at all (cancelled). For LINE markets Volume Weighted Average Price (VWAP) functionality is "
        "disabled."
    )


class BetTargetType(DocumentedEnum):
    BACKERS_PROFIT = doc(
        "The payout requested minus the calculated size at which this LimitOrder is to be placed. "
        "BetTargetType bets are invalid for LINE markets"
    )
    PAYOUT = doc("The total payout requested on a LimitOrder")


class PriceLadderType(DocumentedEnum):
    CLASSIC = doc("Price ladder increments traditionally used for Odds Markets.")
    FINEST = doc("Price ladder with the finest available increment, traditionally used for Asian Handicap markets.")
    LINE_RANGE = doc("Price ladder used for LINE markets. Refer to MarketLineRangeInfo for more details.")


class BetDelayModel(DocumentedEnum):
    PASSIVE = doc(
        "For in-play markets where betDelay > 0, orders that are guaranteed not to match "
        "immediately are accepted straight away, bypassing the bet delay wait."
    )


class MarketTypeCode(StrEnum):
    """This is not a complete list, but only a selection of some popular options for direct access.

    A full list can be retrieved from the API using ListMarketTypes.
    """

    ALT_TOTAL_GOALS = auto()
    ANTEPOST_WIN = auto()
    ASIAN_HANDICAP = auto()
    BOTH_TEAMS_TO_SCORE = auto()
    COMBINED_TOTAL = auto()
    CORRECT_SCORE = auto()
    EACH_WAY = auto()
    EXACTA = auto()
    FORECAST = auto()
    HANDICAP = auto()
    MATCH_BET = auto()
    MATCH_ODDS = auto()
    NUMBER_OF_SETS = auto()
    OTHER_PLACE = auto()
    OUTRIGHT_WINNER = auto()
    OVER_UNDER_05 = auto()
    OVER_UNDER_25 = auto()
    PLACE = auto()
    PLAYER_A_WIN_A_SET = auto()
    PLAYER_B_WIN_A_SET = auto()
    QUARTER_WINNER = auto()
    QUINELLA = auto()
    RACE_WIN_DIST = auto()
    SEASON_SPECIALS = auto()
    SET_BETTING = auto()
    SET_CORRECT_SCORE = auto()
    SET_WINNER = auto()
    TOURNAMENT_WINNER = auto()
    TRAP_CHALLENGE = auto()
    UNUSED = auto()
    WIN = auto()
    WITHOUT_FAV = auto()
