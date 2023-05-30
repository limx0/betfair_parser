import os

import pytest

from betfair_parser import client
from betfair_parser.spec.betting import operations, type_definitions


@pytest.fixture(scope="module")
def appconfig():
    env = os.environ
    config = {
        "username": env.get("BF_USERNAME"),
        "password": env.get("BF_PASSWORD", "") + env.get("BF_TWOFACTOR_CODE", ""),
        "app_key": env.get("BF_APPKEY"),
    }
    if not all(config.values()):
        pytest.skip("Not all login credentials were provided")
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


def xfail_not_logged_in(session):
    if not session.headers.get("X-Authentication"):
        pytest.xfail("session must be logged in")


def test_login(session, appconfig):
    client.login(session, appconfig["username"], appconfig["password"], appconfig["app_key"])
    assert session.headers.get("X-Authentication")
    assert session.headers.get("X-Application")


def test_keep_alive(session):
    xfail_not_logged_in(session)
    client.keep_alive(session)


def test_event_types(session):
    xfail_not_logged_in(session)
    resp = client.request(
        session, operations.ListEventTypes.with_params(filter=type_definitions.MarketFilter(text_query="Horse Racing"))
    )
    assert len(resp) == 1
    assert resp[0].event_type.id == 7
    assert resp[0].event_type.name == "Horse Racing"


def test_events(session):
    xfail_not_logged_in(session)
    resp = client.request(
        session, operations.ListEvents.with_params(filter=type_definitions.MarketFilter(text_query="Horse Racing"))
    )
    assert len(resp) > 10
    assert all(isinstance(item, type_definitions.EventResult) for item in resp)
