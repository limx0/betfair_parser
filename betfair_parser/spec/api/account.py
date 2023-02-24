from typing import Literal

from betfair_parser.spec.api.core import RequestBase


class getAccountFunds(RequestBase):
    method: Literal["AccountAPING/v1.0/getAccountFunds"] = "AccountAPING/v1.0/getAccountFunds"
    params: dict = {}


class getAccountDetails(RequestBase):
    method: Literal["AccountAPING/v1.0/getAccountDetails"] = "AccountAPING/v1.0/getAccountDetails"
    params: dict = {}


class AccountDetails(RequestBase):
    currencyCode: str
    firstName: str
    lastName: str
    localeCode: str
    region: str
    timezone: str
    discountRate: float
    pointsBalance: int
    countryCode: str


class AccountDetailsResponse(RequestBase):
    result: AccountDetails


class AccountFunds(RequestBase):
    availableToBetBalance: float
    exposure: float
    retainedCommission: float
    exposureLimit: float
    discountRate: float
    pointsBalance: int
    wallet: str


class AccountFundsResponse(RequestBase):
    result: AccountFunds
