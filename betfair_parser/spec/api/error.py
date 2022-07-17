from betfair_parser.spec.api.core import APIBase


class Error:
    code: int
    message: str


class ErrorResponse(APIBase):
    error: Error
