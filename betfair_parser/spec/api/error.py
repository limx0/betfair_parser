from betfair_parser.spec.common import BaseMessage


class Error:
    code: int
    message: str


class ErrorResponse(BaseMessage):
    error: Error
