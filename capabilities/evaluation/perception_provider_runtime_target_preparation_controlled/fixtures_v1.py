"""Synthetic, explicit mappings for Provider Runtime Target Preparation."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Tuple

from capabilities.midplatform.core.observation_gateway.perception_routing_candidate_v1 import (
    PerceptionRoutingCandidateV1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.perception_routing_admission_compatibility_v1 import (
    PerceptionRoutingAdmissionCompatibilityCandidateV1,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_target_preparation_v1 import (
    GovernedProviderRuntimeTargetMappingV1,
    ProviderRuntimeTargetPreparationInputV1,
)


PROBLEM = "problem:controlled:provider-runtime-target-preparation"
STATE = "state:controlled:provider-runtime-target-preparation"
CONTEXT = ("context:controlled:provider-runtime-target-preparation",)
CLASS_A = "capability-class:controlled:visual-information"
CLASS_B = "capability-class:controlled:environmental-information"
TARGET_A = ("target:controlled:directional-information",)
TARGET_B = ("target:controlled:environmental-cue",)


@dataclass(frozen=True)
class ProviderRuntimeTargetPreparationCaseV1:
    case_id: str
    request: Any
    expected_status: str
    expected_target_count: int
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


def _compat(
    route: PerceptionRoutingCandidateV1,
    compatibility_ref: str,
) -> PerceptionRoutingAdmissionCompatibilityCandidateV1:
    candidate_ref = f"fpo-compat:{compatibility_ref}"
    return PerceptionRoutingAdmissionCompatibilityCandidateV1(
        admission_compatibility_candidate_ref=candidate_ref,
        source_perception_routing_candidate_ref=route.perception_routing_candidate_ref,
        source_observation_demand_ref=route.source_observation_demand_ref,
        source_capability_requirement_ref=route.source_capability_requirement_ref,
        source_capability_resolution_candidate_ref=route.source_capability_resolution_candidate_ref,
        capability_candidate_ref=route.capability_candidate_ref,
        capability_class_ref=route.capability_class_ref,
        slot_ref=route.slot_ref,
        observation_class=route.observation_class,
        observation_target_refs=route.observation_target_refs,
        observation_constraint_refs=route.observation_constraint_refs,
        expected_information_contribution_refs=route.expected_information_contribution_refs,
        information_need_refs=route.information_need_refs,
        information_gap_refs=route.information_gap_refs,
        source_strategy_ref=route.source_strategy_ref,
        source_branch_ref=route.source_branch_ref,
        parent_cognitive_problem_ref=route.parent_cognitive_problem_ref,
        source_state_ref=STATE,
        context_refs=route.context_refs,
        admission_compatibility_basis_refs=("governed:fpo-admission-compatibility",),
        lineage_refs=(*route.lineage_refs, candidate_ref),
        provenance_refs=route.provenance_refs,
        trace_ref=route.trace_ref,
    )


ROUTE_A = _route(
    "route:controlled:a", "demand:controlled:a", "resolution:controlled:a", "capability:controlled:a"
)
ROUTE_B = _route(
    "route:controlled:b", "demand:controlled:b", "resolution:controlled:b", "capability:controlled:b", CLASS_B, TARGET_B
)
ROUTE_C = _route(
    "route:controlled:c", "demand:controlled:c", "resolution:controlled:c", "capability:controlled:c"
)
SCENARIO12_SIGNAGE = _route(
    "route:scenario12:signage", "demand:scenario12:signage", "resolution:scenario12:signage",
    "capability:scenario12:signage-information", "capability-class:controlled:scenario12:signage-information"
)
SCENARIO12_FLOW = _route(
    "route:scenario12:flow", "demand:scenario12:flow", "resolution:scenario12:flow",
    "capability:scenario12:flow-information", "capability-class:controlled:scenario12:flow-information", TARGET_B
)


COMPAT_A = _compat(ROUTE_A, "compatibility:controlled:a")
COMPAT_B = _compat(ROUTE_B, "compatibility:controlled:b")
COMPAT_C = _compat(ROUTE_C, "compatibility:controlled:c")
COMPAT12_SIGNAGE = _compat(SCENARIO12_SIGNAGE, "compatibility:scenario12:signage")
COMPAT12_FLOW = _compat(SCENARIO12_FLOW, "compatibility:scenario12:flow")


def _mapping(
    compatibility: PerceptionRoutingAdmissionCompatibilityCandidateV1,
    provider_ref: str,
    provider_class_ref: str = "provider-class:controlled:perception",
    *,
    capability_class_ref: str | None = None,
    availability_status: str = "AVAILABLE",
    admission_status: str = "ADMITTED",
    eligible: bool = True,
    model_ref: str | None = None,
    mapping_suffix: str = "a",
) -> GovernedProviderRuntimeTargetMappingV1:
    return GovernedProviderRuntimeTargetMappingV1(
        mapping_ref=f"mapping:{compatibility.admission_compatibility_candidate_ref}:{mapping_suffix}",
        source_admission_compatibility_candidate_ref=compatibility.admission_compatibility_candidate_ref,
        capability_class_ref=capability_class_ref or compatibility.capability_class_ref,
        provider_candidate_ref=provider_ref,
        provider_class_ref=provider_class_ref,
        provider_mapping_basis_refs=("governed:controlled:capability-provider-mapping",),
        provider_admission_refs=(f"provider-admission:{provider_ref}",),
        provider_availability_refs=(f"provider-availability:{provider_ref}",),
        availability_status=availability_status,
        admission_status=admission_status,
        eligible=eligible,
        source_model_ref=model_ref,
    )


def _request(
    ref: str,
    compatibilities: Any,
    mappings: Any,
) -> ProviderRuntimeTargetPreparationInputV1:
    return ProviderRuntimeTargetPreparationInputV1(
        preparation_ref=ref,
        parent_cognitive_problem_ref=PROBLEM,
        source_state_ref=STATE,
        compatibility_candidates=compatibilities,
        provider_mappings=mappings,
        context_refs=CONTEXT,
        trace_ref=f"trace:{ref}",
        provenance_refs=(f"provenance:{ref}",),
    )


def build_provider_runtime_target_preparation_cases_v1() -> Tuple[
    ProviderRuntimeTargetPreparationCaseV1, ...
]:
    return (
        ProviderRuntimeTargetPreparationCaseV1(
            "SINGLE_COMPATIBILITY_SINGLE_PROVIDER", _request("prep:single", (COMPAT_A,), (_mapping(COMPAT_A, "provider:controlled:a"),)),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 1, "single_provider_candidate",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "SINGLE_COMPATIBILITY_MULTIPLE_PROVIDERS", _request("prep:multiple-providers", (COMPAT_A,), (_mapping(COMPAT_A, "provider:controlled:a", mapping_suffix="a"), _mapping(COMPAT_A, "provider:controlled:b", mapping_suffix="b"))),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 2, "multiple_providers_all_retained",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "MULTIPLE_COMPATIBILITY_CANDIDATES", _request("prep:multiple-compat", (COMPAT_A, COMPAT_B), (_mapping(COMPAT_A, "provider:controlled:a"), _mapping(COMPAT_B, "provider:controlled:b"))),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 2, "multiple_compatibility_candidates",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "SAME_PROVIDER_CLASS_TWO_PROVIDER_CANDIDATES", _request("prep:same-provider-class", (COMPAT_A,), (_mapping(COMPAT_A, "provider:controlled:a", mapping_suffix="a"), _mapping(COMPAT_A, "provider:controlled:b", mapping_suffix="b"))),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 2, "same_provider_class_not_deduplicated",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "SAME_PROVIDER_MULTIPLE_DEMANDS", _request("prep:shared-provider", (COMPAT_A, COMPAT_B), (_mapping(COMPAT_A, "provider:controlled:shared"), _mapping(COMPAT_B, "provider:controlled:shared"))),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 2, "same_provider_multiple_demands_not_merged",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "SAME_CAPABILITY_MULTIPLE_PROVIDERS", _request("prep:same-capability", (COMPAT_A,), (_mapping(COMPAT_A, "provider:controlled:a", mapping_suffix="a"), _mapping(COMPAT_A, "provider:controlled:b", mapping_suffix="b"))),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 2, "same_capability_multiple_providers_retained",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "NO_COMPATIBILITY_CANDIDATE", _request("prep:none", (), ()),
            "NO_PROVIDER_TARGET_CANDIDATE", 0, "zero_input_zero_candidate",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "NO_PROVIDER_MAPPING", _request("prep:no-mapping", (COMPAT_A,), ()),
            "NO_PROVIDER_MAPPING", 0, "no_mapping_fails_closed",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "NO_MATCHING_PROVIDER", _request("prep:no-match", (COMPAT_A,), (_mapping(COMPAT_A, "provider:controlled:wrong-class", capability_class_ref=CLASS_B),)),
            "NO_MATCHING_PROVIDER", 0, "no_match_fails_closed",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "PROVIDER_UNAVAILABLE", _request("prep:unavailable", (COMPAT_A,), (_mapping(COMPAT_A, "provider:controlled:unavailable", availability_status="UNAVAILABLE"),)),
            "PROVIDER_UNAVAILABLE", 0, "unavailable_fails_closed",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "PROVIDER_NOT_ADMITTED", _request("prep:not-admitted", (COMPAT_A,), (_mapping(COMPAT_A, "provider:controlled:not-admitted", admission_status="NOT_ADMITTED"),)),
            "PROVIDER_NOT_ADMITTED", 0, "not_admitted_fails_closed",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "INVALID_COMPATIBILITY_CANDIDATE", _request("prep:invalid", (replace(COMPAT_A, candidate_only=False),), (_mapping(COMPAT_A, "provider:controlled:a"),)),
            "INVALID_INPUT", 0, "invalid_compatibility_fails_closed",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "LINEAGE_MISMATCH", _request("prep:lineage-mismatch", (replace(COMPAT_A, source_observation_demand_ref="demand:controlled:other"),), (_mapping(COMPAT_A, "provider:controlled:a"),)),
            "INVALID_INPUT", 0, "lineage_mismatch_fails_closed",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "DUPLICATE_PROVIDER_CANDIDATE", _request("prep:duplicate", (COMPAT_A,), (_mapping(COMPAT_A, "provider:controlled:a", mapping_suffix="a"), _mapping(COMPAT_A, "provider:controlled:a", mapping_suffix="b"))),
            "INVALID_INPUT", 0, "duplicate_provider_candidate_fails_closed",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "MODEL_REF_OPTIONAL", _request("prep:model-optional", (COMPAT_A,), (_mapping(COMPAT_A, "provider:controlled:model-optional", model_ref="model:controlled:opaque"),)),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 1, "model_ref_governed_optional",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "NO_MODEL_INFERENCE", _request("prep:no-model-inference", (COMPAT_A,), (_mapping(COMPAT_A, "provider:controlled:no-model"),)),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 1, "no_model_inference",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "NO_EXECUTION_INSTANCE_CREATION", _request("prep:no-execution-instance", (COMPAT_A,), (_mapping(COMPAT_A, "provider:controlled:a"),)),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 1, "no_execution_instance",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "NO_PROVIDER_BINDING", _request("prep:no-binding", (COMPAT_A,), (_mapping(COMPAT_A, "provider:controlled:a"),)),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 1, "no_provider_binding",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "NO_GATEWAY_ADMISSION", _request("prep:no-gateway-admission", (COMPAT_A,), (_mapping(COMPAT_A, "provider:controlled:a"),)),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 1, "no_gateway_admission",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "SCENARIO12_SIGNAGE", _request("prep:scenario12-signage", (COMPAT12_SIGNAGE,), (_mapping(COMPAT12_SIGNAGE, "provider:controlled:scenario12:signage"),)),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 1, "scenario12_no_ocr_inference",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "SCENARIO12_HUMAN_FLOW", _request("prep:scenario12-flow", (COMPAT12_FLOW,), (_mapping(COMPAT12_FLOW, "provider:controlled:scenario12:flow"),)),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 1, "scenario12_no_vlm_inference",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "SCENARIO12_BOTH", _request("prep:scenario12-both", (COMPAT12_SIGNAGE, COMPAT12_FLOW), (_mapping(COMPAT12_SIGNAGE, "provider:controlled:scenario12:signage"), _mapping(COMPAT12_FLOW, "provider:controlled:scenario12:flow"))),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 2, "scenario12_independent_targets",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "DETERMINISTIC_REPLAY", _request("prep:deterministic", (COMPAT_A, COMPAT_B), (_mapping(COMPAT_A, "provider:controlled:a"), _mapping(COMPAT_B, "provider:controlled:b"))),
            "PROVIDER_TARGET_CANDIDATES_FORMED", 2, "deterministic_replay",
        ),
        ProviderRuntimeTargetPreparationCaseV1(
            "MALFORMED_INPUT_SHAPE", _request("prep:malformed", COMPAT_A, (_mapping(COMPAT_A, "provider:controlled:a"),)),
            "INVALID_INPUT", 0, "malformed_input_fails_closed",
        ),
    )


__all__ = [
    "ProviderRuntimeTargetPreparationCaseV1",
    "build_provider_runtime_target_preparation_cases_v1",
]
