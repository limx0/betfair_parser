from typing import Union

from msgspec.json import Decoder

from betfair_parser.spec.streaming.core import Connection, Status
from betfair_parser.spec.streaming.mcm import MCM
from betfair_parser.spec.streaming.ocm import OCM


STREAM_MESSAGE = Union[Connection, Status, MCM, OCM]
STREAM_DECODER = Decoder(STREAM_MESSAGE)
