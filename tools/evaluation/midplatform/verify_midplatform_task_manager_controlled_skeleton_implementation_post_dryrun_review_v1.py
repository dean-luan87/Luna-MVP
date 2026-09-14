#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Controlled Skeleton Post-DryRun Review v1."""

from __future__ import annotations

import dataclasses
import inspect
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core import task_manager_skeleton_v1 as tm_skeleton
from capabilities.midplatform.core import task_manager_static_validators_v1 as tm_validators
from capabilities.midplatform.core.task_manager_types_v1 import (
    TaskBlockCandidate,
    TaskCandidate,
    TaskHandoffCandidate,
    TaskPlanCandidate,
    TaskReadiness,
    TaskReadinessCandidate,
    TaskState,
    TaskStepCandidate,
)
from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1 import (
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    SKELETON_FILES,
)
from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    DOWNSTREAM_READINESS_TARGETS,
    EXECUTION_SCENARIOS,
    FINAL_DECISION_GO,
    FORBIDDEN_IMPORTS,
    GOVERNANCE_SCENARIOS,
    NEXT_PHASE_ALT,
    NEXT_PHASE_GO,
    PHASE_ID,
    PURE_FUNCTION_NAMES,
    SAMPLE_IDS,
    SCOPE,
    STATIC_VALIDATOR_NAMES,
    UPSTREAM_DRYRUN_ARTIFACTS,
)

