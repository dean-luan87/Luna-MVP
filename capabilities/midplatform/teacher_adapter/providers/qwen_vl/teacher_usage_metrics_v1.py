# -*- coding: utf-8 -*-
"""Teacher Usage Metrics — track real provider invocation quality."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class TeacherUsageMetrics:
    teacher_request_count: int = 0
    teacher_noop_count: int = 0
    teacher_admitted_count: int = 0
    accepted_evidence_count: int = 0
    rejected_claim_count: int = 0
    latency_ms_total: float = 0.0
    cost_estimate_total: float = 0.0
    token_usage_total: int = 0
    events: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def teacher_noop_rate(self) -> float:
        denom = self.teacher_request_count + self.teacher_noop_count
        return round(self.teacher_noop_count / denom, 4) if denom else 0.0

    @property
    def accepted_evidence_rate(self) -> float:
        return (
            round(self.accepted_evidence_count / self.teacher_admitted_count, 4)
            if self.teacher_admitted_count
            else 0.0
        )

    @property
    def rejected_claim_rate(self) -> float:
        return (
            round(self.rejected_claim_count / self.teacher_admitted_count, 4)
            if self.teacher_admitted_count
            else 0.0
        )

    @property
    def latency_ms_avg(self) -> float:
        return (
            round(self.latency_ms_total / self.teacher_admitted_count, 2)
            if self.teacher_admitted_count
            else 0.0
        )

    def record_noop(self, *, case_id: str, reason: str) -> None:
        self.teacher_noop_count += 1
        self.events.append({"event": "teacher_noop", "case_id": case_id, "reason": reason})

    def record_admitted(
        self,
        *,
        case_id: str,
        raw_envelope: Dict[str, Any],
        validation_status: str,
    ) -> None:
        self.teacher_request_count += 1
        self.teacher_admitted_count += 1
        latency = float(raw_envelope.get("latency_ms") or 0)
        self.latency_ms_total += latency
        usage = raw_envelope.get("usage") or {}
        tokens = int(usage.get("total_tokens") or usage.get("input_tokens", 0) + usage.get("output_tokens", 0))
        self.token_usage_total += tokens
        self.cost_estimate_total += round(tokens * 0.00001, 6)
        if validation_status == "accepted_as_evidence":
            self.accepted_evidence_count += 1
        if validation_status == "rejected_by_policy":
            self.rejected_claim_count += 1
        self.events.append({
            "event": "teacher_admitted",
            "case_id": case_id,
            "validation_status": validation_status,
            "latency_ms": latency,
            "live_call": raw_envelope.get("live_call"),
        })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "teacher_request_count": self.teacher_request_count,
            "teacher_noop_count": self.teacher_noop_count,
            "teacher_noop_rate": self.teacher_noop_rate,
            "teacher_admitted_count": self.teacher_admitted_count,
            "accepted_evidence_count": self.accepted_evidence_count,
            "accepted_evidence_rate": self.accepted_evidence_rate,
            "rejected_claim_count": self.rejected_claim_count,
            "rejected_claim_rate": self.rejected_claim_rate,
            "latency_ms_total": self.latency_ms_total,
            "latency_ms_avg": self.latency_ms_avg,
            "cost_estimate_total": self.cost_estimate_total,
            "token_usage_total": self.token_usage_total,
            "events": self.events,
        }


_GLOBAL_METRICS = TeacherUsageMetrics()


def get_teacher_usage_metrics() -> TeacherUsageMetrics:
    return _GLOBAL_METRICS


def reset_teacher_usage_metrics() -> TeacherUsageMetrics:
    global _GLOBAL_METRICS
    _GLOBAL_METRICS = TeacherUsageMetrics()
    return _GLOBAL_METRICS
