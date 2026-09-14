"""Memory candidates remain non-factual until explicitly validated."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
from uuid import uuid4

from .experience_record import ExperienceRecord


@dataclass(frozen=True)
class MemoryCandidate:
    scope: str
    source_record_id: str
    content: Mapping[str, Any]
    confidence: float
    relevance: float
    validation_status: str = "candidate"
    candidate_id: str = field(default_factory=lambda: str(uuid4()))
    retention_class: str = "normal"

    @classmethod
    def from_record(cls, record: ExperienceRecord, retention_class: str = "normal") -> "MemoryCandidate":
        return cls(
            scope=record.scope,
            source_record_id=record.record_id,
            content={"event": dict(record.event), "outcome": dict(record.outcome), "context": dict(record.context)},
            confidence=0.5,
            relevance=0.5,
            retention_class=retention_class,
        )

    def validated(self) -> "MemoryCandidate":
        return MemoryCandidate(
            scope=self.scope,
            source_record_id=self.source_record_id,
            content=dict(self.content),
            confidence=self.confidence,
            relevance=self.relevance,
            validation_status="validated",
            candidate_id=self.candidate_id,
            retention_class=self.retention_class,
        )

    def rejected(self) -> "MemoryCandidate":
        return MemoryCandidate(
            scope=self.scope,
            source_record_id=self.source_record_id,
            content=dict(self.content),
            confidence=self.confidence,
            relevance=self.relevance,
            validation_status="rejected",
            candidate_id=self.candidate_id,
            retention_class=self.retention_class,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "scope": self.scope,
            "source_record_id": self.source_record_id,
            "content": dict(self.content),
            "confidence": self.confidence,
            "relevance": self.relevance,
            "validation_status": self.validation_status,
            "retention_class": self.retention_class,
        }
