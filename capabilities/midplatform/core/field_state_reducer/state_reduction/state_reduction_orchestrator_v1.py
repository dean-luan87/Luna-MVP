from __future__ import annotations

from typing import Any, Dict, Tuple

from .state_reduction_application_planner_v1 import build_policy_application_plan
from .state_reduction_candidate_builder_v1 import build_field_state_candidate
from .state_reduction_conflict_v1 import reduce_conflict
from .state_reduction_contract_loader_v1 import load_state_reduction_contracts_v1
from .state_reduction_core_v1 import reduce_state_core
from .state_reduction_overlay_v1 import reduce_overlay
from .state_reduction_provenance_replay_v1 import (
    build_state_reduction_trace_and_replay,
    candidate_to_min_payload,
)
from .state_reduction_selection_handoff_v1 import validate_selection_handoff
from .state_reduction_state_transition_engine_v1 import evaluate_state_transition
from .state_reduction_types_v1 import (
    ConflictReductionResult,
    OverlayReductionResult,
    PolicyApplicationPlan,
    SelectionHandoffInput,
    StateReductionResult,
    StateTransitionResult,
)


def reduce_selected_policy_to_state_candidate_v1(
    handoff_input: SelectionHandoffInput,
    contracts: Dict[str, Dict[str, Any]] | None = None,
) -> Tuple[StateReductionResult, Dict[str, Any]]:
    _ = contracts if contracts is not None else load_state_reduction_contracts_v1()

    handoff_status, handoff_reasons = validate_selection_handoff(handoff_input)
    application_plan = build_policy_application_plan(
        handoff_input,
        handoff_status,
        handoff_reasons,
    )

    conflict_result = reduce_conflict(
        handoff_input, application_plan.selected_policy_ids
    )
    overlay_result = reduce_overlay(handoff_input, application_plan.selected_policy_ids)

    requested_status, candidate_value, previous_state_ref, core_reasons, core_steps = (
        reduce_state_core(
            handoff_input,
            application_plan,
            conflict_result,
            overlay_result,
        )
    )

    current_status = str(
        handoff_input.existing_state_snapshot.get("status", "candidate")
    )
    transition_result = evaluate_state_transition(
        current_status=current_status,
        requested_status=requested_status,
        temporal_snapshot=handoff_input.temporal_snapshot,
        conflict_snapshot=handoff_input.conflict_snapshot,
        plan_intended_change=application_plan.intended_change_type,
    )

    rejection_reasons = tuple(
        dict.fromkeys(
            list(handoff_reasons)
            + list(application_plan.blocking_reasons)
            + list(core_reasons)
            + list(conflict_result.rejection_reasons)
            + list(overlay_result.rejection_reasons)
            + list(transition_result.rejection_reasons)
        )
    )

    trace_seed_id = f"state_reduction_trace_{handoff_input.reducer_run_id}"
    pre_candidate = build_field_state_candidate(
        handoff_input=handoff_input,
        application_plan=application_plan,
        requested_status=requested_status,
        candidate_value=candidate_value,
        previous_state_ref=previous_state_ref,
        transition_result=transition_result,
        trace_ref=trace_seed_id,
        replay_key="",
        conflicting_event_refs=conflict_result.conflicting_event_refs,
        overlay_result=overlay_result,
    )

    trace, replay_key, _ = build_state_reduction_trace_and_replay(
        reducer_run_id=handoff_input.reducer_run_id,
        field_id=handoff_input.field_id,
        state_type=handoff_input.state_type,
        evaluation_refs=tuple(handoff_input.policy_evaluation_refs),
        selection_refs=(
            handoff_input.selection_trace_ref,
            handoff_input.selection_replay_key,
        ),
        application_steps=application_plan.ordered_application_steps,
        state_reduction_steps=core_steps,
        transition_steps=transition_result.transition_trace,
        conflict_decisions=conflict_result.decision_steps,
        overlay_decisions=overlay_result.decision_steps,
        rejected_operations=rejection_reasons,
        version_snapshots=dict(handoff_input.version_snapshots),
        candidate_payload=candidate_to_min_payload(pre_candidate),
    )

    candidate = build_field_state_candidate(
        handoff_input=handoff_input,
        application_plan=application_plan,
        requested_status=requested_status,
        candidate_value=candidate_value,
        previous_state_ref=previous_state_ref,
        transition_result=transition_result,
        trace_ref=trace.trace_id,
        replay_key=replay_key,
        conflicting_event_refs=conflict_result.conflicting_event_refs,
        overlay_result=overlay_result,
    )

    reduction_status = "state_candidate_built"
    if handoff_status != "accepted":
        reduction_status = "handoff_rejected"
    elif not transition_result.transition_allowed:
        reduction_status = "invalid_transition"
    elif application_plan.intended_change_type == "no_state_change":
        reduction_status = "no_state_change"

    result = StateReductionResult(
        reducer_run_id=handoff_input.reducer_run_id,
        field_id=handoff_input.field_id,
        state_type=handoff_input.state_type,
        reduction_status=reduction_status,
        handoff_status=handoff_status,
        selected_policy_ids=tuple(handoff_input.selected_policy_ids),
        policy_application_plan=application_plan,
        state_candidate=candidate,
        transition_result=transition_result,
        conflict_result=conflict_result,
        overlay_result=overlay_result,
        rejection_reasons=rejection_reasons,
        trace_ref=trace.trace_id,
        replay_key=replay_key,
        version_snapshots=dict(handoff_input.version_snapshots),
        real_state_store_write_implemented=False,
        fact_admission_implemented=False,
        action_trigger_implemented=False,
        runtime_implemented=False,
    )

    trace_dict = {
        "trace_id": trace.trace_id,
        "evaluation_refs": list(trace.evaluation_refs),
        "selection_refs": list(trace.selection_refs),
        "application_steps": list(trace.application_steps),
        "state_reduction_steps": list(trace.state_reduction_steps),
        "transition_steps": list(trace.transition_steps),
        "conflict_decisions": list(trace.conflict_decisions),
        "overlay_decisions": list(trace.overlay_decisions),
        "rejected_operations": list(trace.rejected_operations),
        "version_snapshots": dict(trace.version_snapshots),
        "resulting_candidate_hash": trace.resulting_candidate_hash,
        "replay_key": trace.replay_key,
    }

    return result, trace_dict


