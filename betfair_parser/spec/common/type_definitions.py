import datetime
from typing import Annotated, TypeAlias

import msgspec

from betfair_parser.spec.common.messages import BaseMessage


Date = Annotated[datetime.datetime, msgspec.Meta(title="Date", tz=True)]
IDType = Annotated[
    int, msgspec.Meta(title="IDType", description="integer data, but defined and encoded as string", ge=0)
]

# Betfair defines several input fields as set. Nevertheless, the JSON data is encoded as list. For convenience,
# these data fields should accept a set or a list as input. But currently, there seems to be no good
# solution, to satisfy as well the type checkers as the restrictions of msgspec. Sticking with set
# seems to be the most correct option for now.

Set: TypeAlias = set

# Type aliases as defined within the XML specification with minimalistic validation added.

MarketType = Annotated[str, msgspec.Meta(title="MarketType")]
Venue = Annotated[str, msgspec.Meta(title="Venue")]
MarketId = Annotated[str, msgspec.Meta(title="MarketId")]  # The only ID, that actually needs to be a string
SelectionId = Annotated[int, msgspec.Meta(title="SelectionId", ge=0)]  # The only ID, that is actually defined as int
Handicap = Annotated[float, msgspec.Meta(title="Handicap", gt=-1000, lt=1000)]
EventId = Annotated[IDType, msgspec.Meta(title="EventId")]
EventTypeId = Annotated[IDType, msgspec.Meta(title="EventTypeId")]
CountryCode = Annotated[str, msgspec.Meta(title="CountryCode", min_length=2, max_length=3)]
ExchangeId = Annotated[IDType, msgspec.Meta(title="ExchangeId")]
CompetitionId = Annotated[IDType, msgspec.Meta(title="CompetitionId")]
Price = Annotated[float, msgspec.Meta(title="Price", ge=0, le=1001)]
Size = Annotated[float, msgspec.Meta(title="Size", ge=0)]
BetId = Annotated[IDType, msgspec.Meta(title="BetId")]
MatchId = Annotated[IDType, msgspec.Meta(title="MatchId")]
CustomerRef = Annotated[str, msgspec.Meta(title="CustomerRef")]
CustomerOrderRef = Annotated[str, msgspec.Meta(title="CustomerOrderRef")]
CustomerStrategyRef = Annotated[str, msgspec.Meta(title="CustomerStrategyRef")]


class TimeRange(BaseMessage, frozen=True):
    from_: Date | None = msgspec.field(name="from", default=None)
    to: Date | None = None
