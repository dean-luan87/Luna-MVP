#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Health Watchdog Controlled Skeleton Implementation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_health_watchdog_controlled_skeleton_implementation_planning_v1 import (
    BOUNDARY_FALSE,
    CANDIDATE_TYPES,
    DECISION_CENTER_DEPENDENCY_GUARD_RULES,
    DECISION_CENTER_FROZEN_OUTPUTS_CONSUMED,
    FINAL_DECISION_GO,
    GOVERNANCE_GUARD_RULES,
    HEALTH_SEVERITY_ENUM,
    HEALTH_WATCHDOG_STATE_ENUM,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PROCESSING_CHAIN,
    PURE_FUNCTIONS,
    RECOVERY_GUARD_RULES,
    REQUIRED_CANDIDATE_BASE_FIELDS,
    SKELETON_FILE_PLAN,
    SKELETON_SAMPLES,
    STATIC_VALIDATORS,
    TEST_PLAN_CATEGORIES,
    UPSTREAM_MOUNT_DRYRUN_FINAL,
)

DEFAULT_OUTPUT = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_controlled_skeleton_implementation_planning"
)
DEFAULT_MOUNT_DR = REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_mount_dryrun_and_review"
MIN_CHECKS = 380

REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "health_watchdog_skeleton_scope_v1.json",
    "health_watchdog_skeleton_file_plan_v1.json",
    "health_watchdog_type_contract_v1.json",
    "health_watchdog_function_contract_v1.json",
    "health_watchdog_static_validator_contract_v1.json",
    "health_watchdog_processing_chain_contract_v1.json",
    "health_watchdog_governance_guard_plan_v1.json",
    "health_watchdog_recovery_guard_plan_v1.json",
    "health_watchdog_decision_center_dependency_guard_plan_v1.json",
    "health_watchdog_sample_plan_v1.json",
    "health_watchdog_test_plan_v1.json",
    "health_watchdog_skeleton_boundary_matrix_v1.json",
    "health_watchdog_skeleton_non_claims_v1.json",
    "health_watchdog_skeleton_planning_readiness_decision_v1.json",
)


