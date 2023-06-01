import functools
import os

import pytest

from betfair_parser import client
from betfair_parser.exceptions import AccountAPINGException
from betfair_parser.spec import heartbeat, navigation, race_status
from betfair_parser.spec.accounts import operations as ao, type_definitions as atd
from betfair_parser.spec.betting import enums as be, operations as bo, type_definitions as btd


@pytest.fixture(scope="module")
def appconfig():
    env = os.environ
    config = {
        "username": env.get("BF_USERNAME"),
        "password": env.get("BF_PASSWORD", "") + env.get("BF_TWOFACTOR_CODE", ""),
        "app_key": env.get("BF_APPKEY"),
        "cert_path": env.get("BF_CERTIFICATE"),
        "key_path": env.get("BF_CERTIFICATE_KEY"),
    }
    if not all(config[key] for key in ("username", "password", "app_key")):
        pytest.skip("Not all necessary login credentials were provided")
    return config


@pytest.fixture(scope="module")
def session():
    try:
        import requests  # noqa

        return requests.Session()
    except ImportError:
        try:
            import httpx

            return httpx.Client()
        except ImportError:
            pytest.skip("No suitable http library installed")


def skip_not_logged_in(test_func):
    __tracebackhide__ = True

    @functools.wraps(test_func)
    def test_func_wrapped(session, *args):
        if not session.headers.get("X-Authentication"):
            pytest.skip("session must be logged in")
        return test_func(session, *args)

    return test_func_wrapped


def test_login(session, appconfig):
    client.login(session, appconfig["username"], appconfig["password"], appconfig["app_key"])
    assert session.headers.get("X-Authentication")
    assert session.headers.get("X-Application")


@skip_not_logged_in
def test_keep_alive(session):
    client.keep_alive(session)


@skip_not_logged_in
def test_event_types(session):
    resp = client.request(session, bo.ListEventTypes.with_params(filter=btd.MarketFilter(text_query="Horse Racing")))
    assert len(resp) == 1
    assert resp[0].event_type.id == 7
    assert resp[0].event_type.name == "Horse Racing"


@skip_not_logged_in
def test_events(session):
    resp = client.request(session, bo.ListEvents.with_params(filter=btd.MarketFilter(text_query="Horse Racing")))
    assert len(resp) > 10
    assert all(isinstance(item, btd.EventResult) for item in resp)


@skip_not_logged_in
def test_market_catalogue(session):
    resp = client.request(
        session,
        bo.ListMarketCatalogue.with_params(
            filter=btd.MarketFilter(
                event_type_ids=[be.EventTypeIdCode.HORSE_RACING],
                market_type_codes=[be.MarketTypeCode.WIN],
                market_betting_types=[be.MarketBettingType.ODDS],
            ),
            market_projection=[
                be.MarketProjection.EVENT,
                be.MarketProjection.MARKET_DESCRIPTION,
                be.MarketProjection.RUNNER_DESCRIPTION,
                be.MarketProjection.RUNNER_METADATA,
            ],
            sort=be.MarketSort.FIRST_TO_START,
            max_results=100,
        ),
    )

    assert len(resp) <= 100
    for runner in resp[0].runners:
        assert runner.name
        assert runner.metadata
        assert runner.metadata.age


@skip_not_logged_in
def test_current_orders(session):
    resp = client.request(session, bo.ListCurrentOrders.with_params())
    assert len(resp.current_orders) == 0
    assert not resp.more_available


@skip_not_logged_in
def test_account_funds(session):
    resp = client.request(session, ao.GetAccountFunds.with_params())
    assert isinstance(resp, atd.AccountFundsResponse)
    assert resp.wallet.value == "UK"  # Only UK wallets left
    assert resp.available_to_bet_balance >= 0


@skip_not_logged_in
def test_account_funds_fail(session):
    with pytest.raises(AccountAPINGException) as exc_info:
        client.request(session, ao.GetAccountFunds.with_params(wallet="AUS"))

    err = exc_info.value
    assert "INVALID_PARAMETERS" in str(err)
    assert err.code.name == "INVALID_PARAMETERS"
    print(err)


@skip_not_logged_in
def test_navigation(session):
    menu = client.request(session, navigation.Menu())
    flattened = navigation.flatten_nav_tree(menu)
    assert len(flattened) > 5000


@skip_not_logged_in
def test_heartbeat(session):
    resp = client.request(session, heartbeat.Heartbeat.with_params(preferred_timeout_seconds=300))
    assert isinstance(resp, heartbeat.HeartbeatReport)
    assert resp.actual_timeout_seconds >= 0
    assert resp.action_performed in (heartbeat.ActionPerformed.NONE, heartbeat.ActionPerformed.ALL_BETS_CANCELLED)


@skip_not_logged_in
def test_race_status(session):
    resp = client.request(session, bo.ListEvents.with_params(filter=btd.MarketFilter(event_type_ids=[7])))
    event_ids = [ev_res.event.id for ev_res in resp[::10]]  # every 10th event
    details = client.request(session, race_status.ListRaceDetail.with_params(meeting_ids=event_ids))
    assert len(details) >= len(event_ids)  # There are more than one details / race_ids per event_id
    for d in details:
        assert d.meeting_id or d.race_id
        assert d.response_code
        if d.response_code == race_status.ResponseCode.OK:
            assert d.meeting_id
            assert d.race_id
            assert d.last_updated
            assert d.race_status


@skip_not_logged_in
def test_account_no_appkey(session):
    app_key = session.headers.pop("X-Application")
    with pytest.raises(AccountAPINGException) as exc_info:
        client.request(session, ao.GetAccountFunds.with_params())

    err = exc_info.value
    assert "NO_APP_KEY" in str(err.code)
    assert err.code.name == "NO_APP_KEY"
    session.headers["X-Application"] = app_key
    print(err)


@skip_not_logged_in
def test_logout(session):
    client.logout(session)
    assert not session.headers.get("X-Authentication")


@pytest.fixture(scope="module")
def cert_session(appconfig):
    cert_config = appconfig.get("cert_path"), appconfig.get("key_path")
    if not all(cert_config):
        pytest.skip("No certificate was provided")
    try:
        import requests  # noqa

        session = requests.Session()
        session.cert = cert_config
        return session
    except ImportError:
        try:
            import httpx

            return httpx.Client(transport=httpx.HTTPTransport(cert=cert_config))
        except ImportError:
            pytest.skip("No suitable http library installed")


def test_cert_login(cert_session, appconfig):
    client.cert_login(cert_session, appconfig["username"], appconfig["password"], appconfig["app_key"])
    assert cert_session.headers.get("X-Authentication")
    assert cert_session.headers.get("X-Application")
    client.logout(cert_session)
