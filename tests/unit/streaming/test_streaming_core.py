import msgspec
import pytest

from betfair_parser.core import STREAM_DECODER, read_file
from betfair_parser.spec.streaming import MCM, OCM
from betfair_parser.spec.streaming.ocm import MatchedOrder
from tests.unit.conftest import RESOURCES_DIR


def test_core():
    fn = RESOURCES_DIR / "data/1.185781277.bz2"
    data = list(read_file(fn))
    assert len(data) == 7600


@pytest.mark.parametrize("fn", list(map(str, (RESOURCES_DIR / "streaming").glob("*.json"))))
def test_streaming_files(fn):
    line = open(fn, "rb").read()
    data = msgspec.json.decode(line)
    if isinstance(data, list):
        for line in data:
            data = STREAM_DECODER.decode(msgspec.json.encode(line))
            assert data
    else:
        data = STREAM_DECODER.decode(line)
        assert data


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
