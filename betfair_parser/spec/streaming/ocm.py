from typing import List, Literal, Optional

from betfair_parser.spec.common import BaseMessage


class MatchedOrder(BaseMessage, array_like=True, frozen=True):
    price: float
    size: float


class UnmatchedOrder(BaseMessage, frozen=True):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    id: str
    p: float
    s: float
    side: Literal["B", "L"]
    status: Literal["E", "EC"]
    pt: str
    ot: str
    pd: int
    rfo: Optional[str] = None
    rfs: Optional[str] = None
    rc: Optional[str] = None
    rac: Optional[str] = None
    md: Optional[int] = None
    cd: Optional[int] = None
    ld: Optional[int] = None
    avp: Optional[float] = None
    sm: Optional[float] = None
    sr: Optional[float] = None
    sl: Optional[float] = None
    sc: Optional[float] = None
    sv: Optional[float] = None


class StrategyMatched(BaseMessage, frozen=True):
    mb: Optional[List[MatchedOrder]] = []
    ml: Optional[List[MatchedOrder]] = []


class OrderChanges(BaseMessage, frozen=True):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    id: int
    fullImage: Optional[bool] = False
    hc: Optional[float] = None
    uo: Optional[List[UnmatchedOrder]] = []
    mb: Optional[List[MatchedOrder]] = []
    ml: Optional[List[MatchedOrder]] = []
    smc: Optional[dict[str, StrategyMatched]] = None


class OrderAccountChange(BaseMessage, frozen=True):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    id: str
    accountId: Optional[int] = None
    fullImage: Optional[bool] = False
    orc: List[OrderChanges] = []
    closed: Optional[bool] = None


class OCM(BaseMessage, tag_field="op", tag=str.lower, frozen=True):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    id: int
    clk: str
    pt: int
    oc: List[OrderAccountChange] = []
    initialClk: Optional[str] = None
    status: Optional[int] = None
    conflateMs: Optional[int] = None
    heartbeatMs: Optional[int] = None
    ct: Optional[Literal["HEARTBEAT", "SUB_IMAGE"]] = None
    con: Optional[bool] = None
