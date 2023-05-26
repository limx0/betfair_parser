import re
from typing import ClassVar, Literal, Optional, Union

import msgspec

from betfair_parser.spec.common import BaseMessage, Date, Request, decode, encode
from betfair_parser.spec.constants import Locale


def tag_func(s: str):
    """
    >>> tag_func("EventType")
    'EVENT_TYPE'

    >>> tag_func("Group")
    'GROUP'
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).upper()


class _NavigationParams(BaseMessage, kw_only=True, frozen=True):
    locale: Locale


class NavigationRequest(Request, kw_only=True, frozen=True):
    """
    Navigation requests - https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Navigation+Data+For+Applications
    """

    METHOD_TEMPLATE: ClassVar[str] = "/betting/rest/v1/{locale}/navigation/menu.json"
    params: _NavigationParams
    method: str = METHOD_TEMPLATE.format(locale=Locale.English.value)

    @classmethod
    def with_locale(cls, params: _NavigationParams, locale: Locale):
        method = cls.METHOD_TEMPLATE.format(locale=locale.value)
        return msgspec.structs.replace(cls(params=params), method=method)


class Market(BaseMessage, tag=tag_func, frozen=True):
    name: str
    id: str
    exchange_id: str
    market_type: str
    market_start_time: str
    number_of_winners: Union[int, str]


class Event(BaseMessage, tag=tag_func, frozen=True):
    name: str
    id: str
    country_code: str
    children: list[Union["Group", "Event", Market]]


class Race(BaseMessage, tag=tag_func, frozen=True):
    name: str
    id: str
    country_code: str
    venue: str
    start_time: Date
    children: list[Market]
    race_number: Optional[str] = None


class Group(BaseMessage, tag=tag_func, frozen=True):
    name: str
    id: str
    children: list[Union["Group", Event]]


class EventType(BaseMessage, tag=tag_func, frozen=True):
    name: str
    id: str
    children: list[Union[Group, Event, Race]]


class Navigation(BaseMessage, frozen=True):
    """Navigation"""

    type: Literal["GROUP"]
    name: Literal["ROOT"]
    id: int
    children: list[EventType]


class FlattenedMarket(BaseMessage, kw_only=True, frozen=True, rename=None):
    event_type_name: str
    event_type_id: str
    event_name: Optional[str] = None
    event_id: Optional[str] = None
    event_country_code: Optional[str] = None
    market_name: str
    market_id: str
    market_exchange_id: str
    market_market_type: str
    market_market_start_time: str
    market_number_of_winners: Union[int, str]
    group_name: Optional[str] = None
    group_id: Optional[str] = None
    race_name: Optional[str] = None
    race_id: Optional[str] = None
    race_country_code: Optional[str] = None
    race_venue: Optional[str] = None
    race_start_time: Optional[str] = None
    race_race_number: Optional[str] = None


def navigation_to_flatten_markets(navigation: Navigation, **filters) -> list[FlattenedMarket]:
    flattened = flatten_tree(decode(encode(navigation), type=Navigation), **filters)
    return decode(encode(flattened), type=list[FlattenedMarket])


def flatten_tree(navigation: dict, **filters):
    """
    Flatten a nested dict into a list of dicts with each nested level combined
    into a single dict.
    """
    results = []
    ignore_keys = ("type", "children")

    def _filter(k, v):
        if isinstance(v, str):
            return k == v
        if isinstance(v, (tuple, list)):
            return k in v
        raise TypeError

    def flatten(nav_item, depth: Optional[int] = None):
        depth = depth or 0
        node_type = tag_func(nav_item.__class__.__name__).lower()
        data = {f"{node_type}_{k}": v for k, v in nav_item.to_dict().items() if k not in ignore_keys}
        if hasattr(nav_item, "children"):
            for child in nav_item.children:
                for child_data in flatten(child, depth=depth + 1):
                    if depth == 0:
                        if all(_filter(child_data[k], v) for k, v in filters.items()):
                            results.append(child_data)
                    else:
                        yield {**data, **child_data}
        else:
            yield data

    list(flatten(navigation))
    return results
