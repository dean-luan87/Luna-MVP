from dataclasses import dataclass
from typing import List


@dataclass
class DistortionReport:
    distorted: bool
    severity: str
    reason_codes: List[str]
    recommended_action: str
