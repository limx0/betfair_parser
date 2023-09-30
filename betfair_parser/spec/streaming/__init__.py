from typing import Union

from msgspec.json import Decoder

from betfair_parser.spec.betting.enums import MarketBettingType, MarketStatus, MarketTypeCode, RunnerStatus  # noqa
from betfair_parser.spec.streaming import enums, type_definitions
from betfair_parser.spec.streaming.enums import (
    ChangeType,
    LapseStatusReasonCode,
    MarketDataFilterFields,
    PriceLadderDefinitionType,
    SegmentType,
    StatusErrorCode,
)
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
from betfair_parser.spec.streaming.type_definitions import (
    LPV,
    PV,
    AvailableToBack,
    AvailableToLay,
    BestAvailableToBack,
    BestAvailableToLay,
    BestDisplayAvailableToBack,
    BestDisplayAvailableToLay,
    KeyLineDefinition,
    KeyLineSelection,
    MarketChange,
    MarketDataFilter,
    MarketDefinition,
    MarketFilter,
    MatchedOrder,
    Order,
    OrderFilter,
    OrderMarketChange,
    OrderRunnerChange,
    PriceLadderDefinition,
    RunnerChange,
    RunnerDefinition,
    StartingPriceBack,
    StartingPriceLay,
    StrategyMatchChange,
    Trade,
)


STREAM_REQUEST = Union[Authentication, MarketSubscription, OrderSubscription, Heartbeat]
STREAM_RESPONSE = Union[Connection, Status, MCM, OCM]
CHANGE_MESSAGE = Union[MCM, OCM]
_STREAM_MESSAGES = Union[STREAM_RESPONSE, list[STREAM_RESPONSE], STREAM_REQUEST]
_STREAM_DECODER = Decoder(_STREAM_MESSAGES, strict=False)


def stream_decode(raw: Union[str, bytes]):
    return _STREAM_DECODER.decode(raw)


def stream_decode_lines(raw: Union[str, bytes]):
    return _STREAM_DECODER.decode_lines(raw)
