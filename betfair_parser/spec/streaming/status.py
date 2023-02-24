from typing import Literal, Optional

from betfair_parser.spec.common import BaseMessage


class Connection(BaseMessage, tag_field="op", tag=str.lower):
    """
    Connection Message
    """

    connectionId: str


class Status(BaseMessage, tag_field="op", tag=str.lower):
    """
    Status Message
    """

    id: int
    statusCode: Literal["SUCCESS", "FAILURE"]
    connectionClosed: bool
    errorCode: Optional[str] = None
    errorMessage: Optional[str] = None
    connectionsAvailable: Optional[int] = None
