from __future__ import annotations

from typing import Any, Dict, Mapping, Tuple

from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_visual_invocation_contract_v1 import (
    SCHEMA_VERSION,
    not_fact,
)


def _tuple_str(value: Any) -> Tuple[str, ...]:
    if value is None:
        return tuple()
    if isinstance(value, str):
        return (value,)
    return tuple(str(x) for x in value)


def adapt_field_perception_visual_handoff_input_v1(
    payload: Mapping[str, Any],
) -> Dict[str, Any]:
    req = dict(payload.get("field_perception_visual_handoff_request") or payload)
    plan = dict(req.get("field_perception_plan") or {})
    task_context = dict(req.get("task_context") or {})

    adapted = {
        "schema_version": SCHEMA_VERSION,
        "handoff_request_id": str(req.get("handoff_request_id") or "").strip(),
        "field_perception_plan": plan,
        "plan_id": str(plan.get("plan_id") or req.get("plan_id") or "").strip(),
        "task_context": task_context,
        "task_id": str(
            task_context.get("task_id")
            or req.get("task_id")
            or plan.get("task_id")
            or ""
        ).strip(),
        "field_snapshot_ref": str(
            req.get("field_snapshot_ref") or plan.get("field_snapshot_ref") or ""
        ).strip(),
        "information_gap_ref": str(
            req.get("information_gap_ref")
            or f"gap_ref::{plan.get('plan_id') or req.get('handoff_request_id') or 'unknown'}"
        ),
        "information_gap": tuple(
            req.get("information_gap") or plan.get("information_gap") or ()
        ),
        "observation_goal": str(
            req.get("observation_goal") or plan.get("observation_goal") or ""
        ).strip(),
        "target_region": str(
            req.get("target_region") or plan.get("target_region") or ""
        ).strip(),
        "target_entity_types": _tuple_str(
            req.get("target_entity_types") or plan.get("target_entity_types") or ()
        ),
        "requested_visual_capabilities": _tuple_str(
            req.get("requested_visual_capabilities")
            or plan.get("requested_visual_capabilities")
            or ()
        ),
        "preferred_model_candidates": _tuple_str(
            req.get("preferred_model_candidates")
            or plan.get("preferred_model_candidates")
            or ()
        ),
        "fallback_model_candidates": _tuple_str(
            req.get("fallback_model_candidates")
            or plan.get("fallback_model_candidates")
            or ()
        ),
        "resolution_level": str(
            req.get("resolution_level") or plan.get("resolution_level") or "standard"
        ).strip(),
        "temporal_window": str(
            req.get("temporal_window") or plan.get("temporal_window") or "normal"
        ).strip(),
        "observation_priority": str(
            req.get("observation_priority")
            or plan.get("observation_priority")
            or "normal"
        ).strip(),
        "confidence_requirement": float(
            req.get("confidence_requirement")
            or plan.get("confidence_requirement")
            or 0.8
        ),
        "expected_evidence_types": _tuple_str(
            req.get("expected_evidence_types")
            or plan.get("expected_evidence_types")
            or ()
        ),
        "stop_condition": dict(
            req.get("stop_condition") or plan.get("stop_condition") or {}
        ),
        "reobserve_condition": dict(
            req.get("reobserve_condition") or plan.get("reobserve_condition") or {}
        ),
        "available_visual_capabilities": _tuple_str(
            req.get("available_visual_capabilities") or ()
        ),
        "available_model_assets": tuple(req.get("available_model_assets") or ()),
        "model_manager_snapshot": dict(req.get("model_manager_snapshot") or {}),
        "resource_budget": dict(req.get("resource_budget") or {}),
        "invocation_history": tuple(req.get("invocation_history") or ()),
        "permission_context": dict(req.get("permission_context") or {}),
        "version_snapshot": dict(req.get("version_snapshot") or {}),
        "trace_context": dict(req.get("trace_context") or {}),
        "vision_required": bool(req.get("vision_required", True)),
    }
    adapted["input_valid"] = (
        bool(adapted["handoff_request_id"])
        and bool(adapted["plan_id"])
        and bool(adapted["task_id"])
    )
    adapted["rejection_reasons"] = tuple(
        reason
        for reason, failed in (
            ("missing_handoff_request_id", not bool(adapted["handoff_request_id"])),
            ("missing_plan_id", not bool(adapted["plan_id"])),
            ("missing_task_id", not bool(adapted["task_id"])),
            ("missing_field_snapshot_ref", not bool(adapted["field_snapshot_ref"])),
            ("missing_observation_goal", not bool(adapted["observation_goal"])),
        )
        if failed
    )
    adapted.update(not_fact())
    return adapted
