from typing import Literal

from betfair_parser.spec.api.core import APIBase


class getAccountFunds(APIBase):
    method: Literal["AccountAPING/v1.0/getAccountFunds"] = "AccountAPING/v1.0/getAccountFunds"


class getAccountDetails(APIBase):
    method: Literal["AccountAPING/v1.0/getAccountDetails"] = "AccountAPING/v1.0/getAccountDetails"


class AccountDetails(APIBase):
    currencyCode: str
    firstName: str
    lastName: str
    localeCode: str
    region: str
    timezone: str
    discountRate: float
    pointsBalance: int
    countryCode: str


class AccountDetailsResponse(APIBase):
    result: AccountDetails


class AccountFunds(APIBase):
    availableToBetBalance: float
    exposure: float
    retainedCommission: float
    exposureLimit: float
    discountRate: float
    pointsBalance: int
    wallet: str


class AccountFundsResponse(APIBase):
    result: AccountFunds
