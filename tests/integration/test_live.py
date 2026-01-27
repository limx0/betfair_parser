import functools
import os

import pytest
from requests import Session  # alternatively use httpx.Client

from betfair_parser import client
from betfair_parser.exceptions import AccountAPINGException
from betfair_parser.spec import accounts, betting, heartbeat, navigation, race_status


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
def session() -> Session:
    return Session()


def skip_not_logged_in(test_func):
    __tracebackhide__ = True

    @functools.wraps(test_func)
    def test_func_wrapped(session: Session, *args, **kwargs):
        if not session.headers.get("X-Authentication"):
            pytest.skip("session must be logged in")
        return test_func(session, *args, **kwargs)

    return test_func_wrapped


def test_login(session: Session, appconfig):
    client.login(session, appconfig["username"], appconfig["password"], appconfig["app_key"])
    assert session.headers.get("X-Authentication")
    assert session.headers.get("X-Application")


@skip_not_logged_in
def test_keep_alive(session: Session):
    client.keep_alive(session)


@skip_not_logged_in
def test_account_details(session: Session):
    resp = client.request(session, accounts.GetAccountDetails.with_params())
    assert isinstance(resp, accounts.AccountDetailsResponse)
    assert 0 <= resp.discount_rate < 0.3
    assert resp.currency_code
    assert resp.region
    assert resp.timezone  # Should we check for UTC here?
    assert resp.first_name
    assert resp.last_name


@skip_not_logged_in
def test_account_funds(session: Session):
    resp = client.request(session, accounts.GetAccountFunds.with_params())
    assert isinstance(resp, accounts.AccountFundsResponse)
    assert resp.wallet.value == "UK"  # Only UK wallets left
    assert resp.available_to_bet_balance >= 0
    assert resp.retained_commission >= 0
    assert resp.exposure <= 0  # always returned negative
    assert resp.exposure_limit <= 0  # always returned negative
    assert 0 <= resp.discount_rate <= 0.3
    assert resp.points_balance >= 0


@skip_not_logged_in
def test_account_funds_fail(session: Session):
    with pytest.raises(AccountAPINGException) as exc_info:
        client.request(session, accounts.GetAccountFunds.with_params(wallet="AUS"))

    err = exc_info.value
    assert str(err) == "INVALID_PARAMETERS: Problem parsing the parameters, or a mandatory parameter was not found"
    assert err.code.name == "INVALID_PARAMETERS"


@skip_not_logged_in
def test_event_types(session: Session):
    resp: list[betting.EventTypeResult] = client.request(
        session, betting.ListEventTypes.with_params(filter=betting.MarketFilter(text_query="Horse Racing"))
    )
    assert len(resp) == 1
    horse_racing = resp[0]
    assert horse_racing.event_type.id == 7
    assert horse_racing.event_type.name == "Horse Racing"
    assert horse_racing.market_count > 100
    print(f"Found {horse_racing.market_count} horse racing markets")


@skip_not_logged_in
def test_market_types(session: Session):
    resp: list[betting.MarketTypeResult] = client.request(
        session,
        betting.ListMarketTypes.with_params(
            filter=betting.MarketFilter(event_type_ids={betting.EventTypeIdCode.SOCCER})
        ),
    )
    assert len(resp), "No market types found"
    assert len(resp) > 20
    print(f"Found {len(resp)} soccer market types")
    market_types = [result.market_type for result in resp]
    print(market_types)


@skip_not_logged_in
def test_countries(session: Session):
    resp: list[betting.CountryCodeResult] = client.request(
        session,
        betting.ListCountries.with_params(filter=betting.MarketFilter(event_type_ids={betting.EventTypeIdCode.SOCCER})),
    )
    assert len(resp), "No countries found"
    assert len(resp) > 10
    print(f"Found {len(resp)} countries with soccer markets")

    for result in sorted(resp, key=lambda r: r.market_count, reverse=True):
        assert isinstance(result.country_code, str)
        assert isinstance(result.market_count, int)
        print(result)


@skip_not_logged_in
def test_competitions(session: Session):
    resp: list[betting.CompetitionResult] = client.request(
        session,
        betting.ListCompetitions.with_params(
            filter=betting.MarketFilter(event_type_ids={betting.EventTypeIdCode.SOCCER})
        ),
    )
    assert len(resp), "No football competitions found"
    print(f"Found {len(resp)} soccer competitions")

    for result in sorted(resp, key=lambda r: r.market_count, reverse=True):
        assert isinstance(result, betting.CompetitionResult)
        assert result.market_count
        assert isinstance(result.competition, betting.Competition)
        assert result.competition.id
        assert result.competition.name
        print(result)


@skip_not_logged_in
def test_events(session: Session):
    resp: list[betting.EventResult] = client.request(
        session,
        betting.ListEvents.with_params(
            filter=betting.MarketFilter(event_type_ids={betting.EventTypeIdCode.HORSE_RACING})
        ),
    )
    assert len(resp) > 10
    print(f"Found {len(resp)} UK horse racing events")
    for result in sorted(resp, key=lambda r: r.event.open_date):
        assert isinstance(result.event, betting.Event)
        assert result.event.name
        print(result.event)


