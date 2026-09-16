"""Exception types used across this package.

The exception hierarchy encodes the ORIGIN of an error (which API or endpoint
failed), while the error codes mirror the betfair API 1:1 without carrying any
information about how a client should react to them. The ACTION category is a
separate, orthogonal axis derived from the error code via :func:`classify_error`
(also available as the :attr:`BetfairError.category` property):

- TEMPORARY: server-side issue, retry the same request after a backoff
- LOGIN_REQUIRED: session or subscription expired, re-login and retry the request
- CLIENT_ERROR: the request itself is malformed, don't retry it unmodified
- ACTION_REQUIRED: manual intervention required (account status, credentials, app keys)
"""

from typing import Any

from betfair_parser.strenums import StrEnum, auto


class ErrorCategory(StrEnum):
    """Action category derived from an error code, see :func:`classify_error`."""

    TEMPORARY = auto()
    LOGIN_REQUIRED = auto()
    CLIENT_ERROR = auto()
    ACTION_REQUIRED = auto()


class BetfairError(Exception):
    """Base class for all Exceptions in this package. Allow to hand in custom data with keyword arguments."""

    code: Any  # optional error code, attached via keyword argument

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.__dict__.update(kwargs)

    @property
    def category(self) -> ErrorCategory | None:
        """Action category derived from the error code, see :func:`classify_error`."""
        return classify_error(self)


class JSONError(BetfairError):
    """Issue with the data serialization."""


class APIError(BetfairError):
    """Most general API error."""


class APINGException(APIError):
    """Errors thrown from a betfair operation."""


class AccountAPINGException(APIError):
    """An issue thrown from the accounts API."""


class IdentityError(APIError):
    """An issue thrown from the identity API."""


class LoginError(IdentityError):
    """An issue thrown from the login endpoint.

    Raised for any failed login attempt, regardless of the action category.
    A login error may well be TEMPORARY (e.g. rate limiting), so check
    :attr:`category` / :func:`classify_error` to decide how to react.
    """


# Permanent backwards-compatibility aliases. LoginImpossible doesn't imply
# manual resolution anymore - the action category is determined by the error code.
LoginImpossible = LoginError


class StreamError(APIError):
    """Issues related with the streaming API."""


class StreamAuthenticationError(StreamError):
    """Raised for stream errors before the authentication handshake completed (ExchangeStream.authenticated)."""


