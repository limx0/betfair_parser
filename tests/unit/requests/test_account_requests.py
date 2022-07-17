import msgspec.json

from betfair_parser.spec.api.account import getAccountDetails, getAccountFunds
from tests.resources import read_test_file


def read_account_file(path: str):
    raw = read_test_file(path)
    return msgspec.json.encode(msgspec.json.decode(raw)["json"])


def test_account_details():
    raw = read_account_file("requests/account_details.json")
    details = msgspec.json.decode(raw, type=getAccountDetails)
    assert details.validate()


def test_account_funds():
    raw = read_account_file("requests/account_funds.json")
    funds = msgspec.json.decode(raw, type=getAccountFunds)
    assert funds.validate()