def result_to_dict(result: StateReductionResult) -> Dict[str, Any]:
    plan: PolicyApplicationPlan = result.policy_application_plan
    transition: StateTransitionResult = result.transition_result
    conflict: ConflictReductionResult = result.conflict_result
    overlay: OverlayReductionResult = result.overlay_result

    candidate = result.state_candidate
    candidate_dict = None
    if candidate is not None:
        candidate_dict = {
            "state_candidate_id": candidate.state_candidate_id,
            "field_id": candidate.field_id,
            "state_type": candidate.state_type,
            "candidate_status": candidate.candidate_status,
            "candidate_value": dict(candidate.candidate_value),
            "temporal_status": candidate.temporal_status,
            "confidence_snapshot": dict(candidate.confidence_snapshot),
            "supporting_event_refs": list(candidate.supporting_event_refs),
            "conflicting_event_refs": list(candidate.conflicting_event_refs),
            "overlay_refs": list(candidate.overlay_refs),
            "owner_correction_refs": list(candidate.owner_correction_refs),
            "provenance_refs": list(candidate.provenance_refs),
            "selected_policy_ids": list(candidate.selected_policy_ids),
            "policy_application_plan_ref": candidate.policy_application_plan_ref,
            "previous_state_ref": candidate.previous_state_ref,
            "transition_result": dict(candidate.transition_result),
            "trace_ref": candidate.trace_ref,
            "replay_key": candidate.replay_key,
            "candidate_only": candidate.candidate_only,
            "fact_admitted": candidate.fact_admitted,
            "persisted": candidate.persisted,
        }

    return {
        "reducer_run_id": result.reducer_run_id,
        "field_id": result.field_id,
        "state_type": result.state_type,
        "reduction_status": result.reduction_status,
        "handoff_status": result.handoff_status,
        "selected_policy_ids": list(result.selected_policy_ids),
        "policy_application_plan": {
            "application_plan_id": plan.application_plan_id,
            "selected_policy_ids": list(plan.selected_policy_ids),
            "ordered_application_steps": list(plan.ordered_application_steps),
            "intended_change_type": plan.intended_change_type,
            "target_state_status": plan.target_state_status,
            "supporting_event_refs": list(plan.supporting_event_refs),
            "blocking_reasons": list(plan.blocking_reasons),
            "deferred_actions": list(plan.deferred_actions),
            "candidate_only": plan.candidate_only,
        },
        "state_candidate": candidate_dict,
        "transition_result": {
            "requested_transition": transition.requested_transition,
            "transition_allowed": transition.transition_allowed,
            "transition_status": transition.transition_status,
            "required_evidence": list(transition.required_evidence),
            "rejection_reasons": list(transition.rejection_reasons),
            "transition_trace": list(transition.transition_trace),
        },
        "conflict_result": {
            "conflict_status": conflict.conflict_status,
            "preserve_conflict": conflict.preserve_conflict,
            "provisional_candidate_allowed": conflict.provisional_candidate_allowed,
            "conflicting_event_refs": list(conflict.conflicting_event_refs),
            "rejection_reasons": list(conflict.rejection_reasons),
            "decision_steps": list(conflict.decision_steps),
        },
        "overlay_result": {
            "overlay_status": overlay.overlay_status,
            "overlay_refs": list(overlay.overlay_refs),
            "substrate_mutated": overlay.substrate_mutated,
            "refresh_evidence_required": overlay.refresh_evidence_required,
            "rejection_reasons": list(overlay.rejection_reasons),
            "decision_steps": list(overlay.decision_steps),
        },
        "rejection_reasons": list(result.rejection_reasons),
        "trace_ref": result.trace_ref,
        "replay_key": result.replay_key,
        "version_snapshots": dict(result.version_snapshots),
        "real_state_store_write_implemented": result.real_state_store_write_implemented,
        "fact_admission_implemented": result.fact_admission_implemented,
        "action_trigger_implemented": result.action_trigger_implemented,
        "runtime_implemented": result.runtime_implemented,
    }
