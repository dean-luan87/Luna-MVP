# -*- coding: utf-8 -*-
"""Qwen-VL Model Usage Metrics — Model Manager evaluation input v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

MODEL_ID = "qwen_vl"


@dataclass
class QwenVLModelUsageMetrics:
    model_id: str = MODEL_ID
    usage_count: int = 0
    selected_count: int = 0
    noop_count: int = 0
    rejected_output_count: int = 0
    provider_error_count: int = 0
    accepted_evidence_count: int = 0
    latency_ms_total: float = 0.0
    cost_estimate_total: float = 0.0
    events: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def unsupported_claim_rate(self) -> float:
        denom = self.selected_count or 1
        return round(self.rejected_output_count / denom, 4)

    @property
    def useful_evidence_rate(self) -> float:
        denom = self.selected_count or 1
        return round(self.accepted_evidence_count / denom, 4)

    @property
    def latency_ms_avg(self) -> float:
        return round(self.latency_ms_total / self.selected_count, 2) if self.selected_count else 0.0

    def record_selected(self, *, case_id: str, latency_ms: float = 0.0) -> None:
        self.usage_count += 1
        self.selected_count += 1
        self.latency_ms_total += latency_ms
        self.events.append({"event": "provider_selected", "case_id": case_id, "model_id": self.model_id})

    def record_noop(self, *, case_id: str, reason: str) -> None:
        self.usage_count += 1
        self.noop_count += 1
        self.events.append({"event": "provider_noop", "case_id": case_id, "reason": reason})

    def record_validation(self, *, case_id: str, status: str) -> None:
        if status == "accepted_as_evidence":
            self.accepted_evidence_count += 1
        elif status == "rejected_by_policy":
            self.rejected_output_count += 1
        elif status == "provider_error":
            self.provider_error_count += 1
        self.events.append({"event": "validation", "case_id": case_id, "status": status})

    def to_evaluation_metrics(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "usage_count": self.usage_count,
            "selected_count": self.selected_count,
            "noop_count": self.noop_count,
            "rejected_output_count": self.rejected_output_count,
            "provider_error_count": self.provider_error_count,
            "accepted_evidence_count": self.accepted_evidence_count,
            "unsupported_claim_rate": self.unsupported_claim_rate,
            "useful_evidence_rate": self.useful_evidence_rate,
            "evidence_accept_rate": self.useful_evidence_rate,
            "rejection_rate": self.unsupported_claim_rate,
            "latency_ms_avg": self.latency_ms_avg,
            "cost_estimate_total": self.cost_estimate_total,
            "candidate_only": True,
            "not_fact": True,
        }


_GLOBAL_METRICS = QwenVLModelUsageMetrics()


def get_qwen_model_usage_metrics() -> QwenVLModelUsageMetrics:
    return _GLOBAL_METRICS


def reset_qwen_model_usage_metrics() -> None:
    global _GLOBAL_METRICS
    _GLOBAL_METRICS = QwenVLModelUsageMetrics()
