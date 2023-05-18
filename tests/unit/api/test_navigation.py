import msgspec.json

from betfair_parser.spec.navigation import Navigation, navigation_to_flatten_markets
from tests.resources import read_test_file


def test_navigation():
    raw = read_test_file("responses/navigation_list_navigation.json")
    navigation: Navigation = msgspec.json.decode(raw, type=Navigation)
    assert len(navigation.children) == 28


def test_navigation_market_flatten_navigation():
    raw = read_test_file("responses/navigation_list_navigation.json")
    navigation: Navigation = msgspec.json.decode(raw, type=Navigation)
    markets = navigation_to_flatten_markets(navigation)
    assert len(markets) == 13227
    market = markets[1450].to_dict()
    expected = {
        "event_type_name": "Greyhound Racing",
        "event_type_id": "4339",
        "event_name": None,
        "event_id": None,
        "event_countryCode": None,
        "market_name": "B2 450m",
        "market_id": "1.180709069",
        "market_exchangeId": "1",
        "market_marketType": "WIN",
        "market_marketStartTime": "2021-03-17T19:56:00.000Z",
        "market_numberOfWinners": 1,
        "group_name": None,
        "group_id": None,
        "race_name": "B2 450m",
        "race_id": "30360080.1956",
        "race_countryCode": "GB",
        "race_venue": "Doncaster",
        "race_startTime": "2021-03-17T19:56:00Z",
        "race_raceNumber": None,
    }
    assert market == expected
