# -*- coding: utf-8 -*-
"""占位：蜂巢评分输入包（无自动评分逻辑）。"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass
class HiveModelScoreInputPack:
    score_input_pack_id: str
    model_id: str
    model_version: str
    score_scope: str
    time_range: str
    source_usage_records: List[str] = field(default_factory=list)
    source_quality_records: List[str] = field(default_factory=list)
    source_governance_records: List[str] = field(default_factory=list)
    source_library_records: List[str] = field(default_factory=list)
    source_whitebox_summaries: List[str] = field(default_factory=list)
    sample_size: int = 0
    aggregation_note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> HiveModelScoreInputPack:
        return cls(
            score_input_pack_id=str(d["score_input_pack_id"]),
            model_id=str(d["model_id"]),
            model_version=str(d["model_version"]),
            score_scope=str(d["score_scope"]),
            time_range=str(d["time_range"]),
            source_usage_records=list(d.get("source_usage_records", [])),
            source_quality_records=list(d.get("source_quality_records", [])),
            source_governance_records=list(d.get("source_governance_records", [])),
            source_library_records=list(d.get("source_library_records", [])),
            source_whitebox_summaries=list(d.get("source_whitebox_summaries", [])),
            sample_size=int(d.get("sample_size", 0)),
            aggregation_note=str(d.get("aggregation_note", "")),
        )


def sample_input_pack() -> HiveModelScoreInputPack:
    return HiveModelScoreInputPack(
        score_input_pack_id="hip_sample_001",
        model_id="demo_model",
        model_version="v0",
        score_scope="task_specific",
        time_range="last_7d",
        sample_size=42,
    )
