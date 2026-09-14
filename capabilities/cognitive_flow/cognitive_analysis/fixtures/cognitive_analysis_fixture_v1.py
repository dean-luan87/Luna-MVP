"""Fixed, deterministic object-construction fixtures for A3 skeleton v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Tuple

from ..core.cognitive_analysis_enums_v1 import (
    AdmissionStatusV1, AnalysisResultStatusV1, AnalysisSufficiencyStatusV1,
    BlockingLevelV1, CompetingHypothesisStatusV1, EvidenceRelationV1,
    HypothesisStatusV1, HypothesisTypeV1, InformationGapTypeV1,
    LifecycleStatusV1,
)
from ..core.cognitive_analysis_types_v1 import (
    AnalysisEvidenceAssessmentV1, CognitiveAnalysisAdmissionResultV1,
    CognitiveAnalysisFrameV1, CognitiveAnalysisResultV1,
    CognitiveAnalysisSufficiencyResultV1, CompetingHypothesisSetV1,
    HypothesisCandidateV1, InformationGapRefinementV1,
    ObservationRequestCandidateV1,
)


@dataclass(frozen=True)
class CognitiveAnalysisFixtureV1:
    """One fixture-only case; construction is not cognitive analysis."""

    case_id: str
    case_name: str
    admission: CognitiveAnalysisAdmissionResultV1
    frame: CognitiveAnalysisFrameV1
    hypotheses: Tuple[HypothesisCandidateV1, ...]
    competing_set: CompetingHypothesisSetV1 | None
    assessments: Tuple[AnalysisEvidenceAssessmentV1, ...]
    refinements: Tuple[InformationGapRefinementV1, ...]
    observation_requests: Tuple[ObservationRequestCandidateV1, ...]
    sufficiency: CognitiveAnalysisSufficiencyResultV1
    result: CognitiveAnalysisResultV1
    expected_status: str
    expected_codes: Tuple[str, ...]
    negative_guards: Tuple[str, ...]
    stop_condition: str


def _provenance(case_id: str) -> Mapping[str, Any]:
    return {"fixture": "fixed", "case_id": case_id, "simulation_only": True}


def _frame(case_id: str, context_version: str, admission_ref: str, unknowns: Tuple[str, ...] = ()) -> CognitiveAnalysisFrameV1:
    return CognitiveAnalysisFrameV1(
        analysis_frame_id=f"analysis_frame:{case_id}", analysis_version="v1",
        source_context_ref=f"context:{case_id}", source_context_version=context_version,
        analysis_subject_ref="subject:fixture", task_ref="task:fixture", goal_ref="goal:fixture",
        analysis_scope={"fixture_case": case_id}, temporal_scope={"time_ref": "fixed:2026-07-22T00:00:00Z"},
        selected_evidence_refs=("evidence:primary",), selected_relation_refs=("relation:fixture",),
        known_constraint_refs=("constraint:fixture",), unknown_refs=unknowns,
        admission_ref=admission_ref, previous_analysis_frame_ref=None,
        lifecycle_status=LifecycleStatusV1.ACTIVE, provenance=_provenance(case_id),
        trace_ref=f"trace:{case_id}:frame",
    )


def _hypothesis(case_id: str, frame_ref: str, *, suffix: str, status: HypothesisStatusV1, support: Tuple[str, ...], contradict: Tuple[str, ...] = ()) -> HypothesisCandidateV1:
    return HypothesisCandidateV1(
        hypothesis_id=f"hypothesis:{case_id}:{suffix}", hypothesis_version="v1",
        hypothesis_type=HypothesisTypeV1.STATE_INTERPRETATION,
        statement=f"fixture hypothesis {suffix} for {case_id}", source_context_ref=f"context:{case_id}",
        source_analysis_frame_ref=frame_ref, source_evidence_refs=("evidence:primary",),
        supporting_evidence_refs=support, contradicting_evidence_refs=contradict,
        assumption_refs=("assumption:fixture",), uncertainty={"status": "explicit"},
        confidence_candidate="fixture_only", status=status, previous_hypothesis_ref=None,
        supersedes_hypothesis_ref=None, lifecycle_status=LifecycleStatusV1.ACTIVE,
        provenance=_provenance(case_id), trace_ref=f"trace:{case_id}:hypothesis:{suffix}",
    )


def _assessment(case_id: str, hypothesis_ref: str, relation: EvidenceRelationV1, evidence_ref: str = "evidence:primary") -> AnalysisEvidenceAssessmentV1:
    return AnalysisEvidenceAssessmentV1(
        assessment_id=f"assessment:{case_id}:{hypothesis_ref.rsplit(':', 1)[-1]}",
        assessment_version="v1", evidence_ref=evidence_ref, hypothesis_ref=hypothesis_ref,
        relation=relation, strength_candidate="fixture", reliability_candidate="fixture",
        temporal_relevance="declared", scope_relevance="declared",
        contradiction_reason="fixture_contradiction" if relation is EvidenceRelationV1.CONTRADICTS else None,
        uncertainty={"status": "explicit"},
        lifecycle_status=LifecycleStatusV1.REVOKED if relation is EvidenceRelationV1.REVOKED else LifecycleStatusV1.ACTIVE,
        provenance=_provenance(case_id), trace_ref=f"trace:{case_id}:assessment",
    )


def _sufficiency(case_id: str, frame_ref: str, status: AnalysisSufficiencyStatusV1, *, gaps: Tuple[str, ...] = (), revoked: Tuple[str, ...] = (), warnings: Tuple[str, ...] = ()) -> CognitiveAnalysisSufficiencyResultV1:
    return CognitiveAnalysisSufficiencyResultV1(
        sufficiency_id=f"analysis_sufficiency:{case_id}", source_context_ref=f"context:{case_id}",
        source_analysis_frame_ref=frame_ref, status=status,
        context_sufficiency_ref=f"context_sufficiency:{case_id}",
        evidence_coverage={"fixture": "declared"}, contradiction_level="declared",
        unresolved_critical_gap_refs=gaps, temporal_validity="unknown" if "temporal_validity_unknown" in warnings else "declared",
        revoked_evidence_refs=revoked, permission_restriction_refs=(), hypothesis_stability="declared",
        provenance_complete=True, trace_complete=True, reason_codes=gaps,
        warning_codes=warnings, provenance=_provenance(case_id), trace_ref=f"trace:{case_id}:sufficiency",
    )


def _result(case_id: str, frame: CognitiveAnalysisFrameV1, hypotheses: Tuple[HypothesisCandidateV1, ...], assessments: Tuple[AnalysisEvidenceAssessmentV1, ...], sufficiency: CognitiveAnalysisSufficiencyResultV1, *, status: AnalysisResultStatusV1, sets: Tuple[str, ...] = (), refinements: Tuple[str, ...] = (), requests: Tuple[str, ...] = (), unresolved: Tuple[str, ...] = ()) -> CognitiveAnalysisResultV1:
    return CognitiveAnalysisResultV1(
        analysis_result_id=f"analysis_result:{case_id}", analysis_version="v1",
        source_context_ref=frame.source_context_ref, source_context_version=frame.source_context_version,
        analysis_frame_ref=frame.analysis_frame_id,
        hypothesis_candidate_refs=tuple(item.hypothesis_id for item in hypotheses),
        competing_hypothesis_set_refs=sets,
        evidence_assessment_refs=tuple(item.assessment_id for item in assessments),
        information_gap_refinement_refs=refinements,
        observation_request_candidate_refs=requests, sufficiency_ref=sufficiency.sufficiency_id,
        provisional_interpretation="fixture candidate only", unresolved_questions=unresolved,
        result_status=status, previous_analysis_result_ref=None, supersedes_analysis_result_ref=None,
        lifecycle_status=LifecycleStatusV1.STALE if status is AnalysisResultStatusV1.STALE else LifecycleStatusV1.ACTIVE,
        decision_boundary_admitted=False, state_writeback_admitted=False, runtime_executed=False,
        simulation_only=True, provenance=_provenance(case_id), trace_ref=f"trace:{case_id}:result",
    )


def _gap(case_id: str, frame_ref: str, *, request_ref: str | None = None, gap_type: InformationGapTypeV1 = InformationGapTypeV1.KNOWN_MISSING) -> InformationGapRefinementV1:
    return InformationGapRefinementV1(
        refinement_id=f"gap_refinement:{case_id}", source_gap_ref=f"gap:{case_id}",
        source_analysis_frame_ref=frame_ref, gap_type=gap_type, newly_discovered=False,
        refined_question=f"fixture missing information for {case_id}", required_information_type="fixture_information",
        target_field_refs=("field:fixture",), target_relation_refs=("relation:fixture",),
        priority_candidate="normal", blocking_level=BlockingLevelV1.CRITICAL,
        recommended_observation_scope={"scope": "candidate_only"},
        resolution_criteria=("fixture_resolution",), observation_request_candidate_ref=request_ref,
        lifecycle_status=LifecycleStatusV1.ACTIVE, provenance=_provenance(case_id),
        trace_ref=f"trace:{case_id}:gap",
    )


def _request(case_id: str, frame_ref: str, refinement_ref: str) -> ObservationRequestCandidateV1:
    return ObservationRequestCandidateV1(
        observation_request_candidate_id=f"observation_request:{case_id}",
        source_refinement_ref=refinement_ref, source_analysis_frame_ref=frame_ref,
        requested_information_type="fixture_information", requested_scope={"scope": "candidate_only"},
        target_refs=("field:fixture",), priority_candidate="normal",
        permission_requirement_refs=("permission:required",), execution_admitted=False,
        lifecycle_status=LifecycleStatusV1.ACTIVE, provenance=_provenance(case_id),
        trace_ref=f"trace:{case_id}:observation_request",
    )


def _build_case_v1(
    case_id: str, case_name: str, *, admission_status: AdmissionStatusV1,
    context_status: AnalysisSufficiencyStatusV1, result_status: AnalysisResultStatusV1,
    hypothesis_status: HypothesisStatusV1, relation: EvidenceRelationV1 = EvidenceRelationV1.SUPPORTS,
    warnings: Tuple[str, ...] = (), reasons: Tuple[str, ...] = (), gaps: Tuple[str, ...] = (),
    competing: bool = False, observation_request: bool = False,
) -> CognitiveAnalysisFixtureV1:
    admission = CognitiveAnalysisAdmissionResultV1(
        admission_id=f"analysis_admission:{case_id}", source_context_ref=f"context:{case_id}",
        source_context_version="v1", status=admission_status, reason_codes=reasons,
        blocking_gap_refs=gaps, warning_codes=warnings, permission_allowed=admission_status is not AdmissionStatusV1.REJECTED,
        provenance_complete=True, trace_complete=True, source_snapshot_traceable=True,
        lifecycle_status=LifecycleStatusV1.REFRESH_REQUIRED if "context_refresh_required" in warnings else LifecycleStatusV1.ACTIVE,
        context_sufficiency_status=context_status, context_stale="context_stale" in warnings,
        evidence_revoked="evidence_revoked" in warnings, provenance=_provenance(case_id),
        trace_ref=f"trace:{case_id}:admission",
    )
    frame = _frame(case_id, "v1", admission.admission_id, gaps)
    first = _hypothesis(case_id, frame.analysis_frame_id, suffix="a", status=hypothesis_status,
                        support=() if relation is EvidenceRelationV1.REVOKED else ("evidence:primary",),
                        contradict=("evidence:contradicting",) if relation is EvidenceRelationV1.CONTRADICTS else ())
    hypotheses = (first,)
    assessments = (_assessment(case_id, first.hypothesis_id, relation,
                               "evidence:revoked" if relation is EvidenceRelationV1.REVOKED else "evidence:primary"),)
    competing_set = None
    if competing:
        second = _hypothesis(case_id, frame.analysis_frame_id, suffix="b", status=HypothesisStatusV1.UNDERDETERMINED, support=("evidence:secondary",))
        hypotheses = (first, second)
        assessments = assessments + (_assessment(case_id, second.hypothesis_id, EvidenceRelationV1.SUPPORTS, "evidence:secondary"),)
        competing_set = CompetingHypothesisSetV1(
            competing_set_id=f"competing_set:{case_id}", analysis_question="fixture competing question",
            source_context_ref=frame.source_context_ref, source_analysis_frame_ref=frame.analysis_frame_id,
            hypothesis_refs=tuple(item.hypothesis_id for item in hypotheses),
            compatibility_records=({"left": first.hypothesis_id, "right": second.hypothesis_id, "relation": "mutually_exclusive"},),
            dominant_candidate_ref=None, unresolved_reason_codes=("competing_hypotheses_unresolved",),
            evidence_coverage={"fixture": "partial"}, status=CompetingHypothesisStatusV1.UNRESOLVED,
            lifecycle_status=LifecycleStatusV1.ACTIVE, provenance=_provenance(case_id), trace_ref=f"trace:{case_id}:competing",
        )
    request = _request(case_id, frame.analysis_frame_id, f"gap_refinement:{case_id}") if observation_request else None
    refinement = _gap(case_id, frame.analysis_frame_id, request_ref=request.observation_request_candidate_id if request else None) if gaps or request else None
    sufficiency = _sufficiency(
        case_id, frame.analysis_frame_id,
        AnalysisSufficiencyStatusV1.BLOCKED if admission_status is AdmissionStatusV1.BLOCKED else context_status,
        gaps=gaps, revoked=("evidence:revoked",) if relation is EvidenceRelationV1.REVOKED else (), warnings=warnings,
    )
    result = _result(
        case_id, frame, hypotheses, assessments, sufficiency, status=result_status,
        sets=(competing_set.competing_set_id,) if competing_set else (),
        refinements=(refinement.refinement_id,) if refinement else (),
        requests=(request.observation_request_candidate_id,) if request else (), unresolved=gaps,
    )
    return CognitiveAnalysisFixtureV1(
        case_id, case_name, admission, frame, hypotheses, competing_set, assessments,
        (refinement,) if refinement else (), (request,) if request else (), sufficiency, result,
        result_status.value, warnings + reasons,
        ("no_field_state_writeback", "no_action_execution", "simulation_only"),
        "fixture_objects_constructed_without_analysis_execution",
    )


def build_cognitive_analysis_fixtures_v1() -> Tuple[CognitiveAnalysisFixtureV1, ...]:
    """Build the eight fixed cases without inference, I/O, time, UUID, or random input."""
    return (
        _build_case_v1("case_01_supported", "sufficient_single_hypothesis", admission_status=AdmissionStatusV1.ADMITTED, context_status=AnalysisSufficiencyStatusV1.SUFFICIENT, result_status=AnalysisResultStatusV1.COMPLETE, hypothesis_status=HypothesisStatusV1.SUPPORTED),
        _build_case_v1("case_02_competing", "unresolved_competing_hypotheses", admission_status=AdmissionStatusV1.ADMITTED, context_status=AnalysisSufficiencyStatusV1.CONDITIONALLY_SUFFICIENT, result_status=AnalysisResultStatusV1.PROVISIONAL, hypothesis_status=HypothesisStatusV1.UNDERDETERMINED, warnings=("competing_hypotheses_unresolved",), competing=True),
        _build_case_v1("case_03_contradicted", "contradicted_hypothesis", admission_status=AdmissionStatusV1.ADMITTED, context_status=AnalysisSufficiencyStatusV1.CONDITIONALLY_SUFFICIENT, result_status=AnalysisResultStatusV1.PROVISIONAL, hypothesis_status=HypothesisStatusV1.CONTRADICTED, relation=EvidenceRelationV1.CONTRADICTS, warnings=("evidence_conflict",)),
        _build_case_v1("case_04_insufficient", "context_insufficient_blocked", admission_status=AdmissionStatusV1.BLOCKED, context_status=AnalysisSufficiencyStatusV1.INSUFFICIENT, result_status=AnalysisResultStatusV1.BLOCKED, hypothesis_status=HypothesisStatusV1.UNKNOWN, reasons=("context_insufficient",), gaps=("gap:critical",)),
        _build_case_v1("case_05_revoked", "revoked_evidence_stale", admission_status=AdmissionStatusV1.CONDITIONALLY_ADMITTED, context_status=AnalysisSufficiencyStatusV1.CONDITIONALLY_SUFFICIENT, result_status=AnalysisResultStatusV1.STALE, hypothesis_status=HypothesisStatusV1.UNDERDETERMINED, relation=EvidenceRelationV1.REVOKED, warnings=("evidence_revoked", "context_refresh_required")),
        _build_case_v1("case_06_temporal_unknown", "temporal_unknown_conditional", admission_status=AdmissionStatusV1.CONDITIONALLY_ADMITTED, context_status=AnalysisSufficiencyStatusV1.CONDITIONALLY_SUFFICIENT, result_status=AnalysisResultStatusV1.PROVISIONAL, hypothesis_status=HypothesisStatusV1.UNKNOWN, warnings=("temporal_validity_unknown",)),
        _build_case_v1("case_07_gap_request", "gap_refinement_observation_request", admission_status=AdmissionStatusV1.CONDITIONALLY_ADMITTED, context_status=AnalysisSufficiencyStatusV1.CONDITIONALLY_SUFFICIENT, result_status=AnalysisResultStatusV1.INCOMPLETE, hypothesis_status=HypothesisStatusV1.UNKNOWN, reasons=("critical_information_gap",), gaps=("gap:observation",), observation_request=True),
        _build_case_v1("case_08_writeback_denied", "state_writeback_denied", admission_status=AdmissionStatusV1.BLOCKED, context_status=AnalysisSufficiencyStatusV1.BLOCKED, result_status=AnalysisResultStatusV1.BLOCKED, hypothesis_status=HypothesisStatusV1.UNKNOWN, reasons=("analysis_blocked",)),
    )
