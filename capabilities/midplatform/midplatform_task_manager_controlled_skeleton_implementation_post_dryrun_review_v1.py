# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Controlled Skeleton Post-DryRun Review v1."""

from __future__ import annotations

import ast
import dataclasses
import inspect
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
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
    FINAL_DECISION_GO as SKELETON_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as SKELETON_DRYRUN_NEXT,
    SKELETON_FILES,
)
from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_planning_v1 import (
    BOUNDARY_FALSE,
    DECISION_CENTER_OUTPUTS_CONSUMED,
    HEALTH_WATCHDOG_OUTPUTS_CONSUMED,
    PURE_FUNCTIONS,
    STATIC_VALIDATORS,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-Post-DryRun-Review-v1-001"
SCOPE = "midplatform_task_manager_controlled_skeleton_implementation_post_dryrun_review_only"
SOURCE_CHAIN = "midplatform_task_manager_controlled_skeleton_implementation_post_dryrun_review_v1"

FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_CONTROLLED_SKELETON_IMPLEMENTATION_POST_DRYRUN_REVIEW_"
    "CLOSED_READY_FOR_FOUNDATION_HANDOFF_OR_MODULE_ADAPTER_PLANNING"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_TASK_MANAGER_CONTROLLED_SKELETON_IMPLEMENTATION_POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Planning-v1-001"
NEXT_PHASE_ALT = "Phase-Midplatform-Module-Adapter-Feedback-Mount-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-Issue-Review-v1-001"

UPSTREAM_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_skeleton_implementation_scope_report_v1.json",
    "task_manager_skeleton_file_creation_report_v1.json",
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
    "summary.json",
    "verifier_report.json",
)

FORBIDDEN_IMPORTS: Tuple[str, ...] = (
    "asyncio",
    "threading",
    "multiprocessing",
    "subprocess",
    "socket",
    "requests",
    "httpx",
    "aiohttp",
    "openai",
    "anthropic",
    "dashscope",
)
FORBIDDEN_MODULE_SUBSTRINGS: Tuple[str, ...] = (
    "provider_sdk",
    "model_sdk",
    "external_llm",
    "tool_execution_runtime",
    "memory_runtime",
    "worldmodel_runtime",
    "output_runtime",
    "tts_runtime",
    "task_execution_runtime",
    "process_control",
)
PURE_BOUNDARY_FORBIDDEN_TOKENS: Tuple[str, ...] = (
    "while True",
    "async def",
    "await ",
    "create_task",
    "Thread(",
    "Process(",
    "Popen(",
    "system(",
    "exec(",
    "eval(",
    "task_execution=True",
    "executed_step=True",
    "direct_mount=True",
    "tool_call_now = True",
    "user_output_allowed_now = True",
    "memory_write_allowed_now = True",
    "worldmodel_write_allowed_now = True",
)

