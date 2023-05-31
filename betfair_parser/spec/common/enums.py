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


# https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Additional+Information?preview=/43090178/43090179/EventTypIds.xlsx
EVENT_TYPE_TO_NAME = {
    1: "Soccer",
    2: "Tennis",
    3: "Golf",
    4: "Cricket",
    5: "Rugby Union",
    6: "Boxing",
    7: "Horse Racing",
    8: "Motor Sport",
    9: "Soccer Euro 2000",
    10: "Special Bets",
    11: "Cycling",
    12: "Rowing",
    1477: "Rugby League",
    3503: "Darts",
    3988: "Athletics",
    4339: "Greyhound Racing",
    6231: "Financial Bets",
    6422: "Snooker",
    6423: "American Football",
    7228: "Olympics - Sydney 2000",
    7511: "Baseball",
    7522: "Basketball",
    7523: "Hockey",
    7524: "Ice Hockey",
    7525: "Sumo Wrestling",
    61420: "Australian Rules",
    66598: "Gaelic Football",
    66599: "Hurling",
    72382: "Pool",
    136332: "Chess",
    141540: "2002 Winter Olympics",
    189929: "Poker Room",
    256284: "Trotting",
    300000: "Commonwealth Games",
    315220: "Poker",
    451485: "Winter Sports",
    468328: "Handball",
    606611: "Netball",
    620576: "Swimming",
    627555: "Badminton",
    678378: "International Rules",
    982477: "Bridge",
    998916: "Yachting",
    998917: "Volleyball",
    998918: "Bowls",
    998919: "Bandy",
    998920: "Floorball",
    1444073: "Exchange Poker",
    1444076: "Exchange Blackjack",
    1444085: "Exchange Baccarat",
    1444092: "Exchange Hi Lo",
    1444099: "Exchange Omaha Hi",
    1444115: "Exchange Card Racing",
    1444120: "Casino",
    1444130: "Exchange Roulette",
    1444150: "Exchange Bullseye Roulette",
    1564529: "Soccer - Euro 2004",
    1896798: "Olympics 2004",
    1938544: "Backgammon",
    2030972: "GAA Sports",
    2152880: "Gaelic Games",
    2264869: "Internal Markets",
    2378961: "Politics",
    2593174: "Table Tennis",
    2791893: "Yahoo Racing",
    2872194: "Beach Volleyball",
    2872196: "Canoeing",
    2901849: "Water Polo",
    2977000: "Polo",
    3088925: "Fishing",
    3130721: "Roller Hockey",
    3145419: "Cross Sport Accumulators",
    4609466: "Squash",
    4726642: "Surfing",
    4968929: "Combat Sports",
    5402258: "Exchange Games",
    5412697: "Pelota",
    5545196: "Featured Markets",
    5545197: "Featured Markets",
    10271443: "Exchange Casino",
    10390264: "Ten Pin Bowling",
    15242720: "Tradefair",
    15826206: "Futsal",
    15826207: "Fussball",
    16872235: "Harness Racing",
    18051261: "Olympics 2008",
    18643353: "Equestrian",
    26397698: "Horse Racing - Virtual",
    26420387: "Mixed Martial Arts",
    26686903: "Olympics 2012",
    26886906: "Paralympics 2012",
    27065662: "Triathlon",
    27105927: "Winter Olympics 2018",
    27388198: "Current Affairs",
    27438978: "Virtual Sports",
    27454571: "E-Sports",
    27456382: "Baku 2015",
    27485048: "Wrestling",
    27589895: "Olympics 2016",
    27596832: "New Customer Offer",
    27610222: "UFC",
    27610230: "GAA Football",
    27610231: "GAA Hurling",
    27829360: "MMA / UFC",
    27979456: "Kabaddi",
    28347302: "Gymnastics",
    28347303: "TV Specials",
    28347304: "Music",
    28347305: "Novelty Bets",
    28361978: "Lottery Specials",
    28361979: "Beach Soccer",
    28361980: "Hollywood",
    28361982: "Weightlifting",
    28361983: "Weather",
    28361984: "Ski Jumping",
    28361985: "Nordic Combined",
    28361987: "Alpine Skiing",
    28361988: "Cross Country",
    28361989: "Biathlon",
    28361990: "Freestyle Skiing",
    28361992: "Speed Skating",
    28373540: "Sports Novelties",
}
