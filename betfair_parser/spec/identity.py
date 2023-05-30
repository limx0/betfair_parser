from typing import Literal, Union
from urllib.parse import quote

from betfair_parser.spec.common import BaseResponse, Params, Request, decode
from betfair_parser.spec.constants import EndpointType
from betfair_parser.spec.error_codes import LoginExceptionCode
from betfair_parser.strenums import StrEnum, auto


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
