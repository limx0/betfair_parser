import datetime
import re
from typing import Literal

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
    numberOfWinners: int | str


class Event(BaseMessage, tag=tag_func):
    name: str
    id: str
    countryCode: str
    children: list[Market]


Event = msgspec.defstruct(  # type: ignore
    "Event",
    [("name", str), ("id", str), ("countryCode", str), ("children", list[Market | Event])],
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
    raceNumber: str | None = None


class Group(BaseMessage, tag=tag_func):
    name: str
    id: str
    children: list[Event | Race]


Group = msgspec.defstruct(  # type: ignore
    "Group",
    [("name", str), ("id", str), ("children", list[Event | Race | Group])],
    bases=(BaseMessage,),
    tag=tag_func,
)


class EventType(BaseMessage, tag=tag_func):
    name: str
    id: str
    children: list[Event | Group | Race]


class NavigationMarket(BaseMessage):
    """NavigationMarket"""

    type: Literal["GROUP"]
    name: Literal["ROOT"]
    id: int
    children: list[EventType]
