import re
from typing import Literal, Optional, Union

from betfair_parser.spec.common import BaseMessage, BaseResponse, Date, EndpointType, Request


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
    id: str
    exchange_id: str
    market_type: str
    market_start_time: Date
    number_of_winners: Union[int, str]


class Event(BaseMessage, tag=navigation_tag, frozen=True):
    name: str
    id: int
    country_code: str
    children: list[Union["Group", "Event", Market]]


class Race(BaseMessage, tag=navigation_tag, frozen=True):
    name: str
    id: str
    country_code: str
    venue: str
    start_time: Date
    children: list[Market]
    race_number: Optional[str] = None


class Group(BaseMessage, tag=navigation_tag, frozen=True):
    name: str
    id: str
    children: list[Union["Group", Event]]


class EventType(BaseMessage, tag=navigation_tag, frozen=True):
    name: str
    id: int
    children: list[Union[Group, Event, Race]]


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
    event_type_id: int
    event_name: Optional[str] = None
    event_id: Optional[str] = None
    event_country_code: Optional[str] = None
    market_name: str
    market_id: str
    market_exchange_id: str
    market_market_type: str
    market_market_start_time: Date
    market_number_of_winners: Union[int, str]
    group_name: Optional[str] = None
    group_id: Optional[str] = None
    race_name: Optional[str] = None
    race_id: Optional[str] = None
    race_country_code: Optional[str] = None
    race_venue: Optional[str] = None
    race_start_time: Optional[Date] = None
    race_race_number: Optional[str] = None


def flatten_nav_tree(navigation: Navigation, **filters) -> list[FlattenedMarket]:
    return list(filter_flattened(flattened_nav_iter(navigation), **filters))


def _filter(k, v):
    if isinstance(v, str):
        return k == v
    if isinstance(v, (tuple, list)):
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
