from typing import Literal, Union
from urllib.parse import quote

from betfair_parser.spec.common import BaseResponse, EndpointType, Params, Request, decode
from betfair_parser.strenums import DocumentedEnum, StrEnum, auto, doc


class IdentityRequest(Request, frozen=True):
    endpoint_type = EndpointType.IDENTITY

    def parse_response(self, response):
        return decode(response, type=self.return_type)


class IdentityResponse(BaseResponse, frozen=True):
    def raise_on_error(self):
        """If the response contains some kind of error condition, raise an according Exception."""
        # TODO: Error handling


class LoginStatus(StrEnum):
    SUCCESS = auto()
    LIMITED_ACCESS = auto()
    LOGIN_RESTRICTED = auto()
    FAIL = auto()


class LoginExceptionCode(DocumentedEnum):
    ACCOUNT_ALREADY_LOCKED = doc("the account is already locked")
    ACCOUNT_NOW_LOCKED = doc("the account was just locked")
    ACCOUNT_PENDING_PASSWORD_CHANGE = doc("The account must undergo password recovery to reactivate")
    ACTIONS_REQUIRED = doc("You must login to https://www.betfair.com to provide missing information.")
    AGENT_CLIENT_MASTER = doc("Agent Client Master")
    AGENT_CLIENT_MASTER_SUSPENDED = doc("Suspended Agent Client Master")
    AUTHORIZED_ONLY_FOR_DOMAIN_RO = doc("Attempting to login to the Betfair Romania with a non .ro account.")
    AUTHORIZED_ONLY_FOR_DOMAIN_SE = doc("Attempting to login to the Betfair Sweden with a non .se account.")
    BETTING_RESTRICTED_LOCATION = doc("the account is accessed from a location where betting is restricted")
    CERT_AUTH_REQUIRED = doc("Certificate required or certificate present but could not authenticate with it")
    CHANGE_PASSWORD_REQUIRED = doc("change password required")
    CLOSED = doc("the account is closed")
    DANISH_AUTHORIZATION_REQUIRED = doc("Danish authorization required")
    DENMARK_MIGRATION_REQUIRED = doc("Denmark migration required")
    DUPLICATE_CARDS = doc("duplicate cards")
    EMAIL_LOGIN_NOT_ALLOWED = doc("This account has not opted in to log in with the email")
    INPUT_VALIDATION_ERROR = doc("Input validation failed for not further specified reason")  # not listed
    INTERNAL_ERROR = doc("Not further specified internal error")  # not listed
    INTERNATIONAL_TERMS_ACCEPTANCE_REQUIRED = doc("The latest international terms and conditions must be accepted.")
    INVALID_CONNECTIVITY_TO_REGULATOR_DK = doc(
        "the DK regulator cannot be accessed due to some internal problems in the system behind or in "
        "at regulator; timeout cases included."
    )
    INVALID_CONNECTIVITY_TO_REGULATOR_IT = doc(
        "the IT regulator cannot be accessed due to some internal problems in the system behind or in at "
        "regulator; timeout cases included."
    )
    INVALID_USERNAME_OR_PASSWORD = doc("the username or password are invalid")
    ITALIAN_CONTRACT_ACCEPTANCE_REQUIRED = doc("The latest Italian contract version must be accepted")
    ITALIAN_PROFILING_ACCEPTANCE_REQUIRED = doc("You must login to the website to accept the new conditions")
    KYC_SUSPEND = doc("KYC suspended")
    MULTIPLE_USERS_WITH_SAME_CREDENTIAL = doc("There is more than one account with the same credential")
    NOT_AUTHORIZED_BY_REGULATOR_DK = doc(
        "the user identified by the given credentials is not authorized in the DK's jurisdictions due to the "
        "regulators' policies. Ex: the user for which this session should be created is not allowed to "
        "act(play, bet) in the DK's jurisdiction."
    )
    NOT_AUTHORIZED_BY_REGULATOR_IT = doc(
        "the user identified by the given credentials is not authorized in the IT's jurisdictions due to the "
        "regulators' policies. Ex: the user for which this session should be created is not allowed to "
        "act(play, bet) in the IT's jurisdiction."
    )
    PENDING_AUTH = doc("pending authentication")
    PERSONAL_MESSAGE_REQUIRED = doc("personal message required for the user")
    SECURITY_QUESTION_WRONG_3X = doc("the user has entered wrong the security answer 3 times")
    SECURITY_RESTRICTED_LOCATION = doc("the account is restricted due to security concerns")
    SELF_EXCLUDED = doc("the account has been self-excluded")
    SPAIN_MIGRATION_REQUIRED = doc("Spain migration required")
    SPANISH_TERMS_ACCEPTANCE_REQUIRED = doc("The latest Spanish terms and conditions version must be accepted")
    STRONG_AUTH_CODE_REQUIRED = doc("2 Step Authentication code is required.")
    SUSPENDED = doc("the account is suspended")
    SWEDEN_BANK_ID_VERIFICATION_REQUIRED = doc("Swedish bank id for Betfair.se not provided.")
    SWEDEN_NATIONAL_IDENTIFIER_REQUIRED = doc("Swedish National identifier for Betfair.se not provided.")
    TELBET_TERMS_CONDITIONS_NA = doc("Telbet terms and conditions rejected")
    TEMPORARY_BAN_TOO_MANY_REQUESTS = doc(
        "The limit for successful login requests per minute has been exceeded. "
        "New login attempts will be banned for 20 minutes"
    )
    TRADING_MASTER = doc("Trading Master Account")
    TRADING_MASTER_SUSPENDED = doc("Suspended Trading Master Account")

    # As there can't be a union of two string classes for unambiguous parsing,
    # we need to include the successful case here as well
    NO_ERROR = doc(value="", docstring="No error occured")


class LoginResponse(IdentityResponse, frozen=True):
    token: str  # session token
    product: str  # application key
    status: LoginStatus
    error: LoginExceptionCode


class _LoginParams(Params, frozen=True):
    username: str  # The username to be used for the login

    # The password to be used for the login. For strong auth customers, this should
    # be their password with a 2 factor auth code appended to the password string.
    password: str


class Login(IdentityRequest, kw_only=True, frozen=True):
    method = "login"
    params: _LoginParams
    return_type = LoginResponse

    @staticmethod
    def headers():
        return {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            # X-Application to be set by the application
        }

    def body(self):
        return f"username={quote(self.params.username)}&password={quote(self.params.password)}"


class KeepAliveLogoutResponse(IdentityResponse, frozen=True):
    token: str  # session token
    product: str  # application key
    status: Literal["SUCCESS", "FAIL"]  # noqa
    error: Literal["INPUT_VALIDATION_ERROR", "INTERNAL_ERROR", "NO_SESSION", ""]  # noqa


class KeepAlive(IdentityRequest, frozen=True):
    method = "keepAlive"
    return_type = KeepAliveLogoutResponse


class Logout(IdentityRequest, frozen=True):
    method = "logout"
    return_type = KeepAliveLogoutResponse


class CertLoginResponse(IdentityResponse, frozen=True):
    session_token: str
    login_status: Union[LoginExceptionCode, Literal["SUCCESS"]]

    # Behave like LoginResponse
    @property
    def token(self):
        return self.session_token

    @property
    def status(self):
        return self.login_status


class CertLogin(IdentityRequest, kw_only=True, frozen=True):
    # Subclassing Login would have been more obvious, but then mypy freaks out
    # with a different return_type

    endpoint_type = EndpointType.IDENTITY_CERT
    method = "certlogin"
    params: _LoginParams
    return_type = CertLoginResponse

    headers = Login.headers
    body = Login.body