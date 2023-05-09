from typing import Literal

from betfair_parser.spec.api.core import RequestBase


class getAccountFunds(RequestBase, frozen=True):
    method: Literal["AccountAPING/v1.0/getAccountFunds"] = "AccountAPING/v1.0/getAccountFunds"
    params: dict = {}


class getAccountDetails(RequestBase, frozen=True):
    method: Literal["AccountAPING/v1.0/getAccountDetails"] = "AccountAPING/v1.0/getAccountDetails"
    params: dict = {}


class AccountDetails(RequestBase, frozen=True):
    currencyCode: str
    firstName: str
    lastName: str
    localeCode: str
    region: str
    timezone: str
    discountRate: float
    pointsBalance: int
    countryCode: str


class AccountDetailsResponse(RequestBase, frozen=True):
    result: AccountDetails


class AccountFunds(RequestBase, frozen=True):
    availableToBetBalance: float
    exposure: float
    retainedCommission: float
    exposureLimit: float
    discountRate: float
    pointsBalance: int
    wallet: str


class AccountFundsResponse(RequestBase, frozen=True):
    result: AccountFunds
