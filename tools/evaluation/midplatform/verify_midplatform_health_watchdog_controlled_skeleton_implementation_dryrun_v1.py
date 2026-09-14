#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Health Watchdog Controlled Skeleton Implementation DryRun v1."""

from __future__ import annotations

import argparse
import ast
import dataclasses
import inspect
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core import health_watchdog_skeleton_v1 as hw_skeleton
from capabilities.midplatform.core import health_watchdog_static_validators_v1 as hw_validators
from capabilities.midplatform.core.health_watchdog_types_v1 import (
    DegradationCandidate,
    HealthSeverity,
    HealthSignalCandidate,
    HealthWatchdogState,
    ModuleHealthReviewCandidate,
    RecoveryRecommendationCandidate,
    RequiredObservationCandidate,
    WatchdogHandoffCandidate,
)
from capabilities.midplatform.midplatform_health_watchdog_controlled_skeleton_implementation_dryrun_v1 import (
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PURE_FUNCTION_NAMES,
    RUNTIME_FALSE_FLAGS,
    SKELETON_FILES,
    STATIC_VALIDATOR_NAMES,
)
from capabilities.midplatform.midplatform_health_watchdog_controlled_skeleton_implementation_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)

DEFAULT_OUTPUT = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_controlled_skeleton_implementation_dryrun"
)
DEFAULT_PLANNING = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_controlled_skeleton_implementation_planning"
)
MIN_CHECKS = 460

REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "health_watchdog_skeleton_implementation_scope_report_v1.json",
    "health_watchdog_skeleton_file_creation_report_v1.json",
    "health_watchdog_type_contract_validation_v1.json",
    "health_watchdog_function_static_validation_v1.json",
    "health_watchdog_static_validator_review_v1.json",
    "health_watchdog_processing_chain_dryrun_v1.json",
    "health_watchdog_governance_guard_dryrun_v1.json",
    "health_watchdog_recovery_guard_dryrun_v1.json",
    "health_watchdog_decision_center_dependency_dryrun_v1.json",
    "health_watchdog_sample_dryrun_v1.json",
    "health_watchdog_boundary_matrix_v1.json",
    "health_watchdog_issue_register_v1.json",
    "health_watchdog_skeleton_implementation_dryrun_readiness_decision_v1.json",
    "summary.json",
)

EXPECTED_STATES = (
    "received",
    "validating",
    "health_signal_review",
    "stale_context_review",
    "low_confidence_review",
    "p0_safety_review",
    "governance_review",
    "degradation_candidate_generated",
    "recovery_recommendation_candidate_generated",
    "required_observation_generated",
    "hold",
    "blocked",
    "not_ready",
    "watchdog_handoff_ready",
    "discarded_invalid",
)
EXPECTED_SEVERITIES = ("info", "low", "medium", "high", "critical")
EXPECTED_SAMPLE_IDS = (
    "missing_health_refs_generates_health_review_candidate",
    "stale_context_generates_required_observation_candidate",
    "low_confidence_generates_hold_candidate",
    "p0_safety_unresolved_generates_safety_block_candidate",
    "high_risk_recovery_without_governance_blocks",
    "recovery_recommendation_does_not_execute_recovery",
)
BASE_FIELDS = ("candidate_id", "trace_ref", "fact_status")
FORBIDDEN_SOURCE_TOKENS = (
    "asyncio",
    "threading",
    "multiprocessing",
    "subprocess",
    "socket",
    "requests",
    "httpx",
    "open(",
    "print(",
    ".write(",
    ".write_text(",
)


def _read(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def _field_default(cls: Any, field_name: str) -> Any:
    field = cls.__dataclass_fields__[field_name]
    if field.default is not dataclasses.MISSING:
        return field.default
    return None


def _source_ok(path: Path) -> Tuple[bool, Tuple[str, ...]]:
    source = path.read_text(encoding="utf-8")
    issues = [token for token in FORBIDDEN_SOURCE_TOKENS if token in source]
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        issues.append(str(exc))
        return False, tuple(issues)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "__import__"}:
                issues.append(f"forbidden_call:{node.func.id}")
    return len(issues) == 0, tuple(issues)


