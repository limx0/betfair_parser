from typing import Optional

import msgspec

from betfair_parser.spec.betting.enums import BetStatus, GroupBy, OrderBy, OrderProjection, Side, SortDir
from betfair_parser.spec.betting.type_definitions import (
    CancelExecutionReport,
    CancelInstruction,
    ClearedOrderSummaryReport,
    CurrentOrderSummaryReport,
    MarketVersion,
    PlaceExecutionReport,
    PlaceInstruction,
    ReplaceExecutionReport,
    ReplaceInstruction,
    RunnerId,
    UpdateExecutionReport,
    UpdateInstruction,
)
from betfair_parser.spec.common import (
    BaseMessage,
    BetId,
    CustomerOrderRef,
    CustomerRef,
    CustomerStrategyRef,
    EventId,
    EventTypeId,
    MarketId,
    Request,
    Response,
    TimeRange,
)


class placeOrdersParams(BaseMessage, frozen=True):
    marketId: str
    instructions: list[PlaceInstruction]
    customerRef: Optional[CustomerRef] = None
    marketVersion: Optional[MarketVersion] = None
    customerStrategyRef: Optional[CustomerStrategyRef] = None
    async_: Optional[bool] = msgspec.field(name="async", default=False)


class placeOrders(Request, kw_only=True, frozen=True):
    """Place new orders into market.

    Please note that additional bet sizing rules apply to bets placed into the Italian Exchange.

    In normal circumstances the placeOrders is an atomic operation. PLEASE NOTE: if the
    'Best Execution' features is switched off, placeOrders can return ‘PROCESSED_WITH_ERRORS’
    meaning that some bets can be rejected and other placed when submitted in the same
    PlaceInstruction.
    """

    method = "SportsAPING/v1.0/placeOrders"
    params: placeOrdersParams
    return_type = Response[PlaceExecutionReport]


class cancelOrdersParams(BaseMessage, frozen=True):
    marketId: Optional[str] = None
    instructions: Optional[list[CancelInstruction]] = None
    customerRef: Optional[CustomerRef] = None


class cancelOrders(Request, kw_only=True, frozen=True):
    """
    Cancel all bets OR cancel all bets on a market OR fully or partially cancel particular
    orders on a market. Only LIMIT orders can be cancelled or partially cancelled once placed.
    """

    method = "SportsAPING/v1.0/cancelOrders"
    params: cancelOrdersParams
    return_type = Response[CancelExecutionReport]


class replaceOrdersParams(BaseMessage, frozen=True):
    marketId: str
    instructions: list[ReplaceInstruction]
    customerRef: Optional[CustomerRef] = None
    marketVersion: Optional[MarketVersion] = None
    async_: Optional[bool] = msgspec.field(name="async", default=False)


class replaceOrders(Request, kw_only=True, frozen=True):
    """
    This operation is logically a bulk cancel followed by a bulk place. The cancel is completed
    first then the new orders are placed. The new orders will be placed atomically in that they
    will all be placed or none will be placed. In the case where the new orders cannot be placed
    the cancellations will not be rolled back. See ReplaceInstruction.
    """

    method = "SportsAPING/v1.0/replaceOrders"
    params: replaceOrdersParams
    return_type = Response[ReplaceExecutionReport]


