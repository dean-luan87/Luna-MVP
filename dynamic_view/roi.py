from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple

BBox = Tuple[int, int, int, int]


@dataclass(frozen=True)
class RoiHint:
    """
    ROI 提示：只影响感知层采样/阈值，不是事实
    """

    area_type: str
    hint: str
    bbox: Optional[BBox] = None
    weight: float = 1.1
    constraints: Optional[Dict[str, Any]] = None
    source: str = "attention_window"
