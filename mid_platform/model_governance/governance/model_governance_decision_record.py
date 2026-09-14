# -*- coding: utf-8 -*-
"""占位：中台对蜂巢建议的治理决策留痕（与 schemas.ModelGovernanceRecord 不同；无自动执行）。"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict


@dataclass
class ModelGovernanceDecisionRecord:
    decision_record_id: str
    recommendation_id: str
    model_id: str
    decision_result: str
    decision_reason: str
    decision_constraints: Dict[str, Any] = field(default_factory=dict)
    decision_timestamp: str = ""
    effective_scope: str = ""
    rollback_plan: str = ""
    requires_followup_review: bool = False
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ModelGovernanceDecisionRecord:
        return cls(
            decision_record_id=str(d["decision_record_id"]),
            recommendation_id=str(d["recommendation_id"]),
            model_id=str(d["model_id"]),
            decision_result=str(d["decision_result"]),
            decision_reason=str(d["decision_reason"]),
            decision_constraints=dict(d.get("decision_constraints", {})),
            decision_timestamp=str(d.get("decision_timestamp", "")),
            effective_scope=str(d.get("effective_scope", "")),
            rollback_plan=str(d.get("rollback_plan", "")),
            requires_followup_review=bool(d.get("requires_followup_review", False)),
            notes=str(d.get("notes", "")),
        )
