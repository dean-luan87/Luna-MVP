# -*- coding: utf-8 -*-
"""Qwen-VL Provider Adapter — Model Manager owned v1 (planning)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.lifecycle.model_registry_state_machine_v1 import (
    is_routing_eligible,
)
from capabilities.midplatform.model_manager.providers.qwen_vl.qwen_vl_request_builder_v1 import (
    build_qwen_vl_provider_request,
)
from capabilities.midplatform.model_manager.providers.qwen_vl.qwen_vl_response_parser_v1 import (
    build_evidence_candidate_from_parsed,
    parse_qwen_vl_provider_response,
)
from capabilities.midplatform.model_manager.luna_model_manager_qwen_vl_types_v1 import (
    MODEL_ID,
    POLICY_REF,
)

MOCK_SCENARIOS = {
    "unknown_scene_hypothesis": "unknown_scene_hypothesis",
    "unsupported_brand_claim": "unsupported_brand_claim",
    "provider_timeout": "provider_timeout",
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[4]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path(__file__).resolve().parents[4]


def _load_fixture(fixture_id: str) -> Dict[str, Any]:
    path = (
        _repo_root()
        / "capabilities/midplatform/teacher_adapter/providers/qwen_vl/fixtures/raw_responses"
        / f"{fixture_id}.json"
    )
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def load_qwen_model_from_registry(model_id: str = MODEL_ID) -> Dict[str, Any]:
    """Load Qwen model record from Model Registry — no hardcoded provider call."""
    registry_path = _repo_root() / "capabilities/midplatform/model_manager/registries/model_registry_v1.json"
    if registry_path.is_file():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        for m in registry.get("models") or []:
            if m.get("model_id") == model_id:
                return dict(m)
    profile_path = _repo_root() / "capabilities/midplatform/model_manager/providers/qwen_vl/qwen_vl_provider_profile_v1.json"
    if profile_path.is_file() and model_id == MODEL_ID:
        return json.loads(profile_path.read_text(encoding="utf-8"))
    return {"model_id": model_id, "lifecycle_state": "candidate", "admission_status": "pending"}


def invoke_qwen_vl_provider(
    *,
    provider_request: Dict[str, Any],
    model_record: Dict[str, Any],
    mock_scenario: Optional[str] = None,
    simulate_timeout: bool = False,
) -> Dict[str, Any]:
    """
    Invoke Qwen-VL provider under Model Manager gate.
    Planning: recorded fixtures only unless live flag set elsewhere.
    """
    invoke_id = _uid("qvp")
    if not is_routing_eligible(
        model_record.get("lifecycle_state", "candidate"),
        admission_status=model_record.get("admission_status", ""),
    ):
        return {
            "invoke_id": invoke_id,
            "invoked": False,
            "skip_reason": "lifecycle_not_eligible",
            "model_id": model_record.get("model_id"),
            "candidate_only": True,
            "not_fact": True,
        }

    if simulate_timeout or mock_scenario == "provider_timeout":
        return {
            "invoke_id": invoke_id,
            "invoked": True,
            "provider_error_candidate": True,
            "error_type": "api_timeout",
            "error_detail": "Qwen-VL API timeout simulated",
            "model_id": model_record.get("model_id"),
            "candidate_only": True,
            "not_fact": True,
        }

    fixture_id = mock_scenario or "unknown_scene_hypothesis"
    raw = _load_fixture(fixture_id)
    if not raw:
        raw = {"raw_response": {"output": {"choices": [{"message": {"content": "{}"}}]}}}

    parsed = parse_qwen_vl_provider_response(
        {"raw_response": raw.get("raw_response", raw), "candidate_only": True},
        request_context=provider_request,
    )
    evidence = {}
    if parsed.get("parse_status") == "ok" and not parsed.get("has_unsupported_claim"):
        evidence = build_evidence_candidate_from_parsed(
            parsed,
            situation=provider_request.get("situation_candidate") or {},
        )

    return {
        "invoke_id": invoke_id,
        "invoked": True,
        "model_id": model_record.get("model_id"),
        "provider_request": provider_request,
        "raw_response_ref": fixture_id,
        "parsed_response": parsed,
        "evidence_candidate": evidence or None,
        "provider_error_candidate": parsed.get("parse_status") == "error",
        "has_unsupported_claim": parsed.get("has_unsupported_claim", False),
        "policy_refs": [POLICY_REF],
        "managed_by": "model_manager",
        "no_fact_write": True,
        "candidate_only": True,
        "not_fact": True,
    }


def review_qwen_provider_evidence(
    *,
    provider_result: Dict[str, Any],
    routing_result: Dict[str, Any],
    plan: Dict[str, Any],
    situation: Dict[str, Any],
) -> Dict[str, Any]:
    """Validate provider evidence — unsupported claims rejected."""
    review_id = _uid("qvr")

    if provider_result.get("provider_error_candidate"):
        return {
            "review_id": review_id,
            "validation_status": "provider_error",
            "provider_error_candidate": True,
            "fallback_required": True,
            "selected_plan_unchanged": True,
            "candidate_only": True,
            "not_fact": True,
        }

    if provider_result.get("has_unsupported_claim"):
        return {
            "review_id": review_id,
            "validation_status": "rejected_by_policy",
            "rejection_reason": "unsupported_claim",
            "conflict_candidates": [{"conflict_type": "unsupported_claim", "candidate_only": True}],
            "selected_plan_unchanged": True,
            "l1_scene_unchanged": True,
            "candidate_only": True,
            "not_fact": True,
        }

    evidence = provider_result.get("evidence_candidate")
    if not evidence and routing_result.get("should_request_teacher"):
        return {
            "review_id": review_id,
            "validation_status": "noop",
            "selected_plan_unchanged": True,
            "candidate_only": True,
            "not_fact": True,
        }

    if evidence:
        return {
            "review_id": review_id,
            "validation_status": "accepted_as_evidence",
            "teacher_evidence_candidate": evidence,
            "selected_plan_unchanged": True,
            "l1_scene_unchanged": True,
            "l1_scene_owner": (situation.get("scene_profile_candidate") or {}).get("owned_by"),
            "original_plan_snapshot": {"goal_type": (plan.get("plan_goal_candidate") or {}).get("goal_type")},
            "candidate_only": True,
            "not_fact": True,
        }

    return {
        "review_id": review_id,
        "validation_status": "noop",
        "not_selected_reason": routing_result.get("routing_reason", "not_routing_eligible"),
        "selected_plan_unchanged": True,
        "candidate_only": True,
        "not_fact": True,
    }
