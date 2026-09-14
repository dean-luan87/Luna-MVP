# -*- coding: utf-8 -*-
"""占位：中台接收蜂巢建议的 intake 记录（无自动消费编排）。"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass
class ModelRecommendationIntakeRecord:
    recommendation_id: str
    model_id: str
    recommendation_type: str
    intake_status: str
    intake_timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ModelRecommendationIntakeRecord:
        return cls(
            recommendation_id=str(d["recommendation_id"]),
            model_id=str(d["model_id"]),
            recommendation_type=str(d["recommendation_type"]),
            intake_status=str(d["intake_status"]),
            intake_timestamp=str(d["intake_timestamp"]),
        )
