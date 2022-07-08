from typing import List, Literal

import msgspec


class cancelOrdersInstructions(msgspec.Struct):
    betId: str = "228302937743"


class cancelOrdersParams(msgspec.Struct):
    marketId: str = "1.179082386"
    instructions: List[cancelOrdersInstructions]
    customerRef: str


class cancelOrders(msgspec.Struct):
    method: Literal["SportsAPING/v1.0/cancelOrders"] = "SportsAPING/v1.0/cancelOrders"
    params: cancelOrdersParams
    id: int = 1
    jsonrpc: str = "2.0"
