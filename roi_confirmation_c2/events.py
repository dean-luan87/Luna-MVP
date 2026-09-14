from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Literal, Dict

ManualAction = Literal["CONFIRM", "REJECT", "REVOKE"]


@dataclass(frozen=True)
class ROIManualEvent:
    roi_kind: str
    action: ManualAction
    actor: str
    reason: Dict
    timestamp: float

    def to_dict(self):
        return asdict(self)
