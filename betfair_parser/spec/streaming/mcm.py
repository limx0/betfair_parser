from typing import Annotated, List, Literal, Optional, Union

import msgspec

from betfair_parser.spec.betting.enums import MarketStatus, RunnerStatus
from betfair_parser.spec.betting.type_definitions import PriceLadderDescription
from betfair_parser.spec.common import BaseMessage, Date, EventTypeIdCode, RegulatorCode


class RunnerValues(BaseMessage, frozen=True):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    tv: float  # Traded Volume
    ltp: float  # Last Traded Price
    spn: float  # Starting Price Near
    spf: float  # Starting Price Far


class Runner(BaseMessage, frozen=True):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    sort_priority: int
    id: Union[int, str]
    name: Optional[str] = None
    hc: Optional[Union[float, str]] = None
    status: Optional[RunnerStatus] = None
    adjustment_factor: Optional[float] = None
    selection_id: Optional[str] = None
    bsp: Optional[Union[str, float]] = None
    removal_date: Optional[str] = None

    @property
    def handicap(self) -> str:
        return str(self.hc or 0.0)

    @property
    def runner_id(self) -> int:
        return int(self.selection_id or self.id)


class RunnerKeyLine(BaseMessage, frozen=True):
    id: int
    hc: int


class KeyLineDefinition(BaseMessage, frozen=True):
    kl: list[RunnerKeyLine]


class MarketDefinition(BaseMessage, kw_only=True, frozen=True):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    bsp_market: bool
    turn_in_play_enabled: bool
    persistence_enabled: bool
    market_base_rate: Optional[float]
    market_id: Optional[str] = ""
    market_name: Optional[str] = ""
    event_id: str
    event_type_id: str
    number_of_winners: int
    betting_type: str
    market_type: str
    market_time: str
    competition_id: Optional[str] = ""
    competition_name: Optional[str] = ""
    event_name: Optional[str] = ""
    suspend_time: str
    bsp_reconciled: bool
    complete: bool
    in_play: bool
    cross_matching: bool
    runners_voidable: bool
    number_of_active_runners: int
    bet_delay: int
    status: MarketStatus
    runners: List[Runner]
    regulators: List[RegulatorCode]
    name: Optional[str] = None
    open_date: Optional[str] = None
    timezone: Optional[str] = None
    venue: Optional[str] = None
    version: Optional[int] = None
    country_code: Optional[str] = None
    discount_allowed: Optional[bool] = None
    race_type: Optional[str] = None
    price_ladder_definition: Optional[Union[str, PriceLadderDescription]] = None
    settled_time: Optional[Date] = None
    key_line_definition: Optional[KeyLineDefinition] = None
    each_way_divisor: Optional[float] = None

    @property
    def event_type_name(self) -> str:
        return EventTypeIdCode(int(self.event_type_id)).name


class _PriceVolume(BaseMessage, array_like=True, frozen=True):
    price: float
    volume: float


class _LevelPriceVolume(BaseMessage, array_like=True, frozen=True):
    level: int
    price: float
    volume: float


AvailableToBack = Annotated[_PriceVolume, msgspec.Meta(title="AvailableToBack")]
AvailableToLay = Annotated[_PriceVolume, msgspec.Meta(title="AvailableToLay")]
BestAvailableToBack = Annotated[_LevelPriceVolume, msgspec.Meta(title="BestAvailableToBack")]
BestAvailableToLay = Annotated[_LevelPriceVolume, msgspec.Meta(title="BestAvailableToLay")]
BestDisplayAvailableToBack = Annotated[_LevelPriceVolume, msgspec.Meta(title="BestDisplayAvailableToBack")]
BestDisplayAvailableToLay = Annotated[_LevelPriceVolume, msgspec.Meta(title="BestDisplayAvailableToLay")]
Trade = Annotated[_PriceVolume, msgspec.Meta(title="Trade")]
StartingPriceBack = Annotated[_PriceVolume, msgspec.Meta(title="StartingPriceBack")]
StartingPriceLay = Annotated[_PriceVolume, msgspec.Meta(title="StartingPriceLay")]


class RunnerChange(BaseMessage, frozen=True):
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


class MarketChange(BaseMessage, frozen=True):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    id: str
    market_definition: Optional[MarketDefinition] = None
    rc: List[RunnerChange] = []
    img: bool = False
    tv: Optional[float] = None
    con: Optional[bool] = None


class MCM(BaseMessage, tag_field="op", tag=str.lower, frozen=True):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    pt: int
    clk: Optional[str] = None
    id: Optional[int] = None
    initial_clk: Optional[str] = None
    market_definition: Optional[MarketDefinition] = None
    status: Optional[int] = None
    conflate_ms: Optional[int] = None
    heartbeat_ms: Optional[int] = None
    ct: Optional[Literal["HEARTBEAT", "SUB_IMAGE", "RESUB_DELTA"]] = None
    mc: List[MarketChange] = []
    con: Optional[bool] = None

    @property
    def is_heartbeat(self):
        return self.ct == "HEARTBEAT"

    @property
    def stream_unreliable(self):
        return self.status == 503
