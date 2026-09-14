# -*- coding: utf-8 -*-
"""Luna Midplatform Health Watchdog Controlled Skeleton Implementation Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_health_watchdog_mount_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MOUNT_DRYRUN_FINAL_GO,
    HEALTH_STATES,
    SAMPLE_FLOWS,
)

PHASE_ID = "Phase-Midplatform-Health-Watchdog-Controlled-Skeleton-Implementation-Planning-v1-001"
SCOPE = "midplatform_health_watchdog_controlled_skeleton_implementation_planning_only"
SOURCE_CHAIN = "midplatform_health_watchdog_controlled_skeleton_implementation_planning_v1"

UPSTREAM_MOUNT_DRYRUN_FINAL = MOUNT_DRYRUN_FINAL_GO

FINAL_DECISION_GO = (
    "MIDPLATFORM_HEALTH_WATCHDOG_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING_"
    "READY_FOR_IMPLEMENTATION_DRYRUN"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_HEALTH_WATCHDOG_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Health-Watchdog-Controlled-Skeleton-Implementation-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Health-Watchdog-Controlled-Skeleton-Issue-Review-v1-001"

UPSTREAM_MOUNT_DRYRUN_FILES: Tuple[str, ...] = (
    "mount_dryrun_readiness_decision_v1.json",
    "upstream_mount_contract_consumability_review_v1.json",
    "decision_center_frozen_dependency_review_v1.json",
    "mount_contract_10_section_review_v1.json",
    "input_contract_dryrun_v1.json",
    "output_contract_dryrun_v1.json",
    "processing_model_dryrun_v1.json",
    "health_state_machine_dryrun_v1.json",
    "model_rule_algorithm_placement_review_v1.json",
    "governance_boundary_dryrun_v1.json",
    "recovery_boundary_dryrun_v1.json",
    "downstream_handoff_matrix_review_v1.json",
    "sample_flow_dryrun_v1.json",
    "failure_route_dryrun_review_v1.json",
    "mount_health_metric_scope_review_v1.json",
    "boundary_matrix_review_v1.json",
    "non_claims_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

UPSTREAM_DECISION_CENTER_HANDOFF_FILES: Tuple[str, ...] = (
    "summary.json",
    "handoff_dryrun_readiness_decision_v1.json",
    "verifier_report.json",
)

UPSTREAM_DECISION_CENTER_PLANNING_FILES: Tuple[str, ...] = (
    "decision_center_foundation_version_tag_v1.json",
    "decision_center_frozen_type_interface_v1.json",
    "decision_center_handoff_contract_v1.json",
)

DECISION_CENTER_FROZEN_OUTPUTS_CONSUMED: Tuple[str, ...] = (
    "DecisionCandidate",
    "DecisionReadinessCandidate",
    "DecisionBlockCandidate",
    "DecisionExplanationCandidate",
    "DownstreamDecisionHandoffCandidate",
)

SKELETON_FILE_PLAN: Tuple[Dict[str, Any], ...] = (
    {
        "path": "capabilities/midplatform/core/health_watchdog_types_v1.py",
        "purpose": "HealthWatchdogState, HealthSeverity enums and 6 health/watchdog candidate dataclasses",
        "create_in_this_phase": False,
    },
    {
        "path": "capabilities/midplatform/core/health_watchdog_skeleton_v1.py",
        "purpose": "pure function candidate generators for validation, health classification, degradation, recovery recommendation, handoff",
        "create_in_this_phase": False,
    },
    {
        "path": "capabilities/midplatform/core/health_watchdog_static_validators_v1.py",
        "purpose": "static validators for input/output/recovery/restart/process/write/governance/Decision Center dependency",
        "create_in_this_phase": False,
    },
)

HEALTH_WATCHDOG_STATE_ENUM: Tuple[str, ...] = HEALTH_STATES

HEALTH_SEVERITY_ENUM: Tuple[str, ...] = ("info", "low", "medium", "high", "critical")

REQUIRED_CANDIDATE_BASE_FIELDS: Tuple[str, ...] = ("candidate_id", "trace_ref", "fact_status")

CANDIDATE_TYPES: Tuple[Dict[str, Any], ...] = (
    {
        "type_name": "HealthSignalCandidate",
        "fields": (
            "candidate_id",
            "source_decision_ref",
            "signal_type",
            "severity",
            "health_refs",
            "stale_refs",
            "low_confidence_refs",
            "p0_safety_refs",
            "governance_refs",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "DegradationCandidate",
        "fields": (
            "candidate_id",
            "degradation_type",
            "degradation_level",
            "affected_module_refs",
            "reason",
            "recommended_hold",
            "real_degradation",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
        "real_degradation_default": False,
    },
    {
        "type_name": "RecoveryRecommendationCandidate",
        "fields": (
            "candidate_id",
            "recommendation_type",
            "recommendation_reason",
            "affected_module_refs",
            "governance_required",
            "governance_ref",
            "recovery_execution",
            "restart_allowed",
            "process_control_allowed",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
        "recovery_execution_default": False,
        "restart_allowed_default": False,
        "process_control_allowed_default": False,
    },
    {
        "type_name": "RequiredObservationCandidate",
        "fields": (
            "candidate_id",
            "observation_reason",
            "target_refs",
            "urgency",
            "source_health_signal_ref",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "ModuleHealthReviewCandidate",
        "fields": (
            "candidate_id",
            "module_ref",
            "issue_type",
            "severity",
            "evidence_refs",
            "recommended_status",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "WatchdogHandoffCandidate",
        "fields": (
            "candidate_id",
            "source_candidate_refs",
            "module_adapter_refs",
            "task_manager_refs",
            "decision_center_refs",
            "governance_refs",
            "output_gate_refs",
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
        "function_name": "validate_health_watchdog_input",
        "inputs": ["input_candidate", "guards"],
        "output": "validation_candidate",
        "checks": ["trace", "health_tag", "candidate_not_fact", "source_chain", "governance_requirement"],
        "forbidden": ["runtime_execution", "recovery_execution"],
    },
    {
        "function_name": "classify_health_signal",
        "inputs": ["input_candidate", "severity_rules"],
        "output": "HealthSignalCandidate",
        "forbidden": ["real_health_runtime"],
    },
    {
        "function_name": "evaluate_stale_context_candidate",
        "inputs": ["input_candidate"],
        "output": "RequiredObservationCandidate / hold",
        "condition": "stale_context",
    },
    {
        "function_name": "evaluate_low_confidence_candidate",
        "inputs": ["input_candidate"],
        "output": "hold / required_observation",
        "condition": "low_confidence",
    },
    {
        "function_name": "evaluate_p0_safety_candidate",
        "inputs": ["input_candidate"],
        "output": "safety_block / hold candidate",
        "condition": "p0_safety_unresolved",
    },
    {
        "function_name": "evaluate_degradation_candidate",
        "inputs": ["health_signal", "context"],
        "output": "DegradationCandidate",
        "real_degradation": False,
    },
    {
        "function_name": "build_recovery_recommendation_candidate",
        "inputs": ["health_signal", "degradation", "governance_ref"],
        "output": "RecoveryRecommendationCandidate",
        "recovery_execution": False,
        "restart_allowed": False,
        "process_control_allowed": False,
    },
    {
        "function_name": "build_module_health_review_candidate",
        "inputs": ["health_signal", "module_ref"],
        "output": "ModuleHealthReviewCandidate",
    },
    {
        "function_name": "build_watchdog_handoff_candidate",
        "inputs": ["health_signal", "degradation", "recovery_recommendation", "routes"],
        "output": "WatchdogHandoffCandidate",
        "direct_mount": False,
    },
    {
        "function_name": "validate_health_watchdog_candidate",
        "inputs": ["candidate_object"],
        "output": "ValidationResult",
        "checks": ["candidate_not_fact", "trace", "no_recovery", "no_restart", "no_process_control", "no_output", "no_write"],
    },
)

STATIC_VALIDATORS: Tuple[str, ...] = (
    "validate_hw_input_contract",
    "validate_hw_output_candidate_only",
    "validate_hw_no_recovery_execution",
    "validate_hw_no_restart",
    "validate_hw_no_process_control",
    "validate_hw_no_task_execution",
    "validate_hw_no_user_output",
    "validate_hw_no_memory_worldmodel_write",
    "validate_hw_governance_required_for_high_risk_recovery",
    "validate_hw_no_decision_center_redefinition",
    "validate_hw_boundary_matrix",
)

PROCESSING_CHAIN: Tuple[str, ...] = (
    "validate_health_watchdog_input",
    "classify_health_signal",
    "evaluate_stale_context_candidate",
    "evaluate_low_confidence_candidate",
    "evaluate_p0_safety_candidate",
    "evaluate_degradation_candidate",
    "build_recovery_recommendation_candidate",
    "build_module_health_review_candidate",
    "build_watchdog_handoff_candidate",
)

GOVERNANCE_GUARD_RULES: Tuple[str, ...] = (
    "high-risk recovery recommendation without governance_ref must be blocked / governance_review / not_ready",
    "recovery_recommendation_candidate is not recovery execution",
    "degradation_candidate is not real degradation",
    "watchdog_handoff_candidate is not direct mount",
    "do not bypass L0 Governance Gate",
)

RECOVERY_GUARD_RULES: Tuple[str, ...] = (
    "recovery_execution_attempted -> blocked",
    "module_restart_attempted -> blocked",
    "process_control_attempted -> blocked",
    "permission_release_attempted -> blocked",
    "module_reload_attempted -> blocked",
    "system_command_attempted -> blocked",
    "emergency_output_attempted -> blocked",
    "only recovery_recommendation_candidate may be generated",
)

DECISION_CENTER_DEPENDENCY_GUARD_RULES: Tuple[str, ...] = (
    "only consume Decision Center frozen outputs",
    "must not redefine Decision Center",
    "must not modify DecisionCandidate",
    "must not treat blocked/hold as real system state",
    "must not require Decision Center runtime",
    "new fields require change_control",
)

SKELETON_SAMPLES: Tuple[Dict[str, Any], ...] = tuple(
    {
        "sample_id": flow["flow_id"],
        "description": f"DryRun sample for {flow['flow_id']}",
        "terminal": flow.get("outputs", ["health_signal_candidate"])[0],
    }
    for flow in SAMPLE_FLOWS
)

TEST_PLAN_CATEGORIES: Tuple[str, ...] = (
    "type_completeness",
    "candidate_not_fact",
    "no_real_recovery",
    "no_restart",
    "no_process_control",
    "no_task_execution",
    "no_user_output",
    "no_memory_worldmodel_write",
    "governance_required_for_high_risk_recovery",
    "decision_center_frozen_dependency",
    "health_state_machine",
    "boundary_matrix",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Skeleton Planning ≠ skeleton implementation",
    "Skeleton Planning ≠ Health Watchdog mounted",
    "Skeleton Planning ≠ runtime enabled",
    "Skeleton Planning ≠ recovery execution",
    "Skeleton Planning ≠ restart",
    "Skeleton Planning ≠ process control",
    "Skeleton Planning ≠ task execution",
    "Skeleton Planning ≠ Output Gate ready",
    "Skeleton Planning ≠ user output",
    "Skeleton Planning ≠ Memory / WorldModel write",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_health_watchdog_controlled_skeleton_implementation_planning_only",
    "skeleton_plan_only",
    "health_watchdog_files_not_created_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "health_watchdog_files_created_now",
    "health_watchdog_runtime_enabled_now",
    "health_watchdog_mounted_now",
    "recovery_execution_now",
    "module_restart_now",
    "process_control_now",
    "model_invoked_now",
    "provider_invoked_now",
    "runtime_enabled_now",
    "task_execution_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "output_gate_mounted_now",
    "task_manager_mounted_now",
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
)

DEFAULT_MOUNT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_mount_dryrun_and_review"
)
DEFAULT_MOUNT_PLANNING_ROOT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_mount_planning"
DEFAULT_DECISION_CENTER_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_foundation_handoff_dryrun_and_review"
)
DEFAULT_INFORMATION_INTEGRATION_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_MICRO_OS_FREEZE_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_health_watchdog_controlled_skeleton_implementation_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "foundation_id": "midplatform_decision_center_foundation_v1",
        "depends_on": "midplatform_decision_center_foundation_v1",
        "also_depends_on": [
            "midplatform_information_integration_foundation_v1",
            "midplatform_micro_os_foundation_v1",
        ],
        "runtime_status": "not_enabled",
        "decision_center_foundation_reuse_confirmed": True,
        "must_not_redefine_decision_center": True,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_midplatform_health_watchdog_controlled_skeleton_implementation_planning_v1(
    *,
    midplatform_health_watchdog_mount_dryrun_and_review_root: str,
    midplatform_health_watchdog_mount_planning_root: str,
    midplatform_decision_center_foundation_handoff_dryrun_and_review_root: str,
    midplatform_information_integration_foundation_handoff_dryrun_and_review_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    mount_dr = Path(midplatform_health_watchdog_mount_dryrun_and_review_root).expanduser().resolve()
    mount_plan = Path(midplatform_health_watchdog_mount_planning_root).expanduser().resolve()
    dc_handoff_dr = Path(midplatform_decision_center_foundation_handoff_dryrun_and_review_root).expanduser().resolve()
    ii_handoff_dr = Path(midplatform_information_integration_foundation_handoff_dryrun_and_review_root).expanduser().resolve()
    micro_os_dr = Path(midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = {
        **_planning_meta(),
        "output_root": str(out_root),
        "upstream_mount_dryrun_root": str(mount_dr),
        "upstream_mount_planning_root": str(mount_plan),
        "upstream_decision_center_handoff_dryrun_root": str(dc_handoff_dr),
        "upstream_information_integration_handoff_dryrun_root": str(ii_handoff_dr),
        "upstream_micro_os_freeze_dryrun_root": str(micro_os_dr),
    }

    mount_vr = _try_read_json(mount_dr / "verifier_report.json") or {}
    mount_sm = _try_read_json(mount_dr / "summary.json") or {}
    mount_ready = _try_read_json(mount_dr / "mount_dryrun_readiness_decision_v1.json") or {}
    if mount_vr.get("verifier") != "GO":
        blockers.append("upstream Health Watchdog mount dryrun verifier must be GO")
    if mount_sm.get("final_decision") != UPSTREAM_MOUNT_DRYRUN_FINAL:
        blockers.append("upstream Health Watchdog mount dryrun final_decision mismatch")
    if mount_ready.get("dryrun_pass") is not True:
        blockers.append("upstream Health Watchdog mount dryrun readiness must pass")

    dc_vr = _try_read_json(dc_handoff_dr / "verifier_report.json") or {}
    dc_sm = _try_read_json(dc_handoff_dr / "summary.json") or {}
    if dc_vr.get("verifier") != "GO":
        blockers.append("Decision Center foundation handoff verifier must be GO")
    if dc_sm.get("foundation_id") != "midplatform_decision_center_foundation_v1":
        blockers.append("Decision Center foundation_id mismatch")
    if dc_sm.get("runtime_status") != "not_enabled":
        blockers.append("Decision Center runtime_status must be not_enabled")

    if (_try_read_json(ii_handoff_dr / "summary.json") or {}).get("foundation_id") != "midplatform_information_integration_foundation_v1":
        blockers.append("Information Integration foundation mismatch")
    if (_try_read_json(micro_os_dr / "summary.json") or {}).get("foundation_id") != "midplatform_micro_os_foundation_v1":
        blockers.append("Micro-OS foundation mismatch")

    upstream_mount: Dict[str, Any] = {}
    for fname in UPSTREAM_MOUNT_DRYRUN_FILES:
        data = _try_read_json(mount_dr / fname)
        if data is None:
            blockers.append(f"missing mount dryrun upstream: {fname}")
        upstream_mount[fname.replace("_v1.json", "").replace(".json", "")] = data

    dc_version = _try_read_json(dc_handoff_dr / "foundation_version_tag_review_v1.json") or {}
    dc_type_interface = _try_read_json(dc_handoff_dr / "frozen_type_interface_review_v1.json") or {}
    dc_handoff_contract = _try_read_json(dc_handoff_dr / "handoff_contract_dryrun_v1.json") or {}
    dc_dep = upstream_mount.get("decision_center_frozen_dependency_review") or {}
    if dc_dep.get("decision_center_redefinition_required") is True:
        blockers.append("Decision Center redefinition must not be required")
    if dc_type_interface.get("dryrun_and_review_pass") is not True:
        blockers.append("Decision Center frozen type interface review must match")
    if dc_handoff_contract.get("dryrun_and_review_pass") is not True:
        blockers.append("Decision Center handoff contract review must match")

    hw_files_exist = any((repo_root / f["path"]).is_file() for f in SKELETON_FILE_PLAN)
    if hw_files_exist:
        blockers.append("Health Watchdog skeleton files must not exist in planning phase")

    skeleton_scope = {
        "scope_id": "health_watchdog_skeleton_scope_v1",
        "module_id": "health_watchdog",
        "allowed": ["enum", "dataclass", "pure_function", "static_validator", "candidate_generator"],
        "forbidden": [
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
        ],
        "reuse_decision_center_frozen_outputs": list(DECISION_CENTER_FROZEN_OUTPUTS_CONSUMED),
        "upstream_decision_center_artifacts_consumed": [
            "decision_center_foundation_version_tag_v1",
            "decision_center_frozen_type_interface_v1",
            "decision_center_handoff_contract_v1",
        ],
        **meta,
    }

    skeleton_file_plan = {
        "plan_id": "health_watchdog_skeleton_file_plan_v1",
        "files": list(SKELETON_FILE_PLAN),
        "file_count": len(SKELETON_FILE_PLAN),
        "create_in_this_phase": False,
        "health_watchdog_files_created_now": False,
        **meta,
    }

    type_contract = {
        "contract_id": "health_watchdog_type_contract_v1",
        "enums": {
            "HealthWatchdogState": list(HEALTH_WATCHDOG_STATE_ENUM),
            "HealthSeverity": list(HEALTH_SEVERITY_ENUM),
        },
        "candidate_types": list(CANDIDATE_TYPES),
        "type_count": len(CANDIDATE_TYPES),
        "required_base_fields": list(REQUIRED_CANDIDATE_BASE_FIELDS),
        "all_fact_status_not_fact": True,
        **meta,
    }

    function_contract = {
        "contract_id": "health_watchdog_function_contract_v1",
        "functions": list(PURE_FUNCTIONS),
        "function_count": len(PURE_FUNCTIONS),
        "reuse_decision_center_types": list(DECISION_CENTER_FROZEN_OUTPUTS_CONSUMED),
        "candidate_only_outputs": True,
        **meta,
    }

    static_validator_contract = {
        "contract_id": "health_watchdog_static_validator_contract_v1",
        "validators": list(STATIC_VALIDATORS),
        "validator_count": len(STATIC_VALIDATORS),
        **meta,
    }

    processing_chain_contract = {
        "contract_id": "health_watchdog_processing_chain_contract_v1",
        "chain": list(PROCESSING_CHAIN),
        "chain_count": len(PROCESSING_CHAIN),
        "candidate_only": True,
        **meta,
    }

    governance_guard_plan = {
        "plan_id": "health_watchdog_governance_guard_plan_v1",
        "rules": list(GOVERNANCE_GUARD_RULES),
        "rule_count": len(GOVERNANCE_GUARD_RULES),
        **meta,
    }

    recovery_guard_plan = {
        "plan_id": "health_watchdog_recovery_guard_plan_v1",
        "rules": list(RECOVERY_GUARD_RULES),
        "rule_count": len(RECOVERY_GUARD_RULES),
        **meta,
    }

    decision_center_dependency_guard_plan = {
        "plan_id": "health_watchdog_decision_center_dependency_guard_plan_v1",
        "rules": list(DECISION_CENTER_DEPENDENCY_GUARD_RULES),
        "rule_count": len(DECISION_CENTER_DEPENDENCY_GUARD_RULES),
        **meta,
    }

    sample_plan = {
        "plan_id": "health_watchdog_sample_plan_v1",
        "samples": list(SKELETON_SAMPLES),
        "sample_count": len(SKELETON_SAMPLES),
        **meta,
    }

    test_plan = {
        "plan_id": "health_watchdog_test_plan_v1",
        "categories": list(TEST_PLAN_CATEGORIES),
        "category_count": len(TEST_PLAN_CATEGORIES),
        "execution_phase": "Implementation DryRun",
        "tests": [{"test_id": f"test_{cat}", "category": cat} for cat in TEST_PLAN_CATEGORIES],
        **meta,
    }

    skeleton_boundary_matrix = {
        "matrix_id": "health_watchdog_skeleton_boundary_matrix_v1",
        "global_boundaries": {f: False for f in BOUNDARY_FALSE},
        **meta,
    }

    skeleton_non_claims = {
        "register_id": "health_watchdog_skeleton_non_claims_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    planning_pass = len(blockers) == 0
    readiness = {
        "decision_id": "health_watchdog_skeleton_planning_readiness_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "skeleton_scope_defined": True,
        "file_plan_defined": True,
        "health_watchdog_files_created_now": False,
        "decision_center_foundation_reuse_confirmed": True,
        "must_not_redefine_decision_center": True,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "non_claims": list(NON_CLAIMS),
        "module_id": "health_watchdog",
        "layer": "L5_health",
        "decision_center_foundation_version_reviewed": dc_version.get("dryrun_and_review_pass") is True,
        "decision_center_frozen_type_interface_reviewed": dc_type_interface.get("dryrun_and_review_pass") is True,
        "decision_center_handoff_contract_reviewed": dc_handoff_contract.get("dryrun_and_review_pass") is True,
        **meta,
    }

    return {
        "summary": summary,
        "health_watchdog_skeleton_scope": skeleton_scope,
        "health_watchdog_skeleton_file_plan": skeleton_file_plan,
        "health_watchdog_type_contract": type_contract,
        "health_watchdog_function_contract": function_contract,
        "health_watchdog_static_validator_contract": static_validator_contract,
        "health_watchdog_processing_chain_contract": processing_chain_contract,
        "health_watchdog_governance_guard_plan": governance_guard_plan,
        "health_watchdog_recovery_guard_plan": recovery_guard_plan,
        "health_watchdog_decision_center_dependency_guard_plan": decision_center_dependency_guard_plan,
        "health_watchdog_sample_plan": sample_plan,
        "health_watchdog_test_plan": test_plan,
        "health_watchdog_skeleton_boundary_matrix": skeleton_boundary_matrix,
        "health_watchdog_skeleton_non_claims": skeleton_non_claims,
        "health_watchdog_skeleton_planning_readiness_decision": readiness,
    }
