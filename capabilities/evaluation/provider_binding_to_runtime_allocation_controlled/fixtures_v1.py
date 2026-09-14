"""Controlled fixtures for Provider Binding and Runtime Preparation."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Dict, Tuple

from capabilities.midplatform.provider_runtime_governance.provider_binding_candidate_v1 import (
    ProviderBindingCandidateInputV1,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_runtime_preparation_v1 import (
    ProviderBindingRuntimePreparationCandidateV1,
)
from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    ARCHITECTURE_SOURCE_REF,
    COMMON_GOVERNANCE_PROFILES,
    CONSTITUTION_SOURCE_REF,
    CORE_GOVERNANCE_RULE_REGISTRY_V1,
    GovernanceAuthorityResponsibilityRecordV1,
    PhaseGovernanceProfileV1,
    PROTOCOL_SOURCE_REF,
)


PHASE = "Phase-Provider-Binding-To-Runtime-Allocation-Controlled-Implementation-v1-001"
PROBLEM = "problem:controlled:provider-binding-runtime-allocation"
STATE = "state:controlled:provider-binding-runtime-allocation"
CONTEXT = ("context:controlled:provider-binding-runtime-allocation",)


@dataclass(frozen=True)
class PipelineCaseV1:
    case_id: str
    request: Any
    expected_binding_status: str
    expected_binding_count: int
    run_allocation: bool = False
    run_execution_preparation: bool = False
    expected_allocation_status: str = "NO_RUNTIME_ALLOCATION_PREPARATION_CANDIDATE"
    expected_allocation_count: int = 0
    expected_execution_status: str = "NO_EXECUTION_INSTANCE_PREPARATION_CANDIDATE"
    expected_execution_count: int = 0
    profile: Any = None
    authority_records: Any = None
    postflight_artifact: Any = None
    boundary_payload: Any = None
    failure_ownership_payload: Any = None
    expected_owner: str = ""
    evaluation_marker: str = "controlled_provider_binding_runtime_allocation"


def valid_profile() -> PhaseGovernanceProfileV1:
    return PhaseGovernanceProfileV1(
        phase_ref=PHASE,
        phase_owner_ref="Provider Governance",
        domains=("CONTROLLED_PHASE",),
        owners_touched=(
            "Provider Governance",
            "Runtime Executor",
            "FPO",
            "Observation Gateway",
            "Capability Governance",
        ),
        governance_profiles=COMMON_GOVERNANCE_PROFILES,
        maturity_level="CONTROLLED_V1",
        runtime_level="NONE",
        candidate_only=True,
        read_only=True,
        truth_authority=False,
        world_truth_authority=False,
        runtime_authority=False,
        authority_refs=(
            "authority:provider-binding-preparation",
            "authority:runtime-preparation",
        ),
        responsibility_refs=(
            "responsibility:provider-binding-preparation",
            "responsibility:runtime-preparation",
        ),
        input_contract_refs=(
            "ProviderBindingCandidateInputV1",
            "RuntimeAllocationPreparationInputV1",
        ),
        output_contract_refs=(
            "ProviderBindingCandidateV1",
            "RuntimeAllocationPreparationCandidateV1",
            "ExecutionInstancePreparationCandidateV1",
        ),
        protocol_refs=(PROTOCOL_SOURCE_REF,),
        constitution_refs=(CONSTITUTION_SOURCE_REF,),
        context_refs=CONTEXT,
        trace_ref="trace:provider-binding-runtime-allocation:governance",
    )


def valid_authority_records() -> Tuple[GovernanceAuthorityResponsibilityRecordV1, ...]:
    return (
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="provider-governance:binding-preparation",
            owner_ref="Provider Governance",
            authority_refs=("authority:provider-binding-preparation",),
            responsibility_refs=("responsibility:provider-binding-preparation",),
            decision_types=("provider_binding_candidate_formation",),
            failure_types=("provider_binding_input_failure",),
            authority_responsibility_map=(
                (
                    "authority:provider-binding-preparation",
                    "responsibility:provider-binding-preparation",
                ),
            ),
            responsibility_owner_refs=(
                ("responsibility:provider-binding-preparation", "Provider Governance"),
            ),
            operational_authority=True,
        ),
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="runtime-executor:preparation",
            owner_ref="Runtime Executor",
            authority_refs=("authority:runtime-preparation",),
            responsibility_refs=("responsibility:runtime-preparation",),
            decision_types=("runtime_preparation_candidate_formation",),
            failure_types=("runtime_preparation_failure",),
            authority_responsibility_map=(
                ("authority:runtime-preparation", "responsibility:runtime-preparation"),
            ),
            responsibility_owner_refs=(
                ("responsibility:runtime-preparation", "Runtime Executor"),
            ),
            operational_authority=True,
        ),
    )


def _prep(
    prep_ref: str,
    demand_ref: str,
    provider_ref: str,
    *,
    model_ref: str | None = None,
    capability_class_ref: str = "capability-class:controlled:perception",
) -> ProviderBindingRuntimePreparationCandidateV1:
    target_ref = f"provider-target:{provider_ref}"
    compatibility_ref = f"compatibility:{demand_ref}"
    routing_ref = f"route:{demand_ref}"
    requirement_ref = f"requirement:{demand_ref}"
    resolution_ref = f"resolution:{demand_ref}"
    capability_ref = f"capability:{demand_ref}"
    gap_ref = f"gap:{demand_ref}"
    branch_ref = f"branch:{demand_ref}"
    strategy_ref = f"strategy:{demand_ref}"
    lineage = (
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
        prep_ref,
    )
    return ProviderBindingRuntimePreparationCandidateV1(
        provider_binding_preparation_candidate_ref=prep_ref,
        source_provider_target_candidate_ref=target_ref,
        source_admission_compatibility_candidate_ref=compatibility_ref,
        source_perception_routing_candidate_ref=routing_ref,
        source_observation_demand_ref=demand_ref,
        source_capability_requirement_ref=requirement_ref,
        source_capability_resolution_candidate_ref=resolution_ref,
        capability_candidate_ref=capability_ref,
        capability_class_ref=capability_class_ref,
        provider_candidate_ref=provider_ref,
        provider_class_ref="provider-class:controlled:perception",
        source_model_ref=model_ref,
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
        binding_preparation_basis_refs=("governed:provider-target-to-binding-preparation",),
        context_refs=CONTEXT,
        lineage_refs=lineage,
        provenance_refs=(f"provenance:{prep_ref}",),
        trace_ref=f"trace:{prep_ref}",
    )


PREP_A = _prep("provider-binding-preparation:a", "demand:controlled:a", "provider:controlled:a")
PREP_B = _prep("provider-binding-preparation:b", "demand:controlled:b", "provider:controlled:b", capability_class_ref="capability-class:controlled:environmental")
PREP_SHARED_A = _prep("provider-binding-preparation:shared:a", "demand:controlled:shared:a", "provider:controlled:shared")
PREP_SHARED_B = _prep("provider-binding-preparation:shared:b", "demand:controlled:shared:b", "provider:controlled:shared")
PREP_SAME_CLASS_A = _prep("provider-binding-preparation:same-class:a", "demand:controlled:same-class", "provider:controlled:class:a")
PREP_SAME_CLASS_B = _prep("provider-binding-preparation:same-class:b", "demand:controlled:same-class", "provider:controlled:class:b")
PREP_MODEL = _prep("provider-binding-preparation:model", "demand:controlled:model", "provider:controlled:model", model_ref="model:controlled:explicit")
PREP12_SIGNAGE = _prep("provider-binding-preparation:scenario12:signage", "demand:scenario12:signage", "provider:controlled:scenario12:signage", capability_class_ref="capability-class:controlled:scenario12:signage-information")
PREP12_FLOW = _prep("provider-binding-preparation:scenario12:flow", "demand:scenario12:flow", "provider:controlled:scenario12:flow", capability_class_ref="capability-class:controlled:scenario12:flow-information")


def _request(
    ref: str,
    candidates: Any,
    *,
    runtime_requirement_refs: Tuple[str, ...] = (),
    resource_class_refs: Tuple[str, ...] = (),
    execution_class_refs: Tuple[str, ...] = (),
) -> ProviderBindingCandidateInputV1:
    return ProviderBindingCandidateInputV1(
        preparation_ref=ref,
        parent_cognitive_problem_ref=PROBLEM,
        source_state_ref=STATE,
        preparation_candidates=candidates,
        context_refs=CONTEXT,
        trace_ref=f"trace:{ref}",
        provenance_refs=(f"provenance:{ref}",),
        runtime_requirement_refs=runtime_requirement_refs,
        resource_class_refs=resource_class_refs,
        execution_class_refs=execution_class_refs,
    )


def _pipeline(
    case_id: str,
    ref: str,
    candidates: Any,
    *,
    runtime: bool = False,
    execution: bool = False,
    model: str | None = None,
    runtime_requirements: Tuple[str, ...] = (),
    resource_classes: Tuple[str, ...] = (),
    execution_classes: Tuple[str, ...] = (),
) -> PipelineCaseV1:
    request = _request(
        ref,
        candidates,
        runtime_requirement_refs=runtime_requirements,
        resource_class_refs=resource_classes,
        execution_class_refs=execution_classes,
    )
    return PipelineCaseV1(
        case_id=case_id,
        request=request,
        expected_binding_status=(
            "PROVIDER_BINDING_CANDIDATES_FORMED"
            if candidates
            else "NO_PROVIDER_BINDING_CANDIDATE"
        ),
        expected_binding_count=len(candidates),
        run_allocation=runtime,
        run_execution_preparation=execution,
        expected_allocation_status=(
            "RUNTIME_ALLOCATION_PREPARATION_CANDIDATES_FORMED"
            if runtime and candidates
            else "NO_RUNTIME_ALLOCATION_PREPARATION_CANDIDATE"
        ),
        expected_allocation_count=len(candidates) if runtime and candidates else 0,
        expected_execution_status=(
            "EXECUTION_INSTANCE_PREPARATION_CANDIDATES_FORMED"
            if execution and candidates
            else "NO_EXECUTION_INSTANCE_PREPARATION_CANDIDATE"
        ),
        expected_execution_count=len(candidates) if execution and candidates else 0,
    )


def _postflight_case(case_id: str, artifact: Dict[str, Any], *, failure: Dict[str, Any] | None = None) -> PipelineCaseV1:
    case = _pipeline(case_id, f"prep:{case_id.lower()}", (PREP_A,))
    return replace(case, postflight_artifact=artifact, failure_ownership_payload=failure)


def build_provider_binding_to_runtime_allocation_cases_v1() -> Tuple[PipelineCaseV1, ...]:
    valid_artifact = {
        "candidate_only": True,
        "read_only": True,
        "truth_declared": False,
        "world_truth_declared": False,
        "provider_bound": False,
        "runtime_allocated": False,
        "execution_instance_created": False,
        "provider_session_started": False,
        "gateway_submission": False,
        "resource_allocated": False,
    }
    cases = [
        _pipeline("SINGLE_PROVIDER_BINDING_CANDIDATE", "binding:single", (PREP_A,)),
        _pipeline("MULTIPLE_PROVIDER_BINDING_CANDIDATES", "binding:multiple", (PREP_A, PREP_B)),
        _pipeline("SAME_PROVIDER_MULTI_DEMAND", "binding:same-provider", (PREP_SHARED_A, PREP_SHARED_B)),
        _pipeline("SAME_CLASS_DISTINCT_PROVIDERS", "binding:same-class", (PREP_SAME_CLASS_A, PREP_SAME_CLASS_B)),
        _pipeline("PROVIDER_ONLY_NO_MODEL", "binding:provider-only", (_prep("provider-binding-preparation:provider-only", "demand:provider-only", "provider:controlled:provider-only"),)),
        _pipeline("EXPLICIT_MODEL_CARRY_FORWARD", "binding:model", (PREP_MODEL,)),
        _pipeline("NO_MODEL_INFERENCE", "binding:no-model-inference", (_prep("provider-binding-preparation:no-model", "demand:no-model", "provider:controlled:no-model"),)),
        replace(_pipeline("INVALID_PROVIDER_TARGET", "binding:invalid-target", (replace(PREP_A, candidate_only=False),)), expected_binding_status="INVALID_INPUT", expected_binding_count=0),
        replace(_pipeline("LINEAGE_MISMATCH", "binding:lineage", (replace(PREP_A, source_observation_demand_ref="demand:controlled:other"),)), expected_binding_status="INVALID_INPUT", expected_binding_count=0),
        _pipeline("PROVIDER_NOT_ELIGIBLE", "binding:provider-not-eligible", (PREP_A,)),
        replace(_pipeline("BINDING_INPUT_INCOMPLETE", "binding:incomplete", (replace(PREP_A, observation_target_refs=()),)), expected_binding_status="INVALID_INPUT", expected_binding_count=0),
        _pipeline("PROVIDER_GOVERNANCE_OWNS_BINDING_FAILURE", "binding:failure-owner", (PREP_A,)),
        _pipeline("UPSTREAM_NOT_BLAMED_FOR_PROVIDER_FAILURE", "binding:upstream-not-blamed", (PREP_A,)),
        _pipeline("RUNTIME_REQUIREMENT_PREPARATION", "binding:runtime-requirement", (PREP_A,), runtime=True, runtime_requirements=("runtime-requirement:perception",), resource_classes=("resource-class:perception",), execution_classes=("execution-class:bounded-observation",)),
        _pipeline("NO_CONCRETE_RESOURCE_ALLOCATION", "binding:no-resource", (PREP_A,), runtime=True, runtime_requirements=("runtime-requirement:perception",), resource_classes=("resource-class:perception",), execution_classes=("execution-class:bounded-observation",)),
        _pipeline("NO_EXECUTION_INSTANCE", "binding:no-execution", (PREP_A,), runtime=True, runtime_requirements=("runtime-requirement:perception",), execution_classes=("execution-class:bounded-observation",)),
        _pipeline("EXECUTION_INSTANCE_PREPARATION_ONLY", "binding:execution-prep", (PREP_A,), runtime=True, execution=True, runtime_requirements=("runtime-requirement:perception",), resource_classes=("resource-class:perception",), execution_classes=("execution-class:bounded-observation",)),
        _pipeline("NO_PROVIDER_SESSION_START", "binding:no-session", (PREP_A,), runtime=True, runtime_requirements=("runtime-requirement:perception",), execution_classes=("execution-class:bounded-observation",)),
        _pipeline("NO_GATEWAY_SUBMISSION", "binding:no-gateway", (PREP_A,), runtime=True, runtime_requirements=("runtime-requirement:perception",), execution_classes=("execution-class:bounded-observation",)),
        _pipeline("NO_PROVIDER_BINDING_CANDIDATE", "binding:none", ()),
        _postflight_case("NO_TRUTH", valid_artifact),
        _postflight_case("NO_WORLD_MUTATION", valid_artifact),
        _pipeline("REQUESTER_DOES_NOT_ALLOCATE_RESOURCES", "binding:requester-boundary", (PREP_A,)),
        _pipeline("RUNTIME_OWNS_RESOURCE_FAILURE", "binding:runtime-failure-owner", (PREP_A,)),
        _pipeline("AUTHORITY_RESPONSIBILITY_VALID", "binding:authority-valid", (PREP_A,)),
        _pipeline("BINDING_AUTHORITY_WITHOUT_RESPONSIBILITY_BLOCKED", "binding:authority-without-responsibility", (PREP_A,)),
        _pipeline("RESPONSIBILITY_WITHOUT_BINDING_AUTHORITY_BLOCKED", "binding:responsibility-without-authority", (PREP_A,)),
        _postflight_case("AUTHORITY_LAUNDERING_BLOCKED", {**valid_artifact, "authoritative_effects": ("provider_binding_decision",)}),
        _postflight_case("RESPONSIBILITY_LAUNDERING_BLOCKED", valid_artifact, failure={"authority_ref": "authority:provider-binding", "authority_owner_ref": "Provider Governance", "responsibility_ref": "responsibility:binding-failure", "failure_owner_ref": "Observation Demand", "laundered_as_upstream": True}),
        _pipeline("CANDIDATE_NOT_AUTHORITY", "binding:candidate-boundary", (PREP_A,)),
        _pipeline("GOVERNANCE_PREFLIGHT_REQUIRED", "binding:preflight", (PREP_A,)),
        _postflight_case("GOVERNANCE_POSTFLIGHT_REQUIRED", valid_artifact),
        replace(_pipeline("NO_APPLICABLE_RULES_FAIL_CLOSED", "binding:no-rules", (PREP_A,)), profile=replace(valid_profile(), domains=("UNRELATED_DOMAIN",), governance_profiles=("UNRELATED_PROFILE",))),
        _pipeline("DETERMINISTIC_REPLAY", "binding:deterministic", (PREP_A, PREP_B)),
        replace(
            _pipeline("MALFORMED_INPUT_FAIL_CLOSED", "binding:malformed", (PREP_A,)),
            request={},
            expected_binding_status="INVALID_INPUT",
            expected_binding_count=0,
        ),
        _pipeline("SCENARIO12_SIGNAGE", "binding:scenario12-signage", (PREP12_SIGNAGE,)),
        _pipeline("SCENARIO12_HUMAN_FLOW", "binding:scenario12-flow", (PREP12_FLOW,)),
        _pipeline("SCENARIO12_INDEPENDENT_BINDING_PATHS", "binding:scenario12-both", (PREP12_SIGNAGE, PREP12_FLOW)),
        _pipeline("UNIFIED_FINAL_DECISION_GO", "binding:final-go", (PREP_A,)),
        replace(_pipeline("GOVERNANCE_FAILURE_FORCES_NO_GO", "binding:final-no-go", (PREP_A,)), profile=replace(valid_profile(), domains=("UNRELATED_DOMAIN",), governance_profiles=("UNRELATED_PROFILE",))),
    ]
    finalized = []
    for case in cases:
        current = replace(
            case,
            profile=case.profile or valid_profile(),
            authority_records=case.authority_records or valid_authority_records(),
        )
        if case.case_id == "BINDING_AUTHORITY_WITHOUT_RESPONSIBILITY_BLOCKED":
            current = replace(
                current,
                authority_records=(
                    replace(
                        current.authority_records[0],
                        responsibility_refs=(),
                        authority_responsibility_map=(),
                        responsibility_owner_refs=(),
                    ),
                    current.authority_records[1],
                ),
            )
        elif case.case_id == "RESPONSIBILITY_WITHOUT_BINDING_AUTHORITY_BLOCKED":
            current = replace(
                current,
                authority_records=(
                    replace(
                        current.authority_records[0],
                        authority_refs=(),
                        responsibility_refs=("responsibility:orphan-binding",),
                        authority_responsibility_map=(),
                        responsibility_owner_refs=(
                            ("responsibility:orphan-binding", "Provider Governance"),
                        ),
                    ),
                    current.authority_records[1],
                ),
            )
        elif case.case_id in {
            "PROVIDER_NOT_ELIGIBLE",
            "PROVIDER_GOVERNANCE_OWNS_BINDING_FAILURE",
            "UPSTREAM_NOT_BLAMED_FOR_PROVIDER_FAILURE",
        }:
            failure_payload = {
                "authority_ref": "authority:provider-binding",
                "authority_owner_ref": "Provider Governance",
                "responsibility_ref": "responsibility:binding-failure",
                "failure_owner_ref": "Provider Governance",
            }
            if case.case_id == "PROVIDER_NOT_ELIGIBLE":
                failure_payload["provider_eligible"] = False
            current = replace(
                current,
                failure_ownership_payload=failure_payload,
                expected_owner="Provider Governance",
            )
        elif case.case_id in {"RUNTIME_OWNS_RESOURCE_FAILURE", "RUNTIME_REQUIREMENT_PREPARATION"}:
            current = replace(
                current,
                failure_ownership_payload={
                    "authority_ref": "authority:runtime-preparation",
                    "authority_owner_ref": "Runtime Executor",
                    "responsibility_ref": "responsibility:runtime-preparation",
                    "failure_owner_ref": "Runtime Executor",
                },
                expected_owner="Runtime Executor",
            )
        elif case.case_id == "REQUESTER_DOES_NOT_ALLOCATE_RESOURCES":
            current = replace(
                current,
                boundary_payload={"requester_allocates_resources": False},
            )
        elif case.case_id == "RESPONSIBILITY_LAUNDERING_BLOCKED":
            current = replace(
                current,
                expected_owner="Provider Governance",
            )
        finalized.append(current)
    return tuple(finalized)


def governance_registry_v1():
    return CORE_GOVERNANCE_RULE_REGISTRY_V1


__all__ = [
    "PHASE",
    "PROBLEM",
    "STATE",
    "PipelineCaseV1",
    "valid_profile",
    "valid_authority_records",
    "governance_registry_v1",
    "build_provider_binding_to_runtime_allocation_cases_v1",
]
