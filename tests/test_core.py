import pathlib

import msgspec
import pytest

from betfair_parser.core import STREAM_DECODER, read_file


def test_core():
    fn = "./resources/data/1.185781277.bz2"
    data = list(read_file(fn))
    assert len(data) == 7600


@pytest.mark.parametrize("fn", list(map(str, pathlib.Path("./resources/streaming").glob("*.json"))))
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
