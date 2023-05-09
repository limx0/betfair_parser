import msgspec.json
import pytest

from betfair_parser.spec.api.account import (
    AccountDetailsResponse,
    AccountFundsResponse,
    getAccountDetails,
    getAccountFunds,
)
from tests.resources import read_test_file, id_from_path


def read_account_request(path: str):
    raw = read_test_file(path)
    return msgspec.json.encode(msgspec.json.decode(raw)["json"])


def test_account_details_request():
    raw = read_account_request("requests/account_details.json")
    details = msgspec.json.decode(raw, type=getAccountDetails)
    assert details.validate()


def test_account_funds_request():
    raw = read_account_request("requests/account_funds.json")
    funds = msgspec.json.decode(raw, type=getAccountFunds)
    assert funds.validate()


def test_account_details_response():
    raw = read_test_file("responses/account_details.json")
    details = msgspec.json.decode(raw, type=AccountDetailsResponse)
    assert details.validate()


@pytest.mark.parametrize(
    "path",
    [
        "responses/account_funds_no_exposure.json",
        "responses/account_funds_with_exposure.json",
    ],
    ids=id_from_path,
)
def test_account_funds_response(path):
    raw = read_test_file(path)
    funds = msgspec.json.decode(raw, type=AccountFundsResponse)
    assert funds.validate()
