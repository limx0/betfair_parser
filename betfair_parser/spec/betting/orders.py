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
    BetId,
    CustomerOrderRef,
    CustomerRef,
    CustomerStrategyRef,
    EndpointType,
    EventId,
    EventTypeId,
    MarketId,
    Params,
    Request,
    Response,
    TimeRange,
)


class OrderRequest(Request, frozen=True):
    endpoint_type = EndpointType.BETTING


class _PlaceOrdersParams(Params, frozen=True):
    market_id: str
    instructions: list[PlaceInstruction]
    customer_ref: Optional[CustomerRef] = None
    market_version: Optional[MarketVersion] = None
    customer_strategy_ref: Optional[CustomerStrategyRef] = None
    async_: Optional[bool] = msgspec.field(name="async", default=False)


class PlaceOrders(OrderRequest, kw_only=True, frozen=True):
    """Place new orders into market.

    Please note that additional bet sizing rules apply to bets placed into the Italian Exchange.

    In normal circumstances the placeOrders is an atomic operation. PLEASE NOTE: if the
    'Best Execution' features is switched off, placeOrders can return ‘PROCESSED_WITH_ERRORS’
    meaning that some bets can be rejected and other placed when submitted in the same
    PlaceInstruction.
    """

    method = "SportsAPING/v1.0/placeOrders"
    params: _PlaceOrdersParams
    return_type = Response[PlaceExecutionReport]


class _CancelOrdersParams(Params, frozen=True):
    market_id: Optional[str] = None
    instructions: Optional[list[CancelInstruction]] = None
    customer_ref: Optional[CustomerRef] = None


class CancelOrders(OrderRequest, kw_only=True, frozen=True):
    """
    Cancel all bets OR cancel all bets on a market OR fully or partially cancel particular
    orders on a market. Only LIMIT orders can be cancelled or partially cancelled once placed.
    """

    method = "SportsAPING/v1.0/cancelOrders"
    params: _CancelOrdersParams
    return_type = Response[CancelExecutionReport]


class _ReplaceOrdersParams(Params, frozen=True):
    market_id: str
    instructions: list[ReplaceInstruction]
    customer_ref: Optional[CustomerRef] = None
    market_version: Optional[MarketVersion] = None
    async_: Optional[bool] = msgspec.field(name="async", default=False)


class ReplaceOrders(OrderRequest, kw_only=True, frozen=True):
    """
    This operation is logically a bulk cancel followed by a bulk place. The cancel is completed
    first then the new orders are placed. The new orders will be placed atomically in that they
    will all be placed or none will be placed. In the case where the new orders cannot be placed
    the cancellations will not be rolled back. See ReplaceInstruction.
    """

    method = "SportsAPING/v1.0/replaceOrders"
    params: _ReplaceOrdersParams
    return_type = Response[ReplaceExecutionReport]


class _ListClearedOrdersParams(Params, frozen=True):
    bet_status: BetStatus  # Restricts the results to the specified status.
    event_type_ids: Optional[set[EventTypeId]] = None  # Restricts the results to the specified Event Type IDs.
    event_ids: Optional[set[EventId]] = None  # Restricts the results to the specified Event IDs.
    market_ids: Optional[set[MarketId]] = None  # Restricts the results to the specified market IDs.
    runner_ids: Optional[set[RunnerId]] = None  # Restricts the results to the specified Runners.
    bet_ids: Optional[set[BetId]] = None  # Restricts the results to the specified bet IDs, maximum 1000 betIds
    customer_order_refs: Optional[set[CustomerOrderRef]] = None
    customer_strategy_refs: Optional[set[CustomerStrategyRef]] = None
    side: Optional[Side] = None  # Restricts the results to the specified side.

    # Optionally restricts the results to be from/to the specified settled date. This date is inclusive,
    # i.e. if an order was cleared on exactly this date (to the millisecond) then it will be included
    # in the results. If the from is later than the to, no results will be returned.
    # Please Note: if you have a longer running market that is settled at multiple different times
    # then there is no way to get the returned market rollup to only include bets settled in a certain
    # date range, it will always return the overall position from the market including all settlements.
    settled_date_range: Optional[TimeRange] = None

    # If not supplied then the lowest level is returned, i.e. bet by bet This is only applicable to SETTLED BetStatus.
    group_by: Optional[GroupBy] = None
    include_item_description: Optional[bool] = None
    locale: Optional[str] = None  # The language used for the itemDescription, defaults to account settings
    from_record: Optional[int] = None  # Specifies the first record that will be returned. Records start at index zero.
    record_count: Optional[int] = None  # Number of records from the index position 'fromRecord', maximum 1000


class ListClearedOrders(OrderRequest, kw_only=True, frozen=True):
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
    params: _ListClearedOrdersParams
    return_type = Response[ClearedOrderSummaryReport]


class _ListCurrentOrdersParams(Params, frozen=True):
    """
    Parameters for retrieving a list of current orders.
    """

    bet_ids: Optional[set[BetId]] = None  # Restricts the results to the specified bet IDs
    market_ids: Optional[set[str]] = None  # Restricts the results to the specified market IDs
    order_projection: Optional[OrderProjection] = None  # Restricts the results to the specified order status
    customer_order_refs: Optional[set[CustomerOrderRef]] = None
    customer_strategy_refs: Optional[set[CustomerStrategyRef]] = None
    date_range: Optional[TimeRange] = None  # Restricts the results to be from/to the specified date
    order_by: Optional[OrderBy] = None  # Specifies how the results will be ordered
    sort_dir: Optional[SortDir] = None  # Specifies the direction the results will be sorted in
    from_record: Optional[int] = None  # Specifies the first record that will be returned
    record_count: Optional[int] = None  # Specifies how many records will be returned
    include_item_description: Optional[bool] = None


class ListCurrentOrders(OrderRequest, kw_only=True, frozen=True):
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
    params: _ListCurrentOrdersParams
    return_type = Response[CurrentOrderSummaryReport]


class _UpdateOrdersParams(Params, frozen=True):
    market_id: str  # The market id these orders are to be placed on
    instructions: list[UpdateInstruction]  # The limit of update instructions per request is 60
    customer_ref: Optional[CustomerRef] = None


class UpdateOrders(OrderRequest, kw_only=True, frozen=True):
    """Update non-exposure changing fields."""

    method = "SportsAPING/v1.0/updateOrders"
    params: _UpdateOrdersParams
    return_type = Response[UpdateExecutionReport]
