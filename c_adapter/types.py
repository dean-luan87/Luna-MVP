from dataclasses import dataclass
from enum import Enum


class CDecision(Enum):
    PASS = "pass"
    HOLD = "hold"
    STOP = "stop"


@dataclass
class CInput:
    entity_id: str
    attributes: dict
