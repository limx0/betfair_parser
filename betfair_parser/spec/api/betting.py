from typing import List, Literal, Optional, Union

from betfair_parser.spec.api.core import RequestBase
from betfair_parser.spec.common import BaseMessage
from betfair_parser.spec.constants import OrderResponse, OrderSide, OrderStatus, OrderType


# ------------ ORDER TYPES ------------ #


class LimitOrder(BaseMessage, frozen=True):
    size: Union[str, float]
    price: Union[str, float]
    persistenceType: Literal["PERSIST"]


class MarketOnCloseOrder(BaseMessage, frozen=True):
    liability: str


# ------------ REQUESTS ------------ #


class placeInstructions(BaseMessage, frozen=True):
    selectionId: str
    handicap: str
    customerOrderRef: str
    orderType: OrderType
    side: OrderSide
    limitOrder: Optional[LimitOrder] = None
    marketOnCloseOrder: Optional[MarketOnCloseOrder] = None


class placeOrdersParams(BaseMessage, frozen=True):
    marketId: str
    instructions: List[placeInstructions]
    customerRef: Optional[str]
    customerStrategyRef: Optional[str]


class placeOrders(RequestBase, kw_only=True, frozen=True):
    params: placeOrdersParams
    method: Literal["SportsAPING/v1.0/placeOrders"] = "SportsAPING/v1.0/placeOrders"


class cancelOrdersInstructions(BaseMessage, frozen=True):
    betId: str


class cancelOrdersParams(BaseMessage, frozen=True):
    marketId: str
    instructions: List[cancelOrdersInstructions]
    customerRef: str


class cancelOrders(RequestBase, kw_only=True, frozen=True):
    method: Literal["SportsAPING/v1.0/cancelOrders"] = "SportsAPING/v1.0/cancelOrders"
    params: cancelOrdersParams


class replaceOrdersInstructions(BaseMessage, frozen=True):
    betId: str
    newPrice: float


class replaceOrdersParams(BaseMessage, frozen=True):
    marketId: str
    instructions: List[replaceOrdersInstructions]
    customerRef: str


class replaceOrders(RequestBase, kw_only=True, frozen=True):
    method: Literal["SportsAPING/v1.0/replaceOrders"] = "SportsAPING/v1.0/replaceOrders"
    params: replaceOrdersParams


# ------------ RESPONSES ------------ #


class Instruction(BaseMessage, frozen=True):
    selectionId: int
    handicap: float
    limitOrder: LimitOrder
    customerOrderRef: str
    orderType: OrderType
    side: OrderSide


class InstructionReport(BaseMessage, frozen=True):
    status: OrderResponse
    instruction: Instruction
    errorCode: Optional[str] = None
    betId: Optional[str] = None
    placedDate: Optional[str] = None
    averagePriceMatched: Optional[float] = None
    sizeMatched: Optional[float] = None
    orderStatus: Optional[OrderStatus] = None


class PlaceResult(BaseMessage, frozen=True):
    customerRef: str
    status: OrderResponse
    marketId: str
    instructionReports: Optional[List[InstructionReport]]
    errorCode: Optional[str] = None


class PlaceResultResponse(RequestBase, kw_only=True, frozen=True):
    result: PlaceResult


class ReplaceResultResponse(RequestBase, kw_only=True, frozen=True):
    result: PlaceResult


__all__ = ["placeOrders", "cancelOrders", "replaceOrders"]
