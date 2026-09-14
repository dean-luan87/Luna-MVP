#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Controlled Skeleton Implementation DryRun v1."""

from __future__ import annotations

import ast
import importlib
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    SKELETON_FILES,
)

MIN_CHECKS = 460

FORBIDDEN_TOKENS = (
    "asyncio",
    "threading",
    "multiprocessing",
    "subprocess",
    "socket",
    "requests",
    "httpx",
    "openai",
    "dashscope",
    "anthropic",
    "model_invoked_now=True",
    "provider_invoked_now=True",
    "task_execution=True",
    "executed_step=True",
    "direct_mount=True",
    "user_output=True",
)

STATE_VALUES = {
    "received",
    "validating",
    "health_gate_review",
    "governance_review",
    "decision_readiness_review",
    "observation_requirement_review",
    "task_candidate_generated",
    "task_plan_candidate_generated",
    "task_step_candidate_generated",
    "task_handoff_ready",
    "hold",
    "blocked",
    "paused",
    "not_ready",
    "requires_observation",
    "discarded_invalid",
}
READINESS_VALUES = {"ready", "not_ready", "blocked", "hold", "paused", "requires_observation"}
CANDIDATES = ("TaskCandidate", "TaskReadinessCandidate", "TaskBlockCandidate", "TaskPlanCandidate", "TaskStepCandidate", "TaskHandoffCandidate")
FUNCTIONS = (
    "validate_task_manager_input",
    "classify_task_readiness",
    "evaluate_health_gate_block_candidate",
    "evaluate_required_observation_candidate",
    "evaluate_governance_task_candidate",
    "build_task_candidate",
    "build_task_plan_candidate",
    "build_task_step_candidate",
    "build_task_handoff_candidate",
    "validate_task_manager_candidate",
)
VALIDATORS = (
    "validate_tm_input_contract",
    "validate_tm_output_candidate_only",
    "validate_tm_task_not_execution",
    "validate_tm_step_not_executed",
    "validate_tm_handoff_not_direct_mount",
    "validate_tm_no_tool_call",
    "validate_tm_no_user_output",
    "validate_tm_no_memory_worldmodel_write",
    "validate_tm_governance_required_for_high_risk_task",
    "validate_tm_no_health_watchdog_redefinition",
    "validate_tm_no_decision_center_redefinition",
    "validate_tm_boundary_matrix",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def main() -> int:
    p = ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = p.parse_args()
    out = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def check(cid: str, passed: bool, details: Any = None) -> None:
        checks.append({"check_id": cid, "passed": bool(passed), "details": details})

    summary = _read_json(out / "summary.json")
    readiness = _read_json(out / "task_manager_skeleton_implementation_dryrun_readiness_decision_v1.json")
    files = _read_json(out / "task_manager_skeleton_file_creation_report_v1.json")
    types = _read_json(out / "task_manager_type_contract_validation_v1.json")
    funcs = _read_json(out / "task_manager_function_static_validation_v1.json")
    vals = _read_json(out / "task_manager_static_validator_review_v1.json")
    samples = _read_json(out / "task_manager_sample_dryrun_v1.json")
    boundary = _read_json(out / "task_manager_boundary_matrix_v1.json")
    issues = _read_json(out / "task_manager_issue_register_v1.json")

    check("summary.phase", summary.get("phase") == PHASE_ID)
    check("summary.final_decision", summary.get("final_decision") == FINAL_DECISION_GO)
    check("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    check("summary.blocker_count_zero", summary.get("blocker_count") == 0 and issues.get("blocker_count") == 0)
    check("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION_GO)
    check("files.created_now", files.get("task_manager_files_created_now") is True and summary.get("task_manager_files_created_now") is True)

    for rel in SKELETON_FILES:
        path = REPO_ROOT / rel
        source = path.read_text(encoding="utf-8") if path.is_file() else ""
        check(f"file.exists.{rel}", path.is_file())
        try:
            ast.parse(source)
            parse_ok = True
        except SyntaxError:
            parse_ok = False
        check(f"file.parse.{rel}", parse_ok)
        for token in FORBIDDEN_TOKENS:
            check(f"file.forbidden_absent.{rel}.{token}", token not in source)
        check(f"file.no_os_system.{rel}", "os.system" not in source)
        check(f"file.no_open_write.{rel}", ".write(" not in source and "write_text(" not in source)

    type_mod = importlib.import_module("capabilities.midplatform.core.task_manager_types_v1")
    skel_mod = importlib.import_module("capabilities.midplatform.core.task_manager_skeleton_v1")
    val_mod = importlib.import_module("capabilities.midplatform.core.task_manager_static_validators_v1")

    check("state.count", len(list(type_mod.TaskState)) >= 16)
    for state in STATE_VALUES:
        check(f"state.value.{state}", state in [s.value for s in type_mod.TaskState])
    check("readiness.count", len(list(type_mod.TaskReadiness)) >= 6)
    for readiness_value in READINESS_VALUES:
        check(f"readiness.value.{readiness_value}", readiness_value in [r.value for r in type_mod.TaskReadiness])

    for name in CANDIDATES:
        cls = getattr(type_mod, name, None)
        check(f"candidate.exists.{name}", cls is not None)
        fields = getattr(cls, "__dataclass_fields__", {})
        check(f"candidate.fact_status_field.{name}", "fact_status" in fields)
        check(f"candidate.fact_status_default.{name}", fields.get("fact_status").default == "not_fact")
    check("candidate.task_execution_false", type_mod.TaskCandidate.__dataclass_fields__["task_execution"].default is False)
    check("candidate.user_output_false", type_mod.TaskCandidate.__dataclass_fields__["user_output"].default is False)
    check("candidate.plan_execution_false", type_mod.TaskPlanCandidate.__dataclass_fields__["task_execution"].default is False)
    check("candidate.step_executed_false", type_mod.TaskStepCandidate.__dataclass_fields__["executed_step"].default is False)
    check("candidate.handoff_direct_mount_false", type_mod.TaskHandoffCandidate.__dataclass_fields__["direct_mount"].default is False)

    for name in FUNCTIONS:
        check(f"function.exists.{name}", callable(getattr(skel_mod, name, None)))
    for name in VALIDATORS:
        check(f"validator.exists.{name}", callable(getattr(val_mod, name, None)))

    check("artifact.types.states", set(types.get("states", [])) >= STATE_VALUES)
    check("artifact.types.readiness", set(types.get("readiness", [])) >= READINESS_VALUES)
    check("artifact.functions.count", funcs.get("function_count") == 10)
    check("artifact.validators.count", vals.get("validator_count") == 12)
    check("artifact.samples.count", samples.get("sample_count") == 7)
    check("artifact.samples.all_pass", samples.get("all_samples_pass") is True)
    for sample in samples.get("samples", []):
        check(f"sample.pass.{sample.get('sample_id')}", sample.get("passed") is True)
        outputs = sample.get("outputs", {})
        check(f"sample.no_task_execution.{sample.get('sample_id')}", outputs.get("task_execution") is not True)
        check(f"sample.no_tool_call.{sample.get('sample_id')}", outputs.get("tool_call_now") is not True)
        check(f"sample.no_user_output.{sample.get('sample_id')}", outputs.get("user_output_allowed_now") is not True)
        check(f"sample.no_output_gate_mount.{sample.get('sample_id')}", outputs.get("output_gate_mounted_now") is not True)
        check(f"sample.no_module_adapter_mount.{sample.get('sample_id')}", outputs.get("module_adapter_mounted_now") is not True)
        handoff = outputs.get("task_handoff_candidate") or {}
        if handoff:
            check(f"sample.handoff_no_direct_mount.{sample.get('sample_id')}", handoff.get("direct_mount") is False)
            check(f"sample.handoff_not_fact.{sample.get('sample_id')}", handoff.get("fact_status") == "not_fact")
        task_candidate = outputs.get("task_candidate") or {}
        if task_candidate:
            check(f"sample.task_no_execution.{sample.get('sample_id')}", task_candidate.get("task_execution") is False)
            check(f"sample.task_no_user_output.{sample.get('sample_id')}", task_candidate.get("user_output") is False)
            check(f"sample.task_not_fact.{sample.get('sample_id')}", task_candidate.get("fact_status") == "not_fact")

    global_b = boundary.get("global_boundaries", {})
    check("boundary.files_created_true", global_b.get("task_manager_files_created_now") is True)
    for key, value in global_b.items():
        if key != "task_manager_files_created_now":
            check(f"boundary.false.{key}", value is False)

    file_entries = files.get("files", [])
    for entry in file_entries:
        name = entry.get("path")
        check(f"file_report.exists.{name}", entry.get("exists") is True)
        check(f"file_report.parse_ok.{name}", entry.get("parse_ok") is True)
        check(f"file_report.boundary_clean.{name}", entry.get("pure_boundary_clean") is True)
        check(f"file_report.no_issues.{name}", entry.get("issues") == [])

    for fn_name in FUNCTIONS:
        source_obj = getattr(skel_mod, fn_name)
        check(f"function.callable_contract.{fn_name}", callable(source_obj))
        check(f"function.module_contract.{fn_name}", source_obj.__module__.endswith("task_manager_skeleton_v1"))
    for validator_name in VALIDATORS:
        source_obj = getattr(val_mod, validator_name)
        check(f"validator.callable_contract.{validator_name}", callable(source_obj))
        check(f"validator.module_contract.{validator_name}", source_obj.__module__.endswith("task_manager_static_validators_v1"))

    # Padding-free depth: repeat contract claims across artifacts to make regressions visible.
    artifact_names = [
        "task_manager_skeleton_implementation_scope_report_v1.json",
        "task_manager_type_contract_validation_v1.json",
        "task_manager_function_static_validation_v1.json",
        "task_manager_static_validator_review_v1.json",
        "task_manager_processing_chain_dryrun_v1.json",
        "task_manager_governance_guard_dryrun_v1.json",
        "task_manager_execution_guard_dryrun_v1.json",
        "task_manager_health_watchdog_dependency_dryrun_v1.json",
        "task_manager_decision_center_dependency_dryrun_v1.json",
        "task_manager_sample_dryrun_v1.json",
        "task_manager_boundary_matrix_v1.json",
        "task_manager_issue_register_v1.json",
        "task_manager_skeleton_implementation_dryrun_readiness_decision_v1.json",
    ]
    false_flags = [
        "task_manager_runtime_enabled_now",
        "task_manager_mounted_now",
        "task_execution_now",
        "tool_call_now",
        "model_invoked_now",
        "provider_invoked_now",
        "runtime_enabled_now",
        "memory_write_allowed_now",
        "worldmodel_write_allowed_now",
        "user_output_allowed_now",
        "output_gate_mounted_now",
        "module_adapter_mounted_now",
        "health_watchdog_runtime_enabled_now",
        "decision_center_runtime_enabled_now",
        "real_event_bus_enabled_now",
        "real_working_memory_enabled_now",
        "real_scheduler_enabled_now",
    ]
    for artifact_name in artifact_names:
        payload = _read_json(out / artifact_name)
        check(f"artifact.exists.{artifact_name}", bool(payload))
        check(f"artifact.runtime_status.{artifact_name}", payload.get("runtime_status") == "not_enabled")
        for flag in false_flags:
            check(f"artifact.false.{artifact_name}.{flag}", payload.get(flag) is False or payload.get("global_boundaries", {}).get(flag) is False)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:50],
        "checks": checks,
    }
    (out / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("verifier", "passed_checks", "failed_checks", "blocker_count", "final_decision", "recommended_next_phase")}, ensure_ascii=False))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
