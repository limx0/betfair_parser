import datetime

import pytest

from betfair_parser.endpoints import endpoint
from betfair_parser.spec.common import decode
from betfair_parser.spec.navigation import Menu, Navigation, flatten_nav_tree
from tests.resources import RESOURCES_DIR


def test_navigation_request():
    url = endpoint("ITA").url_for_request(Menu)
    assert url.endswith("/betting/rest/v1/it/navigation/menu.json")


@pytest.fixture(scope="module")  # Frozen anyways, no need to recreate
def navigation_root() -> Navigation:
    raw = RESOURCES_DIR.joinpath("responses/navigation_menu.json").read_bytes()
    return decode(raw, type=Navigation)


def test_navigation(navigation_root):
    assert isinstance(navigation_root, Navigation)
    assert len(navigation_root.children) == 28


def test_navigation_flatten(navigation_root):
    markets = flatten_nav_tree(navigation_root)
    assert len(markets) == 13227
    market = markets[1450].to_dict()
    expected = {
        "event_type_name": "Greyhound Racing",
        "event_type_id": 4339,
        "event_name": None,
        "event_id": None,
        "event_country_code": None,
        "market_name": "B2 450m",
        "market_id": "1.180709069",
        "market_exchange_id": "1",
        "market_market_type": "WIN",
        "market_market_start_time": datetime.datetime(2021, 3, 17, 19, 56, tzinfo=datetime.timezone.utc),
        "market_number_of_winners": 1,
        "group_name": None,
        "group_id": None,
        "race_name": "B2 450m",
        "race_id": "30360080.1956",
        "race_country_code": "GB",
        "race_venue": "Doncaster",
        "race_start_time": datetime.datetime(2021, 3, 17, 19, 56, tzinfo=datetime.timezone.utc),
        "race_race_number": None,
    }
    assert market == expected

    for mkt in markets:
        if mkt.event_id:
            assert isinstance(mkt.event_id, int)
        assert isinstance(mkt.market_market_start_time, datetime.datetime)
