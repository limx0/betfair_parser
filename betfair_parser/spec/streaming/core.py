from typing import Literal, Optional

import msgspec


class StreamMessage(msgspec.Struct, tag_field="op", tag=lambda name: name.lower()):  # type: ignore
    pass


class Connection(StreamMessage):
    """
    Connection Message
    """

    connectionId: str


class Status(StreamMessage):
    """
    Status Message
    """

    id: int
    statusCode: Literal["SUCCESS", "FAILURE"]
    connectionClosed: bool
    errorCode: Optional[str] = None
    errorMessage: Optional[str] = None
    connectionsAvailable: Optional[int] = None
