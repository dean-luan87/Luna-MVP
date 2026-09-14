from __future__ import annotations

from typing import Any, Dict, Iterable, Tuple

from .field_state_reducer_module_types_v1 import (
    FieldStateReducerModuleResultV1,
    MODULE_STATUS_REGISTRY_V1,
)


def _module_status_from(
    *,
    adapted_input_ok: bool,
    evaluation_statuses: Iterable[str],
    admitted_event_count: int,
    selection_status: str,
    reduction_status: str,
    transition_status: str,
    transition_allowed: bool,
    conflict_status: str,
    field_state_candidate: Dict[str, Any] | None,
    rejection_reasons: Tuple[str, ...],
) -> str:
    if not adapted_input_ok:
        return "rejected_input"

    statuses = set(evaluation_statuses)

    if (
        selection_status == "internal_error"
        or reduction_status == "internal_error"
        or transition_status == "internal_error"
        or (not transition_allowed and reduction_status == "invalid_transition")
    ):
        return "internal_error"

    if "governance_review_required" in statuses:
        return "governance_review_required"

    if conflict_status == "unresolved" or "unresolved_conflict" in statuses:
        return "unresolved"
    if conflict_status == "conflicted":
        return "conflicted"

    candidate_temporal_status = ""
    if field_state_candidate is not None:
        candidate_temporal_status = str(
            field_state_candidate.get("temporal_status", "")
        )

    if statuses == {"temporally_invalid"} or candidate_temporal_status in {
        "expired",
        "suspended",
        "revoked",
        "superseded",
    }:
        return "temporally_invalid"

    supporting_event_count = 0
    if field_state_candidate is not None:
        supporting_event_count = len(
            field_state_candidate.get("supporting_event_refs", []) or []
        )

    if statuses == {"insufficient_evidence"}:
        if (
            admitted_event_count == 0
            and supporting_event_count == 0
            and selection_status == "no_eligible_candidate"
            and reduction_status == "no_state_change"
        ):
            return "no_state_change"
        return "insufficient_evidence"

    if any(reason == "owner_review_required" for reason in rejection_reasons):
        return "governance_review_required"

    if selection_status == "no_state_change" or reduction_status == "no_state_change":
        return "no_state_change"

    if "temporally_invalid" in statuses:
        return "temporally_invalid"

    if "insufficient_evidence" in statuses:
        return "insufficient_evidence"

    if not transition_allowed:
        return "internal_error"

    if field_state_candidate is None:
        return "internal_error"

    return "completed_candidate"


def build_module_output_surface_v1(
    *,
    reducer_request_id: str,
    reducer_run_id: str,
    field_id: str,
    state_type: str,
    adapted_input_ok: bool,
    evaluation_summary: Dict[str, Any],
    selection_summary: Dict[str, Any],
    reduction_summary: Dict[str, Any],
    transition_summary: Dict[str, Any],
    field_state_candidate: Dict[str, Any] | None,
    read_model_projection_candidate: Dict[str, Any] | None,
    unresolved_items: Tuple[str, ...],
    rejection_reasons: Tuple[str, ...],
    diagnostics: Dict[str, Any],
    trace_ref: str,
    replay_key: str,
    contract_versions: Dict[str, str],
) -> FieldStateReducerModuleResultV1:
    module_status = _module_status_from(
        adapted_input_ok=adapted_input_ok,
        evaluation_statuses=evaluation_summary.get("evaluation_statuses", []),
        admitted_event_count=int(evaluation_summary.get("admitted_event_count", 0)),
        selection_status=str(selection_summary.get("selection_status", "")),
        reduction_status=str(reduction_summary.get("reduction_status", "")),
        transition_status=str(transition_summary.get("transition_status", "")),
        transition_allowed=bool(transition_summary.get("transition_allowed", False)),
        conflict_status=str(reduction_summary.get("conflict_status", "none")),
        field_state_candidate=field_state_candidate,
        rejection_reasons=tuple(rejection_reasons),
    )

    if module_status not in MODULE_STATUS_REGISTRY_V1:
        module_status = "internal_error"

    return FieldStateReducerModuleResultV1(
        reducer_request_id=reducer_request_id,
        reducer_run_id=reducer_run_id,
        field_id=field_id,
        state_type=state_type,
        module_status=module_status,
        evaluation_summary=dict(evaluation_summary),
        selection_summary=dict(selection_summary),
        reduction_summary=dict(reduction_summary),
        transition_summary=dict(transition_summary),
        field_state_candidate=field_state_candidate,
        read_model_projection_candidate=read_model_projection_candidate,
        unresolved_items=tuple(unresolved_items),
        rejection_reasons=tuple(rejection_reasons),
        diagnostics=dict(diagnostics),
        trace_ref=trace_ref,
        replay_key=replay_key,
        contract_versions=dict(contract_versions),
        candidate_only=True,
        fact_admitted=False,
        state_store_write_executed=False,
        action_trigger_executed=False,
        runtime_execution=False,
    )


def module_result_to_dict(result: FieldStateReducerModuleResultV1) -> Dict[str, Any]:
    return {
        "reducer_request_id": result.reducer_request_id,
        "reducer_run_id": result.reducer_run_id,
        "field_id": result.field_id,
        "state_type": result.state_type,
        "module_status": result.module_status,
        "evaluation_summary": dict(result.evaluation_summary),
        "selection_summary": dict(result.selection_summary),
        "reduction_summary": dict(result.reduction_summary),
        "transition_summary": dict(result.transition_summary),
        "field_state_candidate": result.field_state_candidate,
        "read_model_projection_candidate": result.read_model_projection_candidate,
        "unresolved_items": list(result.unresolved_items),
        "rejection_reasons": list(result.rejection_reasons),
        "diagnostics": dict(result.diagnostics),
        "trace_ref": result.trace_ref,
        "replay_key": result.replay_key,
        "contract_versions": dict(result.contract_versions),
        "candidate_only": result.candidate_only,
        "fact_admitted": result.fact_admitted,
        "state_store_write_executed": result.state_store_write_executed,
        "action_trigger_executed": result.action_trigger_executed,
        "runtime_execution": result.runtime_execution,
    }
