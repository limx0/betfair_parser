import msgspec.json
import pytest

from betfair_parser.spec.accounts.operations import GetAccountDetails, GetAccountFunds, Params
from tests.resources import RESOURCES_DIR, id_from_path


@pytest.mark.parametrize(
    "details",
    [
        GetAccountDetails(),
        GetAccountDetails.with_params(),
        msgspec.json.decode(
            (RESOURCES_DIR / "requests" / "accounts" / "get_account_details.json").read_bytes(), type=GetAccountDetails
        ),
    ],
)
def test_account_details_request(details):
    assert isinstance(details, GetAccountDetails)
    assert isinstance(details.params, Params) or not details.params
    assert details.method.endswith("getAccountDetails")
    assert details.validate()
    enc_details = msgspec.json.encode(details)
    assert "getAccountDetails" in enc_details.decode()


def test_account_details_response():
    raw = (RESOURCES_DIR / "responses" / "accounts" / "get_account_details.json").read_bytes()
    details = msgspec.json.decode(raw, type=GetAccountDetails.return_type)
    assert details.validate()


@pytest.mark.parametrize(
    "funds",
    [
        GetAccountFunds(),
        GetAccountFunds.with_params(),
        msgspec.json.decode(
            (RESOURCES_DIR / "requests" / "accounts" / "get_account_funds.json").read_bytes(), type=GetAccountFunds
        ),
    ],
)
def test_account_funds_request(funds):
    assert isinstance(funds, GetAccountFunds)
    assert isinstance(funds.params, Params) or not funds.params
    assert funds.method.endswith("getAccountFunds")
    assert funds.validate()
    enc_funds = msgspec.json.encode(funds)
    assert "getAccountFunds" in enc_funds.decode()


def test_account_funds_with_params():
    """Make sure that `with_params` still works for optional params."""
    funds = GetAccountFunds.with_params(wallet="UK")
    assert funds.id
    assert funds.params.wallet == "UK"
    assert funds.validate()


@pytest.mark.parametrize(
    "filename",
    [
        "get_account_funds_no_exposure.json",
        "get_account_funds_with_exposure.json",
    ],
    ids=id_from_path,
)
def test_account_funds_response(filename):
    raw = (RESOURCES_DIR / "responses" / "accounts" / filename).read_bytes()
    funds = msgspec.json.decode(raw, type=GetAccountFunds.return_type)
    assert funds.validate()
