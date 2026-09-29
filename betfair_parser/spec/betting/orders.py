from typing import Annotated

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
    betting_tag,
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
    Set,
    TimeRange,
    doc,
)


class _OrderRequest(Request, frozen=True, tag=betting_tag):
    endpoint_type = EndpointType.BETTING


class _PlaceOrdersParams(Params, frozen=True):
    market_id: str
    instructions: list[PlaceInstruction]
    customer_ref: CustomerRef | None = None
    market_version: MarketVersion | None = None
    customer_strategy_ref: CustomerStrategyRef | None = None
    async_: bool | None = msgspec.field(name="async", default=False)


class PlaceOrders(_OrderRequest, kw_only=True, frozen=True):
    """Place new orders into market.

    Please note that additional bet sizing rules apply to bets placed into the Italian Exchange.

    In normal circumstances the placeOrders is an atomic operation. PLEASE NOTE: if the
    'Best Execution' features is switched off, placeOrders can return 'PROCESSED_WITH_ERRORS'
    meaning that some bets can be rejected and other placed when submitted in the same
    PlaceInstruction.
    """

    params: _PlaceOrdersParams
    return_type = Response[PlaceExecutionReport]


class _CancelOrdersParams(Params, frozen=True):
    market_id: str | None = None
    instructions: list[CancelInstruction] | None = None
    customer_ref: CustomerRef | None = None


class CancelOrders(_OrderRequest, kw_only=True, frozen=True):
    """
    Cancel all bets OR cancel all bets on a market OR fully or partially cancel particular
    orders on a market. Only LIMIT orders can be cancelled or partially cancelled once placed.
    """

    params: _CancelOrdersParams
    return_type = Response[CancelExecutionReport]


class _ReplaceOrdersParams(Params, frozen=True):
    market_id: str
    instructions: list[ReplaceInstruction]
    customer_ref: CustomerRef | None = None
    market_version: MarketVersion | None = None
    async_: bool | None = msgspec.field(name="async", default=False)


class ReplaceOrders(_OrderRequest, kw_only=True, frozen=True):
    """
    This operation is logically a bulk cancel followed by a bulk place. The cancel is completed
    first then the new orders are placed. The new orders will be placed atomically in that they
    will all be placed or none will be placed. In the case where the new orders cannot be placed
    the cancellations will not be rolled back. See ReplaceInstruction.
    """

    params: _ReplaceOrdersParams
    return_type = Response[ReplaceExecutionReport]


class _ListClearedOrdersParams(Params, frozen=True):
    bet_status: Annotated[BetStatus, doc("Restricts the results to the specified status.")]
    event_type_ids: Annotated[
        Set[EventTypeId] | None,
        doc("Restricts the results to the specified Event Type IDs."),
    ] = None
    event_ids: Annotated[Set[EventId] | None, doc("Restricts the results to the specified Event IDs.")] = None
    market_ids: Annotated[Set[MarketId] | None, doc("Restricts the results to the specified market IDs.")] = None
    runner_ids: Annotated[Set[RunnerId] | None, doc("Restricts the results to the specified Runners.")] = None
    bet_ids: Annotated[
        Set[BetId] | None,
        doc("Restricts the results to the specified bet IDs, maximum 1000 betIds"),
    ] = None
    customer_order_refs: Set[CustomerOrderRef] | None = None
    customer_strategy_refs: Set[CustomerStrategyRef] | None = None
    side: Annotated[Side | None, doc("Restricts the results to the specified side.")] = None

    settled_date_range: Annotated[
        TimeRange | None,
        doc(
            "Optionally restricts the results to be from/to the specified settled date. This date is inclusive, i.e. "
            "if an order was cleared on exactly this date (to the millisecond) then it will be included in the "
            "results. If 'from' is later than 'to', no results will be returned. Please Note: if you have a longer "
            "running market that is settled at multiple different times then there is no way to get the returned "
            "market rollup to only include bets settled in a certain date range, it will always return the overall "
            "position from the market including all settlements."
        ),
    ] = None

    group_by: Annotated[
        GroupBy | None,
        doc(
            "If not supplied then the lowest level is returned, i.e. bet by bet This is only applicable to SETTLED "
            "BetStatus."
        ),
    ] = None
    include_item_description: bool | None = None
    locale: Annotated[str | None, doc("The language used for the itemDescription, defaults to account settings")] = None
    from_record: Annotated[
        int | None,
        doc("Specifies the first record that will be returned. Records start at index zero."),
    ] = None
    record_count: Annotated[
        int | None,
        doc("Number of records from the index position 'fromRecord', maximum 1000"),
    ] = None


class ListClearedOrders(_OrderRequest, kw_only=True, frozen=True):
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

    params: _ListClearedOrdersParams
    return_type = Response[ClearedOrderSummaryReport]


class _ListCurrentOrdersParams(Params, frozen=True):
    """
    Parameters for retrieving a list of current orders.
    """

    bet_ids: Annotated[Set[BetId] | None, doc("Restricts the results to the specified bet IDs")] = None
    market_ids: Annotated[Set[MarketId] | None, doc("Restricts the results to the specified market IDs")] = None
    order_projection: Annotated[
        OrderProjection | None,
        doc("Restricts the results to the specified order status"),
    ] = None
    customer_order_refs: Set[CustomerOrderRef] | None = None
    customer_strategy_refs: Set[CustomerStrategyRef] | None = None
    date_range: Annotated[TimeRange | None, doc("Restricts the results to be from/to the specified date")] = None
    order_by: Annotated[OrderBy | None, doc("Specifies how the results will be ordered")] = None
    sort_dir: Annotated[SortDir | None, doc("Specifies the direction the results will be sorted in")] = None
    from_record: Annotated[int | None, doc("Specifies the first record that will be returned")] = None
    record_count: Annotated[int | None, doc("Specifies how many records will be returned")] = None
    include_item_description: bool | None = None


class ListCurrentOrders(_OrderRequest, kw_only=True, frozen=True):
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

    params: _ListCurrentOrdersParams
    return_type = Response[CurrentOrderSummaryReport]


class _UpdateOrdersParams(Params, frozen=True):
    market_id: Annotated[str, doc("The market id these orders are to be placed on")]
    instructions: Annotated[list[UpdateInstruction], doc("The limit of update instructions per request is 60")]
    customer_ref: CustomerRef | None = None


class UpdateOrders(_OrderRequest, kw_only=True, frozen=True):
    """Update non-exposure changing fields."""

    params: _UpdateOrdersParams
    return_type = Response[UpdateExecutionReport]
