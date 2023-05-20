from betfair_parser.strenums import DocumentedEnum, doc


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


class AccountAPIExceptionCode(DocumentedEnum):
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


class LoginExceptionCode(DocumentedEnum):
    INVALID_USERNAME_OR_PASSWORD = doc("the username or password are invalid")
    ACCOUNT_NOW_LOCKED = doc("the account was just locked")
    ACCOUNT_ALREADY_LOCKED = doc("the account is already locked")
    PENDING_AUTH = doc("pending authentication")
    TELBET_TERMS_CONDITIONS_NA = doc("Telbet terms and conditions rejected")
    DUPLICATE_CARDS = doc("duplicate cards")
    SECURITY_QUESTION_WRONG_3X = doc("the user has entered wrong the security answer 3 times")
    KYC_SUSPEND = doc("KYC suspended")
    SUSPENDED = doc("the account is suspended")
    CLOSED = doc("the account is closed")
    SELF_EXCLUDED = doc("the account has been self-excluded")
    INVALID_CONNECTIVITY_TO_REGULATOR_DK = doc(
        "the DK regulator cannot be accessed due to some internal problems in the system behind or in "
        "at regulator; timeout cases included."
    )
    NOT_AUTHORIZED_BY_REGULATOR_DK = doc(
        "the user identified by the given credentials is not authorized in the DK's jurisdictions due to the "
        "regulators' policies. Ex: the user for which this session should be created is not allowed to "
        "act(play, bet) in the DK's jurisdiction."
    )
    INVALID_CONNECTIVITY_TO_REGULATOR_IT = doc(
        "the IT regulator cannot be accessed due to some internal problems in the system behind or in at "
        "regulator; timeout cases included."
    )
    NOT_AUTHORIZED_BY_REGULATOR_IT = doc(
        "the user identified by the given credentials is not authorized in the IT's jurisdictions due to the "
        "regulators' policies. Ex: the user for which this session should be created is not allowed to "
        "act(play, bet) in the IT's jurisdiction."
    )
    SECURITY_RESTRICTED_LOCATION = doc("the account is restricted due to security concerns")
    BETTING_RESTRICTED_LOCATION = doc("the account is accessed from a location where betting is restricted")
    TRADING_MASTER = doc("Trading Master Account")
    TRADING_MASTER_SUSPENDED = doc("Suspended Trading Master Account")
    AGENT_CLIENT_MASTER = doc("Agent Client Master")
    AGENT_CLIENT_MASTER_SUSPENDED = doc("Suspended Agent Client Master")
    DANISH_AUTHORIZATION_REQUIRED = doc("Danish authorization required")
    SPAIN_MIGRATION_REQUIRED = doc("Spain migration required")
    DENMARK_MIGRATION_REQUIRED = doc("Denmark migration required")
    SPANISH_TERMS_ACCEPTANCE_REQUIRED = doc("The latest Spanish terms and conditions version must be accepted")
    ITALIAN_CONTRACT_ACCEPTANCE_REQUIRED = doc("The latest Italian contract version must be accepted")
    CERT_AUTH_REQUIRED = doc("Certificate required or certificate present but could not authenticate with it")
    CHANGE_PASSWORD_REQUIRED = doc("change password required")
    PERSONAL_MESSAGE_REQUIRED = doc("personal message required for the user")
    INTERNATIONAL_TERMS_ACCEPTANCE_REQUIRED = doc(
        "The latest international terms and conditions must be accepted prior to logging in."
    )
    EMAIL_LOGIN_NOT_ALLOWED = doc("This account has not opted in to log in with the email")
    MULTIPLE_USERS_WITH_SAME_CREDENTIAL = doc("There is more than one account with the same credential")
    ACCOUNT_PENDING_PASSWORD_CHANGE = doc("The account must undergo password recovery to reactivate")
