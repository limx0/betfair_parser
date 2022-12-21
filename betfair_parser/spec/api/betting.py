from typing import List, Literal, Optional, Union

import msgspec

from betfair_parser.spec.api.core import APIBase, RequestBase


# ------------ ORDER TYPES ------------ #


class LimitOrder(msgspec.Struct):
    size: Union[str, float]
    price: Union[str, float]
    persistenceType: Literal["PERSIST"]


class MarketOnCloseOrder(msgspec.Struct):
    liability: str


# ------------ REQUESTS ------------ #


class placeInstructions(msgspec.Struct):
    selectionId: str
    handicap: str
    customerOrderRef: str
    orderType: Literal["LIMIT", "MARKET_ON_CLOSE"]
    side: Literal["BACK", "LAY"]
    limitOrder: Optional[LimitOrder] = None
    marketOnCloseOrder: Optional[MarketOnCloseOrder] = None


class placeOrdersParams(msgspec.Struct):
    marketId: str
    instructions: List[placeInstructions]
    customerRef: Optional[str]
    customerStrategyRef: Optional[str]


class placeOrders(RequestBase, kw_only=True):  # type: ignore
    params: placeOrdersParams
    method: Literal["SportsAPING/v1.0/placeOrders"] = "SportsAPING/v1.0/placeOrders"


class cancelOrdersInstructions(msgspec.Struct):
    betId: str


class cancelOrdersParams(msgspec.Struct):
    marketId: str
    instructions: List[cancelOrdersInstructions]
    customerRef: str


class cancelOrders(RequestBase, kw_only=True):  # type: ignore
    method: Literal["SportsAPING/v1.0/cancelOrders"] = "SportsAPING/v1.0/cancelOrders"
    params: cancelOrdersParams


class replaceOrdersInstructions(msgspec.Struct):
    betId: str
    newPrice: float


class replaceOrdersParams(msgspec.Struct):
    marketId: str
    instructions: List[replaceOrdersInstructions]
    customerRef: str


class replaceOrders(RequestBase, kw_only=True):  # type: ignore
    method: Literal["SportsAPING/v1.0/replaceOrders"] = "SportsAPING/v1.0/replaceOrders"
    params: replaceOrdersParams


# ------------ RESPONSES ------------ #

STATUS = Literal["SUCCESS", "FAILURE"]
ORDER_STATUS = Literal["EXECUTABLE", "EXECUTION_COMPLETE"]


class Instruction(APIBase):
    selectionId: int
    handicap: float
    limitOrder: LimitOrder


class InstructionReport(APIBase):
    status: STATUS
    instruction: Instruction
    betId: Optional[str] = None
    placedDate: Optional[str] = None
    averagePriceMatched: Optional[float] = None
    sizeMatched: Optional[float] = None
    orderStatus: Optional[ORDER_STATUS] = None


class PlaceResult(APIBase):
    customerRef: str
    status: STATUS
    marketId: str
    instructionReports: Optional[List[InstructionReport]]


class PlaceResultResponse(RequestBase, kw_only=True):  # type: ignore
    result: PlaceResult


class ReplaceResultResponse(RequestBase, kw_only=True):  # type: ignore
    result: PlaceResult


__all__ = ["placeOrders", "cancelOrders", "replaceOrders"]
