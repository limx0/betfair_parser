from typing import Dict, Literal

from betfair_parser.spec.api.core import Base


class getAccountFunds(Base):
    method: Literal["AccountAPING/v1.0/getAccountFunds"] = "AccountAPING/v1.0/getAccountFunds"
    params: Dict = {}


class getAccountDetails(Base):
    method: Literal["AccountAPING/v1.0/getAccountDetails"] = "AccountAPING/v1.0/getAccountDetails"
    params: Dict = {}
