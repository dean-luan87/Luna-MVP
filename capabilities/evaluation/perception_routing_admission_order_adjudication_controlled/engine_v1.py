"""Evaluation-only Route-B order adjudication.

No Gateway, FPO runtime, provider, model, or runtime admission engine is
called here.  The engine records the consequence of the existing Gateway
contract for the current candidate-only handoff.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Iterable, Tuple

from capabilities.midplatform.field_perception_orchestrator.integration.perception_routing_admission_compatibility_v1 import (
    PerceptionRoutingAdmissionCompatibilityCandidateV1,
)

from .fixtures_v1 import RuntimeAdmissionOrderCaseV1, build_runtime_admission_order_cases_v1


PHASE_ID = "Phase-Perception-Routing-To-Runtime-Admission-Controlled-Handoff-v1-001"
NEXT_OWNER = "Provider Governance / Model Manager"


def _snapshot(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _snapshot(item) for key, item in asdict(value).items()}
    if isinstance(value, tuple):
        return [_snapshot(item) for item in value]
    if isinstance(value, list):
        return [_snapshot(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _snapshot(item) for key, item in value.items()}
    return value


def _validate_candidates(value: object) -> Tuple[str, ...]:
    if not isinstance(value, tuple):
        return ("compatibility_candidates_must_be_tuple",)
    errors = []
    refs = []
    for candidate in value:
        if not isinstance(candidate, PerceptionRoutingAdmissionCompatibilityCandidateV1):
            errors.append("invalid_compatibility_candidate_type")
            continue
        refs.append(candidate.admission_compatibility_candidate_ref)
        required = (
            candidate.admission_compatibility_candidate_ref,
            candidate.source_perception_routing_candidate_ref,
            candidate.source_observation_demand_ref,
            candidate.source_capability_requirement_ref,
            candidate.source_capability_resolution_candidate_ref,
            candidate.capability_candidate_ref,
            candidate.capability_class_ref,
            candidate.observation_class,
            candidate.parent_cognitive_problem_ref,
            candidate.source_state_ref,
            candidate.trace_ref,
        )
        if not all(required):
            errors.append(
                f"compatibility_candidate_required_ref_missing:{candidate.admission_compatibility_candidate_ref}"
            )
        if not candidate.candidate_only or not candidate.read_only:
            errors.append(
                f"compatibility_candidate_not_read_only:{candidate.admission_compatibility_candidate_ref}"
            )
        if candidate.truth_declared or candidate.world_truth_declared:
            errors.append(
                f"compatibility_candidate_truth_declared:{candidate.admission_compatibility_candidate_ref}"
            )
        if any(
            (
                candidate.runtime_admission_requested,
                candidate.runtime_admission_executed,
                candidate.fpo_runtime_request,
                candidate.gateway_submission,
                candidate.provider_binding,
                candidate.model_binding,
                candidate.provider_invocation,
                candidate.model_invocation,
                candidate.capability_activation,
                candidate.capability_reservation,
                candidate.slot_reservation,
                candidate.resource_scheduling,
                candidate.observation_execution,
            )
        ):
            errors.append(
                f"compatibility_candidate_runtime_flag_set:{candidate.admission_compatibility_candidate_ref}"
            )
        if candidate.source_perception_routing_candidate_ref not in candidate.lineage_refs:
            errors.append(
                f"routing_lineage_missing:{candidate.admission_compatibility_candidate_ref}"
            )
        if candidate.source_observation_demand_ref not in candidate.lineage_refs:
            errors.append(
                f"demand_lineage_missing:{candidate.admission_compatibility_candidate_ref}"
            )
        if candidate.source_capability_resolution_candidate_ref not in candidate.lineage_refs:
            errors.append(
                f"resolution_lineage_missing:{candidate.admission_compatibility_candidate_ref}"
            )
    if len(set(refs)) != len(refs):
        errors.append("duplicate_compatibility_candidate_ref")
    return tuple(dict.fromkeys(errors))


def _decision(candidate: PerceptionRoutingAdmissionCompatibilityCandidateV1) -> dict[str, Any]:
    return {
        "compatibility_candidate_ref": candidate.admission_compatibility_candidate_ref,
        "source_perception_routing_candidate_ref": candidate.source_perception_routing_candidate_ref,
        "source_observation_demand_ref": candidate.source_observation_demand_ref,
        "source_capability_resolution_candidate_ref": candidate.source_capability_resolution_candidate_ref,
        "parent_cognitive_problem_ref": candidate.parent_cognitive_problem_ref,
        "decision": "PROVIDER_BINDING_PRECEDES_RUNTIME_ADMISSION",
        "next_required_owner": NEXT_OWNER,
        "runtime_admission_candidate_formed": False,
        "runtime_admission_admitted": False,
        "provider_binding": False,
        "model_binding": False,
        "gateway_submission": False,
        "observation_execution": False,
        "lineage_refs": list(candidate.lineage_refs),
        "provenance_refs": list(candidate.provenance_refs),
        "trace_ref": candidate.trace_ref,
    }


def evaluate_case(case: RuntimeAdmissionOrderCaseV1) -> dict[str, Any]:
    before = _snapshot(case.compatibility_candidates)
    errors = _validate_candidates(case.compatibility_candidates)
    if errors:
        status = "INVALID_INPUT"
        decisions: list[dict[str, Any]] = []
    elif not case.compatibility_candidates:
        status = "NO_RUNTIME_ADMISSION_CANDIDATE"
        decisions = []
    else:
        status = "PROVIDER_BINDING_PRECEDES_RUNTIME_ADMISSION"
        decisions = [_decision(candidate) for candidate in case.compatibility_candidates]
    after = _snapshot(case.compatibility_candidates)
    return {
        "case_id": case.case_id,
        "evaluation_marker": case.evaluation_marker,
        "expected_status": case.expected_status,
        "expected_candidate_count": case.expected_candidate_count,
        "formation_status": status,
        "compatibility_candidate_refs": [
            candidate.admission_compatibility_candidate_ref
            for candidate in case.compatibility_candidates
            if isinstance(candidate, PerceptionRoutingAdmissionCompatibilityCandidateV1)
        ],
        "decisions": decisions,
        "compatibility_candidates_snapshot_before": before,
        "compatibility_candidates_snapshot_after": after,
        "validation_errors": list(errors),
        "admission_contract_requires_provider": True,
        "admission_contract_requires_model": False,
        "admission_contract_requires_runtime_observation": True,
        "admission_contract_requires_execution_instance": True,
        "runtime_admission_execution": False,
        "gateway_submission": False,
        "fpo_runtime_invocation": False,
        "provider_binding": False,
        "model_binding": False,
        "provider_invocation": False,
        "model_invocation": False,
        "observation_execution": False,
        "capability_activation": False,
        "slot_reservation": False,
        "resource_scheduling": False,
        "decision_formed": False,
        "task_formed": False,
        "action_formed": False,
        "truth_declared": False,
        "world_truth_declared": False,
        "replay_formation_status": status,
        "replay_decision_refs": [
            item["compatibility_candidate_ref"] for item in decisions
        ],
    }


def build_runtime_admission_order_summary_v1() -> dict[str, Any]:
    cases = [evaluate_case(case) for case in build_runtime_admission_order_cases_v1()]
    return {
        "phase": PHASE_ID,
        "route": "ROUTE_B_ARCHITECTURE_ORDER_ADJUDICATION",
        "status": "ARCHITECTURE_ORDER_ADJUDICATED",
        "synthetic_only": True,
        "controlled_only": True,
        "candidate_only": True,
        "canonical_runtime_admission_owner": "Observation Gateway Governance",
        "compatibility_owner": "Field Perception Orchestrator / Active Observation Control",
        "standalone_runtime_admission_owner_created": False,
        "controlled_pure_runtime_admission_path_exists": False,
        "provider_binding_precedes_runtime_admission": True,
        "model_binding_precedes_runtime_admission": False,
        "runtime_admission_requires_provider": True,
        "runtime_admission_requires_model": False,
        "runtime_admission_requires_runtime_observation": True,
        "runtime_admission_requires_execution_instance": True,
        "runtime_admission_execution": False,
        "gateway_submission": False,
        "fpo_runtime_invocation": False,
        "provider_binding": False,
        "model_binding": False,
        "provider_invocation": False,
        "model_invocation": False,
        "observation_execution": False,
        "capability_activation": False,
        "slot_reservation": False,
        "resource_scheduling": False,
        "evidence_ingress": False,
        "evidence_fusion": False,
        "decision_formed": False,
        "task_formed": False,
        "action_formed": False,
        "current_world_mutation": False,
        "field_mutation": False,
        "memory_pcn_mutation": False,
        "truth_declared": False,
        "world_truth_declared": False,
        "cases": cases,
    }


__all__ = ["build_runtime_admission_order_summary_v1", "evaluate_case"]

