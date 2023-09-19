import msgspec.json
import pytest

from betfair_parser.spec.accounts.operations import GetAccountDetails, GetAccountFunds, _GetAccountDetailsParams
from tests.resources import RESOURCES_DIR, id_from_path


def test_account_details_request():
    raw = RESOURCES_DIR.joinpath("requests/accounts/get_account_details.json").read_bytes()
    details = msgspec.json.decode(raw, type=GetAccountDetails)
    assert details.validate()
    enc_details = msgspec.json.encode(details)
    assert GetAccountDetails.method in enc_details.decode()


def test_account_funds_request():
    raw = RESOURCES_DIR.joinpath("requests/accounts/get_account_funds.json").read_bytes()
    funds = msgspec.json.decode(raw, type=GetAccountFunds)
    assert funds.validate()
    enc_funds = msgspec.json.encode(funds)
    assert GetAccountFunds.method in enc_funds.decode()


def test_account_details_response():
    raw = RESOURCES_DIR.joinpath("responses/accounts/get_account_details.json").read_bytes()
    details = msgspec.json.decode(raw, type=GetAccountDetails.return_type)
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
    raw = RESOURCES_DIR.joinpath(path).read_bytes()
    funds = msgspec.json.decode(raw, type=GetAccountFunds.return_type)
    assert funds.validate()


def test_account_with_params():
    request = GetAccountDetails.with_params()
    assert isinstance(request, GetAccountDetails)
    assert isinstance(request.params, _GetAccountDetailsParams)
