from collections import namedtuple
from typing import List, Literal, Optional, Union

import msgspec

from betfair_parser.constants import EVENT_TYPE_TO_NAME


class RunnerValues(msgspec.Struct):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    tv: float  # Traded Volume
    ltp: float  # Last Traded Price
    spn: float  # Starting Price Near
    spf: float  # Starting Price Far


class Runner(msgspec.Struct):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    sortPriority: int
    id: Union[int, str]
    name: Optional[str] = None
    hc: Optional[Union[float, str]] = None
    status: Optional[str] = None
    adjustmentFactor: Optional[float] = None
    selectionId: Optional[str] = None

    @property
    def handicap(self) -> str:
        return str(self.hc or 0.0)

    @property
    def runner_id(self) -> int:
        return int(self.selectionId or self.id)


class MarketDefinition(msgspec.Struct, kw_only=True):  # type: ignore
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    bspMarket: bool
    turnInPlayEnabled: bool
    persistenceEnabled: bool
    marketBaseRate: Optional[float]
    marketId: Optional[str] = ""
    marketName: Optional[str] = ""
    marketStartTime: Optional[str] = ""
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
    status: str
    runners: List[Runner]
    regulators: List[str]
    name: Optional[str] = None
    openDate: Optional[str] = None
    timezone: Optional[str] = None
    venue: Optional[str] = None
    version: Optional[int] = None
    countryCode: Optional[str] = None
    discountAllowed: Optional[bool] = None

    @property
    def event_type_name(self) -> str:
        return EVENT_TYPE_TO_NAME[self.eventTypeId]

    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__}


class AvailableToBack(namedtuple("AvailableToBack", "price,volume")):
    """AvailableToBack"""

    pass


class AvailableToLay(namedtuple("AvailableToLay", "price,volume")):
    """AvailableToLay"""

    pass


class BestAvailableToBack(namedtuple("BestAvailableToBack", "level,price,volume")):
    """BestAvailableToBack"""

    pass


class BestAvailableToLay(namedtuple("BestAvailableToLay", "level,price,volume")):
    """BestAvailableToLay"""

    pass


class BestDisplayAvailableToBack(namedtuple("BestDisplayAvailableToBack", "level,price,volume")):
    """BestDisplayAvailableToBack"""

    pass


class BestDisplayAvailableToLay(namedtuple("BestDisplayAvailableToLay", "level,price,volume")):
    """BestDisplayAvailableToLay"""

    pass


class Trade(namedtuple("Trade", "price,volume")):
    """Trade"""

    pass


class StartingPriceBack(namedtuple("StartingPriceBack", "price,volume")):
    """StartingPriceBack"""

    pass


class StartingPriceLay(namedtuple("StartingPriceLay", "price,volume")):
    """StartingPriceLay"""

    pass


class RunnerChange(msgspec.Struct):
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
    spb: Optional[List[StartingPriceBack]] = []
    spl: Optional[List[StartingPriceLay]] = []
    trd: Optional[List[Trade]] = []
    ltp: Optional[float] = None
    tv: Optional[float] = None
    hc: Optional[float] = None


class MarketChange(msgspec.Struct):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    id: str
    marketDefinition: Optional[MarketDefinition] = None
    rc: List[RunnerChange] = []
    img: bool = False
    tv: Optional[float] = None
    con: Optional[bool] = None


class MCM(msgspec.Struct, tag_field="op", tag=str.lower):  # type: ignore
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    pt: int
    clk: Optional[str] = None
    id: Optional[int] = None
    initialClk: Optional[str] = None
    status: Optional[int] = None
    conflateMs: Optional[int] = None
    heartbeatMs: Optional[int] = None
    ct: Optional[Literal["HEARTBEAT", "SUB_IMAGE", "RESUB_DELTA"]] = None
    mc: List[MarketChange] = []

    @property
    def is_heartbeat(self):
        return self.ct == "HEARTBEAT"

    @property
    def stream_unreliable(self):
        return self.status == 503
