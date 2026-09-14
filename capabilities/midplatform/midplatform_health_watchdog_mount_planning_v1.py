# -*- coding: utf-8 -*-
"""Luna Midplatform Health Watchdog Mount Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_module_definition_template_v1 import TEMPLATE_SECTIONS
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_decision_center_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DECISION_CENTER_HANDOFF_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as DECISION_CENTER_HANDOFF_DRYRUN_NEXT,
)

PHASE_ID = "Phase-Midplatform-Health-Watchdog-Mount-Planning-v1-001"
SCOPE = "midplatform_health_watchdog_mount_planning_only"
SOURCE_CHAIN = "midplatform_health_watchdog_mount_planning_v1"

UPSTREAM_DECISION_CENTER_HANDOFF_DRYRUN_FINAL = DECISION_CENTER_HANDOFF_DRYRUN_FINAL_GO
UPSTREAM_DECISION_CENTER_HANDOFF_DRYRUN_NEXT = DECISION_CENTER_HANDOFF_DRYRUN_NEXT

FINAL_DECISION_GO = "MIDPLATFORM_HEALTH_WATCHDOG_MOUNT_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_HEALTH_WATCHDOG_MOUNT_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Health-Watchdog-Mount-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Health-WatchDOG-Mount-Issue-Review-v1-001"

UPSTREAM_DECISION_CENTER_HANDOFF_DRYRUN_FILES: Tuple[str, ...] = (
    "handoff_dryrun_readiness_decision_v1.json",
    "foundation_version_tag_review_v1.json",
    "frozen_type_interface_review_v1.json",
    "frozen_function_interface_review_v1.json",
    "frozen_validator_interface_review_v1.json",
    "handoff_contract_dryrun_v1.json",
    "downstream_output_contract_review_v1.json",
    "forbidden_mutation_policy_review_v1.json",
    "change_control_policy_review_v1.json",
    "boundary_freeze_review_v1.json",
    "downstream_readiness_matrix_review_v1.json",
    "route_decision_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

UPSTREAM_DECISION_CENTER_HANDOFF_PLANNING_FILES: Tuple[str, ...] = (
    "decision_center_foundation_version_tag_v1.json",
    "decision_center_frozen_type_interface_v1.json",
    "decision_center_frozen_function_interface_v1.json",
    "decision_center_frozen_validator_interface_v1.json",
    "decision_center_handoff_contract_v1.json",
    "decision_center_downstream_output_contract_v1.json",
    "decision_center_forbidden_mutation_policy_v1.json",
    "decision_center_change_control_policy_v1.json",
    "decision_center_boundary_freeze_v1.json",
    "decision_center_downstream_readiness_matrix_v1.json",
    "decision_center_route_decision_v1.json",
)

UPSTREAM_INFORMATION_INTEGRATION_FILES: Tuple[str, ...] = (
    "summary.json",
    "handoff_dryrun_readiness_decision_v1.json",
    "verifier_report.json",
)

UPSTREAM_MICRO_OS_FILES: Tuple[str, ...] = (
    "summary.json",
    "freeze_dryrun_readiness_decision_v1.json",
    "verifier_report.json",
)

DECISION_CENTER_OUTPUTS_CONSUMED: Tuple[str, ...] = (
    "health_review_candidate",
    "blocked_refs",
    "hold_refs",
    "needs_health_review",
    "safety_refs",
    "stale_context_refs",
    "low_confidence_refs",
    "p0_safety_unresolved_refs",
    "health_fault_refs",
    "governance_pending_refs",
)

INPUT_TYPES: Tuple[str, ...] = (
    "decision_candidate_refs",
    "decision_readiness_candidate_refs",
    "decision_block_candidate_refs",
    "downstream_decision_handoff_candidate_refs",
    "health_review_candidate_refs",
    "blocked_refs",
    "hold_refs",
    "stale_context_refs",
    "low_confidence_refs",
    "p0_safety_unresolved_refs",
    "governance_pending_refs",
    "trace_ref",
    "health_tag",
    "source_chain",
)

INPUT_REQUIRED_FIELDS: Tuple[str, ...] = (
    "candidate_not_fact",
    "trace",
    "health_tag",
    "source_chain",
    "governance_ref_for_high_risk_recovery_recommendation",
)

OUTPUT_CANDIDATES: Tuple[str, ...] = (
    "health_signal_candidate",
    "degradation_candidate",
    "recovery_recommendation_candidate",
    "required_observation_candidate",
    "module_health_review_candidate",
    "watchdog_handoff_candidate",
    "hold_candidate",
    "safety_block_candidate",
    "governance_review_candidate",
)

FORBIDDEN_OUTPUTS: Tuple[str, ...] = (
    "real_recovery_command",
    "restart_command",
    "kill_process_command",
    "runtime_command",
    "user_output",
    "fact",
    "memory_write",
    "worldmodel_write",
)

PROCESSING_STEPS: Tuple[str, ...] = (
    "consume Decision Center health / block / hold refs",
    "validate trace / health_tag / candidate_not_fact",
    "inspect severity",
    "inspect P0/P1 priority",
    "inspect stale / missing / low confidence",
    "inspect governance pending",
    "classify health state",
    "generate health/degradation/recovery recommendation candidate",
    "generate downstream handoff candidate",
)

HEALTH_STATES: Tuple[str, ...] = (
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

MODEL_USES: Tuple[str, ...] = (
    "health_explanation_summary",
    "multi_signal_anomaly_explanation",
    "recovery_recommendation_explanation_draft",
)

RULE_USES: Tuple[str, ...] = (
    "no_real_recovery",
    "no_restart",
    "no_process_control",
    "candidate_fact_boundary",
    "high_risk_recovery_requires_governance",
    "p0_safety_conservative_handling",
    "unresolved_health_blocks_output_task_readiness",
    "output_write_runtime_forbidden",
)

ALGORITHM_USES: Tuple[str, ...] = (
    "severity_scoring",
    "stale_ranking",
    "confidence_threshold_classification",
    "degradation_level_classification",
    "recovery_recommendation_ranking",
)

RESPONSIBILITIES: Tuple[str, ...] = (
    "consume Decision Center health / blocked / hold / safety refs",
    "check health signal completeness",
    "identify stale context",
    "identify missing health",
    "identify low confidence",
    "identify P0 safety unresolved",
    "generate health_signal_candidate",
    "generate degradation_candidate",
    "generate recovery_recommendation_candidate",
    "generate required_observation_candidate",
    "generate module_health_review_candidate",
    "generate watchdog_handoff_candidate",
    "no recovery execution",
    "no module restart",
    "no task execution",
    "no user output",
    "no Memory / WorldModel write",
    "no model/provider invocation",
    "no Governance Gate bypass",
    "never treat health candidate as real system state mutation",
)

DOWNSTREAM_HANDOFFS: Tuple[Dict[str, Any], ...] = (
    {"target": "module_adapter", "payload": "required_observation_candidate", "mount_now": False},
    {"target": "task_manager", "payload": "hold / blocked / health gate candidate", "mount_now": False},
    {"target": "decision_center", "payload": "health review result candidate loopback", "mount_now": False},
    {"target": "governance_gate", "payload": "high-risk recovery / safety block candidate", "mount_now": False},
    {"target": "worldmodel_memory_bridge", "payload": "health observation candidate after admission policy later", "mount_now": False},
    {"target": "output_gate", "payload": "no direct output; only after Output Gate mount and readiness", "mount_now": False},
)

SAMPLE_FLOWS: Tuple[Dict[str, Any], ...] = (
    {
        "flow_id": "missing_health_refs_generates_health_review_candidate",
        "inputs": ["health_review_candidate_refs", "missing_health_refs"],
        "processing": ["validate trace", "classify missing health", "generate module_health_review_candidate"],
        "outputs": ["module_health_review_candidate", "health_signal_candidate"],
        "blocked_paths": ["recovery_execution", "task_execution"],
    },
    {
        "flow_id": "stale_context_generates_required_observation_candidate",
        "inputs": ["stale_context_refs", "trace_ref"],
        "processing": ["stale_context_review", "rank stale refs", "generate required_observation_candidate"],
        "outputs": ["required_observation_candidate", "watchdog_handoff_candidate"],
        "blocked_paths": ["treat_stale_as_fresh", "user_output"],
    },
    {
        "flow_id": "low_confidence_generates_hold_candidate",
        "inputs": ["low_confidence_refs", "decision_readiness_candidate_refs"],
        "processing": ["confidence threshold classification", "generate hold_candidate"],
        "outputs": ["hold_candidate", "degradation_candidate"],
        "blocked_paths": ["force_ready", "task_execution"],
    },
    {
        "flow_id": "p0_safety_unresolved_generates_safety_block_candidate",
        "inputs": ["p0_safety_unresolved_refs", "health_tag"],
        "processing": ["p0_safety_review", "conservative handling", "generate safety_block_candidate"],
        "outputs": ["safety_block_candidate", "governance_review_candidate"],
        "blocked_paths": ["output_gate", "recovery_execution"],
    },
    {
        "flow_id": "high_risk_recovery_without_governance_blocks",
        "inputs": ["recovery_recommendation_candidate", "missing_governance_ref"],
        "processing": ["governance_review", "block high-risk recovery recommendation"],
        "outputs": ["safety_block_candidate", "governance_review_candidate"],
        "blocked_paths": ["governance_bypass", "real_recovery"],
    },
    {
        "flow_id": "recovery_recommendation_does_not_execute_recovery",
        "inputs": ["health_fault_refs", "recovery_recommendation_candidate"],
        "processing": ["classify recovery recommendation", "generate watchdog_handoff_candidate"],
        "outputs": ["recovery_recommendation_candidate", "watchdog_handoff_candidate"],
        "blocked_paths": ["module_restart", "process_control", "system_command"],
    },
)

FAILURE_ROUTES: Tuple[Dict[str, str], ...] = (
    {"route_id": "missing_health_refs", "detection_signal": "health_refs_missing", "impact": "unsafe_readiness", "default_response": "module_health_review_candidate", "hold_or_block_candidate": "hold_candidate", "forbidden_shortcut": "assume_healthy"},
    {"route_id": "missing_trace", "detection_signal": "trace_missing", "impact": "untraceable_health_review", "default_response": "discarded_invalid", "hold_or_block_candidate": "safety_block_candidate", "forbidden_shortcut": "review_without_trace"},
    {"route_id": "missing_source_chain", "detection_signal": "source_chain_missing", "impact": "unverifiable_upstream", "default_response": "hold", "hold_or_block_candidate": "hold_candidate", "forbidden_shortcut": "accept_unknown_source"},
    {"route_id": "stale_context", "detection_signal": "stale_context_ref", "impact": "outdated_health_decision", "default_response": "required_observation_candidate", "hold_or_block_candidate": "hold_candidate", "forbidden_shortcut": "treat_stale_as_current"},
    {"route_id": "low_confidence", "detection_signal": "low_confidence_ref", "impact": "weak_health_basis", "default_response": "hold_candidate", "hold_or_block_candidate": "hold_candidate", "forbidden_shortcut": "force_ready"},
    {"route_id": "p0_safety_unresolved", "detection_signal": "p0_safety_unresolved_ref", "impact": "safety_risk", "default_response": "safety_block_candidate", "hold_or_block_candidate": "safety_block_candidate", "forbidden_shortcut": "ignore_p0"},
    {"route_id": "high_risk_recovery_without_governance", "detection_signal": "governance_ref_missing", "impact": "governance_violation", "default_response": "governance_review_candidate", "hold_or_block_candidate": "safety_block_candidate", "forbidden_shortcut": "bypass_governance"},
    {"route_id": "recovery_execution_attempted", "detection_signal": "recovery_execution_now", "impact": "unauthorized_recovery", "default_response": "blocked", "hold_or_block_candidate": "safety_block_candidate", "forbidden_shortcut": "execute_recovery"},
    {"route_id": "module_restart_attempted", "detection_signal": "module_restart_now", "impact": "unauthorized_restart", "default_response": "blocked", "hold_or_block_candidate": "safety_block_candidate", "forbidden_shortcut": "restart_module"},
    {"route_id": "process_control_attempted", "detection_signal": "process_control_now", "impact": "unauthorized_process_control", "default_response": "blocked", "hold_or_block_candidate": "safety_block_candidate", "forbidden_shortcut": "kill_process"},
    {"route_id": "task_execution_attempted", "detection_signal": "task_execution_now", "impact": "unauthorized_execution", "default_response": "blocked", "hold_or_block_candidate": "safety_block_candidate", "forbidden_shortcut": "execute_task"},
    {"route_id": "output_attempted", "detection_signal": "user_output_allowed_now", "impact": "unauthorized_output", "default_response": "blocked", "hold_or_block_candidate": "safety_block_candidate", "forbidden_shortcut": "direct_output"},
    {"route_id": "memory_write_attempted", "detection_signal": "memory_write_allowed_now", "impact": "unauthorized_memory_write", "default_response": "blocked", "hold_or_block_candidate": "safety_block_candidate", "forbidden_shortcut": "write_memory"},
    {"route_id": "worldmodel_write_attempted", "detection_signal": "worldmodel_write_allowed_now", "impact": "unauthorized_worldmodel_write", "default_response": "blocked", "hold_or_block_candidate": "safety_block_candidate", "forbidden_shortcut": "write_worldmodel"},
    {"route_id": "model_invocation_attempted_now", "detection_signal": "model_invoked_now", "impact": "runtime_violation", "default_response": "hold_planning", "hold_or_block_candidate": "hold_candidate", "forbidden_shortcut": "invoke_model"},
    {"route_id": "provider_invocation_attempted_now", "detection_signal": "provider_invoked_now", "impact": "runtime_violation", "default_response": "hold_planning", "hold_or_block_candidate": "hold_candidate", "forbidden_shortcut": "invoke_provider"},
)

HEALTH_METRICS: Tuple[str, ...] = (
    "health_review_input_count",
    "health_signal_candidate_count",
    "degradation_candidate_count",
    "recovery_recommendation_candidate_count",
    "required_observation_candidate_count",
    "hold_candidate_count",
    "safety_block_candidate_count",
    "stale_context_count",
    "low_confidence_count",
    "p0_safety_unresolved_count",
    "governance_pending_count",
    "recovery_execution_block_count",
    "restart_attempt_block_count",
    "output_attempt_block_count",
    "write_attempt_block_count",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Mount Planning ≠ Health Watchdog implemented",
    "Mount Planning ≠ mounted now",
    "Mount Planning ≠ runtime enabled",
    "Mount Planning ≠ recovery execution",
    "Mount Planning ≠ module restart",
    "Mount Planning ≠ process control",
    "Mount Planning ≠ task execution",
    "Mount Planning ≠ Output Gate ready",
    "Mount Planning ≠ user output",
    "Mount Planning ≠ Memory / WorldModel write",
    "Mount Planning ≠ full safety system",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_health_watchdog_mount_planning_only",
    "mount_planning_only",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "health_watchdog_mounted_now",
    "health_watchdog_runtime_enabled_now",
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

DEFAULT_DECISION_CENTER_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_decision_center_foundation_handoff_dryrun_and_review"
)
DEFAULT_DECISION_CENTER_HANDOFF_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_foundation_handoff_planning"
)
DEFAULT_DECISION_CENTER_POST_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_INFORMATION_INTEGRATION_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_MICRO_OS_FREEZE_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_mount_planning"


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "module_id": "health_watchdog",
        "layer": "L5_health",
        "foundation_id": "midplatform_decision_center_foundation_v1",
        "depends_on": "midplatform_decision_center_foundation_v1",
        "also_depends_on": [
            "midplatform_information_integration_foundation_v1",
            "midplatform_micro_os_foundation_v1",
        ],
        "runtime_status": "not_enabled",
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


def _template_contract() -> Dict[str, Any]:
    return {
        "module_identity": {
            "module_id": "health_watchdog",
            "module_type": "candidate_health_supervision_layer",
            "role": "health supervision and safety degradation candidate generator, not recovery executor",
            "layer": "L5_health",
        },
        "upstream_sources": {
            "upstream_modules": ["decision_center"],
            "frozen_foundation": "midplatform_decision_center_foundation_v1",
            "frozen_outputs_consumed": list(DECISION_CENTER_OUTPUTS_CONSUMED),
        },
        "downstream_targets": {
            "targets": [h["target"] for h in DOWNSTREAM_HANDOFFS],
            "direct_mount_executed": False,
        },
        "input_contract": {
            "input_types": list(INPUT_TYPES),
            "required_fields": list(INPUT_REQUIRED_FIELDS),
            "candidate_not_fact_required": True,
        },
        "processing_scope": {
            "planning_only": True,
            "runtime_execution": False,
            "recovery_execution": False,
            "module_restart": False,
            "process_control": False,
        },
        "output_contract": {
            "outputs": list(OUTPUT_CANDIDATES),
            "all_candidate": True,
            "recovery_recommendation_is_not_recovery_execution": True,
            "degradation_candidate_is_not_real_degradation": True,
            "forbidden_outputs": list(FORBIDDEN_OUTPUTS),
        },
        "module_principles": {
            "candidate_only": True,
            "no_governance_bypass": True,
            "health_candidate_not_real_state_mutation": True,
        },
        "external_constraints": {
            "model_invoked_now": False,
            "provider_invoked_now": False,
            "system_command_allowed": False,
        },
        "runtime_boundaries": {f: False for f in BOUNDARY_FALSE},
        "failure_and_traceability": {
            "failure_routes": [r["route_id"] for r in FAILURE_ROUTES],
            "trace_required": True,
            "source_chain_required": True,
        },
    }


def run_midplatform_health_watchdog_mount_planning_v1(
    *,
    midplatform_decision_center_foundation_handoff_dryrun_and_review_root: str,
    midplatform_decision_center_foundation_handoff_planning_root: str,
    midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review_root: str,
    midplatform_information_integration_foundation_handoff_dryrun_and_review_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dc_handoff_dr = Path(midplatform_decision_center_foundation_handoff_dryrun_and_review_root).expanduser().resolve()
    dc_handoff_plan = Path(midplatform_decision_center_foundation_handoff_planning_root).expanduser().resolve()
    dc_post_dr = Path(midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review_root).expanduser().resolve()
    ii_handoff_dr = Path(midplatform_information_integration_foundation_handoff_dryrun_and_review_root).expanduser().resolve()
    micro_os_dr = Path(midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "output_root": str(out_root),
        "upstream_decision_center_handoff_dryrun_root": str(dc_handoff_dr),
        "upstream_decision_center_handoff_planning_root": str(dc_handoff_plan),
        "upstream_decision_center_post_dryrun_root": str(dc_post_dr),
        "upstream_information_integration_handoff_dryrun_root": str(ii_handoff_dr),
        "upstream_micro_os_freeze_dryrun_root": str(micro_os_dr),
    }

    dc_vr = _try_read_json(dc_handoff_dr / "verifier_report.json") or {}
    dc_sm = _try_read_json(dc_handoff_dr / "summary.json") or {}
    dc_ready = _try_read_json(dc_handoff_dr / "handoff_dryrun_readiness_decision_v1.json") or {}
    if dc_vr.get("verifier") != "GO":
        blockers.append("Decision Center foundation handoff dryrun verifier must be GO")
    if dc_sm.get("final_decision") != UPSTREAM_DECISION_CENTER_HANDOFF_DRYRUN_FINAL:
        blockers.append("Decision Center foundation handoff dryrun final_decision mismatch")
    if dc_ready.get("dryrun_pass") is not True:
        blockers.append("Decision Center foundation handoff dryrun pass flag must be true")

    upstream_dc: Dict[str, Any] = {}
    for fname in UPSTREAM_DECISION_CENTER_HANDOFF_DRYRUN_FILES:
        data = _try_read_json(dc_handoff_dr / fname)
        if data is None:
            blockers.append(f"missing Decision Center handoff dryrun upstream: {fname}")
        upstream_dc[fname.replace("_v1.json", "").replace(".json", "")] = data
    upstream_dc_plan: Dict[str, Any] = {}
    for fname in UPSTREAM_DECISION_CENTER_HANDOFF_PLANNING_FILES:
        data = _try_read_json(dc_handoff_plan / fname)
        if data is None:
            blockers.append(f"missing Decision Center handoff planning upstream: {fname}")
        upstream_dc_plan[fname.replace("_v1.json", "")] = data
    for fname in UPSTREAM_INFORMATION_INTEGRATION_FILES:
        if _try_read_json(ii_handoff_dr / fname) is None:
            blockers.append(f"missing Information Integration upstream: {fname}")
    for fname in UPSTREAM_MICRO_OS_FILES:
        if _try_read_json(micro_os_dr / fname) is None:
            blockers.append(f"missing Micro-OS upstream: {fname}")

    dc_version = upstream_dc_plan.get("decision_center_foundation_version_tag") or {}
    ii_summary = _try_read_json(ii_handoff_dr / "summary.json") or {}
    micro_summary = _try_read_json(micro_os_dr / "summary.json") or {}
    if dc_version.get("foundation_id") != "midplatform_decision_center_foundation_v1":
        blockers.append("Decision Center foundation_id mismatch")
    if dc_version.get("runtime_status") != "not_enabled":
        blockers.append("Decision Center runtime_status must be not_enabled")
    if ii_summary.get("foundation_id") != "midplatform_information_integration_foundation_v1":
        blockers.append("Information Integration foundation mismatch")
    if micro_summary.get("foundation_id") != "midplatform_micro_os_foundation_v1":
        blockers.append("Micro-OS foundation mismatch")

    mount_scope = {
        "scope_id": "health_watchdog_mount_scope_v1",
        "module_id": "health_watchdog",
        "layer": "L5_health",
        "mount_planning_only": True,
        "upstream_foundation": "midplatform_decision_center_foundation_v1",
        "allowed_decision_center_outputs_consumed": list(DECISION_CENTER_OUTPUTS_CONSUMED),
        "allowed_outputs": list(OUTPUT_CANDIDATES),
        "forbidden": [
            "real_recovery",
            "module_restart",
            "process_control",
            "task_execution",
            "user_output",
            "memory_write",
            "worldmodel_write",
            "model_provider_invocation",
            "direct_task_manager_mount",
            "direct_output_gate_mount",
        ],
        "responsibilities": list(RESPONSIBILITIES),
        "must_not_redefine_decision_center": True,
        "direct_mount_executed": False,
        **meta,
    }

    mount_contract = {
        "contract_id": "health_watchdog_mount_contract_v1",
        **_template_contract(),
        **meta,
    }

    input_contract = {
        "contract_id": "health_watchdog_input_contract_v1",
        "input_types": list(INPUT_TYPES),
        "required_fields": list(INPUT_REQUIRED_FIELDS),
        "candidate_not_fact_required": True,
        "trace_required": True,
        "health_tag_required": True,
        "source_chain_required": True,
        "governance_ref_required_for_high_risk_recovery_recommendation": True,
        **meta,
    }

    output_contract = {
        "contract_id": "health_watchdog_output_contract_v1",
        "outputs": list(OUTPUT_CANDIDATES),
        "all_candidate": True,
        "recovery_recommendation_candidate_is_not_recovery_execution": True,
        "degradation_candidate_is_not_real_degradation": True,
        "forbidden_outputs": list(FORBIDDEN_OUTPUTS),
        "fact_status": "not_fact",
        **meta,
    }

    processing_model = {
        "model_id": "health_watchdog_processing_model_v1",
        "steps": list(PROCESSING_STEPS),
        "planning_only": True,
        "real_watchdog_runtime_enabled": False,
        "recovery_execution": False,
        **meta,
    }

    health_state_machine = {
        "machine_id": "health_watchdog_health_state_machine_v1",
        "states": list(HEALTH_STATES),
        "state_count": len(HEALTH_STATES),
        "all_candidate_level": True,
        "runtime_state_mutation": False,
        **meta,
    }

    mra_placement = {
        "placement_id": "health_watchdog_model_rule_algorithm_placement_v1",
        "model_uses_later": list(MODEL_USES),
        "rule_uses": list(RULE_USES),
        "algorithm_uses": list(ALGORITHM_USES),
        "model_invoked_now": False,
        "provider_invoked_now": False,
        "runtime_enabled_now": False,
        **meta,
    }

    governance_boundary = {
        "boundary_id": "health_watchdog_governance_boundary_v1",
        "rules": [
            "do not bypass L0 Governance Gate",
            "high-risk recovery recommendation requires governance_ref",
            "recovery_recommendation_candidate is not recovery execution",
            "degradation_candidate is not real module degradation",
            "output/write/runtime attempts blocked",
            "Health Watchdog must not enter Task Manager or Output Gate runtime directly",
            "Health Watchdog must not rewrite Scheduler priority directly",
        ],
        **meta,
    }

    recovery_boundary = {
        "boundary_id": "health_watchdog_recovery_boundary_v1",
        "rules": [
            "no real recovery",
            "no restart",
            "no kill process",
            "no permissions release",
            "no module reload",
            "no system command",
            "no emergency output",
            "only recovery_recommendation_candidate",
            "only watchdog_handoff_candidate",
            "real recovery later requires authorization / owner-operator approval / recovery protocol",
        ],
        **meta,
    }

    dc_dependency_boundary = {
        "boundary_id": "health_watchdog_decision_center_dependency_boundary_v1",
        "rules": [
            "Health Watchdog may only consume midplatform_decision_center_foundation_v1 frozen outputs",
            "must not redefine Decision Center",
            "must not modify DecisionCandidate",
            "must not treat decision_candidate as final action",
            "must not treat blocked/hold as real system state",
            "must not require Decision Center runtime",
            "new fields require change_control",
        ],
        "foundation_id": "midplatform_decision_center_foundation_v1",
        **meta,
    }

    downstream_handoff = {
        "matrix_id": "health_watchdog_downstream_handoff_matrix_v1",
        "handoffs": list(DOWNSTREAM_HANDOFFS),
        "direct_mount_executed": False,
        **meta,
    }

    sample_flow_plan = {
        "plan_id": "health_watchdog_sample_flow_plan_v1",
        "flows": list(SAMPLE_FLOWS),
        "flow_count": len(SAMPLE_FLOWS),
        **meta,
    }

    failure_matrix = {
        "matrix_id": "health_watchdog_failure_route_matrix_v1",
        "routes": list(FAILURE_ROUTES),
        "route_count": len(FAILURE_ROUTES),
        **meta,
    }

    metric_scope = {
        "scope_id": "health_watchdog_mount_health_metric_scope_v1",
        "metrics": list(HEALTH_METRICS),
        "metric_count": len(HEALTH_METRICS),
        "real_health_runtime_enabled": False,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "health_watchdog_boundary_matrix_v1",
        "global_boundaries": {f: False for f in BOUNDARY_FALSE},
        **meta,
    }

    mount_non_claims = {
        "register_id": "health_watchdog_mount_non_claims_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    planning_pass = len(blockers) == 0
    readiness = {
        "decision_id": "health_watchdog_mount_readiness_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "decision_center_foundation_consumed": True,
        "must_not_redefine_decision_center": True,
        "no_real_recovery": True,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "foundation_id": "midplatform_decision_center_foundation_v1",
        "foundation_version": dc_version.get("version", "1.0.0-skeleton"),
        "runtime_status": "not_enabled",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    return {
        "summary": summary,
        "health_watchdog_mount_scope": mount_scope,
        "health_watchdog_mount_contract": mount_contract,
        "health_watchdog_input_contract": input_contract,
        "health_watchdog_output_contract": output_contract,
        "health_watchdog_processing_model": processing_model,
        "health_watchdog_health_state_machine": health_state_machine,
        "health_watchdog_model_rule_algorithm_placement": mra_placement,
        "health_watchdog_governance_boundary": governance_boundary,
        "health_watchdog_recovery_boundary": recovery_boundary,
        "health_watchdog_decision_center_dependency_boundary": dc_dependency_boundary,
        "health_watchdog_downstream_handoff_matrix": downstream_handoff,
        "health_watchdog_sample_flow_plan": sample_flow_plan,
        "health_watchdog_failure_route_matrix": failure_matrix,
        "health_watchdog_mount_health_metric_scope": metric_scope,
        "health_watchdog_boundary_matrix": boundary_matrix,
        "health_watchdog_mount_non_claims": mount_non_claims,
        "health_watchdog_mount_readiness_decision": readiness,
    }
