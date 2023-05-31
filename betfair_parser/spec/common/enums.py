from betfair_parser.strenums import DocumentedEnum, LowerStrEnum, StrEnum, auto, doc


class EndpointType(LowerStrEnum):
    IDENTITY = auto()
    IDENTITY_CERT = auto()
    NAVIGATION = auto()
    HEARTBEAT = auto()
    ACCOUNTS = auto()
    BETTING = auto()
    SCORES = auto()
    NONE = auto()  # To avoid issues with mypy


EVENT_TYPE_TO_NAME = {
    "1": "Soccer",
    "2": "Tennis",
    "3": "Golf",
    "4": "Cricket",
    "5": "Rugby Union",
    "1477": "Rugby League",
    "6": "Boxing",
    "7": "Horse Racing",
    "8": "Motor Sport",
    "27454571": "Esports",
    "10": "Special Bets",
    "998917": "Volleyball",
    "11": "Cycling",
    "2152880": "Gaelic Games",
    "3988": "Athletics",
    "6422": "Snooker",
    "7511": "Baseball",
    "6231": "Financial Bets",
    "6423": "American Football",
    "7522": "Basketball",
    "7524": "Ice Hockey",
    "61420": "Australian Rules",
    "468328": "Handball",
    "3503": "Darts",
    "26420387": "Mixed Martial Arts",
    "4339": "Greyhound Racing",
    "2378961": "Politics",
}


class RegulatorCodes(DocumentedEnum):
    MR_ESP = doc("SPANISH GAMBLING AUTHORITY")
    MR_INT = doc("GIBRALTER REGULATOR")
    MR_ITA = doc("AMMINISTRAZIONE AUTONOMA DEI MONOPOLI DI STATO")
    MR_NJ = doc("NJRC - NEW JERSEY RACING COMMISSION")
    MR_TGC = doc("THE TASMANIAN GAMING COMMISSION")


class OrderType(DocumentedEnum):
    LIMIT = doc("A normal exchange limit order for immediate execution")
    LIMIT_ON_CLOSE = doc("Limit order for the auction (SP)")
    MARKET_ON_CLOSE = doc("Market order for the auction (SP)")


class OrderSide(StrEnum):
    BACK = auto()
    LAY = auto()


class OrderResponse(StrEnum):
    SUCCESS = auto()
    FAILURE = auto()


class OrderStatus(DocumentedEnum):
    PENDING = doc(
        "An asynchronous order is yet to be processed. Once the bet has been processed by the exchange "
        "(including waiting for any in-play delay), the result will be reported and available on the "
        "Exchange Stream API and API NG. Not a valid search criteria on MarketFilter."
    )
    EXECUTION_COMPLETE = doc("An order that does not have any remaining unmatched portion.")
    EXECUTABLE = doc("An order that has a remaining unmatched portion.")
    EXPIRED = doc(
        "The order is no longer available for execution due to its time in force constraint. "
        "In the case of FILL_OR_KILL orders, this means the order has been killed because it "
        "could not be filled to your specifications. Not a valid search criteria on MarketFilter."
    )


class JSONExceptionCode(DocumentedEnum):
    INVALID_JSON = doc(
        value=-32700,
        docstring=(
            "Invalid JSON was received by the server. An error occurred on the server while " "parsing the JSON text."
        ),
    )
    METHOD_NOT_FOUND = doc(value=-32601, docstring="Method not found")
    INVALID_PARAMETERS = doc(
        value=-32602, docstring="Problem parsing the parameters, or a mandatory parameter was not found"
    )
    JSON_RPC_ERROR = doc(value=-32603, docstring="Internal JSON-RPC error")


class APIExceptionCode(DocumentedEnum):
    TOO_MUCH_DATA = doc("The operation requested too much data")
    INVALID_INPUT_DATA = doc("Invalid input data")
    INVALID_SESSION_INFORMATION = doc("The session token passed is invalid or expired")
    NO_APP_KEY = doc("An application key is required for this operation")
    NO_SESSION = doc("A session token is required for this operation")
    UNEXPECTED_ERROR = doc("An unexpected internal error occurred that prevented successful request processing.")
    INVALID_APP_KEY = doc("The application key passed is invalid")
    TOO_MANY_REQUESTS = doc("There are too many pending requests")
    SERVICE_BUSY = doc("The service is currently too busy to service this request")
    TIMEOUT_ERROR = doc("Internal call to downstream service timed out")
    REQUEST_SIZE_EXCEEDS_LIMIT = doc(
        "The request exceeds the request size limit. Requests are limited to a total of 250"
        "betId's/marketId's (or a combination of both)"
    )
    ACCESS_DENIED = doc(
        "The calling client is not permitted to perform the specific action e.g. the using a Delayed "
        "App Key when placing bets or attempting to place a bet from a restricted jurisdiction."
    )
    SERVICE_UNAVAILABLE = doc("Service is currently unavailable")  # Used only in RaceStatus
