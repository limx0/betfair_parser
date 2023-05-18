from typing import Literal

from betfair_parser.spec.accounts.type_definitions import AccountDetailsResponse, AccountFundsResponse
from betfair_parser.spec.common import RequestBase, Response


class getAccountFunds(RequestBase, frozen=True):
    method: Literal["AccountAPING/v1.0/getAccountFunds"] = "AccountAPING/v1.0/getAccountFunds"
    params: dict = {}
    return_type = Response[AccountFundsResponse]
    throws = None


class getAccountDetails(RequestBase, frozen=True):
    method: Literal["AccountAPING/v1.0/getAccountDetails"] = "AccountAPING/v1.0/getAccountDetails"
    params: dict = {}
    return_type = Response[AccountDetailsResponse]
    throws = None
