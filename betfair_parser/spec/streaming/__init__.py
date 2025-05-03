import msgspec
from msgspec.json import Decoder

from betfair_parser.exceptions import StreamError
from betfair_parser.spec.betting.enums import MarketBettingType, MarketStatus, MarketTypeCode, RunnerStatus  # noqa
from betfair_parser.spec.common import EventTypeIdCode  # noqa for reimport
from betfair_parser.spec.streaming import enums, type_definitions
from betfair_parser.spec.streaming.enums import (
    ChangeType,
    LapseStatusReasonCode,
    MarketDataFilterFields,
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
    RunnerChange,
    RunnerDefinition,
    StartingPriceBack,
    StartingPriceLay,
    StrategyMatchChange,
    StreamRef,
    Trade,
)


StreamRequestType = Authentication | MarketSubscription | OrderSubscription | Heartbeat
StreamResponseType = Connection | Status | MCM | OCM
SubscriptionType = MarketSubscription | OrderSubscription
ChangeMessageType = MCM | OCM
StreamMessageType = StreamResponseType | list[StreamResponseType] | StreamRequestType

_STREAM_DECODER = Decoder(StreamMessageType, strict=False)


def stream_decode(raw: str | bytes) -> StreamMessageType:
    try:
        return _STREAM_DECODER.decode(raw)
    except msgspec.DecodeError as e:
        raise StreamError(str(e))


def stream_decode_lines(raw: str | bytes) -> list[StreamMessageType]:
    try:
        return _STREAM_DECODER.decode_lines(raw)
    except msgspec.DecodeError as e:
        raise StreamError(str(e))