# Error codes mapped to their action category. Keys are the code values as they
# appear on the wire (name for str codes, JSON-RPC number for int codes).
# Not listed means unknown or unclassifiable, e.g. LoginExceptionCode.NO_ERROR.
CODE_TO_CATEGORY: dict[str, ErrorCategory] = {
    # APINGExceptionCode
    "TOO_MUCH_DATA": ErrorCategory.CLIENT_ERROR,
    "INVALID_INPUT_DATA": ErrorCategory.CLIENT_ERROR,
    "INVALID_SESSION_INFORMATION": ErrorCategory.LOGIN_REQUIRED,
    "NO_APP_KEY": ErrorCategory.ACTION_REQUIRED,
    "NO_SESSION": ErrorCategory.LOGIN_REQUIRED,
    "UNEXPECTED_ERROR": ErrorCategory.TEMPORARY,
    "INVALID_APP_KEY": ErrorCategory.ACTION_REQUIRED,
    "TOO_MANY_REQUESTS": ErrorCategory.TEMPORARY,
    "SERVICE_BUSY": ErrorCategory.TEMPORARY,
    "TIMEOUT_ERROR": ErrorCategory.TEMPORARY,
    "REQUEST_SIZE_EXCEEDS_LIMIT": ErrorCategory.CLIENT_ERROR,
    "ACCESS_DENIED": ErrorCategory.ACTION_REQUIRED,
    "SERVICE_UNAVAILABLE": ErrorCategory.TEMPORARY,
    # AccountAPINGExceptionCode
    "DUPLICATE_APP_NAME": ErrorCategory.CLIENT_ERROR,
    "APP_KEY_CREATION_FAILED": ErrorCategory.CLIENT_ERROR,
    "APP_CREATION_FAILED": ErrorCategory.CLIENT_ERROR,
    "SUBSCRIPTION_EXPIRED": ErrorCategory.LOGIN_REQUIRED,
    "INVALID_SUBSCRIPTION_TOKEN": ErrorCategory.LOGIN_REQUIRED,
    "INVALID_CLIENT_REF": ErrorCategory.CLIENT_ERROR,
    "WALLET_TRANSFER_ERROR": ErrorCategory.CLIENT_ERROR,
    "INVALID_VENDOR_CLIENT_ID": ErrorCategory.CLIENT_ERROR,
    "USER_NOT_SUBSCRIBED": ErrorCategory.ACTION_REQUIRED,
    "INVALID_SECRET": ErrorCategory.CLIENT_ERROR,
    "INVALID_AUTH_CODE": ErrorCategory.CLIENT_ERROR,
    "INVALID_GRANT_TYPE": ErrorCategory.CLIENT_ERROR,
    "CUSTOMER_ACCOUNT_CLOSED": ErrorCategory.ACTION_REQUIRED,
    # LoginExceptionCode
    "ACCOUNT_ALREADY_LOCKED": ErrorCategory.ACTION_REQUIRED,
    "ACCOUNT_NOW_LOCKED": ErrorCategory.ACTION_REQUIRED,
    "ACCOUNT_PENDING_PASSWORD_CHANGE": ErrorCategory.ACTION_REQUIRED,
    "ACTIONS_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "AGENT_CLIENT_MASTER": ErrorCategory.ACTION_REQUIRED,
    "AGENT_CLIENT_MASTER_SUSPENDED": ErrorCategory.ACTION_REQUIRED,
    "AUTHORIZED_ONLY_FOR_DOMAIN": ErrorCategory.ACTION_REQUIRED,
    "AUTHORIZED_ONLY_FOR_DOMAIN_RO": ErrorCategory.ACTION_REQUIRED,
    "AUTHORIZED_ONLY_FOR_DOMAIN_SE": ErrorCategory.ACTION_REQUIRED,
    "BETTING_RESTRICTED_LOCATION": ErrorCategory.ACTION_REQUIRED,
    "CERT_AUTH_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "CHANGE_PASSWORD_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "CLOSED": ErrorCategory.ACTION_REQUIRED,
    "CONTACT_VERIFICATION_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "DANISH_AUTHORIZATION_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "DENMARK_MIGRATION_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "EMAIL_LOGIN_NOT_ALLOWED": ErrorCategory.ACTION_REQUIRED,
    "FORBIDDEN": ErrorCategory.ACTION_REQUIRED,
    "INTERNATIONAL_TERMS_ACCEPTANCE_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "INVALID_USERNAME_OR_PASSWORD": ErrorCategory.ACTION_REQUIRED,
    "ITALIAN_CONTRACT_ACCEPTANCE_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "ITALIAN_PROFILING_ACCEPTANCE_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "KYC_SUSPEND": ErrorCategory.ACTION_REQUIRED,
    "MIGRATION_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "MULTI_FACTOR_AUTHENTICATION_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "MULTIPLE_USERS_WITH_SAME_CREDENTIAL": ErrorCategory.CLIENT_ERROR,
    "NOT_AUTHORIZED_BY_REGULATOR_DK": ErrorCategory.ACTION_REQUIRED,
    "NOT_AUTHORIZED_BY_REGULATOR_IT": ErrorCategory.ACTION_REQUIRED,
    "PENDING_AUTH": ErrorCategory.ACTION_REQUIRED,
    "PERSONAL_MESSAGE_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "SECURITY_QUESTION_WRONG_3X": ErrorCategory.ACTION_REQUIRED,
    "SECURITY_RESTRICTED_LOCATION": ErrorCategory.ACTION_REQUIRED,
    "SELF_EXCLUDED": ErrorCategory.ACTION_REQUIRED,
    "SPAIN_MIGRATION_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "SPANISH_TERMS_ACCEPTANCE_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "STRONG_AUTH_CODE_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "STRONG_CODE_FAIL": ErrorCategory.ACTION_REQUIRED,
    "SUSPENDED": ErrorCategory.ACTION_REQUIRED,
    "SWEDEN_BANK_ID_VERIFICATION_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "SWEDEN_NATIONAL_IDENTIFIER_REQUIRED": ErrorCategory.ACTION_REQUIRED,
    "TELBET_TERMS_CONDITIONS_NA": ErrorCategory.ACTION_REQUIRED,
    "TEMPORARY_BAN_TOO_MANY_REQUESTS": ErrorCategory.TEMPORARY,
    "TERMS_AND_CONDITIONS": ErrorCategory.ACTION_REQUIRED,
    "TRADING_MASTER": ErrorCategory.ACTION_REQUIRED,
    "TRADING_MASTER_SUSPENDED": ErrorCategory.ACTION_REQUIRED,
    "DUPLICATE_CARDS": ErrorCategory.CLIENT_ERROR,
    "INPUT_VALIDATION_ERROR": ErrorCategory.CLIENT_ERROR,
    "INTERNAL_ERROR": ErrorCategory.TEMPORARY,
    "INVALID_CONNECTIVITY_TO_REGULATOR_DK": ErrorCategory.TEMPORARY,
    "INVALID_CONNECTIVITY_TO_REGULATOR_IT": ErrorCategory.TEMPORARY,
    "INVALID_PIN": ErrorCategory.CLIENT_ERROR,
    "INVALID_PIN_LOGIN_REQUEST": ErrorCategory.CLIENT_ERROR,
    # JSONExceptionCode (JSON-RPC error numbers)
    "-32700": ErrorCategory.CLIENT_ERROR,  # INVALID_JSON
    "-32601": ErrorCategory.CLIENT_ERROR,  # METHOD_NOT_FOUND
    "-32602": ErrorCategory.CLIENT_ERROR,  # INVALID_PARAMETERS
    "-32603": ErrorCategory.TEMPORARY,  # JSON_RPC_ERROR
    # StatusErrorCode
    "INVALID_INPUT": ErrorCategory.CLIENT_ERROR,
    "TIMEOUT": ErrorCategory.TEMPORARY,
    "NOT_AUTHORIZED": ErrorCategory.ACTION_REQUIRED,
    "MAX_CONNECTION_LIMIT_EXCEEDED": ErrorCategory.ACTION_REQUIRED,
    "SUBSCRIPTION_LIMIT_EXCEEDED": ErrorCategory.CLIENT_ERROR,
    "INVALID_CLOCK": ErrorCategory.CLIENT_ERROR,
    "CONNECTION_FAILED": ErrorCategory.TEMPORARY,
    "INVALID_REQUEST": ErrorCategory.CLIENT_ERROR,
}


def classify_error(e: BaseException) -> ErrorCategory | None:
    """Classify an exception based on its error code.

    Returns the ErrorCategory describing how a client should react, or None if the
    exception carries no error code or the code is unknown.
    """
    code = getattr(e, "code", None)
    if code is None:
        return None
    return CODE_TO_CATEGORY.get(str(getattr(code, "value", code)))
