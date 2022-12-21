from typing import Literal

import msgspec


class APIBase(msgspec.Struct):
    def validate(self):
        return bool(msgspec.json.decode(msgspec.json.encode(self), type=type(self)))


class RequestBase(APIBase):
    jsonrpc: Literal["2.0"] = "2.0"
    id: int = 1
