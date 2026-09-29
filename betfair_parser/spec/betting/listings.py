from typing import Annotated

from betfair_parser.spec.betting.enums import (
    MarketProjection,
    MarketSort,
    MatchProjection,
    OrderProjection,
    TimeGranularity,
)
from betfair_parser.spec.betting.type_definitions import (
    CompetitionResult,
    CountryCodeResult,
    EventResult,
    EventTypeResult,
    MarketBook,
    MarketCatalogue,
    MarketFilter,
    MarketProfitAndLoss,
    MarketTypeResult,
    PriceProjection,
    TimeRangeResult,
    VenueResult,
    betting_tag,
)
from betfair_parser.spec.common import (
    BetId,
    Date,
    EndpointType,
    Handicap,
    MarketId,
    Params,
    Request,
    Response,
    SelectionId,
    Set,
    doc,
)


class _ListingParams(Params, frozen=True):
    filter: MarketFilter
    locale: str | None = None


class _ListingRequest(Request, kw_only=True, frozen=True, tag=betting_tag):
    endpoint_type = EndpointType.BETTING


class ListCompetitions(_ListingRequest, kw_only=True, frozen=True):
    """
    Returns a list of Competitions (i.e., World Cup 2013) associated with the markets selected by
    the MarketFilter. Currently only Football markets have an associated competition.
    """

    params: _ListingParams
    return_type = Response[list[CompetitionResult]]


class ListCountries(_ListingRequest, kw_only=True, frozen=True):
    """
    Returns a list of Countries associated with the markets selected by the MarketFilter.
    """

    params: _ListingParams
    return_type = Response[list[CountryCodeResult]]


class ListEvents(_ListingRequest, kw_only=True, frozen=True):
    """
    Returns a list of Events (i.e, Reading vs. Man United) associated with the markets selected
    by the MarketFilter.
    """

    params: _ListingParams
    return_type = Response[list[EventResult]]


class ListEventTypes(_ListingRequest, kw_only=True, frozen=True):
    """
    Returns a list of Event Types (i.e. Sports) associated with the markets selected by the
    MarketFilter.
    """

    params: _ListingParams
    return_type = Response[list[EventTypeResult]]


class ListMarketTypes(_ListingRequest, kw_only=True, frozen=True):
    """
    Returns a list of market types (i.e. MATCH_ODDS, NEXT_GOAL) associated with the markets selected
    by the MarketFilter. The market types are always the same, regardless of locale.
    """

    params: _ListingParams
    return_type = Response[list[MarketTypeResult]]


class ListVenues(_ListingRequest, kw_only=True, frozen=True):
    """
    Returns a list of Venues (i.e. Cheltenham, Ascot) associated with the markets selected by the
    MarketFilter. Currently, only Horse Racing markets are associated with a Venue.
    """

    params: _ListingParams
    return_type = Response[list[VenueResult]]


# More complex listings


class _ListMarketBookParams(Params, frozen=True):
    market_ids: Annotated[
        Set[MarketId],
        doc("NOTE: This is documented as list, but defined as set here for consistency"),
    ]
    price_projection: Annotated[PriceProjection | None, doc("The desired projection of price data")] = None
    order_projection: Annotated[OrderProjection | None, doc("The orders you want to receive in the response")] = None
    match_projection: Annotated[
        MatchProjection | None,
        doc("If you ask for orders, specifies the representation of matches"),
    ] = None
    include_overall_position: Annotated[
        bool | None,
        doc("If you ask for orders, returns matches for each selection"),
    ] = None
    partition_matched_by_strategy_ref: Annotated[
        bool | None,
        doc("Breakdown of matches by strategy for each selection"),
    ] = None
    customer_strategy_refs: Set[str] | None = None
    currency_code: Annotated[str | None, doc("A Betfair standard currency code")] = None
    locale: Annotated[str | None, doc("The language used for the response")] = None
    matched_since: Annotated[
        Date | None,
        doc("Only orders with at least one fragment matched since the specified date"),
    ] = None
    bet_ids: Annotated[Set[BetId] | None, doc("Only orders with the specified bet IDs")] = None


class ListMarketBook(_ListingRequest, kw_only=True, frozen=True):
    """
    Returns a list of dynamic data about markets. Dynamic data includes prices, the status of the
    market, the status of selections, the traded volume, and the status of any orders you have
    placed in the market.

    Please note: Separate requests should be made for OPEN & CLOSED markets. Request that include
    both OPEN & CLOSED markets will only return those markets that are OPEN.

    Best Practice:
    Customers seeking to use listMarketBook to obtain price, volume, unmatched (EXECUTABLE) orders
    and matched position in a single operation should provide an OrderProjection of “EXECUTABLE” in
    their listMarketBook request and receive all unmatched (EXECUTABLE) orders and the aggregated
    matched volume from all orders irrespective of whether they are partially or fully matched.
    The level of matched volume aggregation (MatchProjection) requested should be
    ROLLED_UP_BY_AVG_PRICE or ROLLED_UP_BY_PRICE, the former being preferred. This provides a single
    call in which you can track prices, traded volume, unmatched orders and your evolving matched
    position with a reasonably fixed, minimally sized response.
    """

    params: _ListMarketBookParams
    return_type = Response[list[MarketBook]]


