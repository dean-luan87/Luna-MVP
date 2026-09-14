# -*- coding: utf-8 -*-
"""占位：蜂巢建议对象（无自动生效）。"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict


@dataclass
class HiveModelRecommendation:
    recommendation_id: str
    model_id: str
    recommendation_type: str
    recommendation_priority: str
    recommendation_reason: str
    based_on_score_record_id: str
    suggested_action: str
    suggested_constraints: Dict[str, Any] = field(default_factory=dict)
    requires_human_review: bool = False
    requires_shadow_validation: bool = False
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> HiveModelRecommendation:
        return cls(
            recommendation_id=str(d["recommendation_id"]),
            model_id=str(d["model_id"]),
            recommendation_type=str(d["recommendation_type"]),
            recommendation_priority=str(d["recommendation_priority"]),
            recommendation_reason=str(d["recommendation_reason"]),
            based_on_score_record_id=str(d["based_on_score_record_id"]),
            suggested_action=str(d["suggested_action"]),
            suggested_constraints=dict(d.get("suggested_constraints", {})),
            requires_human_review=bool(d.get("requires_human_review", False)),
            requires_shadow_validation=bool(d.get("requires_shadow_validation", False)),
            notes=str(d.get("notes", "")),
        )


def sample_recommendation() -> HiveModelRecommendation:
    return HiveModelRecommendation(
        recommendation_id="hmr_sample_001",
        model_id="demo_model",
        recommendation_type="keep_observing",
        recommendation_priority="low",
        recommendation_reason="placeholder",
        based_on_score_record_id="hsr_sample_001",
        suggested_action="none",
    )
