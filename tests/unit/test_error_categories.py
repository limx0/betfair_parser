"""Tests for the error code classification, see betfair_parser.exceptions."""

import asyncio
import io

import pytest

from betfair_parser.exceptions import (
    CODE_TO_CATEGORY,
    AccountAPINGException,
    ErrorCategory,
    LoginError,
    LoginImpossible,
    StreamAuthenticationError,
    StreamError,
    classify_error,
)
from betfair_parser.spec.accounts.operations import GetAccountFunds
from betfair_parser.spec.common.enums import AccountAPINGExceptionCode, APINGExceptionCode
from betfair_parser.spec.identity import Login, LoginExceptionCode
from betfair_parser.spec.streaming import Status, stream_decode
from betfair_parser.spec.streaming.enums import StatusErrorCode
from betfair_parser.stream import AsyncStream, AsyncStreamReader, ExchangeStream, StreamReader
from tests.resources import RESOURCES_DIR


INVALID_SESSION_INFORMATION_RESPONSE = (
    RESOURCES_DIR / "responses" / "accounts" / "get_account_funds_error_invalid_session_information.json"
)
INVALID_PARAMETERS_RESPONSE = (
    RESOURCES_DIR / "responses" / "accounts" / "get_account_funds_error_invalid_parameters.json"
)
STREAM_STATUS_ERROR = RESOURCES_DIR / "responses" / "streaming" / "status_error.json"
CONNECTION_RESPONSE = (RESOURCES_DIR / "responses" / "streaming" / "connection.json").read_bytes()
AUTH_FAILURE_RESPONSE = (
    b'{"op":"status","statusCode":"FAILURE","errorCode":"NO_SESSION",'
    b'"errorMessage":"authentication failed","connectionClosed":true}\n'
)


class FakeStream(io.RawIOBase):
    """Minimal sync/async stand-in for the stream io used in the connect handshake."""

    def __init__(self, lines):
        super().__init__()
        self.lines = list(lines)

    def readline(self, size: int = -1):
        return self.lines.pop(0)

    def write(self, data):
        pass


class FakeAsyncStream(AsyncStream):
    def __init__(self, lines):
        super().__init__(endpoint="fake")
        self.lines = list(lines)

    async def readline(self):
        return self.lines.pop(0)

    async def write(self, data):
        pass


def test_registry_keys_and_values():
    for code, category in CODE_TO_CATEGORY.items():
        assert isinstance(code, str)
        assert isinstance(category, ErrorCategory)


def test_registry_covers_all_str_error_codes():
    error_enums = (
        APINGExceptionCode,
        AccountAPINGExceptionCode,
        LoginExceptionCode,
        StatusErrorCode,
    )
    not_errors = {LoginExceptionCode.NO_ERROR.value, LoginExceptionCode.SUCCESS.value}
    for enum_cls in error_enums:
        for member in enum_cls:
            if member.value not in not_errors:
                assert member.value in CODE_TO_CATEGORY, f"{enum_cls.__name__}.{member.name} is not classified"


@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("INVALID_SESSION_INFORMATION", ErrorCategory.LOGIN_REQUIRED),
        ("NO_SESSION", ErrorCategory.LOGIN_REQUIRED),
        ("SUBSCRIPTION_EXPIRED", ErrorCategory.LOGIN_REQUIRED),
        ("TOO_MANY_REQUESTS", ErrorCategory.TEMPORARY),
        ("SERVICE_BUSY", ErrorCategory.TEMPORARY),
        ("TIMEOUT_ERROR", ErrorCategory.TEMPORARY),
        ("TEMPORARY_BAN_TOO_MANY_REQUESTS", ErrorCategory.TEMPORARY),
        ("NO_APP_KEY", ErrorCategory.ACTION_REQUIRED),
        ("INVALID_APP_KEY", ErrorCategory.ACTION_REQUIRED),
        ("INVALID_USERNAME_OR_PASSWORD", ErrorCategory.ACTION_REQUIRED),
        ("KYC_SUSPEND", ErrorCategory.ACTION_REQUIRED),
        ("INVALID_INPUT_DATA", ErrorCategory.CLIENT_ERROR),
        ("-32700", ErrorCategory.CLIENT_ERROR),
        ("-32602", ErrorCategory.CLIENT_ERROR),
        ("-32603", ErrorCategory.TEMPORARY),
        ("SOME_UNKNOWN_ERROR_CODE", None),
    ],
)
def test_classify_error_by_raw_code(code, expected):
    assert classify_error(AccountAPINGException("message", code=code)) == expected


def test_classify_error_by_enum_code():
    assert (
        classify_error(AccountAPINGException("message", code=APINGExceptionCode.INVALID_SESSION_INFORMATION))
        == ErrorCategory.LOGIN_REQUIRED
    )
    assert (
        classify_error(LoginError("message", code=LoginExceptionCode.TEMPORARY_BAN_TOO_MANY_REQUESTS))
        == ErrorCategory.TEMPORARY
    )
    assert classify_error(StreamError("message", code=StatusErrorCode.NO_SESSION)) == ErrorCategory.LOGIN_REQUIRED


