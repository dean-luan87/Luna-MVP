# -*- coding: utf-8 -*-
"""占位：图书馆单条经验（无自动提炼）。"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass
class LibraryExperienceRecord:
    experience_id: str
    source_scope: str
    source_task_type: str
    source_model_id: Optional[str]
    problem_type: str
    context_summary: str
    evidence_refs: List[str]
    raw_confidence: float
    library_status: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> LibraryExperienceRecord:
        return cls(
            experience_id=str(d["experience_id"]),
            source_scope=str(d["source_scope"]),
            source_task_type=str(d["source_task_type"]),
            source_model_id=(
                None if d.get("source_model_id") in (None, "") else str(d["source_model_id"])
            ),
            problem_type=str(d["problem_type"]),
            context_summary=str(d.get("context_summary", "")),
            evidence_refs=list(d.get("evidence_refs", [])),
            raw_confidence=float(d.get("raw_confidence", 0.0)),
            library_status=str(d.get("library_status", "draft")),
        )
