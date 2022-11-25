import msgspec.json
import pytest

from betfair_parser.spec.api.markets import NavigationMarket
from tests.resources import read_test_file


@pytest.mark.parametrize(
    "raw",
    [
        read_test_file("responses/navigation_list_navigation.json"),
    ],
)
@pytest.mark.skip(reason="not implemented")
def test_navigation_market(raw):
    nav = msgspec.json.decode(raw, type=NavigationMarket)
    assert nav.event_type_name == ""


# @pytest.mark.parametrize(
#     "raw",
#     [
#         read_test_file("responses/betting_list_market_catalogue.json"),
#     ]
# )
# @pytest.mark.skip(reason="not implemented")
# def test_market_catalogue(raw):
#     catalog = msgspec.json.decode(raw, type=MarketCatalog)
#     assert catalog.event_type_name == ""
