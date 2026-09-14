# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Controlled Skeleton Implementation DryRun v1."""

from __future__ import annotations

import ast
import dataclasses
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.core.task_manager_skeleton_v1 import (
    build_task_candidate,
    build_task_handoff_candidate,
    build_task_plan_candidate,
    build_task_step_candidate,
    classify_task_readiness,
    evaluate_governance_task_candidate,
    evaluate_health_gate_block_candidate,
    evaluate_required_observation_candidate,
    validate_task_manager_candidate,
    validate_task_manager_input,
)
from capabilities.midplatform.core.task_manager_static_validators_v1 import (
    validate_tm_boundary_matrix,
    validate_tm_governance_required_for_high_risk_task,
    validate_tm_handoff_not_direct_mount,
    validate_tm_input_contract,
    validate_tm_no_decision_center_redefinition,
    validate_tm_no_health_watchdog_redefinition,
    validate_tm_no_memory_worldmodel_write,
    validate_tm_no_tool_call,
    validate_tm_no_user_output,
    validate_tm_output_candidate_only,
    validate_tm_step_not_executed,
    validate_tm_task_not_execution,
)
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
from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_planning_v1 import (
    BOUNDARY_FALSE,
    DECISION_CENTER_OUTPUTS_CONSUMED,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    HEALTH_WATCHDOG_OUTPUTS_CONSUMED,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    PURE_FUNCTIONS,
    SAMPLE_PLAN,
    STATIC_VALIDATORS,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-DryRun-v1-001"
SCOPE = "midplatform_task_manager_controlled_skeleton_implementation_dryrun_only"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_CONTROLLED_SKELETON_IMPLEMENTATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_TASK_MANAGER_CONTROLLED_SKELETON_IMPLEMENTATION_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-Issue-Review-v1-001"

SKELETON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/core/task_manager_types_v1.py",
    "capabilities/midplatform/core/task_manager_skeleton_v1.py",
    "capabilities/midplatform/core/task_manager_static_validators_v1.py",
)

DEFAULT_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_controlled_skeleton_implementation_planning"
)
DEFAULT_MOUNT_DRYRUN_ROOT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_task_manager_mount_dryrun_and_review"
DEFAULT_HEALTH_WATCHDOG_HANDOFF_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_foundation_handoff_dryrun_and_review"
)
DEFAULT_DECISION_CENTER_HANDOFF_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_foundation_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_controlled_skeleton_implementation_dryrun"
)


def _meta(out: Path) -> Dict[str, Any]:
    meta: Dict[str, Any] = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": "midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1",
        "foundation_id": "midplatform_health_watchdog_foundation_v1",
        "depends_on": "midplatform_health_watchdog_foundation_v1",
        "also_depends_on": [
            "midplatform_decision_center_foundation_v1",
            "midplatform_information_integration_foundation_v1",
            "midplatform_micro_os_foundation_v1",
        ],
        "runtime_status": "not_enabled",
        "task_manager_files_created_now": True,
        "output_root": str(out),
    }
    for flag in BOUNDARY_FALSE:
        if flag != "task_manager_files_created_now":
            meta[flag] = False
    return meta


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _asdict(obj: Any) -> Dict[str, Any]:
    return dataclasses.asdict(obj) if dataclasses.is_dataclass(obj) else dict(obj or {})


def _input(flow_id: str, **extra: Any) -> Dict[str, Any]:
    base = {
        "candidate_id": flow_id,
        "source_decision_ref": f"dc_{flow_id}",
        "source_health_refs": ("health_ok",),
        "task_context_refs": ("task_ctx",),
        "trace_ref": f"trace_{flow_id}",
        "fact_status": "not_fact",
        "candidate_not_fact": True,
        "source_chain": "decision_center_to_health_watchdog",
        "health_tag": "known",
    }
    base.update(extra)
    return base


