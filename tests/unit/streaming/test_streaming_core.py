import msgspec
import pytest

from betfair_parser.core import STREAM_DECODER, read_file
from betfair_parser.spec.streaming import OCM
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
