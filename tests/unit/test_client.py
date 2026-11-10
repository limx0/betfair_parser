"""Unit tests for the minimalistic client, using a fake requests-like session.

The integration tests in `tests/integration/test_live.py` cover the client against the
real API (skipped without credentials), these tests cover the full client logic offline.
"""

import json

import pytest

from betfair_parser import client
from betfair_parser.endpoints import ENDPOINTS
from betfair_parser.exceptions import AccountAPINGException, APIError, IdentityError, LoginError
from betfair_parser.spec.accounts import GetAccountFunds
from tests.resources import RESOURCES_DIR


class FakeResponse:
    """Structural `requests.Response` replacement."""

    def __init__(self, content, status_error=None):
        self.content = content
        self._status_error = status_error

    def raise_for_status(self):
        if self._status_error is not None:
            raise self._status_error


class FakeSession:
    """Structural `requests.Session` replacement, recording all posts.

    Real HTTP libraries merge the session headers into each request, so the recorded
    per-call headers only contain the headers handed to `post` explicitly.
    """

    def __init__(self):
        self.headers = {}
        self.calls = []
        self.responses = {}

    def respond_to(self, url_fragment, content, status_error=None):
        self.responses[url_fragment] = FakeResponse(content, status_error)

    def post(self, url, *, headers=None, data=None):
        self.calls.append((url, headers, data))
        for fragment, response in self.responses.items():
            if fragment in url:
                return response
        raise AssertionError(f"Unexpected POST to {url}")


def identity_response(token="sess-token", product="app-key", status="SUCCESS", error=""):
    return json.dumps({"token": token, "product": product, "status": status, "error": error}).encode()


def test_request_parses_result():
    session = FakeSession()
    request = GetAccountFunds.with_params()
    raw = json.loads((RESOURCES_DIR / "responses" / "accounts" / "get_account_funds_no_exposure.json").read_bytes())
    raw["id"] = request.id
    session.respond_to("getAccountFunds", json.dumps(raw).encode())

    result = client.request(session, request)

    url, headers, body = session.calls[0]
    assert url == ENDPOINTS.url_for_request(request)
    assert headers == request.headers()
    assert body == request.body()
    assert result.validate()


def test_request_error_raises_aping_exception():
    session = FakeSession()
    request = GetAccountFunds.with_params()
    error = {"jsonrpc": "2.0", "id": request.id, "error": {"code": -32602, "message": "DSC-0018"}}
    session.respond_to("getAccountFunds", json.dumps(error).encode())

    with pytest.raises(AccountAPINGException, match="INVALID_PARAMETERS") as exc_info:
        client.request(session, request)

    assert exc_info.value.code.name == "INVALID_PARAMETERS"
    assert exc_info.value.code.value == -32602
    assert str(exc_info.value.response.error.exception_code).startswith("INVALID_PARAMETERS")
    assert exc_info.value.request is request


def test_request_response_id_mismatch():
    session = FakeSession()
    request = GetAccountFunds.with_params()
    raw = json.loads((RESOURCES_DIR / "responses" / "accounts" / "get_account_funds_no_exposure.json").read_bytes())
    raw["id"] = request.id + 1
    session.respond_to("getAccountFunds", json.dumps(raw).encode())

    with pytest.raises(APIError, match="does not match"):
        client.request(session, request)


def test_request_http_error_propagates():
    session = FakeSession()
    session.respond_to("getAccountFunds", b"{}", status_error=ValueError("bad request"))

    with pytest.raises(ValueError, match="bad request"):
        client.request(session, GetAccountFunds.with_params())


def test_login_sets_session_headers():
    session = FakeSession()
    session.respond_to("login", identity_response())

    client.login(session, "user", "pass", "app-key", two_factor_code="123456")

    assert session.headers == {"X-Application": "app-key", "X-Authentication": "sess-token"}
    url, headers, data = session.calls[0]
    assert url == ENDPOINTS.identity + "login"
    assert headers == {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    assert data == b"username=user&password=pass123456"


def test_login_failure_raises_login_error():
    session = FakeSession()
    session.respond_to("login", identity_response(token="", product="", status="FAIL", error="INPUT_VALIDATION_ERROR"))

    with pytest.raises(LoginError, match="INPUT_VALIDATION_ERROR"):
        client.login(session, "user", "pass", "app-key")


def test_keep_alive_renews_token():
    session = FakeSession()
    session.headers.update({"X-Application": "app-key", "X-Authentication": "old-token"})
    session.respond_to("keepAlive", identity_response(token="renewed-token"))

    client.keep_alive(session)

    assert session.headers["X-Authentication"] == "renewed-token"
    url, _, data = session.calls[0]
    assert url == ENDPOINTS.identity + "keepAlive"
    assert data == b""


def test_cert_login_sets_session_token():
    session = FakeSession()
    session.respond_to("certlogin", json.dumps({"loginStatus": "SUCCESS", "sessionToken": "cert-token"}).encode())

    client.cert_login(session, "user", "pass", "app-key")

    assert session.headers == {"X-Application": "app-key", "X-Authentication": "cert-token"}
    url, _, data = session.calls[0]
    assert url == ENDPOINTS.identity_cert + "certlogin"
    assert data == b"username=user&password=pass"


def test_logout_pops_token():
    session = FakeSession()
    session.headers["X-Authentication"] = "tok"
    session.respond_to("logout", identity_response(token="", product="", status="SUCCESS"))

    client.logout(session)

    assert "X-Authentication" not in session.headers


def test_logout_pops_token_even_on_error():
    session = FakeSession()
    session.headers["X-Authentication"] = "tok"
    session.respond_to("logout", identity_response(token="", product="", status="FAIL", error="INTERNAL_ERROR"))

    with pytest.raises(IdentityError):
        client.logout(session)

    assert "X-Authentication" not in session.headers
