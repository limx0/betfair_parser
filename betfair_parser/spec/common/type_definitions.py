import datetime
from typing import Annotated, Optional, Union

import msgspec

from betfair_parser.spec.common.messages import BaseMessage


# Type aliases with minimalistic validation. More would be great.

Date = Annotated[datetime.datetime, msgspec.Meta(title="Date", tz=True)]
SelectionId = Annotated[int, msgspec.Meta(title="SelectionId")]
Venue = Annotated[str, msgspec.Meta(title="Venue")]
MarketId = Annotated[str, msgspec.Meta(title="MarketId")]
Handicap = Annotated[float, msgspec.Meta(title="Handicap")]
EventId = Annotated[str, msgspec.Meta(title="EventId")]
EventTypeId = Annotated[int, msgspec.Meta(title="EventTypeId")]
CountryCode = Annotated[str, msgspec.Meta(title="CountryCode", min_length=2, max_length=3)]
ExchangeId = Annotated[str, msgspec.Meta(title="ExchangeId")]
CompetitionId = Annotated[str, msgspec.Meta(title="CompetitionId")]
Price = Annotated[float, msgspec.Meta(title="Price")]
Size = Annotated[float, msgspec.Meta(title="Size")]
BetId = Annotated[Union[str, int], msgspec.Meta(title="BetId")]
MatchId = Annotated[Union[str, int], msgspec.Meta(title="MatchId")]
CustomerRef = Annotated[Union[str, int], msgspec.Meta(title="CustomerRef")]
CustomerOrderRef = Annotated[Union[str, int], msgspec.Meta(title="CustomerOrderRef")]
CustomerStrategyRef = Annotated[Union[str, int], msgspec.Meta(title="CustomerStrategyRef")]


class TimeRange(BaseMessage, frozen=True):
    from_: Optional[Date] = msgspec.field(name="from", default=None)
    to: Optional[Date] = None
