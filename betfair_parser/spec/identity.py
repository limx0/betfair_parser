from typing import Annotated, Literal
from urllib.parse import quote

import msgspec

from betfair_parser.exceptions import IdentityError, LoginImpossible
from betfair_parser.spec.common import BaseResponse, EndpointType, Params, Request, decode
from betfair_parser.strenums import DocumentedEnum, StrEnum, auto, doc


class _IdentityRequest(Request, frozen=True):
    endpoint_type = EndpointType.IDENTITY

    def parse_response(self, response, raise_errors=True):
        resp = decode(response, type=self.return_type)
        if resp.is_error and raise_errors:
            raise self.throws(str(resp.error), response=resp, request=self)
        return resp

    def body(self):
        return b""


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

    # In case of a successful login, the error field is an empty string. To express this, either a
    # Union[LoginExceptionCode, Literal[""]] or a subclass of this enum, extending the fields, would
    # be the most explicit way to express this behaviour. Unfortunately, we can't have a union
    # of two string classes for unambiguous parsing with msgspec. And also unfortunately, python
    # enums can't be subclassed in a straight forward way. So let's add the successful status
    # codes here as well.
    NO_ERROR = doc(value="", docstring="No error occurred")  # for login
    SUCCESS = doc(value="SUCCESS", docstring="No error occurred, operation successful")  # for certlogin


LoginStatusCode = Annotated[LoginExceptionCode, msgspec.Meta(title="LoginStatusCode")]


class LoginResponse(BaseResponse, frozen=True):
    token: str  # session token
    product: str  # application key
    status: LoginStatus
    error: LoginExceptionCode

    @property
    def is_error(self):
        return self.status != LoginStatus.SUCCESS


class _LoginParams(Params, frozen=True):
    username: str  # The username to be used for the login

    # The password to be used for the login. For strong auth customers, this should
    # be their password with a two-factor auth code appended to the password string.
    password: str


class Login(_IdentityRequest, kw_only=True, frozen=True):
    params: _LoginParams
    return_type = LoginResponse
    throws = LoginImpossible

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            # X-Application to be set by the application
        }

    def body(self) -> bytes:
        return f"username={quote(self.params.username)}&password={quote(self.params.password)}".encode()


class KeepAliveLogoutResponse(BaseResponse, frozen=True):
    token: str  # session token
    product: str  # application key
    status: Literal["SUCCESS", "FAIL"]
    error: Literal["INPUT_VALIDATION_ERROR", "INTERNAL_ERROR", "NO_SESSION", ""]

    @property
    def is_error(self):
        return self.status != "SUCCESS"


class KeepAlive(_IdentityRequest, frozen=True):
    params: Params | None = None
    return_type = KeepAliveLogoutResponse
    throws = IdentityError


class Logout(_IdentityRequest, frozen=True):
    params: Params | None = None
    return_type = KeepAliveLogoutResponse
    throws = IdentityError


class CertLoginResponse(BaseResponse, frozen=True):
    login_status: LoginStatusCode
    session_token: str = ""

    # Behave like LoginResponse
    @property
    def token(self):
        return self.session_token

    @property
    def status(self):
        return self.login_status

    @property
    def error(self):
        return self.login_status if self.is_error else None

    @property
    def is_error(self):
        return self.status != LoginExceptionCode.SUCCESS


class CertLogin(_IdentityRequest, kw_only=True, frozen=True, tag=str.lower):
    # Subclassing Login would have been more obvious, but then mypy freaks out
    # due to a different return_type

    endpoint_type = EndpointType.IDENTITY_CERT
    params: _LoginParams
    return_type = CertLoginResponse
    throws = LoginImpossible

    headers = staticmethod(Login.headers)  # type: ignore[assignment,unused-ignore]
    body = Login.body
