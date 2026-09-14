"""Synthetic inputs for runtime-admission order adjudication.

This package does not construct or execute Gateway runtime admission.  It
records the order decision that follows from the existing Gateway contract.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

from capabilities.midplatform.field_perception_orchestrator.integration.perception_routing_admission_compatibility_v1 import (
    PerceptionRoutingAdmissionCompatibilityCandidateV1,
)


PROBLEM = "problem:controlled:runtime-admission-order"
STATE = "state:controlled:runtime-admission-order"
CONTEXT = ("context:controlled:runtime-admission-order",)


@dataclass(frozen=True)
class RuntimeAdmissionOrderCaseV1:
    case_id: str
    compatibility_candidates: Tuple[
        PerceptionRoutingAdmissionCompatibilityCandidateV1, ...
    ]
    expected_status: str
    expected_candidate_count: int
    evaluation_marker: str


def _candidate(
    candidate_ref: str,
    route_ref: str,
    demand_ref: str,
    capability_ref: str,
    capability_class_ref: str,
) -> PerceptionRoutingAdmissionCompatibilityCandidateV1:
    requirement_ref = f"requirement:{demand_ref}"
    resolution_ref = f"resolution:{demand_ref}"
    need_ref = f"need:{demand_ref}"
    gap_ref = f"gap:{demand_ref}"
    strategy_ref = f"strategy:{demand_ref}"
    branch_ref = f"branch:{demand_ref}"
    return PerceptionRoutingAdmissionCompatibilityCandidateV1(
        admission_compatibility_candidate_ref=candidate_ref,
        source_perception_routing_candidate_ref=route_ref,
        source_observation_demand_ref=demand_ref,
        source_capability_requirement_ref=requirement_ref,
        source_capability_resolution_candidate_ref=resolution_ref,
        capability_candidate_ref=capability_ref,
        capability_class_ref=capability_class_ref,
        slot_ref="",
        observation_class="PERCEPTION",
        observation_target_refs=(f"target:{demand_ref}",),
        observation_constraint_refs=(),
        expected_information_contribution_refs=(f"contribution:{demand_ref}",),
        information_need_refs=(need_ref,),
        information_gap_refs=(gap_ref,),
        source_strategy_ref=strategy_ref,
        source_branch_ref=branch_ref,
        parent_cognitive_problem_ref=PROBLEM,
        source_state_ref=STATE,
        context_refs=CONTEXT,
        admission_compatibility_basis_refs=(
            "governed:runtime-admission-order-review",
        ),
        lineage_refs=(
            PROBLEM,
            need_ref,
            gap_ref,
            branch_ref,
            strategy_ref,
            demand_ref,
            requirement_ref,
            resolution_ref,
            capability_ref,
            route_ref,
            candidate_ref,
        ),
        provenance_refs=(f"provenance:{candidate_ref}",),
        trace_ref=f"trace:{candidate_ref}",
    )


COMPAT_A = _candidate(
    "fpo-admission-compatibility:controlled:a",
    "perception-routing:controlled:a",
    "demand:controlled:a",
    "capability:controlled:a",
    "capability-class:controlled:visual-information",
)
COMPAT_B = _candidate(
    "fpo-admission-compatibility:controlled:b",
    "perception-routing:controlled:b",
    "demand:controlled:b",
    "capability:controlled:b",
    "capability-class:controlled:environmental-information",
)
SCENARIO12_SIGNAGE = _candidate(
    "fpo-admission-compatibility:scenario12:signage",
    "perception-routing:scenario12:signage",
    "demand:scenario12:signage",
    "capability:scenario12:signage-information",
    "capability-class:controlled:scenario12:signage-information",
)
SCENARIO12_FLOW = _candidate(
    "fpo-admission-compatibility:scenario12:flow",
    "perception-routing:scenario12:flow",
    "demand:scenario12:flow",
    "capability:scenario12:flow-information",
    "capability-class:controlled:scenario12:flow-information",
)


def build_runtime_admission_order_cases_v1() -> Tuple[
    RuntimeAdmissionOrderCaseV1, ...
]:
    return (
        RuntimeAdmissionOrderCaseV1(
            "ADMISSION_CONTRACT_REQUIRES_PROVIDER",
            (COMPAT_A,),
            "PROVIDER_BINDING_PRECEDES_RUNTIME_ADMISSION",
            1,
            "admission_contract_requires_provider",
        ),
        RuntimeAdmissionOrderCaseV1(
            "ADMISSION_CONTRACT_REQUIRES_RUNTIME_TARGET",
            (COMPAT_A,),
            "PROVIDER_BINDING_PRECEDES_RUNTIME_ADMISSION",
            1,
            "admission_contract_requires_runtime_target",
        ),
        RuntimeAdmissionOrderCaseV1(
            "MODEL_METADATA_NOT_REQUIRED_BY_GATEWAY_PROOF",
            (COMPAT_A,),
            "PROVIDER_BINDING_PRECEDES_RUNTIME_ADMISSION",
            1,
            "model_not_fabricated",
        ),
        RuntimeAdmissionOrderCaseV1(
            "COMPATIBILITY_CANDIDATE_LACKS_PROVIDER",
            (COMPAT_A,),
            "PROVIDER_BINDING_PRECEDES_RUNTIME_ADMISSION",
            1,
            "provider_missing_no_fabrication",
        ),
        RuntimeAdmissionOrderCaseV1(
            "COMPATIBILITY_CANDIDATE_LACKS_MODEL",
            (COMPAT_A,),
            "PROVIDER_BINDING_PRECEDES_RUNTIME_ADMISSION",
            1,
            "model_missing_no_fabrication",
        ),
        RuntimeAdmissionOrderCaseV1(
            "NO_FABRICATION",
            (COMPAT_A,),
            "PROVIDER_BINDING_PRECEDES_RUNTIME_ADMISSION",
            1,
            "no_provider_or_model_fabrication",
        ),
        RuntimeAdmissionOrderCaseV1(
            "CURRENT_ORDER_BLOCKED",
            (COMPAT_A,),
            "PROVIDER_BINDING_PRECEDES_RUNTIME_ADMISSION",
            1,
            "current_order_blocked",
        ),
        RuntimeAdmissionOrderCaseV1(
            "NO_COMPATIBILITY_CANDIDATE",
            (),
            "NO_RUNTIME_ADMISSION_CANDIDATE",
            0,
            "zero_input",
        ),
        RuntimeAdmissionOrderCaseV1(
            "INVALID_COMPATIBILITY_CANDIDATE",
            (replace(COMPAT_A, candidate_only=False),),
            "INVALID_INPUT",
            0,
            "invalid_candidate_fails_closed",
        ),
        RuntimeAdmissionOrderCaseV1(
            "SCENARIO12_SIGNAGE",
            (SCENARIO12_SIGNAGE,),
            "PROVIDER_BINDING_PRECEDES_RUNTIME_ADMISSION",
            1,
            "scenario12_signage_abstract",
        ),
        RuntimeAdmissionOrderCaseV1(
            "SCENARIO12_HUMAN_FLOW",
            (SCENARIO12_FLOW,),
            "PROVIDER_BINDING_PRECEDES_RUNTIME_ADMISSION",
            1,
            "scenario12_human_flow_abstract",
        ),
        RuntimeAdmissionOrderCaseV1(
            "SCENARIO12_BOTH",
            (SCENARIO12_SIGNAGE, SCENARIO12_FLOW),
            "PROVIDER_BINDING_PRECEDES_RUNTIME_ADMISSION",
            2,
            "scenario12_two_lineages",
        ),
        RuntimeAdmissionOrderCaseV1(
            "DETERMINISTIC_REPLAY",
            (COMPAT_A, COMPAT_B),
            "PROVIDER_BINDING_PRECEDES_RUNTIME_ADMISSION",
            2,
            "deterministic_replay",
        ),
        RuntimeAdmissionOrderCaseV1(
            "MALFORMED_INPUT_SHAPE",
            ("not-a-compatibility-candidate",),  # type: ignore[arg-type]
            "INVALID_INPUT",
            0,
            "malformed_input_fails_closed",
        ),
    )


__all__ = [
    "RuntimeAdmissionOrderCaseV1",
    "build_runtime_admission_order_cases_v1",
]

