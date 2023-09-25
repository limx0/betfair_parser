from collections import defaultdict
from dataclasses import dataclass


ACCOUNTS = "https://api.betfair.com/exchange/account/json-rpc/v1/"
BETTING = "https://api.betfair.com/exchange/betting/json-rpc/v1/"
SCORES = "https://api.betfair.com/exchange/scores/json-rpc/v1/"
STREAM = "ndjson://stream-api.betfair.com:443"
STREAM_INTEGRATION = "ndjson://stream-api-integration.betfair.com:443"
SILKS = "https://content-cache.cdnppb.net/feeds_images/Horses/SilkColours/"

_IDENTITY = "https://identitysso.betfair{tld}/api/"
_IDENTITY_CERT = "https://identitysso-cert.betfair{tld}/api/"
_NAVIGATION = "https://api.betfair{tld}/exchange/betting/rest/v1/{locale}/navigation/menu.json"
_HEARTBEAT = "https://api.betfair{tld}/exchange/heartbeat/json-rpc/v1/"

IDENTITY = defaultdict(
    lambda: _IDENTITY.format(tld=".com"),
    ESP=_IDENTITY.format(tld=".es"),
    ITA=_IDENTITY.format(tld=".it"),
    ROU=_IDENTITY.format(tld=".ro"),
    SWE=_IDENTITY.format(tld=".se"),
    AUS=_IDENTITY.format(tld=".com.au"),
)
IDENTITY_CERT = defaultdict(
    lambda: _IDENTITY_CERT.format(tld=".com"),
    ESP=_IDENTITY_CERT.format(tld=".es"),
    ITA=_IDENTITY_CERT.format(tld=".it"),
    ROU=_IDENTITY_CERT.format(tld=".ro"),
    SWE=_IDENTITY_CERT.format(tld=".se"),
)
NAVIGATION = defaultdict(
    lambda: _NAVIGATION.format(tld=".com", locale="en"),
    ESP=_NAVIGATION.format(tld=".es", locale="es"),
    ITA=_NAVIGATION.format(tld=".it", locale="it"),
    DEU=_NAVIGATION.format(tld=".com", locale="de"),
    SWE=_NAVIGATION.format(tld=".com", locale="sv"),
    PRT=_NAVIGATION.format(tld=".com", locale="pt"),
    RUS=_NAVIGATION.format(tld=".com", locale="ru"),
    DNK=_NAVIGATION.format(tld=".com", locale="da"),
)
HEARTBEAT = defaultdict(
    lambda: _HEARTBEAT.format(tld=".com", locale="en"),
    ESP=_HEARTBEAT.format(tld=".es", locale="es"),
    ITA=_HEARTBEAT.format(tld=".it", locale="it"),
)


@dataclass(frozen=True)
class EndpointConfig:
    identity: str
    identity_cert: str
    navigation: str
    heartbeat: str
    stream: str
    accounts = ACCOUNTS
    betting = BETTING
    scores = SCORES

    def for_request(self, req):
        return getattr(self, req.endpoint_type.value)

    def url_for_request(self, req):
        return f"{self.for_request(req)}{req.method}"


def endpoint(country_code="GBR", integration=False):
    return EndpointConfig(
        identity=IDENTITY[country_code],
        identity_cert=IDENTITY_CERT[country_code],
        navigation=NAVIGATION[country_code],
        heartbeat=HEARTBEAT[country_code],
        stream=STREAM_INTEGRATION if integration else STREAM,
    )


ENDPOINTS = endpoint()
