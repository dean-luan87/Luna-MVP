#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Controlled Skeleton Implementation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_planning_v1 import (
    BOUNDARY_FALSE,
    CANDIDATE_TYPES,
    DECISION_CENTER_DEPENDENCY_GUARD_RULES,
    DECISION_CENTER_OUTPUTS_CONSUMED,
    EXECUTION_GUARD_RULES,
    FINAL_DECISION_GO,
    GOVERNANCE_GUARD_RULES,
    HEALTH_WATCHDOG_DEPENDENCY_GUARD_RULES,
    HEALTH_WATCHDOG_OUTPUTS_CONSUMED,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PROCESSING_CHAIN,
    PURE_FUNCTIONS,
    REQUIRED_BASE_FIELDS,
    SAMPLE_PLAN,
    SKELETON_FILE_PLAN,
    STATIC_VALIDATORS,
    TASK_READINESS_ENUM,
    TASK_STATE_ENUM,
    TEST_PLAN_CATEGORIES,
)
from capabilities.midplatform.midplatform_task_manager_mount_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MOUNT_DRYRUN_FINAL_GO,
)

MIN_CHECKS = 400
DEFAULT_OUTPUT = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_task_manager_controlled_skeleton_implementation_planning"
)
DEFAULT_MOUNT = REPO_ROOT / "_tmp_eval_out" / "midplatform_task_manager_mount_dryrun_and_review"

REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "task_manager_skeleton_scope_v1.json",
    "task_manager_skeleton_file_plan_v1.json",
    "task_manager_type_contract_v1.json",
    "task_manager_function_contract_v1.json",
    "task_manager_static_validator_contract_v1.json",
    "task_manager_processing_chain_contract_v1.json",
    "task_manager_governance_guard_plan_v1.json",
    "task_manager_execution_guard_plan_v1.json",
    "task_manager_health_watchdog_dependency_guard_plan_v1.json",
    "task_manager_decision_center_dependency_guard_plan_v1.json",
    "task_manager_sample_plan_v1.json",
    "task_manager_test_plan_v1.json",
    "task_manager_skeleton_boundary_matrix_v1.json",
    "task_manager_skeleton_non_claims_v1.json",
    "task_manager_skeleton_planning_readiness_decision_v1.json",
)


