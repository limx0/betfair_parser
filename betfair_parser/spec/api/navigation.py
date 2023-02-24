import datetime
import re
from typing import Literal, Optional, Union

import msgspec

from betfair_parser.spec.common import BaseMessage


def tag_func(s: str):
    """
    >>> tag_func("EventType")
    'EVENT_TYPE'

    >>> tag_func("Group")
    'GROUP'
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).upper()


class Market(BaseMessage, tag=tag_func):
    name: str
    id: str
    exchangeId: str
    marketType: str
    marketStartTime: str
    numberOfWinners: Union[int, str]


class Event(BaseMessage, tag=tag_func):
    name: str
    id: str
    countryCode: str
    children: list[Market]


Event = msgspec.defstruct(  # type: ignore
    "Event",
    [("name", str), ("id", str), ("countryCode", str), ("children", list[Union[Market, Event]])],
    bases=(BaseMessage,),
    tag=tag_func,
)


class Race(BaseMessage, tag=tag_func):
    name: str
    id: str
    countryCode: str
    venue: str
    startTime: datetime.datetime
    children: list[Market]
    raceNumber: Optional[str] = None


class Group(BaseMessage, tag=tag_func):
    name: str
    id: str
    children: list[Union[Event, Race]]


Group = msgspec.defstruct(  # type: ignore
    "Group",
    [("name", str), ("id", str), ("children", list[Union[Event, Race, Group]])],
    bases=(BaseMessage,),
    tag=tag_func,
)


class EventType(BaseMessage, tag=tag_func):
    name: str
    id: str
    children: list[Union[Event, Group, Race]]


class NavigationMarket(BaseMessage):
    """NavigationMarket"""

    type: Literal["GROUP"]
    name: Literal["ROOT"]
    id: int
    children: list[EventType]


class FlattenedMarket(BaseMessage, kw_only=True):
    event_type_name: str
    event_type_id: str
    event_name: Optional[str] = None
    event_id: Optional[str] = None
    event_countryCode: Optional[str] = None
    market_name: str
    market_id: str
    market_exchangeId: str
    market_marketType: str
    market_marketStartTime: str
    market_numberOfWinners: Union[int, str]
    group_name: Optional[str] = None
    group_id: Optional[str] = None
    race_name: Optional[str] = None
    race_id: Optional[str] = None
    race_countryCode: Optional[str] = None
    race_venue: Optional[str] = None
    race_startTime: Optional[str] = None
    race_raceNumber: Optional[str] = None


def flatten_navigation(raw: bytes, **filters) -> list[FlattenedMarket]:
    data = msgspec.json.decode(raw)
    flattened = flatten_tree(data, **filters)
    return msgspec.json.decode(msgspec.json.encode(flattened), type=list[FlattenedMarket])


def flatten_tree(y: dict, **filters):
    """
    Flatten a nested dict into a list of dicts with each nested level combined
    into a single dict.
    """
    results = []
    ignore_keys = ("type", "children")

    def flatten(dict_like, depth: Optional[int] = None):
        def _filter(k, v):
            if isinstance(v, str):
                return k == v
            elif isinstance(v, (tuple, list)):
                return k in v
            else:
                raise TypeError

        depth = depth or 0
        node_type = dict_like["type"].lower()
        data = {f"{node_type}_{k}": v for k, v in dict_like.items() if k not in ignore_keys}
        if "children" in dict_like:
            for child in dict_like["children"]:
                for child_data in flatten(child, depth=depth + 1):
                    if depth == 0:
                        if all(_filter(child_data[k], v) for k, v in filters.items()):
                            results.append(child_data)
                    else:
                        yield {**data, **child_data}
        else:
            yield data

    list(flatten(y))
    return results
