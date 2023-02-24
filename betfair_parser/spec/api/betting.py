from typing import List, Literal, Optional, Union

from betfair_parser.constants import OrderResponse, OrderSide, OrderStatus, OrderType
from betfair_parser.spec.api.core import RequestBase
from betfair_parser.spec.common import BaseMessage


# ------------ ORDER TYPES ------------ #


class LimitOrder(BaseMessage):
    size: Union[str, float]
    price: Union[str, float]
    persistenceType: Literal["PERSIST"]


class MarketOnCloseOrder(BaseMessage):
    liability: str


# ------------ REQUESTS ------------ #


class placeInstructions(BaseMessage):
    selectionId: str
    handicap: str
    customerOrderRef: str
    orderType: OrderType
    side: OrderSide
    limitOrder: Optional[LimitOrder] = None
    marketOnCloseOrder: Optional[MarketOnCloseOrder] = None


class placeOrdersParams(BaseMessage):
    marketId: str
    instructions: List[placeInstructions]
    customerRef: Optional[str]
    customerStrategyRef: Optional[str]


class placeOrders(RequestBase, kw_only=True):
    params: placeOrdersParams
    method: Literal["SportsAPING/v1.0/placeOrders"] = "SportsAPING/v1.0/placeOrders"


class cancelOrdersInstructions(BaseMessage):
    betId: str


class cancelOrdersParams(BaseMessage):
    marketId: str
    instructions: List[cancelOrdersInstructions]
    customerRef: str


class cancelOrders(RequestBase, kw_only=True):
    method: Literal["SportsAPING/v1.0/cancelOrders"] = "SportsAPING/v1.0/cancelOrders"
    params: cancelOrdersParams


class replaceOrdersInstructions(BaseMessage):
    betId: str
    newPrice: float


class replaceOrdersParams(BaseMessage):
    marketId: str
    instructions: List[replaceOrdersInstructions]
    customerRef: str


class replaceOrders(RequestBase, kw_only=True):
    method: Literal["SportsAPING/v1.0/replaceOrders"] = "SportsAPING/v1.0/replaceOrders"
    params: replaceOrdersParams


# ------------ RESPONSES ------------ #


class Instruction(BaseMessage):
    selectionId: int
    handicap: float
    limitOrder: LimitOrder
    customerOrderRef: str
    orderType: OrderType
    side: OrderSide


class InstructionReport(BaseMessage):
    status: OrderResponse
    instruction: Instruction
    errorCode: Optional[str] = None
    betId: Optional[str] = None
    placedDate: Optional[str] = None
    averagePriceMatched: Optional[float] = None
    sizeMatched: Optional[float] = None
    orderStatus: Optional[OrderStatus] = None


class PlaceResult(BaseMessage):
    customerRef: str
    status: OrderResponse
    marketId: str
    instructionReports: Optional[List[InstructionReport]]
    errorCode: Optional[str] = None


class PlaceResultResponse(RequestBase, kw_only=True):
    result: PlaceResult


class ReplaceResultResponse(RequestBase, kw_only=True):
    result: PlaceResult


__all__ = ["placeOrders", "cancelOrders", "replaceOrders"]
