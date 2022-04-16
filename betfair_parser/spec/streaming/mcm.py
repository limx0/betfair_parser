from typing import List, Literal, Optional, Union

import msgspec

from betfair_parser.spec.streaming.core import StreamMessage


class MarketSubscription(msgspec.Struct):
    op: Literal["marketSubscription"]
    id: int


class PriceSize(msgspec.Struct, array_like=True):  # type: ignore
    price: float
    size: float


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

    status: str
    sortPriority: int
    id: Union[int, str]
    hc: Optional[str] = None
    adjustmentFactor: Optional[float] = None


class MarketDefinition(msgspec.Struct):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    bspMarket: bool
    turnInPlayEnabled: bool
    persistenceEnabled: bool
    marketBaseRate: float
    eventId: str
    eventTypeId: str
    numberOfWinners: int
    bettingType: str
    marketType: str
    marketTime: str
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
    venue: Optional[str] = None
    countryCode: Optional[str] = None
    discountAllowed: bool
    timezone: str
    openDate: str
    version: int


class RunnerChange(msgspec.Struct):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    atb: Optional[List[PriceSize]] = []  # Best Available To Back
    atl: Optional[List[PriceSize]] = []  # Best Available To Lay
    batb: Optional[List[PriceSize]] = []  # Best Available To Back
    batl: Optional[List[PriceSize]] = []  # Best Available To Lay
    bdatb: Optional[List[PriceSize]] = []  # Best Display Available To Back  (virtual)
    bdatl: Optional[List[PriceSize]] = []  # Best Display Available To Lay (virtual)
    trd: Optional[List[PriceSize]] = []
    ltp: Optional[float] = None
    tv: Optional[float] = None
    id: Union[int, str]
    hc: Optional[float] = None


class MarketChange(msgspec.Struct):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    id: str
    marketDefinition: Optional[MarketDefinition] = None
    rc: Optional[List[RunnerChange]] = []
    img: bool = False
    tv: Optional[float] = None
    con: Optional[bool] = None


class MCM(StreamMessage):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    id: Optional[int] = None
    initialClk: Optional[str] = None
    status: Optional[int] = None
    clk: str
    conflateMs: Optional[int] = None
    heartbeatMs: Optional[int] = None
    pt: int
    ct: Optional[Literal["HEARTBEAT", "SUB_IMAGE", "RESUB_DELTA"]] = None
    mc: List[MarketChange] = []

    @property
    def is_heartbeat(self):
        return self.ct == "HEARTBEAT"

    @property
    def stream_unreliable(self):
        return self.status == 503
