# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class ModelUsageRecord:
    """模型调用留痕（宪法第十条最小字段）。"""

    record_id: str
    model_id: str
    task_type: str
    caller_module: str
    input_contract_version: str
    output_contract_version: str
    latency_ms: float
    success: bool
    cost_estimate: Optional[float]
    timestamp: float

    def __post_init__(self) -> None:
        self.record_id = str(self.record_id).strip()
        self.model_id = str(self.model_id).strip()
        if not self.record_id or not self.model_id:
            raise ValueError("record_id and model_id are required")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ModelUsageRecord:
        return cls(
            record_id=str(d["record_id"]),
            model_id=str(d["model_id"]),
            task_type=str(d["task_type"]),
            caller_module=str(d["caller_module"]),
            input_contract_version=str(d["input_contract_version"]),
            output_contract_version=str(d["output_contract_version"]),
            latency_ms=float(d["latency_ms"]),
            success=bool(d["success"]),
            cost_estimate=float(d["cost_estimate"]) if d.get("cost_estimate") is not None else None,
            timestamp=float(d["timestamp"]),
        )
