import msgspec.json
import pytest

from betfair_parser.spec.api.markets import Runner
from betfair_parser.spec.api.navigation import flatten_navigation
from tests.resources import read_test_file


@pytest.mark.parametrize(
    "raw",
    [
        read_test_file("responses/navigation_list_navigation.json"),
    ],
)
def test_navigation_market_flatten_navigation(raw):
    data = msgspec.json.decode(raw)
    assert data
    markets = flatten_navigation(raw)
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
        "race_startTime": "2021-03-17T19:56:00.000Z",
        "race_raceNumber": None,
    }
    assert market == expected


@pytest.mark.parametrize(
    "data",
    [
        {
            "selectionId": 40274538,
            "runnerName": "Philadelphia 76ers",
            "handicap": 0.0,
            "sortPriority": 1,
            "metadata": {"runnerId": "40274538"},
        },
        {
            "selectionId": 50758919,
            "runnerName": "1. Gentacheeva",
            "handicap": 0.0,
            "sortPriority": 1,
            "metadata": {
                "runnerId": "50758919",
            },
        },
    ],
)
def test_runner_name(data):
    runner: Runner = msgspec.json.decode(msgspec.json.encode(data), type=Runner)
    assert runner.runnerName == data["runnerName"]
    assert runner.handicap == data["handicap"]
    assert runner.sortPriority == data["sortPriority"]
    assert runner.runner_name == data["runnerName"]
    assert runner.runner_id == int(data["metadata"]["runnerId"])


# @pytest.mark.parametrize(
#     "raw",
#     [
#         read_test_file("responses/betting_list_market_catalogue.json"),
#     ]
# )
# @pytest.mark.skip(reason="not implemented")
# def test_market_catalogue(raw):
#     catalog = msgspec.json.decode(raw, type=MarketCatalog)
#     assert catalog.event_type_name == ""
