from typing import Optional

from betfair_parser.spec.common import BaseMessage, Date, Request, Response
from betfair_parser.strenums import DocumentedEnum, doc


class RaceStatus(DocumentedEnum):
    DORMANT = doc("There is no data available for this race.")
    DELAYED = doc("The start of the race has been delayed")
    PARADING = doc("The horses/greyhounds are in the parade ring")
    GOINGDOWN = doc("The horses are going down to the starting post")
    GOINGBEHIND = doc("The horses are going behind the stalls")
    APPROACHING = doc("The greyhounds are approaching the traps")
    GOINGINTRAPS = doc("The greyhounds are being put in the traps")
    HARERUNNING = doc("The hare has been started")
    ATTHEPOST = doc("The horses are at the post")
    OFF = doc("The greyhound/horse race has started")
    FINISHED = doc("The race has finished")
    FINALRESULT = doc("The result has been declared (Greyhounds only)")
    FALSESTART = doc("There has been a false start")
    PHOTOGRAPH = doc("The result of the race is subject to a photo finish")
    RESULT = doc("The result of the race has been announced")
    WEIGHEDIN = doc("The jockeys have weighed in")
    RACEVOID = doc("The race has been declared void")
    NORACE = doc("The race has been declared a no race")
    MEETINGABANDONED = doc("The meeting has been abandoned")
    RERUN = doc("The race will be rerun")
    ABANDONED = doc("The race has been abandoned")


class ResponseCode(DocumentedEnum):
    OK = doc("Data returned successfully")
    NO_NEW_UPDATES = doc("No updates since the passes UpdateSequence")
    NO_LIVE_DATA_AVAILABLE = doc("Event scores are no longer available or are not on the schedule")
    SERVICE_UNAVAILABLE = doc("Data feed for the event type (tennis/football etc) is currently unavailable")
    UNEXPECTED_ERROR = doc("An unexpected error occurred retrieving score data")
    LIVE_DATA_TEMPORARILY_UNAVAILABLE = doc(
        "Live Data feed for this event/match is temporarily unavailable, data could potentially be stale"
    )


class RaceDetails(BaseMessage, kw_only=True, frozen=True):
    meetingId: str  # The unique Id for the meeting equivalent to the eventId as returned by listEvents
    raceId: str  # The unique Id for the race in the format meetingId.raceTime (hhmm)
    raceStatus: RaceStatus  # The current status of the race.
    lastUpdated: Date  # This is the time the data was last updated
    sequence: int  # This is the unique identifier associated to each update of the data
    responseCode: ResponseCode


class listRaceDetailsParams(BaseMessage, frozen=True):
    meetingIds: Optional[set[str]] = None  # Restricts the results to the specified meeting IDs.
    raceIds: Optional[set[str]] = None  # Restricts the results to the specified race IDs.


class listRaceDetail(Request, kw_only=True, frozen=True):
    method = "ScoresAPING/v1.0/listRaceDetails"
    params: listRaceDetailsParams
    return_type = Response[list[RaceDetails]]
