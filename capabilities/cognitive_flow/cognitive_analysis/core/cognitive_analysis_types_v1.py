"""Immutable, serializable A3 Cognitive Analysis skeleton objects v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from typing import Any, Mapping, Tuple

from .cognitive_analysis_enums_v1 import (
    AdmissionStatusV1, AnalysisResultStatusV1, AnalysisSufficiencyStatusV1,
    BlockingLevelV1, CompetingHypothesisStatusV1, EvidenceRelationV1,
    HypothesisStatusV1, HypothesisTypeV1, InformationGapTypeV1,
    LifecycleStatusV1,
)


COGNITIVE_ANALYSIS_SCHEMA_VERSION_V1 = "luna.cognitive_analysis.v1"


def to_jsonable_v1(value: Any) -> Any:
    """Convert immutable skeleton data to JSON-compatible primitives."""
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return to_jsonable_v1(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): to_jsonable_v1(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [to_jsonable_v1(item) for item in value]
    if isinstance(value, list):
        return [to_jsonable_v1(item) for item in value]
    return value


@dataclass(frozen=True)
class CognitiveAnalysisAdmissionResultV1:
    admission_id: str
    source_context_ref: str
    source_context_version: str
    status: AdmissionStatusV1
    reason_codes: Tuple[str, ...]
    blocking_gap_refs: Tuple[str, ...]
    warning_codes: Tuple[str, ...]
    permission_allowed: bool
    provenance_complete: bool
    trace_complete: bool
    source_snapshot_traceable: bool
    lifecycle_status: LifecycleStatusV1
    context_sufficiency_status: AnalysisSufficiencyStatusV1
    context_stale: bool
    evidence_revoked: bool
    provenance: Mapping[str, Any]
    trace_ref: str
    schema_version: str = COGNITIVE_ANALYSIS_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class CognitiveAnalysisFrameV1:
    analysis_frame_id: str
    analysis_version: str
    source_context_ref: str
    source_context_version: str
    analysis_subject_ref: str
    task_ref: str
    goal_ref: str
    analysis_scope: Mapping[str, Any]
    temporal_scope: Mapping[str, Any]
    selected_evidence_refs: Tuple[str, ...]
    selected_relation_refs: Tuple[str, ...]
    known_constraint_refs: Tuple[str, ...]
    unknown_refs: Tuple[str, ...]
    admission_ref: str
    previous_analysis_frame_ref: str | None
    lifecycle_status: LifecycleStatusV1
    provenance: Mapping[str, Any]
    trace_ref: str
    schema_version: str = COGNITIVE_ANALYSIS_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class HypothesisCandidateV1:
    hypothesis_id: str
    hypothesis_version: str
    hypothesis_type: HypothesisTypeV1
    statement: str
    source_context_ref: str
    source_analysis_frame_ref: str
    source_evidence_refs: Tuple[str, ...]
    supporting_evidence_refs: Tuple[str, ...]
    contradicting_evidence_refs: Tuple[str, ...]
    assumption_refs: Tuple[str, ...]
    uncertainty: Mapping[str, Any]
    confidence_candidate: str
    status: HypothesisStatusV1
    previous_hypothesis_ref: str | None
    supersedes_hypothesis_ref: str | None
    lifecycle_status: LifecycleStatusV1
    provenance: Mapping[str, Any]
    trace_ref: str
    schema_version: str = COGNITIVE_ANALYSIS_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class CompetingHypothesisSetV1:
    competing_set_id: str
    analysis_question: str
    source_context_ref: str
    source_analysis_frame_ref: str
    hypothesis_refs: Tuple[str, ...]
    compatibility_records: Tuple[Mapping[str, Any], ...]
    dominant_candidate_ref: str | None
    unresolved_reason_codes: Tuple[str, ...]
    evidence_coverage: Mapping[str, Any]
    status: CompetingHypothesisStatusV1
    lifecycle_status: LifecycleStatusV1
    provenance: Mapping[str, Any]
    trace_ref: str
    schema_version: str = COGNITIVE_ANALYSIS_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class AnalysisEvidenceAssessmentV1:
    assessment_id: str
    assessment_version: str
    evidence_ref: str
    hypothesis_ref: str
    relation: EvidenceRelationV1
    strength_candidate: str
    reliability_candidate: str
    temporal_relevance: str
    scope_relevance: str
    contradiction_reason: str | None
    uncertainty: Mapping[str, Any]
    lifecycle_status: LifecycleStatusV1
    provenance: Mapping[str, Any]
    trace_ref: str
    schema_version: str = COGNITIVE_ANALYSIS_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class InformationGapRefinementV1:
    refinement_id: str
    source_gap_ref: str | None
    source_analysis_frame_ref: str
    gap_type: InformationGapTypeV1
    newly_discovered: bool
    refined_question: str
    required_information_type: str
    target_field_refs: Tuple[str, ...]
    target_relation_refs: Tuple[str, ...]
    priority_candidate: str
    blocking_level: BlockingLevelV1
    recommended_observation_scope: Mapping[str, Any]
    resolution_criteria: Tuple[str, ...]
    observation_request_candidate_ref: str | None
    lifecycle_status: LifecycleStatusV1
    provenance: Mapping[str, Any]
    trace_ref: str
    schema_version: str = COGNITIVE_ANALYSIS_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class ObservationRequestCandidateV1:
    observation_request_candidate_id: str
    source_refinement_ref: str
    source_analysis_frame_ref: str
    requested_information_type: str
    requested_scope: Mapping[str, Any]
    target_refs: Tuple[str, ...]
    priority_candidate: str
    permission_requirement_refs: Tuple[str, ...]
    execution_admitted: bool
    lifecycle_status: LifecycleStatusV1
    provenance: Mapping[str, Any]
    trace_ref: str
    schema_version: str = COGNITIVE_ANALYSIS_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class CognitiveAnalysisSufficiencyResultV1:
    sufficiency_id: str
    source_context_ref: str
    source_analysis_frame_ref: str
    status: AnalysisSufficiencyStatusV1
    context_sufficiency_ref: str
    evidence_coverage: Mapping[str, Any]
    contradiction_level: str
    unresolved_critical_gap_refs: Tuple[str, ...]
    temporal_validity: str
    revoked_evidence_refs: Tuple[str, ...]
    permission_restriction_refs: Tuple[str, ...]
    hypothesis_stability: str
    provenance_complete: bool
    trace_complete: bool
    reason_codes: Tuple[str, ...]
    warning_codes: Tuple[str, ...]
    provenance: Mapping[str, Any]
    trace_ref: str
    schema_version: str = COGNITIVE_ANALYSIS_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class CognitiveAnalysisResultV1:
    analysis_result_id: str
    analysis_version: str
    source_context_ref: str
    source_context_version: str
    analysis_frame_ref: str
    hypothesis_candidate_refs: Tuple[str, ...]
    competing_hypothesis_set_refs: Tuple[str, ...]
    evidence_assessment_refs: Tuple[str, ...]
    information_gap_refinement_refs: Tuple[str, ...]
    observation_request_candidate_refs: Tuple[str, ...]
    sufficiency_ref: str
    provisional_interpretation: str | None
    unresolved_questions: Tuple[str, ...]
    result_status: AnalysisResultStatusV1
    previous_analysis_result_ref: str | None
    supersedes_analysis_result_ref: str | None
    lifecycle_status: LifecycleStatusV1
    decision_boundary_admitted: bool
    state_writeback_admitted: bool
    runtime_executed: bool
    simulation_only: bool
    provenance: Mapping[str, Any]
    trace_ref: str
    schema_version: str = COGNITIVE_ANALYSIS_SCHEMA_VERSION_V1
