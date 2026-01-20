from dataclasses import dataclass, field
from typing import List, Optional, Literal


@dataclass(frozen=True)
class EnvelopeSignal:
    present: bool
    level: Literal["NONE", "LOW", "MEDIUM", "HIGH"]
    domain: Literal["VISION", "EMOTION", "SOCIAL", "SYSTEM"]
    type: str
    time_to_event: Optional[float]
    reason_codes: List[str] = field(default_factory=list)
