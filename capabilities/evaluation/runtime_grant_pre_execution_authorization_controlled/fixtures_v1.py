"""Synthetic fixtures for the Runtime Grant authorization boundary."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Dict, Tuple

from capabilities.midplatform.core.runtime_executor.runtime_allocation_preparation_candidate_v1 import (
    RuntimeAllocationPreparationCandidateV1,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    AUTHORITY_REF,
    OWNER,
    RESPONSIBILITY_REF,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_runtime_preparation_v1 import (
    ProviderBindingRuntimePreparationInputV1,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_target_preparation_v1 import (
    ProviderRuntimeTargetPreparationCandidateV1,
)
from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    ARCHITECTURE_SOURCE_REF,
    CONSTITUTION_SOURCE_REF,
    GovernanceAuthorityResponsibilityRecordV1,
    PhaseGovernanceProfileV1,
    PROTOCOL_SOURCE_REF,
)
from capabilities.evaluation.provider_binding_runtime_preparation_responsibility_controlled.fixtures_v1 import (
    PROBLEM,
    STATE,
    CONTEXT,
    TARGET_A,
    TARGET12_FLOW,
    TARGET12_SIGNAGE,
)


PHASE = "Phase-Runtime-Grant-PreExecution-Authorization-Controlled-Implementation-v1-001"
EVALUATION_MARKER = "controlled_runtime_grant_pre_execution_authorization"


@dataclass(frozen=True)
class RuntimeGrantCaseV1:
    case_id: str
    target_candidates: Any
    expected_status: str
    expected_decision: str | None
    expected_count: int
    permission_status: str = "ALLOWED"
    provider_binding_status: str = "ELIGIBLE"
    capability_admission_status: str = "ADMITTED"
    safety_status: str = "ALLOWED"
    constitution_status: str = "ALLOWED"
    resource_feasibility_status: str = "SATISFIABLE"
    runtime_boundary_status: str = "VALID"
    freshness_status: str = "FRESH"
    validity_status: str = "FRESH"
    execution_ready: bool = True
    profile: Any = None
    authority_records: Any = None
    boundary_payload: Any = None
    failure_ownership_payload: Any = None
    postflight_artifact: Any = None
    malformed_grant_input: bool = False
    fpo_continuation_status: str = "CONTINUE"
    gateway_admission_status: str = "NOT_REQUESTED"
    grant_authority_ref: str = AUTHORITY_REF
    grant_responsibility_ref: str = RESPONSIBILITY_REF


def valid_profile() -> PhaseGovernanceProfileV1:
    return PhaseGovernanceProfileV1(
        phase_ref=PHASE,
        phase_owner_ref=OWNER,
        domains=("CONTROLLED_PHASE",),
        owners_touched=(
            OWNER,
            "Provider Governance",
            "Runtime Executor",
            "Resource Governance",
            "Safety Governance",
            "Protocol Manager",
            "FPO",
            "Observation Gateway",
        ),
        governance_profiles=(
            "GOVERNED_EXECUTION",
            "AUTHORITY_RESPONSIBILITY",
            "READ_ONLY",
            "NO_TRUTH",
            "NO_WORLD_MUTATION",
            "NO_RUNTIME",
            "NO_PROVIDER_INVOCATION",
            "NO_MODEL_INVOCATION",
            "NO_DECISION_ACTION_TASK",
            "REQUESTER_EXECUTOR_BOUNDARY",
        ),
        maturity_level="CONTROLLED_V1",
        runtime_level="NONE",
        # This phase deliberately contains an authoritative permission
        # decision, while remaining non-runtime and non-mutating.
        candidate_only=False,
        read_only=True,
        truth_authority=False,
        world_truth_authority=False,
        runtime_authority=False,
        authority_refs=(AUTHORITY_REF,),
        responsibility_refs=(RESPONSIBILITY_REF,),
        input_contract_refs=(
            "ProviderBindingCandidateV1",
            "RuntimeAllocationPreparationCandidateV1",
            "ExecutionInstancePreparationCandidateV1",
            "RuntimeExecutionGrantInputV1",
        ),
        output_contract_refs=("RuntimeExecutionGrantDecisionV1",),
        protocol_refs=(PROTOCOL_SOURCE_REF,),
        constitution_refs=(CONSTITUTION_SOURCE_REF,),
        context_refs=CONTEXT,
        trace_ref="trace:runtime-grant:governance",
    )


def valid_authority_records() -> Tuple[GovernanceAuthorityResponsibilityRecordV1, ...]:
    return (
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="permission-admission:runtime-execution-grant",
            owner_ref=OWNER,
            authority_refs=(AUTHORITY_REF,),
            responsibility_refs=(RESPONSIBILITY_REF,),
            decision_types=("runtime_execution_grant_decision",),
            failure_types=("runtime_execution_grant_decision_failure",),
            authority_responsibility_map=((AUTHORITY_REF, RESPONSIBILITY_REF),),
            responsibility_owner_refs=((RESPONSIBILITY_REF, OWNER),),
            admission_authority=True,
            candidate_only=False,
        ),
    )


def _target_request(case_id: str, candidates: Any) -> ProviderBindingRuntimePreparationInputV1:
    return ProviderBindingRuntimePreparationInputV1(
        preparation_ref=f"grant-target:{case_id.lower()}",
        parent_cognitive_problem_ref=PROBLEM,
        source_state_ref=STATE,
        provider_target_candidates=candidates,
        context_refs=CONTEXT,
        trace_ref=f"trace:grant-target:{case_id.lower()}",
        provenance_refs=(f"provenance:grant-target:{case_id.lower()}",),
    )


def _case(
    case_id: str,
    candidates: Any = (TARGET_A,),
    *,
    expected_status: str = "RUNTIME_EXECUTION_GRANTS_FORMED",
    expected_decision: str | None = "GRANTED",
    expected_count: int = 1,
    **kwargs: Any,
) -> RuntimeGrantCaseV1:
    return RuntimeGrantCaseV1(
        case_id=case_id,
        target_candidates=candidates,
        expected_status=expected_status,
        expected_decision=expected_decision,
        expected_count=expected_count,
        profile=kwargs.pop("profile", valid_profile()),
        authority_records=kwargs.pop("authority_records", valid_authority_records()),
        **kwargs,
    )


def build_runtime_grant_cases_v1() -> Tuple[RuntimeGrantCaseV1, ...]:
    invalid_record = replace(valid_authority_records()[0], authority_responsibility_map=())
    orphan_record = replace(
        valid_authority_records()[0],
        responsibility_refs=(RESPONSIBILITY_REF, "responsibility:orphan"),
    )
    no_rules_profile = replace(valid_profile(), governance_profiles=())
    invalid_target = replace(TARGET_A, candidate_only=False)
    stale = _case("STALE_GRANT_BLOCKED", freshness_status="STALE", expected_decision="DENIED")
    return (
        _case("COMPLETE_REQUEST_READY_FOR_AUTHORIZATION"),
        _case("INCOMPLETE_REQUEST_BLOCKED", runtime_boundary_status="INVALID", expected_decision="DENIED"),
        _case("PROVIDER_BINDING_REQUIRED", provider_binding_status="NOT_ADMITTED", expected_decision="DENIED"),
        _case("PROVIDER_BINDING_DENIED", provider_binding_status="DENIED", expected_decision="DENIED"),
        _case("PERMISSION_ALLOWED"),
        _case("PERMISSION_DENIED", permission_status="DENIED", expected_decision="DENIED"),
        _case("PERMISSION_DEFERRED", permission_status="DEFERRED", expected_decision="DEFERRED"),
        _case("SAFETY_ALLOWED"),
        _case("SAFETY_DENIED", safety_status="DENIED", expected_decision="DENIED"),
        _case("CONSTITUTION_BLOCKS_EXECUTION", constitution_status="BLOCKED", expected_decision="DENIED"),
        _case("RUNTIME_BOUNDARY_VALID"),
        _case("RUNTIME_BOUNDARY_INVALID", runtime_boundary_status="INVALID", expected_decision="DENIED"),
        _case("EXECUTION_READY_NOT_AUTHORIZED", execution_ready=False, expected_decision="DENIED"),
        _case("AUTHORIZED_NOT_EXECUTED"),
        _case("GRANT_WITHOUT_AUTHORITY_BLOCKED", grant_authority_ref="", expected_status="INVALID_INPUT", expected_decision=None, expected_count=0),
        _case("AUTHORITY_WITHOUT_RESPONSIBILITY_BLOCKED", authority_records=(invalid_record,), expected_status="INVALID_INPUT", expected_decision=None, expected_count=0),
        _case("RESPONSIBILITY_WITHOUT_AUTHORITY_BLOCKED", authority_records=(orphan_record,), expected_status="INVALID_INPUT", expected_decision=None, expected_count=0),
        _case("AUTHORITY_LAUNDERING_BLOCKED", postflight_artifact={"authoritative_effects": ("unowned_execution_approval",)}),
        _case("RESPONSIBILITY_LAUNDERING_BLOCKED", failure_ownership_payload={"authority_ref": AUTHORITY_REF, "responsibility_ref": RESPONSIBILITY_REF, "authority_owner_ref": OWNER, "failure_owner_ref": OWNER, "laundered_as_upstream": True}),
        stale,
        _case("EXPIRED_GRANT_BLOCKED", validity_status="EXPIRED", expected_decision="DENIED"),
        _case("REVOKED_GRANT_BLOCKED", validity_status="REVOKED", expected_decision="REVOKED"),
        _case("RESOURCE_AVAILABLE_NOT_EQUAL_GRANT", permission_status="DENIED", resource_feasibility_status="SATISFIABLE", expected_decision="DENIED"),
        _case("GRANT_NOT_EQUAL_RESOURCE_ALLOCATION"),
        _case("PROVIDER_BINDING_NOT_EQUAL_GRANT", permission_status="DENIED", expected_decision="DENIED"),
        _case("CAPABILITY_ADMITTED_NOT_AUTO_GRANT", capability_admission_status="ADMITTED", permission_status="DENIED", expected_decision="DENIED"),
        _case("FPO_CONTINUATION_NOT_EQUAL_GRANT", permission_status="DENIED", fpo_continuation_status="CONTINUE", expected_decision="DENIED"),
        _case("GATEWAY_ADMISSION_NOT_EQUAL_GRANT", gateway_admission_status="NOT_ADMITTED"),
        _case("NO_PROVIDER_SELECTION"),
        _case("NO_MODEL_SELECTION"),
        _case("NO_SEMANTIC_REWRITE"),
        _case("NO_RESOURCE_ALLOCATION"),
        _case("NO_EXECUTION_INSTANCE_CREATION"),
        _case("NO_PROVIDER_SESSION_START"),
        _case("NO_GATEWAY_SUBMISSION"),
        _case("FAILURE_OWNER_PERMISSION", permission_status="DENIED", expected_decision="DENIED"),
        _case("FAILURE_OWNER_PROVIDER", provider_binding_status="DENIED", expected_decision="DENIED"),
        _case("FAILURE_OWNER_RUNTIME_GRANT", permission_status="DENIED", expected_decision="DENIED"),
        _case("FAILURE_OWNER_RESOURCE", resource_feasibility_status="UNAVAILABLE", expected_decision="DENIED"),
        _case("GOVERNANCE_PREFLIGHT_REQUIRED"),
        _case("GOVERNANCE_POSTFLIGHT_REQUIRED"),
        _case("NO_APPLICABLE_RULES_FAIL_CLOSED", profile=no_rules_profile, expected_status="INVALID_INPUT", expected_decision=None, expected_count=0),
        _case("DETERMINISTIC_DECISION", candidates=(TARGET_A,), expected_count=1),
        _case("MALFORMED_INPUT_FAIL_CLOSED", candidates=TARGET_A, expected_status="INVALID_INPUT", expected_decision=None, expected_count=0),
        _case("SCENARIO12_SIGNAGE", candidates=(TARGET12_SIGNAGE,)),
        _case("SCENARIO12_HUMAN_FLOW", candidates=(TARGET12_FLOW,)),
        _case("SCENARIO12_BOTH", candidates=(TARGET12_SIGNAGE, TARGET12_FLOW), expected_count=2),
    )


__all__ = [
    "PHASE",
    "EVALUATION_MARKER",
    "RuntimeGrantCaseV1",
    "build_runtime_grant_cases_v1",
]
