from typing import Literal

import msgspec


class APIBase(msgspec.Struct):
    jsonrpc: Literal["2.0"]
    id: int = 1

    def validate(self):
        return bool(msgspec.json.decode(msgspec.json.encode(self), type=type(self)))
