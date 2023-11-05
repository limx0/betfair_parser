from functools import partial

from betfair_parser.spec.common import BaseMessage, EndpointType, Params, Request, Response, method_tag
from betfair_parser.strenums import DocumentedEnum, doc


heartbeat_tag = partial(method_tag, "HeartbeatAPING/v1.0/")


class ActionPerformed(DocumentedEnum):
    NONE = doc("No action was performed since last heartbeat, or this is the first heartbeat")
    CANCELLATION_REQUEST_SUBMITTED = doc("A request to cancel all unmatched bets was submitted since last heartbeat")
    ALL_BETS_CANCELLED = doc("All unmatched bets were cancelled since last heartbeat")
    SOME_BETS_NOT_CANCELLED = doc("Not all unmatched bets were cancelled since last heartbeat")
    CANCELLATION_REQUEST_ERROR = doc("There was an error requesting cancellation, no bets have been cancelled")
    CANCELLATION_STATUS_UNKNOWN = doc("There was no response from requesting cancellation, cancellation status unknown")


class HeartbeatReport(BaseMessage, frozen=True):
    """Response from heartbeat operation."""

    action_performed: ActionPerformed  # The action performed since your last heartbeat request.
    actual_timeout_seconds: int  # The actual timeout applied to your heartbeat request


class _HeartbeatParams(Params, frozen=True):
    # Maximum period in seconds that may elapse (without a subsequent heartbeat request),
    # before a cancellation request is automatically submitted on your behalf. The minimum
    # value is 10, the maximum value permitted is 300.
    preferred_timeout_seconds: int


class Heartbeat(Request, kw_only=True, frozen=True, tag=heartbeat_tag):
    """
    This heartbeat operation is provided to help customers have their positions managed automatically in the
    event of their API clients losing connectivity with the Betfair API. If a heartbeat request is not received
    within a prescribed time period, then Betfair will attempt to cancel all 'LIMIT' type bets for the given
    customer on the given exchange. There is no guarantee that this service will result in all bets being
    cancelled as there are a number of circumstances where bets are unable to be cancelled. Manual intervention
    is strongly advised in the event of a loss of connectivity to ensure that positions are correctly managed.
    If this service becomes unavailable for any reason, then your heartbeat will be unregistered automatically
    to avoid bets being inadvertently cancelled upon resumption of service. you should manage your position
    manually until the service is resumed. Heartbeat data may also be lost in the unlikely event of nodes
    failing within the cluster, which may result in your position not being managed until a subsequent heartbeat
    request is received.
    """

    endpoint_type = EndpointType.HEARTBEAT
    params: _HeartbeatParams
    return_type = Response[HeartbeatReport]
