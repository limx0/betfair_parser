import re
from typing import Literal, Union

from betfair_parser.spec.common import (
    BaseMessage,
    BaseResponse,
    Date,
    EndpointType,
    EventId,
    EventTypeId,
    MarketId,
    Request,
)


def navigation_tag(class_name: str):
    """
    >>> navigation_tag("EventType")
    'EVENT_TYPE'

    >>> navigation_tag("Group")
    'GROUP'
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).upper()


class Market(BaseMessage, tag=navigation_tag, frozen=True):
    name: str
    id: MarketId
    exchange_id: str
    market_type: str
    market_start_time: Date
    number_of_winners: int | str


class Event(BaseMessage, tag=navigation_tag, frozen=True):
    name: str
    id: EventId
    country_code: str
    children: list[Union["Group", "Event", Market]]


class Race(BaseMessage, tag=navigation_tag, frozen=True):
    name: str
    id: str
    country_code: str
    venue: str
    start_time: Date
    children: list[Market]
    race_number: str | None = None


class Group(BaseMessage, tag=navigation_tag, frozen=True):
    name: str
    id: str
    children: list[Union["Group", Event]]


class EventType(BaseMessage, tag=navigation_tag, frozen=True):
    name: str
    id: EventTypeId
    children: list[Group | Event | Race]


class Navigation(BaseResponse, frozen=True):
    """Navigation root"""

    type: Literal["GROUP"]
    name: Literal["ROOT"]
    id: int
    children: list[EventType]

    @property
    def result(self):
        # Play along with ordinary RPC Response objects
        return self


class Menu(Request, kw_only=True, frozen=True, tag=""):
    """
    Navigation request
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Navigation+Data+For+Applications
    """

    endpoint_type = EndpointType.NAVIGATION
    params: None = None
    id: int = 0
    return_type = Navigation

    @classmethod
    def with_params(cls, request_id=None, **kwargs):
        # Force id to 0 to avoid issues with message validation
        return cls(id=0, **kwargs)

    def body(self):
        return b""


class FlattenedMarket(BaseMessage, kw_only=True, frozen=True, rename=None):
    event_type_name: str
    event_type_id: EventTypeId
    event_name: str | None = None
    event_id: EventId | None = None
    event_country_code: str | None = None
    market_name: str
    market_id: MarketId
    market_exchange_id: str
    market_market_type: str
    market_market_start_time: Date
    market_number_of_winners: int | str
    group_name: str | None = None
    group_id: str | None = None
    race_name: str | None = None
    race_id: str | None = None
    race_country_code: str | None = None
    race_venue: str | None = None
    race_start_time: Date | None = None
    race_race_number: str | None = None


def flatten_nav_tree(navigation: Navigation, **filters) -> list[FlattenedMarket]:
    return list(filter_flattened(flattened_nav_iter(navigation), **filters))


def _filter(k, v):
    if isinstance(v, str):
        return k == v
    if isinstance(v, tuple | list):
        return k in v
    raise TypeError


def filter_flattened(nav_iter, **filters):
    for flattened in nav_iter:
        if all(_filter(getattr(flattened, k), v) for k, v in filters.items()):
            yield flattened


def flattened_nav_iter(node, **context):
    node_type_name = navigation_tag(node.__class__.__name__).lower()
    context[node_type_name] = node
    if isinstance(node, Market):
        flattened = _flattened_from_context(context)
        yield flattened
    else:
        for child in node.children:
            yield from flattened_nav_iter(child, **context)


def _flattened_from_context(ctx):
    ctx.pop("navigation")
    return FlattenedMarket(
        **{
            f"{node_type}_{k}": v
            for node_type, nav_item in ctx.items()
            for k, v in nav_item.to_dict().items()
            if k not in ("type", "children")
        }
    )
