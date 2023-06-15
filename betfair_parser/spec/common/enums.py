from enum import Enum

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


class RegulatorCode(DocumentedEnum):
    MR_ESP = doc("SPANISH GAMBLING AUTHORITY")
    MR_INT = doc("GIBRALTER REGULATOR")
    MR_ITA = doc("AMMINISTRAZIONE AUTONOMA DEI MONOPOLI DI STATO")
    MR_NJ = doc("NJRC - NEW JERSEY RACING COMMISSION")
    MR_TGC = doc("THE TASMANIAN GAMING COMMISSION")


class OrderType(DocumentedEnum):
    LIMIT = doc("A normal exchange limit order for immediate execution")
    LIMIT_ON_CLOSE = doc("Limit order for the auction (SP)")
    MARKET_ON_CLOSE = doc("Market order for the auction (SP)")
    MARKET_AT_THE_CLOSE = doc("Undocumented, but found out there in the wild, likely a mistake by Betfair")


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
            "Invalid JSON was received by the server. An error occurred on the server while parsing the JSON text."
        ),
    )
    METHOD_NOT_FOUND = doc(value=-32601, docstring="Method not found")
    INVALID_PARAMETERS = doc(
        value=-32602, docstring="Problem parsing the parameters, or a mandatory parameter was not found"
    )
    JSON_RPC_ERROR = doc(value=-32603, docstring="Internal JSON-RPC error")


class APINGExceptionCode(DocumentedEnum):
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


# This needs to  be here and not in accounts, as we need it for the error struct definition
class AccountAPINGExceptionCode(DocumentedEnum):
    INVALID_INPUT_DATA = doc("Invalid input data. Please check the format of your request.")
    INVALID_SESSION_INFORMATION = doc(
        "The session token hasn't been provided, is invalid or has expired. You must login "
        "again to create a new session token."
    )
    UNEXPECTED_ERROR = doc("An unexpected internal error occurred that prevented successful request processing.")
    INVALID_APP_KEY = doc("The application key passed is invalid or is not present.")
    SERVICE_BUSY = doc("The service is currently too busy to service this request.")
    TIMEOUT_ERROR = doc("The internal call to downstream service timed out.")
    DUPLICATE_APP_NAME = doc("Duplicate application name.")
    APP_KEY_CREATION_FAILED = doc(
        "Creating application key version has failed. Please check that your application name is unique "
        "and doesn't contain your Betfair username."
    )
    APP_CREATION_FAILED = doc("Application creation has been failed.")
    NO_SESSION = doc(
        "A session token header ('X-Authentication') has not been provided in the request. Please note: "
        "The same error is returned by the Keep Alive operation if the X-Authentication header is provided "
        "but the session value is invalid or if the session has expired."
    )
    NO_APP_KEY = doc("An application key header ('X-Application') has not been provided in the request.")
    SUBSCRIPTION_EXPIRED = doc("An application key is required for this operation.")
    INVALID_SUBSCRIPTION_TOKEN = doc("The subscription token provided doesn't exist.")
    TOO_MANY_REQUESTS = doc("Too many requests. For more details relating to this error please see FAQ's.")
    INVALID_CLIENT_REF = doc("Invalid length for the client reference.")
    WALLET_TRANSFER_ERROR = doc("There was a problem transferring funds between your wallets.")
    INVALID_VENDOR_CLIENT_ID = doc("The vendor client ID is not subscribed to this Application Key.")
    USER_NOT_SUBSCRIBED = doc(
        "The user making the request is not subscribed to the Application Key they are trying to perform "
        "the action on (e.g. creating an Authorisation Code)."
    )
    INVALID_SECRET = doc("The vendor making the request has provided a vendor secret that does not match our records.")
    INVALID_AUTH_CODE = doc("The vendor making the request has not provided a valid authorization code.")
    INVALID_GRANT_TYPE = doc(
        "The vendor making the request has not provided a valid grant_type, or the grant_type they have "
        "passed does not match the parameters (authCode/refreshToken)."
    )
    CUSTOMER_ACCOUNT_CLOSED = doc("A token could not be created because the customer's account is CLOSED.")


