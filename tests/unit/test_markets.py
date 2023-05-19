import msgspec.json
import pytest

from betfair_parser.spec.betting.type_definitions import MarketCatalogue, RunnerCatalog
from betfair_parser.spec.common import decode, encode
from tests.resources import assert_json_equal, read_test_file


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
    runner: RunnerCatalog = msgspec.json.decode(msgspec.json.encode(data), type=RunnerCatalog)
    assert runner.runnerName == data["runnerName"]
    assert runner.handicap == data["handicap"]
    assert runner.sortPriority == data["sortPriority"]
    assert runner.runner_name == data["runnerName"]
    assert runner.runner_id == int(data["metadata"]["runnerId"])


def test_market_catalogue():
    raw = read_test_file("responses/betting/list_market_catalogue.json")
    catalog = decode(raw, type=list[MarketCatalogue])
    assert len(catalog) == 12035
    expected = {
        "marketId": "1.180697651",
        "marketName": "First Half Goals 2.5",
        "marketStartTime": "2021-03-19T19:00:00.000Z",
        "description": {
            "persistenceEnabled": True,
            "bspMarket": False,
            "marketTime": "2021-03-19T19:00:00.000Z",
            "suspendTime": "2021-03-19T19:00:00.000Z",
            "settleTime": None,
            "bettingType": "ODDS",
            "turnInPlayEnabled": True,
            "marketType": "FIRST_HALF_GOALS_25",
            "regulator": "MALTA LOTTERIES AND GAMBLING AUTHORITY",
            "marketBaseRate": 5.0,
            "discountAllowed": True,
            "wallet": "UK wallet",
            "rules": "<!--Football - First Half Goals --><br>How many goals will be scored in this first half of this match?\xa0<br> All bets apply to Full Time according to the match officials, plus any stoppage time. Extra-time/penalty shoot-outs are not included.<br><br></b>For further information please see <a href=http://content.betfair.com/aboutus/content.asp?sWhichKey=Rules%20and%20Regulations#undefined.do style=color:0163ad; text-decoration: underline; target=_blank>Rules & Regs<br><br>\n",  # noqa
            "rulesHasDate": True,
            "priceLadderDescription": {"type": "CLASSIC"},
            "lineRangeInfo": None,
            "eachWayDivisor": None,
            "clarifications": None,
            "raceType": None,
        },
        "totalMatched": 0.0,
        "runners": [
            {
                "selectionId": 47972,
                "runnerName": "Under 2.5 Goals",
                "sortPriority": 1,
                "handicap": 0.0,
                "metadata": {"runnerId": "47972"},
            },
            {
                "selectionId": 47973,
                "runnerName": "Over 2.5 Goals",
                "sortPriority": 2,
                "handicap": 0.0,
                "metadata": {"runnerId": "47973"},
            },
        ],
        "eventType": {"id": 1, "name": "Soccer"},
        "event": {
            "id": "30359506",
            "name": "Almere City v Den Bosch",
            "timezone": "GMT",
            "openDate": "2021-03-19T19:00:00.000Z",
            "countryCode": "NL",
            "venue": None,
        },
        "competition": {"id": "11", "name": "Dutch Eerste Divisie"},
    }
    result = decode(encode(catalog[5000]))
    assert_json_equal(result, expected)
