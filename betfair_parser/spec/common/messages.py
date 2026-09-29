import re
from itertools import count
from typing import Annotated, Any, ClassVar, Literal, get_type_hints

import msgspec

from betfair_parser.exceptions import APIError, APINGException, JSONError
from betfair_parser.spec.common.enums import (
    AccountAPINGExceptionCode,
    APINGExceptionCode,
    EndpointType,
    JSONExceptionCode,
)


def doc(docstring: str | None = None) -> msgspec.Meta:
    """Create msgspec type metadata with a documentation string, for use in ``Annotated`` type hints.

    >>> doc("The market id these orders are to be placed on")
    msgspec.Meta(description='The market id these orders are to be placed on')
    """
    return msgspec.Meta(description=docstring)


def _unwrap_meta(info: Any) -> tuple[str | None, Any]:
    """Strip msgspec.inspect.Metadata wrappers, returning their description and the inner type info."""
    description = None
    while isinstance(info, msgspec.inspect.Metadata):
        description = info.extra_json_schema.get("description") or description
        info = info.type
    return description, info


def _descend_index(info: Any, bracket: str) -> tuple[str | None, Any] | None:
    """Descend into a sequence item or mapping value of a path bracket part like ``[0]`` or ``[...]``.

    msgspec masks dict keys in error paths as ``[...]``, so the value type is the best we can resolve.
    """
    _, info = _unwrap_meta(info)
    item_type = None
    if bracket.isdigit():
        index = int(bracket)
        item_type = getattr(info, "item_type", None)  # list, set, variadic tuple
        if item_type is None:
            item_types = getattr(info, "item_types", None)  # fixed-length tuple
            if item_types is not None and index < len(item_types):
                item_type = item_types[index]
    else:  # masked dict key
        item_type = getattr(info, "value_type", None)
    if item_type is None:
        return None
    return _unwrap_meta(item_type)


def _descend_brackets(info: Any, brackets: list[str]) -> tuple[str | None, Any] | None:
    """Descend into the sequence items / masked dict values of all bracket parts of a path segment."""
    description = None
    for bracket in brackets:
        matched = _descend_index(info, bracket)
        if matched is None:
            return None
        description, info = matched
    return description, info


def _match_field(info: Any, name: str) -> tuple[str | None, Any] | None:
    """Match a JSON path segment name against the fields of a type info.

    Returns the description and the type info of the matched field, or None if it can't be matched.
    Sequences, mappings and unions are descended into on a best-effort basis. Ambiguous unions
    (multiple members with a structurally differing field of the same name) are not descended into,
    since a wrong description would be worse than no description at all.
    """
    description, info = _unwrap_meta(info)
    while True:
        if isinstance(info, msgspec.inspect.StructType):
            for field in info.fields:
                if field.encode_name == name:
                    return _unwrap_meta(field.type)
            return None
        item_type = getattr(info, "item_type", None)
        if item_type is None:
            item_types = getattr(info, "item_types", None)
            if item_types is not None:  # fixed-length tuple without an index in the path
                item_type = item_types[0]
        if item_type is not None:  # list, set, tuple
            _, info = _unwrap_meta(item_type)
            continue
        value_type = getattr(info, "value_type", None)
        if value_type is not None:  # dict
            _, info = _unwrap_meta(value_type)
            continue
        if isinstance(info, msgspec.inspect.UnionType):
            candidates = []
            for member in info.types:
                _, inner = _unwrap_meta(member)
                if isinstance(inner, msgspec.inspect.StructType | msgspec.inspect.ListType | msgspec.inspect.TupleType):
                    matched = _match_field(inner, name)
                    if matched:
                        candidates.append(matched)
            if not candidates:
                return None
            first_desc, first_info = candidates[0]
            if all(desc == first_desc and inner == first_info for desc, inner in candidates[1:]):
                return first_desc or description, first_info
            return None
        return None


def _split_error_path(path: str) -> list[str]:
    """Split an error path on dots, ignoring dots within brackets (e.g. the dict key mask ``[...]``)."""
    segments = []
    depth = 0
    current = ""
    for char in path:
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
        if char == "." and depth <= 0:
            segments.append(current)
            current = ""
        else:
            current += char
    segments.append(current)
    return segments


