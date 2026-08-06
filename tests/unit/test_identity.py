import pytest

from betfair_parser.endpoints import ENDPOINTS
from betfair_parser.spec.common import first_lower
from betfair_parser.spec.identity import CertLogin, CertLoginResponse, KeepAlive, LoginResponse, Logout


@pytest.mark.parametrize("msg", [KeepAlive(), KeepAlive.with_params(), Logout(), Logout.with_params()])
def test_request_init(msg):
    """
    Identity requests don't use a request id and don't use the request `method` encoded by msgspec
    within the request body. So the initialisation with `with_params` can be omitted, if there are
    no parameters. The objects should behave the same regardless of the initialisation.
    """
    assert msg.method == first_lower(type(msg).__name__)
    assert not msg.body()
    assert ENDPOINTS.url_for_request(msg).endswith(f"/api/{first_lower(type(msg).__name__)}")
    assert msg.validate()


def test_login_response():
    resp = b'{"token":"","product":"","status":"FAIL","error":"INPUT_VALIDATION_ERROR"}'
    assert LoginResponse.parse(resp)


def test_login_response_with_last_login_date():
    resp = b'{"token":"","product":"","status":"SUCCESS","error":"","lastLoginDate":"01/01/2026 12:34:56"}'
    parsed = LoginResponse.parse(resp)
    assert parsed.last_login_date == "01/01/2026 12:34:56"


@pytest.mark.parametrize(
    "status",
    [
        "CONTACT_VERIFICATION_REQUIRED",
        "MIGRATION_REQUIRED",
        "TERMS_AND_CONDITIONS",
        "MULTI_FACTOR_AUTHENTICATION_REQUIRED",
        "AUTHORIZED_ONLY_FOR_DOMAIN",
        "STRONG_CODE_FAIL",
        "FORBIDDEN",
        "NO_SESSION",
        "INVALID_PIN",
        "INVALID_PIN_LOGIN_REQUEST",
    ],
)
def test_certlogin_response_new_status_codes(status):
    """Recently added Betfair loginStatus codes must be decodable."""
    raw = f'{{"sessionToken":"","loginStatus":"{status}"}}'.encode()
    assert CertLoginResponse.parse(raw).login_status.value == status


def test_certlogin():
    """CertLogin is the only method, that doesn't use camelCase for the method name."""
    msg = CertLogin.with_params(username="asdf", password="test")
    assert msg.method == type(msg).__name__.lower()
    assert ENDPOINTS.url_for_request(msg).endswith(f"/api/{type(msg).__name__.lower()}")
