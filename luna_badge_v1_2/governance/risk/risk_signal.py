from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RiskSignal:
    risk_present: bool
    risk_level: Optional[str]
    risk_type: Optional[str]
    time_to_risk: Optional[float]
    confidence: Optional[float]
