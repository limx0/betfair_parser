from typing import Literal

from betfair_parser.spec.common import BaseMessage


class RequestBase(BaseMessage, kw_only=True):
    jsonrpc: Literal["2.0"] = "2.0"
    id: int = 1
