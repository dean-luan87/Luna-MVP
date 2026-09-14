"""Synthetic fixtures for the execution-result to evidence boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    ARCHITECTURE_SOURCE_REF,
    CONSTITUTION_SOURCE_REF,
    PROTOCOL_SOURCE_REF,
    GovernanceAuthorityResponsibilityRecordV1,
    PhaseGovernanceProfileV1,
)


PHASE = "Phase-Provider-Invocation-Result-Runtime-Observation-Gateway-Evidence-Controlled-Integration-v1-001"
EVALUATION_MARKER = "CONTROLLED_PROVIDER_INVOCATION_RUNTIME_OBSERVATION_GATEWAY_EVIDENCE"
OWNER = "Provider Runtime Observation Integration"
PROBLEM = "problem:controlled:provider-observation-evidence"
STATE = "state:controlled:provider-observation-evidence"
CONTEXT = ("context:controlled:provider-observation-evidence",)
AUTHORITY = "authority:observation-evidence-integration"
RESPONSIBILITY = "responsibility:observation-evidence-integration"


@dataclass(frozen=True)
class IntegrationCaseV1:
    case_id: str
    source_case_id: str = "PROVIDER_ONLY_BINDING_BOUND"
    source_case_ids: Tuple[str, ...] = ()
    outcome: str = "COMPLETED"
    invoke: bool = True
    expected_formation_status: str = "RUNTIME_OBSERVATION_FORMED"
    expected_gateway_admission_status: str = "ADMITTED_OBSERVATION"
    expected_evidence_formation_status: str = "EVIDENCE_CREATED"
    expected_observation_count: int = 1
    expected_evidence_count: int = 1
    expected_preflight_status: str = "PASS"
    expected_postflight_status: str = "PASS"
    malformed_invocation_result: bool = False
    gateway_malformed_observation: bool = False
    gateway_lineage_mismatch: bool = False
    gateway_unknown_provider: bool = False
    duplicate_observation: bool = False
    replay: bool = False
    truth_attempt: bool = False
    authority_records: Optional[Tuple[GovernanceAuthorityResponsibilityRecordV1, ...]] = None


def valid_profile() -> PhaseGovernanceProfileV1:
    return PhaseGovernanceProfileV1(
        phase_ref=PHASE,
        phase_owner_ref=OWNER,
        domains=("CONTROLLED_PHASE",),
        owners_touched=(
            "Provider Runtime Governance", "Runtime Executor", "Provider Governance",
            "Permission / Admission Manager", "Observation Gateway", "Protocol Manager",
        ),
        governance_profiles=(
            "GOVERNED_EXECUTION", "AUTHORITY_RESPONSIBILITY", "CANDIDATE_ONLY",
            "READ_ONLY", "NO_TRUTH", "NO_WORLD_MUTATION", "NO_RUNTIME",
            "NO_PROVIDER_INVOCATION", "NO_MODEL_INVOCATION", "NO_DECISION_ACTION_TASK",
            "REQUESTER_EXECUTOR_BOUNDARY", "ADAPTER_BOUNDARY",
        ),
        maturity_level="CONTROLLED_V1",
        runtime_level="NONE",
        candidate_only=True,
        read_only=True,
        truth_authority=False,
        world_truth_authority=False,
        runtime_authority=False,
        authority_refs=(),
        responsibility_refs=(),
        input_contract_refs=(
            "ProviderInvocationResultV1", "RuntimeObservationEnvelopeV1",
            "ObservationIngressRequestV1",
        ),
        output_contract_refs=(
            "RuntimeObservationEnvelopeV1", "ObservationGatewayResultV1",
            "PerceptionEvidenceV1",
        ),
        protocol_refs=(PROTOCOL_SOURCE_REF,),
        constitution_refs=(CONSTITUTION_SOURCE_REF,),
        context_refs=CONTEXT,
        trace_ref="trace:provider-invocation-observation-evidence:governance",
    )


def valid_authority_records() -> Tuple[GovernanceAuthorityResponsibilityRecordV1, ...]:
    return (
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="provider-runtime-observation-integration:formation",
            owner_ref=OWNER,
            authority_refs=(AUTHORITY,),
            responsibility_refs=(RESPONSIBILITY,),
            decision_types=("controlled_observation_evidence_handoff",),
            failure_types=("observation_evidence_handoff_failure",),
            authority_responsibility_map=((AUTHORITY, RESPONSIBILITY),),
            responsibility_owner_refs=((RESPONSIBILITY, OWNER),),
            operational_authority=True,
            candidate_only=False,
        ),
    )


def _blocked_authority_records() -> Tuple[GovernanceAuthorityResponsibilityRecordV1, ...]:
    return (
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="provider-runtime-observation-integration:authority-without-responsibility",
            owner_ref=OWNER,
            authority_refs=(AUTHORITY,),
            responsibility_refs=(),
            decision_types=("controlled_observation_evidence_handoff",),
            failure_types=("observation_evidence_handoff_failure",),
            authority_responsibility_map=(),
            candidate_only=False,
        ),
    )


def _blocked_responsibility_records() -> Tuple[GovernanceAuthorityResponsibilityRecordV1, ...]:
    return (
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="provider-runtime-observation-integration:responsibility-without-authority",
            owner_ref=OWNER,
            authority_refs=(),
            responsibility_refs=(RESPONSIBILITY,),
            decision_types=("controlled_observation_evidence_handoff",),
            failure_types=("observation_evidence_handoff_failure",),
            authority_responsibility_map=(),
            responsibility_owner_refs=((RESPONSIBILITY, OWNER),),
            candidate_only=False,
        ),
    )


def build_provider_invocation_observation_evidence_cases_v1() -> Tuple[IntegrationCaseV1, ...]:
    cases = [
        IntegrationCaseV1("VALID_COMPLETED_INVOCATION_FORMS_RUNTIME_OBSERVATION"),
        IntegrationCaseV1("FAILED_INVOCATION_NO_NORMAL_OBSERVATION", outcome="FAILED", expected_formation_status="RUNTIME_OBSERVATION_FORMATION_BLOCKED", expected_gateway_admission_status="NOT_ATTEMPTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0),
        IntegrationCaseV1("TIMED_OUT_INVOCATION_NO_NORMAL_OBSERVATION", outcome="TIMED_OUT", expected_formation_status="RUNTIME_OBSERVATION_FORMATION_BLOCKED", expected_gateway_admission_status="NOT_ATTEMPTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0),
        IntegrationCaseV1("STOPPED_INVOCATION_NO_NORMAL_OBSERVATION", outcome="STOPPED", expected_formation_status="RUNTIME_OBSERVATION_FORMATION_BLOCKED", expected_gateway_admission_status="NOT_ATTEMPTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0),
        IntegrationCaseV1("REVOKED_INVOCATION_NO_NORMAL_OBSERVATION", outcome="REVOKED", expected_formation_status="RUNTIME_OBSERVATION_FORMATION_BLOCKED", expected_gateway_admission_status="NOT_ATTEMPTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0),
        IntegrationCaseV1("RUNTIME_OBSERVATION_PRESERVES_PROVIDER_REF"),
        IntegrationCaseV1("RUNTIME_OBSERVATION_PRESERVES_CAPABILITY_REF"),
        IntegrationCaseV1("RUNTIME_OBSERVATION_PRESERVES_BINDING_REF"),
        IntegrationCaseV1("RUNTIME_OBSERVATION_PRESERVES_GRANT_REF"),
        IntegrationCaseV1("RUNTIME_OBSERVATION_PRESERVES_ALLOCATION_REF"),
        IntegrationCaseV1("RUNTIME_OBSERVATION_PRESERVES_EXECUTION_INSTANCE_REF"),
        IntegrationCaseV1("RUNTIME_OBSERVATION_PRESERVES_SESSION_REF"),
        IntegrationCaseV1("RUNTIME_OBSERVATION_PRESERVES_INVOCATION_REF"),
        IntegrationCaseV1("RUNTIME_OBSERVATION_MODEL_NULL_ALLOWED"),
        IntegrationCaseV1("RUNTIME_OBSERVATION_MODEL_CARRY_FORWARD", source_case_id="MODEL_REF_CARRY_FORWARD_BINDING"),
        IntegrationCaseV1("NO_INVOCATION_RESULT", invoke=False, expected_formation_status="NO_INVOCATION_RESULT", expected_gateway_admission_status="NOT_ATTEMPTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0),
        IntegrationCaseV1("GATEWAY_ADMITS_VALID_RUNTIME_OBSERVATION"),
        IntegrationCaseV1("GATEWAY_REJECTS_MALFORMED_OBSERVATION", gateway_malformed_observation=True, expected_gateway_admission_status="REJECTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0),
        IntegrationCaseV1("GATEWAY_REJECTS_LINEAGE_MISMATCH", gateway_lineage_mismatch=True, expected_gateway_admission_status="REJECTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0),
        IntegrationCaseV1("GATEWAY_REJECTS_UNKNOWN_PROVIDER_LINEAGE", gateway_unknown_provider=True, expected_gateway_admission_status="REJECTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0),
        IntegrationCaseV1("GATEWAY_REJECTS_INVALID_EXECUTION_LINEAGE", gateway_lineage_mismatch=True, expected_gateway_admission_status="REJECTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0),
        IntegrationCaseV1("GATEWAY_ADMISSION_NOT_TRUTH"),
        IntegrationCaseV1("GATEWAY_DOES_NOT_TRIGGER_PROVIDER"),
        IntegrationCaseV1("GATEWAY_DOES_NOT_TRIGGER_MODEL"),
        IntegrationCaseV1("EVIDENCE_CREATED_FROM_ADMITTED_OBSERVATION"),
        IntegrationCaseV1("REJECTED_OBSERVATION_NO_EVIDENCE", gateway_malformed_observation=True, expected_gateway_admission_status="REJECTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0),
        IntegrationCaseV1("EVIDENCE_READ_ONLY"),
        IntegrationCaseV1("EVIDENCE_NON_TRUTH"),
        IntegrationCaseV1("EVIDENCE_PRESERVES_OBSERVATION_REF"),
        IntegrationCaseV1("EVIDENCE_PRESERVES_GATEWAY_ADMISSION_REF"),
        IntegrationCaseV1("EVIDENCE_PRESERVES_PROVIDER_LINEAGE"),
        IntegrationCaseV1("EVIDENCE_PRESERVES_COGNITIVE_LINEAGE"),
        IntegrationCaseV1("EVIDENCE_MODEL_NULL_ALLOWED"),
        IntegrationCaseV1("EVIDENCE_NOT_SUFFICIENCY_DECISION"),
        IntegrationCaseV1("EVIDENCE_NOT_CURRENT_WORLD"),
        IntegrationCaseV1("EVIDENCE_NOT_FIELD_MUTATION"),
        IntegrationCaseV1("EVIDENCE_NOT_CONTEXT_MUTATION"),
        IntegrationCaseV1("EVIDENCE_NOT_MEMORY"),
        IntegrationCaseV1("EVIDENCE_NOT_EXPERIENCE"),
        IntegrationCaseV1("DETERMINISTIC_OBSERVATION_REF"),
        IntegrationCaseV1("DETERMINISTIC_GATEWAY_ADMISSION_REF"),
        IntegrationCaseV1("DETERMINISTIC_EVIDENCE_REF"),
        IntegrationCaseV1("REPLAY_OBSERVATION_IDEMPOTENT", replay=True),
        IntegrationCaseV1("REPLAY_EVIDENCE_IDEMPOTENT", replay=True),
        IntegrationCaseV1("DISTINCT_INVOCATIONS_DISTINCT_OBSERVATIONS", source_case_ids=("SCENARIO12_SIGNAGE", "SCENARIO12_HUMAN_FLOW"), expected_observation_count=2, expected_evidence_count=2),
        IntegrationCaseV1("NO_RANDOM_UUID"),
        IntegrationCaseV1("NO_TIMESTAMP_IDENTITY"),
        IntegrationCaseV1("NO_REAL_PROVIDER_CALL"),
        IntegrationCaseV1("NO_REAL_MODEL_CALL"),
        IntegrationCaseV1("NO_NETWORK"),
        IntegrationCaseV1("NO_SUBPROCESS"),
        IntegrationCaseV1("NO_THREAD"),
        IntegrationCaseV1("NO_SOCKET"),
        IntegrationCaseV1("NO_CAMERA"),
        IntegrationCaseV1("NO_OCR"),
        IntegrationCaseV1("NO_YOLO"),
        IntegrationCaseV1("NO_SLAM"),
        IntegrationCaseV1("NO_VLM"),
        IntegrationCaseV1("AUTHORITY_RESPONSIBILITY_VALID"),
        IntegrationCaseV1("AUTHORITY_WITHOUT_RESPONSIBILITY_BLOCKED", expected_preflight_status="GOVERNANCE_PREFLIGHT_BLOCKED", expected_gateway_admission_status="NOT_ATTEMPTED", expected_formation_status="NOT_EXECUTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0, authority_records=_blocked_authority_records()),
        IntegrationCaseV1("RESPONSIBILITY_WITHOUT_AUTHORITY_BLOCKED", expected_preflight_status="GOVERNANCE_PREFLIGHT_BLOCKED", expected_gateway_admission_status="NOT_ATTEMPTED", expected_formation_status="NOT_EXECUTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0, authority_records=_blocked_responsibility_records()),
        IntegrationCaseV1("PREFLIGHT_REQUIRED"),
        IntegrationCaseV1("PREFLIGHT_BLOCK_HARD_STOPS_PIPELINE", expected_preflight_status="GOVERNANCE_PREFLIGHT_BLOCKED", expected_gateway_admission_status="NOT_ATTEMPTED", expected_formation_status="NOT_EXECUTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0, authority_records=_blocked_authority_records()),
        IntegrationCaseV1("POSTFLIGHT_REQUIRED"),
        IntegrationCaseV1("WORLD_TRUTH_BLOCKED", truth_attempt=True, expected_postflight_status="GOVERNANCE_POSTFLIGHT_BLOCKED"),
        IntegrationCaseV1("CURRENT_WORLD_MUTATION_BLOCKED"),
        IntegrationCaseV1("SCENARIO12_SIGNAGE_RUNTIME_OBSERVATION", source_case_id="SCENARIO12_SIGNAGE"),
        IntegrationCaseV1("SCENARIO12_FLOW_RUNTIME_OBSERVATION", source_case_id="SCENARIO12_HUMAN_FLOW"),
        IntegrationCaseV1("SCENARIO12_SIGNAGE_GATEWAY_ADMITTED", source_case_id="SCENARIO12_SIGNAGE"),
        IntegrationCaseV1("SCENARIO12_FLOW_GATEWAY_ADMITTED", source_case_id="SCENARIO12_HUMAN_FLOW"),
        IntegrationCaseV1("SCENARIO12_SIGNAGE_EVIDENCE", source_case_id="SCENARIO12_SIGNAGE"),
        IntegrationCaseV1("SCENARIO12_FLOW_EVIDENCE", source_case_id="SCENARIO12_HUMAN_FLOW"),
        IntegrationCaseV1("SCENARIO12_INDEPENDENT_OBSERVATION_LINEAGE", source_case_ids=("SCENARIO12_SIGNAGE", "SCENARIO12_HUMAN_FLOW"), expected_observation_count=2, expected_evidence_count=2),
        IntegrationCaseV1("SCENARIO12_INDEPENDENT_EVIDENCE_LINEAGE", source_case_ids=("SCENARIO12_SIGNAGE", "SCENARIO12_HUMAN_FLOW"), expected_observation_count=2, expected_evidence_count=2),
        IntegrationCaseV1("SCENARIO12_NO_SEMANTIC_INTERPRETATION", source_case_ids=("SCENARIO12_SIGNAGE", "SCENARIO12_HUMAN_FLOW"), expected_observation_count=2, expected_evidence_count=2),
        IntegrationCaseV1("SCENARIO12_NO_MODEL_INFERENCE", source_case_ids=("SCENARIO12_SIGNAGE", "SCENARIO12_HUMAN_FLOW"), expected_observation_count=2, expected_evidence_count=2),
        IntegrationCaseV1("MALFORMED_INVOCATION_RESULT_FAIL_CLOSED", malformed_invocation_result=True, expected_formation_status="INVALID_INPUT", expected_gateway_admission_status="NOT_ATTEMPTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0),
        IntegrationCaseV1("MALFORMED_RUNTIME_OBSERVATION_FAIL_CLOSED", gateway_malformed_observation=True, expected_gateway_admission_status="REJECTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0),
        IntegrationCaseV1("MALFORMED_GATEWAY_INPUT_FAIL_CLOSED", gateway_unknown_provider=True, expected_gateway_admission_status="REJECTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0),
        IntegrationCaseV1("DETERMINISTIC_REPLAY", replay=True),
        IntegrationCaseV1("UNIFIED_FINAL_DECISION_GO"),
        IntegrationCaseV1("GOVERNANCE_FAILURE_FORCES_NO_GO", expected_preflight_status="GOVERNANCE_PREFLIGHT_BLOCKED", expected_gateway_admission_status="NOT_ATTEMPTED", expected_formation_status="NOT_EXECUTED", expected_evidence_formation_status="NO_EVIDENCE", expected_observation_count=0, expected_evidence_count=0, authority_records=_blocked_authority_records()),
    ]
    return tuple(cases)


__all__ = [
    "PHASE", "EVALUATION_MARKER", "OWNER", "PROBLEM", "STATE", "CONTEXT",
    "AUTHORITY", "RESPONSIBILITY", "IntegrationCaseV1", "valid_profile",
    "valid_authority_records", "build_provider_invocation_observation_evidence_cases_v1",
]
