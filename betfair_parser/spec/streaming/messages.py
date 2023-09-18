"""
Definition of the betfair streaming API messages as defined in:
- https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
- https://github.com/betfair/stream-api-sample-code/blob/master/ESASwaggerSchema.json
 """

from typing import List, Literal, Optional, Union

from betfair_parser.spec.common import BaseMessage
from betfair_parser.spec.streaming.enums import ChangeType, SegmentType, StatusErrorCode
from betfair_parser.spec.streaming.type_definitions import (
    MarketChange,
    MarketDataFilter,
    MarketDefinition,
    MarketFilter,
    OrderFilter,
    OrderMarketChange,
)


def first_lower(s: str) -> str:
    """Lower only the first character of a string."""
    return s[:1].lower() + s[1:]


class StreamRequest(BaseMessage, tag_field="op", tag=first_lower, omit_defaults=True, frozen=True):
    id: Optional[Union[int, str]] = None  # Client generated unique id to link request with response (like json rpc)


class StreamResponse(BaseMessage, tag_field="op", tag=str.lower, omit_defaults=True, frozen=True):
    id: Optional[Union[int, str]] = None  # Client generated unique id to link request with response (like json rpc)


class Authentication(StreamRequest, kw_only=True, frozen=True):
    app_key: str
    session: str


class _Subscription(StreamRequest, kw_only=True, frozen=True):
    """Common parent class for any Subscription request."""

    clk: Optional[str] = None  # Token value delta (received in MarketChangeMessage) for resuming a subscription
    conflate_ms: Optional[int] = None  # the conflation rate (looped back on initial image: bounds are 0 to 120000)
    heartbeat_ms: Optional[int] = None  # the heartbeat rate (looped back on initial image: bounds are 500 to 5000)
    initial_clk: Optional[str] = None  # Token value that should be passed to resume a subscription
    segmentation_enabled: bool = True  # allow server to send large sets of data in segments, instead of a single block


class MarketSubscription(_Subscription, kw_only=True, frozen=True):
    market_filter: MarketFilter
    market_data_filter: MarketDataFilter


class OrderSubscription(_Subscription, kw_only=True, frozen=True):
    order_filter: OrderFilter  # Optional filter applied to order subscription


class Heartbeat(StreamRequest, frozen=True):
    pass


class Connection(StreamResponse, kw_only=True, frozen=True):
    connection_id: str


class Status(StreamResponse, kw_only=True, frozen=True):
    connection_closed: bool
    connection_id: Optional[str] = None
    connections_available: Optional[int] = None  # The number of connections available for this account at this moment
    error_code: Optional[StatusErrorCode] = None
    error_message: Optional[str] = None  # Additional message in case of a failure
    status_code: Literal["SUCCESS", "FAILURE"]  # The status of the last request

    @property
    def is_error(self):
        return self.status_code != "SUCCESS"


class _ChangeMessage(StreamResponse, kw_only=True, frozen=True):
    """Common parent class for any ChangeMessage."""

    clk: Optional[str] = None  # Token value (non-null) should be stored for resuming in case of a disconnect
    con: Optional[bool] = None  # TODO: Undocumented in swagger, mb misplaced in the tests?
    conflate_ms: Optional[int] = None  # the conflation rate (may differ from that requested if subscription is delayed)
    ct: Optional[ChangeType] = None
    heartbeat_ms: Optional[int] = None  # heartbeat rate (may differ from requested: bounds are 500 to 30000)
    initial_clk: Optional[str] = None  # Token value (non-null) should be stored for resuming in case of a disconnect
    pt: int  # Publish Time (in millis since epoch) that the changes were generated
    segment_type: Optional[SegmentType] = None  # denotes the beginning and end of a segmentation
    status: Optional[int] = None  # null if the stream is up to date and 503 if the services are experiencing latencies

    @property
    def is_heartbeat(self):
        return self.ct == ChangeType.HEARTBEAT

    @property
    def stream_unreliable(self):
        return self.status == 503


class MCM(_ChangeMessage, kw_only=True, frozen=True):
    market_definition: Optional[MarketDefinition] = None  # Undocumented in swagger
    mc: Optional[List[MarketChange]] = None  # empty for heartbeats


class OCM(_ChangeMessage, kw_only=True, frozen=True):
    oc: Optional[List[OrderMarketChange]] = None  # empty for heartbeats
