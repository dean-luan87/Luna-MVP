from dataclasses import dataclass
from enum import Enum


class CState(Enum):
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"


@dataclass
class CStateContext:
    state: CState
    fail_count: int
