from typing import Generic, Literal, Optional, TypeVar

import msgspec

from betfair_parser.spec.common.enums import APIExceptionCode, EndpointType, JSONExceptionCode


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


class BaseMessage(msgspec.Struct, kw_only=True, forbid_unknown_fields=True, frozen=True, rename="camel"):
    @classmethod
    def parse(cls, raw):
        return decode(raw, type=cls)

    def validate(self):
        return bool(decode(encode(self), type=type(self)))

    def to_dict(self):
        return msgspec.structs.asdict(self)


class Params(BaseMessage, omit_defaults=True, frozen=True):
    """By default, don't send None and other default values in operation parameters."""


class BaseResponse(BaseMessage, frozen=True):
    """Base class for Response, ErrorResponse and IdentityResponse."""

    def raise_on_error(self):
        """If the response contains some kind of error condition, raise an according Exception."""


class RPC(BaseMessage, frozen=True):
    jsonrpc: Literal["2.0"] = "2.0"
    id: int = 1


ResultType = TypeVar("ResultType")
ParamsType = TypeVar("ParamsType")
ErrorCode = TypeVar("ErrorCode")


class Response(RPC, BaseResponse, Generic[ResultType], kw_only=True, frozen=True):
    result: ResultType


class JsonError(BaseMessage, frozen=True):
    code: JSONExceptionCode
    message: str


class ErrorResponse(RPC, BaseResponse, kw_only=True, frozen=True):
    error: JsonError


class APIException(BaseMessage, Generic[ErrorCode], kw_only=True, frozen=True):
    error_code: ErrorCode
    error_details: Optional[str] = None  # The stack trace of the error
    request_uuid: Optional[str] = msgspec.field(name="requestUUID", default=None)


class Request(RPC, Generic[ParamsType], kw_only=True, frozen=True):
    method: str = ""
    params: ParamsType = {}  # type: ignore
    return_type = BaseResponse  # not to be serialized, so no type definition
    throws = APIException[APIExceptionCode]  # not to be serialized, so no type definition
    endpoint_type = EndpointType.NONE

    @classmethod
    def with_params(cls, request_id=1, **kwargs):
        params_cls = cls.__annotations__["params"]
        return cls(
            params=params_cls(**kwargs),
            method=cls.method,
            id=request_id,
        )

    @staticmethod
    def headers():
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            # X-Application to be set by the application
            # X-Authentication to be set by the application
        }

    def body(self):
        return encode(self)

    def parse_response(self, response):
        resp = decode(response, type=self.return_type)
        if resp.id != self.id:
            raise ValueError(f"Response ID ({resp.id}) does not match Request ID ({self.id})")
        resp.raise_on_error()
        return resp.result
