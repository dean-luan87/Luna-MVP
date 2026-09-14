"""Synthetic, candidate-only fixtures for the FPO compatibility seam."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Tuple

from capabilities.midplatform.core.observation_gateway.perception_routing_candidate_v1 import (
    PerceptionRoutingCandidateV1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.perception_routing_admission_compatibility_v1 import (
    PerceptionRoutingAdmissionCompatibilityInputV1,
)


PROBLEM = "problem:controlled:perception-admission-compatibility"
STATE = "state:controlled:perception-admission-compatibility"
CONTEXT = ("context:controlled:perception-admission-compatibility",)
TARGET_A = ("target:controlled:directional-information",)
TARGET_B = ("target:controlled:environmental-cue",)
CLASS_A = "capability-class:controlled:visual-information"
CLASS_B = "capability-class:controlled:environmental-information"


@dataclass(frozen=True)
class PerceptionRoutingAdmissionCompatibilityCaseV1:
    case_id: str
    request: PerceptionRoutingAdmissionCompatibilityInputV1
    expected_status: str
    expected_candidate_count: int
    evaluation_marker: str


def _route(
    route_ref: str,
    demand_ref: str,
    resolution_ref: str,
    capability_ref: str,
    capability_class_ref: str = CLASS_A,
    target_refs: Tuple[str, ...] = TARGET_A,
) -> PerceptionRoutingCandidateV1:
    return PerceptionRoutingCandidateV1(
        perception_routing_candidate_ref=route_ref,
        source_observation_demand_ref=demand_ref,
        source_capability_requirement_ref=f"requirement:{demand_ref}",
        source_capability_resolution_candidate_ref=resolution_ref,
        capability_candidate_ref=capability_ref,
        capability_class_ref=capability_class_ref,
        slot_ref="",
        observation_class="PERCEPTION",
        observation_target_refs=target_refs,
        observation_constraint_refs=(),
        expected_information_contribution_refs=(f"contribution:{demand_ref}",),
        information_need_refs=(f"need:{demand_ref}",),
        information_gap_refs=(f"gap:{demand_ref}",),
        source_strategy_ref=f"strategy:{demand_ref}",
        source_branch_ref=f"branch:{demand_ref}",
        parent_cognitive_problem_ref=PROBLEM,
        routing_basis_refs=("governed:resolution-to-perception-routing",),
        context_refs=CONTEXT,
        lineage_refs=(
            PROBLEM,
            f"need:{demand_ref}",
            f"gap:{demand_ref}",
            f"branch:{demand_ref}",
            f"strategy:{demand_ref}",
            demand_ref,
            f"requirement:{demand_ref}",
            capability_ref,
            resolution_ref,
            route_ref,
        ),
        provenance_refs=(f"provenance:{route_ref}",),
        trace_ref=f"trace:{route_ref}",
    )


ROUTE_A = _route(
    "perception-routing:controlled:a",
    "demand:controlled:a",
    "resolution:controlled:a",
    "capability:controlled:a",
)
ROUTE_B = _route(
    "perception-routing:controlled:b",
    "demand:controlled:b",
    "resolution:controlled:b",
    "capability:controlled:b",
    CLASS_B,
    TARGET_B,
)
SAME_CLASS_ROUTE_B = _route(
    "perception-routing:controlled:same-class:b",
    "demand:controlled:a",
    "resolution:controlled:same-class:b",
    "capability:controlled:same-class:b",
)
SHARED_CAPABILITY_ROUTE_B = _route(
    "perception-routing:controlled:shared:b",
    "demand:controlled:b",
    "resolution:controlled:shared:b",
    "capability:controlled:a",
    CLASS_B,
    TARGET_B,
)
SCENARIO12_SIGNAGE = _route(
    "perception-routing:scenario12:signage",
    "demand:scenario12:signage",
    "resolution:scenario12:signage",
    "capability:scenario12:signage-information",
    "capability-class:controlled:scenario12:signage-information",
)
SCENARIO12_FLOW = _route(
    "perception-routing:scenario12:flow",
    "demand:scenario12:flow",
    "resolution:scenario12:flow",
    "capability:scenario12:flow-information",
    "capability-class:controlled:scenario12:flow-information",
    TARGET_B,
)


def _request(ref: str, routes: Any) -> PerceptionRoutingAdmissionCompatibilityInputV1:
    return PerceptionRoutingAdmissionCompatibilityInputV1(
        compatibility_ref=ref,
        parent_cognitive_problem_ref=PROBLEM,
        source_state_ref=STATE,
        routing_candidates=routes,
        context_refs=CONTEXT,
        trace_ref=f"trace:{ref}",
        provenance_refs=(f"provenance:{ref}",),
    )


def build_perception_routing_admission_compatibility_cases_v1() -> Tuple[
    PerceptionRoutingAdmissionCompatibilityCaseV1, ...
]:
    cases = (
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "SINGLE_ROUTING_CANDIDATE_COMPATIBLE", _request("compatibility:single", (ROUTE_A,)),
            "ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 1, "single_route_single_candidate",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "MULTIPLE_ROUTING_CANDIDATES", _request("compatibility:multiple", (ROUTE_A, ROUTE_B)),
            "ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 2, "multiple_routes_no_winner",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "SAME_CLASS_MULTIPLE_ROUTES", _request("compatibility:same-class", (ROUTE_A, SAME_CLASS_ROUTE_B)),
            "ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 2, "same_class_not_deduplicated",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "SAME_CAPABILITY_MULTIPLE_DEMANDS", _request("compatibility:shared-capability", (ROUTE_A, SHARED_CAPABILITY_ROUTE_B)),
            "ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 2, "same_capability_multiple_demands_not_merged",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "NO_ROUTING_CANDIDATE", _request("compatibility:none", ()),
            "NO_ADMISSION_COMPATIBILITY_CANDIDATE", 0, "zero_route_zero_candidate",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "INVALID_ROUTING_CANDIDATE", _request("compatibility:invalid", (replace(ROUTE_A, candidate_only=False),)),
            "INVALID_INPUT", 0, "invalid_route_fails_closed",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "LINEAGE_MISMATCH", _request("compatibility:lineage-mismatch", (replace(ROUTE_A, source_observation_demand_ref="demand:controlled:other"),)),
            "INVALID_INPUT", 0, "lineage_mismatch_fails_closed",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "MISSING_REQUIRED_TARGET_FIELD", _request("compatibility:missing-target", (replace(ROUTE_A, observation_target_refs=()),)),
            "ADMISSION_COMPATIBILITY_GAP", 0, "missing_target_fails_closed",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "HISTORICAL_REQUEST_REQUIRES_PROVIDER_FIELD", _request("compatibility:historical-provider", (ROUTE_A,)),
            "ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 1, "provider_not_fabricated",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "HISTORICAL_REQUEST_REQUIRES_MODEL_FIELD", _request("compatibility:historical-model", (ROUTE_A,)),
            "ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 1, "model_not_fabricated",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "CAPABILITY_ADMITTED_BUT_RUNTIME_NOT_AUTO_ADMITTED", _request("compatibility:no-auto-runtime-admission", (ROUTE_A,)),
            "ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 1, "capability_admission_not_runtime_admission",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "SCENARIO12_SIGNAGE", _request("compatibility:scenario12-signage", (SCENARIO12_SIGNAGE,)),
            "ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 1, "scenario12_signage_no_ocr_inference",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "SCENARIO12_HUMAN_FLOW", _request("compatibility:scenario12-flow", (SCENARIO12_FLOW,)),
            "ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 1, "scenario12_flow_no_model_inference",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "SCENARIO12_BOTH", _request("compatibility:scenario12-both", (SCENARIO12_SIGNAGE, SCENARIO12_FLOW)),
            "ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 2, "scenario12_two_candidates",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "DETERMINISTIC_REPLAY", _request("compatibility:deterministic", (ROUTE_A, ROUTE_B)),
            "ADMISSION_COMPATIBILITY_CANDIDATE_FORMED", 2, "deterministic_replay",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "MALFORMED_INPUT_SHAPE", _request("compatibility:malformed", ROUTE_A),
            "INVALID_INPUT", 0, "malformed_input_fails_closed",
        ),
        PerceptionRoutingAdmissionCompatibilityCaseV1(
            "UNSUPPORTED_OBSERVATION_CLASS", _request("compatibility:unsupported-class", (replace(ROUTE_A, observation_class="UNSUPPORTED"),)),
            "ADMISSION_COMPATIBILITY_GAP", 0, "unsupported_observation_class_fails_closed",
        ),
    )
    return cases


__all__ = [
    "PerceptionRoutingAdmissionCompatibilityCaseV1",
    "build_perception_routing_admission_compatibility_cases_v1",
]
