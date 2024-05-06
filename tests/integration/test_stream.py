import datetime

import pytest
from requests import Session  # alternatively use httpx.Client

from betfair_parser import client
from betfair_parser.cache import MarketDefinition, RunnerOrderBook
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
from betfair_parser.stream import AsyncStream, ExchangeStream, StreamReader, changed_markets, create_stream_io
from tests.integration.test_live import appconfig  # noqa: F401


@pytest.fixture(scope="module")
def session(appconfig) -> Session:  # noqa
    s = Session()
    try:
        client.login(s, appconfig["username"], appconfig["password"], appconfig["app_key"])
    except BetfairError:
        pytest.skip("session could not be logged in")
    return s


MARKET_STREAM_ID = 1
ORDER_STREAM_ID = 2
SUBSCRIPTIONS = [
    MarketSubscription(
        id=MARKET_STREAM_ID,
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
    OrderSubscription(id=ORDER_STREAM_ID, heartbeat_ms=500, order_filter=OrderFilter()),
]


@pytest.mark.parametrize(
    "subscription",
    SUBSCRIPTIONS,
    ids=lambda x: type(x).__name__,
)
def test_stream(session, subscription, iterations=3):
    app_key = session.headers.get("X-Application")
    token = session.headers.get("X-Authentication")
    esm = ExchangeStream(app_key, token)

    with create_stream_io(STREAM_INTEGRATION) as stream:
        print(esm.receive(stream))  # read connection
        stream.write(esm.connect())  # send auth
        print(esm.receive(stream))

        stream.write(esm.subscribe(subscription))
        msg: Status = esm.receive(stream)
        assert isinstance(msg, Status)
        assert not msg.is_error, f"{msg.error_code.name}: {msg.error_message}"
        assert not msg.connection_closed
        assert msg.id == subscription.id

        print(subscription)
        print(msg)

        req_type = MCM if isinstance(subscription, MarketSubscription) else OCM
        for _ in range(iterations):
            msg = esm.receive(stream)
            assert isinstance(msg, req_type)
            print(msg)


@pytest.mark.parametrize(
    "subscription",
    SUBSCRIPTIONS,
    ids=lambda x: type(x).__name__,
)
@pytest.mark.asyncio
async def test_stream_async(session, subscription, iterations=3):
    token = session.headers.get("X-Authentication")
    app_key = session.headers.get("X-Application")
    esm = ExchangeStream(app_key, token)

    async with AsyncStream(STREAM_INTEGRATION) as stream:
        esm.receive_bytes(await stream.readline())
        await stream.write(esm.connect())
        esm.receive_bytes(await stream.readline())
        await stream.write(esm.subscribe(subscription))

        msg: Status = esm.receive_bytes(await stream.readline())
        assert isinstance(msg, Status)
        assert not msg.is_error, f"{msg.error_code.name}: {msg.error_message}"
        assert not msg.connection_closed
        assert msg.id == subscription.id

        print(subscription)
        print(msg)

        req_type = MCM if isinstance(subscription, MarketSubscription) else OCM
        for _ in range(iterations):
            msg = esm.receive_bytes(await stream.readline())
            assert isinstance(msg, req_type)
            print(msg)


def test_stream_reader(session, iterations=15):
    app_key = session.headers.get("X-Application")
    token = session.headers.get("X-Authentication")

    sr = StreamReader(app_key, token)
    for subscription in SUBSCRIPTIONS:
        sr.subscribe(subscription)  # type: ignore[arg-type]

    with create_stream_io(STREAM_INTEGRATION) as stream:
        for i, change_msg in enumerate(sr.iter_changes(stream)):
            changed_ids = changed_markets(change_msg)
            if not changed_ids:
                continue
            assert all(change_id.startswith("1.") for change_id in changed_ids)
            assert all(change_id in sr.caches[MARKET_STREAM_ID].order_book for change_id in changed_ids)  # type: ignore[union-attr]
            if i >= iterations:
                break

    assert sr.caches[ORDER_STREAM_ID].orders is not None  # type: ignore[union-attr]

    market_definitions: dict[str, MarketDefinition] = sr.caches[MARKET_STREAM_ID].definitions  # type: ignore[union-attr]
    assert len(market_definitions) > 20
    assert all(isinstance(key, str) for key in market_definitions)
    assert all(isinstance(md, MarketDefinition) for md in market_definitions.values())

    now = datetime.datetime.utcnow().astimezone(datetime.timezone.utc)
    order_book = sr.caches[MARKET_STREAM_ID].order_book  # type: ignore[union-attr]
    assert len(order_book) == len(market_definitions)
    assert all(isinstance(key, str) for key in order_book)
    for market_id, market_order_book in order_book.items():
        if (market_definitions[market_id].suspend_time - now).seconds > 6 * 60 * 60:  # 6h
            # data further in the future is likely to be incomplete and leads to errors
            continue
        for runner_order_book in market_order_book.values():
            assert isinstance(runner_order_book, RunnerOrderBook)
            if not runner_order_book.total_volume:
                # skip empty order books
                continue
            assert runner_order_book.available_to_back or runner_order_book.available_to_lay[1.01]
            assert runner_order_book.available_to_lay or runner_order_book.available_to_back[1000]
            assert runner_order_book.last_traded_price

            # fields must be deleted when nulled
            for volume in runner_order_book.available_to_back.values():
                assert volume
            for volume in runner_order_book.available_to_lay.values():
                assert volume
