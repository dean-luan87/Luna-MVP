"""Synthetic fixtures for authoritative mechanical execution records."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Tuple

from capabilities.evaluation.perception_provider_runtime_target_preparation_controlled.fixtures_v1 import (
    PROBLEM,
    STATE,
    CONTEXT,
    COMPAT_A,
    COMPAT_B,
    COMPAT12_SIGNAGE,
    COMPAT12_FLOW,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_target_preparation_v1 import (
    GovernedProviderRuntimeTargetMappingV1,
)
from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    ARCHITECTURE_SOURCE_REF,
    CONSTITUTION_SOURCE_REF,
    GovernanceAuthorityResponsibilityRecordV1,
    PhaseGovernanceProfileV1,
    PROTOCOL_SOURCE_REF,
)


PHASE = "Phase-Provider-Binding-Runtime-Allocation-Execution-Instance-Controlled-Implementation-v1-001"
EVALUATION_MARKER = "controlled_provider_binding_runtime_allocation_execution_instance"
AUTH_BINDING = "authority:provider-binding-decision"
RESP_BINDING = "responsibility:provider-binding-decision"
AUTH_ALLOCATION = "authority:runtime-allocation"
RESP_ALLOCATION = "responsibility:runtime-allocation"
AUTH_INSTANCE = "authority:execution-instance-creation"
RESP_INSTANCE = "responsibility:execution-identity"


@dataclass(frozen=True)
class ExecutionCaseV1:
    case_id: str
    compatibility_candidates: Any = (COMPAT_A,)
    provider_mappings: Any = ()
    expected_preflight_status: str = "PASS"
    expected_binding_status: str = "PROVIDER_BINDING_DECISIONS_FORMED"
    expected_binding_count: int = 1
    expected_bound_count: int = 1
    expected_allocation_status: str = "RUNTIME_ALLOCATION_RECORDS_FORMED"
    expected_allocation_count: int = 1
    expected_allocated_count: int = 1
    expected_instance_status: str = "EXECUTION_INSTANCES_CREATED"
    expected_instance_count: int = 1
    permission_status: str = "ALLOWED"
    provider_binding_status: str = "ELIGIBLE"
    capability_admission_status: str = "ADMITTED"
    safety_status: str = "ALLOWED"
    constitution_status: str = "ALLOWED"
    resource_feasibility_status: str = "SATISFIABLE"
    grant_resource_feasibility_status: str | None = None
    allocation_outcome: str = "AUTO"
    runtime_boundary_status: str = "VALID"
    freshness_status: str = "FRESH"
    validity_status: str = "FRESH"
    execution_ready: bool = True
    provider_eligibility_status: str = "ELIGIBLE"
    binding_status: str = "BOUND"
    binding_validity_status: str = "FRESH"
    profile: Any = None
    authority_records: Any = None
    malformed_grant: bool = False
    no_instance: bool = False
    revoke_grant_before_instance: bool = False
    revoke_binding_before_instance: bool = False
    release_allocation: bool = False
    boundary_payload: Any = None
    failure_ownership_payload: Any = None
    postflight_artifact: Any = None


def valid_profile() -> PhaseGovernanceProfileV1:
    return PhaseGovernanceProfileV1(
        phase_ref=PHASE,
        phase_owner_ref="Runtime Executor",
        domains=("CONTROLLED_PHASE",),
        owners_touched=(
            "Provider Governance", "Permission / Admission Manager", "Runtime Executor",
            "Resource Governance", "FPO", "Observation Gateway", "Protocol Manager",
        ),
        governance_profiles=(
            "GOVERNED_EXECUTION", "AUTHORITY_RESPONSIBILITY", "READ_ONLY", "NO_TRUTH",
            "NO_WORLD_MUTATION", "NO_PROVIDER_INVOCATION", "NO_MODEL_INVOCATION",
            "NO_DECISION_ACTION_TASK", "REQUESTER_EXECUTOR_BOUNDARY", "ADAPTER_BOUNDARY",
        ),
        maturity_level="CONTROLLED_V1",
        runtime_level="NONE",
        # Mechanical authoritative records are allowed; runtime invocation is not.
        candidate_only=False,
        read_only=True,
        truth_authority=False,
        world_truth_authority=False,
        runtime_authority=False,
        authority_refs=(AUTH_BINDING, AUTH_ALLOCATION, AUTH_INSTANCE),
        responsibility_refs=(RESP_BINDING, RESP_ALLOCATION, RESP_INSTANCE),
        input_contract_refs=(
            "ProviderBindingCandidateV1", "RuntimeExecutionGrantDecisionV1",
            "RuntimeAllocationPreparationCandidateV1", "ExecutionInstancePreparationCandidateV1",
        ),
        output_contract_refs=("ProviderBindingDecisionV1", "RuntimeAllocationRecordV1", "ExecutionInstanceV1"),
        protocol_refs=(PROTOCOL_SOURCE_REF,),
        constitution_refs=(CONSTITUTION_SOURCE_REF,),
        context_refs=CONTEXT,
        trace_ref="trace:provider-binding-runtime-allocation-execution:governance",
        mechanical_authority=True,
    )


def valid_authority_records() -> Tuple[GovernanceAuthorityResponsibilityRecordV1, ...]:
    return (
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="provider-governance:binding-decision",
            owner_ref="Provider Governance",
            authority_refs=(AUTH_BINDING,), responsibility_refs=(RESP_BINDING,),
            decision_types=("provider_binding_decision",), failure_types=("provider_binding_failure",),
            authority_responsibility_map=((AUTH_BINDING, RESP_BINDING),),
            responsibility_owner_refs=((RESP_BINDING, "Provider Governance"),),
            operational_authority=True, candidate_only=False,
        ),
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="runtime-executor:allocation",
            owner_ref="Runtime Executor",
            authority_refs=(AUTH_ALLOCATION,), responsibility_refs=(RESP_ALLOCATION,),
            decision_types=("runtime_allocation_decision",), failure_types=("allocation_failure",),
            authority_responsibility_map=((AUTH_ALLOCATION, RESP_ALLOCATION),),
            responsibility_owner_refs=((RESP_ALLOCATION, "Runtime Executor"),),
            operational_authority=True, runtime_authority=True, candidate_only=False,
        ),
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="runtime-executor:execution-identity",
            owner_ref="Runtime Executor",
            authority_refs=(AUTH_INSTANCE,), responsibility_refs=(RESP_INSTANCE,),
            decision_types=("execution_instance_creation",), failure_types=("execution_identity_failure",),
            authority_responsibility_map=((AUTH_INSTANCE, RESP_INSTANCE),),
            responsibility_owner_refs=((RESP_INSTANCE, "Runtime Executor"),),
            operational_authority=True, runtime_authority=True, candidate_only=False,
        ),
    )


def _mapping(
    compatibility: Any,
    provider_ref: str,
    *,
    suffix: str = "a",
    model_ref: str | None = None,
) -> GovernedProviderRuntimeTargetMappingV1:
    return GovernedProviderRuntimeTargetMappingV1(
        mapping_ref=f"mapping:{compatibility.admission_compatibility_candidate_ref}:{suffix}",
        source_admission_compatibility_candidate_ref=compatibility.admission_compatibility_candidate_ref,
        capability_class_ref=compatibility.capability_class_ref,
        provider_candidate_ref=provider_ref,
        provider_class_ref="provider-class:controlled:perception",
        provider_mapping_basis_refs=("governed:controlled:capability-provider-mapping",),
        provider_admission_refs=(f"provider-admission:{provider_ref}",),
        provider_availability_refs=(f"provider-availability:{provider_ref}",),
        availability_status="AVAILABLE",
        admission_status="ADMITTED",
        eligible=True,
        source_model_ref=model_ref,
    )


def _default_mappings(compatibilities: Any) -> Any:
    if not isinstance(compatibilities, tuple):
        return ()
    return tuple(
        _mapping(item, f"provider:controlled:{index}")
        for index, item in enumerate(compatibilities, start=1)
    )


def _case(case_id: str, compatibilities: Any = (COMPAT_A,), mappings: Any = None, **kwargs: Any) -> ExecutionCaseV1:
    return ExecutionCaseV1(
        case_id=case_id,
        compatibility_candidates=compatibilities,
        provider_mappings=_default_mappings(compatibilities) if mappings is None else mappings,
        profile=kwargs.pop("profile", valid_profile()),
        authority_records=kwargs.pop("authority_records", valid_authority_records()), **kwargs,
    )


def build_provider_binding_runtime_allocation_execution_cases_v1() -> Tuple[ExecutionCaseV1, ...]:
    invalid_profile = replace(valid_profile(), governance_profiles=())
    invalid_records = replace(valid_authority_records()[0], authority_responsibility_map=())
    model_mapping = (_mapping(COMPAT_A, "provider:controlled:model", model_ref="model:controlled:explicit"),)
    cases = [
        _case("PROVIDER_ONLY_BINDING_BOUND"),
        _case("MODEL_REF_CARRY_FORWARD_BINDING", compatibilities=(COMPAT_A,), mappings=model_mapping),
        _case("MODEL_NOT_INFERRED"),
        _case("PROVIDER_BINDING_DENIED", provider_eligibility_status="DENIED", expected_binding_count=1, expected_bound_count=0, expected_allocation_status="INVALID_INPUT", expected_allocation_count=0, expected_allocated_count=0, expected_instance_status="INVALID_INPUT", expected_instance_count=0),
        _case("PROVIDER_BINDING_REVOKED", binding_status="REVOKED", binding_validity_status="REVOKED", expected_bound_count=0, expected_allocation_status="INVALID_INPUT", expected_allocation_count=0, expected_allocated_count=0, expected_instance_status="INVALID_INPUT", expected_instance_count=0),
        _case("VALID_GRANT_REQUIRED"),
        _case("DENIED_GRANT_BLOCKS_ALLOCATION", permission_status="DENIED", expected_binding_status="NO_PROVIDER_BINDING_DECISION", expected_binding_count=0, expected_bound_count=0, expected_allocation_status="NO_RUNTIME_ALLOCATION_RECORD", expected_allocation_count=0, expected_allocated_count=0, expected_instance_status="NO_EXECUTION_INSTANCE", expected_instance_count=0),
        _case("EXPIRED_GRANT_BLOCKS_ALLOCATION", validity_status="EXPIRED", expected_binding_status="NO_PROVIDER_BINDING_DECISION", expected_binding_count=0, expected_bound_count=0, expected_allocation_status="NO_RUNTIME_ALLOCATION_RECORD", expected_allocation_count=0, expected_allocated_count=0, expected_instance_status="NO_EXECUTION_INSTANCE", expected_instance_count=0),
        _case("REVOKED_GRANT_BLOCKS_ALLOCATION", validity_status="REVOKED", expected_binding_status="NO_PROVIDER_BINDING_DECISION", expected_binding_count=0, expected_bound_count=0, expected_allocation_status="NO_RUNTIME_ALLOCATION_RECORD", expected_allocation_count=0, expected_allocated_count=0, expected_instance_status="NO_EXECUTION_INSTANCE", expected_instance_count=0),
        _case("STALE_GRANT_BLOCKS_ALLOCATION", freshness_status="STALE", expected_binding_status="NO_PROVIDER_BINDING_DECISION", expected_binding_count=0, expected_bound_count=0, expected_allocation_status="NO_RUNTIME_ALLOCATION_RECORD", expected_allocation_count=0, expected_allocated_count=0, expected_instance_status="NO_EXECUTION_INSTANCE", expected_instance_count=0),
        _case("RESOURCE_FEASIBLE"),
        _case("RESOURCE_UNAVAILABLE", resource_feasibility_status="UNAVAILABLE", expected_allocation_count=1, expected_allocated_count=0, expected_instance_status="INVALID_INPUT", expected_instance_count=0),
        _case("FEASIBILITY_NOT_EQUAL_ALLOCATION"),
        _case("AUTHORITATIVE_ALLOCATION"),
        _case("ALLOCATION_DENIED", allocation_outcome="DENIED", expected_allocated_count=0, expected_instance_status="INVALID_INPUT", expected_instance_count=0),
        _case("ALLOCATION_FAILED", allocation_outcome="FAILED", expected_allocated_count=0, expected_instance_status="INVALID_INPUT", expected_instance_count=0),
        _case("ALLOCATION_RELEASED", release_allocation=True, expected_allocated_count=0, expected_instance_status="INVALID_INPUT", expected_instance_count=0),
        _case("REQUESTER_DOES_NOT_CHOOSE_GPU"),
        _case("REQUESTER_DOES_NOT_CHOOSE_WORKER"),
        _case("EXECUTOR_OWNS_ALLOCATION_IDENTITY"),
        _case("EXECUTION_INSTANCE_CREATED"),
        _case("EXECUTION_INSTANCE_UNIQUE", compatibilities=(COMPAT_A, COMPAT_B), expected_binding_count=2, expected_bound_count=2, expected_allocation_count=2, expected_allocated_count=2, expected_instance_count=2),
        _case("EXECUTION_INSTANCE_DETERMINISTIC"),
        _case("CREATED_NOT_STARTED"),
        _case("NO_PROVIDER_SESSION"),
        _case("NO_PROVIDER_INVOCATION"),
        _case("NO_MODEL_INVOCATION"),
        _case("NO_GATEWAY"),
        _case("NO_OBSERVATION"),
        _case("NO_EVIDENCE"),
        _case("NO_WORLD_TRUTH"),
        _case("BINDING_AUTHORITY_RESPONSIBILITY_VALID"),
        _case("ALLOCATION_AUTHORITY_RESPONSIBILITY_VALID"),
        _case("EXECUTION_AUTHORITY_RESPONSIBILITY_VALID"),
        _case("AUTHORITY_WITHOUT_RESPONSIBILITY_BLOCKED", expected_preflight_status="GOVERNANCE_PREFLIGHT_BLOCKED", authority_records=(invalid_records,)),
        _case("RESPONSIBILITY_WITHOUT_AUTHORITY_BLOCKED", expected_preflight_status="GOVERNANCE_PREFLIGHT_BLOCKED", authority_records=(replace(valid_authority_records()[0], responsibility_refs=(RESP_BINDING, "responsibility:orphan")),)),
        _case("FAILURE_OWNER_PROVIDER", provider_eligibility_status="DENIED", expected_bound_count=0, expected_allocation_status="INVALID_INPUT", expected_allocation_count=0, expected_allocated_count=0, expected_instance_status="INVALID_INPUT", expected_instance_count=0),
        _case("FAILURE_OWNER_PERMISSION", permission_status="DENIED", expected_binding_status="NO_PROVIDER_BINDING_DECISION", expected_binding_count=0, expected_bound_count=0, expected_allocation_status="NO_RUNTIME_ALLOCATION_RECORD", expected_allocation_count=0, expected_allocated_count=0, expected_instance_status="NO_EXECUTION_INSTANCE", expected_instance_count=0),
        _case("FAILURE_OWNER_RESOURCE", resource_feasibility_status="UNAVAILABLE", expected_allocated_count=0, expected_instance_status="INVALID_INPUT", expected_instance_count=0),
        _case("FAILURE_OWNER_RUNTIME", runtime_boundary_status="INVALID", expected_binding_status="NO_PROVIDER_BINDING_DECISION", expected_binding_count=0, expected_bound_count=0, expected_allocation_status="NO_RUNTIME_ALLOCATION_RECORD", expected_allocation_count=0, expected_allocated_count=0, expected_instance_status="NO_EXECUTION_INSTANCE", expected_instance_count=0),
        _case("LINEAGE_MATCH"),
        _case("LINEAGE_MISMATCH_BLOCKED", compatibilities=(replace(COMPAT_A, parent_cognitive_problem_ref="problem:other"),), expected_binding_status="NO_PROVIDER_BINDING_DECISION", expected_binding_count=0, expected_bound_count=0, expected_allocation_status="NO_RUNTIME_ALLOCATION_RECORD", expected_allocation_count=0, expected_allocated_count=0, expected_instance_status="NO_EXECUTION_INSTANCE", expected_instance_count=0),
        _case("SAME_PROVIDER_MULTI_DEMAND", compatibilities=(COMPAT_A, COMPAT_B), mappings=(_mapping(COMPAT_A, "provider:controlled:shared"), _mapping(COMPAT_B, "provider:controlled:shared")), expected_binding_count=2, expected_bound_count=2, expected_allocation_count=2, expected_allocated_count=2, expected_instance_count=2),
        _case("MULTIPLE_PROVIDER_DISTINCT_BINDINGS", compatibilities=(COMPAT_A, COMPAT_B), expected_binding_count=2, expected_bound_count=2, expected_allocation_count=2, expected_allocated_count=2, expected_instance_count=2),
        _case("PROVIDER_ONLY_EXECUTION_INSTANCE"),
        _case("EXPLICIT_MODEL_EXECUTION_INSTANCE", compatibilities=(COMPAT_A,), mappings=model_mapping),
        _case("GRANT_RECHECK_BEFORE_INSTANCE", revoke_grant_before_instance=True, expected_instance_status="INVALID_INPUT", expected_instance_count=0),
        _case("BINDING_REVOKED_BEFORE_INSTANCE", revoke_binding_before_instance=True, expected_allocation_status="RUNTIME_ALLOCATION_RECORDS_FORMED", expected_allocation_count=1, expected_allocated_count=1, expected_instance_status="INVALID_INPUT", expected_instance_count=0),
        _case("ALLOCATION_REQUIRED_BEFORE_INSTANCE", no_instance=True, expected_instance_status="NO_EXECUTION_INSTANCE", expected_instance_count=0),
        _case("EXECUTION_READY_NOT_EXECUTED"),
        _case("GOVERNANCE_PREFLIGHT_REQUIRED"),
        _case("GOVERNANCE_POSTFLIGHT_REQUIRED"),
        _case("NO_APPLICABLE_RULES_FAIL_CLOSED", profile=invalid_profile, expected_binding_status="NO_PROVIDER_BINDING_DECISION", expected_binding_count=0, expected_bound_count=0, expected_allocation_status="NO_RUNTIME_ALLOCATION_RECORD", expected_allocation_count=0, expected_allocated_count=0, expected_instance_status="NO_EXECUTION_INSTANCE", expected_instance_count=0),
        _case("MALFORMED_INPUT_FAIL_CLOSED", compatibilities=COMPAT_A, expected_binding_status="NO_PROVIDER_BINDING_DECISION", expected_binding_count=0, expected_bound_count=0, expected_allocation_status="NO_RUNTIME_ALLOCATION_RECORD", expected_allocation_count=0, expected_allocated_count=0, expected_instance_status="NO_EXECUTION_INSTANCE", expected_instance_count=0),
        _case("SCENARIO12_SIGNAGE", compatibilities=(COMPAT12_SIGNAGE,), mappings=(_mapping(COMPAT12_SIGNAGE, "provider:controlled:scenario12:signage"),)),
        _case("SCENARIO12_HUMAN_FLOW", compatibilities=(COMPAT12_FLOW,), mappings=(_mapping(COMPAT12_FLOW, "provider:controlled:scenario12:flow"),)),
        _case("SCENARIO12_INDEPENDENT_BINDING_PATHS", compatibilities=(COMPAT12_SIGNAGE, COMPAT12_FLOW), mappings=(_mapping(COMPAT12_SIGNAGE, "provider:controlled:scenario12:signage"), _mapping(COMPAT12_FLOW, "provider:controlled:scenario12:flow")), expected_binding_count=2, expected_bound_count=2, expected_allocation_count=2, expected_allocated_count=2, expected_instance_count=2),
        _case("DETERMINISTIC_REPLAY"),
    ]
    return tuple(cases)


__all__ = ["PHASE", "EVALUATION_MARKER", "ExecutionCaseV1", "valid_profile", "valid_authority_records", "build_provider_binding_runtime_allocation_execution_cases_v1"]
