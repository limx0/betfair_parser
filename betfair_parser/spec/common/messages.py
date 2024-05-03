from itertools import count
from typing import Any, ClassVar, Generic, Literal, TypeVar, get_type_hints

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
        return msgspec.json.decode(raw, strict=False, type=type)
    except msgspec.DecodeError as e:
        raise JSONError(str(e)) from e


def encode(data: Any) -> bytes:
    try:
        return msgspec.json.encode(data)
    except msgspec.EncodeError as e:
        raise JSONError(str(e)) from e


def first_lower(s: str) -> str:
    """Lower only the first character of a string."""
    return s[:1].lower() + s[1:]


def method_tag(prefix: str, class_name: str) -> str:
    return prefix + first_lower(class_name)


class BaseMessage(
    msgspec.Struct,
    kw_only=True,
    forbid_unknown_fields=True,
    omit_defaults=True,
    repr_omit_defaults=True,
    frozen=True,
    rename="camel",
):
    @classmethod
    def parse(cls, raw):
        return decode(raw, type=cls)

    def validate(self):
        return bool(decode(encode(self), type=type(self)))

    def to_dict(self):
        return msgspec.structs.asdict(self)

    def replace(self, **kwargs):
        return msgspec.structs.replace(self, **kwargs)


class Params(BaseMessage, frozen=True):
    """
    Base class for request parameters. Don't send None and other redundant default
    values. If not subclassed, this class is used to describe an empty parameter set.
    """


class BaseResponse(BaseMessage, frozen=True):
    """Base class for Response, ErrorResponse and identity responses."""

    @property
    def is_error(self):
        """True, if the response is some kind of error."""
        return False


class RPC(BaseMessage, omit_defaults=False, repr_omit_defaults=False, frozen=True):
    jsonrpc: Literal["2.0"] = "2.0"
    id: int = 1


ResultType = TypeVar("ResultType")
ParamsType = TypeVar("ParamsType")
ErrorCode = TypeVar("ErrorCode")


class ExceptionDetails(BaseMessage, Generic[ErrorCode], kw_only=True, frozen=True):
    error_code: ErrorCode
    error_details: str | None = None  # The stack trace of the error
    request_uuid: str | None = msgspec.field(name="requestUUID", default=None)

    @property
    def code(self) -> ErrorCode:
        return self.error_code


class ExceptionData(BaseMessage, frozen=True, rename=None):
    exception_name: Literal["APINGException", "AccountAPINGException"] = msgspec.field(name="exceptionname")
    APINGException: ExceptionDetails[APINGExceptionCode] | None = None
    AccountAPINGException: ExceptionDetails[AccountAPINGExceptionCode] | None = None

    @property
    def error(self) -> ExceptionDetails:
        return getattr(self, self.exception_name)

    @property
    def code(self) -> str:
        return self.error.code


class RPCError(BaseMessage, frozen=True):
    code: int  # JSONExceptionCode or any other undocumented integer code, if it's an APINGException
    message: str  # Something like "DSC-0018", "AANGX-0011", ...
    data: ExceptionData | None = None  # The interesting part

    @property
    def exception_code(self):
        """Return some form of ExceptionCode, whatever error we get."""
        return self.data.code if self.data else JSONExceptionCode(self.code)

    def __str__(self) -> str:
        return str(self.exception_code)


class Response(RPC, BaseResponse, Generic[ResultType], kw_only=True, frozen=True):
    """RPC response. Either an error or a result."""

    result: ResultType | None = None
    error: RPCError | None = None

    @property
    def is_error(self) -> bool:
        return self.error is not None


_default_id_generator = count(1)


def _failsafe_issubclass(x: Any, A: type) -> bool:
    try:
        return issubclass(x, A)
    except TypeError:
        return False


class Request(RPC, kw_only=True, frozen=True, tag_field="method", tag=first_lower):
    # class variables for subclassing, which msgspec won't serialize in messages
    endpoint_type: ClassVar[EndpointType] = EndpointType.NONE
    return_type: ClassVar[type] = Response
    throws: ClassVar[type] = APINGException  # JSON error definition

    # Having no default for `params` makes sure, that initializing a message object that
    # requires parameters without explicitly calling the `with_params` constructor fails.
    params: Params

    @classmethod
    def _params_cls(cls) -> type:
        """Get the according parameter class from the type hints."""
        hinted_type = get_type_hints(cls)["params"]
        if _failsafe_issubclass(hinted_type, Params):
            # params: Params
            return hinted_type
        if hinted_type is type(None):
            # params: None
            return dict
        if hinted_type.__args__:
            # params: Optional[Params]
            hinted_type = hinted_type.__args__[0]
            if _failsafe_issubclass(hinted_type, Params):
                return hinted_type
        return dict

    @classmethod
    def with_params(cls, request_id=None, **kwargs):
        """General constructor for RPC requests."""
        params = cls._params_cls()(**kwargs)
        if request_id is None:
            request_id = next(_default_id_generator)
        return cls(
            params=params,
            id=request_id,
        )

    @property
    def method(self) -> str:
        """Return the RPC request method as defined by the classes tag configuration."""
        return str(self.__struct_config__.tag)

    @staticmethod
    def headers() -> dict[str, str]:
        """HTTP headers of the request."""
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            # X-Application to be set by the application
            # X-Authentication to be set by the application
        }

    def body(self) -> bytes:
        """HTTP body of the request."""
        return encode(self)

    def parse_response(self, response: bytes, raise_errors: bool = True):
        """Parse the received response into the defined return type."""
        resp = decode(response, type=self.return_type)
        if resp.id != self.id:
            raise APIError(f"Response ID ({resp.id}) does not match Request ID ({self.id})")
        if not resp.is_error:
            return resp.result
        if not raise_errors:
            return resp.error
        raise self.throws(
            str(resp.error.exception_code),
            response=resp,
            request=self,
            code=resp.error.exception_code,
        )
