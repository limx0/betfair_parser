from typing import Optional

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
)
from betfair_parser.spec.common import BaseMessage, BetId, Date, MarketId, Request, Response, SelectionId


class _ListingParams(BaseMessage, frozen=True):
    filter: MarketFilter
    locale: Optional[str] = None


class ListCompetitions(Request, kw_only=True, frozen=True):
    """
    Returns a list of Competitions (i.e., World Cup 2013) associated with the markets selected by
    the MarketFilter. Currently only Football markets have an associated competition.
    """

    method = "SportsAPING/v1.0/listCompetitions"
    params: _ListingParams
    return_type = Response[list[CompetitionResult]]


class ListCountries(Request, kw_only=True, frozen=True):
    """
    Returns a list of Countries associated with the markets selected by the MarketFilter.
    """

    method = "SportsAPING/v1.0/listCountries"
    params: _ListingParams
    return_type = Response[list[CountryCodeResult]]


class ListEvents(Request, kw_only=True, frozen=True):
    """
    Returns a list of Events (i.e, Reading vs. Man United) associated with the markets selected
    by the MarketFilter.
    """

    method = "SportsAPING/v1.0/listEvents"
    params: _ListingParams
    return_type = Response[list[EventResult]]


class ListEventTypes(Request, kw_only=True, frozen=True):
    """
    Returns a list of Event Types (i.e. Sports) associated with the markets selected by the
    MarketFilter.
    """

    method = "SportsAPING/v1.0/listEventTypes"
    params: _ListingParams
    return_type = Response[list[EventTypeResult]]


class ListMarketTypes(Request, kw_only=True, frozen=True):
    """
    Returns a list of market types (i.e. MATCH_ODDS, NEXT_GOAL) associated with the markets selected
    by the MarketFilter. The market types are always the same, regardless of locale.
    """

    method = "SportsAPING/v1.0/listMarketTypes"
    params: _ListingParams
    return_type = Response[list[MarketTypeResult]]


class ListVenues(Request, kw_only=True, frozen=True):
    """
    Returns a list of Venues (i.e. Cheltenham, Ascot) associated with the markets selected by the
    MarketFilter. Currently, only Horse Racing markets are associated with a Venue.
    """

    method = "SportsAPING/v1.0/listVenues"
    params: _ListingParams
    return_type = Response[list[VenueResult]]


# More complex listings


class _ListMarketBookParams(BaseMessage, frozen=True):
    market_ids: list[str]  # One or more market ids
    price_projection: Optional[
        PriceProjection
    ] = None  # The projection of price data you want to receive in the response
    order_projection: Optional[OrderProjection] = None  # The orders you want to receive in the response
    match_projection: Optional[MatchProjection] = None  # If you ask for orders, specifies the representation of matches
    include_overall_position: Optional[bool] = None  # If you ask for orders, returns matches for each selection
    partition_matched_by_strategy_ref: Optional[
        bool
    ] = None  # Returns the breakdown of matches by strategy for each selection
    customer_strategy_refs: Optional[set[str]] = None
    currency_code: Optional[str] = None  # A Betfair standard currency code
    locale: Optional[str] = None  # The language used for the response
    matched_since: Optional[
        Date
    ] = None  # Restricts to orders with at least one fragment matched since the specified date
    bet_ids: Optional[set[BetId]] = None  # Restricts to orders with the specified bet IDs


class ListMarketBook(Request, kw_only=True, frozen=True):
    """
    Returns a list of dynamic data about markets. Dynamic data includes prices, the status of the
    market, the status of selections, the traded volume, and the status of any orders you have
    placed in the market.

    Please note: Separate requests should be made for OPEN & CLOSED markets. Request that include
    both OPEN & CLOSED markets will only return those markets that are OPEN.

    Best Practice:
    Customers seeking to use listMarketBook to obtain price, volume, unmatched (EXECUTABLE) orders
    and matched position in a single operation should provide an OrderProjectionof “EXECUTABLE” in
    their listMarketBook request and receive all unmatched (EXECUTABLE) orders and the aggregated
    matched volume from all orders irrespective of whether they are partially or fully matched.
    The level of matched volume aggregation (MatchProjection) requested should be
    ROLLED_UP_BY_AVG_PRICE or ROLLED_UP_BY_PRICE, the former being preferred. This provides a single
    call in which you can track prices, traded volume, unmatched orders and your evolving matched
    position with a reasonably fixed, minimally sized response.
    """

    method = "SportsAPING/v1.0/listMarketBook"
    params: _ListMarketBookParams
    return_type = Response[list[MarketBook]]


