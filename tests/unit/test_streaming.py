import msgspec

from betfair_parser.spec.streaming import MCM, OCM, stream_decode
from betfair_parser.spec.streaming.type_definitions import MatchedOrder, RunnerStatus, StartingPriceLay
from tests.resources import RESOURCES_DIR


def test_ocm():
    raw = (
        b'{"op":"ocm","id":2,"clk":"AAAAAAAAAAAAAA==","pt":1669350204489,"oc":[{"id":"1.206818134","fullImage":true,'
        b'"orc":[{"id":49914337,"fullImage":true,"uo":[],"mb":[],"ml":[[2, 100]]}]}]}'
    )
    ocm: OCM = stream_decode(raw)
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
    mcm: MCM = stream_decode(raw)
    assert isinstance(mcm, MCM)
    assert mcm.mc[0].market_definition.runners[0].hc == 0.0
    assert mcm.mc[0].market_definition.runners[0].handicap == "0.0"
    assert mcm.mc[0].market_definition.runners[0].id == 237474
    assert mcm.mc[0].market_definition.runners[0].runner_id == 237474


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
    mcm: MCM = stream_decode(msgspec.json.encode(raw))
    data = msgspec.json.decode(msgspec.json.encode(mcm))
    result = set(data["mc"][0]["marketDefinition"].keys())
    expected = set(raw["mc"][0]["marketDefinition"].keys())  # type: ignore
    assert expected - result == set()


def test_mcm_no_clk():
    raw = b'{"op": "mcm", "clk": null, "pt": 1576840503572, "mc": []}'  # noqa
    mcm: MCM = stream_decode(raw)
    assert mcm.clk is None


def test_mcm_market_definition_each_way():
    raw = (RESOURCES_DIR / "responses/streaming/mcm_market_definition_each_way.json").read_bytes()
    mcm: MCM = stream_decode(raw)
    assert mcm.mc[0].market_definition.market_type == "EACH_WAY"
    assert mcm.mc[0].market_definition.each_way_divisor == 4.0


def test_bsp_data():
    raw = (RESOURCES_DIR / "responses/streaming/mcm_bsp_data.json").read_bytes()
    mcm: MCM = stream_decode(raw)[0]
    rc = mcm.mc[0].rc[0]
    assert rc.spl == [StartingPriceLay(price=1.01, volume=2.8)]
    assert rc.spn == 4.5


def test_bsp_result():
    raw = (RESOURCES_DIR / "responses/streaming/mcm_market_definition_bsp.json").read_bytes()
    mcm: MCM = stream_decode(raw)
    runners = mcm.mc[0].market_definition.runners
    assert runners[0].bsp == 2.0008034621107256
    assert runners[0].status == RunnerStatus.WINNER
