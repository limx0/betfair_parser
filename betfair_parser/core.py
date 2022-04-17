from typing import Union

import fsspec
import msgspec
from msgspec.json import Decoder

from betfair_parser.spec.streaming.core import Connection, Status
from betfair_parser.spec.streaming.mcm import MCM
from betfair_parser.spec.streaming.ocm import OCM


STREAM_DECODER = Decoder(Union[Connection, Status, MCM, OCM])


def read_file(fsspec_url: str):
    with fsspec.open(fsspec_url, compression="infer") as f:
        for line in f:
            try:
                data = STREAM_DECODER.decode(line)
            except msgspec.DecodeError as e:
                print("ERR", e)
                print(msgspec.json.decode(line))
                raise e
            yield data
