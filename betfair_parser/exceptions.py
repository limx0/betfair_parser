class BetfairError(Exception):
    """Base class for all Exceptions in this package. Allow to hand in custom data with keyword arguments."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.__dict__.update(kwargs)


class JSONError(BetfairError):
    """Issue with the data serialization."""


class APIError(BetfairError):
    """Most general API error."""


class APINGException(APIError):
    """Errors thrown from a betfair operation."""


class AccountAPINGException(APIError):
    """An issue thrown from the accounts API."""


class IdentityError(APIError):
    """An issue thrown from the identity API."""


class LoginImpossible(IdentityError):
    """This probably needs manual resolution."""


class StreamError(APIError):
    """Issues related with the streaming API."""


class StreamAuthenticationError(StreamError):
    """Authentication for the stream API is not possible."""
