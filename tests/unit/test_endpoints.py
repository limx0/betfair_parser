from dataclasses import dataclass

import pytest

from betfair_parser.endpoints import endpoint
from betfair_parser.spec.common.enums import EndpointType


@dataclass(frozen=True)
class _StubRequest:
    """Minimal request stand-in: url_for_request only reads endpoint_type and method."""

    endpoint_type: EndpointType
    method: str = "TestOperation"


@pytest.mark.parametrize(
    ("endpoint_type", "base_url"),
    [
        (EndpointType.IDENTITY, "https://identitysso.betfair.com/api/"),
        (EndpointType.IDENTITY_CERT, "https://identitysso-cert.betfair.com/api/"),
        (EndpointType.NAVIGATION, "https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json"),
        (EndpointType.HEARTBEAT, "https://api.betfair.com/exchange/heartbeat/json-rpc/v1/"),
        (EndpointType.ACCOUNTS, "https://api.betfair.com/exchange/account/json-rpc/v1/"),
        (EndpointType.BETTING, "https://api.betfair.com/exchange/betting/json-rpc/v1/"),
        (EndpointType.SCORES, "https://api.betfair.com/exchange/scores/json-rpc/v1/"),
    ],
)
def test_url_for_request(endpoint_type: EndpointType, base_url: str):
    assert endpoint().url_for_request(_StubRequest(endpoint_type)) == f"{base_url}TestOperation"


def test_url_for_request_unknown_endpoint_type():
    with pytest.raises(ValueError, match="Unknown endpoint type"):
        endpoint().url_for_request(_StubRequest(EndpointType.NONE))


@pytest.mark.parametrize(
    ("country_code", "identity_url"),
    [
        ("GBR", "https://identitysso.betfair.com/api/"),
        ("ESP", "https://identitysso.betfair.es/api/"),
        ("ITA", "https://identitysso.betfair.it/api/"),
        ("SWE", "https://identitysso.betfair.se/api/"),
    ],
)
def test_endpoint_country_codes(country_code: str, identity_url: str):
    config = endpoint(country_code)
    assert config.identity == identity_url


def test_endpoint_integration_stream():
    assert endpoint().stream == "ndjson://stream-api.betfair.com:443"
    assert endpoint(integration=True).stream == "ndjson://stream-api-integration.betfair.com:443"
