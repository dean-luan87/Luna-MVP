from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from ..field_state_reducer_behavior_policy_error_types_v1 import ERROR_NAMESPACE_V1
from ..field_state_reducer_behavior_policy_registry_skeleton_v1 import policy_ids_v1
from ..field_state_reducer_behavior_policy_static_validators_v1 import (
    validate_state_type_known,
)
from .policy_evaluation_condition_evaluator_v1 import evaluate_conditions
from .policy_evaluation_confidence_evaluator_v1 import evaluate_confidence
from .policy_evaluation_conflict_evaluator_v1 import evaluate_conflict
from .policy_evaluation_contract_loader_v1 import load_policy_evaluation_contracts_v1
from .policy_evaluation_evidence_evaluator_v1 import evaluate_evidence_sufficiency
from .policy_evaluation_governance_evaluator_v1 import evaluate_governance
from .policy_evaluation_replay_v1 import build_evaluation_replay_key
from .policy_evaluation_rule_loader_v1 import build_condition_rules_for_policy
from .policy_evaluation_temporal_evaluator_v1 import evaluate_temporal
from .policy_evaluation_types_v1 import (
    EvaluationInput,
    EvaluationTrace,
    PolicyEvaluationResult,
)


def _build_snapshot_versions(contracts: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
    return {
        "policy_registry_version": "v1",
        "eligibility_matrix_version": "v1",
        "evaluation_matrix_version": str(
            contracts["evaluation_matrix"].get("version", "v1")
        ),
        "condition_registry_version": str(
            contracts["condition_registry"].get("version", "v1")
        ),
        "operator_registry_version": str(
            contracts["operator_registry"].get("version", "v1")
        ),
        "evidence_contract_version": str(
            contracts["evidence_contract"].get("version", "v1")
        ),
        "temporal_contract_version": str(
            contracts["temporal_contract"].get("version", "v1")
        ),
        "confidence_contract_version": str(
            contracts["confidence_contract"].get("version", "v1")
        ),
        "conflict_contract_version": str(
            contracts["conflict_contract"].get("version", "v1")
        ),
        "governance_contract_version": str(
            contracts["governance_contract"].get("version", "v1")
        ),
        "evaluation_contract_version": evaluation_contract_version_or_default(
            contracts
        ),
    }


def evaluation_contract_version_or_default(contracts: Dict[str, Dict[str, Any]]) -> str:
    return str(contracts["result_schema"].get("version", "v1"))


def _status_from_pipeline(
    condition_blocked: bool,
    evidence_status: str,
    temporal_status: str,
    confidence_passed: bool,
    conflict_status: str,
    governance_passed: bool,
) -> str:
    if evidence_status in {
        "insufficient",
        "missing_required_source",
        "missing_provenance",
        "stale_evidence",
        "contradictory",
    }:
        return "insufficient_evidence"
    if temporal_status == "temporally_invalid":
        return "temporally_invalid"
    if not confidence_passed:
        return "ineligible"
    if conflict_status in {
        "unresolved_conflict",
        "blocked",
        "governance_review_required",
    }:
        return conflict_status
    if not governance_passed:
        return "governance_review_required"
    if condition_blocked:
        return "blocked"
    return "eligible_candidate"


def _boundary_reasons(evaluation_input: EvaluationInput) -> Tuple[str, ...]:
    reasons: List[str] = []
    if evaluation_input.runtime_state_dependency_requested:
        reasons.append("runtime_dependency_requested")
    if evaluation_input.provider_recall_requested:
        reasons.append("external_dependency_requested")
    if evaluation_input.external_lookup_requested:
        reasons.append("external_dependency_requested")
    if evaluation_input.model_call_requested:
        reasons.append("external_dependency_requested")
    if evaluation_input.state_write_requested:
        reasons.append("runtime_dependency_requested")
    if evaluation_input.action_trigger_requested:
        reasons.append("runtime_dependency_requested")
    return tuple(dict.fromkeys(reasons))


def evaluate_single_policy_v1(
    evaluation_input: EvaluationInput,
    contracts: Dict[str, Dict[str, Any]] | None = None,
) -> PolicyEvaluationResult:
    loaded = (
        contracts if contracts is not None else load_policy_evaluation_contracts_v1()
    )

    matrix_rows = list(loaded["evaluation_matrix"].get("policies", []))
    matrix_by_policy = {str(row.get("policy_id", "")): row for row in matrix_rows}

    policy_id = evaluation_input.policy_id
    status_from_known_state, _ = validate_state_type_known(evaluation_input.state_type)

    missing_input_fields: List[str] = []
    if not evaluation_input.policy_registry_version:
        missing_input_fields.append("policy_registry_version")
    if not evaluation_input.eligibility_matrix_version:
        missing_input_fields.append("eligibility_matrix_version")
    if not evaluation_input.evaluation_contract_version:
        missing_input_fields.append("evaluation_contract_version")

    base_rejection_reasons: List[str] = list(_boundary_reasons(evaluation_input))
    if policy_id not in set(policy_ids_v1()) or policy_id not in matrix_by_policy:
        base_rejection_reasons.append("unknown_policy")
    if not status_from_known_state:
        base_rejection_reasons.append("unknown_state_type")
    if missing_input_fields:
        base_rejection_reasons.append("missing_version_snapshot")

    if base_rejection_reasons:
        snapshot_versions = _build_snapshot_versions(loaded)
        replay = build_evaluation_replay_key(evaluation_input, snapshot_versions)
        trace = EvaluationTrace(
            trace_id=f"trace_{evaluation_input.evaluation_id}",
            evaluation_id=evaluation_input.evaluation_id,
            policy_id=evaluation_input.policy_id,
            ordered_rule_ids=tuple(),
            evaluated_rule_ids=tuple(),
            rule_results=tuple(),
            short_circuit_steps=("invalid_input_guard",),
            evidence_refs=tuple(),
            temporal_refs=tuple(),
            confidence_refs=tuple(),
            conflict_refs=tuple(),
            governance_refs=tuple(),
            rejection_reason_refs=tuple(dict.fromkeys(base_rejection_reasons)),
            snapshot_versions=snapshot_versions,
            replay_key=replay.replay_key,
            created_at=datetime.now(timezone.utc).isoformat(),
            base_trace=None,
        )
        return PolicyEvaluationResult(
            evaluation_id=evaluation_input.evaluation_id,
            policy_id=evaluation_input.policy_id,
            state_type=evaluation_input.state_type,
            evaluation_status="invalid_input",
            satisfied_rule_ids=tuple(),
            unsatisfied_rule_ids=tuple(),
            blocked_rule_ids=tuple(),
            skipped_rule_ids=tuple(),
            missing_input_fields=tuple(missing_input_fields),
            evidence_sufficiency_status="insufficient",
            temporal_evaluation_status="temporally_invalid",
            confidence_evaluation_status="ineligible",
            conflict_evaluation_status="unresolved_conflict",
            governance_evaluation_status="governance_review_required",
            rejection_reasons=tuple(dict.fromkeys(base_rejection_reasons)),
            selection_candidate_allowed=False,
            evaluation_trace_ref=trace.trace_id,
            replay_key=replay.replay_key,
            evaluated_contract_versions=snapshot_versions,
        )

    policy_row = matrix_by_policy[policy_id]
    rules = build_condition_rules_for_policy(
        policy_id, tuple(policy_row.get("evaluation_rules", []))
    )
    condition_results = evaluate_conditions(rules, evaluation_input)

    satisfied_rule_ids = tuple(r.rule_id for r in condition_results if r.passed)
    unsatisfied_rule_ids = tuple(
        r.rule_id for r in condition_results if not r.passed and not r.blocking
    )
    blocked_rule_ids = tuple(
        r.rule_id for r in condition_results if not r.passed and r.blocking
    )

    evidence = evaluate_evidence_sufficiency(
        evaluation_input, loaded["evidence_contract"]
    )
    temporal = evaluate_temporal(evaluation_input, loaded["temporal_contract"])
    confidence = evaluate_confidence(evaluation_input, loaded["confidence_contract"])
    conflict = evaluate_conflict(evaluation_input, loaded["conflict_contract"])
    governance = evaluate_governance(evaluation_input, loaded["governance_contract"])

    rejection_reasons: List[str] = []
    rejection_reasons.extend(
        [r.rejection_reason for r in condition_results if r.rejection_reason]
    )
    rejection_reasons.extend(evidence.rejection_reasons)
    if temporal.rejection_reason:
        rejection_reasons.append(temporal.rejection_reason)
    if confidence.rejection_reason:
        rejection_reasons.append(confidence.rejection_reason)
    if conflict.rejection_reason:
        rejection_reasons.append(conflict.rejection_reason)
    if not governance.passed:
        rejection_reasons.append("owner_review_required")

    final_status = _status_from_pipeline(
        condition_blocked=len(blocked_rule_ids) > 0,
        evidence_status=evidence.status,
        temporal_status=temporal.status,
        confidence_passed=confidence.passed,
        conflict_status=conflict.status,
        governance_passed=governance.passed,
    )

    selection_candidate_allowed = final_status == "eligible_candidate"
    snapshot_versions = _build_snapshot_versions(loaded)
    replay = build_evaluation_replay_key(evaluation_input, snapshot_versions)

    trace = EvaluationTrace(
        trace_id=f"trace_{evaluation_input.evaluation_id}",
        evaluation_id=evaluation_input.evaluation_id,
        policy_id=evaluation_input.policy_id,
        ordered_rule_ids=tuple(
            rule.rule_id for rule in sorted(rules, key=lambda x: x.evaluation_order)
        ),
        evaluated_rule_ids=tuple(r.rule_id for r in condition_results),
        rule_results=tuple(
            {
                "rule_id": r.rule_id,
                "passed": r.passed,
                "blocking": r.blocking,
                "missing_inputs": r.missing_inputs,
                "rejection_reason": r.rejection_reason,
            }
            for r in condition_results
        ),
        short_circuit_steps=tuple(),
        evidence_refs=(f"evidence:{evidence.status}",),
        temporal_refs=(f"temporal:{temporal.status}",),
        confidence_refs=(f"confidence:{confidence.status}",),
        conflict_refs=(f"conflict:{conflict.status}",),
        governance_refs=(f"governance:{governance.status}",),
        rejection_reason_refs=tuple(dict.fromkeys(rejection_reasons)),
        snapshot_versions=snapshot_versions,
        replay_key=replay.replay_key,
        created_at=datetime.now(timezone.utc).isoformat(),
        base_trace=None,
    )

    return PolicyEvaluationResult(
        evaluation_id=evaluation_input.evaluation_id,
        policy_id=evaluation_input.policy_id,
        state_type=evaluation_input.state_type,
        evaluation_status=final_status,
        satisfied_rule_ids=satisfied_rule_ids,
        unsatisfied_rule_ids=unsatisfied_rule_ids,
        blocked_rule_ids=blocked_rule_ids,
        skipped_rule_ids=tuple(),
        missing_input_fields=tuple(
            dict.fromkeys(list(missing_input_fields) + list(evidence.missing_inputs))
        ),
        evidence_sufficiency_status=evidence.status,
        temporal_evaluation_status=temporal.status,
        confidence_evaluation_status=confidence.status,
        conflict_evaluation_status=conflict.status,
        governance_evaluation_status=governance.status,
        rejection_reasons=tuple(dict.fromkeys(rejection_reasons)),
        selection_candidate_allowed=selection_candidate_allowed,
        evaluation_trace_ref=trace.trace_id,
        replay_key=replay.replay_key,
        evaluated_contract_versions=snapshot_versions,
    )


def result_to_dict(result: PolicyEvaluationResult) -> Dict[str, Any]:
    return {
        "evaluation_id": result.evaluation_id,
        "policy_id": result.policy_id,
        "state_type": result.state_type,
        "evaluation_status": result.evaluation_status,
        "satisfied_rule_ids": list(result.satisfied_rule_ids),
        "unsatisfied_rule_ids": list(result.unsatisfied_rule_ids),
        "blocked_rule_ids": list(result.blocked_rule_ids),
        "skipped_rule_ids": list(result.skipped_rule_ids),
        "missing_input_fields": list(result.missing_input_fields),
        "evidence_sufficiency_status": result.evidence_sufficiency_status,
        "temporal_evaluation_status": result.temporal_evaluation_status,
        "confidence_evaluation_status": result.confidence_evaluation_status,
        "conflict_evaluation_status": result.conflict_evaluation_status,
        "governance_evaluation_status": result.governance_evaluation_status,
        "rejection_reasons": list(result.rejection_reasons),
        "selection_candidate_allowed": result.selection_candidate_allowed,
        "evaluation_trace_ref": result.evaluation_trace_ref,
        "replay_key": result.replay_key,
        "evaluated_contract_versions": dict(result.evaluated_contract_versions),
        "policy_selection_executed": result.policy_selection_executed,
        "policy_execution_executed": result.policy_execution_executed,
        "state_mutation_executed": result.state_mutation_executed,
        "fact_promotion_executed": result.fact_promotion_executed,
        "action_trigger_executed": result.action_trigger_executed,
        "runtime_execution": result.runtime_execution,
        "error_namespace": ERROR_NAMESPACE_V1,
    }