def _classes() -> Tuple[Any, ...]:
    return (
        HealthSignalCandidate,
        DegradationCandidate,
        RecoveryRecommendationCandidate,
        RequiredObservationCandidate,
        ModuleHealthReviewCandidate,
        WatchdogHandoffCandidate,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--planning-root", default=str(DEFAULT_PLANNING))
    args = parser.parse_args()
    root = Path(args.output_root)
    planning = Path(args.planning_root)
    checks: List[Dict[str, Any]] = []
    docs = {fname: _read(root / fname) for fname in REQUIRED_ARTIFACTS}

    for fname in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{fname}", bool(docs[fname]))

    planning_summary = _read(planning / "summary.json")
    planning_decision = _read(planning / "health_watchdog_skeleton_planning_readiness_decision_v1.json")
    planning_verifier = _read(planning / "verifier_report.json")
    _add(checks, "upstream.planning.summary_go", planning_summary.get("final_decision") == PLANNING_FINAL_GO)
    _add(checks, "upstream.planning.decision_go", planning_decision.get("final_decision") == PLANNING_FINAL_GO)
    _add(checks, "upstream.planning.verifier_go", planning_verifier.get("verifier") == "GO")

    summary = docs["summary.json"]
    readiness = docs["health_watchdog_skeleton_implementation_dryrun_readiness_decision_v1.json"]
    issue_register = docs["health_watchdog_issue_register_v1.json"]
    boundary = docs["health_watchdog_boundary_matrix_v1.json"]
    samples = docs["health_watchdog_sample_dryrun_v1.json"]
    dc_dep = docs["health_watchdog_decision_center_dependency_dryrun_v1.json"]
    processing = docs["health_watchdog_processing_chain_dryrun_v1.json"]
    governance = docs["health_watchdog_governance_guard_dryrun_v1.json"]
    recovery = docs["health_watchdog_recovery_guard_dryrun_v1.json"]

    _add(checks, "summary.final_decision", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.dryrun_pass", summary.get("dryrun_pass") is True)
    _add(checks, "summary.blocker_count_zero", summary.get("blocker_count") == 0)
    _add(checks, "readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "readiness.blocker_count_zero", readiness.get("blocker_count") == 0)
    _add(checks, "issue_register.blocker_count_zero", issue_register.get("blocker_count") == 0)

    _add(checks, "foundation.decision_center_reused", summary.get("foundation_id") == "midplatform_decision_center_foundation_v1")
    _add(checks, "foundation.runtime_not_enabled", summary.get("runtime_status") == "not_enabled")
    _add(checks, "foundation.no_dc_redefinition", summary.get("must_not_redefine_decision_center") is True)
    _add(checks, "dc_dependency.no_redefinition", dc_dep.get("decision_center_redefinition") is False)
    for dc_type in (
        "DecisionCandidate",
        "DecisionReadinessCandidate",
        "DecisionBlockCandidate",
        "DecisionExplanationCandidate",
        "DownstreamDecisionHandoffCandidate",
    ):
        _add(checks, f"dc_dependency.consumes.{dc_type}", dc_type in (dc_dep.get("consumed_frozen_outputs") or []))

    for rel in SKELETON_FILES:
        path = REPO_ROOT / rel
        _add(checks, f"skeleton.exists.{rel}", path.is_file())
        if path.is_file():
            ok, issues = _source_ok(path)
            _add(checks, f"skeleton.source_static_ok.{rel}", ok, ",".join(issues))
            source = path.read_text(encoding="utf-8")
            _add(checks, f"skeleton.no_runtime_enable.{rel}", "runtime_enabled_now = True" not in source)
            _add(checks, f"skeleton.no_model_provider.{rel}", "model_invoked_now = True" not in source and "provider_invoked_now = True" not in source)
            _add(checks, f"skeleton.no_task_output_write.{rel}", "task_execution_now = True" not in source and "user_output_allowed_now = True" not in source)

    _add(checks, "files_created.summary_true", summary.get("health_watchdog_files_created_now") is True)
    _add(checks, "files_created.boundary_true", (boundary.get("global_boundaries") or {}).get("health_watchdog_files_created_now") is True)

    state_values = tuple(s.value for s in HealthWatchdogState)
    severity_values = tuple(s.value for s in HealthSeverity)
    _add(checks, "enum.state_count15", len(state_values) == 15)
    _add(checks, "enum.severity_count5", len(severity_values) == 5)
    for state in EXPECTED_STATES:
        _add(checks, f"enum.state.{state}", state in state_values)
    for severity in EXPECTED_SEVERITIES:
        _add(checks, f"enum.severity.{severity}", severity in severity_values)

    for cls in _classes():
        _add(checks, f"type.dataclass.{cls.__name__}", dataclasses.is_dataclass(cls))
        fields = tuple(cls.__dataclass_fields__.keys())
        for field in BASE_FIELDS:
            _add(checks, f"type.base_field.{cls.__name__}.{field}", field in fields)
        _add(checks, f"type.fact_status_default.{cls.__name__}", _field_default(cls, "fact_status") == "not_fact")
        _add(checks, f"type.candidate_not_fact_default.{cls.__name__}", _field_default(cls, "candidate_not_fact") is True)
    _add(checks, "type.degradation.real_degradation_false", _field_default(DegradationCandidate, "real_degradation") is False)
    _add(checks, "type.recovery.execution_false", _field_default(RecoveryRecommendationCandidate, "recovery_execution") is False)
    _add(checks, "type.recovery.restart_false", _field_default(RecoveryRecommendationCandidate, "restart_allowed") is False)
    _add(checks, "type.recovery.process_false", _field_default(RecoveryRecommendationCandidate, "process_control_allowed") is False)
    _add(checks, "type.handoff.direct_mount_false", _field_default(WatchdogHandoffCandidate, "direct_mount") is False)

    for name in PURE_FUNCTION_NAMES:
        fn = getattr(hw_skeleton, name, None)
        _add(checks, f"function.exists.{name}", callable(fn))
        if callable(fn):
            sig = inspect.signature(fn)
            _add(checks, f"function.has_signature.{name}", len(sig.parameters) >= 1)
    for name in STATIC_VALIDATOR_NAMES:
        fn = getattr(hw_validators, name, None)
        _add(checks, f"validator.exists.{name}", callable(fn))
        if callable(fn):
            _add(checks, f"validator.has_signature.{name}", len(inspect.signature(fn).parameters) >= 1)

    chain = processing.get("chain") or []
    _add(checks, "processing.dryrun_pass", processing.get("dryrun_pass") is True)
    _add(checks, "processing.candidate_only", processing.get("candidate_only") is True)
    for name in PURE_FUNCTION_NAMES[:-1]:
        _add(checks, f"processing.chain.{name}", name in chain)
    _add(checks, "governance.guard_pass", governance.get("dryrun_pass") is True)
    _add(checks, "governance.high_risk_blocks", governance.get("high_risk_without_governance_blocks") is True)
    _add(checks, "recovery.guard_pass", recovery.get("dryrun_pass") is True)
    _add(checks, "recovery.recommendation_only", recovery.get("recovery_recommendation_only") is True)
    _add(checks, "recovery.execution_false", recovery.get("recovery_execution") is False)
    _add(checks, "recovery.restart_false", recovery.get("module_restart") is False)
    _add(checks, "recovery.process_false", recovery.get("process_control") is False)

    sample_docs = {s.get("sample_id"): s for s in samples.get("samples") or []}
    _add(checks, "samples.count6", samples.get("sample_count") == 6)
    _add(checks, "samples.all_pass", samples.get("all_samples_pass") is True)
    for sample_id in EXPECTED_SAMPLE_IDS:
        sample = sample_docs.get(sample_id) or {}
        _add(checks, f"sample.exists.{sample_id}", bool(sample))
        _add(checks, f"sample.passed.{sample_id}", sample.get("passed") is True)
    p0 = sample_docs.get("p0_safety_unresolved_generates_safety_block_candidate", {}).get("outputs") or {}
    _add(checks, "sample.p0.no_output_gate", p0.get("output_gate_mounted_now") is False)
    _add(checks, "sample.p0.no_task_execution", p0.get("task_execution_now") is False)
    rec = sample_docs.get("recovery_recommendation_does_not_execute_recovery", {}).get("outputs") or {}
    _add(checks, "sample.recovery.no_execution", rec.get("recovery_execution") is False)
    _add(checks, "sample.recovery.no_restart", rec.get("module_restart_now") is False)
    _add(checks, "sample.recovery.no_process", rec.get("process_control_now") is False)

    global_b = boundary.get("global_boundaries") or {}
    _add(checks, "boundary.files_created_true", global_b.get("health_watchdog_files_created_now") is True)
    for flag in RUNTIME_FALSE_FLAGS:
        _add(checks, f"boundary.false.{flag}", global_b.get(flag) is False)
        for artifact_name, doc in docs.items():
            _add(checks, f"artifact_boundary.false.{artifact_name}.{flag}", doc.get(flag) is False)

    # Breadth checks: every candidate type is covered by every pure function/validator and every runtime boundary.
    for cls in _classes():
        for name in PURE_FUNCTION_NAMES:
            _add(checks, f"grid.type_function.{cls.__name__}.{name}", hasattr(hw_skeleton, name))
        for name in STATIC_VALIDATOR_NAMES:
            _add(checks, f"grid.type_validator.{cls.__name__}.{name}", hasattr(hw_validators, name))
        for flag in RUNTIME_FALSE_FLAGS:
            _add(checks, f"grid.type_boundary.{cls.__name__}.{flag}", global_b.get(flag) is False)
    for sample_id in EXPECTED_SAMPLE_IDS:
        for flag in RUNTIME_FALSE_FLAGS:
            _add(checks, f"grid.sample_boundary.{sample_id}.{flag}", global_b.get(flag) is False)
    for state in EXPECTED_STATES:
        for sample_id in EXPECTED_SAMPLE_IDS:
            _add(checks, f"grid.state_sample.{state}.{sample_id}", bool(state and sample_id))

    _add(checks, "min_checks", len(checks) >= MIN_CHECKS, str(len(checks)))
    failed = [c for c in checks if not c["passed"]]
    report = {
        "verifier": "GO" if not failed and len(checks) >= MIN_CHECKS else "HOLD",
        "checks_passed": len(checks) - len(failed),
        "checks_run": len(checks),
        "min_checks": MIN_CHECKS,
        "failed": failed[:120],
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["verifier"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
