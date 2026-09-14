from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..field_state_reducer_behavior_policy_error_types_v1 import ERROR_NAMESPACE_V1
from .policy_selection_candidate_filter_v1 import filter_eligible_candidates
from .policy_selection_composition_eligibility_v1 import resolve_composition_eligibility
from .policy_selection_contract_loader_v1 import load_policy_selection_contracts_v1
from .policy_selection_exclusion_resolver_v1 import resolve_mutual_exclusion
from .policy_selection_precedence_resolver_v1 import resolve_precedence
from .policy_selection_replay_v1 import build_policy_selection_replay_key
from .policy_selection_types_v1 import (
    PolicySelectionInput,
    PolicySelectionResult,
    PolicySelectionTrace,
)


def _snapshot_versions(selection_input: PolicySelectionInput) -> Dict[str, str]:
    return {
        "policy_registry_version": selection_input.policy_registry_version,
        "eligibility_matrix_version": selection_input.eligibility_matrix_version,
        "precedence_matrix_version": selection_input.precedence_matrix_version,
        "composition_contract_version": selection_input.composition_contract_version,
        "replay_contract_version": selection_input.replay_contract_version,
    }


def _input_validation_reasons(selection_input: PolicySelectionInput) -> Tuple[str, ...]:
    reasons: List[str] = []
    if not selection_input.selection_id:
        reasons.append("invalid_input")
    if not selection_input.reducer_run_id:
        reasons.append("invalid_input")
    if not selection_input.field_id:
        reasons.append("invalid_input")
    if not selection_input.state_type:
        reasons.append("invalid_input")
    if not selection_input.policy_registry_version:
        reasons.append("missing_version_snapshot")
    if not selection_input.eligibility_matrix_version:
        reasons.append("missing_version_snapshot")
    if not selection_input.precedence_matrix_version:
        reasons.append("missing_version_snapshot")
    if not selection_input.composition_contract_version:
        reasons.append("missing_version_snapshot")
    if not selection_input.replay_contract_version:
        reasons.append("missing_version_snapshot")
    return tuple(dict.fromkeys(reasons))


