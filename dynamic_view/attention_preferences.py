from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AttentionPreference:
    roi_kind: str
    weight: float
    source: str
    environment_id: str
