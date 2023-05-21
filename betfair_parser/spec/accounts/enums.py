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
