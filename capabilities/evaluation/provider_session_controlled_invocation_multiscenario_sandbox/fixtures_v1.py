"""Multi-scenario fixtures for the controlled Provider session boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    ARCHITECTURE_SOURCE_REF,
    CONSTITUTION_SOURCE_REF,
    GovernanceAuthorityResponsibilityRecordV1,
    PhaseGovernanceProfileV1,
    PROTOCOL_SOURCE_REF,
)


PHASE = "Phase-Provider-Session-Controlled-Invocation-MultiScenario-Sandbox-v1-001"
EVALUATION_MARKER = "CONTROLLED_PROVIDER_SESSION_INVOCATION_MULTISCENARIO_SANDBOX"
OWNER = "Provider Runtime Governance"
AUTH_SESSION = "authority:provider-runtime-session-lifecycle"
RESP_SESSION = "responsibility:provider-runtime-session-lifecycle"
AUTH_INVOCATION = "authority:controlled-provider-invocation"
RESP_INVOCATION = "responsibility:controlled-provider-invocation"
PROBLEM = "problem:controlled:provider-session"
STATE = "state:controlled:provider-session"
CONTEXT = ("context:controlled:provider-session",)


@dataclass(frozen=True)
class SessionCaseV1:
    case_id: str
    source_case_id: str = "PROVIDER_ONLY_BINDING_BOUND"
    outcome: str = "COMPLETED"
    invoke: bool = True
    expected_session_status: str = "PROVIDER_RUNTIME_SESSION_CREATED"
    expected_invocation_status: str = "PROVIDER_INVOCATION_COMPLETED"
    grant_status: Optional[str] = None
    grant_validity_status: Optional[str] = None
    binding_status: Optional[str] = None
    binding_validity_status: Optional[str] = None
    allocation_status: Optional[str] = None
    instance_state: Optional[str] = None
    invocation_grant_status: Optional[str] = None
    invocation_binding_status: Optional[str] = None
    invocation_allocation_status: Optional[str] = None
    invocation_instance_state: Optional[str] = None
    lineage_mismatch: bool = False
    malformed_session: bool = False
    malformed_invocation: bool = False
    duplicate_start: bool = False
    expected_session_count: int = 1
    expected_invocation_count: int = 1
    expected_blocked: bool = False
    authority_records: Optional[Tuple[GovernanceAuthorityResponsibilityRecordV1, ...]] = None


def valid_profile() -> PhaseGovernanceProfileV1:
    return PhaseGovernanceProfileV1(
        phase_ref=PHASE,
        phase_owner_ref=OWNER,
        domains=("CONTROLLED_PHASE",),
        owners_touched=(
            "Provider Runtime Governance", "Runtime Executor", "Permission / Admission Manager",
            "Provider Governance", "FPO", "Observation Gateway", "Protocol Manager",
        ),
        governance_profiles=(
            "GOVERNED_EXECUTION", "AUTHORITY_RESPONSIBILITY", "READ_ONLY", "NO_TRUTH",
            "NO_WORLD_MUTATION", "NO_RUNTIME", "NO_PROVIDER_INVOCATION", "NO_MODEL_INVOCATION",
            "NO_DECISION_ACTION_TASK", "REQUESTER_EXECUTOR_BOUNDARY", "ADAPTER_BOUNDARY",
        ),
        maturity_level="CONTROLLED_V1",
        runtime_level="NONE",
        candidate_only=False,
        read_only=True,
        truth_authority=False,
        world_truth_authority=False,
        runtime_authority=False,
        authority_refs=(AUTH_SESSION, AUTH_INVOCATION),
        responsibility_refs=(RESP_SESSION, RESP_INVOCATION),
        input_contract_refs=(
            "ProviderBindingDecisionV1", "RuntimeExecutionGrantDecisionV1",
            "RuntimeAllocationRecordV1", "ExecutionInstanceV1",
        ),
        output_contract_refs=("ProviderRuntimeSessionV1", "ProviderInvocationRecordV1"),
        protocol_refs=(PROTOCOL_SOURCE_REF,),
        constitution_refs=(CONSTITUTION_SOURCE_REF,),
        context_refs=CONTEXT,
        trace_ref="trace:provider-session:governance",
        mechanical_authority=True,
    )


def valid_authority_records() -> Tuple[GovernanceAuthorityResponsibilityRecordV1, ...]:
    return (
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="provider-runtime-governance:session",
            owner_ref=OWNER,
            authority_refs=(AUTH_SESSION,),
            responsibility_refs=(RESP_SESSION,),
            decision_types=("provider_runtime_session_lifecycle",),
            failure_types=("provider_runtime_session_failure",),
            authority_responsibility_map=((AUTH_SESSION, RESP_SESSION),),
            responsibility_owner_refs=((RESP_SESSION, OWNER),),
            operational_authority=True,
            candidate_only=False,
        ),
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="provider-runtime-governance:invocation",
            owner_ref=OWNER,
            authority_refs=(AUTH_INVOCATION,),
            responsibility_refs=(RESP_INVOCATION,),
            decision_types=("controlled_provider_invocation",),
            failure_types=("provider_invocation_failure",),
            authority_responsibility_map=((AUTH_INVOCATION, RESP_INVOCATION),),
            responsibility_owner_refs=((RESP_INVOCATION, OWNER),),
            operational_authority=True,
            candidate_only=False,
        ),
    )


def build_provider_session_cases_v1() -> Tuple[SessionCaseV1, ...]:
    blocked_records = (
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="provider-runtime-governance:session-invalid",
            owner_ref=OWNER,
            authority_refs=(AUTH_SESSION,),
            responsibility_refs=(),
            decision_types=("provider_runtime_session_lifecycle",),
            failure_types=("provider_runtime_session_failure",),
            authority_responsibility_map=(),
            candidate_only=False,
        ),
    )
    responsibility_only_records = (
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="provider-runtime-governance:invocation-invalid",
            owner_ref=OWNER,
            authority_refs=(),
            responsibility_refs=(RESP_INVOCATION,),
            decision_types=("controlled_provider_invocation",),
            failure_types=("provider_invocation_failure",),
            authority_responsibility_map=(),
            responsibility_owner_refs=((RESP_INVOCATION, OWNER),),
            candidate_only=False,
        ),
    )
    cases = (
        SessionCaseV1("SESSION_CREATED_FROM_VALID_INSTANCE", invoke=False, expected_invocation_status="NO_INVOCATION", expected_invocation_count=0),
        SessionCaseV1("SESSION_REQUIRES_BOUND_PROVIDER", binding_status="DENIED", expected_session_status="INVALID_INPUT", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("SESSION_REQUIRES_FRESH_GRANT", grant_validity_status="STALE", expected_session_status="INVALID_INPUT", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("SESSION_REQUIRES_ALLOCATED_RUNTIME", allocation_status="RELEASED", expected_session_status="INVALID_INPUT", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("SESSION_REQUIRES_VALID_INSTANCE", instance_state="FAILED", expected_session_status="INVALID_INPUT", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("PROVIDER_ONLY_SESSION_MODEL_NULL", invoke=False, expected_invocation_status="NO_INVOCATION", expected_invocation_count=0),
        SessionCaseV1("MODEL_REF_CARRY_FORWARD", source_case_id="MODEL_REF_CARRY_FORWARD_BINDING", invoke=False, expected_invocation_status="NO_INVOCATION", expected_invocation_count=0),
        SessionCaseV1("MODEL_NOT_INFERRED", invoke=False, expected_invocation_status="NO_INVOCATION", expected_invocation_count=0),
        SessionCaseV1("INVOCATION_STARTED", outcome="COMPLETED"),
        SessionCaseV1("CREATED_NOT_STARTED", invoke=False, expected_invocation_status="NO_INVOCATION", expected_invocation_count=0),
        SessionCaseV1("SESSION_CREATED_NOT_INVOKED", invoke=False, expected_invocation_status="NO_INVOCATION", expected_invocation_count=0),
        SessionCaseV1("INVOCATION_COMPLETED", outcome="COMPLETED"),
        SessionCaseV1("INVOCATION_FAILED", outcome="FAILED", expected_invocation_status="PROVIDER_INVOCATION_FAILED"),
        SessionCaseV1("INVOCATION_TIMED_OUT", outcome="TIMED_OUT", expected_invocation_status="PROVIDER_INVOCATION_TIMED_OUT"),
        SessionCaseV1("INVOCATION_STOPPED", outcome="STOPPED", expected_invocation_status="PROVIDER_INVOCATION_STOPPED"),
        SessionCaseV1("INVOCATION_REVOKED", outcome="REVOKED", expected_invocation_status="PROVIDER_INVOCATION_REVOKED"),
        SessionCaseV1("GRANT_DENIED_BLOCKS_SESSION", grant_status="DENIED", expected_session_status="INVALID_INPUT", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("GRANT_STALE_BLOCKS_SESSION", grant_validity_status="STALE", expected_session_status="INVALID_INPUT", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("GRANT_EXPIRED_BLOCKS_SESSION", grant_validity_status="EXPIRED", expected_session_status="INVALID_INPUT", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("GRANT_REVOKED_BLOCKS_SESSION", grant_status="REVOKED", grant_validity_status="REVOKED", expected_session_status="INVALID_INPUT", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("GRANT_REVOKED_BEFORE_INVOCATION", invocation_grant_status="REVOKED", expected_invocation_status="INVALID_INPUT", expected_invocation_count=0),
        SessionCaseV1("BINDING_REVOKED_BLOCKS_START", invocation_binding_status="REVOKED", expected_invocation_status="INVALID_INPUT", expected_invocation_count=0),
        SessionCaseV1("ALLOCATION_RELEASED_BLOCKS_START", invocation_allocation_status="RELEASED", expected_invocation_status="INVALID_INPUT", expected_invocation_count=0),
        SessionCaseV1("INSTANCE_REVOKED_BLOCKS_SESSION", instance_state="REVOKED", expected_session_status="INVALID_INPUT", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("INSTANCE_FAILED_BLOCKS_SESSION", instance_state="FAILED", expected_session_status="INVALID_INPUT", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("LINEAGE_MATCH", invoke=False, expected_invocation_status="NO_INVOCATION", expected_invocation_count=0),
        SessionCaseV1("LINEAGE_MISMATCH_BLOCKED", lineage_mismatch=True, expected_session_status="INVALID_INPUT", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("DUPLICATE_START_BLOCKED", duplicate_start=True, expected_invocation_status="NO_INVOCATION", expected_invocation_count=0),
        SessionCaseV1("DETERMINISTIC_SESSION_REF", invoke=False, expected_invocation_status="NO_INVOCATION", expected_invocation_count=0),
        SessionCaseV1("DETERMINISTIC_INVOCATION_REF"),
        SessionCaseV1("DISTINCT_INVOCATIONS_DISTINCT_REF", source_case_id="SCENARIO12_INDEPENDENT_BINDING_PATHS", expected_session_count=2, expected_invocation_count=2),
        SessionCaseV1("NO_RANDOM_UUID", invoke=False, expected_invocation_status="NO_INVOCATION", expected_invocation_count=0),
        SessionCaseV1("NO_TIMESTAMP_IDENTITY", invoke=False, expected_invocation_status="NO_INVOCATION", expected_invocation_count=0),
        SessionCaseV1("NO_REAL_PROVIDER_CALL"),
        SessionCaseV1("NO_REAL_MODEL_CALL"),
        SessionCaseV1("NO_CAMERA"),
        SessionCaseV1("NO_OCR"),
        SessionCaseV1("NO_YOLO"),
        SessionCaseV1("NO_SLAM"),
        SessionCaseV1("NO_VLM"),
        SessionCaseV1("NO_NETWORK"),
        SessionCaseV1("NO_SUBPROCESS"),
        SessionCaseV1("NO_THREAD"),
        SessionCaseV1("NO_SOCKET"),
        SessionCaseV1("FPO_DOES_NOT_CREATE_RUNTIME_SESSION", invoke=False, expected_invocation_status="NO_INVOCATION", expected_invocation_count=0),
        SessionCaseV1("REQUESTER_DOES_NOT_START_PROVIDER"),
        SessionCaseV1("PERMISSION_MANAGER_DOES_NOT_INVOKE_PROVIDER"),
        SessionCaseV1("PROVIDER_RUNTIME_FAILURE_OWNER", outcome="FAILED", expected_invocation_status="PROVIDER_INVOCATION_FAILED"),
        SessionCaseV1("GRANT_FAILURE_OWNER", grant_status="DENIED", expected_session_status="INVALID_INPUT", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("RESOURCE_FAILURE_OWNER", invocation_allocation_status="RELEASED", expected_invocation_status="INVALID_INPUT", expected_invocation_count=0),
        SessionCaseV1("BINDING_FAILURE_OWNER", binding_status="REVOKED", expected_session_status="INVALID_INPUT", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("AUTHORITY_RESPONSIBILITY_VALID", invoke=False, expected_invocation_status="NO_INVOCATION", expected_invocation_count=0),
        SessionCaseV1("AUTHORITY_WITHOUT_RESPONSIBILITY_BLOCKED", authority_records=blocked_records, expected_session_status="NO_PROVIDER_RUNTIME_SESSION", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("RESPONSIBILITY_WITHOUT_AUTHORITY_BLOCKED", authority_records=responsibility_only_records, expected_session_status="NO_PROVIDER_RUNTIME_SESSION", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("PREFLIGHT_REQUIRED", invoke=False, expected_invocation_status="NO_INVOCATION", expected_invocation_count=0),
        SessionCaseV1("POSTFLIGHT_REQUIRED"),
        SessionCaseV1("PREFLIGHT_BLOCK_HARD_STOPS_ENGINE", authority_records=blocked_records, expected_session_status="NO_PROVIDER_RUNTIME_SESSION", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("SCENARIO12_SIGNAGE_SESSION", source_case_id="SCENARIO12_SIGNAGE"),
        SessionCaseV1("SCENARIO12_FLOW_SESSION", source_case_id="SCENARIO12_HUMAN_FLOW"),
        SessionCaseV1("SCENARIO12_INDEPENDENT_LINEAGE", source_case_id="SCENARIO12_INDEPENDENT_BINDING_PATHS", expected_session_count=2, expected_invocation_count=2),
        SessionCaseV1("SCENARIO12_NO_MODEL_INFERENCE", source_case_id="SCENARIO12_INDEPENDENT_BINDING_PATHS", expected_session_count=2, expected_invocation_count=2),
        SessionCaseV1("SCENARIO12_OPAQUE_RESULTS", source_case_id="SCENARIO12_INDEPENDENT_BINDING_PATHS", expected_session_count=2, expected_invocation_count=2),
        SessionCaseV1("MALFORMED_INPUT_FAIL_CLOSED", malformed_session=True, expected_session_status="INVALID_INPUT", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
        SessionCaseV1("DETERMINISTIC_REPLAY"),
        SessionCaseV1("UNIFIED_FINAL_DECISION_GO"),
        SessionCaseV1("GOVERNANCE_FAILURE_FORCES_NO_GO", authority_records=blocked_records, expected_session_status="NO_PROVIDER_RUNTIME_SESSION", expected_invocation_status="NO_INVOCATION", expected_session_count=0, expected_invocation_count=0, expected_blocked=True),
    )
    return cases


__all__ = ["PHASE", "EVALUATION_MARKER", "OWNER", "PROBLEM", "STATE", "CONTEXT", "SessionCaseV1", "valid_profile", "valid_authority_records", "build_provider_session_cases_v1"]
