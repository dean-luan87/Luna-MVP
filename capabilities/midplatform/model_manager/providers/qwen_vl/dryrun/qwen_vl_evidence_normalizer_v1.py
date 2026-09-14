# -*- coding: utf-8 -*-
"""Qwen-VL Evidence Normalizer — Model Manager dryrun pipeline v1."""

from __future__ import annotations

from typing import Any, Dict, Optional

from capabilities.midplatform.teacher_adapter.providers.qwen_vl.evidence_normalizer_v1 import (
    normalize_teacher_evidence,
)

FORBIDDEN_EVIDENCE_FIELDS = (
    "scene_fact",
    "selected_plan",
    "tool_execution",
    "fact_write",
    "internal_memory",
)


def normalize_qwen_evidence_candidate(
    *,
    parsed_response: Dict[str, Any],
    situation_candidate: Dict[str, Any],
    plan_candidate: Optional[Dict[str, Any]] = None,
    raw_envelope: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Raw Response → Parser → Evidence Normalizer → evidence_candidate.
    Reuses frozen teacher normalizer; output owned by Model Manager.
    """
    normalized = normalize_teacher_evidence(
        parsed_response=parsed_response,
        situation_candidate=situation_candidate,
        plan_candidate=plan_candidate,
        raw_envelope=raw_envelope,
    )
    normalized["managed_by"] = "model_manager"
    normalized["provider_pipeline"] = ["raw_response", "parser", "evidence_normalizer", "validation"]
    for forbidden in FORBIDDEN_EVIDENCE_FIELDS:
        if forbidden in normalized:
            normalized.pop(forbidden, None)
    return normalized


def detect_unsupported_claim(normalized: Dict[str, Any]) -> bool:
    """Detect unsupported claim after normalizer governance."""
    if normalized.get("unsupported_claim"):
        return True
    risks = normalized.get("policy_risk_candidates") or []
    return "unsupported_claim" in risks
