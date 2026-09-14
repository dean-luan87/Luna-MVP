# -*- coding: utf-8 -*-
"""
任务优化（task_optimization）协议占位。

描述 task_plan_v1 → task_plan_v2 的可追踪优化，与 PlanDelta 对齐；不直接执行。
详见：docs/architecture/task/LUNA_TASK_PROTOCOL_AND_MODEL_GATE_V1.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TaskOptimizationRecord:
    """单次优化记录：可审计、可进白盒/图书馆。"""

    optimization_id: str
    source_plan_id: str
    target_plan_id: str
    optimization_reason: str
    requires_confirmation: bool = True
    confidence: float = 1.0
    changes_summary: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "optimization_id": self.optimization_id,
            "source_plan_id": self.source_plan_id,
            "target_plan_id": self.target_plan_id,
            "optimization_reason": self.optimization_reason,
            "requires_confirmation": self.requires_confirmation,
            "confidence": self.confidence,
            "changes_summary": list(self.changes_summary),
            "metadata": dict(self.metadata),
        }
