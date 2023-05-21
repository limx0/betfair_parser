import datetime
from typing import Annotated, Generic, Literal, Optional, TypeVar, Union

import msgspec

from betfair_parser.spec.error import APIExceptionCode, JSONExceptionCode
from betfair_parser.strenums import DocumentedEnum, StrEnum, auto, doc


class IntStr(int):
    """Class for marking misformatted integer JSON fields, e.g. "123" instead of 123."""


class FloatStr(float):
    """Class for marking misformatted float JSON fields, e.g. "-5.5" instead of -5.5."""


def encode_intfloat(obj):
    """Encode int and float subtypes as ordinary ints and floats."""
    if isinstance(obj, int):
        return int(obj)
    if isinstance(obj, float):
        return float(obj)
    raise TypeError("Unencodable type")


def decode_intfloat(type_, obj):
    """
    Betfair uses JSON formatting inconsistently. For requests to their API they
    format int and float values in all of their examples as '"123"' and '"5.5"',
    even if those quotation marks aren't necessary and violate JSON
    specification.

    This decoding hook gets rid of any quotation marks and restores the original
    data type. Unfortunately we can't use plain int and float, but need to define
    a subclass of them, so that the dec_hook can do it's job.
    """
    if type_ is IntStr:
        if isinstance(obj, int):
            return IntStr(obj)
        return IntStr(obj.strip("'\" "))
    if type_ is FloatStr:
        if isinstance(obj, (float, int)):
            return FloatStr(obj)
        return FloatStr(obj.strip("'\" "))
    raise TypeError("Undecodable type")


def decode(raw, type=None):
    if type is None:
        return msgspec.json.decode(raw, dec_hook=decode_intfloat)
    return msgspec.json.decode(raw, type=type, dec_hook=decode_intfloat)


def encode(data):
    return msgspec.json.encode(data, enc_hook=encode_intfloat)


class BaseMessage(msgspec.Struct, kw_only=True, forbid_unknown_fields=True, frozen=True):
    def validate(self):
        return bool(decode(encode(self), type=type(self)))

    def to_dict(self):
        return msgspec.structs.asdict(self)


class RPC(BaseMessage, frozen=True):
    jsonrpc: Literal["2.0"] = "2.0"
    id: int = 1


ResultType = TypeVar("ResultType")
ErrorCode = TypeVar("ErrorCode")


class Response(RPC, Generic[ResultType], kw_only=True, frozen=True):
    result: ResultType


class JsonError(BaseMessage, frozen=True):
    code: JSONExceptionCode
    message: str


class ErrorResponse(RPC, kw_only=True, frozen=True):
    error: JsonError


class APIException(BaseMessage, Generic[ErrorCode], kw_only=True, frozen=True):
    errorCode: ErrorCode
    errorDetails: Optional[str] = None  # The stack trace of the error
    requestUUID: Optional[str] = None


class Request(RPC, kw_only=True, frozen=True):
    method: str
    params: msgspec.Struct
    response_type = None  # not to be serialized, so no type definition
    throws = APIException[APIExceptionCode]  # not to be serialized, so no type definition


# Type aliases with minimalistic validation

Date = Annotated[datetime.datetime, msgspec.Meta(title="Date", tz=True)]
SelectionId = Annotated[IntStr, msgspec.Meta(title="SelectionId")]
Venue = Annotated[str, msgspec.Meta(title="Venue")]
MarketId = Annotated[str, msgspec.Meta(title="MarketId")]
Handicap = Annotated[FloatStr, msgspec.Meta(title="Handicap")]
EventId = Annotated[str, msgspec.Meta(title="EventId")]
EventTypeId = Annotated[IntStr, msgspec.Meta(title="EventTypeId")]
CountryCode = Annotated[str, msgspec.Meta(title="CountryCode", min_length=2, max_length=3)]
ExchangeId = Annotated[str, msgspec.Meta(title="ExchangeId")]
CompetitionId = Annotated[str, msgspec.Meta(title="CompetitionId")]
Price = Annotated[FloatStr, msgspec.Meta(title="Price")]
Size = Annotated[FloatStr, msgspec.Meta(title="Size")]
BetId = Annotated[Union[str, int], msgspec.Meta(title="BetId")]
MatchId = Annotated[Union[str, int], msgspec.Meta(title="MatchId")]
CustomerRef = Annotated[Union[str, int], msgspec.Meta(title="CustomerRef")]
CustomerOrderRef = Annotated[Union[str, int], msgspec.Meta(title="CustomerOrderRef")]
CustomerStrategyRef = Annotated[Union[str, int], msgspec.Meta(title="CustomerStrategyRef")]


# Enums and type definitions, that are used in multiple parts of the API


class OrderType(DocumentedEnum):
    LIMIT = doc("A normal exchange limit order for immediate execution")
    LIMIT_ON_CLOSE = doc("Limit order for the auction (SP)")
    MARKET_ON_CLOSE = doc("Market order for the auction (SP)")


class OrderSide(StrEnum):
    BACK = auto()
    LAY = auto()


class OrderResponse(StrEnum):
    SUCCESS = auto()
    FAILURE = auto()


class OrderStatus(DocumentedEnum):
    PENDING = doc(
        "An asynchronous order is yet to be processed. Once the bet has been processed by the exchange "
        "(including waiting for any in-play delay), the result will be reported and available on the "
        "Exchange Stream API and API NG. Not a valid search criteria on MarketFilter."
    )
    EXECUTION_COMPLETE = doc("An order that does not have any remaining unmatched portion.")
    EXECUTABLE = doc("An order that has a remaining unmatched portion.")
    EXPIRED = doc(
        "The order is no longer available for execution due to its time in force constraint. "
        "In the case of FILL_OR_KILL orders, this means the order has been killed because it "
        "could not be filled to your specifications. Not a valid search criteria on MarketFilter."
    )


class TimeRange(BaseMessage, frozen=True):
    from_: Optional[Date] = msgspec.field(name="from", default=None)
    to: Optional[Date] = None
