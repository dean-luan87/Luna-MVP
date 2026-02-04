from enum import Enum


class ObservationState(Enum):
    NOT_SEEN = "not_seen"
    APPEARED = "appeared"
    STABLE = "stable"
    INVISIBLE = "invisible"
    RECOVERED = "recovered"
    DISAPPEARED = "disappeared"
