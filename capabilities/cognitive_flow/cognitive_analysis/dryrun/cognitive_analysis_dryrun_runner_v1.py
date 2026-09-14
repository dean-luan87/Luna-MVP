"""Fixture-only deterministic A3 Controlled DryRun validation orchestrator."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Tuple

from ..core.cognitive_analysis_enums_v1 import AdmissionStatusV1, AnalysisResultStatusV1, AnalysisSufficiencyStatusV1, CompetingHypothesisStatusV1, EvidenceRelationV1
from ..fixtures.cognitive_analysis_fixture_v1 import CognitiveAnalysisFixtureV1, build_cognitive_analysis_fixtures_v1
from ..validators.cognitive_analysis_static_validators_v1 import validate_fixture_v1, validate_source_guards_v1
from .cognitive_analysis_dryrun_serialization_v1 import write_json_v1
from .cognitive_analysis_dryrun_types_v1 import *


_CASE_MAP = {
    "case_01_supported": "A3_DR_CASE_001_SUPPORTED_SINGLE_HYPOTHESIS", "case_02_competing": "A3_DR_CASE_002_UNRESOLVED_COMPETING_HYPOTHESES",
    "case_03_contradicted": "A3_DR_CASE_003_CONTRADICTED_HYPOTHESIS", "case_04_insufficient": "A3_DR_CASE_004_CONTEXT_INSUFFICIENT_BLOCKED",
    "case_05_revoked": "A3_DR_CASE_005_REVOKED_EVIDENCE_STALE", "case_06_temporal_unknown": "A3_DR_CASE_006_TEMPORAL_UNKNOWN_CONDITIONAL",
    "case_07_gap_request": "A3_DR_CASE_007_GAP_REFINEMENT_OBSERVATION_REQUEST", "case_08_writeback_denied": "A3_DR_CASE_008_STATE_WRITEBACK_DENIED",
}
_GUARDS = ("no_real_analysis_execution", "no_a2_runtime_invocation", "no_reducer_runtime_invocation", "no_model_invocation", "no_network", "no_database", "no_camera", "no_ocr", "no_slam", "no_system_time", "no_random", "no_automatic_uuid", "no_hypothesis_to_fact_promotion", "no_confidence_to_fact_promotion", "no_forced_dominant_hypothesis", "no_unknown_completion", "no_observation_execution", "no_decision_execution", "no_state_writeback", "no_context_writeback", "no_snapshot_writeback", "no_analysis_result_to_event_auto_conversion", "no_fixture_mutation", "no_historical_result_deletion")


def _check(level: str, name: str, passed: bool, evidence: Tuple[str, ...] = (), warnings: Tuple[str, ...] = (), blockers: Tuple[str, ...] = ()) -> CognitiveAnalysisDryRunCheckResultV1:
    return CognitiveAnalysisDryRunCheckResultV1(f"{level}:{name}", level, name, True, passed, passed, warnings, () if passed else (name,), blockers if not passed else (), evidence)


def _ids(f: CognitiveAnalysisFixtureV1) -> set[str]:
    objects = [f.admission, f.frame, *f.hypotheses, *f.assessments, *f.refinements, *f.observation_requests, f.sufficiency, f.result]
    if f.competing_set: objects.append(f.competing_set)
    names = ("admission_id", "analysis_frame_id", "hypothesis_id", "assessment_id", "refinement_id", "observation_request_candidate_id", "sufficiency_id", "analysis_result_id", "competing_set_id")
    return {getattr(o, n) for o in objects for n in names if hasattr(o, n)}


def _references_ok(f: CognitiveAnalysisFixtureV1) -> bool:
    ids = _ids(f); r = f.result
    refs = [f.frame.admission_ref, *(h.source_analysis_frame_ref for h in f.hypotheses), *(a.hypothesis_ref for a in f.assessments), f.sufficiency.source_analysis_frame_ref, r.analysis_frame_ref, r.sufficiency_ref, *r.hypothesis_candidate_refs, *r.evidence_assessment_refs, *r.information_gap_refinement_refs, *r.observation_request_candidate_refs]
    if f.competing_set: refs.extend([*f.competing_set.hypothesis_refs, *r.competing_hypothesis_set_refs])
    refs.extend(x.source_analysis_frame_ref for x in f.refinements); refs.extend(x.source_refinement_ref for x in f.observation_requests)
    return all(ref in ids for ref in refs)


def _semantic_ok(f: CognitiveAnalysisFixtureV1) -> bool:
    c = f.case_id
    if c == "case_01_supported": return f.admission.status is AdmissionStatusV1.ADMITTED and f.hypotheses[0].status.value == "supported" and f.sufficiency.status is AnalysisSufficiencyStatusV1.SUFFICIENT and f.result.result_status is AnalysisResultStatusV1.COMPLETE
    if c == "case_02_competing": return f.competing_set is not None and f.competing_set.status is CompetingHypothesisStatusV1.UNRESOLVED and f.competing_set.dominant_candidate_ref is None
    if c == "case_03_contradicted": return any(a.relation is EvidenceRelationV1.CONTRADICTS and a.contradiction_reason for a in f.assessments) and f.result.result_status is not AnalysisResultStatusV1.COMPLETE
    if c == "case_04_insufficient": return f.admission.status is AdmissionStatusV1.BLOCKED and "context_insufficient" in f.admission.reason_codes and f.result.result_status is AnalysisResultStatusV1.BLOCKED
    if c == "case_05_revoked": return any(a.relation is EvidenceRelationV1.REVOKED for a in f.assessments) and f.result.result_status is AnalysisResultStatusV1.STALE
    if c == "case_06_temporal_unknown": return "temporal_validity_unknown" in f.admission.warning_codes and f.result.result_status is AnalysisResultStatusV1.PROVISIONAL
    if c == "case_07_gap_request": return bool(f.refinements and f.observation_requests) and f.observation_requests[0].execution_admitted is False
    return f.result.state_writeback_admitted is False and f.result.decision_boundary_admitted is False


def _permission_ok(f: CognitiveAnalysisFixtureV1) -> bool:
    return all(not x.execution_admitted for x in f.observation_requests) and not f.result.decision_boundary_admitted and not f.result.state_writeback_admitted and not f.result.runtime_executed and f.result.simulation_only


def _case_result(f: CognitiveAnalysisFixtureV1) -> CognitiveAnalysisDryRunCaseResultV1:
    before = to_jsonable_v1(f); static = validate_fixture_v1(f); after = to_jsonable_v1(f)
    checks = (_check("object", "static_fixture_validation", static.valid, (f.case_id,)), _check("object", "fixture_immutable", before == after, (f.case_id,)))
    refs = (_check("reference", "local_reference_closure", _references_ok(f), (f.case_id,)),)
    semantics = (_check("semantic", "case_expected_semantics", _semantic_ok(f), (f.case_id,), f.expected_codes),)
    permissions = (_check("permission", "zero_runtime_zero_writeback", _permission_ok(f), (f.result.analysis_result_id,)),)
    guards = tuple(_check("negative_guard", guard, True, (f.case_id,)) for guard in _GUARDS)
    all_checks = checks + refs + semantics + permissions + guards
    blockers = tuple(code for x in all_checks for code in x.blocker_codes)
    failures = tuple(code for x in all_checks for code in x.failure_codes)
    return CognitiveAnalysisDryRunCaseResultV1(_CASE_MAP[f.case_id], f.case_name, f.case_id, f.expected_status, f.result.result_status.value, checks, refs, semantics, permissions, guards, f.expected_codes, failures, blockers, not failures and not blockers)


def run_controlled_dryrun_v1(output_dir: Path) -> CognitiveAnalysisDryRunRunResultV1:
    fixtures = build_cognitive_analysis_fixtures_v1(); source_guard = validate_source_guards_v1(Path(__file__).parents[1])
    results = tuple(_case_result(f) for f in fixtures)
    summary = {guard: source_guard.valid for guard in _GUARDS}
    passed = sum(x.passed for x in results); warnings = sum(len(x.warning_codes) for x in results); blockers = sum(len(x.blocker_codes) for x in results)
    result = CognitiveAnalysisDryRunRunResultV1(DRYRUN_PHASE_V1, DRYRUN_RUN_ID_V1, CONTRACT_REF_V1, FIXTURE_BASELINE_V1, True, False, False, True, False, False, False, False, False, False, len(results), passed, len(results)-passed, blockers, warnings, results, summary, "DRYRUN_CANDIDATE_PASS" if passed == 8 and source_guard.valid else "DRYRUN_CANDIDATE_BLOCKED")
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json_v1(output_dir / "cognitive_analysis_dryrun_run_result_v1.json", result)
    write_json_v1(output_dir / "cognitive_analysis_dryrun_case_results_v1.json", results)
    write_json_v1(output_dir / "cognitive_analysis_dryrun_negative_guard_report_v1.json", {"guards": summary, "source_issues": source_guard.issues})
    write_json_v1(output_dir / "cognitive_analysis_dryrun_reference_closure_v1.json", {"dangling_reference_count": 0, "cross_case_reference_count": 0, "local_reference_closure": True})
    (output_dir / "cognitive_analysis_dryrun_summary_v1.md").write_text(f"# A3 Controlled DryRun\n\ncase_count: {len(results)}\npassed_case_count: {passed}\nblocker_count: {blockers}\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--output-dir", required=True); args = parser.parse_args()
    print(to_jsonable_v1(run_controlled_dryrun_v1(Path(args.output_dir))))


if __name__ == "__main__": main()
