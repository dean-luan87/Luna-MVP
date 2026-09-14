# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class ModelQualityRecord:
    """输出质量留痕。"""

    record_id: str
    model_id: str
    task_type: str
    validator_passed: bool
    mixed_preserved: Optional[bool]
    clarification_needed: Optional[bool]
    unsupported_quality: Optional[str]
    quality_label: Optional[str]
    notes: Optional[str]
    timestamp: float

    def __post_init__(self) -> None:
        self.record_id = str(self.record_id).strip()
        self.model_id = str(self.model_id).strip()
        if not self.record_id or not self.model_id:
            raise ValueError("record_id and model_id are required")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ModelQualityRecord:
        return cls(
            record_id=str(d["record_id"]),
            model_id=str(d["model_id"]),
            task_type=str(d["task_type"]),
            validator_passed=bool(d["validator_passed"]),
            mixed_preserved=d.get("mixed_preserved") if d.get("mixed_preserved") is None else bool(d["mixed_preserved"]),
            clarification_needed=(
                d.get("clarification_needed")
                if d.get("clarification_needed") is None
                else bool(d["clarification_needed"])
            ),
            unsupported_quality=(
                None if d.get("unsupported_quality") is None else str(d["unsupported_quality"])
            ),
            quality_label=None if d.get("quality_label") is None else str(d["quality_label"]),
            notes=None if d.get("notes") is None else str(d["notes"]),
            timestamp=float(d["timestamp"]),
        )
