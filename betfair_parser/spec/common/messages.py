from typing import Any, Generic, Literal, Optional, TypeVar

import msgspec

from betfair_parser.exceptions import APIError, APINGException, JSONError
from betfair_parser.spec.common.enums import (
    AccountAPINGExceptionCode,
    APINGExceptionCode,
    EndpointType,
    JSONExceptionCode,
)


def decode(raw: bytes, type: Any = Any) -> Any:
    try:
        return msgspec.json.decode(raw, strict=False, type=type)  # type: ignore
    except msgspec.DecodeError as e:
        raise JSONError(str(e)) from e


def encode(data: Any) -> bytes:
    try:
        return msgspec.json.encode(data)
    except msgspec.EncodeError as e:
        raise JSONError(str(e)) from e


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
    """Base class for Response, ErrorResponse and identity responses."""

    @property
    def is_error(self):
        """True, if the response is some kind of error."""
        return False


class RPC(BaseMessage, frozen=True):
    jsonrpc: Literal["2.0"] = "2.0"
    id: int = 1


ResultType = TypeVar("ResultType")
ParamsType = TypeVar("ParamsType")
ErrorCode = TypeVar("ErrorCode")


class ExceptionDetails(BaseMessage, Generic[ErrorCode], kw_only=True, frozen=True):
    error_code: ErrorCode
    error_details: Optional[str] = None  # The stack trace of the error
    request_uuid: Optional[str] = msgspec.field(name="requestUUID", default=None)

    @property
    def code(self):
        return self.error_code


class ExceptionData(BaseMessage, frozen=True, rename=None):
    exception_name: Literal["APINGException", "AccountAPINGException"] = msgspec.field(name="exceptionname")
    APINGException: Optional[ExceptionDetails[APINGExceptionCode]] = None
    AccountAPINGException: Optional[ExceptionDetails[AccountAPINGExceptionCode]] = None

    @property
    def error(self):
        return getattr(self, self.exception_name)

    @property
    def code(self):
        return self.error.code


class RPCError(BaseMessage, frozen=True):
    code: int  # JSONExceptionCode or any other undocumented integer code, if it's an APINGException
    message: str  # Something like "DSC-0018", "AANGX-0011", ...
    data: Optional[ExceptionData] = None  # The interesting part

    @property
    def exception_code(self):
        """Return some form of ExceptionCode, whatever error we get."""
        return self.data.code if self.data else JSONExceptionCode(self.code)

    def __str__(self):
        return str(self.exception_code)


class Response(RPC, BaseResponse, Generic[ResultType], kw_only=True, frozen=True):
    """RPC response. Either an error or a result."""

    result: Optional[ResultType] = None
    error: Optional[RPCError] = None

    @property
    def is_error(self):
        return self.error is not None


class Request(RPC, Generic[ParamsType], kw_only=True, frozen=True):
    endpoint_type = EndpointType.NONE
    method: str = ""
    params: ParamsType = {}  # type: ignore
    return_type = Response  # not to be serialized, so no type definition
    throws = APINGException  # JSON error definition

    @classmethod
    def with_params(cls, request_id=1, **kwargs):
        params_cls = cls.__annotations__.get("params", dict)
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

    def parse_response(self, response, raise_errors=True):
        resp = decode(response, type=self.return_type)
        if resp.id != self.id:
            raise APIError(f"Response ID ({resp.id}) does not match Request ID ({self.id})")
        if resp.is_error:
            if raise_errors:
                exception = self.throws(
                    str(resp.error.exception_code),
                    response=resp,
                    request=self,
                    code=resp.error.exception_code,
                )
                raise exception
            return resp.error
        return resp.result
