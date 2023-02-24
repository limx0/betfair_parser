from typing import Literal, Optional

from betfair_parser.spec.common import BaseMessage


class PriceLadderDescription(BaseMessage):
    """PriceLadderDescription"""

    type: Literal["CLASSIC", "LINE_RANGE", "FINEST"]


class LineRangeInfo(BaseMessage):
    """LineRangeInfo"""

    maxUnitValue: float
    minUnitValue: float
    interval: float
    marketUnit: str


class Description(BaseMessage):
    """Description"""

    persistenceEnabled: bool
    bspMarket: bool
    marketTime: str
    suspendTime: str
    bettingType: str
    turnInPlayEnabled: bool
    marketType: str
    regulator: str
    marketBaseRate: float
    discountAllowed: bool
    wallet: str
    rules: str
    rulesHasDate: bool
    priceLadderDescription: PriceLadderDescription
    lineRangeInfo: Optional[LineRangeInfo] = None
    eachWayDivisor: Optional[float] = None
    clarifications: Optional[str] = None
    raceType: Optional[str] = None


class EventType(BaseMessage):
    """EventType"""

    id: str
    name: str


class Competition(BaseMessage):
    """Competition"""

    id: str
    name: str


class Event(BaseMessage):
    """Event"""

    id: str
    name: str
    timezone: str
    openDate: str
    countryCode: Optional[str] = None
    venue: Optional[str] = None


class Runner(BaseMessage):
    """
    https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Exchange+Stream+API
    """

    selectionId: int
    runnerName: str
    sortPriority: Optional[int] = None
    handicap: Optional[float] = None
    status: Optional[str] = None
    adjustmentFactor: Optional[float] = None
    metadata: Optional[dict] = None

    @property
    def runner_name(self):
        return self.runnerName

    @property
    def runner_id(self):
        if self.selectionId:
            return self.selectionId
        elif self.metadata.get("runnerId"):
            return int(self.metadata.get("runnerId"))
        return None


class MarketCatalog(BaseMessage):
    """MarketCatalog"""

    marketId: str
    marketName: str
    marketStartTime: str
    description: Description
    totalMatched: float
    runners: list[Runner]
    eventType: EventType
    event: Event
    competition: Optional[Competition] = None

    @property
    def competition_id(self) -> str:
        if not self.competition:
            return ""
        return self.competition.id

    @property
    def competition_name(self) -> str:
        if not self.competition:
            return ""
        return self.competition.name
