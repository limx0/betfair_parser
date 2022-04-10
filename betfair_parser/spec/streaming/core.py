from typing import Literal

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

    statusCode: Literal["SUCCESS", "FAILURE"]
    connectionClosed: bool
    errorCode: str
    errorMessage: str
    connectionsAvailable: int
