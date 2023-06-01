from typing import Union

from msgspec.json import Decoder

from betfair_parser.spec.streaming.mcm import MCM
from betfair_parser.spec.streaming.ocm import OCM
from betfair_parser.spec.streaming.status import Connection, Status


_STREAM_MESSAGE = Union[Connection, Status, MCM, OCM]
_STREAM_DECODER = Decoder(_STREAM_MESSAGE)


def stream_decode(raw: bytes):
    return _STREAM_DECODER.decode(raw)
