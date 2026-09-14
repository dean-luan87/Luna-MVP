from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class PalRoiHint:
    roi_kind: str
    area: Optional[Tuple[int, int, int, int]]
    confidence: float
    reason: str
    ttl_s: float
