"""
Minimalistic client example

`session` should be some requests session or httpx client.

This library aims for compatibility with any kind of http client. Thus, the objects within
the specification provide a straight forward way to quickly construct a http request out of
a prepared header and body.
"""

from collections.abc import MutableMapping
from typing import TYPE_CHECKING, Any, Protocol

from betfair_parser.endpoints import ENDPOINTS, EndpointConfig
from betfair_parser.spec.common import Request
from betfair_parser.spec.identity import CertLogin, KeepAlive, Login, Logout


class HTTPResponse(Protocol):
    """Structural response subset provided by `requests.Response` as well as `httpx.Response`."""

    @property
    def content(self) -> bytes: ...

    def raise_for_status(self) -> object: ...


class HTTPSession(Protocol):
    """Structural session subset provided by `requests.Session` as well as `httpx.Client`."""

    @property
    def headers(self) -> MutableMapping[str, str]: ...

    def post(
        self, url: str, *, headers: MutableMapping[str, str] | None = None, data: bytes | None = None
    ) -> HTTPResponse: ...


if TYPE_CHECKING:
    # Keep the protocol structurally satisfied by the reference implementations. requests' stubs
    # declare header values as `str | bytes`, but only str values are ever used with this library.
    from typing import cast

    from requests import Response, Session

    _session_check: HTTPSession = cast(HTTPSession, Session())
    _response_check: HTTPResponse = Response()


def request(session: HTTPSession, req: Request, endpoints: EndpointConfig = ENDPOINTS) -> Any:
    """Minimalistic client example."""

    url = endpoints.url_for_request(req)
    raw_resp = session.post(url, headers=req.headers(), data=req.body())
    raw_resp.raise_for_status()
    return req.parse_response(raw_resp.content, raise_errors=True)


def login(
    session: HTTPSession,
    username: str,
    password: str,
    app_key: str,
    two_factor_code: str = "",
    endpoints: EndpointConfig = ENDPOINTS,
) -> None:
    """Authenticate a session to betfair.

    The optional two-factor code is simply appended to the password, as expected by betfair.
    """

    session.headers.update({"X-Application": app_key})
    resp = request(
        session,
        Login.with_params(username=username, password=password + two_factor_code),
        endpoints=endpoints,
    )
    session.headers.update(
        {
            "X-Authentication": resp.token,
            "X-Application": resp.product,
        }
    )


def keep_alive(session: HTTPSession, endpoints: EndpointConfig = ENDPOINTS) -> None:
    """Renew authentication."""

    resp = request(session, KeepAlive(), endpoints=endpoints)
    session.headers.update({"X-Authentication": resp.token})


def cert_login(
    session: HTTPSession, username: str, password: str, app_key: str, endpoints: EndpointConfig = ENDPOINTS
) -> None:
    """Bot authentication. Session certificates need to be properly configured already."""

    session.headers.update({"X-Application": app_key})
    resp = request(
        session,
        CertLogin.with_params(username=username, password=password),
        endpoints=endpoints,
    )
    session.headers.update({"X-Authentication": resp.token})


def logout(session: HTTPSession, endpoints: EndpointConfig = ENDPOINTS) -> None:
    try:
        request(session, Logout(), endpoints=endpoints)
    finally:
        session.headers.pop("X-Authentication", None)
