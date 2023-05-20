import msgspec.json
import pytest

from betfair_parser.spec.accounts.operations import getAccountDetails, getAccountFunds
from tests.resources import id_from_path, read_test_file


def test_account_details_request():
    raw = read_test_file("requests/accounts/get_account_details.json")
    details = msgspec.json.decode(raw, type=getAccountDetails)
    assert details.validate()
    enc_details = msgspec.json.encode(details)
    assert getAccountDetails.method in enc_details.decode()


def test_account_funds_request():
    raw = read_test_file("requests/accounts/get_account_funds.json")
    funds = msgspec.json.decode(raw, type=getAccountFunds)
    assert funds.validate()
    enc_funds = msgspec.json.encode(funds)
    assert getAccountFunds.method in enc_funds.decode()


def test_account_details_response():
    raw = read_test_file("responses/accounts/get_account_details.json")
    details = msgspec.json.decode(raw, type=getAccountDetails.return_type)
    assert details.validate()


@pytest.mark.parametrize(
    "path",
    [
        "responses/accounts/get_account_funds_no_exposure.json",
        "responses/accounts/get_account_funds_with_exposure.json",
    ],
    ids=id_from_path,
)
def test_account_funds_response(path):
    raw = read_test_file(path)
    funds = msgspec.json.decode(raw, type=getAccountFunds.return_type)
    assert funds.validate()
