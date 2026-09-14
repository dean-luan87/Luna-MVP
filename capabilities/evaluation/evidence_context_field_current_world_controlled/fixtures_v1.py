"""Deterministic fixtures for the Evidence -> Field boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    CONSTITUTION_SOURCE_REF,
    PROTOCOL_SOURCE_REF,
    GovernanceAuthorityResponsibilityRecordV1,
    PhaseGovernanceProfileV1,
)


PHASE = "Phase-Evidence-Context-Field-Current-World-Controlled-Integration-v1-001"
EVALUATION_MARKER = "CONTROLLED_EVIDENCE_CONTEXT_FIELD_CURRENT_WORLD"
OWNER = "Field / Current World Controlled Integration"
CONTEXT_REF = "context:controlled:field-current-world:v1"
FIELD_REF = "field:controlled:perception:v1"
AUTHORITY = "authority:field-reducer-boundary"
RESPONSIBILITY = "responsibility:field-reducer-boundary"
EVALUATED_AT = "2026-09-04T00:00:00Z"


@dataclass(frozen=True)
class FieldIntegrationCaseV1:
    case_id: str
    scenario: str = "normal"
    field_ref: str = FIELD_REF
    expected_candidate_status: str = "FIELD_EVENT_CANDIDATE_FORMED"
    expected_admission_status: str = "admitted_event"
    expected_reducer_status: str = "completed_candidate"
    expected_field_state_present: bool = True
    expected_context_present: bool = True
    expected_preflight_status: str = "PASS"
    expected_postflight_status: str = "PASS"
    malformed_evidence: bool = False
    stale_evidence: bool = False
    insufficient_evidence: bool = False
    context_mismatch: bool = False
    context_owner_mismatch: bool = False
    skip_event_admission: bool = False
    conflict: bool = False
    correction: bool = False
    temporary_overlay: bool = False
    expired_overlay: bool = False
    refresh: bool = False
    reopened: bool = False
    duplicate_event: bool = False
    world_truth_attempt: bool = False
    direct_mutation_attempt: bool = False
    malformed_lineage: bool = False
    authority_records: Optional[Tuple[GovernanceAuthorityResponsibilityRecordV1, ...]] = None


def valid_profile() -> PhaseGovernanceProfileV1:
    return PhaseGovernanceProfileV1(
        phase_ref=PHASE,
        phase_owner_ref=OWNER,
        domains=("CONTROLLED_PHASE",),
        owners_touched=(
            "Field Event Admission",
            "Field State Reducer",
            "Context Foundation",
            "Cognitive State Formation",
            "Protocol Manager",
        ),
        governance_profiles=(
            "GOVERNED_EXECUTION",
            "AUTHORITY_RESPONSIBILITY",
            "CANDIDATE_ONLY",
            "READ_ONLY",
            "NO_TRUTH",
            "NO_WORLD_MUTATION",
            "NO_RUNTIME",
            "NO_PROVIDER_INVOCATION",
            "NO_MODEL_INVOCATION",
            "NO_DECISION_ACTION_TASK",
            "REQUESTER_EXECUTOR_BOUNDARY",
            "ADAPTER_BOUNDARY",
        ),
        maturity_level="CONTROLLED_V1",
        runtime_level="NONE",
        candidate_only=True,
        read_only=True,
        truth_authority=False,
        world_truth_authority=False,
        runtime_authority=False,
        authority_refs=(AUTHORITY,),
        responsibility_refs=(RESPONSIBILITY,),
        input_contract_refs=(
            "PerceptionEvidenceV1",
            "FieldEventCandidateV1",
            "FieldEventAdmissionResultV1",
            "FieldStateReducerModuleRequestV1",
            "ContextEnvelopeCandidateV1",
        ),
        output_contract_refs=(
            "FieldEventCandidateV1",
            "FieldStateCandidate",
            "FieldStateV1",
            "CurrentWorldCandidateV1",
        ),
        protocol_refs=(PROTOCOL_SOURCE_REF,),
        constitution_refs=(CONSTITUTION_SOURCE_REF,),
        context_refs=(CONTEXT_REF,),
        trace_ref="trace:evidence-context-field-current-world:governance",
    )


def valid_authority_records() -> Tuple[GovernanceAuthorityResponsibilityRecordV1, ...]:
    return (
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="field-state-reducer:controlled-boundary",
            owner_ref="Field State Reducer",
            authority_refs=(AUTHORITY,),
            responsibility_refs=(RESPONSIBILITY,),
            decision_types=("field_state_candidate_reduction",),
            failure_types=("field_reduction_failure",),
            authority_responsibility_map=((AUTHORITY, RESPONSIBILITY),),
            responsibility_owner_refs=((RESPONSIBILITY, "Field State Reducer"),),
            operational_authority=False,
            mutation_authority=False,
            candidate_only=True,
        ),
    )


def _authority_without_responsibility() -> Tuple[GovernanceAuthorityResponsibilityRecordV1, ...]:
    return (
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="field-state-reducer:invalid-authority-only",
            owner_ref="Field State Reducer",
            authority_refs=(AUTHORITY,),
            responsibility_refs=(),
            decision_types=("field_state_candidate_reduction",),
            failure_types=("field_reduction_failure",),
            authority_responsibility_map=(),
            candidate_only=True,
        ),
    )


def _responsibility_without_authority() -> Tuple[GovernanceAuthorityResponsibilityRecordV1, ...]:
    return (
        GovernanceAuthorityResponsibilityRecordV1(
            module_ref="field-state-reducer:invalid-responsibility-only",
            owner_ref="Field State Reducer",
            authority_refs=(),
            responsibility_refs=(RESPONSIBILITY,),
            decision_types=("field_state_candidate_reduction",),
            failure_types=("field_reduction_failure",),
            authority_responsibility_map=(),
            responsibility_owner_refs=((RESPONSIBILITY, "Field State Reducer"),),
            candidate_only=True,
        ),
    )


def _case(case_id: str, **kwargs: object) -> FieldIntegrationCaseV1:
    return FieldIntegrationCaseV1(case_id, **kwargs)


def build_evidence_context_field_current_world_cases_v1() -> Tuple[FieldIntegrationCaseV1, ...]:
    cases = [
        _case("VALID_EVIDENCE_FORMS_FIELD_EVENT_CANDIDATE"),
        _case("MALFORMED_EVIDENCE_NO_CANDIDATE", expected_candidate_status="INVALID_INPUT", expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_REDUCER", expected_field_state_present=False, malformed_evidence=True),
        _case("STALE_EVIDENCE_NO_UNGOVERNED_UPDATE", expected_candidate_status="FIELD_EVENT_CANDIDATE_BLOCKED", expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_REDUCER", expected_field_state_present=False, stale_evidence=True),
        _case("UNKNOWN_REMAINS_UNKNOWN", expected_candidate_status="NOT_EXECUTED", expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_UPDATE", expected_field_state_present=False, insufficient_evidence=True),
        _case("CONTEXT_REF_PRESERVED"),
        _case("CONTEXT_NOT_TRUTH_SOURCE"),
        _case("EVIDENCE_CONTEXT_CANNOT_MUTATE_FIELD"),
        _case("ROLE_REF_READ_ONLY"),
        _case("FIELD_EVENT_CANDIDATE_ONLY"),
        _case("FIELD_EVENT_CANDIDATE_NON_TRUTH"),
        _case("FIELD_EVENT_CANDIDATE_READ_ONLY"),
        _case("EVENT_ADMISSION_REQUIRED", expected_admission_status="REQUIRES_ADMISSION", expected_reducer_status="NO_REDUCER", expected_field_state_present=False, skip_event_admission=True),
        _case("NON_ADMITTED_EVENT_NOT_REDUCED", expected_admission_status="REQUIRES_ADMISSION", expected_reducer_status="NO_REDUCER", expected_field_state_present=False, skip_event_admission=True),
        _case("ADMITTED_EVENT_REACHES_REDUCER"),
        _case("REDUCER_IS_SINGLE_MUTATION_AUTHORITY"),
        _case("GATEWAY_CANNOT_MUTATE_FIELD"),
        _case("EVIDENCE_CANNOT_MUTATE_FIELD"),
        _case("CONTEXT_DIRECT_MUTATION_BLOCKED"),
        _case("PROVIDER_CANNOT_MUTATE_FIELD"),
        _case("FPO_CANNOT_MUTATE_FIELD_DIRECTLY"),
        _case("REDUCER_DETERMINISTIC"),
        _case("REDUCER_REPLAY_STABLE", duplicate_event=True),
        _case("DUPLICATE_EVENT_IDEMPOTENT", duplicate_event=True),
        _case("ROAD_ACCESSIBLE_EVENT"),
        _case("CONSTRUCTION_NOTICE_EVENT", temporary_overlay=True),
        _case("BARRIER_VISUAL_EVENT"),
        _case("ROAD_BLOCKED_EVENT", scenario="road-blocked"),
        _case("TEMPORARY_PASSAGE_EVENT", temporary_overlay=True),
        _case("CONFLICT_EVENT_RETAINED", scenario="conflict", conflict=True, expected_reducer_status="unresolved"),
        _case("CONFLICT_NOT_AUTO_RESOLVED", scenario="conflict", conflict=True, expected_reducer_status="unresolved"),
        _case("NO_LAST_WRITE_WINS_UNLESS_CANONICAL", scenario="conflict", conflict=True, expected_reducer_status="unresolved"),
        _case("CORRECTION_PRESERVES_PRIOR_PROVENANCE", correction=True),
        _case("CORRECTION_REFERENCES_TARGET_EVENT", correction=True),
        _case("OVERLAY_EXPIRED", temporary_overlay=True, expired_overlay=True, expected_reducer_status="temporally_invalid"),
        _case("EXPIRED_STATE_REMOVED_BY_REDUCER", temporary_overlay=True, expired_overlay=True, expected_reducer_status="temporally_invalid"),
        _case("REFRESH_EVIDENCE_EXTENDS_TEMPORARY_STATE", temporary_overlay=True, refresh=True),
        _case("REFRESH_REQUIRES_VALID_LINEAGE", temporary_overlay=True, refresh=True),
        _case("ROAD_REOPENED_EVENT", reopened=True),
        _case("REOPEN_DOES_NOT_DELETE_HISTORY", reopened=True),
        _case("FIELD_STATE_PRESERVES_EVENT_REF"),
        _case("FIELD_STATE_PRESERVES_EVIDENCE_REF"),
        _case("FIELD_STATE_PRESERVES_OBSERVATION_LINEAGE"),
        _case("FIELD_STATE_PRESERVES_PROVIDER_LINEAGE"),
        _case("FIELD_STATE_DOMAIN_AUTHORITATIVE"),
        _case("FIELD_STATE_NOT_ABSOLUTE_WORLD_TRUTH"),
        _case("WORLD_TRUTH_NOT_DECLARED"),
        _case("NO_MEMORY_WRITE"),
        _case("NO_EXPERIENCE_WRITE"),
        _case("NO_DECISION"),
        _case("NO_TASK"),
        _case("NO_ACTION"),
        _case("NO_PROVIDER_RECALL"),
        _case("NO_GATEWAY_RECALL"),
        _case("NO_NEW_OBSERVATION_DEMAND"),
        _case("NO_REAL_PROVIDER"),
        _case("NO_REAL_MODEL"),
        _case("NO_NETWORK"),
        _case("NO_SUBPROCESS"),
        _case("NO_THREAD"),
        _case("NO_SOCKET"),
        _case("NO_CAMERA"),
        _case("NO_OCR"),
        _case("NO_YOLO"),
        _case("NO_SLAM"),
        _case("NO_VLM"),
        _case("AUTHORITY_RESPONSIBILITY_VALID"),
        _case("AUTHORITY_WITHOUT_RESPONSIBILITY_BLOCKED", expected_preflight_status="GOVERNANCE_PREFLIGHT_BLOCKED", expected_candidate_status="NOT_EXECUTED", expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_REDUCER", expected_field_state_present=False, authority_records=_authority_without_responsibility()),
        _case("RESPONSIBILITY_WITHOUT_AUTHORITY_BLOCKED", expected_preflight_status="GOVERNANCE_PREFLIGHT_BLOCKED", expected_candidate_status="NOT_EXECUTED", expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_REDUCER", expected_field_state_present=False, authority_records=_responsibility_without_authority()),
        _case("PREFLIGHT_REQUIRED"),
        _case("PREFLIGHT_BLOCK_NO_FIELD_EFFECT", expected_preflight_status="GOVERNANCE_PREFLIGHT_BLOCKED", expected_candidate_status="NOT_EXECUTED", expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_REDUCER", expected_field_state_present=False, authority_records=_authority_without_responsibility()),
        _case("POSTFLIGHT_REQUIRED"),
        _case("MALFORMED_EVENT_FAIL_CLOSED", malformed_evidence=True, expected_candidate_status="INVALID_INPUT", expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_REDUCER", expected_field_state_present=False),
        _case("MALFORMED_CONTEXT_REF_FAIL_CLOSED", context_mismatch=True, expected_candidate_status="INVALID_INPUT", expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_REDUCER", expected_field_state_present=False, expected_context_present=False),
        _case("CONTEXT_PROJECTION_OWNER_MISMATCH_BLOCKED", context_owner_mismatch=True, expected_candidate_status="INVALID_INPUT", expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_REDUCER", expected_field_state_present=False, expected_context_present=False),
        _case("CROSS_DEMAND_CONTAMINATION_BLOCKED", malformed_lineage=True, expected_candidate_status="FIELD_EVENT_CANDIDATE_BLOCKED", expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_REDUCER", expected_field_state_present=False),
        _case("CROSS_PROVIDER_LINEAGE_CONTAMINATION_BLOCKED", malformed_lineage=True, expected_candidate_status="FIELD_EVENT_CANDIDATE_BLOCKED", expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_REDUCER", expected_field_state_present=False),
        _case("DETERMINISTIC_FIELD_CANDIDATE_REF"),
        _case("DETERMINISTIC_EVENT_REF"),
        _case("DETERMINISTIC_FIELD_STATE"),
        _case("REPLAY_IDEMPOTENT", duplicate_event=True),
        _case("SCENARIO12_SIGNAGE_FIELD_CANDIDATE", scenario="signage"),
        _case("SCENARIO12_FLOW_FIELD_CANDIDATE", scenario="human-flow"),
        _case("SCENARIO12_INDEPENDENT_FIELD_LINEAGE", scenario="both", field_ref="field:scenario12:independent"),
        _case("SCENARIO12_NO_AUTOMERGE", scenario="both", field_ref="field:scenario12:independent"),
        _case("SCENARIO12_NO_EXIT_TRUTH", scenario="signage"),
        _case("SCENARIO12_NO_MODEL_INFERENCE", scenario="human-flow"),
        _case("EVIDENCE_INSUFFICIENCY_REMAINS_UPSTREAM", expected_candidate_status="NOT_EXECUTED", insufficient_evidence=True, expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_UPDATE", expected_field_state_present=False),
        _case("UNKNOWN_FIELD_STATE_IS_LEGAL", expected_candidate_status="NOT_EXECUTED", insufficient_evidence=True, expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_UPDATE", expected_field_state_present=False),
        _case("STALE_LINEAGE_REQUIRES_REFRESH", stale_evidence=True, expected_candidate_status="FIELD_EVENT_CANDIDATE_BLOCKED", expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_REDUCER", expected_field_state_present=False),
        _case("CORRECTION_RELATION_IS_EXPLICIT", correction=True),
        _case("EXPIRY_IS_EVENT_GOVERNED", temporary_overlay=True, expired_overlay=True, expected_reducer_status="temporally_invalid"),
        _case("REFRESH_DOES_NOT_INFER_TRUTH", temporary_overlay=True, refresh=True),
        _case("REOPEN_IS_NEW_EVENT", reopened=True),
        _case("CONFLICT_RETAINS_COMPETING_REFS", scenario="conflict", conflict=True, expected_reducer_status="unresolved"),
        _case("MALFORMED_LINEAGE_NO_REDUCER", malformed_lineage=True, expected_candidate_status="FIELD_EVENT_CANDIDATE_BLOCKED", expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_REDUCER", expected_field_state_present=False),
        _case("CONTEXT_SCOPE_REFERENCE_ONLY"),
        _case("REDUCER_OUTPUT_IS_CANDIDATE"),
        _case("EVIDENCE_IS_NOT_EVENT_TRUTH"),
        _case("MODEL_NULL_REMAINS_OPTIONAL"),
        _case("EXPLICIT_MODEL_CARRY_FORWARD"),
        _case("WORLD_TRUTH_DECLARATION_BLOCKED", world_truth_attempt=True, expected_postflight_status="GOVERNANCE_POSTFLIGHT_BLOCKED"),
        _case("DIRECT_FIELD_MUTATION_BLOCKED", direct_mutation_attempt=True, expected_postflight_status="GOVERNANCE_POSTFLIGHT_BLOCKED"),
        _case("UNIFIED_FINAL_DECISION_GO"),
        _case("GOVERNANCE_FAILURE_FORCES_NO_GO", expected_preflight_status="GOVERNANCE_PREFLIGHT_BLOCKED", expected_candidate_status="NOT_EXECUTED", expected_admission_status="NOT_ATTEMPTED", expected_reducer_status="NO_REDUCER", expected_field_state_present=False, authority_records=_authority_without_responsibility()),
    ]
    return tuple(cases)


__all__ = [
    "PHASE", "EVALUATION_MARKER", "OWNER", "CONTEXT_REF", "FIELD_REF",
    "AUTHORITY", "RESPONSIBILITY", "EVALUATED_AT", "FieldIntegrationCaseV1",
    "valid_profile", "valid_authority_records",
    "build_evidence_context_field_current_world_cases_v1",
]
