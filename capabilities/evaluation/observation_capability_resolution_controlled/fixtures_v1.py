"""Synthetic fixtures for controlled Observation Demand capability resolution."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

from capabilities.midplatform.core.cognitive_flow.observation_demand_formation_v1 import (
    ObservationDemandCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.observation_demand_capability_resolution_v1 import (
    GovernedCapabilityInventoryEntryV1,
    GovernedObservationCapabilityRequirementMappingV1,
    ObservationDemandCapabilityResolutionInputV1,
)


SOURCE_MODE = "CONTROLLED_OBSERVATION_CAPABILITY_RESOLUTION_TEST"
PARENT_PROBLEM_REF = "problem:controlled:observation-capability:v1"
SOURCE_STATE_REF = "state:controlled:observation-capability:v1"
NEED_REF_A = "need:controlled:observation-capability:a:v1"
NEED_REF_B = "need:controlled:observation-capability:b:v1"
GAP_REF_A = "gap:controlled:observation-capability:a:v1"
GAP_REF_B = "gap:controlled:observation-capability:b:v1"


@dataclass(frozen=True)
class ObservationCapabilityResolutionCaseV1:
    case_id: str
    request: ObservationDemandCapabilityResolutionInputV1
    expected_status: str
    expected_candidate_count: int
    evaluation_marker: str = ""


def _demand(
    demand_ref: str,
    strategy_ref: str,
    branch_ref: str,
    *,
    need_ref: str = NEED_REF_A,
    gap_ref: str = GAP_REF_A,
    candidate_only: bool = True,
) -> ObservationDemandCandidateV1:
    return ObservationDemandCandidateV1(
        observation_demand_ref=demand_ref,
        parent_cognitive_problem_ref=PARENT_PROBLEM_REF,
        source_state_ref=SOURCE_STATE_REF,
        source_strategy_ref=strategy_ref,
        source_coordination_decision_ref=f"coordination-decision:{strategy_ref}",
        source_branch_ref=branch_ref,
        information_need_refs=(need_ref,),
        information_gap_refs=(gap_ref,),
        acquisition_basis_refs=(f"basis:{strategy_ref}",),
        expected_information_contribution_refs=(f"contribution:{strategy_ref}",),
        observation_class="PERCEPTION",
        observation_target_refs=(f"target:{strategy_ref}",),
        observation_constraint_refs=(),
        context_refs=("context:controlled:observation-capability:v1",),
        lineage_refs=(
            "problem:controlled:observation-capability:v1",
            need_ref,
            gap_ref,
            branch_ref,
            strategy_ref,
            demand_ref,
        ),
        provenance_refs=(f"provenance:{demand_ref}",),
        trace_ref=f"trace:{demand_ref}",
        candidate_only=candidate_only,
    )


def _mapping(
    demand: ObservationDemandCandidateV1,
    capability_class_ref: str,
    *,
    capability_class_refs: Tuple[str, ...] | None = None,
) -> GovernedObservationCapabilityRequirementMappingV1:
    return GovernedObservationCapabilityRequirementMappingV1(
        mapping_ref=f"mapping:{demand.observation_demand_ref}",
        observation_demand_ref=demand.observation_demand_ref,
        required_capability_class_refs=(capability_class_refs or (capability_class_ref,)),
        mapping_basis_refs=(f"basis:capability-mapping:{capability_class_ref}",),
        provenance_refs=(f"provenance:capability-mapping:{demand.observation_demand_ref}",),
        trace_ref=f"trace:capability-mapping:{demand.observation_demand_ref}",
    )


def _inventory(
    candidate_ref: str,
    capability_class_ref: str,
    *,
    availability_status: str = "AVAILABLE",
    admission_status: str = "ADMITTED",
    eligible: bool = True,
) -> GovernedCapabilityInventoryEntryV1:
    return GovernedCapabilityInventoryEntryV1(
        capability_candidate_ref=candidate_ref,
        capability_class_ref=capability_class_ref,
        availability_status=availability_status,
        admission_status=admission_status,
        eligible=eligible,
        slot_ref=f"slot:{candidate_ref}",
        provenance_refs=(f"provenance:inventory:{candidate_ref}",),
        trace_ref=f"trace:inventory:{candidate_ref}",
    )


def _request(
    resolution_ref: str,
    demands: Tuple[ObservationDemandCandidateV1, ...],
    mappings: Tuple[GovernedObservationCapabilityRequirementMappingV1, ...],
    inventory: Tuple[GovernedCapabilityInventoryEntryV1, ...],
    *,
    candidate_only: bool = True,
) -> ObservationDemandCapabilityResolutionInputV1:
    return ObservationDemandCapabilityResolutionInputV1(
        resolution_ref=resolution_ref,
        parent_cognitive_problem_ref=PARENT_PROBLEM_REF,
        source_state_ref=SOURCE_STATE_REF,
        observation_demands=demands,
        governed_requirement_mappings=mappings,
        capability_inventory=inventory,
        current_cognitive_state_ref=SOURCE_STATE_REF,
        context_refs=("context:controlled:observation-capability:v1",),
        trace_ref=f"trace:capability-resolution:{resolution_ref}",
        provenance_refs=("provenance:controlled:observation-capability:v1",),
        candidate_only=candidate_only,
    )


def build_observation_capability_resolution_cases_v1() -> Tuple[ObservationCapabilityResolutionCaseV1, ...]:
    demand_a = _demand("demand:controlled:a", "strategy:controlled:a", "branch:controlled:a")
    demand_b = _demand("demand:controlled:b", "strategy:controlled:b", "branch:controlled:b", need_ref=NEED_REF_B, gap_ref=GAP_REF_B)
    class_a = "capability-class:controlled:visual-perception"
    class_b = "capability-class:controlled:environment-cue-perception"

    return (
        ObservationCapabilityResolutionCaseV1(
            "SINGLE_DEMAND_SINGLE_CAPABILITY_MATCH",
            _request("single", (demand_a,), (_mapping(demand_a, class_a),), (_inventory("capability:single:a", class_a),)),
            "CAPABILITY_CANDIDATES_RESOLVED",
            1,
        ),
        ObservationCapabilityResolutionCaseV1(
            "SINGLE_DEMAND_MULTIPLE_CAPABILITY_MATCHES",
            _request("multiple", (demand_a,), (_mapping(demand_a, class_a),), (_inventory("capability:multiple:a", class_a), _inventory("capability:multiple:b", class_a))),
            "CAPABILITY_CANDIDATES_RESOLVED",
            2,
        ),
        ObservationCapabilityResolutionCaseV1(
            "TWO_INDEPENDENT_DEMANDS",
            _request("two", (demand_a, demand_b), (_mapping(demand_a, class_a), _mapping(demand_b, class_b)), (_inventory("capability:two:a", class_a), _inventory("capability:two:b", class_b))),
            "CAPABILITY_CANDIDATES_RESOLVED",
            2,
        ),
        ObservationCapabilityResolutionCaseV1("NO_OBSERVATION_DEMAND", _request("zero", (), (), ()), "NO_CAPABILITY_REQUIREMENT", 0),
        ObservationCapabilityResolutionCaseV1("MISSING_GOVERNED_CAPABILITY_MAPPING", _request("missing-mapping", (demand_a,), (), (_inventory("capability:missing:a", class_a),)), "NO_CAPABILITY_REQUIREMENT", 0),
        ObservationCapabilityResolutionCaseV1("NO_MATCHING_CAPABILITY", _request("no-match", (demand_a,), (_mapping(demand_a, class_a),), (_inventory("capability:no-match:b", class_b),)), "NO_MATCHING_CAPABILITY", 0),
        ObservationCapabilityResolutionCaseV1("MATCHING_CAPABILITY_UNAVAILABLE", _request("unavailable", (demand_a,), (_mapping(demand_a, class_a),), (_inventory("capability:unavailable:a", class_a, availability_status="UNAVAILABLE"),)), "CAPABILITY_UNAVAILABLE", 0),
        ObservationCapabilityResolutionCaseV1("NOT_ADMITTED_CAPABILITY", _request("not-admitted", (demand_a,), (_mapping(demand_a, class_a),), (_inventory("capability:not-admitted:a", class_a, admission_status="NOT_ADMITTED", eligible=False),)), "CAPABILITY_UNAVAILABLE", 0),
        ObservationCapabilityResolutionCaseV1("SCENARIO_12_SIGNAGE_DEMAND", _request("scenario12-signage", (demand_a,), (_mapping(demand_a, "capability-class:controlled:scenario12:signage-information"),), (_inventory("capability:scenario12:signage", "capability-class:controlled:scenario12:signage-information"),)), "CAPABILITY_CANDIDATES_RESOLVED", 1),
        ObservationCapabilityResolutionCaseV1("SCENARIO_12_HUMAN_FLOW_DEMAND", _request("scenario12-flow", (demand_b,), (_mapping(demand_b, "capability-class:controlled:scenario12:flow-information"),), (_inventory("capability:scenario12:flow", "capability-class:controlled:scenario12:flow-information"),)), "CAPABILITY_CANDIDATES_RESOLVED", 1),
        ObservationCapabilityResolutionCaseV1("SAME_CLASS_MULTIPLE_DEMANDS", _request("same-class", (demand_a, demand_b), (_mapping(demand_a, class_a), _mapping(demand_b, class_a)), (_inventory("capability:same-class:a", class_a),)), "CAPABILITY_CANDIDATES_RESOLVED", 2),
        ObservationCapabilityResolutionCaseV1("INVALID_DEMAND_INPUT", _request("invalid-demand", (replace(demand_a, candidate_only=False),), (_mapping(demand_a, class_a),), (_inventory("capability:invalid:a", class_a),)), "INVALID_INPUT", 0),
        ObservationCapabilityResolutionCaseV1("UNSUPPORTED_MULTI_CLASS_REQUIREMENT", _request("multi-class", (demand_a,), (_mapping(demand_a, class_a, capability_class_refs=(class_a, class_b)),), (_inventory("capability:multi-class:a", class_a), _inventory("capability:multi-class:b", class_b))), "UNSUPPORTED_REQUIREMENT_SHAPE", 0),
        ObservationCapabilityResolutionCaseV1("DETERMINISTIC_REPLAY", _request("deterministic", (demand_a,), (_mapping(demand_a, class_a),), (_inventory("capability:deterministic:a", class_a),)), "CAPABILITY_CANDIDATES_RESOLVED", 1),
    )


__all__ = [
    "ObservationCapabilityResolutionCaseV1",
    "SOURCE_MODE",
    "build_observation_capability_resolution_cases_v1",
]
