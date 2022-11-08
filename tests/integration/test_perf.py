import fsspec

from betfair_parser.core import parse
from tests.unit.conftest import RESOURCES_DIR


def run(lines: list[bytes]):
    return [parse(line) for line in lines]


def test_performance(benchmark):
    fn = RESOURCES_DIR / "data/27312315.bz2"
    with fsspec.open(fn, compression="infer") as f:
        lines = f.read().split(b"\n")[:-1]
    result = benchmark.pedantic(run, args=(lines,), rounds=1, iterations=1)
    assert len(result) == 50854
