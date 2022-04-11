from betfair_parser.core import read_file
from tests.unit.test_core import RESOURCES_DIR


def run():
    fn = RESOURCES_DIR / "data/27312315.bz2"
    return list(read_file(fn))


def test_large_file():
    fn = RESOURCES_DIR / "data/27312315.bz2"
    return list(read_file(fn))


def test_my_stuff(benchmark):
    # benchmark something
    result = benchmark(
        run,
    )

    # Extra code, to verify that the run completed correctly.
    # Sometimes you may want to check the result, fast functions
    # are no good if they return incorrect results :-)
    assert len(result) == 123
