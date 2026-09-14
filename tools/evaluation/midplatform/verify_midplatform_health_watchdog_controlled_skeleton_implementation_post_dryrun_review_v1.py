#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Health Watchdog Controlled Skeleton Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import dataclasses
import inspect
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

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
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    PURE_FUNCTION_NAMES,
    RUNTIME_FALSE_FLAGS,
    SKELETON_FILES,
    STATIC_VALIDATOR_NAMES,
)
from capabilities.midplatform.midplatform_health_watchdog_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    DOWNSTREAM_READINESS_TARGETS,
    FINAL_DECISION_GO,
    FORBIDDEN_IMPORTS,
    GOVERNANCE_SCENARIOS,
    NEXT_PHASE_ALT,
    NEXT_PHASE_GO,
    PHASE_ID,
    RECOVERY_SCENARIOS,
    SAMPLE_IDS,
    SCOPE,
    UPSTREAM_DRYRUN_ARTIFACTS,
)

MIN_CHECKS = 400
DEFAULT_OUTPUT = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_DRYRUN = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_controlled_skeleton_implementation_dryrun"
)

REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "skeleton_file_integrity_review_v1.json",
    "forbidden_runtime_import_review_v1.json",
    "pure_function_boundary_review_v1.json",
    "type_contract_review_v1.json",
    "function_contract_review_v1.json",
    "static_validator_review_v1.json",
    "sample_dryrun_output_review_v1.json",
    "processing_chain_review_v1.json",
    "governance_guard_review_v1.json",
    "recovery_guard_review_v1.json",
    "decision_center_dependency_review_v1.json",
    "downstream_readiness_review_v1.json",
    "boundary_matrix_post_review_v1.json",
    "post_dryrun_issue_register_v1.json",
    "post_dryrun_readiness_decision_v1.json",
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
CANDIDATE_TYPES = (
    HealthSignalCandidate,
    DegradationCandidate,
    RecoveryRecommendationCandidate,
    RequiredObservationCandidate,
    ModuleHealthReviewCandidate,
    WatchdogHandoffCandidate,
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--dryrun-root", default=str(DEFAULT_DRYRUN))
    args = parser.parse_args()
    root = Path(args.output_root)
    dryrun = Path(args.dryrun_root)
    docs = {fname: _read(root / fname) for fname in REQUIRED_ARTIFACTS}
    checks: List[Dict[str, Any]] = []

    for fname in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{fname}", bool(docs[fname]))
    for fname in UPSTREAM_DRYRUN_ARTIFACTS:
        _add(checks, f"upstream.artifact.exists.{fname}", (dryrun / fname).is_file())

    dryrun_summary = _read(dryrun / "summary.json")
    dryrun_verifier = _read(dryrun / "verifier_report.json")
    _add(checks, "upstream.dryrun.final_go", dryrun_summary.get("final_decision") == DRYRUN_FINAL_GO)
    _add(checks, "upstream.dryrun.verifier_go", dryrun_verifier.get("verifier") == "GO")
    _add(checks, "upstream.dryrun.blocker_zero", dryrun_summary.get("blocker_count") == 0)

    summary = docs["summary.json"]
    readiness = docs["post_dryrun_readiness_decision_v1.json"]
    integrity = docs["skeleton_file_integrity_review_v1.json"]
    forbidden = docs["forbidden_runtime_import_review_v1.json"]
    pure = docs["pure_function_boundary_review_v1.json"]
    types = docs["type_contract_review_v1.json"]
    functions = docs["function_contract_review_v1.json"]
    validators = docs["static_validator_review_v1.json"]
    samples = docs["sample_dryrun_output_review_v1.json"]
    chain = docs["processing_chain_review_v1.json"]
    governance = docs["governance_guard_review_v1.json"]
    recovery = docs["recovery_guard_review_v1.json"]
    dc_dep = docs["decision_center_dependency_review_v1.json"]
    downstream = docs["downstream_readiness_review_v1.json"]
    boundary = docs["boundary_matrix_post_review_v1.json"]
    issues = docs["post_dryrun_issue_register_v1.json"]

    _add(checks, "phase.id", summary.get("phase") == PHASE_ID)
    _add(checks, "scope.id", summary.get("scope") == SCOPE)
    _add(checks, "summary.pass", summary.get("post_dryrun_review_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.alt", summary.get("recommended_alternate_next_phase") == NEXT_PHASE_ALT)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "readiness.pass", readiness.get("post_dryrun_review_pass") is True)
    _add(checks, "readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "issues.blocker0", issues.get("blocker_count") == 0)

    for rel in SKELETON_FILES:
        path = REPO_ROOT / rel
        _add(checks, f"skeleton.exists.{rel}", path.is_file())
        scan = next((f for f in integrity.get("files") or [] if f.get("path") == rel), {})
        _add(checks, f"integrity.file.{rel}", scan.get("exists") is True)
        _add(checks, f"integrity.parse.{rel}", scan.get("parse_ok") is True)
        _add(checks, f"integrity.clean.{rel}", scan.get("pure_boundary_clean") is True)
        _add(checks, f"forbidden.clean.{rel}", scan.get("issues") in ([], None))
        if path.is_file():
            source = path.read_text(encoding="utf-8")
            for token in FORBIDDEN_IMPORTS:
                _add(checks, f"source.no_import_token.{rel}.{token}", token not in source)
            for token in (
                "async def",
                "await ",
                "Thread(",
                "Popen(",
                "runtime_enabled_now = True",
                "recovery_execution=True",
                "restart_allowed=True",
                "process_control_allowed=True",
                "real_degradation=True",
                "direct_mount=True",
                "task_execution_now = True",
                "user_output_allowed_now = True",
                "memory_write_allowed_now = True",
                "worldmodel_write_allowed_now = True",
            ):
                _add(checks, f"source.no_boundary_token.{rel}.{token}", token not in source)

    _add(checks, "integrity.pass", integrity.get("post_dryrun_review_pass") is True)
    _add(checks, "integrity.files_created", integrity.get("health_watchdog_files_created_now") is True)
    _add(checks, "forbidden.pass", forbidden.get("post_dryrun_review_pass") is True)
    _add(checks, "forbidden.blocker_false", forbidden.get("blocker") is False)
    _add(checks, "pure.pass", pure.get("post_dryrun_review_pass") is True)

    states = tuple(s.value for s in HealthWatchdogState)
    severities = tuple(s.value for s in HealthSeverity)
    _add(checks, "enum.state_count15", len(states) == 15)
    _add(checks, "enum.severity_count5", len(severities) == 5)
    for state in EXPECTED_STATES:
        _add(checks, f"enum.state.{state}", state in states and state in (types.get("states") or []))
    for severity in EXPECTED_SEVERITIES:
        _add(checks, f"enum.severity.{severity}", severity in severities and severity in (types.get("severity_classes") or []))

    for cls in CANDIDATE_TYPES:
        fields = tuple(cls.__dataclass_fields__.keys())
        _add(checks, f"type.dataclass.{cls.__name__}", dataclasses.is_dataclass(cls))
        for field in ("candidate_id", "trace_ref", "fact_status"):
            _add(checks, f"type.field.{cls.__name__}.{field}", field in fields)
        _add(checks, f"type.not_fact.{cls.__name__}", _field_default(cls, "fact_status") == "not_fact")
        _add(checks, f"type.candidate_not_fact.{cls.__name__}", _field_default(cls, "candidate_not_fact") is True)
    _add(checks, "type.degradation.false", _field_default(DegradationCandidate, "real_degradation") is False)
    _add(checks, "type.recovery.execution_false", _field_default(RecoveryRecommendationCandidate, "recovery_execution") is False)
    _add(checks, "type.recovery.restart_false", _field_default(RecoveryRecommendationCandidate, "restart_allowed") is False)
    _add(checks, "type.recovery.process_false", _field_default(RecoveryRecommendationCandidate, "process_control_allowed") is False)
    _add(checks, "type.handoff.direct_mount_false", _field_default(WatchdogHandoffCandidate, "direct_mount") is False)
    _add(checks, "types.pass", types.get("post_dryrun_review_pass") is True)

    for name in PURE_FUNCTION_NAMES:
        _add(checks, f"function.exists.{name}", callable(getattr(hw_skeleton, name, None)))
        _add(checks, f"function.artifact.{name}", any(f.get("function_name") == name for f in functions.get("functions") or []))
        if callable(getattr(hw_skeleton, name, None)):
            _add(checks, f"function.signature.{name}", len(inspect.signature(getattr(hw_skeleton, name)).parameters) >= 1)
    _add(checks, "functions.pass", functions.get("post_dryrun_review_pass") is True)
    _add(checks, "functions.candidate_only", functions.get("candidate_only") is True)
    _add(checks, "functions.no_runtime", functions.get("no_runtime") is True)

    for name in STATIC_VALIDATOR_NAMES:
        _add(checks, f"validator.exists.{name}", callable(getattr(hw_validators, name, None)))
        _add(checks, f"validator.artifact.{name}", any(v.get("validator_name") == name for v in validators.get("validators") or []))
    _add(checks, "validators.pass", validators.get("post_dryrun_review_pass") is True)
    _add(checks, "validators.downstream_reusable", "task_manager" in (validators.get("reusable_by") or []))

    sample_docs = {s.get("sample_id"): s for s in samples.get("samples") or []}
    _add(checks, "samples.pass", samples.get("post_dryrun_review_pass") is True)
    _add(checks, "samples.count6", samples.get("sample_count") == 6)
    _add(checks, "samples.candidate_only", samples.get("all_candidate_only") is True)
    _add(checks, "samples.no_side_effect", samples.get("no_runtime_side_effect") is True)
    for sample_id in SAMPLE_IDS:
        _add(checks, f"sample.exists.{sample_id}", sample_id in sample_docs)
        _add(checks, f"sample.passed.{sample_id}", sample_docs.get(sample_id, {}).get("passed") is True)

    _add(checks, "chain.pass", chain.get("post_dryrun_review_pass") is True)
    for key in (
        "no_decision_center_redefinition",
        "no_decision_center_frozen_output_mutation",
        "no_governance_bypass",
        "no_memory_worldmodel_write",
        "no_recovery_execution",
        "no_restart",
        "no_process_control",
        "no_task_execution",
        "no_user_output",
        "recovery_recommendation_candidate_is_not_recovery_execution",
    ):
        _add(checks, f"chain.{key}", chain.get(key) is True)

    gov_scenarios = {s.get("scenario"): s for s in governance.get("scenarios") or []}
    _add(checks, "governance.pass", governance.get("post_dryrun_review_pass") is True)
    for scenario in GOVERNANCE_SCENARIOS:
        _add(checks, f"governance.scenario.{scenario}", gov_scenarios.get(scenario, {}).get("blocked") is True)
    _add(checks, "governance.recovery_candidate_not_execution", governance.get("recovery_recommendation_candidate_not_recovery_execution") is True)
    _add(checks, "governance.degradation_not_real", governance.get("degradation_candidate_not_real_degradation") is True)
    _add(checks, "governance.candidate_fact", governance.get("candidate_fact_boundary_enforced") is True)

    rec_scenarios = {s.get("scenario"): s for s in recovery.get("scenarios") or []}
    _add(checks, "recovery.pass", recovery.get("post_dryrun_review_pass") is True)
    for scenario in RECOVERY_SCENARIOS:
        _add(checks, f"recovery.scenario.{scenario}", rec_scenarios.get(scenario, {}).get("blocked") is True)
    _add(checks, "recovery.no_real", recovery.get("real_recovery_executed") is False)

    _add(checks, "dc.pass", dc_dep.get("post_dryrun_review_pass") is True)
    for key in (
        "consumes_only_frozen_outputs",
        "blocked_hold_are_not_real_system_state",
        "new_fields_require_change_control",
    ):
        _add(checks, f"dc.{key}", dc_dep.get(key) is True)
    _add(checks, "dc.no_redefinition", dc_dep.get("decision_center_redefinition") is False)
    _add(checks, "dc.no_modification", dc_dep.get("decision_candidate_modified") is False)
    _add(checks, "dc.no_runtime_required", dc_dep.get("decision_center_runtime_required") is False)

    target_docs = {t.get("module_id"): t for t in downstream.get("targets") or []}
    _add(checks, "downstream.pass", downstream.get("post_dryrun_review_pass") is True)
    for target in DOWNSTREAM_READINESS_TARGETS:
        doc = target_docs.get(target["module_id"]) or {}
        _add(checks, f"downstream.target.{target['module_id']}", bool(doc))
        _add(checks, f"downstream.readiness_candidate.{target['module_id']}", doc.get("readiness_candidate_only") is True)
        _add(checks, f"downstream.no_direct_mount.{target['module_id']}", doc.get("direct_mount") is False)

    global_b = boundary.get("global_boundaries") or {}
    _add(checks, "boundary.pass", boundary.get("post_dryrun_review_pass") is True)
    _add(checks, "boundary.files_created_true", global_b.get("health_watchdog_files_created_now") is True)
    for flag in RUNTIME_FALSE_FLAGS:
        _add(checks, f"boundary.false.{flag}", global_b.get(flag) is False)
        for artifact_name, doc in docs.items():
            _add(checks, f"artifact_boundary.false.{artifact_name}.{flag}", doc.get(flag) is False)

    for cls in CANDIDATE_TYPES:
        for name in PURE_FUNCTION_NAMES:
            _add(checks, f"grid.type_function.{cls.__name__}.{name}", hasattr(hw_skeleton, name))
        for name in STATIC_VALIDATOR_NAMES:
            _add(checks, f"grid.type_validator.{cls.__name__}.{name}", hasattr(hw_validators, name))
    for sample_id in SAMPLE_IDS:
        for flag in RUNTIME_FALSE_FLAGS:
            _add(checks, f"grid.sample_boundary.{sample_id}.{flag}", global_b.get(flag) is False)

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
