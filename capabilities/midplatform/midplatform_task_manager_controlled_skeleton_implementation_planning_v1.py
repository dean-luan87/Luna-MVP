# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Controlled Skeleton Implementation Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_task_manager_mount_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MOUNT_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_task_manager_mount_planning_v1 import SAMPLE_FLOWS, TASK_STATES

PHASE_ID = "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-Planning-v1-001"
SCOPE = "midplatform_task_manager_controlled_skeleton_implementation_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_controlled_skeleton_implementation_planning_v1"

FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING_READY_FOR_IMPLEMENTATION_DRYRUN"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_TASK_MANAGER_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-Issue-Review-v1-001"

UPSTREAM_MOUNT_DRYRUN_FILES: Tuple[str, ...] = (
    "mount_dryrun_readiness_decision_v1.json",
    "upstream_mount_contract_consumability_review_v1.json",
    "health_watchdog_frozen_dependency_review_v1.json",
    "decision_center_frozen_dependency_review_v1.json",
    "mount_contract_10_section_review_v1.json",
    "input_contract_dryrun_v1.json",
    "output_contract_dryrun_v1.json",
    "processing_model_dryrun_v1.json",
    "task_state_machine_dryrun_v1.json",
    "model_rule_algorithm_placement_review_v1.json",
    "governance_boundary_dryrun_v1.json",
    "downstream_handoff_matrix_review_v1.json",
    "sample_flow_dryrun_v1.json",
    "failure_route_dryrun_review_v1.json",
    "mount_health_metric_scope_review_v1.json",
    "boundary_matrix_review_v1.json",
    "non_claims_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

SKELETON_FILE_PLAN: Tuple[Dict[str, Any], ...] = (
    {
        "path": "capabilities/midplatform/core/task_manager_types_v1.py",
        "purpose": "TaskState, TaskReadiness enums and task candidate dataclasses",
        "create_in_this_phase": False,
    },
    {
        "path": "capabilities/midplatform/core/task_manager_skeleton_v1.py",
        "purpose": "pure function task candidate generators and validation chain",
        "create_in_this_phase": False,
    },
    {
        "path": "capabilities/midplatform/core/task_manager_static_validators_v1.py",
        "purpose": "static validators for candidate-only task boundaries",
        "create_in_this_phase": False,
    },
)

TASK_STATE_ENUM: Tuple[str, ...] = TASK_STATES
TASK_READINESS_ENUM: Tuple[str, ...] = ("ready", "not_ready", "blocked", "hold", "paused", "requires_observation")
REQUIRED_BASE_FIELDS: Tuple[str, ...] = ("candidate_id", "trace_ref", "fact_status")

HEALTH_WATCHDOG_OUTPUTS_CONSUMED: Tuple[str, ...] = (
    "HealthSignalCandidate",
    "DegradationCandidate",
    "RecoveryRecommendationCandidate",
    "RequiredObservationCandidate",
    "ModuleHealthReviewCandidate",
    "WatchdogHandoffCandidate",
)
DECISION_CENTER_OUTPUTS_CONSUMED: Tuple[str, ...] = (
    "DecisionCandidate",
    "DecisionReadinessCandidate",
    "DecisionBlockCandidate",
    "DecisionExplanationCandidate",
    "DownstreamDecisionHandoffCandidate",
)

CANDIDATE_TYPES: Tuple[Dict[str, Any], ...] = (
    {
        "type_name": "TaskCandidate",
        "fields": (
            "candidate_id",
            "source_decision_ref",
            "source_health_refs",
            "task_context_refs",
            "readiness",
            "task_state",
            "task_summary",
            "governance_ref",
            "health_gate_refs",
            "blocker_refs",
            "trace_ref",
            "fact_status",
            "task_execution",
            "user_output",
        ),
        "fact_status_default": "not_fact",
        "task_execution_default": False,
        "user_output_default": False,
    },
    {
        "type_name": "TaskReadinessCandidate",
        "fields": (
            "candidate_id",
            "task_candidate_ref",
            "readiness",
            "readiness_reason",
            "blocker_refs",
            "health_gate_refs",
            "required_observation_refs",
            "governance_pending",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "TaskBlockCandidate",
        "fields": (
            "candidate_id",
            "block_type",
            "block_reason",
            "blocked_refs",
            "forbidden_route",
            "hold_or_reobserve_candidate",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "TaskPlanCandidate",
        "fields": (
            "candidate_id",
            "task_candidate_ref",
            "plan_summary",
            "planned_step_refs",
            "dependency_refs",
            "blocker_refs",
            "trace_ref",
            "fact_status",
            "task_execution",
        ),
        "fact_status_default": "not_fact",
        "task_execution_default": False,
    },
    {
        "type_name": "TaskStepCandidate",
        "fields": (
            "candidate_id",
            "task_candidate_ref",
            "step_order",
            "step_summary",
            "required_capability_refs",
            "required_observation_refs",
            "blocker_refs",
            "trace_ref",
            "fact_status",
            "executed_step",
        ),
        "fact_status_default": "not_fact",
        "executed_step_default": False,
    },
    {
        "type_name": "TaskHandoffCandidate",
        "fields": (
            "candidate_id",
            "task_candidate_ref",
            "module_adapter_refs",
            "output_gate_refs",
            "worldmodel_memory_bridge_refs",
            "decision_center_refs",
            "health_watchdog_refs",
            "governance_refs",
            "handoff_allowed",
            "direct_mount",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
        "direct_mount_default": False,
    },
)

PURE_FUNCTIONS: Tuple[Dict[str, Any], ...] = (
    {
        "function_name": "validate_task_manager_input",
        "inputs": ["input_candidate", "guards"],
        "output": "validation_candidate",
        "checks": ["trace", "health_tag", "candidate_not_fact", "source_chain", "governance_requirement"],
    },
    {
        "function_name": "classify_task_readiness",
        "inputs": ["input_candidate", "health_refs", "decision_refs", "governance_ref"],
        "output": "TaskReadinessCandidate",
        "forbidden": ["real_task_runtime"],
    },
    {
        "function_name": "evaluate_health_gate_block_candidate",
        "inputs": ["input_candidate", "health_refs"],
        "output": "TaskBlockCandidate",
    },
    {
        "function_name": "evaluate_required_observation_candidate",
        "inputs": ["input_candidate", "observation_refs"],
        "output": "requires_observation / required_observation_handoff_candidate",
    },
    {
        "function_name": "evaluate_governance_task_candidate",
        "inputs": ["input_candidate", "governance_ref"],
        "output": "blocked / governance_pending",
    },
    {
        "function_name": "build_task_candidate",
        "inputs": ["input_candidate", "readiness_candidate", "governance_ref"],
        "output": "TaskCandidate",
        "task_execution": False,
        "user_output": False,
    },
    {
        "function_name": "build_task_plan_candidate",
        "inputs": ["task_candidate", "context"],
        "output": "TaskPlanCandidate",
        "task_execution": False,
    },
    {
        "function_name": "build_task_step_candidate",
        "inputs": ["task_candidate", "plan_candidate", "step_context"],
        "output": "TaskStepCandidate",
        "executed_step": False,
    },
    {
        "function_name": "build_task_handoff_candidate",
        "inputs": ["task_candidate", "readiness_candidate", "routes"],
        "output": "TaskHandoffCandidate",
        "direct_mount": False,
    },
    {
        "function_name": "validate_task_manager_candidate",
        "inputs": ["candidate_object"],
        "output": "ValidationResult",
        "checks": ["candidate_not_fact", "trace", "no_execution", "no_tool_call", "no_output", "no_write", "no_direct_mount"],
    },
)

STATIC_VALIDATORS: Tuple[str, ...] = (
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

GOVERNANCE_GUARD_RULES: Tuple[str, ...] = (
    "high-risk task without governance_ref must be blocked / governance_review / not_ready",
    "task_candidate is not task execution",
    "task_step_candidate is not executed step",
    "task_handoff_candidate is not direct mount",
    "do not bypass L0 Governance Gate",
)

EXECUTION_GUARD_RULES: Tuple[str, ...] = (
    "task_execution_attempted -> blocked",
    "tool_call_attempted -> blocked",
    "output_attempted -> blocked",
    "memory_write_attempted -> blocked",
    "worldmodel_write_attempted -> blocked",
    "direct_mount_attempted -> blocked",
    "only task_candidate / task_block_candidate / handoff_candidate may be generated",
)

HEALTH_WATCHDOG_DEPENDENCY_GUARD_RULES: Tuple[str, ...] = (
    "only consume Health Watchdog frozen outputs",
    "must not redefine Health Watchdog",
    "must not modify health/watchdog candidate",
    "must not treat hold / blocked / safety_block as executed task",
    "must not treat recovery_recommendation_candidate as recovered",
    "must not require Health Watchdog runtime",
    "new fields require change_control",
)

DECISION_CENTER_DEPENDENCY_GUARD_RULES: Tuple[str, ...] = (
    "only consume Decision Center frozen outputs",
    "must not redefine Decision Center",
    "must not modify DecisionCandidate",
    "must not treat decision_candidate as final action",
    "must not require Decision Center runtime",
    "new fields require change_control",
)

SAMPLE_PLAN: Tuple[Dict[str, Any], ...] = tuple(
    {
        "sample_id": flow["flow_id"],
        "description": f"Implementation DryRun sample for {flow['flow_id']}",
        "terminal": flow["output_candidate"],
    }
    for flow in SAMPLE_FLOWS
)

TEST_PLAN_CATEGORIES: Tuple[str, ...] = (
    "type_completeness",
    "candidate_not_fact",
    "no_task_execution",
    "no_tool_call",
    "no_user_output",
    "no_memory_worldmodel_write",
    "no_direct_mount",
    "governance_required_for_high_risk_task",
    "health_watchdog_frozen_dependency",
    "decision_center_frozen_dependency",
    "task_state_machine",
    "boundary_matrix",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "task_manager_files_created_now",
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
)

NON_CLAIMS: Tuple[str, ...] = (
    "Skeleton Planning ≠ skeleton implementation",
    "Skeleton Planning ≠ Task Manager mounted",
    "Skeleton Planning ≠ runtime enabled",
    "Skeleton Planning ≠ task execution",
    "Skeleton Planning ≠ tool call",
    "Skeleton Planning ≠ Output Gate ready",
    "Skeleton Planning ≠ user output",
    "Skeleton Planning ≠ Memory / WorldModel write",
    "Skeleton Planning ≠ full task pipeline",
)

DEFAULT_MOUNT_DRYRUN_ROOT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_task_manager_mount_dryrun_and_review"
DEFAULT_MOUNT_PLANNING_ROOT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_task_manager_mount_planning"
DEFAULT_HEALTH_WATCHDOG_HANDOFF_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_foundation_handoff_dryrun_and_review"
)
DEFAULT_DECISION_CENTER_HANDOFF_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_foundation_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_controlled_skeleton_implementation_planning"
)


def _meta(output_root: Path, mount_dryrun_root: Path, mount_planning_root: Path) -> Dict[str, Any]:
    meta: Dict[str, Any] = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "module_id": "task_manager",
        "layer": "L6_task_candidate_management",
        "foundation_id": "midplatform_health_watchdog_foundation_v1",
        "depends_on": "midplatform_health_watchdog_foundation_v1",
        "also_depends_on": [
            "midplatform_decision_center_foundation_v1",
            "midplatform_information_integration_foundation_v1",
            "midplatform_micro_os_foundation_v1",
        ],
        "runtime_status": "not_enabled",
        "task_manager_controlled_skeleton_implementation_planning_only": True,
        "skeleton_plan_only": True,
        "output_root": str(output_root),
        "upstream_mount_dryrun_root": str(mount_dryrun_root),
        "upstream_mount_planning_root": str(mount_planning_root),
        "must_not_redefine_health_watchdog": True,
        "must_not_redefine_decision_center": True,
    }
    for flag in BOUNDARY_FALSE:
        meta[flag] = False
    return meta


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def run_midplatform_task_manager_controlled_skeleton_implementation_planning_v1(
    *,
    task_manager_mount_dryrun_root: str,
    task_manager_mount_planning_root: str,
    health_watchdog_handoff_dryrun_root: str,
    decision_center_handoff_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    mount_dr = Path(task_manager_mount_dryrun_root).expanduser().resolve()
    mount_plan = Path(task_manager_mount_planning_root).expanduser().resolve()
    hw_root = Path(health_watchdog_handoff_dryrun_root).expanduser().resolve()
    dc_root = Path(decision_center_handoff_dryrun_root).expanduser().resolve()
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, mount_dr, mount_plan)
    blockers: List[str] = []

    mount_summary = _read_json(mount_dr / "summary.json")
    mount_verifier = _read_json(mount_dr / "verifier_report.json")
    if mount_summary.get("final_decision") != "MIDPLATFORM_TASK_MANAGER_MOUNT_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING":
        blockers.append("task_manager_mount_dryrun_final_decision_not_go")
    if mount_verifier.get("verifier") != "GO":
        blockers.append("task_manager_mount_dryrun_verifier_not_go")
    for fname in UPSTREAM_MOUNT_DRYRUN_FILES:
        if not (mount_dr / fname).is_file():
            blockers.append(f"missing_mount_dryrun_artifact:{fname}")
    if _read_json(hw_root / "summary.json").get("foundation_id") != "midplatform_health_watchdog_foundation_v1":
        blockers.append("health_watchdog_foundation_id_mismatch")
    if _read_json(dc_root / "summary.json").get("foundation_id") != "midplatform_decision_center_foundation_v1":
        blockers.append("decision_center_foundation_id_mismatch")
    if any((repo_root / item["path"]).is_file() for item in SKELETON_FILE_PLAN):
        blockers.append("task_manager_skeleton_files_must_not_exist_in_planning_phase")

    scope = {
        "object_id": "task_manager_skeleton_scope_v1",
        "allowed": ["enum", "dataclass", "pure_function", "static_validator", "candidate_generator"],
        "forbidden": [
            "real_task_manager_runtime",
            "task_execution",
            "tool_call",
            "model_provider_invocation",
            "memory_worldmodel_write",
            "user_output",
            "direct_mount",
        ],
        "consumes_health_watchdog_frozen_outputs": list(HEALTH_WATCHDOG_OUTPUTS_CONSUMED),
        "consumes_decision_center_frozen_outputs": list(DECISION_CENTER_OUTPUTS_CONSUMED),
        **meta,
    }
    file_plan = {
        "object_id": "task_manager_skeleton_file_plan_v1",
        "files": list(SKELETON_FILE_PLAN),
        "file_count": len(SKELETON_FILE_PLAN),
        "create_in_this_phase": False,
        "task_manager_files_created_now": False,
        **{k: v for k, v in meta.items() if k != "task_manager_files_created_now"},
    }
    type_contract = {
        "object_id": "task_manager_type_contract_v1",
        "enums": {"TaskState": list(TASK_STATE_ENUM), "TaskReadiness": list(TASK_READINESS_ENUM)},
        "candidate_types": list(CANDIDATE_TYPES),
        "type_count": len(CANDIDATE_TYPES),
        "required_base_fields": list(REQUIRED_BASE_FIELDS),
        "all_fact_status_not_fact": True,
        **meta,
    }
    function_contract = {
        "object_id": "task_manager_function_contract_v1",
        "functions": list(PURE_FUNCTIONS),
        "function_count": len(PURE_FUNCTIONS),
        "candidate_only": True,
        **meta,
    }
    validator_contract = {
        "object_id": "task_manager_static_validator_contract_v1",
        "validators": list(STATIC_VALIDATORS),
        "validator_count": len(STATIC_VALIDATORS),
        **meta,
    }
    processing_chain = {
        "object_id": "task_manager_processing_chain_contract_v1",
        "chain": list(PROCESSING_CHAIN),
        "candidate_only": True,
        **meta,
    }
    governance_guard = {
        "object_id": "task_manager_governance_guard_plan_v1",
        "rules": list(GOVERNANCE_GUARD_RULES),
        **meta,
    }
    execution_guard = {
        "object_id": "task_manager_execution_guard_plan_v1",
        "rules": list(EXECUTION_GUARD_RULES),
        **meta,
    }
    hw_guard = {
        "object_id": "task_manager_health_watchdog_dependency_guard_plan_v1",
        "rules": list(HEALTH_WATCHDOG_DEPENDENCY_GUARD_RULES),
        **meta,
    }
    dc_guard = {
        "object_id": "task_manager_decision_center_dependency_guard_plan_v1",
        "rules": list(DECISION_CENTER_DEPENDENCY_GUARD_RULES),
        **meta,
    }
    sample_plan = {
        "object_id": "task_manager_sample_plan_v1",
        "samples": list(SAMPLE_PLAN),
        "sample_count": len(SAMPLE_PLAN),
        **meta,
    }
    test_plan = {
        "object_id": "task_manager_test_plan_v1",
        "categories": list(TEST_PLAN_CATEGORIES),
        "category_count": len(TEST_PLAN_CATEGORIES),
        "execution_phase": "Implementation DryRun",
        **meta,
    }
    boundary_matrix = {
        "object_id": "task_manager_skeleton_boundary_matrix_v1",
        "global_boundaries": {flag: False for flag in BOUNDARY_FALSE},
        **meta,
    }
    non_claims = {
        "object_id": "task_manager_skeleton_non_claims_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }
    planning_pass = len(blockers) == 0
    readiness = {
        "object_id": "task_manager_skeleton_planning_readiness_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "blocker_count": len(blockers),
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "blocker_count": len(blockers),
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        **meta,
    }
    return {
        "summary": summary,
        "task_manager_skeleton_scope": scope,
        "task_manager_skeleton_file_plan": file_plan,
        "task_manager_type_contract": type_contract,
        "task_manager_function_contract": function_contract,
        "task_manager_static_validator_contract": validator_contract,
        "task_manager_processing_chain_contract": processing_chain,
        "task_manager_governance_guard_plan": governance_guard,
        "task_manager_execution_guard_plan": execution_guard,
        "task_manager_health_watchdog_dependency_guard_plan": hw_guard,
        "task_manager_decision_center_dependency_guard_plan": dc_guard,
        "task_manager_sample_plan": sample_plan,
        "task_manager_test_plan": test_plan,
        "task_manager_skeleton_boundary_matrix": boundary_matrix,
        "task_manager_skeleton_non_claims": non_claims,
        "task_manager_skeleton_planning_readiness_decision": readiness,
    }
