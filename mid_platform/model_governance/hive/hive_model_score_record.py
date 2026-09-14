# -*- coding: utf-8 -*-
"""占位：蜂巢评分记录（无自动评分逻辑）。"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass
class HiveModelScoreRecord:
    score_record_id: str
    model_id: str
    model_version: str
    score_scope: str
    score_timestamp: str
    overall_score: float
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    risk_flags: List[str] = field(default_factory=list)
    positioning_result: str = ""
    confidence_level: str = "low"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> HiveModelScoreRecord:
        return cls(
            score_record_id=str(d["score_record_id"]),
            model_id=str(d["model_id"]),
            model_version=str(d["model_version"]),
            score_scope=str(d["score_scope"]),
            score_timestamp=str(d["score_timestamp"]),
            overall_score=float(d["overall_score"]),
            dimension_scores=dict(d.get("dimension_scores", {})),
            risk_flags=list(d.get("risk_flags", [])),
            positioning_result=str(d.get("positioning_result", "")),
            confidence_level=str(d.get("confidence_level", "low")),
        )


def sample_score_record() -> HiveModelScoreRecord:
    return HiveModelScoreRecord(
        score_record_id="hsr_sample_001",
        model_id="demo_model",
        model_version="v0",
        score_scope="global",
        score_timestamp="2026-04-01T00:00:00Z",
        overall_score=0.0,
        dimension_scores={
            "stability_score": 0.0,
            "quality_score": 0.0,
            "latency_score": 0.0,
            "cost_score": 0.0,
            "governance_friendliness_score": 0.0,
            "evolvability_score": 0.0,
        },
    )
