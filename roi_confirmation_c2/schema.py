from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Literal

ConfirmMode = Literal["AUTO", "MANUAL", "REJECTED"]


@dataclass(frozen=True)
class ROIDefaultEntry:
    roi_kind: str
    mode: ConfirmMode
    version: str
    reason: Dict

    def to_dict(self):
        return asdict(self)
