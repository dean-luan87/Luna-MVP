from dataclasses import dataclass
from enum import Enum


class CAction(Enum):
    STOP = "STOP"
    HOLD = "HOLD"
    AVOID_LEFT = "AVOID_LEFT"
    AVOID_RIGHT = "AVOID_RIGHT"
    REQUEST_TAKEOVER = "REQUEST_TAKEOVER"
    NONE = "NONE"


@dataclass
class COutput:
    action: CAction
    confidence: float
    reason: str
    c_state: "CState"
    threshold_version_id: str = "default"

    def __post_init__(self) -> None:
        if not isinstance(self.action, CAction):
            raise ValueError("COutput.action must be a CAction enum.")
        if not (0.0 <= float(self.confidence) <= 1.0):
            raise ValueError("COutput.confidence must be within [0, 1].")
        if not isinstance(self.threshold_version_id, str):
            raise ValueError("COutput.threshold_version_id must be a string.")