def _split_segment(segment: str) -> tuple[str, list[str]]:
    """Split a path segment into the field name and its bracket parts (indices or the dict key mask)."""
    parts = re.split(r"\[([^\[\]]*)\]", segment)
    return parts[0], parts[1::2]


def enriched_validation_error(error: msgspec.ValidationError, type: Any) -> str:
    """Return a validation error message, enriched with the documented description of the failing field.

    The description is appended in parentheses, e.g.::

        Expected `str`, got `int` - at `$.params.marketId` (The market id these orders are to be placed on)
    """
    message = str(error)
    try:
        if " - at `" not in message:
            return message
        path = message.rsplit(" - at `", 1)[1].rstrip("`")
        info: Any = msgspec.inspect.type_info(type)
        description = None
        for segment in _split_error_path(path):
            name, brackets = _split_segment(segment)
            if name == "$":
                # root marker: bare non-struct roots carry their index within the brackets
                if not brackets:
                    continue
                indexed = _descend_brackets(info, brackets)
                if indexed is None:
                    break
                description = indexed[0] or description
                info = indexed[1]
                continue
            matched = _match_field(info, name)
            if matched is None:
                break
            description = matched[0] or description
            info = matched[1]
            if brackets:  # descend into the indexed items, their descriptions may be the most specific ones
                indexed = _descend_brackets(info, brackets)
                if indexed is None:
                    break
                description = indexed[0] or description
                info = indexed[1]
        if description:
            message = f"{message} ({description})"
    except Exception:  # noqa: BLE001, S110 - error message enrichment must never mask the original error
        pass
    return message


def decode(raw: bytes, type: Any = Any) -> Any:
    try:
        return msgspec.json.decode(raw, strict=False, type=type)
    except msgspec.ValidationError as e:
        raise JSONError(enriched_validation_error(e, type)) from e
    except msgspec.DecodeError as e:
        raise JSONError(str(e)) from e


def encode(data: object) -> bytes:
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


class ExceptionDetails[ErrorCode](BaseMessage, kw_only=True, frozen=True):
    error_code: ErrorCode
    error_details: Annotated[str | None, doc("The stack trace of the error")] = None
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
    code: Annotated[int, doc("JSONExceptionCode or any other undocumented integer code, if it's an APINGException")]
    message: Annotated[str, doc('Something like "DSC-0018", "AANGX-0011", ...')]
    data: Annotated[ExceptionData | None, doc("The interesting part")] = None

    @property
    def exception_code(self):
        """Return some form of ExceptionCode, whatever error we get."""
        return self.data.code if self.data else JSONExceptionCode(self.code)

    def __str__(self) -> str:
        return str(self.exception_code)


class Response[ResultType](RPC, BaseResponse, kw_only=True, frozen=True):
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


def _resolve_params_cls(cls: type) -> type:
    """Get the according parameter class from the type hints of a Request subclass."""
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


class Request(RPC, kw_only=True, frozen=True, tag_field="method", tag=first_lower):
    # class variables for subclassing, which msgspec won't serialize in messages
    endpoint_type: ClassVar[EndpointType] = EndpointType.NONE
    return_type: ClassVar[type] = Response
    throws: ClassVar[type] = APINGException  # JSON error definition
    params_cls: ClassVar[type] = Params  # resolved eagerly per subclass, see __init_subclass__

    # Having no default for `params` makes sure, that initializing a message object that
    # requires parameters without explicitly calling the `with_params` constructor fails.
    params: Params

    def __init_subclass__(cls, **kwargs):
        # resolve the parameter class once at class definition, so that `with_params` never
        # pays for the get_type_hints reflection - not even on the first call
        super().__init_subclass__(**kwargs)  # msgspec consumes the class keywords here
        cls.params_cls = _resolve_params_cls(cls)

    @classmethod
    def with_params(cls, request_id=None, **kwargs):
        """General constructor for RPC requests."""
        params = cls.params_cls(**kwargs)
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
