import pytest

from betfair_parser.core import read_file
from betfair_parser.spec.betting.type_definitions import MarketCatalogue
from betfair_parser.spec.common import Request, Response, decode
from tests.resources import RESOURCES_DIR, id_from_path


@pytest.mark.parametrize("path", sorted((RESOURCES_DIR / "requests").glob("*/*.json")), ids=id_from_path)
def test_read_requests(path):
    raw = path.read_bytes()
    assert decode(raw, type=Request)


@pytest.mark.parametrize("path", sorted((RESOURCES_DIR / "responses").glob("*/*.json")), ids=id_from_path)
def test_read_responses(path):
    raw = path.read_bytes()
    if "market_catalogue" in str(path):
        # That data was cut out from the complete response
        parse_type = list[MarketCatalogue]
    else:
        parse_type = Response
    resp = decode(raw, type=parse_type)
    assert resp

    if "market_catalogue" in str(path):
        assert len(resp)
    elif "error" in str(path):
        assert resp.error
    else:
        assert resp.result


@pytest.mark.parametrize(
    ["filename", "n_items"],
    [
        ("1.185781277.bz2", 7600),
        ("1.205822330.bz2", 5654),
        ("27312315.bz2", 50854),
    ],
)
def test_archive(filename, n_items):
    path = RESOURCES_DIR / "data" / filename
    results = list(read_file(path))
    assert len(results) == n_items
