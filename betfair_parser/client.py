"""
Minimalistic client example

`session` should be some requests session or httpx client.

This library aims for compatibility with any kind of http client. Thus, the objects within
the specification provide a straight forward way to quickly construct a http request out of
of a prepared header and body.
"""

from betfair_parser.endpoints import ENDPOINTS
from betfair_parser.spec.common import Request
from betfair_parser.spec.identity import CertLogin, KeepAlive, Login, Logout


def request(session, req: Request, endpoints=ENDPOINTS):
    """Minimalistic client example."""

    url = endpoints.url_for_request(req)
    raw_resp = session.post(url, headers=req.headers(), data=req.body())
    raw_resp.raise_for_status()  # TODO: This should be wrapped
    resp = req.parse_response(raw_resp.content)
    return resp


def login(session, username, password, app_key, two_factor_code="", endpoints=ENDPOINTS):
    """Authenticate a session to betfair."""

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


def keep_alive(session, endpoints=ENDPOINTS):
    """Renew authentication."""

    resp = request(session, KeepAlive(), endpoints=endpoints)
    session.headers.update({"X-Authentication": resp.token})


def certlogin(session, username, password, app_key, two_factor_code="", endpoints=ENDPOINTS):
    """Bot authentication. Session certificates need to be properly configured already."""

    session.headers.update({"X-Application": app_key})
    resp = request(
        session,
        CertLogin.with_params(username=username, password=password + two_factor_code),
        endpoints=endpoints,
    )
    session.headers.update({"X-Authentication": resp.token})


def logout(session, endpoints=ENDPOINTS):
    request(session, Logout(), endpoints=endpoints)
    del session.headers["X-Authentication"]