"""Pure, deterministic validators for A3 Cognitive Analysis skeleton v1."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Tuple

from ..core.cognitive_analysis_enums_v1 import (
    AdmissionStatusV1, AnalysisResultStatusV1, AnalysisSufficiencyStatusV1,
    CompetingHypothesisStatusV1, EvidenceRelationV1, HypothesisStatusV1,
    LifecycleStatusV1,
)
from ..core.cognitive_analysis_invariants_v1 import (
    observation_request_invariant_issues_v1, result_boundary_invariant_issues_v1,
)
from ..core.cognitive_analysis_types_v1 import (
    AnalysisEvidenceAssessmentV1, CognitiveAnalysisAdmissionResultV1,
    CognitiveAnalysisFrameV1, CognitiveAnalysisResultV1,
    CognitiveAnalysisSufficiencyResultV1, CompetingHypothesisSetV1,
    HypothesisCandidateV1, InformationGapRefinementV1,
)
from ..fixtures.cognitive_analysis_fixture_v1 import CognitiveAnalysisFixtureV1


_BANNED_IMPORT_ROOTS_V1 = {
    "requests", "httpx", "socket", "sqlite3", "sqlalchemy", "pymongo", "redis",
    "random", "uuid", "datetime", "time", "subprocess", "urllib",
}
_BANNED_ATTRIBUTE_CALLS_V1 = {
    "now", "utcnow", "today", "time", "uuid1", "uuid4", "random", "randint", "randrange",
}


@dataclass(frozen=True)
class StaticValidationIssueV1:
    code: str
    object_ref: str
    message: str


@dataclass(frozen=True)
class StaticValidationResultV1:
    subject_ref: str
    issues: Tuple[StaticValidationIssueV1, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def _issue(code: str, object_ref: str, message: str) -> StaticValidationIssueV1:
    return StaticValidationIssueV1(code, object_ref, message)


def _missing_refs(object_ref: str, values: Mapping[str, str | None]) -> Tuple[StaticValidationIssueV1, ...]:
    return tuple(
        _issue(f"missing_{name}", object_ref, f"{name} must be a non-empty reference")
        for name, value in values.items()
        if not isinstance(value, str) or not value.strip()
    )


def validate_admission_v1(admission: CognitiveAnalysisAdmissionResultV1) -> Tuple[StaticValidationIssueV1, ...]:
    issues = list(_missing_refs(admission.admission_id, {
        "source_context_ref": admission.source_context_ref,
        "source_context_version": admission.source_context_version,
        "trace_ref": admission.trace_ref,
    }))
    if not isinstance(admission.status, AdmissionStatusV1):
        issues.append(_issue("invalid_admission_status", admission.admission_id, "status must be AdmissionStatusV1"))
    if admission.status is AdmissionStatusV1.ADMITTED and not admission.permission_allowed:
        issues.append(_issue("admitted_permission_required", admission.admission_id, "admitted requires permission"))
    if admission.status is AdmissionStatusV1.BLOCKED and not admission.reason_codes:
        issues.append(_issue("blocked_reason_required", admission.admission_id, "blocked requires reason_codes"))
    if admission.context_sufficiency_status is AnalysisSufficiencyStatusV1.INSUFFICIENT and admission.status is AdmissionStatusV1.ADMITTED:
        issues.append(_issue("insufficient_context_not_admitted", admission.admission_id, "insufficient Context cannot be admitted"))
    if admission.context_stale and admission.status is AdmissionStatusV1.ADMITTED and not admission.warning_codes:
        issues.append(_issue("stale_context_warning_required", admission.admission_id, "stale admitted Context requires warning"))
    if admission.evidence_revoked and not (admission.warning_codes or admission.reason_codes):
        issues.append(_issue("revoked_evidence_signal_required", admission.admission_id, "revoked evidence requires warning or reason"))
    return tuple(issues)


def validate_frame_v1(frame: CognitiveAnalysisFrameV1) -> Tuple[StaticValidationIssueV1, ...]:
    issues = list(_missing_refs(frame.analysis_frame_id, {
        "analysis_version": frame.analysis_version,
        "source_context_ref": frame.source_context_ref,
        "source_context_version": frame.source_context_version,
        "admission_ref": frame.admission_ref,
        "trace_ref": frame.trace_ref,
    }))
    if not isinstance(frame.lifecycle_status, LifecycleStatusV1):
        issues.append(_issue("invalid_frame_lifecycle", frame.analysis_frame_id, "lifecycle must be controlled"))
    return tuple(issues)


def validate_hypothesis_v1(hypothesis: HypothesisCandidateV1, revoked_refs: Tuple[str, ...]) -> Tuple[StaticValidationIssueV1, ...]:
    issues = list(_missing_refs(hypothesis.hypothesis_id, {
        "hypothesis_version": hypothesis.hypothesis_version,
        "statement": hypothesis.statement,
        "source_context_ref": hypothesis.source_context_ref,
        "source_analysis_frame_ref": hypothesis.source_analysis_frame_ref,
        "trace_ref": hypothesis.trace_ref,
    }))
    if not isinstance(hypothesis.status, HypothesisStatusV1):
        issues.append(_issue("invalid_hypothesis_status", hypothesis.hypothesis_id, "status must be controlled"))
    if set(hypothesis.supporting_evidence_refs).intersection(revoked_refs):
        issues.append(_issue("revoked_evidence_cannot_support", hypothesis.hypothesis_id, "revoked evidence cannot remain support"))
    return tuple(issues)


def validate_competing_set_v1(competing_set: CompetingHypothesisSetV1 | None) -> Tuple[StaticValidationIssueV1, ...]:
    if competing_set is None:
        return ()
    issues = list(_missing_refs(competing_set.competing_set_id, {
        "analysis_question": competing_set.analysis_question,
        "source_context_ref": competing_set.source_context_ref,
        "source_analysis_frame_ref": competing_set.source_analysis_frame_ref,
        "trace_ref": competing_set.trace_ref,
    }))
    if len(competing_set.hypothesis_refs) < 2:
        issues.append(_issue("competing_set_requires_two_hypotheses", competing_set.competing_set_id, "set requires at least two hypotheses"))
    if competing_set.dominant_candidate_ref and competing_set.dominant_candidate_ref not in competing_set.hypothesis_refs:
        issues.append(_issue("dominant_candidate_not_member", competing_set.competing_set_id, "dominant must be a member"))
    if competing_set.status is CompetingHypothesisStatusV1.UNRESOLVED and competing_set.dominant_candidate_ref:
        issues.append(_issue("unresolved_set_cannot_force_dominant", competing_set.competing_set_id, "unresolved set must not force dominant"))
    return tuple(issues)


def validate_assessment_v1(assessment: AnalysisEvidenceAssessmentV1) -> Tuple[StaticValidationIssueV1, ...]:
    issues = list(_missing_refs(assessment.assessment_id, {
        "evidence_ref": assessment.evidence_ref,
        "hypothesis_ref": assessment.hypothesis_ref,
        "trace_ref": assessment.trace_ref,
    }))
    if not isinstance(assessment.relation, EvidenceRelationV1):
        issues.append(_issue("invalid_evidence_relation", assessment.assessment_id, "relation must be controlled"))
    if assessment.relation is EvidenceRelationV1.REVOKED and assessment.lifecycle_status is not LifecycleStatusV1.REVOKED:
        issues.append(_issue("revoked_assessment_lifecycle_required", assessment.assessment_id, "revoked relation requires revoked lifecycle"))
    return tuple(issues)


def validate_refinement_v1(refinement: InformationGapRefinementV1) -> Tuple[StaticValidationIssueV1, ...]:
    issues = list(_missing_refs(refinement.refinement_id, {
        "source_analysis_frame_ref": refinement.source_analysis_frame_ref,
        "refined_question": refinement.refined_question,
        "required_information_type": refinement.required_information_type,
        "trace_ref": refinement.trace_ref,
    }))
    if not refinement.newly_discovered and not refinement.source_gap_ref:
        issues.append(_issue("source_gap_required", refinement.refinement_id, "existing gap refinement needs source_gap_ref"))
    return tuple(issues)


def validate_sufficiency_v1(sufficiency: CognitiveAnalysisSufficiencyResultV1) -> Tuple[StaticValidationIssueV1, ...]:
    issues = list(_missing_refs(sufficiency.sufficiency_id, {
        "source_context_ref": sufficiency.source_context_ref,
        "source_analysis_frame_ref": sufficiency.source_analysis_frame_ref,
        "context_sufficiency_ref": sufficiency.context_sufficiency_ref,
        "trace_ref": sufficiency.trace_ref,
    }))
    if sufficiency.unresolved_critical_gap_refs and sufficiency.status is AnalysisSufficiencyStatusV1.SUFFICIENT:
        issues.append(_issue("critical_gap_prevents_sufficient", sufficiency.sufficiency_id, "critical gaps prevent sufficient status"))
    if sufficiency.revoked_evidence_refs and not (sufficiency.warning_codes or sufficiency.reason_codes):
        issues.append(_issue("revoked_evidence_must_be_reflected", sufficiency.sufficiency_id, "revocation needs reason or warning"))
    if sufficiency.temporal_validity == "unknown" and sufficiency.status is AnalysisSufficiencyStatusV1.SUFFICIENT:
        issues.append(_issue("unknown_time_not_sufficient", sufficiency.sufficiency_id, "unknown time cannot silently be sufficient"))
    return tuple(issues)


def validate_result_v1(result: CognitiveAnalysisResultV1) -> Tuple[StaticValidationIssueV1, ...]:
    issues = list(_missing_refs(result.analysis_result_id, {
        "analysis_version": result.analysis_version,
        "source_context_ref": result.source_context_ref,
        "source_context_version": result.source_context_version,
        "analysis_frame_ref": result.analysis_frame_ref,
        "sufficiency_ref": result.sufficiency_ref,
        "trace_ref": result.trace_ref,
    }))
    if not isinstance(result.result_status, AnalysisResultStatusV1):
        issues.append(_issue("invalid_result_status", result.analysis_result_id, "result status must be controlled"))
    for code in result_boundary_invariant_issues_v1(result):
        issues.append(_issue(code, result.analysis_result_id, "A3 boundary invariant violated"))
    return tuple(issues)


def validate_fixture_v1(fixture: CognitiveAnalysisFixtureV1) -> StaticValidationResultV1:
    """Validate fixture objects only; this function performs no analysis."""
    issues = list(validate_admission_v1(fixture.admission))
    issues.extend(validate_frame_v1(fixture.frame))
    revoked = tuple(item.evidence_ref for item in fixture.assessments if item.relation is EvidenceRelationV1.REVOKED)
    for hypothesis in fixture.hypotheses:
        issues.extend(validate_hypothesis_v1(hypothesis, revoked))
    issues.extend(validate_competing_set_v1(fixture.competing_set))
    for assessment in fixture.assessments:
        issues.extend(validate_assessment_v1(assessment))
    for refinement in fixture.refinements:
        issues.extend(validate_refinement_v1(refinement))
    for request in fixture.observation_requests:
        for code in observation_request_invariant_issues_v1(request):
            issues.append(_issue(code, request.observation_request_candidate_id, "request must remain candidate-only"))
    issues.extend(validate_sufficiency_v1(fixture.sufficiency))
    issues.extend(validate_result_v1(fixture.result))
    return StaticValidationResultV1(fixture.case_id, tuple(issues))


def validate_fixture_collection_v1(fixtures: Iterable[CognitiveAnalysisFixtureV1]) -> Mapping[str, StaticValidationResultV1]:
    """Return deterministic validation results indexed by fixed case id."""
    return {fixture.case_id: validate_fixture_v1(fixture) for fixture in fixtures}


def validate_source_guards_v1(source_root: Path) -> StaticValidationResultV1:
    """Use AST-only source inspection for forbidden runtime capability imports/calls."""
    issues = []
    for path in sorted(source_root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    if root in _BANNED_IMPORT_ROOTS_V1:
                        issues.append(_issue("forbidden_import", path.name, root))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in _BANNED_ATTRIBUTE_CALLS_V1:
                issues.append(_issue("forbidden_time_random_or_uuid_call", path.name, node.func.attr))
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and "writeback" in node.name.lower():
                issues.append(_issue("forbidden_writeback_helper", path.name, node.name))
    return StaticValidationResultV1("source_guard", tuple(issues))
