from betfair_parser.core import read_file
from tests.unit.conftest import RESOURCES_DIR


def test_event():
    fn = RESOURCES_DIR / "data/27312315.bz2"
    results = list(read_file(fn))
    assert len(results) == 50854


def test_market():
    fn = RESOURCES_DIR / "data/1.185781277.bz2"
    results = list(read_file(fn))
    assert len(results) == 7600
