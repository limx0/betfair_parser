import json

import msgspec
import pytest

from betfair_parser.core import STREAM_DECODER, parse, read_file
from betfair_parser.spec.streaming import MCM, OCM
from betfair_parser.spec.streaming.mcm import RunnerStatus, StartingPriceLay
from betfair_parser.spec.streaming.ocm import MatchedOrder
from tests.unit.conftest import RESOURCES_DIR
from tests.resources import id_from_path


def test_read_file_example1():
    fn = RESOURCES_DIR / "data/1.185781277.bz2"
    data = list(read_file(fn))
    assert len(data) == 7600


def test_read_file_example2():
    fn = RESOURCES_DIR / "data/1.205822330.bz2"
    data = list(read_file(fn))
    assert len(data) == 5654


@pytest.mark.parametrize("fn", list(map(str, (RESOURCES_DIR / "streaming").glob("*.json"))), ids=id_from_path)
def test_streaming_files(fn):
    line = open(fn, "rb").read()
    data = msgspec.json.decode(line)
    if isinstance(data, list):
        for line in data:
            data = STREAM_DECODER.decode(msgspec.json.encode(line))
            assert data
    else:
        try:
            data = STREAM_DECODER.decode(line)
            assert data
        except (msgspec.DecodeError, msgspec.ValidationError) as e:
            print("ERR", e)
            print(msgspec.json.decode(line))
            raise e


def test_ocm():
    raw = (
        b'{"op":"ocm","id":2,"clk":"AAAAAAAAAAAAAA==","pt":1669350204489,"oc":[{"id":"1.206818134","fullImage":true,'
        b'"orc":[{"id":49914337,"fullImage":true,"uo":[],"mb":[],"ml":[[2, 100]]}]}]}'
    )
    ocm: OCM = STREAM_DECODER.decode(raw)
    assert isinstance(ocm, OCM)
    assert ocm.oc[0].orc[0].ml[0] == MatchedOrder(price=2.0, size=100)


def test_mcm():
    raw = (
        b'{"op":"mcm","id":1,"clk":"AKO0qwIAjoPCAgCmkeIC","pt":1634070799115,"mc":[{"id":"1.189081501",'
        b'"marketDefinition":{"marketId":"1.189081501","bspMarket":false,"turnInPlayEnabled":true,'
        b'"persistenceEnabled":true,"marketBaseRate":null,"eventId":"30999984","eventTypeId":"7522",'
        b'"numberOfWinners":1,"eventName":"Detroit Pistons @ New York Knicks","countryCode":"GB",'
        b'"bettingType":"ODDS","marketType":"MATCH_ODDS","marketTime":"2021-10-13T23:40:00.000Z",'
        b'"suspendTime":"2021-10-13T23:40:00.000Z","bspReconciled":false,"complete":true,"inPlay":false,'
        b'"crossMatching":false,"runnersVoidable":false,"numberOfActiveRunners":0,"betDelay":5,"status":"CLOSED",'
        b'"runners":[{"id":237474,"name":"Detroit Pistons","hc":0.0,"sortPriority":1,"status":"LOSER"},'
        b'{"id":237482,"name":"New York Knicks","hc":0.0,"sortPriority":2,"status":"WINNER"}],"regulators":["MR_INT"],'
        b'"discountAllowed":null,"timezone":"GMT","openDate":"2021-10-13T23:40:00.000Z","version":4099822530,'
        b'"priceLadderDefinition":"CLASSIC"}}]}'
    )
    mcm: MCM = STREAM_DECODER.decode(raw)
    assert isinstance(mcm, MCM)
    assert mcm.mc[0].marketDefinition.runners[0].hc == 0.0
    assert mcm.mc[0].marketDefinition.runners[0].handicap == "0.0"
    assert mcm.mc[0].marketDefinition.runners[0].id == 237474
    assert mcm.mc[0].marketDefinition.runners[0].selectionId is None
    assert mcm.mc[0].marketDefinition.runners[0].runner_id == 237474


