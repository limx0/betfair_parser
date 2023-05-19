from betfair_parser.spec.common import BaseMessage, Request, Response
from betfair_parser.strenums import DocumentedEnum, doc


class ActionPerformed(DocumentedEnum):
    NONE = doc("No action was performed since last heartbeat, or this is the first heartbeat")
    CANCELLATION_REQUEST_SUBMITTED = doc("A request to cancel all unmatched bets was submitted since last heartbeat")
    ALL_BETS_CANCELLED = doc("All unmatched bets were cancelled since last heartbeat")
    SOME_BETS_NOT_CANCELLED = doc("Not all unmatched bets were cancelled since last heartbeat")
    CANCELLATION_REQUEST_ERROR = doc("There was an error requesting cancellation, no bets have been cancelled")
    CANCELLATION_STATUS_UNKNOWN = doc("There was no response from requesting cancellation, cancellation status unknown")


class HeartbeatReport(BaseMessage, frozen=True):
    """Response from heartbeat operation."""

    actionPerformed: ActionPerformed  # The action performed since your last heartbeat request.
    actualTimeoutSeconds: int  # The actual timeout applied to your heartbeat request


class heartbeatParams(BaseMessage, frozen=True):
    # Maximum period in seconds that may elapse (without a subsequent heartbeat request),
    # before a cancellation request is automatically submitted on your behalf. The minimum
    # value is 10, the maximum value permitted is 300.
    preferredTimeoutSeconds: int


class heartbeat(Request, kw_only=True, frozen=True):
    """
    Returns a list of Competitions (i.e., World Cup 2013) associated with the markets selected by
    the MarketFilter. Currently only Football markets have an associated competition.
    """

    method = "HeartbeatAPING/v1.0/heartbeat"
    params: heartbeatParams
    return_type = Response[HeartbeatReport]
