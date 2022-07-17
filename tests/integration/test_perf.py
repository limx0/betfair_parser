from betfair_parser.core import read_file
from tests.unit.conftest import RESOURCES_DIR


def run():
    fn = RESOURCES_DIR / "data/27312315.bz2"
    return list(read_file(fn))


def test_performance(benchmark):
    # benchmark something
    result = benchmark.pedantic(run, rounds=1, iterations=1)

    assert len(result) == 50854
