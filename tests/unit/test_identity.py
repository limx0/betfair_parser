import pytest

from betfair_parser.endpoints import ENDPOINTS
from betfair_parser.spec.identity import KeepAlive, LoginResponse, Logout


@pytest.mark.parametrize("msg", [KeepAlive(), KeepAlive.with_params(), Logout(), Logout.with_params()])
def test_request_init(msg):
    """
    Identity requests don't use a request id and don't use the request `method` encoded by msgspec
    within the request body. So the initialisation with `with_params` can be omitted, if there are
    no parameters. The objects should behave the same regardless of the initialisation.
    """
    assert msg.method.lower() == type(msg).__name__.lower()
    assert not msg.body()
    assert ENDPOINTS.url_for_request(msg).lower().endswith(f"/api/{type(msg).__name__.lower()}")
    assert msg.validate()


def test_login_response():
    resp = b'{"token":"","product":"","status":"FAIL","error":"INPUT_VALIDATION_ERROR"}'
    assert LoginResponse.parse(resp)
