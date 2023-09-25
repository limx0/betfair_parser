import pytest
from requests import Session  # alternatively use httpx.Client

from betfair_parser import client
from betfair_parser.endpoints import STREAM_INTEGRATION
from betfair_parser.exceptions import BetfairError
from betfair_parser.spec.common import EventTypeIdCode
from betfair_parser.spec.streaming import (
    MCM,
    OCM,
    MarketBettingType,
    MarketDataFilter,
    MarketDataFilterFields,
    MarketFilter,
    MarketSubscription,
    MarketTypeCode,
    OrderFilter,
    OrderSubscription,
    Status,
)
from betfair_parser.stream import AsyncStream, Stream
from tests.integration.test_live import appconfig  # noqa: F401


@pytest.fixture(scope="module")
def session(appconfig) -> Session:  # noqa
    s = Session()
    try:
        client.login(s, appconfig["username"], appconfig["password"], appconfig["app_key"])
    except BetfairError:
        pytest.skip("session could not be logged in")
    return s


SUBSCRIPTIONS = [
    MarketSubscription(
        id=1,
        heartbeat_ms=500,
        market_filter=MarketFilter(
            betting_types=[MarketBettingType.ODDS],
            event_type_ids=[EventTypeIdCode.HORSE_RACING],
            country_codes=["GB", "IE"],
            market_types=[MarketTypeCode.WIN],
        ),
        market_data_filter=MarketDataFilter(
            fields=[
                MarketDataFilterFields.EX_MARKET_DEF,
                MarketDataFilterFields.EX_ALL_OFFERS,
                MarketDataFilterFields.EX_LTP,
                MarketDataFilterFields.EX_TRADED_VOL,
            ],
        ),
    ),
    OrderSubscription(id=2, heartbeat_ms=500, order_filter=OrderFilter()),
]


@pytest.mark.parametrize(
    "subscription",
    SUBSCRIPTIONS,
    ids=lambda x: type(x).__name__,
)
def test_stream(session, subscription, iterations=3):
    token = session.headers.get("X-Authentication")
    app_key = session.headers.get("X-Application")

    with Stream(STREAM_INTEGRATION) as strm:
        strm.authenticate(app_key, token)
        strm.send(subscription)
        msg: Status = strm.receive()
        assert isinstance(msg, Status)
        assert not msg.is_error, f"{msg.error_code.name}: {msg.error_message}"
        assert not msg.connection_closed
        assert msg.id == subscription.id

        print(subscription)
        print(msg)

        req_type = MCM if isinstance(subscription, MarketSubscription) else OCM
        for _ in range(iterations):
            msg = strm.receive()
            assert isinstance(msg, req_type)
            print(msg)


@pytest.mark.parametrize(
    "subscription",
    SUBSCRIPTIONS,
    ids=lambda x: type(x).__name__,
)
@pytest.mark.asyncio
async def test_async_stream(session, subscription, iterations=3):
    token = session.headers.get("X-Authentication")
    app_key = session.headers.get("X-Application")

    async with AsyncStream(STREAM_INTEGRATION) as strm:
        await strm.authenticate(app_key, token)
        await strm.send(subscription)
        msg: Status = await strm.receive()
        assert isinstance(msg, Status)
        assert not msg.is_error, f"{msg.error_code.name}: {msg.error_message}"
        assert not msg.connection_closed
        assert msg.id == subscription.id

        print(subscription)
        print(msg)

        req_type = MCM if isinstance(subscription, MarketSubscription) else OCM
        for _ in range(iterations):
            msg = await strm.receive()
            assert isinstance(msg, req_type)
            print(msg)