def test_mcm_no_missing_fields():
    raw = {
        "op": "mcm",
        "clk": "7977927644",
        "pt": 1541992250576,
        "mc": [
            {
                "id": "1.147666818",
                "marketDefinition": {
                    "bspMarket": False,
                    "turnInPlayEnabled": True,
                    "persistenceEnabled": True,
                    "marketBaseRate": 5.0,
                    "eventId": "28045743",
                    "eventTypeId": "4",
                    "numberOfWinners": 1,
                    "bettingType": "ODDS",
                    "marketType": "TOURNAMENT_WINNER",
                    "marketTime": "2018-11-30T23:40:00.000Z",
                    "suspendTime": "2018-11-30T23:40:00.000Z",
                    "bspReconciled": False,
                    "complete": True,
                    "inPlay": False,
                    "crossMatching": False,
                    "runnersVoidable": False,
                    "numberOfActiveRunners": 8,
                    "betDelay": 0,
                    "status": "OPEN",
                    "runners": [
                        {
                            "status": "ACTIVE",
                            "sortPriority": 1,
                            "id": 12217371,
                            "name": "Perth Scorchers WBBL",
                        },
                        {
                            "status": "ACTIVE",
                            "sortPriority": 2,
                            "id": 12217558,
                            "name": "Sydney Sixers WBBL",
                        },
                        {
                            "status": "ACTIVE",
                            "sortPriority": 3,
                            "id": 12215567,
                            "name": "Adelaide Strikers WBBL",
                        },
                        {
                            "status": "ACTIVE",
                            "sortPriority": 4,
                            "id": 12217241,
                            "name": "Sydney Thunder WBBL",
                        },
                        {
                            "status": "ACTIVE",
                            "sortPriority": 5,
                            "id": 12217559,
                            "name": "Brisbane Heat WBBL",
                        },
                        {
                            "status": "ACTIVE",
                            "sortPriority": 6,
                            "id": 12217370,
                            "name": "Hobart Hurricanes WBBL",
                        },
                        {
                            "status": "ACTIVE",
                            "sortPriority": 7,
                            "id": 12215569,
                            "name": "Melbourne Renegades WBBL",
                        },
                        {
                            "status": "ACTIVE",
                            "sortPriority": 8,
                            "id": 12217242,
                            "name": "Melbourne Stars WBBL",
                        },
                    ],
                    "regulators": ["MR_INT"],
                    "countryCode": "AU",
                    "discountAllowed": False,
                    "timezone": "Australia/Sydney",
                    "openDate": "2017-12-09T02:45:00.000Z",
                    "version": 2511916192,
                    "name": "Winner 2018/19",
                    "eventName": "WBBL",
                },
                "rc": [],
                "con": True,
                "img": False,
            }
        ],
    }
    mcm: MCM = STREAM_DECODER.decode(msgspec.json.encode(raw))
    data = msgspec.json.decode(msgspec.json.encode(mcm))
    result = set(data["mc"][0]["marketDefinition"].keys())
    expected = set(raw["mc"][0]["marketDefinition"].keys())
    assert expected - result == set()


def test_mcm_no_clk():
    raw = b'{"op": "mcm", "clk": null, "pt": 1576840503572, "mc": []}'  # noqa
    mcm: MCM = STREAM_DECODER.decode(raw)
    assert mcm.clk is None


