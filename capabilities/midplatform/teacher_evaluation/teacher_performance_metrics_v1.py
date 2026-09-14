# -*- coding: utf-8 -*-
"""Teacher Performance Metrics — aggregate evaluation statistics v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class TeacherPerformanceMetrics:
    sample_count: int = 0
    admitted_count: int = 0
    noop_count: int = 0
    accepted_evidence_count: int = 0
    accepted_alternative_count: int = 0
    rejected_count: int = 0
    unsupported_claim_count: int = 0
    scene_conflict_count: int = 0
    policy_violation_count: int = 0
    noop_correct_count: int = 0
    latency_ms_total: float = 0.0
    cost_estimate_total: float = 0.0
    value_score_total: float = 0.0
    records: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def evidence_accept_rate(self) -> float:
        denom = self.admitted_count or 1
        return round((self.accepted_evidence_count + self.accepted_alternative_count) / denom, 4)

    @property
    def rejection_rate(self) -> float:
        denom = self.admitted_count or 1
        return round(self.rejected_count / denom, 4)

    @property
    def hallucination_rate(self) -> float:
        denom = self.admitted_count or 1
        return round((self.unsupported_claim_count + self.scene_conflict_count) / denom, 4)

    @property
    def unsupported_claim_rate(self) -> float:
        denom = self.admitted_count or 1
        return round(self.unsupported_claim_count / denom, 4)

    @property
    def scene_conflict_rate(self) -> float:
        denom = self.admitted_count or 1
        return round(self.scene_conflict_count / denom, 4)

    @property
    def policy_violation_rate(self) -> float:
        denom = self.admitted_count or 1
        return round(self.policy_violation_count / denom, 4)

    @property
    def useful_evidence_rate(self) -> float:
        return self.evidence_accept_rate

    @property
    def teacher_noop_correct_rate(self) -> float:
        denom = self.noop_count or 1
        return round(self.noop_correct_count / denom, 4) if self.noop_count else 0.0

    @property
    def latency_ms_avg(self) -> float:
        return round(self.latency_ms_total / self.admitted_count, 2) if self.admitted_count else 0.0

    @property
    def teacher_value_score_avg(self) -> float:
        return round(self.value_score_total / self.sample_count, 4) if self.sample_count else 0.0

    def add_record(self, record: Dict[str, Any]) -> None:
        self.sample_count += 1
        self.records.append(record)
        admission = record.get("admission_status", "")
        validation = record.get("validation_status", "")
        outcome = record.get("evaluation_outcome", "")

        if admission == "noop":
            self.noop_count += 1
            if record.get("teacher_noop_correct"):
                self.noop_correct_count += 1
            return

        self.admitted_count += 1
        self.latency_ms_total += float(record.get("latency_ms") or 0)
        self.cost_estimate_total += float(record.get("cost_estimate") or 0)
        self.value_score_total += float(record.get("value_score") or 0)

        if validation == "accepted_as_evidence":
            self.accepted_evidence_count += 1
        elif validation == "accepted_as_alternative":
            self.accepted_alternative_count += 1
        elif validation == "rejected_by_policy":
            self.rejected_count += 1

        if outcome == "unsupported_claim":
            self.unsupported_claim_count += 1
        if outcome == "scene_conflict":
            self.scene_conflict_count += 1
        if outcome in ("policy_rejection", "unsupported_claim", "scene_conflict"):
            self.policy_violation_count += 1

    def to_reliability_metrics(self, *, provider_id: str, metrics_id: str) -> Dict[str, Any]:
        return {
            "metrics_id": metrics_id,
            "provider_id": provider_id,
            "sample_count": self.sample_count,
            "evidence_accept_rate": self.evidence_accept_rate,
            "rejection_rate": self.rejection_rate,
            "hallucination_rate": self.hallucination_rate,
            "unsupported_claim_rate": self.unsupported_claim_rate,
            "scene_conflict_rate": self.scene_conflict_rate,
            "policy_violation_rate": self.policy_violation_rate,
            "useful_evidence_rate": self.useful_evidence_rate,
            "teacher_noop_correct_rate": self.teacher_noop_correct_rate,
            "latency_ms_avg": self.latency_ms_avg,
            "cost_estimate_total": round(self.cost_estimate_total, 6),
            "teacher_value_score": self.teacher_value_score_avg,
            "candidate_only": True,
            "not_fact": True,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample_count": self.sample_count,
            "evidence_accept_rate": self.evidence_accept_rate,
            "rejection_rate": self.rejection_rate,
            "hallucination_rate": self.hallucination_rate,
            "unsupported_claim_rate": self.unsupported_claim_rate,
            "scene_conflict_rate": self.scene_conflict_rate,
            "policy_violation_rate": self.policy_violation_rate,
            "useful_evidence_rate": self.useful_evidence_rate,
            "teacher_noop_correct_rate": self.teacher_noop_correct_rate,
            "latency_ms_avg": self.latency_ms_avg,
            "cost_estimate_total": self.cost_estimate_total,
            "teacher_value_score_avg": self.teacher_value_score_avg,
        }


_GLOBAL_METRICS = TeacherPerformanceMetrics()


def get_performance_metrics() -> TeacherPerformanceMetrics:
    return _GLOBAL_METRICS


def reset_performance_metrics() -> TeacherPerformanceMetrics:
    global _GLOBAL_METRICS
    _GLOBAL_METRICS = TeacherPerformanceMetrics()
    return _GLOBAL_METRICS
