import datetime
from enum import Enum
from typing import List, Literal, Optional, Union

from betfair_parser.constants import EVENT_TYPE_TO_NAME
from betfair_parser.spec.api.markets import PriceLadderDescription
from betfair_parser.spec.common import BaseMessage


class RunnerStatus(Enum):
    ACTIVE = "ACTIVE"
    REMOVED = "REMOVED"
    WINNER = "WINNER"
    PLACED = "PLACED"
    LOSER = "LOSER"
    HIDDEN = "HIDDEN"


class MarketStatus(Enum):
    OPEN = "OPEN"
    SUSPENDED = "SUSPENDED"
    CLOSED = "CLOSED"


class RunnerValues(BaseMessage):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    tv: float  # Traded Volume
    ltp: float  # Last Traded Price
    spn: float  # Starting Price Near
    spf: float  # Starting Price Far


class Runner(BaseMessage):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    sortPriority: int
    id: Union[int, str]
    name: Optional[str] = None
    hc: Optional[Union[float, str]] = None
    status: Optional[RunnerStatus] = None
    adjustmentFactor: Optional[float] = None
    selectionId: Optional[str] = None
    bsp: Optional[Union[str, float]] = None
    removalDate: Optional[str] = None

    @property
    def handicap(self) -> str:
        return str(self.hc or 0.0)

    @property
    def runner_id(self) -> int:
        return int(self.selectionId or self.id)


class RunnerKeyLine(BaseMessage):
    id: int
    hc: int


class KeyLineDefinition(BaseMessage):
    kl: list[RunnerKeyLine]


class MarketDefinition(BaseMessage, kw_only=True):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    bspMarket: bool
    turnInPlayEnabled: bool
    persistenceEnabled: bool
    marketBaseRate: Optional[float]
    marketId: Optional[str] = ""
    marketName: Optional[str] = ""
    eventId: str
    eventTypeId: str
    numberOfWinners: int
    bettingType: str
    marketType: str
    marketTime: str
    competitionId: Optional[str] = ""
    competitionName: Optional[str] = ""
    eventName: Optional[str] = ""
    suspendTime: str
    bspReconciled: bool
    complete: bool
    inPlay: bool
    crossMatching: bool
    runnersVoidable: bool
    numberOfActiveRunners: int
    betDelay: int
    status: MarketStatus
    runners: List[Runner]
    regulators: List[str]
    name: Optional[str] = None
    openDate: Optional[str] = None
    timezone: Optional[str] = None
    venue: Optional[str] = None
    version: Optional[int] = None
    countryCode: Optional[str] = None
    discountAllowed: Optional[bool] = None
    raceType: Optional[Literal["Flat"]] = None
    priceLadderDefinition: Optional[Union[str, PriceLadderDescription]] = None
    settledTime: Optional[datetime.datetime] = None
    keyLineDefinition: Optional[KeyLineDefinition] = None

    @property
    def event_type_name(self) -> str:
        return EVENT_TYPE_TO_NAME[self.eventTypeId]

    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__}


class AvailableToBack(BaseMessage, array_like=True):
    """AvailableToBack"""

    price: float
    volume: float


class AvailableToLay(BaseMessage, array_like=True):
    """AvailableToLay"""

    price: float
    volume: float


class BestAvailableToBack(BaseMessage, array_like=True):
    """BestAvailableToBack"""

    level: int
    price: float
    volume: float


class BestAvailableToLay(BaseMessage, array_like=True):
    """BestAvailableToLay"""

    level: int
    price: float
    volume: float


class BestDisplayAvailableToBack(BaseMessage, array_like=True):
    """BestDisplayAvailableToBack"""

    level: int
    price: float
    volume: float


class BestDisplayAvailableToLay(BaseMessage, array_like=True):
    """BestDisplayAvailableToLay"""

    level: int
    price: float
    volume: float


class Trade(BaseMessage, array_like=True):
    """Trade"""

    price: float
    volume: float


class StartingPriceBack(BaseMessage, array_like=True):
    """StartingPriceBack"""

    price: float
    volume: float


class StartingPriceLay(BaseMessage, array_like=True):
    """StartingPriceLay"""

    price: float
    volume: float


class RunnerChange(BaseMessage):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    id: Union[int, str]
    atb: Optional[List[AvailableToBack]] = []
    atl: Optional[List[AvailableToLay]] = []
    batb: Optional[List[BestAvailableToBack]] = []
    batl: Optional[List[BestAvailableToLay]] = []
    bdatb: Optional[List[BestDisplayAvailableToBack]] = []
    bdatl: Optional[List[BestDisplayAvailableToLay]] = []
    spb: Optional[List[StartingPriceBack]] = []  # Starting Price (Available To) Back
    spl: Optional[List[StartingPriceLay]] = []  # Starting Price (Available To) Lay
    spn: Optional[Union[float, str]] = None  # Starting Price Near
    spf: Optional[Union[int, float, str]] = None  # Starting Price Far
    trd: Optional[List[Trade]] = []
    ltp: Optional[float] = None
    tv: Optional[float] = None
    hc: Optional[float] = None


class MarketChange(BaseMessage):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    id: str
    marketDefinition: Optional[MarketDefinition] = None
    rc: List[RunnerChange] = []
    img: bool = False
    tv: Optional[float] = None
    con: Optional[bool] = None


class MCM(BaseMessage, tag_field="op", tag=str.lower):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    pt: int
    clk: Optional[str] = None
    id: Optional[int] = None
    initialClk: Optional[str] = None
    marketDefinition: Optional[MarketDefinition] = None
    status: Optional[int] = None
    conflateMs: Optional[int] = None
    heartbeatMs: Optional[int] = None
    ct: Optional[Literal["HEARTBEAT", "SUB_IMAGE", "RESUB_DELTA"]] = None
    mc: List[MarketChange] = []
    con: Optional[bool] = None

    @property
    def is_heartbeat(self):
        return self.ct == "HEARTBEAT"

    @property
    def stream_unreliable(self):
        return self.status == 503
