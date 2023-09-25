from typing import Union

from msgspec.json import Decoder

from betfair_parser.spec.betting.enums import MarketBettingType  # noqa: F401
from betfair_parser.spec.betting.enums import MarketStatus  # noqa: F401
from betfair_parser.spec.betting.enums import MarketTypeCode  # noqa: F401
from betfair_parser.spec.betting.enums import RunnerStatus  # noqa: F401
from betfair_parser.spec.streaming.messages import (
    MCM,
    OCM,
    Authentication,
    Connection,
    Heartbeat,
    MarketSubscription,
    OrderSubscription,
    Status,
)
from betfair_parser.spec.streaming.type_definitions import MarketDataFilter  # noqa: F401
from betfair_parser.spec.streaming.type_definitions import MarketDataFilterFields  # noqa: F401
from betfair_parser.spec.streaming.type_definitions import MarketFilter  # noqa: F401
from betfair_parser.spec.streaming.type_definitions import OrderFilter  # noqa: F401


STREAM_REQUEST = Union[Authentication, MarketSubscription, OrderSubscription, Heartbeat]
STREAM_RESPONSE = Union[Connection, Status, MCM, OCM]
_STREAM_MESSAGES = Union[STREAM_RESPONSE, list[STREAM_RESPONSE], STREAM_REQUEST]
_STREAM_DECODER = Decoder(_STREAM_MESSAGES, strict=False)


def stream_decode(raw: bytes):
    return _STREAM_DECODER.decode(raw)
