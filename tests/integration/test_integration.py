from betfair_parser.core import read_file
from tests.unit.test_core import RESOURCES_DIR


def test_run():
    fn = RESOURCES_DIR / "data/27312315.bz2"
    results = list(read_file(fn))
    assert len(results) == 50854