class listClearedOrdersParams(BaseMessage, frozen=True):
    betStatus: BetStatus  # Restricts the results to the specified status.
    eventTypeIds: Optional[set[EventTypeId]] = None  # Restricts the results to the specified Event Type IDs.
    eventIds: Optional[set[EventId]] = None  # Restricts the results to the specified Event IDs.
    marketIds: Optional[set[MarketId]] = None  # Restricts the results to the specified market IDs.
    runnerIds: Optional[set[RunnerId]] = None  # Restricts the results to the specified Runners.
    betIds: Optional[set[BetId]] = None  # Restricts the results to the specified bet IDs, maximum 1000 betIds
    customerOrderRefs: Optional[set[CustomerOrderRef]] = None
    customerStrategyRefs: Optional[set[CustomerStrategyRef]] = None
    side: Optional[Side] = None  # Restricts the results to the specified side.

    # Optionally restricts the results to be from/to the specified settled date. This date is inclusive,
    # i.e. if an order was cleared on exactly this date (to the millisecond) then it will be included
    # in the results. If the from is later than the to, no results will be returned.
    # Please Note: if you have a longer running market that is settled at multiple different times
    # then there is no way to get the returned market rollup to only include bets settled in a certain
    # date range, it will always return the overall position from the market including all settlements.
    settledDateRange: Optional[TimeRange] = None

    # If not supplied then the lowest level is returned, i.e. bet by bet This is only applicable to SETTLED BetStatus.
    groupBy: Optional[GroupBy] = None
    includeItemDescription: Optional[bool] = None
    locale: Optional[str] = None  # The language used for the itemDescription, defaults to account settings
    fromRecord: Optional[int] = None  # Specifies the first record that will be returned. Records start at index zero.
    recordCount: Optional[int] = None  # Number of records from the index position 'fromRecord', maximum 1000


class listClearedOrders(Request, kw_only=True, frozen=True):
    """
    Returns a list of settled bets based on the bet status, ordered by settled date. To retrieve
    more than 1000 records, you need to make use of the fromRecord and recordCount parameters.

    By default the service will return all available data for the last 90 days (see Best Practice
    note below).  The fields available at each roll-up are available here

    Best Practice:
    You should specify a settledDateRange "from" date when making requests for data. This reduces
    the amount of data that requires downloading & improves the speed of the response. Specifying
    a "from" date of the last call will ensure that only new data is returned.
    """

    method = "SportsAPING/v1.0/listClearedOrders"
    params: listClearedOrdersParams
    return_type = Response[ClearedOrderSummaryReport]


class listCurrentOrdersParams(BaseMessage, frozen=True):
    """
    Parameters for retrieving a list of current orders.
    """

    betIds: Optional[set[BetId]] = None  # Restricts the results to the specified bet IDs
    marketIds: Optional[set[str]] = None  # Restricts the results to the specified market IDs
    orderProjection: Optional[OrderProjection] = None  # Restricts the results to the specified order status
    customerOrderRefs: Optional[set[CustomerOrderRef]] = None
    customerStrategyRefs: Optional[set[CustomerStrategyRef]] = None
    dateRange: Optional[TimeRange] = None  # Restricts the results to be from/to the specified date
    orderBy: Optional[OrderBy] = None  # Specifies how the results will be ordered
    sortDir: Optional[SortDir] = None  # Specifies the direction the results will be sorted in
    fromRecord: Optional[int] = None  # Specifies the first record that will be returned
    recordCount: Optional[int] = None  # Specifies how many records will be returned
    includeItemDescription: Optional[bool] = None


class listCurrentOrders(Request, kw_only=True, frozen=True):
    """
    Returns a list of your current orders. Optionally you can filter and sort your current orders
    using the various parameters, setting none of the parameters will return all of your current
    orders up to a maximum of 1000 bets, ordered BY_BET and sorted EARLIEST_TO_LATEST. To retrieve
    more than 1000 orders, you need to make use of the fromRecord and recordCount parameters.

    Best Practice:
    To efficiently track new bet matches from a specific time, customers should use a combination of
    the dateRange, orderBy "BY_MATCH_TIME" and orderProjection “ALL” to filter fully/partially matched
    orders from the list of returned bets. The response will then filter out any bet records that
    have no matched date and provide a list of betIds in the order which they are fully/partially
    matched from the date and time specified in the dateRange field.
    """

    method = "SportsAPING/v1.0/listCurrentOrders"
    params: listCurrentOrdersParams
    return_type = Response[CurrentOrderSummaryReport]


class updateOrdersParams(BaseMessage, frozen=True):
    marketId: str  # The market id these orders are to be placed on
    instructions: list[UpdateInstruction]  # The limit of update instructions per request is 60
    customerRef: Optional[CustomerRef] = None


class updateOrders(Request, kw_only=True, frozen=True):
    """Update non-exposure changing fields."""

    method = "SportsAPING/v1.0/updateOrders"
    params: updateOrdersParams
    return_type = Response[UpdateExecutionReport]
