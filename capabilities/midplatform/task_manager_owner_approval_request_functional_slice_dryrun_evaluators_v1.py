# -*- coding: utf-8 -*-
"""Per-slice dryrun evaluators for Owner Approval Request functional slice dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

FORBIDDEN_TRANSITION_FLAGS: Tuple[str, ...] = (
    "candidate_to_real_request_issued",
    "candidate_to_authorization_request_created",
    "candidate_to_grant_issued",
    "package_to_authorization_request",
    "package_to_authorization_grant",
    "package_to_real_request_issuance",
    "absent_to_request_record_created",
    "absent_to_approval_record_created",
    "absent_to_ack_record_created",
    "absent_to_evidence_bound_created",
    "boundary_to_closure_executed",
    "absent_to_notification_sent",
    "absent_to_grant",
    "not_frozen_to_foundation_frozen",
    "absent_to_runtime_enabled",
    "absent_to_adapter_implemented",
    "absent_to_whitebox_integrated",
)


def _absence_met(ctx: Dict[str, Any], keys: List[str]) -> bool:
    absence = ctx.get("absence") or {}
    return all(absence.get(k) is True for k in keys)


def _dryrun_base(slice_plan: Dict[str, Any], *, slice_id: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "slice_id": slice_id,
        "dryrun_id": f"{slice_id}_dryrun_v1",
        "primary_result": slice_plan.get("primary_result"),
        "fallback_or_defer_strategy": slice_plan.get("fallback_or_defer_strategy"),
        "execution_allowed": False,
        "test_executed": True,
        "real_execution": False,
        "forbidden_state_transitions_observed": [],
        **meta,
    }


def eval_owner_approval_request_candidate_lifecycle(
    slice_plan: Dict[str, Any], *, ctx: Dict[str, Any], meta: Dict[str, Any]
) -> Dict[str, Any]:
    sid = "owner_approval_request_candidate_lifecycle"
    pkg = ctx.get("auth_package") or {}
    routing = ctx.get("routing") or {}
    entry_condition_met = (
        ctx.get("prior_functional_slice_planning_go") is True
        and ctx.get("prior_integrated_implementation_go") is True
        and ctx.get("prior_authorization_preparation_dryrun_go") is True
    )
    input_objects_present = (
        pkg.get("authorization_package_candidate") is True
        and routing.get("missing_conditions_routing_complete") is True
    )
    output_objects_candidate = (
        pkg.get("authorization_package_candidate") is True
        and ctx.get("real_request_issuance_authorized") is False
    )
    state_path_closed = len(slice_plan.get("state_path") or []) >= 5
    forbidden_absent = (
        ctx.get("request_issued_absent") is True
        and ctx.get("authorization_request_absent") is True
        and ctx.get("grant_absent") is True
    )
    success_criteria_met = input_objects_present and output_objects_candidate and forbidden_absent
    failure_criteria_recognizable = bool(slice_plan.get("failure_criteria"))
    absence_met = _absence_met(ctx, list(slice_plan.get("required_absence_conditions") or []))
    primary_result_reached = (
        entry_condition_met
        and output_objects_candidate
        and forbidden_absent
        and absence_met
    )
    dryrun_ok = (
        primary_result_reached
        and entry_condition_met
        and input_objects_present
        and state_path_closed
        and forbidden_absent
        and success_criteria_met
        and failure_criteria_recognizable
        and bool(slice_plan.get("fallback_or_defer_strategy"))
        and absence_met
    )
    return {
        **_dryrun_base(slice_plan, slice_id=sid, meta=meta),
        "primary_result_reached": primary_result_reached,
        "entry_condition_met": entry_condition_met,
        "input_objects_present": input_objects_present,
        "output_objects_candidate": output_objects_candidate,
        "state_path_closed": state_path_closed,
        "forbidden_state_transitions_absent": forbidden_absent,
        "success_criteria_met": success_criteria_met,
        "failure_criteria_recognizable": failure_criteria_recognizable,
        "required_absence_conditions_met": absence_met,
        "fallback_or_defer_strategy_present": bool(slice_plan.get("fallback_or_defer_strategy")),
        f"{sid}_dryrun_ok": dryrun_ok,
    }


def eval_authorization_preparation_lifecycle(
    slice_plan: Dict[str, Any], *, ctx: Dict[str, Any], meta: Dict[str, Any]
) -> Dict[str, Any]:
    sid = "authorization_preparation_lifecycle"
    pkg = ctx.get("auth_package") or {}
    checklist = ctx.get("checklist") or {}
    items = {i.get("item_id"): i for i in checklist.get("items") or []}
    entry_condition_met = pkg.get("issuance_authorization_preparation_package_complete") is True
    input_objects_present = pkg.get("package_id") == "issuance_authorization_preparation_package_v1"
    output_objects_candidate = (
        pkg.get("authorization_package_candidate") is True
        and pkg.get("executes_real_authorization") is False
    )
    state_path_closed = len(slice_plan.get("state_path") or []) >= 5
    forbidden_absent = (
        ctx.get("authorization_request_absent") is True
        and ctx.get("grant_absent") is True
        and ctx.get("real_request_issuance_authorized") is False
    )
    success_criteria_met = (
        output_objects_candidate
        and items.get("owner_operator_explicit_approval", {}).get("satisfied") is False
        and items.get("authorization_request_readiness", {}).get("satisfied") is False
        and forbidden_absent
    )
    failure_criteria_recognizable = bool(slice_plan.get("failure_criteria"))
    absence_met = _absence_met(ctx, list(slice_plan.get("required_absence_conditions") or []))
    primary_result_reached = success_criteria_met and absence_met and forbidden_absent
    dryrun_ok = (
        primary_result_reached
        and entry_condition_met
        and input_objects_present
        and state_path_closed
        and forbidden_absent
        and failure_criteria_recognizable
        and bool(slice_plan.get("fallback_or_defer_strategy"))
        and absence_met
    )
    return {
        **_dryrun_base(slice_plan, slice_id=sid, meta=meta),
        "primary_result_reached": primary_result_reached,
        "entry_condition_met": entry_condition_met,
        "input_objects_present": input_objects_present,
        "output_objects_candidate": output_objects_candidate,
        "state_path_closed": state_path_closed,
        "forbidden_state_transitions_absent": forbidden_absent,
        "success_criteria_met": success_criteria_met,
        "failure_criteria_recognizable": failure_criteria_recognizable,
        "required_absence_conditions_met": absence_met,
        "fallback_or_defer_strategy_present": bool(slice_plan.get("fallback_or_defer_strategy")),
        f"{sid}_dryrun_ok": dryrun_ok,
    }


def eval_record_approval_ack_evidence_closure_lifecycle(
    slice_plan: Dict[str, Any], *, ctx: Dict[str, Any], meta: Dict[str, Any]
) -> Dict[str, Any]:
    sid = "record_approval_ack_evidence_closure_lifecycle"
    closure = ctx.get("closure_boundary") or {}
    entry_condition_met = closure.get("record_approval_ack_evidence_boundary_complete") is True
    input_objects_present = len(closure.get("rows") or []) >= 4
    output_objects_candidate = (
        ctx.get("request_record_absent") is True
        and ctx.get("approval_record_absent") is True
        and ctx.get("ack_record_absent") is True
        and ctx.get("evidence_bound_record_absent") is True
    )
    state_path_closed = len(slice_plan.get("state_path") or []) >= 6
    forbidden_absent = output_objects_candidate and ctx.get("closure_not_executed") is True
    success_criteria_met = forbidden_absent and entry_condition_met
    failure_criteria_recognizable = bool(slice_plan.get("failure_criteria"))
    absence_met = _absence_met(ctx, list(slice_plan.get("required_absence_conditions") or []))
    primary_result_reached = success_criteria_met and absence_met
    dryrun_ok = (
        primary_result_reached
        and entry_condition_met
        and input_objects_present
        and state_path_closed
        and forbidden_absent
        and failure_criteria_recognizable
        and bool(slice_plan.get("fallback_or_defer_strategy"))
        and absence_met
    )
    return {
        **_dryrun_base(slice_plan, slice_id=sid, meta=meta),
        "primary_result_reached": primary_result_reached,
        "entry_condition_met": entry_condition_met,
        "input_objects_present": input_objects_present,
        "output_objects_candidate": output_objects_candidate,
        "state_path_closed": state_path_closed,
        "forbidden_state_transitions_absent": forbidden_absent,
        "success_criteria_met": success_criteria_met,
        "failure_criteria_recognizable": failure_criteria_recognizable,
        "required_absence_conditions_met": absence_met,
        "fallback_or_defer_strategy_present": bool(slice_plan.get("fallback_or_defer_strategy")),
        f"{sid}_dryrun_ok": dryrun_ok,
    }


def eval_absence_and_rollback_safety_lifecycle(
    slice_plan: Dict[str, Any], *, ctx: Dict[str, Any], meta: Dict[str, Any]
) -> Dict[str, Any]:
    sid = "absence_and_rollback_safety_lifecycle"
    entry_condition_met = ctx.get("non_execution_boundary_ok") is True
    input_objects_present = bool(ctx.get("absence"))
    output_objects_candidate = _absence_met(ctx, list(slice_plan.get("required_absence_conditions") or []))
    state_path_closed = len(slice_plan.get("state_path") or []) >= 7
    forbidden_absent = output_objects_candidate and not ctx.get("runtime_forbidden_violation")
    success_criteria_met = forbidden_absent and entry_condition_met
    failure_criteria_recognizable = bool(slice_plan.get("failure_criteria"))
    absence_met = output_objects_candidate
    primary_result_reached = success_criteria_met
    dryrun_ok = (
        primary_result_reached
        and entry_condition_met
        and input_objects_present
        and state_path_closed
        and forbidden_absent
        and failure_criteria_recognizable
        and bool(slice_plan.get("fallback_or_defer_strategy"))
        and absence_met
    )
    return {
        **_dryrun_base(slice_plan, slice_id=sid, meta=meta),
        "primary_result_reached": primary_result_reached,
        "entry_condition_met": entry_condition_met,
        "input_objects_present": input_objects_present,
        "output_objects_candidate": output_objects_candidate,
        "state_path_closed": state_path_closed,
        "forbidden_state_transitions_absent": forbidden_absent,
        "success_criteria_met": success_criteria_met,
        "failure_criteria_recognizable": failure_criteria_recognizable,
        "required_absence_conditions_met": absence_met,
        "fallback_or_defer_strategy_present": bool(slice_plan.get("fallback_or_defer_strategy")),
        f"{sid}_dryrun_ok": dryrun_ok,
    }


SLICE_EVALUATORS = {
    "owner_approval_request_candidate_lifecycle": eval_owner_approval_request_candidate_lifecycle,
    "authorization_preparation_lifecycle": eval_authorization_preparation_lifecycle,
    "record_approval_ack_evidence_closure_lifecycle": eval_record_approval_ack_evidence_closure_lifecycle,
    "absence_and_rollback_safety_lifecycle": eval_absence_and_rollback_safety_lifecycle,
}