class EventTypeIdCode(int, Enum):
    """Unique identifier for event types

    This is not a complete list and only serves for ease of use. For a full list, use the ListEventTypes API call.

    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Additional+Information?preview=/43090178/43090179/EventTypIds.xlsx
    """

    SOCCER = 1
    TENNIS = 2
    GOLF = 3
    CRICKET = 4
    RUGBY_UNION = 5
    BOXING = 6
    HORSE_RACING = 7
    MOTOR_SPORT = 8
    SPECIAL_BETS = 10
    CYCLING = 11
    ROWING = 12
    RUGBY_LEAGUE = 1477
    DARTS = 3503
    ATHLETICS = 3988
    GREYHOUND_RACING = 4339
    FINANCIAL_BETS = 6231
    SNOOKER = 6422
    AMERICAN_FOOTBALL = 6423
    BASEBALL = 7511
    BASKETBALL = 7522
    HOCKEY = 7523
    ICE_HOCKEY = 7524
    SUMO_WRESTLING = 7525
    AUSTRALIAN_RULES = 61420
    GAELIC_FOOTBALL = 66598
    HURLING = 66599
    POOL = 72382
    CHESS = 136332
    POKER_ROOM = 189929
    TROTTING = 256284
    COMMONWEALTH_GAMES = 300000
    POKER = 315220
    WINTER_SPORTS = 451485
    HANDBALL = 468328
    NETBALL = 606611
    SWIMMING = 620576
    BADMINTON = 627555
    INTERNATIONAL_RULES = 678378
    BRIDGE = 982477
    YACHTING = 998916
    VOLLEYBALL = 998917
    BOWLS = 998918
    BANDY = 998919
    FLOORBALL = 998920
    EXCHANGE_POKER = 1444073
    EXCHANGE_BLACKJACK = 1444076
    EXCHANGE_BACCARAT = 1444085
    EXCHANGE_HI_LO = 1444092
    EXCHANGE_OMAHA_HI = 1444099
    EXCHANGE_CARD_RACING = 1444115
    CASINO = 1444120
    EXCHANGE_ROULETTE = 1444130
    EXCHANGE_BULLSEYE_ROULETTE = 1444150
    BACKGAMMON = 1938544
    GAA_SPORTS = 2030972
    GAELIC_GAMES = 2152880
    INTERNAL_MARKETS = 2264869
    POLITICS = 2378961
    TABLE_TENNIS = 2593174
    YAHOO_RACING = 2791893
    BEACH_VOLLEYBALL = 2872194
    CANOEING = 2872196
    WATER_POLO = 2901849
    POLO = 2977000
    FISHING = 3088925
    ROLLER_HOCKEY = 3130721
    CROSS_SPORT_ACCUMULATORS = 3145419
    SQUASH = 4609466
    SURFING = 4726642
    COMBAT_SPORTS = 4968929
    EXCHANGE_GAMES = 5402258
    PELOTA = 5412697
    FEATURED_MARKETS = 5545197
    EXCHANGE_CASINO = 10271443
    TEN_PIN_BOWLING = 10390264
    TRADEFAIR = 15242720
    FUTSAL = 15826206
    FUSSBALL = 15826207
    HARNESS_RACING = 16872235
    EQUESTRIAN = 18643353
    HORSE_RACING_VIRTUAL = 26397698
    MIXED_MARTIAL_ARTS = 26420387
    TRIATHLON = 27065662
    CURRENT_AFFAIRS = 27388198
    VIRTUAL_SPORTS = 27438978
    E_SPORTS = 27454571
    WRESTLING = 27485048
    NEW_CUSTOMER_OFFER = 27596832
    UFC = 27610222
    GAA_FOOTBALL = 27610230
    GAA_HURLING = 27610231
    MMA_UFC = 27829360
    KABADDI = 27979456
    GYMNASTICS = 28347302
    TV_SPECIALS = 28347303
    MUSIC = 28347304
    NOVELTY_BETS = 28347305
    LOTTERY_SPECIALS = 28361978
    BEACH_SOCCER = 28361979
    HOLLYWOOD = 28361980
    WEIGHTLIFTING = 28361982
    WEATHER = 28361983
    SKI_JUMPING = 28361984
    NORDIC_COMBINED = 28361985
    ALPINE_SKIING = 28361987
    CROSS_COUNTRY = 28361988
    BIATHLON = 28361989
    FREESTYLE_SKIING = 28361990
    SPEED_SKATING = 28361992
    SPORTS_NOVELTIES = 28373540
