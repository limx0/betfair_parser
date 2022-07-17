from typing import List, Literal, Optional

import msgspec

from betfair_parser.spec.api.core import APIBase


class LimitOrder(msgspec.Struct):
    size: str
    price: str
    persistenceType: Literal["PERSIST"]


class MarketOnCloseOrder(msgspec.Struct):
    liability: str


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


class placeOrders(APIBase):
    method: Literal["SportsAPING/v1.0/placeOrders"] = "SportsAPING/v1.0/placeOrders"
    params: placeOrdersParams


class cancelOrdersInstructions(msgspec.Struct):
    betId: str


class cancelOrdersParams(msgspec.Struct):
    marketId: str
    instructions: List[cancelOrdersInstructions]
    customerRef: str


class cancelOrders(APIBase):
    method: Literal["SportsAPING/v1.0/cancelOrders"] = "SportsAPING/v1.0/cancelOrders"
    params: cancelOrdersParams


class replaceOrdersInstructions(msgspec.Struct):
    betId: str
    newPrice: float


class replaceOrdersParams(msgspec.Struct):
    marketId: str
    instructions: List[replaceOrdersInstructions]
    customerRef: str


class replaceOrders(APIBase):
    method: Literal["SportsAPING/v1.0/replaceOrders"] = "SportsAPING/v1.0/replaceOrders"
    params: replaceOrdersParams


__all__ = ["placeOrders", "cancelOrders", "replaceOrders"]
