from typing import Literal, Optional

from betfair_parser.spec.common import BaseMessage
from betfair_parser.strenums import DocumentedEnum, doc


class StatusErrorCode(DocumentedEnum):
    # General errors not sent with id linking to specific request (as no request context)
    INVALID_INPUT = doc(
        "Failure code returned when an invalid input is provided (could not " "deserialize the message)"
    )
    TIMEOUT = doc("Failure code when a client times out (i.e. too slow sending data)")

    # Specific to authentication
    NO_APP_KEY = doc("Failure code returned when an application key is not found in the message")
    INVALID_APP_KEY = doc("Failure code returned when an invalid application key is received")
    NO_SESSION = doc("Failure code returned when a session token is not found in the message")
    INVALID_SESSION_INFORMATION = doc("Failure code returned when an invalid session token is received")
    NOT_AUTHORIZED = doc("Failure code returned when client is not authorized to perform the operation")
    MAX_CONNECTION_LIMIT_EXCEEDED = doc(
        "Failure code returned when a client tries to create more connections than allowed to"
    )
    TOO_MANY_REQUESTS = doc("Failure code returned when a client makes too many requests within a short time period")

    # Specific to subscription requests
    SUBSCRIPTION_LIMIT_EXCEEDED = doc(
        "Customer tried to subscribe to more markets than allowed to - set to 200 markets by default"
    )
    INVALID_CLOCK = doc(
        "Failure code returned when an invalid clock is provided on re-subscription "
        "(check initialClk / clk supplied)"
    )

    # General errors which may or may not be linked to specific request id
    UNEXPECTED_ERROR = doc("Failure code returned when an internal error occurred on the server")
    CONNECTION_FAILED = doc("Failure code used when the client / server connection is terminated")


class Connection(BaseMessage, tag_field="op", tag=str.lower, frozen=True):
    """Connection Message"""

    connectionId: str


class Status(BaseMessage, tag_field="op", tag=str.lower, frozen=True):
    """Status Message"""

    statusCode: Literal["SUCCESS", "FAILURE"]
    connectionClosed: bool
    id: Optional[int] = None
    connectionsAvailable: Optional[int] = None
    connectionId: Optional[str] = None
    errorCode: Optional[StatusErrorCode] = None
    errorMessage: Optional[str] = None
