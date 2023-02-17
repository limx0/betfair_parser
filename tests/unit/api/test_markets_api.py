import msgspec.json
import pytest

from betfair_parser.spec.api.markets import Runner


# @pytest.mark.parametrize(
#     "raw",
#     [
#         read_test_file("responses/navigation_list_navigation.json"),
#     ],
# )
# @pytest.mark.skip(reason="not implemented")
# def test_navigation_market(raw):
#     nav = msgspec.json.decode(raw, type=NavigationMarket)
#     assert nav.event_type_name == ""


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