def _read(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--mount-dryrun-root", default=str(DEFAULT_MOUNT))
    args = parser.parse_args()
    root = Path(args.output_root)
    mount = Path(args.mount_dryrun_root)
    docs = {fname: _read(root / fname) for fname in REQUIRED_ARTIFACTS}
    checks: List[Dict[str, Any]] = []

    for fname in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{fname}", bool(docs[fname]))

    mount_summary = _read(mount / "summary.json")
    mount_verifier = _read(mount / "verifier_report.json")
    _add(checks, "upstream.mount.final_go", mount_summary.get("final_decision") == MOUNT_DRYRUN_FINAL_GO)
    _add(checks, "upstream.mount.verifier_go", mount_verifier.get("verifier") == "GO")

    summary = docs["summary.json"]
    scope = docs["task_manager_skeleton_scope_v1.json"]
    file_plan = docs["task_manager_skeleton_file_plan_v1.json"]
    types = docs["task_manager_type_contract_v1.json"]
    funcs = docs["task_manager_function_contract_v1.json"]
    validators = docs["task_manager_static_validator_contract_v1.json"]
    chain = docs["task_manager_processing_chain_contract_v1.json"]
    gov = docs["task_manager_governance_guard_plan_v1.json"]
    execution = docs["task_manager_execution_guard_plan_v1.json"]
    hw_guard = docs["task_manager_health_watchdog_dependency_guard_plan_v1.json"]
    dc_guard = docs["task_manager_decision_center_dependency_guard_plan_v1.json"]
    samples = docs["task_manager_sample_plan_v1.json"]
    tests = docs["task_manager_test_plan_v1.json"]
    boundary = docs["task_manager_skeleton_boundary_matrix_v1.json"]
    nc = docs["task_manager_skeleton_non_claims_v1.json"]
    readiness = docs["task_manager_skeleton_planning_readiness_decision_v1.json"]

    _add(checks, "summary.pass", summary.get("planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "foundation.hw", summary.get("foundation_id") == "midplatform_health_watchdog_foundation_v1")
    _add(checks, "foundation.runtime", summary.get("runtime_status") == "not_enabled")
    _add(checks, "no_redefine.hw", summary.get("must_not_redefine_health_watchdog") is True)
    _add(checks, "no_redefine.dc", summary.get("must_not_redefine_decision_center") is True)

    for item in HEALTH_WATCHDOG_OUTPUTS_CONSUMED:
        _add(checks, f"scope.hw_output.{item}", item in (scope.get("consumes_health_watchdog_frozen_outputs") or []))
    for item in DECISION_CENTER_OUTPUTS_CONSUMED:
        _add(checks, f"scope.dc_output.{item}", item in (scope.get("consumes_decision_center_frozen_outputs") or []))
    for allowed in ("enum", "dataclass", "pure_function", "static_validator", "candidate_generator"):
        _add(checks, f"scope.allowed.{allowed}", allowed in (scope.get("allowed") or []))

    planned = file_plan.get("files") or []
    _add(checks, "file_plan.count3", len(planned) == 3)
    _add(checks, "file_plan.no_create", file_plan.get("create_in_this_phase") is False)
    _add(checks, "file_plan.files_created_false", file_plan.get("task_manager_files_created_now") is False)
    for item in SKELETON_FILE_PLAN:
        match = [f for f in planned if f.get("path") == item["path"]]
        _add(checks, f"file_plan.path.{item['path']}", bool(match))
        _add(checks, f"file_absent.{item['path']}", not (REPO_ROOT / item["path"]).exists())

    enums = types.get("enums") or {}
    for state in TASK_STATE_ENUM:
        _add(checks, f"enum.state.{state}", state in (enums.get("TaskState") or []))
    for readiness_value in TASK_READINESS_ENUM:
        _add(checks, f"enum.readiness.{readiness_value}", readiness_value in (enums.get("TaskReadiness") or []))
    type_docs = {t.get("type_name"): t for t in types.get("candidate_types") or []}
    _add(checks, "type.count6", len(type_docs) == 6)
    for expected in CANDIDATE_TYPES:
        doc = type_docs.get(expected["type_name"]) or {}
        fields = doc.get("fields") or []
        _add(checks, f"type.exists.{expected['type_name']}", bool(doc))
        for field in expected["fields"]:
            _add(checks, f"type.field.{expected['type_name']}.{field}", field in fields)
        for base in REQUIRED_BASE_FIELDS:
            _add(checks, f"type.base.{expected['type_name']}.{base}", base in fields)
        _add(checks, f"type.not_fact.{expected['type_name']}", doc.get("fact_status_default") == "not_fact")
    _add(checks, "type.task.execution_false", type_docs.get("TaskCandidate", {}).get("task_execution_default") is False)
    _add(checks, "type.task.user_output_false", type_docs.get("TaskCandidate", {}).get("user_output_default") is False)
    _add(checks, "type.step.executed_false", type_docs.get("TaskStepCandidate", {}).get("executed_step_default") is False)
    _add(checks, "type.handoff.direct_false", type_docs.get("TaskHandoffCandidate", {}).get("direct_mount_default") is False)

    fn_docs = {f.get("function_name"): f for f in funcs.get("functions") or []}
    _add(checks, "functions.count10", len(fn_docs) == 10)
    for fn in PURE_FUNCTIONS:
        _add(checks, f"function.exists.{fn['function_name']}", fn["function_name"] in fn_docs)
        _add(checks, f"function.output.{fn['function_name']}", bool(fn_docs.get(fn["function_name"], {}).get("output")))
    _add(checks, "function.build_task.execution_false", fn_docs.get("build_task_candidate", {}).get("task_execution") is False)
    _add(checks, "function.step.executed_false", fn_docs.get("build_task_step_candidate", {}).get("executed_step") is False)
    _add(checks, "function.handoff.direct_false", fn_docs.get("build_task_handoff_candidate", {}).get("direct_mount") is False)

    validator_set = set(validators.get("validators") or [])
    _add(checks, "validators.count12", len(validator_set) == 12)
    for val in STATIC_VALIDATORS:
        _add(checks, f"validator.{val}", val in validator_set)

    for item in PROCESSING_CHAIN:
        _add(checks, f"chain.{item}", item in (chain.get("chain") or []))
    _add(checks, "chain.candidate_only", chain.get("candidate_only") is True)
    for rule in GOVERNANCE_GUARD_RULES:
        _add(checks, f"gov.rule.{rule[:50]}", rule in (gov.get("rules") or []))
    for rule in EXECUTION_GUARD_RULES:
        _add(checks, f"execution.rule.{rule[:50]}", rule in (execution.get("rules") or []))
    for rule in HEALTH_WATCHDOG_DEPENDENCY_GUARD_RULES:
        _add(checks, f"hw_guard.rule.{rule[:50]}", rule in (hw_guard.get("rules") or []))
    for rule in DECISION_CENTER_DEPENDENCY_GUARD_RULES:
        _add(checks, f"dc_guard.rule.{rule[:50]}", rule in (dc_guard.get("rules") or []))

    _add(checks, "samples.count7", samples.get("sample_count") >= 7)
    sample_ids = {s.get("sample_id") for s in samples.get("samples") or []}
    for sample in SAMPLE_PLAN:
        _add(checks, f"sample.{sample['sample_id']}", sample["sample_id"] in sample_ids)
    categories = set(tests.get("categories") or [])
    for cat in TEST_PLAN_CATEGORIES:
        _add(checks, f"test.{cat}", cat in categories)

    global_b = boundary.get("global_boundaries") or {}
    for flag in BOUNDARY_FALSE:
        _add(checks, f"boundary.false.{flag}", global_b.get(flag) is False)
        for artifact_name, doc in docs.items():
            _add(checks, f"artifact_boundary.false.{artifact_name}.{flag}", doc.get(flag) is False)
    for claim in NON_CLAIMS:
        _add(checks, f"non_claim.{claim}", claim in (nc.get("non_claims") or []))

    for type_name in type_docs:
        for fn_name in fn_docs:
            _add(checks, f"grid.type_function.{type_name}.{fn_name}", bool(type_name and fn_name))
        for flag in BOUNDARY_FALSE:
            _add(checks, f"grid.type_boundary.{type_name}.{flag}", global_b.get(flag) is False)
    for sample in SAMPLE_PLAN:
        for flag in BOUNDARY_FALSE:
            _add(checks, f"grid.sample_boundary.{sample['sample_id']}.{flag}", global_b.get(flag) is False)

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
