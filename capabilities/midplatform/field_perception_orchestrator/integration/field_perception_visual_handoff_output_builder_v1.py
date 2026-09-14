from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_visual_invocation_contract_v1 import (
    BOUNDARY_FALSE_FIELDS,
    CAPABILITY_ID,
    INTEGRATION_STATUSES,
    not_fact,
)


def resolve_integration_status_v1(
    input_candidate: Mapping[str, Any],
    deduplication_result: Mapping[str, Any],
    budget_decision: Mapping[str, Any],
    eligible_model_candidates: tuple[Mapping[str, Any], ...],
    observation_request_candidate: Mapping[str, Any] | None,
) -> str:
    if not bool(input_candidate.get("input_valid", False)):
        return "invalid_input"
    if bool(
        (input_candidate.get("permission_context") or {}).get("request_rejected", False)
    ):
        return "permission_rejected"
    if bool((input_candidate.get("permission_context") or {}).get("conflicted", False)):
        return "conflicted"
    if not bool(input_candidate.get("vision_required", True)):
        return "no_visual_invocation_required"
    if not bool(input_candidate.get("requested_visual_capabilities")):
        return "insufficient_plan"

    dedup = str(deduplication_result.get("deduplication_status") or "")
    if dedup == "duplicate_active_request":
        return "duplicate_suppressed"
    if dedup == "fresh_evidence_reuse":
        return "fresh_evidence_reused"

    if not eligible_model_candidates:
        return "no_eligible_model"

    level = str(
        (budget_decision.get("budget_decision") or {}).get("budget_level") or "normal"
    )
    if level in {"constrained", "critical"}:
        return "budget_degraded"

    if observation_request_candidate is not None:
        return "handoff_ready"
    return "observation_request_candidate_ready"


def build_visual_handoff_result_v1(
    integration_status: str,
    handoff_id: str,
    input_candidate: Mapping[str, Any],
    vision_request_candidate: Mapping[str, Any] | None,
    model_requirement_candidate: Mapping[str, Any] | None,
    eligible_model_candidates: tuple[Mapping[str, Any], ...],
    rejected_model_candidates: tuple[Mapping[str, Any], ...],
    observation_request_candidate: Mapping[str, Any] | None,
    deduplication_result: Mapping[str, Any],
    budget_decision: Mapping[str, Any],
    result_link_contract: Mapping[str, Any] | None,
    diagnostics: Mapping[str, Any],
    trace_ref: str,
    replay_key: str,
    rejection_reasons: tuple[str, ...],
) -> Dict[str, Any]:
    status = (
        integration_status
        if integration_status in INTEGRATION_STATUSES
        else "internal_error"
    )
    output = {
        "capability_id": CAPABILITY_ID,
        "integration_status": status,
        "handoff_id": handoff_id,
        "plan_id": input_candidate.get("plan_id"),
        "task_id": input_candidate.get("task_id"),
        "field_snapshot_ref": input_candidate.get("field_snapshot_ref"),
        "information_gap_ref": input_candidate.get("information_gap_ref"),
        "observation_goal": input_candidate.get("observation_goal"),
        "vision_required": bool(input_candidate.get("vision_required", True)),
        "vision_request_candidate": vision_request_candidate,
        "model_requirement_candidate": model_requirement_candidate,
        "eligible_model_candidates": tuple(eligible_model_candidates),
        "rejected_model_candidates": tuple(rejected_model_candidates),
        "observation_request_candidate": observation_request_candidate,
        "deduplication_result": dict(deduplication_result),
        "budget_decision": dict(budget_decision),
        "result_link_contract": result_link_contract,
        "diagnostics": dict(diagnostics),
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "rejection_reasons": tuple(rejection_reasons),
        "boundary_flags": {k: False for k in BOUNDARY_FALSE_FIELDS},
        **not_fact(),
    }
    for field in BOUNDARY_FALSE_FIELDS:
        output[field] = False
    return output
