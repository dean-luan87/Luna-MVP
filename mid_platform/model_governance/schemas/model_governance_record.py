# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass
class ModelGovernanceRecord:
    """治理事件留痕。"""

    record_id: str
    model_id: str
    task_type: str
    fallback_triggered: bool
    degradation_triggered: bool
    schema_violation: bool
    illegal_mapping: bool
    governance_blocked: bool
    policy_violation: bool
    timestamp: float

    def __post_init__(self) -> None:
        self.record_id = str(self.record_id).strip()
        self.model_id = str(self.model_id).strip()
        if not self.record_id or not self.model_id:
            raise ValueError("record_id and model_id are required")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ModelGovernanceRecord:
        return cls(
            record_id=str(d["record_id"]),
            model_id=str(d["model_id"]),
            task_type=str(d["task_type"]),
            fallback_triggered=bool(d["fallback_triggered"]),
            degradation_triggered=bool(d["degradation_triggered"]),
            schema_violation=bool(d["schema_violation"]),
            illegal_mapping=bool(d["illegal_mapping"]),
            governance_blocked=bool(d["governance_blocked"]),
            policy_violation=bool(d["policy_violation"]),
            timestamp=float(d["timestamp"]),
        )