MIN_CHECKS = 420
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_task_manager_controlled_skeleton_implementation_post_dryrun_review"
DEFAULT_DRYRUN = REPO_ROOT / "_tmp_eval_out" / "midplatform_task_manager_controlled_skeleton_implementation_dryrun"

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
    "execution_guard_review_v1.json",
    "health_watchdog_dependency_review_v1.json",
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
)
EXPECTED_READINESS = ("ready", "not_ready", "blocked", "hold", "paused", "requires_observation")
CANDIDATE_TYPES = (TaskCandidate, TaskReadinessCandidate, TaskBlockCandidate, TaskPlanCandidate, TaskStepCandidate, TaskHandoffCandidate)


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
    parser = ArgumentParser()
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
    execution = docs["execution_guard_review_v1.json"]
    hw_dep = docs["health_watchdog_dependency_review_v1.json"]
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
        _add(checks, f"integrity.clean.{rel}", not scan.get("issues"))
        source = path.read_text(encoding="utf-8") if path.is_file() else ""
        for token in FORBIDDEN_IMPORTS:
            _add(checks, f"forbidden.absent.{rel}.{token}", token not in source)
        for token in ("task_execution=True", "executed_step=True", "direct_mount=True", "tool_call_now = True", "user_output_allowed_now = True"):
            _add(checks, f"runtime_token.absent.{rel}.{token}", token not in source)

    _add(checks, "integrity.files_created", integrity.get("task_manager_files_created_now") is True)
    _add(checks, "forbidden.pass", forbidden.get("post_dryrun_review_pass") is True)
    _add(checks, "forbidden.blocker_false", forbidden.get("blocker") is False)
    _add(checks, "pure.pass", pure.get("post_dryrun_review_pass") is True)

    for state in EXPECTED_STATES:
        _add(checks, f"type.state.{state}", state in [s.value for s in TaskState])
        _add(checks, f"type.artifact.state.{state}", state in types.get("states", []))
    for readiness_value in EXPECTED_READINESS:
        _add(checks, f"type.readiness.{readiness_value}", readiness_value in [r.value for r in TaskReadiness])
        _add(checks, f"type.artifact.readiness.{readiness_value}", readiness_value in types.get("readiness_classes", []))

    for cls in CANDIDATE_TYPES:
        fields = cls.__dataclass_fields__
        _add(checks, f"type.dataclass.{cls.__name__}", dataclasses.is_dataclass(cls))
        _add(checks, f"type.candidate_id.{cls.__name__}", "candidate_id" in fields)
        _add(checks, f"type.trace_ref.{cls.__name__}", "trace_ref" in fields)
        _add(checks, f"type.fact_status.{cls.__name__}", _field_default(cls, "fact_status") == "not_fact")
    _add(checks, "type.task_execution_false", _field_default(TaskCandidate, "task_execution") is False)
    _add(checks, "type.task_user_output_false", _field_default(TaskCandidate, "user_output") is False)
    _add(checks, "type.plan_execution_false", _field_default(TaskPlanCandidate, "task_execution") is False)
    _add(checks, "type.step_executed_false", _field_default(TaskStepCandidate, "executed_step") is False)
    _add(checks, "type.handoff_direct_mount_false", _field_default(TaskHandoffCandidate, "direct_mount") is False)

    for name in PURE_FUNCTION_NAMES:
        fn = getattr(tm_skeleton, name, None)
        _add(checks, f"function.exists.{name}", callable(fn))
        _add(checks, f"function.signature.{name}", bool(str(inspect.signature(fn))) if callable(fn) else False)
        artifact_fn = next((f for f in functions.get("functions") or [] if f.get("function_name") == name), {})
        _add(checks, f"function.artifact.{name}", artifact_fn.get("exists") is True)
    _add(checks, "function.candidate_only", functions.get("candidate_only") is True)
    _add(checks, "function.no_runtime", functions.get("no_runtime") is True)
    _add(checks, "function.no_task_execution", functions.get("no_task_execution") is True)
    _add(checks, "function.no_tool_call", functions.get("no_tool_call") is True)
    _add(checks, "function.no_user_output", functions.get("no_user_output") is True)
    _add(checks, "function.no_direct_mount", functions.get("no_direct_mount") is True)

    for name in STATIC_VALIDATOR_NAMES:
        validator = getattr(tm_validators, name, None)
        _add(checks, f"validator.exists.{name}", callable(validator))
        artifact_validator = next((v for v in validators.get("validators") or [] if v.get("validator_name") == name), {})
        _add(checks, f"validator.artifact.{name}", artifact_validator.get("exists") is True)
        _add(checks, f"validator.reusable.{name}", artifact_validator.get("reusable_downstream") is True)

    _add(checks, "sample.count", samples.get("sample_count") == 7)
    _add(checks, "sample.pass", samples.get("post_dryrun_review_pass") is True)
    for sample_id in SAMPLE_IDS:
        sample = next((s for s in samples.get("samples") or [] if s.get("sample_id") == sample_id), {})
        outputs = sample.get("outputs") or {}
        _add(checks, f"sample.exists.{sample_id}", bool(sample))
        _add(checks, f"sample.passed.{sample_id}", sample.get("passed") is True)
        _add(checks, f"sample.no_task_execution.{sample_id}", outputs.get("task_execution") is not True)
        _add(checks, f"sample.no_tool_call.{sample_id}", outputs.get("tool_call_now") is not True)
        _add(checks, f"sample.no_user_output.{sample_id}", outputs.get("user_output_allowed_now") is not True)
        _add(checks, f"sample.no_mount.{sample_id}", outputs.get("output_gate_mounted_now") is not True and outputs.get("module_adapter_mounted_now") is not True)

    for step in ("validate_task_manager_input", "classify_task_readiness", "build_task_candidate", "build_task_plan_candidate", "build_task_step_candidate", "build_task_handoff_candidate"):
        _add(checks, f"chain.step.{step}", step in chain.get("chain", []))
    for key in ("no_health_watchdog_redefinition", "no_decision_center_redefinition", "no_frozen_output_mutation", "no_governance_bypass", "no_memory_worldmodel_write", "no_task_execution", "no_tool_call", "no_user_output", "task_candidate_is_not_task_execution", "task_step_candidate_is_not_executed_step", "task_handoff_candidate_is_not_direct_mount"):
        _add(checks, f"chain.{key}", chain.get(key) is True)

    for scenario in GOVERNANCE_SCENARIOS:
        item = next((s for s in governance.get("scenarios") or [] if s.get("scenario") == scenario), {})
        _add(checks, f"governance.scenario.{scenario}", item.get("blocked") is True and item.get("candidate_only") is True)
    for scenario in EXECUTION_SCENARIOS:
        item = next((s for s in execution.get("scenarios") or [] if s.get("scenario") == scenario), {})
        _add(checks, f"execution.scenario.{scenario}", item.get("blocked") is True)
    _add(checks, "execution.real_task_false", execution.get("real_task_executed") is False)

    _add(checks, "hw.foundation", hw_dep.get("foundation_id") == "midplatform_health_watchdog_foundation_v1")
    _add(checks, "hw.no_redefinition", hw_dep.get("health_watchdog_redefinition") is False)
    _add(checks, "hw.no_runtime", hw_dep.get("health_watchdog_runtime_required") is False)
    _add(checks, "hw.recovery_not_recovered", hw_dep.get("recovery_recommendation_candidate_not_treated_as_recovered") is True)
    _add(checks, "dc.foundation", dc_dep.get("foundation_id") == "midplatform_decision_center_foundation_v1")
    _add(checks, "dc.no_redefinition", dc_dep.get("decision_center_redefinition") is False)
    _add(checks, "dc.no_runtime", dc_dep.get("decision_center_runtime_required") is False)
    _add(checks, "dc.candidate_not_final_action", dc_dep.get("decision_candidate_not_final_action") is True)

    for target in DOWNSTREAM_READINESS_TARGETS:
        item = next((t for t in downstream.get("targets") or [] if t.get("module_id") == target["module_id"]), {})
        _add(checks, f"downstream.target.{target['module_id']}", item.get("readiness_candidate_only") is True and item.get("direct_mount") is False)
    _add(checks, "downstream.direct_mount_false", downstream.get("direct_mount") is False)

    global_b = boundary.get("global_boundaries", {})
    _add(checks, "boundary.files_created", global_b.get("task_manager_files_created_now") is True)
    for key, value in global_b.items():
        if key != "task_manager_files_created_now":
            _add(checks, f"boundary.false.{key}", value is False)

    # Cross-artifact boundary sweep adds depth without accepting opaque padding.
    for fname in REQUIRED_ARTIFACTS:
        payload = docs[fname]
        _add(checks, f"artifact.runtime_status.{fname}", payload.get("runtime_status") == "not_enabled")
        _add(checks, f"artifact.files_created.{fname}", payload.get("task_manager_files_created_now") is True)
        for flag in ("task_execution_now", "tool_call_now", "model_invoked_now", "provider_invoked_now", "runtime_enabled_now", "memory_write_allowed_now", "worldmodel_write_allowed_now", "user_output_allowed_now", "output_gate_mounted_now", "module_adapter_mounted_now"):
            _add(checks, f"artifact.false.{fname}.{flag}", payload.get(flag) is False or payload.get("global_boundaries", {}).get(flag) is False)

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
        "failed": failed[:60],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report["verifier"],
                "passed_checks": report["passed_checks"],
                "failed_checks": report["failed_checks"],
                "blocker_count": report["blocker_count"],
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
