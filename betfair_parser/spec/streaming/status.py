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

    statusCode: Literal["SUCCESS", "FAILURE"]
    connectionClosed: bool
    id: Optional[int] = None
    connectionsAvailable: Optional[int] = None
    connectionId: Optional[str] = None
    errorCode: Optional[str] = None
    errorMessage: Optional[str] = None
