from typing import Literal

import msgspec

from betfair_parser.spec.betting.type_definitions import (
    CancelExecutionReport,
    CancelInstruction,
    MarketVersion,
    PlaceExecutionReport,
    PlaceInstruction,
    ReplaceExecutionReport,
    ReplaceInstruction,
)
from betfair_parser.spec.common import BaseMessage, RequestBase, Response


class placeOrdersParams(BaseMessage, frozen=True):
    marketId: str
    instructions: list[PlaceInstruction]
    customerRef: str | None = None
    marketVersion: MarketVersion | None = None
    customerStrategyRef: str | None = None
    async_: bool = msgspec.field(name="async", default=False)


class placeOrders(RequestBase, kw_only=True, frozen=True):
    method: Literal["SportsAPING/v1.0/placeOrders"] = "SportsAPING/v1.0/placeOrders"
    params: placeOrdersParams
    return_type = Response[PlaceExecutionReport]


class cancelOrdersParams(BaseMessage, frozen=True):
    marketId: str | None = None
    instructions: list[CancelInstruction] | None = None
    customerRef: str | None = None


class cancelOrders(RequestBase, kw_only=True, frozen=True):
    """
    Cancel all bets OR cancel all bets on a market OR fully or partially cancel particular
    orders on a market. Only LIMIT orders can be cancelled or partially cancelled once placed.
    """

    method: Literal["SportsAPING/v1.0/cancelOrders"] = "SportsAPING/v1.0/cancelOrders"
    params: cancelOrdersParams
    return_type = Response[CancelExecutionReport]


class replaceOrdersParams(BaseMessage, frozen=True):
    marketId: str
    instructions: list[ReplaceInstruction]
    customerRef: str | None = None
    marketVersion: MarketVersion | None = None
    async_: bool = msgspec.field(name="async", default=False)


class replaceOrders(RequestBase, kw_only=True, frozen=True):
    """
    This operation is logically a bulk cancel followed by a bulk place. The cancel is completed
    first then the new orders are placed. The new orders will be placed atomically in that they
    will all be placed or none will be placed. In the case where the new orders cannot be placed
    the cancellations will not be rolled back. See ReplaceInstruction.
    """

    method: Literal["SportsAPING/v1.0/replaceOrders"] = "SportsAPING/v1.0/replaceOrders"
    params: replaceOrdersParams
    return_type = Response[ReplaceExecutionReport]