class _ListMarketCatalogueParams(BaseMessage, kw_only=True, frozen=True):
    filter: MarketFilter  # The filter to select desired markets
    market_projection: Optional[set[MarketProjection]] = None  # The type and amount of data returned about the market
    sort: Optional[MarketSort] = None  # The order of the results, defaults to RANK
    max_results: int  # Limit on the total number of results returned
    locale: Optional[str] = None  # The language used for the response


class ListMarketCatalogue(Request, kw_only=True, frozen=True):
    """
    Returns a list of information about published (ACTIVE/SUSPENDED) markets that does not change
    (or changes very rarely). You use listMarketCatalogue to retrieve the name of the market, the
    names of selections and other information about markets.  Market Data Request Limits apply to
    requests made to listMarketCatalogue.

    Please note: listMarketCatalogue does not return markets that are CLOSED.
    """

    method = "SportsAPING/v1.0/listMarketCatalogue"
    params: _ListMarketCatalogueParams
    return_type = Response[list[MarketCatalogue]]


class _ListMarketProfitAndLossParams(BaseMessage, frozen=True):
    market_ids: set[MarketId]  # List of markets to calculate profit and loss
    include_settled_bets: Optional[bool] = False  # Option to include settled bets (partially settled markets only)
    include_bsp_bets: Optional[bool] = False  # Option to include BSP bets
    net_of_commission: Optional[bool] = False  # Option to return profit and loss net of users current commission rate


class ListMarketProfitAndLoss(Request, kw_only=True, frozen=True):
    """Returns a list of Countries associated with the markets selected by the MarketFilter."""

    method = "SportsAPING/v1.0/listMarketProfitAndLoss"
    params: _ListMarketProfitAndLossParams
    return_type = Response[list[MarketProfitAndLoss]]


class _ListRunnerBookParams(BaseMessage, frozen=True):
    market_id: MarketId  # The unique id for the market
    selection_id: SelectionId  # The unique id for the selection in the market
    handicap: Optional[float] = None  # The handicap associated with the runner in case of Asian handicap market
    price_projection: Optional[PriceProjection] = None
    order_projection: Optional[OrderProjection] = None
    match_projection: Optional[MatchProjection] = None  # If you ask for orders, specifies the representation of matches
    include_overall_position: Optional[bool] = None  # If you ask for orders, returns matches for each selection
    partition_matched_by_strategy_ref: Optional[
        bool
    ] = None  # Return a breakdown of matches by strategy for each selection
    customer_strategy_refs: Optional[set[str]] = None
    currency_code: Optional[str] = None  # A Betfair standard currency code
    locale: Optional[str] = None  # The language used for the response
    matched_since: Optional[Date] = None  # Restricts to orders with at least one fragment matched since specified date
    bet_ids: Optional[set[BetId]] = None  # Restricts to orders with the specified bet IDs


class ListRunnerBook(Request, kw_only=True, frozen=True):
    """
    Returns a list of dynamic data about a market and a specified runner. Dynamic data includes
    prices, the status of the market, the status of selections, the traded volume, and the status
    of any orders you have placed in the market..
    """

    method = "SportsAPING/v1.0/listRunnerBook"
    params: _ListRunnerBookParams
    return_type = Response[list[MarketBook]]


class _ListTimeRangesParams(BaseMessage, frozen=True):
    # The filter to select desired markets. All markets that match the criteria in the filter are selected.
    filter: MarketFilter
    # The granularity of time periods that correspond to markets selected by the market filter.
    granularity: TimeGranularity


class ListTimeRanges(Request, kw_only=True, frozen=True):
    """
    Returns a list of time ranges in the granularity specified in the request (i.e. 3PM to 4PM,
    Aug 14th to Aug 15th) associated with the markets selected by the MarketFilter.
    """

    method = "SportsAPING/v1.0/listTimeRanges"
    params: _ListTimeRangesParams
    return_type = Response[list[TimeRangeResult]]
