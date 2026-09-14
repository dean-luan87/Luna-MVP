"""Synthetic target candidates and responsibility audit fixtures."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Tuple

from capabilities.midplatform.provider_runtime_governance.provider_binding_runtime_preparation_v1 import (
    ProviderBindingRuntimePreparationInputV1,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_target_preparation_v1 import (
    ProviderRuntimeTargetPreparationCandidateV1,
)


PROBLEM = "problem:controlled:provider-binding-preparation"
STATE = "state:controlled:provider-binding-preparation"
CONTEXT = ("context:controlled:provider-binding-preparation",)


@dataclass(frozen=True)
class ProviderBindingRuntimePreparationCaseV1:
    case_id: str
    request: Any
    expected_status: str
    expected_candidate_count: int
    evaluation_marker: str


@dataclass(frozen=True)
class ResponsibilityAuditCaseV1:
    case_id: str
    requester: str
    requirement_complexity_owner: str
    executor_complexity_owner: str
    expected_outcome: str


def _target(
    target_ref: str,
    demand_ref: str,
    provider_ref: str,
    provider_class_ref: str = "provider-class:controlled:perception",
    capability_class_ref: str = "capability-class:controlled:perception",
    *,
    model_ref: str | None = None,
) -> ProviderRuntimeTargetPreparationCandidateV1:
    compatibility_ref = f"compatibility:{demand_ref}"
    routing_ref = f"route:{demand_ref}"
    requirement_ref = f"requirement:{demand_ref}"
    resolution_ref = f"resolution:{demand_ref}"
    capability_ref = f"capability:{demand_ref}"
    gap_ref = f"gap:{demand_ref}"
    branch_ref = f"branch:{demand_ref}"
    strategy_ref = f"strategy:{demand_ref}"
    candidate_lineage = (
        PROBLEM,
        f"need:{demand_ref}",
        gap_ref,
        branch_ref,
        strategy_ref,
        demand_ref,
        requirement_ref,
        capability_ref,
        resolution_ref,
        routing_ref,
        compatibility_ref,
        target_ref,
    )
    return ProviderRuntimeTargetPreparationCandidateV1(
        provider_target_candidate_ref=target_ref,
        source_admission_compatibility_candidate_ref=compatibility_ref,
        source_perception_routing_candidate_ref=routing_ref,
        source_observation_demand_ref=demand_ref,
        source_capability_requirement_ref=requirement_ref,
        source_capability_resolution_candidate_ref=resolution_ref,
        capability_candidate_ref=capability_ref,
        capability_class_ref=capability_class_ref,
        provider_candidate_ref=provider_ref,
        provider_class_ref=provider_class_ref,
        source_model_ref=model_ref,
        provider_mapping_basis_refs=("governed:controlled:provider-mapping",),
        provider_admission_refs=(f"provider-admission:{provider_ref}",),
        provider_availability_refs=(f"provider-availability:{provider_ref}",),
        observation_class="PERCEPTION",
        observation_target_refs=(f"target:{demand_ref}",),
        observation_constraint_refs=(),
        expected_information_contribution_refs=(f"contribution:{demand_ref}",),
        information_need_refs=(f"need:{demand_ref}",),
        information_gap_refs=(gap_ref,),
        source_strategy_ref=strategy_ref,
        source_branch_ref=branch_ref,
        parent_cognitive_problem_ref=PROBLEM,
        source_state_ref=STATE,
        context_refs=CONTEXT,
        lineage_refs=candidate_lineage,
        provenance_refs=(f"provenance:{target_ref}",),
        trace_ref=f"trace:{target_ref}",
    )


TARGET_A = _target("provider-target:controlled:a", "demand:controlled:a", "provider:controlled:a")
TARGET_B = _target("provider-target:controlled:b", "demand:controlled:b", "provider:controlled:b", capability_class_ref="capability-class:controlled:environmental")
TARGET_SHARED = _target("provider-target:controlled:shared", "demand:controlled:shared", "provider:controlled:shared")
TARGET_SHARED_B = _target("provider-target:controlled:shared:b", "demand:controlled:shared:b", "provider:controlled:shared")
TARGET_SAME_CLASS_A = _target("provider-target:controlled:same-class:a", "demand:controlled:same-class", "provider:controlled:class:a")
TARGET_SAME_CLASS_B = _target("provider-target:controlled:same-class:b", "demand:controlled:same-class", "provider:controlled:class:b")
TARGET_SAME_DEMAND_B = _target("provider-target:controlled:same-demand:b", "demand:controlled:same-demand", "provider:controlled:second")
TARGET12_SIGNAGE = _target("provider-target:scenario12:signage", "demand:scenario12:signage", "provider:controlled:scenario12:signage", capability_class_ref="capability-class:controlled:scenario12:signage-information")
TARGET12_FLOW = _target("provider-target:scenario12:flow", "demand:scenario12:flow", "provider:controlled:scenario12:flow", capability_class_ref="capability-class:controlled:scenario12:flow-information")


def _request(ref: str, targets: Any) -> ProviderBindingRuntimePreparationInputV1:
    return ProviderBindingRuntimePreparationInputV1(
        preparation_ref=ref,
        parent_cognitive_problem_ref=PROBLEM,
        source_state_ref=STATE,
        provider_target_candidates=targets,
        context_refs=CONTEXT,
        trace_ref=f"trace:{ref}",
        provenance_refs=(f"provenance:{ref}",),
    )


def build_provider_binding_runtime_preparation_cases_v1() -> Tuple[ProviderBindingRuntimePreparationCaseV1, ...]:
    return (
        ProviderBindingRuntimePreparationCaseV1("COMPLETE_REQUIREMENT_REACHES_PROVIDER", _request("prep:responsibility:complete", (TARGET_A,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "complete_requirement_reaches_provider"),
        ProviderBindingRuntimePreparationCaseV1("INCOMPLETE_REQUIREMENT_NOT_REPAIRED_DOWNSTREAM", _request("prep:responsibility:incomplete", (replace(TARGET_A, observation_target_refs=()),)), "INVALID_INPUT", 0, "incomplete_requirement_not_repaired"),
        ProviderBindingRuntimePreparationCaseV1("PROVIDER_DOES_NOT_REINTERPRET_DEMAND", _request("prep:responsibility:no-reinterpret", (TARGET_A,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "provider_does_not_reinterpret_demand"),
        ProviderBindingRuntimePreparationCaseV1("PROVIDER_DOES_NOT_CREATE_CAPABILITY_REQUIREMENT", _request("prep:responsibility:no-new-requirement", (TARGET_A,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "provider_does_not_create_requirement"),
        ProviderBindingRuntimePreparationCaseV1("GATEWAY_DOES_NOT_SELECT_PROVIDER", _request("prep:responsibility:gateway", (TARGET_A,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "gateway_does_not_select_provider"),
        ProviderBindingRuntimePreparationCaseV1("FPO_DOES_NOT_BIND_PROVIDER", _request("prep:responsibility:fpo", (TARGET_A,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "fpo_does_not_bind_provider"),
        ProviderBindingRuntimePreparationCaseV1("MODEL_MANAGER_DOES_NOT_CREATE_COGNITIVE_NEED", _request("prep:responsibility:model-manager", (TARGET_A,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "model_manager_does_not_create_need"),
        ProviderBindingRuntimePreparationCaseV1("REQUESTER_OWNS_MISSING_TARGET", _request("prep:responsibility:missing-target", (replace(TARGET_A, observation_target_refs=()),)), "INVALID_INPUT", 0, "requester_missing_target_fail_closed"),
        ProviderBindingRuntimePreparationCaseV1("PROVIDER_OWNS_PROVIDER_UNAVAILABLE", _request("prep:responsibility:provider-unavailable", (TARGET_A,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "provider_unavailability_owner_preserved"),
        ProviderBindingRuntimePreparationCaseV1("RESOURCE_FAILURE_NOT_RECAST_AS_COGNITIVE_FAILURE", _request("prep:responsibility:resource", (TARGET_A,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "resource_failure_stays_operational"),
        ProviderBindingRuntimePreparationCaseV1("EXECUTION_FAILURE_NOT_RECAST_AS_DEMAND_MUTATION", _request("prep:responsibility:execution", (TARGET_A,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "execution_failure_stays_runtime"),
        ProviderBindingRuntimePreparationCaseV1("SINGLE_PROVIDER_TARGET", _request("prep:single", (TARGET_A,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "single_target"),
        ProviderBindingRuntimePreparationCaseV1("MULTIPLE_PROVIDER_TARGETS", _request("prep:multiple", (TARGET_A, TARGET_B)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 2, "multiple_targets"),
        ProviderBindingRuntimePreparationCaseV1("SAME_PROVIDER_MULTI_DEMAND", _request("prep:same-provider", (TARGET_SHARED, TARGET_SHARED_B)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 2, "same_provider_multi_demand"),
        ProviderBindingRuntimePreparationCaseV1("SAME_CLASS_DISTINCT_PROVIDERS", _request("prep:same-class", (TARGET_SAME_CLASS_A, TARGET_SAME_CLASS_B)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 2, "same_class_distinct_providers"),
        ProviderBindingRuntimePreparationCaseV1("NO_PROVIDER_TARGET", _request("prep:none", ()), "NO_PROVIDER_BINDING_PREPARATION_CANDIDATE", 0, "zero_target"),
        ProviderBindingRuntimePreparationCaseV1("INVALID_PROVIDER_TARGET", _request("prep:invalid", (replace(TARGET_A, candidate_only=False),)), "INVALID_INPUT", 0, "invalid_target"),
        ProviderBindingRuntimePreparationCaseV1("LINEAGE_MISMATCH", _request("prep:lineage", (replace(TARGET_A, source_observation_demand_ref="demand:controlled:other"),)), "INVALID_INPUT", 0, "lineage_mismatch"),
        ProviderBindingRuntimePreparationCaseV1("MODEL_OPTIONAL", _request("prep:model-optional", (TARGET_A,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "model_optional"),
        ProviderBindingRuntimePreparationCaseV1("NO_MODEL_INFERENCE", _request("prep:no-model", (replace(TARGET_A, source_model_ref=None),)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "no_model_inference"),
        ProviderBindingRuntimePreparationCaseV1("NO_EXECUTION_INSTANCE", _request("prep:no-execution-instance", (TARGET_A,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "no_execution_instance"),
        ProviderBindingRuntimePreparationCaseV1("NO_RUNTIME_ALLOCATION", _request("prep:no-runtime-allocation", (TARGET_A,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "no_runtime_allocation"),
        ProviderBindingRuntimePreparationCaseV1("NO_GATEWAY_SUBMISSION", _request("prep:no-gateway", (TARGET_A,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "no_gateway_submission"),
        ProviderBindingRuntimePreparationCaseV1("SCENARIO12_SIGNAGE", _request("prep:scenario12:signage", (TARGET12_SIGNAGE,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "scenario12_signage_abstract"),
        ProviderBindingRuntimePreparationCaseV1("SCENARIO12_HUMAN_FLOW", _request("prep:scenario12:flow", (TARGET12_FLOW,)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 1, "scenario12_flow_abstract"),
        ProviderBindingRuntimePreparationCaseV1("SCENARIO12_BOTH", _request("prep:scenario12:both", (TARGET12_SIGNAGE, TARGET12_FLOW)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 2, "scenario12_independent_targets"),
        ProviderBindingRuntimePreparationCaseV1("DETERMINISTIC_REPLAY", _request("prep:deterministic", (TARGET_A, TARGET_B)), "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED", 2, "deterministic_replay"),
        ProviderBindingRuntimePreparationCaseV1("MALFORMED_INPUT", _request("prep:malformed", TARGET_A), "INVALID_INPUT", 0, "malformed_input"),
    )


def build_responsibility_audit_cases_v1() -> Tuple[ResponsibilityAuditCaseV1, ...]:
    return (
        ResponsibilityAuditCaseV1("COMPLETE_REQUIREMENT_REACHES_PROVIDER", "Observation Demand", "Observation Demand", "Runtime", "complete semantic demand is carried forward"),
        ResponsibilityAuditCaseV1("INCOMPLETE_REQUIREMENT_NOT_REPAIRED_DOWNSTREAM", "Observation Demand", "Observation Demand", "Provider Governance", "downstream fails closed and does not invent target"),
        ResponsibilityAuditCaseV1("PROVIDER_DOES_NOT_REINTERPRET_DEMAND", "Provider Runtime Target Preparation", "Observation Demand", "Provider Governance", "provider consumes explicit refs only"),
        ResponsibilityAuditCaseV1("PROVIDER_DOES_NOT_CREATE_CAPABILITY_REQUIREMENT", "Capability Governance", "Capability Governance", "Provider Governance", "provider does not create cognitive requirement"),
        ResponsibilityAuditCaseV1("GATEWAY_DOES_NOT_SELECT_PROVIDER", "Provider Governance", "Provider Governance", "Observation Gateway", "Gateway validates ingress, not provider choice"),
        ResponsibilityAuditCaseV1("FPO_DOES_NOT_BIND_PROVIDER", "FPO", "FPO", "Provider Governance", "FPO remains semantic control owner"),
        ResponsibilityAuditCaseV1("MODEL_MANAGER_DOES_NOT_CREATE_COGNITIVE_NEED", "Cognitive owner", "Cognitive owner", "Model Manager", "Model Manager does not create Need"),
        ResponsibilityAuditCaseV1("REQUESTER_OWNS_MISSING_TARGET", "Observation Demand", "Observation Demand", "Provider Governance", "missing requirement is requester failure"),
        ResponsibilityAuditCaseV1("PROVIDER_OWNS_PROVIDER_UNAVAILABLE", "Provider Governance", "Provider Governance", "Provider Governance", "provider availability failure stays provider-owned"),
        ResponsibilityAuditCaseV1("RESOURCE_FAILURE_NOT_RECAST_AS_COGNITIVE_FAILURE", "Runtime Allocation", "Runtime Allocation", "Resource owner", "resource failure remains operational"),
        ResponsibilityAuditCaseV1("EXECUTION_FAILURE_NOT_RECAST_AS_DEMAND_MUTATION", "Runtime", "Observation Demand", "Runtime", "execution failure does not mutate demand"),
    )


__all__ = [
    "ProviderBindingRuntimePreparationCaseV1",
    "ResponsibilityAuditCaseV1",
    "build_provider_binding_runtime_preparation_cases_v1",
    "build_responsibility_audit_cases_v1",
]