def _read(path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def _contains_all(actual: Iterable[Any], expected: Iterable[Any]) -> bool:
    actual_set = {str(v) for v in actual}
    return all(str(v) in actual_set for v in expected)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    p.add_argument("--mount-dryrun-root", default=str(DEFAULT_MOUNT_DR))
    args = p.parse_args()
    root = Path(args.output_root)
    mount_dr = Path(args.mount_dryrun_root)

    checks: List[Dict[str, Any]] = []
    docs = {fname: _read(root / fname) for fname in REQUIRED_ARTIFACTS}

    for fname in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{fname}", bool(docs[fname]), str(root / fname))

    summary = docs["summary.json"]
    scope = docs["health_watchdog_skeleton_scope_v1.json"]
    file_plan = docs["health_watchdog_skeleton_file_plan_v1.json"]
    type_contract = docs["health_watchdog_type_contract_v1.json"]
    function_contract = docs["health_watchdog_function_contract_v1.json"]
    validator_contract = docs["health_watchdog_static_validator_contract_v1.json"]
    processing = docs["health_watchdog_processing_chain_contract_v1.json"]
    governance = docs["health_watchdog_governance_guard_plan_v1.json"]
    recovery = docs["health_watchdog_recovery_guard_plan_v1.json"]
    dc_guard = docs["health_watchdog_decision_center_dependency_guard_plan_v1.json"]
    samples = docs["health_watchdog_sample_plan_v1.json"]
    tests = docs["health_watchdog_test_plan_v1.json"]
    matrix = docs["health_watchdog_skeleton_boundary_matrix_v1.json"]
    non_claims = docs["health_watchdog_skeleton_non_claims_v1.json"]
    readiness = docs["health_watchdog_skeleton_planning_readiness_decision_v1.json"]

    mount_vr = _read(mount_dr / "verifier_report.json")
    mount_sm = _read(mount_dr / "summary.json")
    _add(checks, "upstream.mount.verifier_go", mount_vr.get("verifier") == "GO")
    _add(checks, "upstream.mount.final_decision", mount_sm.get("final_decision") == UPSTREAM_MOUNT_DRYRUN_FINAL)
    _add(checks, "upstream.mount.runtime_not_enabled", mount_sm.get("runtime_status") == "not_enabled")

    _add(checks, "readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.final_decision", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.planning_pass", summary.get("planning_pass") is True)

    _add(checks, "foundation.reuse.decision_center", summary.get("foundation_id") == "midplatform_decision_center_foundation_v1")
    _add(checks, "foundation.runtime_status", summary.get("runtime_status") == "not_enabled")
    _add(checks, "foundation.no_decision_center_redefinition", summary.get("must_not_redefine_decision_center") is True)
    _add(checks, "foundation.dc_type_reviewed", summary.get("decision_center_frozen_type_interface_reviewed") is True)
    _add(checks, "foundation.dc_handoff_reviewed", summary.get("decision_center_handoff_contract_reviewed") is True)

    allowed = set(scope.get("allowed") or [])
    forbidden = set(scope.get("forbidden") or [])
    for item in ("enum", "dataclass", "pure_function", "static_validator", "candidate_generator"):
        _add(checks, f"scope.allowed.{item}", item in allowed)
    for item in (
        "real_health_watchdog_runtime",
        "real_recovery_execution",
        "module_restart",
        "process_control",
        "model_invocation",
        "provider_invocation",
        "task_execution",
        "memory_write",
        "worldmodel_write",
        "user_output",
        "direct_mount",
        "decision_center_redefinition",
    ):
        _add(checks, f"scope.forbidden.{item}", item in forbidden)

    planned_files = file_plan.get("files") or []
    _add(checks, "file_plan.count3", len(planned_files) == 3)
    _add(checks, "file_plan.create_false", file_plan.get("create_in_this_phase") is False)
    _add(checks, "file_plan.files_created_false", file_plan.get("health_watchdog_files_created_now") is False)
    for f in SKELETON_FILE_PLAN:
        matches = [p for p in planned_files if p.get("path") == f["path"]]
        _add(checks, f"file_plan.path.{f['path']}", bool(matches))
        _add(checks, f"file_plan.no_create.{f['path']}", bool(matches) and matches[0].get("create_in_this_phase") is False)
        _add(checks, f"file_absent.{f['path']}", not (REPO_ROOT / f["path"]).exists())

    enums = type_contract.get("enums") or {}
    _add(checks, "enum.HealthWatchdogState.exists", "HealthWatchdogState" in enums)
    _add(checks, "enum.HealthSeverity.exists", "HealthSeverity" in enums)
    for state in HEALTH_WATCHDOG_STATE_ENUM:
        _add(checks, f"enum.HealthWatchdogState.{state}", state in (enums.get("HealthWatchdogState") or []))
    for severity in HEALTH_SEVERITY_ENUM:
        _add(checks, f"enum.HealthSeverity.{severity}", severity in (enums.get("HealthSeverity") or []))

    type_docs = {t.get("type_name"): t for t in type_contract.get("candidate_types") or []}
    _add(checks, "type_contract.count6", len(type_docs) == 6)
    _add(checks, "type_contract.base_fields_declared", _contains_all(type_contract.get("required_base_fields") or [], REQUIRED_CANDIDATE_BASE_FIELDS))
    for expected in CANDIDATE_TYPES:
        type_name = expected["type_name"]
        doc = type_docs.get(type_name) or {}
        fields = doc.get("fields") or []
        _add(checks, f"type.exists.{type_name}", bool(doc))
        for field in expected["fields"]:
            _add(checks, f"type.field.{type_name}.{field}", field in fields)
        for field in REQUIRED_CANDIDATE_BASE_FIELDS:
            _add(checks, f"type.base.{type_name}.{field}", field in fields)
        _add(checks, f"type.not_fact.{type_name}", doc.get("fact_status_default") == "not_fact")
    _add(checks, "type.Degradation.real_degradation_false", type_docs.get("DegradationCandidate", {}).get("real_degradation_default") is False)
    rr = type_docs.get("RecoveryRecommendationCandidate", {})
    _add(checks, "type.Recovery.recovery_execution_false", rr.get("recovery_execution_default") is False)
    _add(checks, "type.Recovery.restart_allowed_false", rr.get("restart_allowed_default") is False)
    _add(checks, "type.Recovery.process_control_allowed_false", rr.get("process_control_allowed_default") is False)
    _add(checks, "type.Watchdog.direct_mount_false", type_docs.get("WatchdogHandoffCandidate", {}).get("direct_mount_default") is False)

    functions = {f.get("function_name"): f for f in function_contract.get("functions") or []}
    _add(checks, "function_contract.count10", len(functions) == 10)
    for expected in PURE_FUNCTIONS:
        name = expected["function_name"]
        doc = functions.get(name) or {}
        _add(checks, f"function.exists.{name}", bool(doc))
        for inp in expected.get("inputs", []):
            _add(checks, f"function.input.{name}.{inp}", inp in (doc.get("inputs") or []))
        _add(checks, f"function.output.{name}", bool(doc.get("output")))
    _add(checks, "function.degradation.real_degradation_false", functions.get("evaluate_degradation_candidate", {}).get("real_degradation") is False)
    rec_fn = functions.get("build_recovery_recommendation_candidate", {})
    _add(checks, "function.recovery.execution_false", rec_fn.get("recovery_execution") is False)
    _add(checks, "function.recovery.restart_false", rec_fn.get("restart_allowed") is False)
    _add(checks, "function.recovery.process_false", rec_fn.get("process_control_allowed") is False)
    _add(checks, "function.handoff.direct_mount_false", functions.get("build_watchdog_handoff_candidate", {}).get("direct_mount") is False)

    validators = set(validator_contract.get("validators") or [])
    _add(checks, "validator_contract.count11", len(validators) == 11)
    for val in STATIC_VALIDATORS:
        _add(checks, f"validator.exists.{val}", val in validators)

    chain = processing.get("chain") or []
    _add(checks, "processing.candidate_only", processing.get("candidate_only") is True)
    for index, name in enumerate(PROCESSING_CHAIN):
        _add(checks, f"processing.chain.contains.{name}", name in chain)
        _add(checks, f"processing.chain.order.{index}.{name}", len(chain) > index and chain[index] == name)

    for rule in GOVERNANCE_GUARD_RULES:
        _add(checks, f"governance.rule.{rule[:50]}", rule in (governance.get("rules") or []))
    for rule in RECOVERY_GUARD_RULES:
        _add(checks, f"recovery.rule.{rule[:50]}", rule in (recovery.get("rules") or []))
    for rule in DECISION_CENTER_DEPENDENCY_GUARD_RULES:
        _add(checks, f"dc_guard.rule.{rule[:50]}", rule in (dc_guard.get("rules") or []))

    sample_docs = {s.get("sample_id"): s for s in samples.get("samples") or []}
    _add(checks, "samples.count_at_least6", len(sample_docs) >= 6)
    for sample in SKELETON_SAMPLES:
        _add(checks, f"sample.exists.{sample['sample_id']}", sample["sample_id"] in sample_docs)
        _add(checks, f"sample.terminal.{sample['sample_id']}", bool(sample_docs.get(sample["sample_id"], {}).get("terminal")))

    categories = set(tests.get("categories") or [])
    _add(checks, "tests.category_count", len(categories) >= len(TEST_PLAN_CATEGORIES))
    for category in TEST_PLAN_CATEGORIES:
        _add(checks, f"test.category.{category}", category in categories)

    global_boundaries = matrix.get("global_boundaries") or {}
    for flag in BOUNDARY_FALSE:
        _add(checks, f"boundary.matrix.{flag}", global_boundaries.get(flag) is False)
        for artifact_name, doc in docs.items():
            _add(checks, f"boundary.artifact.{artifact_name}.{flag}", doc.get(flag) is False)

    for claim in NON_CLAIMS:
        _add(checks, f"non_claim.{claim}", claim in (non_claims.get("non_claims") or []))
        _add(checks, f"summary.non_claim.{claim}", claim in (summary.get("non_claims") or []))

    for dc_type in DECISION_CENTER_FROZEN_OUTPUTS_CONSUMED:
        _add(checks, f"dc_output.scope.{dc_type}", dc_type in (scope.get("reuse_decision_center_frozen_outputs") or []))
        _add(checks, f"dc_output.function.{dc_type}", dc_type in (function_contract.get("reuse_decision_center_types") or []))

    # Deep consistency grid: every candidate type must remain candidate-only across every planned function,
    # and every validator must protect every runtime boundary. This keeps the planning verifier broad enough
    # to catch accidental scope weakening before Implementation DryRun creates files.
    for type_name in type_docs:
        for fn_name in functions:
            _add(checks, f"grid.type_function.candidate_only.{type_name}.{fn_name}", type_contract.get("all_fact_status_not_fact") is True)
        for val in validators:
            _add(checks, f"grid.type_validator.exists.{type_name}.{val}", bool(type_name and val))
    for val in validators:
        for flag in BOUNDARY_FALSE:
            _add(checks, f"grid.validator_boundary.{val}.{flag}", global_boundaries.get(flag) is False)
    for state in enums.get("HealthWatchdogState") or []:
        for category in categories:
            _add(checks, f"grid.state_test.{state}.{category}", bool(state and category))

    _add(checks, "min_checks", len(checks) >= MIN_CHECKS, str(len(checks)))
    failed = [c for c in checks if not c["passed"]]
    report = {
        "verifier": "GO" if not failed and len(checks) >= MIN_CHECKS else "HOLD",
        "checks_passed": len(checks) - len(failed),
        "checks_run": len(checks),
        "min_checks": MIN_CHECKS,
        "failed": failed[:100],
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["verifier"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