class _ListMarketCatalogueParams(Params, kw_only=True, frozen=True):
    filter: Annotated[MarketFilter, doc("The filter to select desired markets")]
    market_projection: Annotated[
        Set[MarketProjection] | None,
        doc("The type and amount of data returned about the market"),
    ] = None
    sort: Annotated[MarketSort | None, doc("The order of the results, defaults to RANK")] = None
    max_results: Annotated[int, doc("Limit on the total number of results returned")] = 1000
    locale: Annotated[str | None, doc("The language used for the response")] = None


class ListMarketCatalogue(_ListingRequest, kw_only=True, frozen=True):
    """
    Returns a list of information about published (ACTIVE/SUSPENDED) markets that does not change
    (or changes very rarely). You use listMarketCatalogue to retrieve the name of the market, the
    names of selections and other information about markets. Market Data Request Limits apply to
    requests made to listMarketCatalogue.

    Please note: listMarketCatalogue does not return markets that are CLOSED.
    """

    params: _ListMarketCatalogueParams
    return_type = Response[list[MarketCatalogue]]


# Comfort alias: betfair's official operation name is "listMarketCatalogue", but "catalog"
# is a common enough spelling that both are supported permanently - neither is deprecated.
ListMarketCatalog = ListMarketCatalogue


class _ListMarketProfitAndLossParams(Params, frozen=True):
    market_ids: Annotated[Set[MarketId], doc("List of markets to calculate profit and loss")]
    include_settled_bets: Annotated[
        bool | None,
        doc("Option to include settled bets (partially settled markets only)"),
    ] = False
    include_bsp_bets: Annotated[bool | None, doc("Option to include BSP bets")] = False
    net_of_commission: Annotated[
        bool | None,
        doc("Option to return profit and loss net of users current commission rate"),
    ] = False


class ListMarketProfitAndLoss(_ListingRequest, kw_only=True, frozen=True):
    """Returns a list of Countries associated with the markets selected by the MarketFilter."""

    params: _ListMarketProfitAndLossParams
    return_type = Response[list[MarketProfitAndLoss]]


class _ListRunnerBookParams(Params, frozen=True):
    market_id: Annotated[MarketId, doc("The unique id for the market")]
    selection_id: Annotated[SelectionId, doc("The unique id for the selection in the market")]
    handicap: Annotated[
        Handicap | None,
        doc(
            "If specified, the handicap is used in conjunction with the selectionId to pick which "
            "runner to return prices for"
        ),
    ] = None
    price_projection: PriceProjection | None = None
    order_projection: OrderProjection | None = None
    match_projection: Annotated[
        MatchProjection | None,
        doc("If you ask for orders, specifies the representation of matches"),
    ] = None
    include_overall_position: Annotated[
        bool | None,
        doc("If you ask for orders, returns matches for each selection"),
    ] = None
    partition_matched_by_strategy_ref: Annotated[bool | None, doc("Return a breakdown of matches by strategy")] = None
    customer_strategy_refs: Set[str] | None = None
    currency_code: Annotated[str | None, doc("A Betfair standard currency code")] = None
    locale: Annotated[str | None, doc("The language used for the response")] = None
    matched_since: Annotated[
        Date | None,
        doc("Restricts to orders with at least one fragment matched since specified date"),
    ] = None
    bet_ids: Annotated[Set[BetId] | None, doc("Restricts to orders with the specified bet IDs")] = None


class ListRunnerBook(_ListingRequest, kw_only=True, frozen=True):
    """
    Returns a list of dynamic data about a market and a specified runner. Dynamic data includes
    prices, the status of the market, the status of selections, the traded volume, and the status
    of any orders you have placed in the market.
    """

    params: _ListRunnerBookParams
    return_type = Response[list[MarketBook]]


class _ListTimeRangesParams(Params, frozen=True):
    filter: Annotated[
        MarketFilter,
        doc("The filter to select desired markets. All markets that match the criteria in the filter are selected."),
    ]
    granularity: Annotated[
        TimeGranularity,
        doc("The granularity of time periods that correspond to markets selected by the market filter."),
    ]


class ListTimeRanges(_ListingRequest, kw_only=True, frozen=True):
    """
    Returns a list of time ranges in the granularity specified in the request (i.e. 3PM to 4PM,
    Aug 14th to Aug 15th) associated with the markets selected by the MarketFilter.
    """

    params: _ListTimeRangesParams
    return_type = Response[list[TimeRangeResult]]