def select_policy_v1(
    selection_input: PolicySelectionInput,
    contracts: Dict[str, Dict[str, Any]] | None = None,
) -> Tuple[PolicySelectionResult, PolicySelectionTrace]:
    loaded = (
        contracts if contracts is not None else load_policy_selection_contracts_v1()
    )
    versions = _snapshot_versions(selection_input)

    input_eval_ids = tuple(
        str(row.get("evaluation_id", "")) for row in selection_input.evaluation_results
    )
    validation_reasons = _input_validation_reasons(selection_input)

    if validation_reasons:
        replay = build_policy_selection_replay_key(
            selection_input,
            versions,
            ordered_policy_ids=tuple(),
            selected_policy_ids=tuple(),
        )
        trace = PolicySelectionTrace(
            trace_id=f"selection_trace_{selection_input.selection_id}",
            input_evaluation_ids=input_eval_ids,
            eligible_policy_ids=tuple(),
            rejected_policy_ids=tuple(),
            ordered_policy_ids=tuple(),
            excluded_policy_ids=tuple(),
            selected_policy_ids=tuple(),
            composition_sequence=tuple(),
            precedence_steps=tuple(),
            exclusion_steps=tuple(),
            tie_break_steps=tuple(),
            rejection_reasons=validation_reasons,
            selection_status="invalid_input",
            snapshot_versions=versions,
            replay_key=replay.replay_key,
        )
        result = PolicySelectionResult(
            selection_id=selection_input.selection_id,
            reducer_run_id=selection_input.reducer_run_id,
            field_id=selection_input.field_id,
            state_type=selection_input.state_type,
            input_evaluation_ids=input_eval_ids,
            eligible_policy_ids=tuple(),
            rejected_policy_ids=tuple(),
            ordered_policy_ids=tuple(),
            excluded_policy_ids=tuple(),
            selected_policy_ids=tuple(),
            composition_sequence=tuple(),
            precedence_steps=tuple(),
            exclusion_steps=tuple(),
            tie_break_steps=tuple(),
            rejection_reasons=validation_reasons,
            selection_status="invalid_input",
            replay_key=replay.replay_key,
            evaluated_contract_versions=versions,
            selection_trace_ref=trace.trace_id,
        )
        return result, trace

    candidates, rejected_policy_ids, filter_reasons = filter_eligible_candidates(
        selection_input.evaluation_results,
        loaded["policy_registry"].get("policies", []),
        state_type=selection_input.state_type,
    )

    precedence_result, tie_steps = resolve_precedence(
        candidates,
        loaded["precedence_matrix"],
    )

    exclusion_result = resolve_mutual_exclusion(
        precedence_result.ordered_candidates,
        loaded["policy_registry"].get("policies", []),
        loaded["composition_contract"],
        loaded["conflict_policy"],
    )

    composition_candidate = resolve_composition_eligibility(
        exclusion_result.kept_candidates,
        loaded["composition_contract"],
        loaded["policy_registry"].get("policies", []),
    )

    rejection_reasons: List[str] = []
    rejection_reasons.extend(filter_reasons)
    rejection_reasons.extend(precedence_result.rejection_reasons)
    rejection_reasons.extend(exclusion_result.rejection_reasons)
    if composition_candidate.reason:
        rejection_reasons.append(composition_candidate.reason)

    selected_policy_ids: Tuple[str, ...] = tuple()
    selection_status = "no_eligible_candidate"

    if precedence_result.unresolved:
        selection_status = "unresolved_precedence"
    elif exclusion_result.unresolved:
        selection_status = "unresolved_exclusion"
    elif not exclusion_result.kept_candidates:
        fallback = [c for c in candidates if c.policy_id == "no_state_change"]
        if fallback:
            selected_policy_ids = ("no_state_change",)
            selection_status = "no_state_change"
        else:
            selection_status = "no_eligible_candidate"
    elif composition_candidate.eligible:
        selected_policy_ids = composition_candidate.composition_sequence
        selection_status = "selected_composition"
    else:
        selected_policy_ids = (exclusion_result.kept_candidates[0].policy_id,)
        if selected_policy_ids[0] == "no_state_change":
            selection_status = "no_state_change"
        else:
            selection_status = "selected_single"

    replay = build_policy_selection_replay_key(
        selection_input,
        versions,
        ordered_policy_ids=precedence_result.ordered_policy_ids,
        selected_policy_ids=selected_policy_ids,
    )

    trace = PolicySelectionTrace(
        trace_id=f"selection_trace_{selection_input.selection_id}",
        input_evaluation_ids=input_eval_ids,
        eligible_policy_ids=tuple(c.policy_id for c in candidates),
        rejected_policy_ids=rejected_policy_ids,
        ordered_policy_ids=precedence_result.ordered_policy_ids,
        excluded_policy_ids=tuple(
            dict.fromkeys(
                list(precedence_result.excluded_policy_ids)
                + list(exclusion_result.excluded_policy_ids)
            )
        ),
        selected_policy_ids=selected_policy_ids,
        composition_sequence=composition_candidate.composition_sequence,
        precedence_steps=precedence_result.precedence_steps,
        exclusion_steps=exclusion_result.exclusion_steps,
        tie_break_steps=tie_steps,
        rejection_reasons=tuple(dict.fromkeys(rejection_reasons)),
        selection_status=selection_status,
        snapshot_versions=versions,
        replay_key=replay.replay_key,
    )

    result = PolicySelectionResult(
        selection_id=selection_input.selection_id,
        reducer_run_id=selection_input.reducer_run_id,
        field_id=selection_input.field_id,
        state_type=selection_input.state_type,
        input_evaluation_ids=input_eval_ids,
        eligible_policy_ids=trace.eligible_policy_ids,
        rejected_policy_ids=trace.rejected_policy_ids,
        ordered_policy_ids=trace.ordered_policy_ids,
        excluded_policy_ids=trace.excluded_policy_ids,
        selected_policy_ids=trace.selected_policy_ids,
        composition_sequence=trace.composition_sequence,
        precedence_steps=trace.precedence_steps,
        exclusion_steps=trace.exclusion_steps,
        tie_break_steps=trace.tie_break_steps,
        rejection_reasons=trace.rejection_reasons,
        selection_status=trace.selection_status,
        replay_key=replay.replay_key,
        evaluated_contract_versions=versions,
        selection_trace_ref=trace.trace_id,
    )

    return result, trace


def result_to_dict(result: PolicySelectionResult) -> Dict[str, Any]:
    return {
        "selection_id": result.selection_id,
        "reducer_run_id": result.reducer_run_id,
        "field_id": result.field_id,
        "state_type": result.state_type,
        "input_evaluation_ids": list(result.input_evaluation_ids),
        "eligible_policy_ids": list(result.eligible_policy_ids),
        "rejected_policy_ids": list(result.rejected_policy_ids),
        "ordered_policy_ids": list(result.ordered_policy_ids),
        "excluded_policy_ids": list(result.excluded_policy_ids),
        "selected_policy_ids": list(result.selected_policy_ids),
        "composition_sequence": list(result.composition_sequence),
        "precedence_steps": list(result.precedence_steps),
        "exclusion_steps": list(result.exclusion_steps),
        "tie_break_steps": list(result.tie_break_steps),
        "rejection_reasons": list(result.rejection_reasons),
        "selection_status": result.selection_status,
        "replay_key": result.replay_key,
        "evaluated_contract_versions": dict(result.evaluated_contract_versions),
        "selection_trace_ref": result.selection_trace_ref,
        "policy_execution_executed": result.policy_execution_executed,
        "state_mutation_executed": result.state_mutation_executed,
        "fact_promotion_executed": result.fact_promotion_executed,
        "action_trigger_executed": result.action_trigger_executed,
        "runtime_execution": result.runtime_execution,
        "error_namespace": ERROR_NAMESPACE_V1,
    }