def test_classify_error_without_code():
    assert classify_error(AccountAPINGException("message")) is None
    assert classify_error(ValueError("message")) is None


def test_classify_error_non_error_code():
    assert classify_error(LoginError("message", code=LoginExceptionCode.NO_ERROR)) is None
    assert classify_error(LoginError("message", code=LoginExceptionCode.SUCCESS)) is None


def test_category_property():
    exc = AccountAPINGException("message", code=APINGExceptionCode.INVALID_SESSION_INFORMATION)
    assert exc.category == ErrorCategory.LOGIN_REQUIRED
    assert AccountAPINGException("message").category is None
    assert classify_error(exc) == exc.category


def test_backwards_compatibility_names():
    """LoginImpossible stays a permanent alias, StreamAuthenticationError is a real subclass now.
    Neither name implies the action category anymore - check .category instead."""
    assert LoginImpossible is LoginError
    assert issubclass(StreamAuthenticationError, StreamError)
    try:
        raise LoginError("message", code="INVALID_USERNAME_OR_PASSWORD")
    except LoginImpossible as exc:
        assert exc.category == ErrorCategory.ACTION_REQUIRED


def test_stream_auth_handshake_failure():
    reader = StreamReader(app_key="app_key", token="token")
    stream = FakeStream([CONNECTION_RESPONSE, AUTH_FAILURE_RESPONSE])
    with pytest.raises(StreamAuthenticationError) as exc_info:
        reader.connect(stream)
    assert isinstance(exc_info.value, StreamError)
    assert exc_info.value.code.name == "NO_SESSION"
    assert exc_info.value.category == ErrorCategory.LOGIN_REQUIRED


def test_stream_auth_handshake_failure_async():
    async def connect():
        reader = AsyncStreamReader(app_key="app_key", token="token")
        stream = FakeAsyncStream([CONNECTION_RESPONSE, AUTH_FAILURE_RESPONSE])
        with pytest.raises(StreamAuthenticationError) as exc_info:
            await reader.connect_async(stream)
        return exc_info.value

    exc = asyncio.run(connect())
    assert isinstance(exc, StreamError)
    assert exc.code.name == "NO_SESSION"
    assert exc.category == ErrorCategory.LOGIN_REQUIRED


def test_stream_error_type_by_authentication_state():
    """Status errors before the authentication handshake completed raise StreamAuthenticationError,
    errors on an authenticated stream raise the generic StreamError."""
    msg = stream_decode(STREAM_STATUS_ERROR.read_bytes())
    assert isinstance(msg, Status)
    stream = ExchangeStream(app_key="app_key", token="token")
    with pytest.raises(StreamAuthenticationError):
        stream.handle_status(msg)

    stream.authenticated = True
    with pytest.raises(StreamError) as exc_info:
        stream.handle_status(msg)
    assert type(exc_info.value) is StreamError
    assert exc_info.value.code.name == "TIMEOUT"
    assert exc_info.value.category == ErrorCategory.TEMPORARY


def test_invalid_session_information_regression():
    """Regression test for the production incident: getAccountFunds with an expired session token
    returned INVALID_SESSION_INFORMATION, which has to be classified as LOGIN_REQUIRED."""
    raw = INVALID_SESSION_INFORMATION_RESPONSE.read_bytes()
    with pytest.raises(AccountAPINGException) as exc_info:
        GetAccountFunds.with_params(request_id=1).parse_response(raw)
    assert exc_info.value.code.name == "INVALID_SESSION_INFORMATION"
    # the client-visible error string must stay exactly as it was before
    assert str(exc_info.value) == (
        "INVALID_SESSION_INFORMATION: The session token hasn't been provided, is invalid or has expired. "
        "You must login again to create a new session token."
    )
    assert classify_error(exc_info.value) == ErrorCategory.LOGIN_REQUIRED


def test_invalid_parameters_regression():
    raw = INVALID_PARAMETERS_RESPONSE.read_bytes()
    with pytest.raises(AccountAPINGException) as exc_info:
        GetAccountFunds.with_params(request_id=1).parse_response(raw)
    assert exc_info.value.code.name == "INVALID_PARAMETERS"
    assert classify_error(exc_info.value) == ErrorCategory.CLIENT_ERROR


def test_stream_status_error_classification():
    msg = stream_decode(STREAM_STATUS_ERROR.read_bytes())
    assert isinstance(msg, Status)
    stream = ExchangeStream(app_key="app_key", token="token")
    stream.authenticated = True
    with pytest.raises(StreamError) as exc_info:
        stream.handle_status(msg)
    assert type(exc_info.value) is StreamError
    assert exc_info.value.code.name == "TIMEOUT"
    assert classify_error(exc_info.value) == ErrorCategory.TEMPORARY


def test_identity_error_classification():
    raw = b'{"token":"","product":"","status":"FAIL","error":"INVALID_USERNAME_OR_PASSWORD"}'
    with pytest.raises(LoginError) as exc_info:
        Login.with_params(username="user", password="pass").parse_response(raw)
    assert exc_info.value.code.name == "INVALID_USERNAME_OR_PASSWORD"
    assert classify_error(exc_info.value) == ErrorCategory.ACTION_REQUIRED