def test_mcm_market_definition_each_way():
    raw = b'{"op":"mcm","clk":"5900908932","pt":1652976054034,"mc":[{"id":"1.199318717","marketDefinition":{"bspMarket":false,"turnInPlayEnabled":true,"persistenceEnabled":true,"marketBaseRate":5.0,"eventId":"31466188","eventTypeId":"7","numberOfWinners":2,"eachWayDivisor":4.0,"bettingType":"ODDS","marketType":"EACH_WAY","marketTime":"2022-05-20T18:03:00.000Z","suspendTime":"2022-05-20T18:03:00.000Z","bspReconciled":false,"complete":true,"inPlay":false,"crossMatching":false,"runnersVoidable":false,"numberOfActiveRunners":7,"betDelay":0,"status":"OPEN","runners":[{"adjustmentFactor":20.67,"status":"ACTIVE","sortPriority":1,"id":14766968,"name":"Militia"},{"adjustmentFactor":18.37,"status":"ACTIVE","sortPriority":2,"id":38218050,"name":"Mellys Flyer"},{"adjustmentFactor":16.49,"status":"ACTIVE","sortPriority":3,"id":13118864,"name":"John Kirkup"},{"adjustmentFactor":16.49,"status":"ACTIVE","sortPriority":4,"id":18267118,"name":"Glory Fighter"},{"adjustmentFactor":12.46,"status":"ACTIVE","sortPriority":5,"id":28562926,"name":"Isle Of Lismore"},{"adjustmentFactor":12.46,"status":"ACTIVE","sortPriority":6,"id":10058014,"name":"Dark Shot"},{"adjustmentFactor":3.03,"status":"ACTIVE","sortPriority":7,"id":5704647,"name":"Duke Of Firenze"}],"regulators":["MR_INT"],"venue":"Catterick","countryCode":"GB","discountAllowed":false,"timezone":"Europe/London","openDate":"2022-05-20T16:20:00.000Z","version":4565022575,"name":"Each Way","eventName":"Catterick 20th May"},"rc":[],"con":true,"img":false}]}'  # noqa
    mcm: MCM = STREAM_DECODER.decode(raw)
    assert mcm.mc[0].marketDefinition.marketType == "EACH_WAY"
    assert mcm.mc[0].marketDefinition.eachWayDivisor == 4.0


def test_bsp_data():
    lines = json.loads((RESOURCES_DIR / "streaming/streaming_bsp_data.json").read_text())
    # for line in lines:
    #     raw = msgspec.json.encode(line)
    #     mcm: MCM = parse(raw)
    # for mc in mcm.mc:
    #     for rc in mc.rc:
    #         print(rc.spb, rc.spl, rc.spf, rc.spn)

    mcm = parse(msgspec.json.encode(lines[0]))
    rc = mcm.mc[0].rc[0]
    assert rc.spl == [StartingPriceLay(price=1.01, volume=2.8)]
    assert rc.spn == 4.5


def test_bsp_result():
    r = b'{"op":"mcm","id":1,"clk":"ANjxBACiiQQAlpQD","pt":1672131753550,"mc":[{"id":"1.208011084","marketDefinition":{"bspMarket":true,"turnInPlayEnabled":false,"persistenceEnabled":false,"marketBaseRate":7,"eventId":"31987078","eventTypeId":"4339","numberOfWinners":1,"bettingType":"ODDS","marketType":"WIN","marketTime":"2022-12-27T09:00:00.000Z","suspendTime":"2022-12-27T09:00:00.000Z","bspReconciled":true,"complete":true,"inPlay":false,"crossMatching":false,"runnersVoidable":false,"numberOfActiveRunners":0,"betDelay":0,"status":"CLOSED","settledTime":"2022-12-27T09:02:21.000Z","runners":[{"status":"WINNER","sortPriority":1,"bsp":2.0008034621107256,"id":45967562},{"status":"LOSER","sortPriority":2,"bsp":5.5,"id":45565847},{"status":"LOSER","sortPriority":3,"bsp":9.2,"id":47727833},{"status":"LOSER","sortPriority":4,"bsp":166.61668896346615,"id":47179469},{"status":"LOSER","sortPriority":5,"bsp":44,"id":51247493},{"status":"LOSER","sortPriority":6,"bsp":32,"id":42324350},{"status":"LOSER","sortPriority":7,"bsp":7.4,"id":51247494},{"status":"LOSER","sortPriority":8,"bsp":32.28604557164013,"id":48516342}],"regulators":["MR_INT"],"venue":"Warragul","countryCode":"AU","discountAllowed":true,"timezone":"Australia/Sydney","openDate":"2022-12-27T07:46:00.000Z","version":4968605121,"priceLadderDefinition":{"type":"CLASSIC"}}}]}'  # noqa
    mcm = parse(r)
    runners = mcm.mc[0].marketDefinition.runners
    assert runners[0].bsp == 2.0008034621107256
    assert runners[0].status == RunnerStatus.WINNER
