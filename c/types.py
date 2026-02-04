from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class CDecision(Enum):
    PASS = "pass"
    HOLD = "hold"
    STOP = "stop"


@dataclass
class CInput:
    perception_health: str
    obstacle_distance_m: Optional[float]
    human_proximity_m: Optional[float]
    traffic_light: Optional[str]
    crosswalk_signal: Optional[str]
    passage_state: Optional[str]
    floor_state: Optional[str]
    facility_state: Optional[str]
    confidence: Dict[str, float]
    device_state: Dict[str, Any]


@dataclass
class CResult:
    decision: CDecision
    reason_code: str
    layer: str
    facts: Dict[str, Any]
