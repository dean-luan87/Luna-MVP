from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Dict, Any

AdviceSource = Literal["pal", "roi", "ocr"]


@dataclass
class AdviceCandidate:
    advice_id: str
    source: AdviceSource
    level: str  # "emergency" | "normal"
    kind: str
    priority: float
    payload: Dict[str, Any]
