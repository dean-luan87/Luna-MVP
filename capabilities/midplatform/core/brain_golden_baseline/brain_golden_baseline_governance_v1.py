"""Deterministic, metadata-only Golden Baseline governance.

This module deliberately does not import phase runners, provider modules, or
runtime executors. It loads the already-reviewed B5 planning artifacts and
validates their references and invariants.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple

from .brain_golden_baseline_types_v1 import (
    BASELINE_ID,
    BASELINE_VERSION,
    COMPATIBILITY_STATUSES,
    BaselineIssue,
    BaselineSnapshot,
    ChangeImpact,
    CompatibilityDecision,
)


REPO_ROOT = Path(__file__).resolve().parents[4]
PLANNING_ROOT = REPO_ROOT / "docs" / "architecture" / (
    "luna_brain_b5_real_evidence_cognitive_loop_golden_baseline_planning_v1"
)

_REFERENCE_FILES = {
    "manifest": "golden_baseline_manifest_plan_v1.json",
    "inventory": "inventory_v1.json",
    "owner_matrix": "canonical_owner_matrix_v1.json",
    "regression_index": "regression_index_v1.json",
    "change_impact": "change_impact_matrix_v1.json",
    "compatibility": "compatibility_policy_v1.json",
    "guards": "negative_guard_baseline_v1.json",
    "trace": "trace_provenance_baseline_v1.json",
    "candidate_truth": "candidate_truth_boundary_v1.json",
    "feedback": "feedback_observation_loop_v1.json",
    "real_synthetic": "real_synthetic_boundary_v1.json",
    "deferred": "deferred_capabilities_v1.json",
}

EXPECTED_PHASES = ("S3-Y11", "B1", "B2", "B3", "B4")
EXPECTED_REGRESSION_COUNTS = {
    "S3-Y11": 19,
    "B1": 23,
    "B2": 24,
    "B3": 26,
    "B4": 28,
    "C01-C36": 36,
    "O01-O36": 36,
    "INTENT-S01-S12": 12,
    "DECISION-D01-D14": 14,
}

EXPECTED_GUARDS = {
    "provider_semantic_authority",
    "automatic_fact_admission",
    "direct_field_mutation",
    "current_world_truth_declaration",
    "hypothesis_as_fact",
    "cognitive_state_owns_intent",
    "direct_intent_mutation_outside_intent_governance",
    "decision_as_action",
    "task_as_action",
    "runtime_execution_in_b1_b4",
    "provider_invocation_from_cognitive_feedback",
    "automatic_retry",
    "hidden_cognitive_loop",
    "hidden_decision_loop",
    "hidden_task_loop",
    "memory_write",
    "experience_learning",
    "online_learning",
    "semantic_compression",
    "dynamic_cognitive_function_execution",
    "database_write",
    "vector_store_write",
    "embedding_execution",
    "ocr_execution",
    "slam_execution",
    "vio_execution",
    "vlm_execution",
    "real_action_execution",
    "device_control",
    "scheduler_execution",
}


def _read_json(path: Path) -> Mapping[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def load_baseline_snapshot() -> BaselineSnapshot:
    """Load the authoritative planning artifacts without executing them."""

    values: Dict[str, Mapping[str, Any]] = {}
    for key, filename in _REFERENCE_FILES.items():
        values[key] = _read_json(PLANNING_ROOT / filename)
    trace = dict(values["trace"])
    if "required_reference_classes" not in trace and "required_ref_classes" in trace:
        trace["required_reference_classes"] = list(trace["required_ref_classes"])
    values["trace"] = trace
    return BaselineSnapshot(**values)


def _issue(issues: list[BaselineIssue], code: str, detail: str) -> None:
    issues.append(BaselineIssue(code=code, detail=detail))


def _phase_index(snapshot: BaselineSnapshot) -> Sequence[Mapping[str, Any]]:
    phases = snapshot.inventory.get("phase_index", [])
    return phases if isinstance(phases, list) else []


def _suite_index(snapshot: BaselineSnapshot) -> Sequence[Mapping[str, Any]]:
    suites = snapshot.regression_index.get("suites", [])
    return suites if isinstance(suites, list) else []


def _normalized_phase_index(snapshot: BaselineSnapshot) -> Sequence[Mapping[str, Any]]:
    """Expose the phase fields required by B5 from existing indexed records.

    The planning inventory stores phase and regression metadata in separate
    records. This joins those existing references; it does not invent a new
    phase asset or modify a business contract.
    """

    suites = {item.get("id"): item for item in _suite_index(snapshot)}
    phase_boundaries = {
        "S3-Y11": {
            "candidate_truth_boundary": (
                "candidate_only_evidence",
                "truth_declared=false",
                "fact_admitted=false",
                "provider_semantic_authority=false",
            ),
            "mutation_boundary": (
                "single_frame_bounded",
                "no_provider_continuation",
                "no_downstream_field_world_intent_decision_task_mutation",
            ),
        },
        "B1": {
            "candidate_truth_boundary": (
                "gateway_admission_required",
                "candidate_only_current_world",
                "no_truth_promotion",
            ),
            "mutation_boundary": (
                "field_state_reducer_only",
                "field_state_mutation_not_executed",
                "current_world_direct_mutation=false",
            ),
        },
        "B2": {
            "candidate_truth_boundary": (
                "world_truth_promoted=false",
                "hypothesis_as_fact=false",
                "candidate_only_cognitive_state_and_flow",
            ),
            "mutation_boundary": (
                "current_world_read_only",
                "no_field_state_mutation",
                "no_intent_decision_task_mutation",
            ),
        },
        "B3": {
            "candidate_truth_boundary": (
                "potential_intent_not_active_intent",
                "decision_candidate_only",
                "task_candidate_only",
            ),
            "mutation_boundary": (
                "intent_governance_only",
                "decision_governance_only",
                "task_manager_only",
                "no_action_runtime_execution",
            ),
        },
        "B4": {
            "candidate_truth_boundary": (
                "controlled_runtime_result_fixture",
                "outcome_candidate_not_world_truth",
                "task_success_not_external_success",
            ),
            "mutation_boundary": (
                "no_action_execution",
                "no_runtime_execution",
                "no_task_direct_mutation_outside_task_manager",
                "no_memory_learning",
            ),
        },
    }
    normalized = []
    for phase in _phase_index(snapshot):
        suite = suites.get(phase.get("id"), {})
        boundary = phase_boundaries[phase.get("id")]
        normalized.append(
            {
                "phase_id": phase.get("id"),
                "owner_refs": suite.get("owner"),
                "implementation_refs": phase.get("implementation"),
                "documentation_refs": phase.get("verifier"),
                "runner_ref": phase.get("runner"),
                "verifier_ref": phase.get("verifier"),
                "scenario_count": phase.get("scenario_count"),
                "real_components": phase.get("real_component"),
                "synthetic_components": phase.get("controlled_components", ()),
                "candidate_truth_boundary": boundary["candidate_truth_boundary"],
                "mutation_boundary": boundary["mutation_boundary"],
                "guard_refs": "negative_guard_baseline_v1.json",
            }
        )
    return normalized


def normalized_phase_index(snapshot: BaselineSnapshot | None = None) -> Sequence[Mapping[str, Any]]:
    """Return phase boundary summaries normalized for Golden Baseline use."""

    return _normalized_phase_index(snapshot or load_baseline_snapshot())


def validate_baseline(snapshot: BaselineSnapshot | None = None) -> Tuple[BaselineIssue, ...]:
    """Return consistency issues; no runner or runtime is invoked."""

    snapshot = snapshot or load_baseline_snapshot()
    issues: list[BaselineIssue] = []
    manifest = snapshot.manifest

    if manifest.get("manifest_id") != BASELINE_ID:
        _issue(issues, "BASELINE_ID_MISMATCH", "manifest_id is not canonical")
    if manifest.get("baseline_version") != BASELINE_VERSION:
        _issue(issues, "BASELINE_VERSION_MISMATCH", "planned B5 version is missing")
    for field in (
        "owner_matrix_version",
        "contract_set_version",
        "regression_index_version",
        "negative_guard_version",
        "trace_contract_version",
    ):
        if not manifest.get(field):
            _issue(issues, "VERSION_FIELD_MISSING", field)

    phase_ids = tuple(item.get("id") for item in _phase_index(snapshot))
    if phase_ids != EXPECTED_PHASES:
        _issue(issues, "PHASE_MEMBERSHIP_INCOMPLETE", repr(phase_ids))
    if tuple(manifest.get("phase_set", ())) != EXPECTED_PHASES:
        _issue(issues, "MANIFEST_PHASE_SET_MISMATCH", repr(manifest.get("phase_set")))
    required_phase_fields = (
        "phase_id",
        "implementation_refs",
        "documentation_refs",
        "runner_ref",
        "verifier_ref",
        "scenario_count",
        "real_components",
        "synthetic_components",
        "candidate_truth_boundary",
        "mutation_boundary",
        "guard_refs",
    )
    for phase in _normalized_phase_index(snapshot):
        for field in required_phase_fields:
            if field not in phase:
                _issue(issues, "PHASE_FIELD_MISSING", f"{phase.get('phase_id')}:{field}")
        for relative in (phase.get("implementation_refs"), phase.get("runner_ref"), phase.get("verifier_ref")):
            if relative and not (REPO_ROOT / relative).exists():
                _issue(issues, "PHASE_REFERENCE_MISSING", str(relative))
    for relative in manifest.get("references", ()):
        if not (PLANNING_ROOT / relative).exists():
            _issue(issues, "MANIFEST_REFERENCE_MISSING", str(relative))

    owner_records = snapshot.owner_matrix.get("owners", [])
    owner_names = [item.get("concept") for item in owner_records if isinstance(item, dict)]
    if len(owner_names) != len(set(owner_names)):
        _issue(issues, "OWNER_MATRIX_DUPLICATE_CONCEPT", "concepts must be unique")
    if snapshot.owner_matrix.get("new_owner") is not False:
        _issue(issues, "NEW_OWNER_DECLARED", "Golden Baseline must not add a semantic owner")
    for item in owner_records:
        if not all(item.get(field) for field in ("owner", "mutation_authority", "admission_authority", "lifecycle_authority")):
            _issue(issues, "OWNER_RECORD_INCOMPLETE", repr(item))

    suites = _suite_index(snapshot)
    suite_ids = {item.get("id") for item in suites}
    for suite_id, expected_count in EXPECTED_REGRESSION_COUNTS.items():
        if suite_id not in suite_ids:
            _issue(issues, "REGRESSION_SUITE_MISSING", suite_id)
            continue
        record = next(item for item in suites if item.get("id") == suite_id)
        if record.get("scenario_count") != expected_count:
            _issue(issues, "SCENARIO_COUNT_MISMATCH", suite_id)
    for suite in suites:
        for field in ("id", "owner", "runner", "verifier", "scenario_count", "required_guards"):
            if field not in suite:
                _issue(issues, "REGRESSION_FIELD_MISSING", f"{suite.get('id')}:{field}")
        for relative in (suite.get("runner"), suite.get("verifier")):
            if relative and not (REPO_ROOT / relative).exists():
                _issue(issues, "REGRESSION_REFERENCE_MISSING", str(relative))
    task = next((item for item in suites if item.get("id") == "TASK-B3-SUBRANGE"), None)
    if not task or task.get("scenario_count") != "not independently declared; B3-16..B3-20 and B3-26":
        _issue(issues, "TASK_COVERAGE_FABRICATED", "Task must remain a B3 subrange")
    if snapshot.regression_index.get("execution_policy") != "B5 indexes suites; it does not execute them":
        _issue(issues, "REGRESSION_EXECUTION_POLICY_INVALID", "B5 must be metadata-only")

    guards = set(snapshot.guards.get("false", ()))
    missing_guards = EXPECTED_GUARDS - guards
    for guard in sorted(missing_guards):
        _issue(issues, "GUARD_MISSING", guard)
    if snapshot.guards.get("policy") != "guard weakening is a full-baseline review and cannot be silent":
        _issue(issues, "GUARD_POLICY_MISSING", "guard weakening policy is not frozen")

    required_trace = (
        "trace_refs",
        "provenance_refs",
        "temporal_refs",
        "uncertainty_refs",
        "conflict_refs",
        "contradiction_refs",
    )
    trace_refs = set(snapshot.trace.get("required_reference_classes", ()))
    for ref_name in required_trace:
        if ref_name not in trace_refs:
            _issue(issues, "TRACE_CLASS_MISSING", ref_name)
    if snapshot.trace.get("provenance_grants_authority") is not False:
        _issue(issues, "PROVENANCE_AUTHORITY_LEAK", "provenance must not grant authority")

    for field in ("real_components", "controlled_or_synthetic_components"):
        if not snapshot.real_synthetic.get(field):
            _issue(issues, "BOUNDARY_MISSING", field)
    if not snapshot.deferred.get("deferred"):
        _issue(issues, "DEFERRED_CAPABILITIES_MISSING", "deferred list is empty")

    if set(snapshot.compatibility.get("statuses", ())) != set(COMPATIBILITY_STATUSES):
        _issue(issues, "COMPATIBILITY_TAXONOMY_INCOMPLETE", "all five statuses are required")
    rules = snapshot.change_impact.get("rules", [])
    if len(rules) < 10 or snapshot.change_impact.get("silent_impact_reduction") is not False:
        _issue(issues, "CHANGE_IMPACT_MATRIX_INCOMPLETE", "change impact policy is incomplete")

    return tuple(issues)


def classify_change_impact(change_domain: str) -> ChangeImpact:
    """Classify declared metadata; this never executes the returned suites."""

    key = " ".join(change_domain.replace("_", " ").lower().split())
    mapping = {
        "visual evidence contract": ("S3", "B1", "downstream evidence compatibility"),
        "observation gateway": ("S3", "B1", "B2", "B3", "B4"),
        "current world": ("B1", "B2", "B3", "B4"),
        "cognitive state formation": ("B2", "B3", "B4"),
        "cognitive flow": ("B2", "B3", "B4"),
        "intent governance": ("B3", "B4"),
        "decision governance": ("B3", "B4"),
        "task manager": ("B3", "B4"),
        "decision or task contract": ("B3", "B4"),
        "outcome evaluation": ("B4",),
        "negative guard": ("FULL_GOLDEN_BASELINE_REVIEW",),
        "trace contract": ("AFFECTED_UPSTREAM_SUITE", "ALL_DOWNSTREAM_IF_REVERSE_TRACE_BREAKS"),
    }
    required = mapping.get(key, ("FULL_GOLDEN_BASELINE_REVIEW",))
    level = "FULL_GOLDEN_BASELINE_REVIEW" if "FULL_GOLDEN_BASELINE_REVIEW" in required else "TARGETED_REGRESSION"
    return ChangeImpact(change_domain=change_domain, required_regressions=required, review_level=level)


def classify_compatibility(*, declared_classification: str, semantic_change: bool, guard_or_trace_change: bool = False) -> CompatibilityDecision:
    """Classify explicit change metadata; filenames and execution are ignored."""

    if declared_classification not in COMPATIBILITY_STATUSES:
        return CompatibilityDecision("BLOCKED_CHANGE", "unknown compatibility classification", ("FULL_GOLDEN_BASELINE_REVIEW",))
    if guard_or_trace_change:
        return CompatibilityDecision("REQUIRES_FULL_REGRESSION", "guard or trace semantics require full review", ("FULL_GOLDEN_BASELINE_REVIEW",))
    if semantic_change and declared_classification == "BACKWARD_COMPATIBLE":
        return CompatibilityDecision("BLOCKED_CHANGE", "semantic change cannot be declared backward compatible", ("FULL_GOLDEN_BASELINE_REVIEW",))
    if declared_classification == "BREAKING_CHANGE":
        return CompatibilityDecision("BREAKING_CHANGE", "declared breaking semantic change", ("FULL_GOLDEN_BASELINE_REVIEW",))
    return CompatibilityDecision(declared_classification, "accepted declared metadata classification", ())
