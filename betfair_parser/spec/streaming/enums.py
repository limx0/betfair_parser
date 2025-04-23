from betfair_parser.strenums import DocumentedEnum, StrEnum, auto, doc


class ChangeType(StrEnum):
    HEARTBEAT = auto()
    SUB_IMAGE = auto()
    RESUB_DELTA = auto()


class SegmentType(StrEnum):
    SEG_START = auto()
    SEG = auto()
    SEG_END = auto()


class StatusErrorCode(DocumentedEnum):
    # General errors not sent with id linking to specific request (as no request context)
    INVALID_INPUT = doc("Failure code returned when an invalid input is provided (could not deserialize the message)")
    TIMEOUT = doc("Failure code when a client times out (i.e. too slow sending data)")

    # Specific to authentication
    NO_APP_KEY = doc("Failure code returned when an application key is not found in the message")
    INVALID_APP_KEY = doc("Failure code returned when an invalid application key is received")
    NO_SESSION = doc("Failure code returned when a session token is not found in the message")
    INVALID_SESSION_INFORMATION = doc("Failure code returned when an invalid session token is received")
    NOT_AUTHORIZED = doc("Failure code returned when client is not authorized to perform the operation")
    MAX_CONNECTION_LIMIT_EXCEEDED = doc(
        "Failure code returned when a client tries to create more connections than allowed to"
    )
    TOO_MANY_REQUESTS = doc("Failure code returned when a client makes too many requests within a short time period")

    # Specific to subscription requests
    SUBSCRIPTION_LIMIT_EXCEEDED = doc(
        "Customer tried to subscribe to more markets than allowed to - set to 200 markets by default"
    )
    INVALID_CLOCK = doc(
        "Failure code returned when an invalid clock is provided on re-subscription (check initialClk / clk supplied)"
    )

    # General errors which may or may not be linked to specific request id
    UNEXPECTED_ERROR = doc("Failure code returned when an internal error occurred on the server")
    CONNECTION_FAILED = doc("Failure code used when the client / server connection is terminated")
    INVALID_REQUEST = doc("Invalid Request")


class LapseStatusReasonCode(DocumentedEnum):
    """The reason that some portion or all of this order has been lapsed. Unset if no portion of the order is lapsed."""

    MKT_UNKNOWN = doc(
        "The market was unknown, presumably removed from the matcher (closed) between bet placement and matching."
    )
    MKT_INVALID = doc("The market was known about but in an invalid state.")
    RNR_UNKNOWN = doc("The runner was unknown, presumably removed between bet placement and matching.")
    TIME_ELAPSED = doc("The bet was waiting in the queue too long, so was lapsed for safety.")
    CURRENCY_UNKNOWN = doc("The bet's currency ID was not recognised by the matcher.")
    PRICE_INVALID = doc("The bet's price was invalid, e.g. outside the defined ladder for the market.")
    MKT_SUSPENDED = doc("The market was suspended at the time the bet came to be matched.")
    MKT_VERSION = doc(
        "The bet had a maximum market version set, and the market's version on matching was greater than this."
    )
    LINE_TARGET = doc("The bet was on a line market, but was requested targeting profit or payout.")
    LINE_SP = doc("The bet was on a line market, but was either a BSP bet directly or requested to PERSIST_TO_SP.")
    SP_IN_PLAY = doc("The bet was a BSP bet that had somehow come to be placed after turn-in-play.")
    SMALL_STAKE = doc("The bet's stake was worth less than half a penny in GBP.")
    PRICE_IMP_TOO_LARGE = doc(
        "When the bet came to be matched, the price available was better than its best-permitted price, "
        "suggesting a significant shift in the market, presumably due to a major incident, which may have "
        "rendered the bet unwanted."
    )


class MarketDataFilterFields(DocumentedEnum):
    EX_BEST_OFFERS_DISP = doc(
        "Best prices including Virtual Bets - depth is controlled by ladderLevels (1 to 10) - Please note: "
        "The virtual price stream is updated ~150 m/s after non-virtual prices. Virtual prices are calculated "
        "for all ladder levels."
    )
    EX_BEST_OFFERS = doc("Best prices not including Virtual Bets - depth is controlled by ladderLevels (1 to 10).")
    EX_ALL_OFFERS = doc("Full available to BACK/LAY ladder.")
    EX_TRADED = doc("Full traded ladder. This is the amount traded at any price on any selection in the market")
    EX_TRADED_VOL = doc("Market and runner level traded volume.")
    EX_LTP = doc("The 'Last Price Matched' on a selection.")
    EX_MARKET_DEF = doc("Send market definitions. To receive updates to any of the following fields")
    SP_TRADED = doc("Starting price ladder.")
    SP_PROJECTED = doc("Starting price projection prices. To receive any update to the Betfair SP Near and Far price.")