@skip_not_logged_in
def test_market_catalogue_horseracing(session: Session):
    resp: list[betting.MarketCatalogue] = client.request(
        session,
        betting.ListMarketCatalogue.with_params(
            filter=betting.MarketFilter(
                event_type_ids={betting.EventTypeIdCode.HORSE_RACING},
                market_type_codes={betting.MarketTypeCode.WIN},
                market_betting_types={betting.MarketBettingType.ODDS},
                market_countries={"GB", "IE"},
            ),
            market_projection=[
                betting.MarketProjection.EVENT,
                betting.MarketProjection.MARKET_DESCRIPTION,
                betting.MarketProjection.RUNNER_DESCRIPTION,
                betting.MarketProjection.RUNNER_METADATA,
            ],
            sort=betting.MarketSort.FIRST_TO_START,
            max_results=100,
        ),
    )

    assert len(resp) <= 100
    print(resp[0])
    for runner in resp[0].runners:
        assert runner.name
        assert runner.metadata
        assert runner.metadata
        assert runner.metadata.cloth_number
        assert runner.metadata.colours_description


@skip_not_logged_in
def test_market_catalogue_football(session: Session):
    resp: list[betting.MarketCatalogue] = client.request(
        session,
        betting.ListMarketCatalogue.with_params(
            filter=betting.MarketFilter(
                event_type_ids={betting.EventTypeIdCode.SOCCER},
                market_type_codes={betting.MarketTypeCode.MATCH_ODDS, betting.MarketTypeCode.ASIAN_HANDICAP},
                market_betting_types={
                    betting.MarketBettingType.ODDS,
                    betting.MarketBettingType.ASIAN_HANDICAP_DOUBLE_LINE,
                },
                market_countries={"GB", "IE"},
                bet_delay_models={betting.BetDelayModel.PASSIVE},
            ),
            market_projection=[
                betting.MarketProjection.EVENT,
                betting.MarketProjection.MARKET_DESCRIPTION,
                betting.MarketProjection.RUNNER_DESCRIPTION,
            ],
            sort=betting.MarketSort.FIRST_TO_START,
            max_results=100,
        ),
    )

    assert len(resp) <= 100
    print(resp[0])
    for runner in resp[0].runners:
        assert runner.name
    for market in resp:
        if market.description.bet_delay_models:
            assert market.description.bet_delay_models


@skip_not_logged_in
def test_current_orders(session: Session):
    resp: betting.CurrentOrderSummaryReport = client.request(session, betting.ListCurrentOrders.with_params())
    assert not resp.more_available
    if len(resp.current_orders):
        for order in resp.current_orders:
            assert isinstance(order, betting.CurrentOrderSummary)
            assert order.bet_id
            assert order.market_id
            assert order.selection_id
            assert order.side in (betting.Side.BACK, betting.Side.LAY)
            assert 1 < order.price_size.price < 1001
            assert order.price_size.size > 0


@skip_not_logged_in
def test_navigation(session: Session):
    menu = client.request(session, navigation.Menu())
    assert isinstance(menu, navigation.Navigation)
    flattened = navigation.flatten_nav_tree(menu)
    assert len(flattened) > 5000


@skip_not_logged_in
def test_heartbeat(session: Session):
    resp = client.request(session, heartbeat.Heartbeat.with_params(preferred_timeout_seconds=300))
    assert isinstance(resp, heartbeat.HeartbeatReport)
    assert resp.actual_timeout_seconds >= 0
    assert resp.action_performed in (heartbeat.ActionPerformed.NONE, heartbeat.ActionPerformed.ALL_BETS_CANCELLED)


@skip_not_logged_in
def test_race_status(session: Session):
    resp = client.request(
        session,
        betting.ListEvents.with_params(
            filter=betting.MarketFilter(event_type_ids={betting.EventTypeIdCode.HORSE_RACING})
        ),
    )
    event_ids = [ev_res.event.id for ev_res in resp[::10]]  # every 10th event
    details = client.request(session, race_status.ListRaceDetails.with_params(meeting_ids=event_ids))
    assert len(details) >= len(event_ids)  # There are more than one details / race_ids per event_id
    for d in details:
        assert isinstance(d, race_status.RaceDetails)
        assert d.meeting_id or d.race_id
        assert d.response_code
        if d.response_code == race_status.ResponseCode.OK:
            assert d.meeting_id
            assert d.race_id
            assert d.last_updated
            assert d.race_status


@skip_not_logged_in
def test_account_no_appkey(session: Session):
    app_key = session.headers.pop("X-Application")
    with pytest.raises(AccountAPINGException) as exc_info:
        client.request(session, accounts.GetAccountFunds.with_params())

    err = exc_info.value
    assert "NO_APP_KEY" in str(err.code)
    assert str(err) == "NO_APP_KEY: An application key header ('X-Application') has not been provided in the request."
    assert err.code.name == "NO_APP_KEY"

    # restore the app key for further tests
    session.headers["X-Application"] = app_key


@skip_not_logged_in
def test_logout(session: Session):
    client.logout(session)
    assert not session.headers.get("X-Authentication")


@pytest.fixture(scope="module")
def cert_session(appconfig):
    cert_config = appconfig.get("cert_path"), appconfig.get("key_path")
    if not all(cert_config):
        pytest.skip("No certificate was provided")
    session = Session()
    session.cert = cert_config
    # alternatively: session = httpx.Client(transport=httpx.HTTPTransport(cert=cert_config))
    return session


def test_cert_login(cert_session, appconfig):
    client.cert_login(cert_session, appconfig["username"], appconfig["password"], appconfig["app_key"])
    assert cert_session.headers.get("X-Authentication")
    assert cert_session.headers.get("X-Application")
    client.logout(cert_session)
