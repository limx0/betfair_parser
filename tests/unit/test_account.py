import msgspec.json
import pytest

from betfair_parser.spec.accounts.operations import (
    GetAccountDetails,
    GetAccountFunds,
    _GetAccountDetailsParams,
    _GetAccountFundsParams,
)
from tests.resources import RESOURCES_DIR, id_from_path


@pytest.mark.parametrize(
    "msg_type",
    [GetAccountDetails, GetAccountFunds],
)
def test_init_requires_params(msg_type):
    """
    Even if some methods don't require params, if the request requires the class variable
    `method` set into the message body, it must be initialized with the factory method
    `with_params`. This is unfortunate, but only affects these two methods.
    """
    with pytest.raises(TypeError):
        msg_type()


@pytest.mark.parametrize(
    "details",
    [
        GetAccountDetails.with_params(),
        msgspec.json.decode(
            (RESOURCES_DIR / "requests" / "accounts" / "get_account_details.json").read_bytes(), type=GetAccountDetails
        ),
    ],
)
def test_account_details_request(details):
    assert isinstance(details, GetAccountDetails)
    assert isinstance(details.params, _GetAccountDetailsParams)
    assert details.method == GetAccountDetails.method
    assert details.validate()
    enc_details = msgspec.json.encode(details)
    assert GetAccountDetails.method in enc_details.decode()


def test_account_details_response():
    raw = (RESOURCES_DIR / "responses" / "accounts" / "get_account_details.json").read_bytes()
    details = msgspec.json.decode(raw, type=GetAccountDetails.return_type)
    assert details.validate()


@pytest.mark.parametrize(
    "funds",
    [
        GetAccountFunds.with_params(),
        msgspec.json.decode(
            (RESOURCES_DIR / "requests" / "accounts" / "get_account_funds.json").read_bytes(), type=GetAccountFunds
        ),
    ],
)
def test_account_funds_request(funds):
    assert isinstance(funds, GetAccountFunds)
    assert isinstance(funds.params, _GetAccountFundsParams)
    assert funds.method == GetAccountFunds.method
    assert funds.validate()
    enc_funds = msgspec.json.encode(funds)
    assert GetAccountFunds.method in enc_funds.decode()


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
