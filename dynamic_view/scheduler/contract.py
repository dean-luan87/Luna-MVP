from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ContractMode(Enum):
    AUTONOMOUS = "autonomous"
    TASK = "task"


@dataclass(frozen=True)
class ObservationPolicy:
    max_invisible_time: float
    priority: int
    recovery_grace_time: float


@dataclass(frozen=True)
class ObservationContract:
    contract_id: str
    mode: ContractMode
    entity_id: Optional[str]
    policy: ObservationPolicy