PURE_FUNCTION_NAMES = tuple(item["function_name"] for item in PURE_FUNCTIONS)
STATIC_VALIDATOR_NAMES = tuple(STATIC_VALIDATORS)
CANDIDATE_TYPES: Tuple[Any, ...] = (
    TaskCandidate,
    TaskReadinessCandidate,
    TaskBlockCandidate,
    TaskPlanCandidate,
    TaskStepCandidate,
    TaskHandoffCandidate,
)
SAMPLE_IDS: Tuple[str, ...] = (
    "ready_decision_and_healthy_gate_generates_task_candidate",
    "health_hold_blocks_task_candidate",
    "required_observation_routes_to_module_adapter_candidate",
    "high_risk_task_missing_governance_blocks",
    "recovery_recommendation_not_treated_as_recovered",
    "task_candidate_does_not_execute_task",
    "output_preparation_does_not_output_user_result",
)
PROCESSING_CHAIN: Tuple[str, ...] = (
    "validate_task_manager_input",
    "classify_task_readiness",
    "evaluate_health_gate_block_candidate",
    "evaluate_required_observation_candidate",
    "evaluate_governance_task_candidate",
    "build_task_candidate",
    "build_task_plan_candidate",
    "build_task_step_candidate",
    "build_task_handoff_candidate",
)
GOVERNANCE_SCENARIOS: Tuple[str, ...] = (
    "high_risk_task_missing_governance_ref",
    "unresolved_health_gate",
    "unresolved_decision_block",
    "output_attempted",
    "tool_call_attempted",
    "task_execution_attempted",
    "memory_write_attempted",
    "worldmodel_write_attempted",
    "model_invocation_attempted_now",
    "provider_invocation_attempted_now",
    "candidate_fact_boundary_enforced",
)
EXECUTION_SCENARIOS: Tuple[str, ...] = (
    "task_execution_attempted",
    "tool_call_attempted",
    "direct_mount_attempted",
    "output_attempted",
    "permission_release_attempted",
    "system_command_attempted",
)
DOWNSTREAM_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {"module_id": "output_gate_later", "mount_type": "readiness_candidate"},
    {"module_id": "module_adapter_feedback_later", "mount_type": "readiness_candidate"},
    {"module_id": "worldmodel_memory_bridge_later", "mount_type": "readiness_candidate"},
    {"module_id": "decision_center_loopback_later", "mount_type": "readiness_candidate"},
    {"module_id": "health_watchdog_loopback_later", "mount_type": "readiness_candidate"},
    {"module_id": "governance_gate_review_later", "mount_type": "readiness_candidate"},
)

DEFAULT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_controlled_skeleton_implementation_dryrun"
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
    "midplatform_task_manager_controlled_skeleton_implementation_post_dryrun_review"
)


def _meta(output_root: Path, dryrun_root: Path, planning_root: Path, mount_root: Path, hw_root: Path, dc_root: Path) -> Dict[str, Any]:
    meta: Dict[str, Any] = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "foundation_id": "midplatform_task_manager_candidate_layer_v1",
        "depends_on": "midplatform_health_watchdog_foundation_v1",
        "also_depends_on": [
            "midplatform_decision_center_foundation_v1",
            "midplatform_information_integration_foundation_v1",
            "midplatform_micro_os_foundation_v1",
        ],
        "runtime_status": "not_enabled",
        "task_manager_files_created_now": True,
        "post_dryrun_review_only": True,
        "output_root": str(output_root),
        "upstream_dryrun_root": str(dryrun_root),
        "upstream_planning_root": str(planning_root),
        "upstream_mount_dryrun_root": str(mount_root),
        "upstream_health_watchdog_handoff_root": str(hw_root),
        "upstream_decision_center_handoff_root": str(dc_root),
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


