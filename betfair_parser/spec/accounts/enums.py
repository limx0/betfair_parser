from betfair_parser.strenums import DocumentedEnum, doc


class SubscriptionStatus(DocumentedEnum):
    ALL = doc("Any subscription status")
    ACTIVATED = doc("Only activated subscriptions")
    UNACTIVATED = doc("Only unactivated subscriptions")
    CANCELLED = doc("Only cancelled subscriptions")
    EXPIRED = doc("Only expired subscriptions")


class Status(DocumentedEnum):
    SUCCESS = doc("Success status")


class ItemClass(DocumentedEnum):
    UNKNOWN = doc(
        "Statement item not mapped to a specific class. All values will be concatenated "
        "into a single key/value pair.The key will be 'unknownStatementItem' and the "
        "value will be a comma separated string.Please note: This is used to represent "
        "commission payment items."
    )


class Wallet(DocumentedEnum):
    UK = doc("The Global Exchange wallet")
    AUSTRALIAN = doc("@Deprecated but still mentioned in the XML specification")


class IncludeItem(DocumentedEnum):
    ALL = doc("Include all items")
    DEPOSITS_WITHDRAWALS = doc("Include payments only")
    EXCHANGE = doc("Include exchange bets only")
    POKER_ROOM = doc("Include poker transactions only")


class WinLose(DocumentedEnum):
    RESULT_ERR = doc(
        "Record has been affected by a unsettlement. There is no impact on the balance "
        "for these records, this is just a label to say that these are to be corrected."
    )
    RESULT_FIX = doc(
        "Record is a correction to the balance to reverse the impact of records shown "
        "as in error. If commission has been paid on the original settlement then there "
        "will be a second FIX record to reverse the commission."
    )
    RESULT_LOST = doc("Loss")
    RESULT_NOT_APPLICABLE = doc("Amounts relating to commission payments.")
    RESULT_WON = doc("Won")
    COMMISSION_REVERSAL = doc(
        "Betfair has restored the funds to your account that it previously received from you in commission."
    )


class GrantType(DocumentedEnum):
    AUTHORIZATION_CODE = doc(
        "Returned via the Vendor Web API token request. The authorization code will be valid "
        "for a single use for 10 minutes."
    )
    REFRESH_TOKEN = doc("A token that can be used to create a new access token when using the Vendor Web API")


class TokenType(DocumentedEnum):
    BEARER = doc("Token type used for Vendor Web API interactions for making requests on a customers behalf.")


class AffiliateRelationStatus(DocumentedEnum):
    INVALID_USER = doc("Provided vendor client ID is not valid")
    AFFILIATED = doc("Vendor client ID valid and affiliated")
    NOT_AFFILIATED = doc("Vendor client ID valid but not affiliated")


class MarketType(DocumentedEnum):
    """Legacy data"""

    A = doc("Asian Handicap")
    L = doc("Line market")
    O = doc("Odds market")  # noqa
    R = doc("Range market.")
    NOT_APPLICABLE = doc("The market does not have an applicable marketType.")


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
