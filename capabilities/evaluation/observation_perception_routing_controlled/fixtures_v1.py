"""Synthetic fixtures for the Observation Demand to routing boundary."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Tuple

from capabilities.midplatform.core.cognitive_flow.observation_demand_formation_v1 import (
    ObservationDemandCandidateV1,
)
from capabilities.midplatform.core.observation_gateway.perception_routing_candidate_v1 import (
    PerceptionRoutingFormationInputV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.observation_demand_capability_resolution_v1 import (
    ObservationDemandCapabilityRequirementAdapterV1,
    ObservationDemandCapabilityResolutionCandidateV1,
    ObservationDemandCapabilityResolutionResultV1,
)


SOURCE_STATE = "state:controlled:perception-routing"
PROBLEM = "problem:controlled:perception-routing"
NEED_A = "need:controlled:a"
NEED_B = "need:controlled:b"
GAP_A = "gap:controlled:a"
GAP_B = "gap:controlled:b"
CLASS_A = "capability-class:controlled:visual-information"
CLASS_B = "capability-class:controlled:environmental-cue"


@dataclass(frozen=True)
class PerceptionRoutingCaseV1:
    case_id: str
    request: PerceptionRoutingFormationInputV1
    expected_status: str
    expected_route_count: int
    evaluation_marker: str


def _demand(
    ref: str,
    strategy_ref: str,
    branch_ref: str,
    need_ref: str = NEED_A,
    gap_ref: str = GAP_A,
    target_ref: str = "target:controlled:directional-information",
) -> ObservationDemandCandidateV1:
    return ObservationDemandCandidateV1(
        observation_demand_ref=ref,
        parent_cognitive_problem_ref=PROBLEM,
        source_state_ref=SOURCE_STATE,
        source_strategy_ref=strategy_ref,
        source_coordination_decision_ref=f"coordination:controlled:{strategy_ref}",
        source_branch_ref=branch_ref,
        information_need_refs=(need_ref,),
        information_gap_refs=(gap_ref,),
        acquisition_basis_refs=(f"basis:{strategy_ref}",),
        expected_information_contribution_refs=(f"contribution:{need_ref}",),
        observation_class="PERCEPTION",
        observation_target_refs=(target_ref,),
        observation_constraint_refs=(),
        context_refs=("context:controlled:perception-routing",),
        lineage_refs=(PROBLEM, need_ref, gap_ref, branch_ref, strategy_ref, ref),
        provenance_refs=(f"provenance:{ref}",),
        trace_ref=f"trace:{ref}",
    )


def _requirement(
    demand: ObservationDemandCandidateV1,
    requirement_ref: str,
    capability_class_ref: str,
) -> ObservationDemandCapabilityRequirementAdapterV1:
    return ObservationDemandCapabilityRequirementAdapterV1(
        requirement_ref=requirement_ref,
        source_observation_demand_ref=demand.observation_demand_ref,
        source_strategy_ref=demand.source_strategy_ref,
        source_branch_ref=demand.source_branch_ref,
        parent_cognitive_problem_ref=PROBLEM,
        source_state_ref=SOURCE_STATE,
        information_need_refs=demand.information_need_refs,
        information_gap_refs=demand.information_gap_refs,
        required_capability_class_ref=capability_class_ref,
        source_mapping_ref=f"mapping:{demand.observation_demand_ref}",
        mapping_basis_refs=(f"governed-mapping:{capability_class_ref}",),
        lineage_refs=(*demand.lineage_refs, requirement_ref),
        provenance_refs=(f"provenance:{requirement_ref}",),
        trace_ref=f"trace:{requirement_ref}",
    )


def _resolution_candidate(
    demand: ObservationDemandCandidateV1,
    requirement: ObservationDemandCapabilityRequirementAdapterV1,
    resolution_candidate_ref: str,
    capability_candidate_ref: str,
    capability_class_ref: str,
    *,
    candidate_only: bool = True,
    availability_status: str = "AVAILABLE",
    admission_status: str = "ADMITTED",
) -> ObservationDemandCapabilityResolutionCandidateV1:
    return ObservationDemandCapabilityResolutionCandidateV1(
        capability_resolution_candidate_ref=resolution_candidate_ref,
        capability_candidate_ref=capability_candidate_ref,
        capability_class_ref=capability_class_ref,
        source_requirement_ref=requirement.requirement_ref,
        source_observation_demand_ref=demand.observation_demand_ref,
        source_strategy_ref=demand.source_strategy_ref,
        source_branch_ref=demand.source_branch_ref,
        parent_cognitive_problem_ref=PROBLEM,
        source_state_ref=SOURCE_STATE,
        information_need_refs=demand.information_need_refs,
        information_gap_refs=demand.information_gap_refs,
        match_basis_refs=("governed:exact-capability-class", capability_class_ref),
        availability_status=availability_status,
        admission_status=admission_status,
        lineage_refs=(*requirement.lineage_refs, capability_candidate_ref, resolution_candidate_ref),
        provenance_refs=(f"provenance:{resolution_candidate_ref}",),
        trace_ref=f"trace:{resolution_candidate_ref}",
        candidate_only=candidate_only,
    )


def _resolution_result(
    resolution_ref: str,
    demands: Tuple[ObservationDemandCandidateV1, ...],
    requirements: Tuple[ObservationDemandCapabilityRequirementAdapterV1, ...],
    candidates: Tuple[ObservationDemandCapabilityResolutionCandidateV1, ...],
    status: str = "CAPABILITY_CANDIDATES_RESOLVED",
) -> ObservationDemandCapabilityResolutionResultV1:
    demand_refs = tuple(item.observation_demand_ref for item in demands)
    candidate_refs = tuple(item.capability_resolution_candidate_ref for item in candidates)
    return ObservationDemandCapabilityResolutionResultV1(
        resolution_ref=resolution_ref,
        parent_cognitive_problem_ref=PROBLEM,
        source_state_ref=SOURCE_STATE,
        resolution_status=status,
        input_observation_demand_refs=demand_refs,
        requirement_refs=tuple(item.requirement_ref for item in requirements),
        resolved_candidate_refs=candidate_refs,
        resolved_candidates=candidates,
        excluded_observation_demand_refs=tuple(
            ref for ref in demand_refs
            if ref not in {item.source_observation_demand_ref for item in candidates}
        ),
        excluded_inventory_refs=(),
        exclusion_reasons=(),
        requirements=requirements,
        current_cognitive_state_ref=SOURCE_STATE,
        context_refs=("context:controlled:perception-routing",),
        provenance_refs=(f"provenance:{resolution_ref}",),
        trace_ref=f"trace:{resolution_ref}",
    )


def _request(
    request_ref: str,
    demands: Any,
    requirements: Any,
    resolution: ObservationDemandCapabilityResolutionResultV1,
) -> PerceptionRoutingFormationInputV1:
    return PerceptionRoutingFormationInputV1(
        formation_ref=request_ref,
        parent_cognitive_problem_ref=PROBLEM,
        source_state_ref=SOURCE_STATE,
        observation_demands=demands,
        capability_requirements=requirements,
        resolution_result=resolution,
        context_refs=("context:controlled:perception-routing",),
        trace_ref=f"trace:{request_ref}",
        provenance_refs=(f"provenance:{request_ref}",),
    )


def _single(
    request_ref: str = "formation:single",
    *,
    capability_class_ref: str = CLASS_A,
    capability_candidate_ref: str = "capability:controlled:a",
    resolution_candidate_ref: str = "resolution:controlled:a",
    candidate_only: bool = True,
) -> PerceptionRoutingFormationInputV1:
    demand = _demand("demand:controlled:a", "strategy:controlled:a", "branch:controlled:a")
    requirement = _requirement(demand, "requirement:controlled:a", capability_class_ref)
    candidate = _resolution_candidate(
        demand,
        requirement,
        resolution_candidate_ref,
        capability_candidate_ref,
        capability_class_ref,
        candidate_only=candidate_only,
    )
    return _request(
        request_ref,
        (demand,),
        (requirement,),
        _resolution_result("resolution-run:single", (demand,), (requirement,), (candidate,)),
    )


def build_perception_routing_cases_v1() -> Tuple[PerceptionRoutingCaseV1, ...]:
    demand_a = _demand("demand:controlled:a", "strategy:controlled:a", "branch:controlled:a")
    demand_b = _demand("demand:controlled:b", "strategy:controlled:b", "branch:controlled:b", NEED_B, GAP_B, "target:controlled:environmental-cue")
    requirement_a = _requirement(demand_a, "requirement:controlled:a", CLASS_A)
    requirement_b = _requirement(demand_b, "requirement:controlled:b", CLASS_B)
    candidate_a = _resolution_candidate(demand_a, requirement_a, "resolution:controlled:a", "capability:controlled:a", CLASS_A)
    candidate_b = _resolution_candidate(demand_b, requirement_b, "resolution:controlled:b", "capability:controlled:b", CLASS_B)

    single = _single()
    multiple_candidates = _request(
        "formation:multiple-candidates",
        (demand_a,),
        (requirement_a,),
        _resolution_result(
            "resolution-run:multiple-candidates", (demand_a,), (requirement_a,),
            (candidate_a, _resolution_candidate(demand_a, requirement_a, "resolution:controlled:b", "capability:controlled:b", CLASS_A)),
        ),
    )
    two_demands = _request(
        "formation:two-demands", (demand_a, demand_b), (requirement_a, requirement_b),
        _resolution_result("resolution-run:two-demands", (demand_a, demand_b), (requirement_a, requirement_b), (candidate_a, candidate_b)),
    )
    same_class = _request(
        "formation:same-class", (demand_a,),
        (requirement_a,),
        _resolution_result(
            "resolution-run:same-class", (demand_a,),
            (requirement_a,),
            (
                candidate_a,
                _resolution_candidate(
                    demand_a,
                    requirement_a,
                    "resolution:controlled:same-class:b",
                    "capability:controlled:same-class:b",
                    CLASS_A,
                ),
            ),
        ),
    )
    shared_candidate = _request(
        "formation:shared-capability", (demand_a, demand_b),
        (requirement_a, _requirement(demand_b, "requirement:controlled:b", CLASS_A)),
        _resolution_result(
            "resolution-run:shared-capability", (demand_a, demand_b),
            (requirement_a, _requirement(demand_b, "requirement:controlled:b", CLASS_A)),
            (
                candidate_a,
                _resolution_candidate(
                    demand_b,
                    _requirement(demand_b, "requirement:controlled:b", CLASS_A),
                    "resolution:controlled:b",
                    "capability:controlled:a",
                    CLASS_A,
                ),
            ),
        ),
    )
    no_demand = _request(
        "formation:no-demand", (), (),
        _resolution_result("resolution-run:no-demand", (), (), (), "NO_CAPABILITY_REQUIREMENT"),
    )
    no_requirement = _request(
        "formation:no-requirement", (demand_a,), (),
        _resolution_result("resolution-run:no-requirement", (demand_a,), (), (), "NO_CAPABILITY_REQUIREMENT"),
    )
    no_match = _request(
        "formation:no-match", (demand_a,), (requirement_a,),
        _resolution_result("resolution-run:no-match", (demand_a,), (requirement_a,), (), "NO_MATCHING_CAPABILITY"),
    )
    unavailable = _request(
        "formation:unavailable", (demand_a,), (requirement_a,),
        _resolution_result("resolution-run:unavailable", (demand_a,), (requirement_a,), (), "CAPABILITY_UNAVAILABLE"),
    )
    not_admitted = _request(
        "formation:not-admitted", (demand_a,), (requirement_a,),
        _resolution_result("resolution-run:not-admitted", (demand_a,), (requirement_a,), (), "CAPABILITY_UNAVAILABLE"),
    )
    invalid_resolution = _request(
        "formation:invalid-resolution", (demand_a,), (requirement_a,),
        _resolution_result(
            "resolution-run:invalid-resolution", (demand_a,), (requirement_a,),
            (replace(candidate_a, candidate_only=False),),
        ),
    )
    mismatch = _request(
        "formation:lineage-mismatch", (demand_b,), (requirement_a,),
        _resolution_result("resolution-run:lineage-mismatch", (demand_a,), (requirement_a,), (candidate_a,)),
    )
    signage = _single("formation:scenario12-signage", capability_class_ref="capability-class:controlled:scenario12:signage-information", capability_candidate_ref="capability:scenario12:signage", resolution_candidate_ref="resolution:scenario12:signage")
    flow_demand = _demand("demand:scenario12:flow", "strategy:scenario12:flow", "branch:scenario12", NEED_A, GAP_A, "target:scenario12:human-flow")
    flow_requirement = _requirement(flow_demand, "requirement:scenario12:flow", "capability-class:controlled:scenario12:flow-information")
    flow_candidate = _resolution_candidate(flow_demand, flow_requirement, "resolution:scenario12:flow", "capability:scenario12:flow", flow_requirement.required_capability_class_ref)
    flow = _request("formation:scenario12-flow", (flow_demand,), (flow_requirement,), _resolution_result("resolution-run:scenario12-flow", (flow_demand,), (flow_requirement,), (flow_candidate,)))
    both = _request("formation:scenario12-both", (demand_a, flow_demand), (requirement_a, flow_requirement), _resolution_result("resolution-run:scenario12-both", (demand_a, flow_demand), (requirement_a, flow_requirement), (candidate_a, flow_candidate)))
    malformed = _single("formation:malformed",)
    malformed = replace(malformed, observation_demands=demand_a)

    cases = (
        PerceptionRoutingCaseV1("SINGLE_DEMAND_SINGLE_CAPABILITY_SINGLE_ROUTE", single, "ROUTING_CANDIDATES_FORMED", 1, "single_resolution_single_route"),
        PerceptionRoutingCaseV1("SINGLE_DEMAND_MULTIPLE_CAPABILITY_CANDIDATES", multiple_candidates, "ROUTING_CANDIDATES_FORMED", 2, "multiple_capabilities_multiple_routes"),
        PerceptionRoutingCaseV1("TWO_INDEPENDENT_DEMANDS", two_demands, "ROUTING_CANDIDATES_FORMED", 2, "two_demands_lineage_independent"),
        PerceptionRoutingCaseV1("SAME_DEMAND_SAME_CLASS_TWO_CANDIDATES", same_class, "ROUTING_CANDIDATES_FORMED", 2, "same_class_candidates_not_deduplicated"),
        PerceptionRoutingCaseV1("SAME_CAPABILITY_SUPPORTS_TWO_DEMANDS", shared_candidate, "ROUTING_CANDIDATES_FORMED", 2, "same_capability_multiple_demands_not_merged"),
        PerceptionRoutingCaseV1("NO_OBSERVATION_DEMAND", no_demand, "NO_ROUTING_CANDIDATE", 0, "zero_demand_no_route"),
        PerceptionRoutingCaseV1("NO_CAPABILITY_REQUIREMENT", no_requirement, "NO_ROUTING_CANDIDATE", 0, "zero_capability_no_route"),
        PerceptionRoutingCaseV1("NO_MATCHING_CAPABILITY", no_match, "NO_ROUTING_CANDIDATE", 0, "no_matching_capability_no_route"),
        PerceptionRoutingCaseV1("CAPABILITY_UNAVAILABLE", unavailable, "NO_ROUTING_CANDIDATE", 0, "unavailable_capability_no_route"),
        PerceptionRoutingCaseV1("CAPABILITY_NOT_ADMITTED", not_admitted, "NO_ROUTING_CANDIDATE", 0, "not_admitted_capability_no_route"),
        PerceptionRoutingCaseV1("INVALID_RESOLUTION_CANDIDATE", invalid_resolution, "INVALID_INPUT", 0, "invalid_resolution_candidate_fails_closed"),
        PerceptionRoutingCaseV1("DEMAND_CAPABILITY_LINEAGE_MISMATCH", mismatch, "INVALID_INPUT", 0, "demand_capability_lineage_mismatch_fails_closed"),
        PerceptionRoutingCaseV1("SCENARIO_12_SIGNAGE", signage, "ROUTING_CANDIDATES_FORMED", 1, "scenario12_signage_no_ocr_route_inference"),
        PerceptionRoutingCaseV1("SCENARIO_12_HUMAN_FLOW", flow, "ROUTING_CANDIDATES_FORMED", 1, "scenario12_flow_no_model_route_inference"),
        PerceptionRoutingCaseV1("SCENARIO_12_BOTH_STRATEGIES", both, "ROUTING_CANDIDATES_FORMED", 2, "scenario12_two_routes"),
        PerceptionRoutingCaseV1("DETERMINISTIC_REPLAY", single, "ROUTING_CANDIDATES_FORMED", 1, "deterministic_replay"),
        PerceptionRoutingCaseV1("MALFORMED_INPUT_SHAPE", malformed, "INVALID_INPUT", 0, "malformed_input_fails_closed"),
    )
    return cases


__all__ = ["PerceptionRoutingCaseV1", "build_perception_routing_cases_v1"]
