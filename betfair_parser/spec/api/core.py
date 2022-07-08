from typing import Literal

import msgspec


class Base(msgspec.Struct):
    jsonrpc: Literal["2.0"]
    id: int = 1