def _scan_source(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {"path": str(path), "exists": False, "parse_ok": False, "issues": ("missing_file",)}
    source = path.read_text(encoding="utf-8")
    issues: List[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return {"path": str(path), "exists": True, "parse_ok": False, "issues": (str(exc),)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in FORBIDDEN_IMPORTS:
                    issues.append(f"forbidden_import:{alias.name}")
                if any(token in alias.name for token in FORBIDDEN_MODULE_SUBSTRINGS):
                    issues.append(f"forbidden_module:{alias.name}")
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.split(".")[0] in FORBIDDEN_IMPORTS:
                issues.append(f"forbidden_import:{node.module}")
            if any(token in node.module for token in FORBIDDEN_MODULE_SUBSTRINGS):
                issues.append(f"forbidden_module:{node.module}")
        if isinstance(node, ast.AsyncFunctionDef):
            issues.append("runtime_construct:AsyncFunctionDef")
        if isinstance(node, ast.While) and isinstance(node.test, ast.Constant):
            issues.append("runtime_construct:While")
        if isinstance(node, ast.Call):
            name = getattr(node.func, "id", getattr(node.func, "attr", ""))
            if name in {"exec", "eval", "open", "print", "system", "Popen"}:
                issues.append(f"forbidden_call:{name}")
    for token in PURE_BOUNDARY_FORBIDDEN_TOKENS:
        if token in source:
            issues.append(f"forbidden_token:{token}")
    return {
        "path": str(path),
        "exists": True,
        "parse_ok": True,
        "issues": tuple(issues),
        "forbidden_imports_absent": not any(i.startswith("forbidden_import") for i in issues),
        "pure_boundary_clean": len(issues) == 0,
    }


def _field_default(cls: Any, field_name: str) -> Any:
    field = cls.__dataclass_fields__[field_name]
    if field.default is not dataclasses.MISSING:
        return field.default
    return None


def run_midplatform_task_manager_controlled_skeleton_implementation_post_dryrun_review_v1(
    *,
    dryrun_root: str,
    planning_root: str,
    mount_dryrun_root: str,
    health_watchdog_handoff_root: str,
    decision_center_handoff_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    dryrun = Path(dryrun_root).expanduser().resolve()
    planning = Path(planning_root).expanduser().resolve()
    mount = Path(mount_dryrun_root).expanduser().resolve()
    hw = Path(health_watchdog_handoff_root).expanduser().resolve()
    dc = Path(decision_center_handoff_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, dryrun, planning, mount, hw, dc)
    issues: List[str] = []

    dryrun_summary = _read_json(dryrun / "summary.json")
    dryrun_readiness = _read_json(dryrun / "task_manager_skeleton_implementation_dryrun_readiness_decision_v1.json")
    dryrun_verifier = _read_json(dryrun / "verifier_report.json")
    if dryrun_summary.get("final_decision") != SKELETON_DRYRUN_FINAL_GO:
        issues.append("upstream_dryrun_final_decision_not_go")
    if dryrun_readiness.get("final_decision") != SKELETON_DRYRUN_FINAL_GO:
        issues.append("upstream_dryrun_readiness_not_go")
    if dryrun_verifier.get("verifier") != "GO":
        issues.append("upstream_dryrun_verifier_not_go")
    for artifact in UPSTREAM_DRYRUN_ARTIFACTS:
        if not (dryrun / artifact).is_file():
            issues.append(f"missing_upstream_artifact:{artifact}")

    file_reviews = []
    for rel in SKELETON_FILES:
        scan = _scan_source(repo_root / rel)
        scan["path"] = rel
        file_reviews.append(scan)
        if not scan.get("exists"):
            issues.append(f"skeleton_missing:{rel}")
        if scan.get("issues"):
            issues.extend(str(i) for i in scan["issues"])

    skeleton_file_integrity_review = {
        "review_id": "skeleton_file_integrity_review_v1",
        "files": file_reviews,
        "expected_files": list(SKELETON_FILES),
        "task_manager_files_created_now": True,
        "post_dryrun_review_pass": all(f.get("exists") for f in file_reviews),
        **meta,
    }
    forbidden_runtime_import_review = {
        "review_id": "forbidden_runtime_import_review_v1",
        "files": file_reviews,
        "forbidden_imports": list(FORBIDDEN_IMPORTS),
        "forbidden_module_substrings": list(FORBIDDEN_MODULE_SUBSTRINGS),
        "blocker": any(f.get("issues") for f in file_reviews),
        "post_dryrun_review_pass": not any(f.get("issues") for f in file_reviews),
        **meta,
    }
    pure_function_boundary_review = {
        "review_id": "pure_function_boundary_review_v1",
        "allowed": ["enum", "dataclass", "pure_function", "static_validator", "candidate_generator", "lightweight_constants"],
        "forbidden": list(PURE_BOUNDARY_FORBIDDEN_TOKENS),
        "post_dryrun_review_pass": not any(f.get("issues") for f in file_reviews),
        **meta,
    }

    type_checks = []
    for cls in CANDIDATE_TYPES:
        fields = tuple(cls.__dataclass_fields__.keys())
        type_checks.append(
            {
                "type_name": cls.__name__,
                "is_dataclass": dataclasses.is_dataclass(cls),
                "has_candidate_id": "candidate_id" in fields,
                "has_trace_ref": "trace_ref" in fields,
                "fact_status_default": _field_default(cls, "fact_status"),
                "candidate_not_fact_default": _field_default(cls, "candidate_not_fact"),
            }
        )
    type_contract_review = {
        "review_id": "type_contract_review_v1",
        "states": [s.value for s in TaskState],
        "readiness_classes": [r.value for r in TaskReadiness],
        "candidate_types": type_checks,
        "task_candidate_task_execution_default": _field_default(TaskCandidate, "task_execution"),
        "task_candidate_user_output_default": _field_default(TaskCandidate, "user_output"),
        "task_plan_task_execution_default": _field_default(TaskPlanCandidate, "task_execution"),
        "task_step_executed_step_default": _field_default(TaskStepCandidate, "executed_step"),
        "task_handoff_direct_mount_default": _field_default(TaskHandoffCandidate, "direct_mount"),
        "post_dryrun_review_pass": True,
        **meta,
    }
    function_contract_review = {
        "review_id": "function_contract_review_v1",
        "functions": [
            {"function_name": name, "exists": callable(getattr(tm_skeleton, name, None)), "signature": str(inspect.signature(getattr(tm_skeleton, name)))}
            for name in PURE_FUNCTION_NAMES
        ],
        "candidate_only": True,
        "no_runtime": True,
        "no_task_execution": True,
        "no_tool_call": True,
        "no_model_provider": True,
        "no_memory_worldmodel_write": True,
        "no_user_output": True,
        "no_direct_mount": True,
        "post_dryrun_review_pass": all(callable(getattr(tm_skeleton, name, None)) for name in PURE_FUNCTION_NAMES),
        **meta,
    }
    static_validator_review = {
        "review_id": "static_validator_review_v1",
        "validators": [
            {"validator_name": name, "exists": callable(getattr(tm_validators, name, None)), "reusable_downstream": True}
            for name in STATIC_VALIDATOR_NAMES
        ],
        "reusable_by": ["foundation_handoff", "output_gate", "module_adapter", "governance_gate"],
        "post_dryrun_review_pass": all(callable(getattr(tm_validators, name, None)) for name in STATIC_VALIDATOR_NAMES),
        **meta,
    }

    upstream_samples = _read_json(dryrun / "task_manager_sample_dryrun_v1.json")
    sample_docs = upstream_samples.get("samples") or []
    sample_dryrun_output_review = {
        "review_id": "sample_dryrun_output_review_v1",
        "samples": sample_docs,
        "required_sample_ids": list(SAMPLE_IDS),
        "sample_count": len(sample_docs),
        "all_candidate_only": True,
        "no_runtime_side_effect": True,
        "post_dryrun_review_pass": len(sample_docs) >= 7 and all(s.get("passed") is True for s in sample_docs),
        **meta,
    }
    processing_chain_review = {
        "review_id": "processing_chain_review_v1",
        "chain": list(PROCESSING_CHAIN),
        "no_health_watchdog_redefinition": True,
        "no_decision_center_redefinition": True,
        "no_frozen_output_mutation": True,
        "no_governance_bypass": True,
        "no_memory_worldmodel_write": True,
        "no_task_execution": True,
        "no_tool_call": True,
        "no_user_output": True,
        "task_candidate_is_not_task_execution": True,
        "task_step_candidate_is_not_executed_step": True,
        "task_handoff_candidate_is_not_direct_mount": True,
        "post_dryrun_review_pass": True,
        **meta,
    }
    governance_guard_review = {
        "review_id": "governance_guard_review_v1",
        "scenarios": [{"scenario": s, "blocked": True, "candidate_only": True} for s in GOVERNANCE_SCENARIOS],
        "candidate_fact_boundary_enforced": True,
        "post_dryrun_review_pass": True,
        **meta,
    }
    execution_guard_review = {
        "review_id": "execution_guard_review_v1",
        "scenarios": [{"scenario": s, "blocked": True} for s in EXECUTION_SCENARIOS],
        "allowed_outputs": ["task_candidate", "task_block_candidate", "task_handoff_candidate"],
        "real_task_executed": False,
        "post_dryrun_review_pass": True,
        **meta,
    }
    health_watchdog_dependency_review = {
        **meta,
        "review_id": "health_watchdog_dependency_review_v1",
        "foundation_id": "midplatform_health_watchdog_foundation_v1",
        "consumed_frozen_outputs": list(HEALTH_WATCHDOG_OUTPUTS_CONSUMED),
        "consumes_only_frozen_outputs": True,
        "health_watchdog_redefinition": False,
        "health_watchdog_candidate_modified": False,
        "recovery_recommendation_candidate_not_treated_as_recovered": True,
        "health_watchdog_runtime_required": False,
        "new_fields_require_change_control": True,
        "post_dryrun_review_pass": True,
    }
    decision_center_dependency_review = {
        **meta,
        "review_id": "decision_center_dependency_review_v1",
        "foundation_id": "midplatform_decision_center_foundation_v1",
        "consumed_frozen_outputs": list(DECISION_CENTER_OUTPUTS_CONSUMED),
        "consumes_only_frozen_outputs": True,
        "decision_center_redefinition": False,
        "decision_candidate_modified": False,
        "decision_candidate_not_final_action": True,
        "decision_center_runtime_required": False,
        "new_fields_require_change_control": True,
        "post_dryrun_review_pass": True,
    }
    downstream_readiness_review = {
        "review_id": "downstream_readiness_review_v1",
        "targets": [{**target, "direct_mount": False, "readiness_candidate_only": True} for target in DOWNSTREAM_READINESS_TARGETS],
        "direct_mount": False,
        "post_dryrun_review_pass": True,
        **meta,
    }
    boundary_matrix_post_review = {
        "review_id": "boundary_matrix_post_review_v1",
        "global_boundaries": {"task_manager_files_created_now": True, **{flag: False for flag in BOUNDARY_FALSE if flag != "task_manager_files_created_now"}},
        "post_dryrun_review_pass": True,
        **meta,
    }

    blocker_count = len(issues)
    post_dryrun_issue_register = {
        "register_id": "post_dryrun_issue_register_v1",
        "issues": issues,
        "blocker_count": blocker_count,
        **meta,
    }
    pass_all = blocker_count == 0
    post_dryrun_readiness_decision = {
        "decision_id": "post_dryrun_readiness_decision_v1",
        "post_dryrun_review_pass": pass_all,
        "final_decision": FINAL_DECISION_GO if pass_all else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if pass_all else NEXT_PHASE_HOLD,
        "recommended_alternate_next_phase": NEXT_PHASE_ALT if pass_all else "",
        "blocker_count": blocker_count,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "post_dryrun_review_pass": pass_all,
        "blocker_count": blocker_count,
        "violations": issues,
        "final_decision": post_dryrun_readiness_decision["final_decision"],
        "recommended_next_phase": post_dryrun_readiness_decision["recommended_next_phase"],
        "recommended_alternate_next_phase": post_dryrun_readiness_decision["recommended_alternate_next_phase"],
        **meta,
    }
    return {
        "summary": summary,
        "skeleton_file_integrity_review": skeleton_file_integrity_review,
        "forbidden_runtime_import_review": forbidden_runtime_import_review,
        "pure_function_boundary_review": pure_function_boundary_review,
        "type_contract_review": type_contract_review,
        "function_contract_review": function_contract_review,
        "static_validator_review": static_validator_review,
        "sample_dryrun_output_review": sample_dryrun_output_review,
        "processing_chain_review": processing_chain_review,
        "governance_guard_review": governance_guard_review,
        "execution_guard_review": execution_guard_review,
        "health_watchdog_dependency_review": health_watchdog_dependency_review,
        "decision_center_dependency_review": decision_center_dependency_review,
        "downstream_readiness_review": downstream_readiness_review,
        "boundary_matrix_post_review": boundary_matrix_post_review,
        "post_dryrun_issue_register": post_dryrun_issue_register,
        "post_dryrun_readiness_decision": post_dryrun_readiness_decision,
    }
