"""Metadata-only integrated closure governance.

No phase Runner, Verifier, provider, model, or runtime is imported or called.
Closure consumes explicit user-terminal evidence records only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple

from ..brain_golden_baseline_governance_v1 import (
    EXPECTED_PHASES,
    EXPECTED_REGRESSION_COUNTS,
    REPO_ROOT,
    load_baseline_snapshot,
    normalized_phase_index,
    validate_baseline,
)
from .integrated_closure_types_v1 import (
    FREEZE_STATES,
    VERIFICATION_STATUSES,
    FreezeCandidateV1,
    RegressionEvidenceRecordV1,
)


REGISTERED_EVIDENCE_PATH = REPO_ROOT / "docs" / "architecture" / "luna_brain_integrated_golden_baseline_closure_v1" / "terminal_evidence_registration_v1.json"


REQUIRED_SUITE_IDS = (
    "S3-Y11",
    "B1",
    "B2",
    "B3",
    "B4",
    "C01-C36",
    "O01-O36",
    "INTENT-S01-S12",
    "DECISION-D01-D14",
    "TASK-B3-SUBRANGE",
)

REQUIRED_CANDIDATE_TRUTH = (
    "Visual Evidence != Fact",
    "CurrentWorldCandidate != World Truth",
    "Hypothesis != Fact",
    "Intent Candidate != guaranteed Intent execution",
    "Decision Candidate != Action",
    "TaskCandidate != Runtime",
    "ActionCandidate != Runtime execution",
    "Controlled Runtime Result != real execution",
    "Outcome Candidate != World Truth",
    "Task success candidate != verified external success",
)

REQUIRED_TRACE_CLASSES = (
    "trace_refs",
    "provenance_refs",
    "temporal_refs",
    "uncertainty_refs",
    "conflict_refs",
    "contradiction_refs",
)

MUTATION_OWNERS = {
    "Field State": "Field State Reducer",
    "Intent": "Intent Governance",
    "Task": "Task Manager",
    "Action": "Action Governance",
    "Runtime execution/result": "Runtime Executor",
    "Outcome": "Outcome Evaluation Governance",
    "Memory/Experience": "Cognitive Memory & Experience Governance",
    "Learning": "Cognitive Learning Governance",
}

CANONICAL_OWNERS = {
    "Visual Evidence": "Field Perception Orchestrator / Vision Provider Integration",
    "Observation Gateway": "Observation Gateway Governance",
    "Context": "Context Foundation",
    "Field Event": "Field Event Admission",
    "Field State": "Field State Reducer",
    "Current World candidate": "Cognitive State Formation / Current World representation",
    "Cognitive State": "Cognitive State Formation Governance",
    "Cognitive Flow": "Cognitive Flow Governance",
    "Attention": "Cognitive Attention Governance",
    "Hypothesis": "Cognitive Hypothesis Governance",
    "PCN": "Personal Cognitive Network Governance",
    "Intent": "Intent Governance",
    "Decision": "Decision Governance",
    "Task": "Task Manager",
    "Action": "Action Governance",
    "Runtime execution/result": "Runtime Executor",
    "Outcome": "Outcome Evaluation Governance",
    "Observation Need/Reobserve": "FPO / Active Observation Control",
    "Memory/Experience": "Cognitive Memory & Experience Governance",
    "Learning": "Cognitive Learning Governance",
}

ROUTE_MATRIX = (
    {
        "edge_id": "S3_TO_B1",
        "upstream": "S3-Y11",
        "downstream": "B1",
        "output_refs": ("VisualDetectionEvidenceCandidateV1",),
        "input_refs": ("VisualDetectionEvidenceCandidateV1", "ObservationGatewayEvidenceHandoffCandidateV1"),
        "mapping_declared": True,
        "direct_owner_bypass": False,
    },
    {
        "edge_id": "B1_TO_B2",
        "upstream": "B1",
        "downstream": "B2",
        "output_refs": ("CurrentWorldCandidateV1",),
        "input_refs": ("CurrentWorldCandidateV1",),
        "mapping_declared": True,
        "direct_owner_bypass": False,
    },
    {
        "edge_id": "B2_TO_B3",
        "upstream": "B2",
        "downstream": "B3",
        "output_refs": ("Cognitive State", "Cognitive Flow", "Attention", "Hypothesis"),
        "input_refs": ("validated B2 refs",),
        "mapping_declared": True,
        "direct_owner_bypass": False,
    },
    {
        "edge_id": "B3_TO_B4",
        "upstream": "B3",
        "downstream": "B4",
        "output_refs": ("Decision Candidate", "TaskCandidate", "Task readiness"),
        "input_refs": ("validated B3 refs",),
        "mapping_declared": True,
        "direct_owner_bypass": False,
    },
    {
        "edge_id": "B4_TO_BASELINE_FEEDBACK",
        "upstream": "B4",
        "downstream": "Golden Baseline feedback loop",
        "output_refs": ("Outcome", "Reconsideration", "Reobserve"),
        "input_refs": ("Observation Need", "FPO / Active Observation Control"),
        "mapping_declared": True,
        "direct_owner_bypass": False,
    },
)


def _suite_records(snapshot: Any) -> Dict[str, Mapping[str, Any]]:
    return {record["id"]: record for record in snapshot.regression_index.get("suites", [])}


def _empty_evidence(snapshot: Any) -> Dict[str, RegressionEvidenceRecordV1]:
    suites = _suite_records(snapshot)
    return {
        suite_id: RegressionEvidenceRecordV1.from_mapping({}, expected=suites[suite_id])
        for suite_id in REQUIRED_SUITE_IDS
    }


def load_terminal_evidence(path: Path | None = None) -> Dict[str, RegressionEvidenceRecordV1]:
    """Load explicit user-terminal records; absent input remains PENDING."""

    snapshot = load_baseline_snapshot()
    records = _empty_evidence(snapshot)
    if path is None and REGISTERED_EVIDENCE_PATH.exists():
        path = REGISTERED_EVIDENCE_PATH
    if path is None:
        return records
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    raw_records = payload.get("records", payload) if isinstance(payload, dict) else payload
    if not isinstance(raw_records, list):
        raise ValueError("terminal evidence must contain a records list")
    suites = _suite_records(snapshot)
    for raw in raw_records:
        if not isinstance(raw, dict) or raw.get("suite_id") not in suites:
            continue
        suite_id = raw["suite_id"]
        records[suite_id] = RegressionEvidenceRecordV1.from_mapping(raw, expected=suites[suite_id])
    return records


def _evidence_issues(records: Mapping[str, RegressionEvidenceRecordV1]) -> Tuple[str, ...]:
    issues: list[str] = []
    for suite_id in REQUIRED_SUITE_IDS:
        record = records.get(suite_id)
        if record is None:
            issues.append(f"{suite_id}:EVIDENCE_RECORD_MISSING")
            continue
        if record.verification_status not in VERIFICATION_STATUSES:
            issues.append(f"{suite_id}:INVALID_VERIFICATION_STATUS")
        if record.verification_status != "VERIFIED":
            issues.append(f"{suite_id}:USER_TERMINAL_VERIFICATION_REQUIRED")
            continue
        if not record.verified_by_user_terminal:
            issues.append(f"{suite_id}:NOT_VERIFIED_BY_USER_TERMINAL")
        if record.expected_scenario_count != "not independently declared; B3-16..B3-20 and B3-26":
            if record.observed_scenario_count != record.expected_scenario_count:
                issues.append(f"{suite_id}:SCENARIO_COUNT_MISMATCH")
        if record.all_cases_passed is not True:
            issues.append(f"{suite_id}:CASES_NOT_PASSING")
        if record.failed_case_ids:
            issues.append(f"{suite_id}:FAILED_CASES_PRESENT")
        if record.blocker_count != 0:
            issues.append(f"{suite_id}:BLOCKERS_PRESENT")
        if not record.artifact_ref:
            issues.append(f"{suite_id}:ARTIFACT_REFERENCE_MISSING")
        if record.expected_scenario_count == "not independently declared; B3-16..B3-20 and B3-26":
            if record.coverage_mode != "B3_SUBSCOPE":
                issues.append(f"{suite_id}:TASK_COVERAGE_MODE_MISSING")
            if record.subscope_refs != ("B3-16", "B3-17", "B3-18", "B3-19", "B3-20", "B3-26"):
                issues.append(f"{suite_id}:TASK_SUBSCOPE_MISMATCH")
    return tuple(issues)


def _continuity_checks(snapshot: Any) -> Dict[str, bool]:
    phases = tuple(item.get("phase_id") for item in normalized_phase_index(snapshot))
    phase_ok = phases == EXPECTED_PHASES
    suites = _suite_records(snapshot)
    indexed = all(suite_id in suites for suite_id in REQUIRED_SUITE_IDS)
    route_ok = all(
        edge["mapping_declared"]
        and not edge["direct_owner_bypass"]
        and edge["output_refs"]
        and edge["input_refs"]
        for edge in ROUTE_MATRIX
    )
    owner_records = snapshot.owner_matrix.get("owners", [])
    owner_by_concept = {item.get("concept"): item for item in owner_records}
    owner_ok = len(owner_by_concept) == len(owner_records) and all(
        owner_by_concept.get(concept, {}).get("owner") == expected_owner
        for concept, expected_owner in CANONICAL_OWNERS.items()
    )
    mutation_ok = owner_ok and all(
        MUTATION_OWNERS[concept]
        in (
            str(owner_by_concept[concept].get("owner", ""))
            + " "
            + str(owner_by_concept[concept].get("mutation_authority", ""))
        )
        for concept in MUTATION_OWNERS
    )
    candidate_data = snapshot.candidate_truth
    candidate_asset = snapshot.real_synthetic
    candidate_ok = set(candidate_data.get("invariants", ())) == set(REQUIRED_CANDIDATE_TRUTH)
    candidate_ok = candidate_ok and candidate_data.get("natural_language_conclusion") is False
    trace_classes = set(snapshot.trace.get("required_reference_classes", ()))
    trace_ok = set(REQUIRED_TRACE_CLASSES).issubset(trace_classes) and snapshot.trace.get("provenance_grants_authority") is False
    boundary_ok = bool(candidate_asset.get("real_components")) and bool(candidate_asset.get("controlled_or_synthetic_components"))
    feedback = snapshot.feedback
    feedback_ok = (
        "Observation Need" in feedback.get("route", "")
        and feedback.get("reconsideration_is_retry") is False
        and feedback.get("provider_invocation_from_cognition") is False
        and feedback.get("automatic_camera_activation") is False
        and feedback.get("provider_autonomy") is False
    )
    guard_ok = not validate_baseline(snapshot)
    return {
        "phase_membership_complete": phase_ok,
        "required_regression_suites_indexed": indexed,
        "cross_phase_contract_continuity": route_ok,
        "owner_continuity": owner_ok,
        "mutation_continuity": mutation_ok,
        "candidate_truth_continuity": candidate_ok,
        "trace_provenance_continuity": trace_ok,
        "real_synthetic_continuity": boundary_ok,
        "feedback_loop_continuity": feedback_ok,
        "negative_guard_continuity": guard_ok,
    }


def evaluate_freeze_candidate(
    evidence: Mapping[str, RegressionEvidenceRecordV1],
    *,
    snapshot: Any | None = None,
) -> FreezeCandidateV1:
    snapshot = snapshot or load_baseline_snapshot()
    reasons = list(_evidence_issues(evidence))
    continuity = _continuity_checks(snapshot)
    reasons.extend(name for name, passed in continuity.items() if not passed)
    if reasons:
        return FreezeCandidateV1("NOT_READY", False, tuple(reasons), False)
    return FreezeCandidateV1("READY_TO_FREEZE", True, (), False)


def build_closure_result(evidence_path: Path | None = None) -> dict[str, Any]:
    snapshot = load_baseline_snapshot()
    evidence = load_terminal_evidence(evidence_path)
    continuity = _continuity_checks(snapshot)
    candidate = evaluate_freeze_candidate(evidence, snapshot=snapshot)
    return {
        "phase": "Phase-Luna-Brain-Integrated-Golden-Baseline-Closure-v1-001",
        "mode": "INTEGRATED_CLOSURE_ONLY",
        "owner": "Brain Golden Baseline Governance",
        "baseline_id": snapshot.manifest["manifest_id"],
        "required_suite_count": len(REQUIRED_SUITE_IDS),
        "required_suite_ids": list(REQUIRED_SUITE_IDS),
        "continuity": continuity,
        "terminal_evidence_required": True,
        "terminal_evidence_status": {suite_id: record.verification_status for suite_id, record in evidence.items()},
        "terminal_evidence_records": {suite_id: record.__dict__ for suite_id, record in evidence.items()},
        "freeze_candidate_state": candidate.state,
        "freeze_candidate_eligible": candidate.eligible,
        "freeze_candidate_reasons": list(candidate.reasons),
        "manifest_state_mutated": candidate.manifest_state_mutated,
        "automatic_regression_execution": False,
        "business_logic_execution": False,
        "provider_invocation": False,
        "runtime_execution": False,
    }
