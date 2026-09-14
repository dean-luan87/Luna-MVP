# -*- coding: utf-8 -*-
"""Candidate Output Contract v1 — unified candidate output constraints for Luna Validation Factory."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

CONTRACT_ID = "candidate_output_contract_v1"

BASE_CONSTRAINTS: Dict[str, Any] = {
    "candidate_only": True,
    "fact_status": "not_fact",
    "write_allowed": False,
    "runtime_action_allowed": False,
    "source_chain_required": True,
    "trial_scope_required": True,
    "provenance_required": True,
    "timestamp_required_when_applicable": True,
}

CANDIDATE_TYPES: Tuple[str, ...] = (
    "visual_observation_candidate",
    "ocr_result_candidate",
    "navigation_guidance_candidate",
    "task_response_candidate",
    "speech_response_candidate",
    "memory_lookup_candidate",
    "world_model_readonly_candidate",
)


def validate_candidate_output(
    candidate: Dict[str, Any],
    *,
    expected_type: str,
    require_timestamp: bool = False,
) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if candidate.get("output_type") != expected_type and candidate.get("candidate_type") != expected_type:
        issues.append(f"type must be {expected_type}")
    if candidate.get("candidate_only") is not True:
        issues.append("candidate_only must be true")
    if candidate.get("fact_status") != "not_fact":
        issues.append("fact_status must be not_fact")
    if candidate.get("write_allowed") is True:
        issues.append("write_allowed must be false")
    if candidate.get("runtime_action_allowed") is True:
        issues.append("runtime_action_allowed must be false")
    if BASE_CONSTRAINTS["source_chain_required"] and not candidate.get("source_chain"):
        issues.append("source_chain required")
    if BASE_CONSTRAINTS["trial_scope_required"] and not candidate.get("trial_scope"):
        issues.append("trial_scope required")
    if require_timestamp and not candidate.get("observation_timestamp") and not candidate.get("timestamp"):
        issues.append("timestamp required")
    return len(issues) == 0, issues


def build_contract_document(*, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    m = dict(meta or {})
    return {
        "contract_id": CONTRACT_ID,
        "version": "v1",
        "base_constraints": dict(BASE_CONSTRAINTS),
        "candidate_types": list(CANDIDATE_TYPES),
        "entrypoint": "validate_candidate_output(candidate, expected_type=...)",
        **m,
    }