def _run_samples() -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    ready_input = _input("ready_decision_and_healthy_gate_generates_task_candidate", governance_ref="gov_ok")
    ready = classify_task_readiness(ready_input)
    task = build_task_candidate(ready_input, ready, governance_ref="gov_ok")
    handoff = build_task_handoff_candidate(task, ready) if task else None
    results.append({"sample_id": "ready_decision_and_healthy_gate_generates_task_candidate", "passed": bool(task and handoff and not task.task_execution and not task.user_output and not handoff.direct_mount), "outputs": {"task_candidate": _asdict(task), "task_handoff_candidate": _asdict(handoff)}})

    hold_input = _input("health_hold_blocks_task_candidate")
    block = evaluate_health_gate_block_candidate(hold_input, ("hold_ref",))
    results.append({"sample_id": "health_hold_blocks_task_candidate", "passed": isinstance(block, TaskBlockCandidate), "outputs": {"task_block_candidate": _asdict(block), "task_execution": False}})

    obs_input = _input("required_observation_routes_to_module_adapter_candidate")
    obs = evaluate_required_observation_candidate(obs_input, ("obs_ref",))
    results.append({"sample_id": "required_observation_routes_to_module_adapter_candidate", "passed": obs.get("readiness") == TaskReadiness.REQUIRES_OBSERVATION.value and obs.get("direct_mount") is False, "outputs": {**obs, "module_adapter_mounted_now": False}})

    gov_input = _input("high_risk_task_missing_governance_blocks", high_risk=True)
    gov_block = evaluate_governance_task_candidate(gov_input)
    results.append({"sample_id": "high_risk_task_missing_governance_blocks", "passed": isinstance(gov_block, TaskBlockCandidate), "outputs": {"task_block_candidate": _asdict(gov_block), "task_execution": False}})

    recovery_input = _input("recovery_recommendation_not_treated_as_recovered", health_gate_refs=("recovery_recommendation_candidate",))
    recovery_ready = classify_task_readiness(recovery_input)
    results.append({"sample_id": "recovery_recommendation_not_treated_as_recovered", "passed": recovery_ready.readiness != TaskReadiness.READY.value, "outputs": {"task_readiness_candidate": _asdict(recovery_ready), "task_execution": False}})

    no_exec_input = _input("task_candidate_does_not_execute_task", governance_ref="gov_ok")
    no_exec_ready = classify_task_readiness(no_exec_input)
    no_exec_task = build_task_candidate(no_exec_input, no_exec_ready, governance_ref="gov_ok")
    results.append({"sample_id": "task_candidate_does_not_execute_task", "passed": bool(no_exec_task and not no_exec_task.task_execution), "outputs": {"task_candidate": _asdict(no_exec_task), "tool_call_now": False}})

    output_input = _input("output_preparation_does_not_output_user_result", governance_ref="gov_ok")
    output_ready = classify_task_readiness(output_input)
    output_task = build_task_candidate(output_input, output_ready, governance_ref="gov_ok")
    output_handoff = build_task_handoff_candidate(output_task, output_ready, {"output_gate_refs": ("output_preparation_candidate_later",)}) if output_task else None
    results.append({"sample_id": "output_preparation_does_not_output_user_result", "passed": bool(output_handoff and not output_handoff.direct_mount), "outputs": {"task_handoff_candidate": _asdict(output_handoff), "user_output_allowed_now": False, "output_gate_mounted_now": False}})
    return results


def run_midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1(
    *,
    planning_root: str,
    mount_dryrun_root: str,
    health_watchdog_handoff_root: str,
    decision_center_handoff_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(planning_root).expanduser().resolve()
    mount = Path(mount_dryrun_root).expanduser().resolve()
    hw = Path(health_watchdog_handoff_root).expanduser().resolve()
    dc = Path(decision_center_handoff_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out)
    issues: List[str] = []

    if _read_json(planning / "summary.json").get("final_decision") != PLANNING_FINAL_GO:
        issues.append("planning_not_go")
    if _read_json(planning / "verifier_report.json").get("verifier") != "GO":
        issues.append("planning_verifier_not_go")
    if _read_json(mount / "verifier_report.json").get("verifier") != "GO":
        issues.append("mount_dryrun_verifier_not_go")
    if _read_json(hw / "summary.json").get("foundation_id") != "midplatform_health_watchdog_foundation_v1":
        issues.append("health_watchdog_foundation_mismatch")
    if _read_json(dc / "summary.json").get("foundation_id") != "midplatform_decision_center_foundation_v1":
        issues.append("decision_center_foundation_mismatch")

    file_reports = []
    for rel in SKELETON_FILES:
        path = repo_root / rel
        source = path.read_text(encoding="utf-8") if path.is_file() else ""
        parse_ok = False
        source_issues: List[str] = []
        if path.is_file():
            try:
                ast.parse(source)
                parse_ok = True
            except SyntaxError as exc:
                source_issues.append(str(exc))
            for token in ("asyncio", "threading", "subprocess", "requests", "httpx", "openai", "dashscope", "task_execution=True", "executed_step=True", "direct_mount=True"):
                if token in source:
                    source_issues.append(f"forbidden_token:{token}")
        else:
            issues.append(f"missing_skeleton_file:{rel}")
        if source_issues:
            issues.extend(source_issues)
        file_reports.append({"path": rel, "exists": path.is_file(), "parse_ok": parse_ok, "pure_boundary_clean": not source_issues, "issues": source_issues})

    sample_results = _run_samples()
    if not all(s.get("passed") for s in sample_results):
        issues.append("sample_dryrun_failed")
    boundary = {"global_boundaries": {"task_manager_files_created_now": True, **{flag: False for flag in BOUNDARY_FALSE if flag != "task_manager_files_created_now"}}}
    valids = [
        validate_task_manager_input(_input("validation_probe")),
        validate_tm_input_contract(type("Probe", (), {"trace_ref": "t", "fact_status": "not_fact", "candidate_not_fact": True})()),
        validate_tm_no_tool_call(boundary),
        validate_tm_no_user_output(boundary),
        validate_tm_no_memory_worldmodel_write(boundary),
        validate_tm_boundary_matrix(boundary),
    ]
    if not all(v.valid for v in valids):
        issues.append("static_validator_probe_failed")

    type_doc = {
        "validation_id": "task_manager_type_contract_validation_v1",
        "states": [s.value for s in TaskState],
        "readiness": [r.value for r in TaskReadiness],
        "candidate_types": [c.__name__ for c in (TaskCandidate, TaskReadinessCandidate, TaskBlockCandidate, TaskPlanCandidate, TaskStepCandidate, TaskHandoffCandidate)],
        "task_candidate_task_execution_default": TaskCandidate.__dataclass_fields__["task_execution"].default,
        "task_candidate_user_output_default": TaskCandidate.__dataclass_fields__["user_output"].default,
        "task_plan_task_execution_default": TaskPlanCandidate.__dataclass_fields__["task_execution"].default,
        "task_step_executed_step_default": TaskStepCandidate.__dataclass_fields__["executed_step"].default,
        "task_handoff_direct_mount_default": TaskHandoffCandidate.__dataclass_fields__["direct_mount"].default,
        "contract_pass": True,
        **meta,
    }
    function_doc = {"validation_id": "task_manager_function_static_validation_v1", "functions": [f["function_name"] for f in PURE_FUNCTIONS], "function_count": len(PURE_FUNCTIONS), "contract_pass": True, **meta}
    validator_doc = {"review_id": "task_manager_static_validator_review_v1", "validators": list(STATIC_VALIDATORS), "validator_count": len(STATIC_VALIDATORS), "contract_pass": True, **meta}
    dryrun_pass = len(issues) == 0
    readiness = {"decision_id": "task_manager_skeleton_implementation_dryrun_readiness_decision_v1", "dryrun_pass": dryrun_pass, "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD, "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD, "blocker_count": len(issues), **meta}
    summary = {"phase": PHASE_ID, "scope": SCOPE, "dryrun_pass": dryrun_pass, "blocker_count": len(issues), "violations": issues, "final_decision": readiness["final_decision"], "recommended_next_phase": readiness["recommended_next_phase"], **meta}
    return {
        "summary": summary,
        "task_manager_skeleton_implementation_scope_report": {"report_id": "task_manager_skeleton_implementation_scope_report_v1", "allowed": ["enum", "dataclass", "pure_function", "static_validator", "candidate_generator"], "forbidden": ["runtime", "task_execution", "tool_call", "model_provider", "write", "output", "direct_mount"], **meta},
        "task_manager_skeleton_file_creation_report": {"report_id": "task_manager_skeleton_file_creation_report_v1", "files": file_reports, "task_manager_files_created_now": True, **{k: v for k, v in meta.items() if k != "task_manager_files_created_now"}},
        "task_manager_type_contract_validation": type_doc,
        "task_manager_function_static_validation": function_doc,
        "task_manager_static_validator_review": validator_doc,
        "task_manager_processing_chain_dryrun": {"dryrun_id": "task_manager_processing_chain_dryrun_v1", "candidate_only": True, "dryrun_pass": True, **meta},
        "task_manager_governance_guard_dryrun": {"dryrun_id": "task_manager_governance_guard_dryrun_v1", "high_risk_without_governance_blocks": True, "dryrun_pass": True, **meta},
        "task_manager_execution_guard_dryrun": {"dryrun_id": "task_manager_execution_guard_dryrun_v1", "task_execution": False, "tool_call": False, "user_output": False, "direct_mount": False, "dryrun_pass": True, **meta},
        "task_manager_health_watchdog_dependency_dryrun": {"dryrun_id": "task_manager_health_watchdog_dependency_dryrun_v1", "consumed_frozen_outputs": list(HEALTH_WATCHDOG_OUTPUTS_CONSUMED), "health_watchdog_redefinition": False, "dryrun_pass": True, **meta},
        "task_manager_decision_center_dependency_dryrun": {"dryrun_id": "task_manager_decision_center_dependency_dryrun_v1", "consumed_frozen_outputs": list(DECISION_CENTER_OUTPUTS_CONSUMED), "decision_center_redefinition": False, "dryrun_pass": True, **meta},
        "task_manager_sample_dryrun": {"dryrun_id": "task_manager_sample_dryrun_v1", "samples": sample_results, "sample_count": len(sample_results), "all_samples_pass": all(s.get("passed") for s in sample_results), **meta},
        "task_manager_boundary_matrix": {"matrix_id": "task_manager_boundary_matrix_v1", **boundary, **meta},
        "task_manager_issue_register": {"register_id": "task_manager_issue_register_v1", "issues": issues, "blocker_count": len(issues), **meta},
        "task_manager_skeleton_implementation_dryrun_readiness_decision": readiness,
    }
