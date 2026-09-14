# -*- coding: utf-8 -*-
"""Luna Midplatform Decision Center Mount Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_information_integration_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as HANDOFF_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as HANDOFF_DRYRUN_NEXT,
)

PHASE_ID = "Phase-Midplatform-Decision-Center-Mount-Planning-v1-001"
SCOPE = "midplatform_decision_center_mount_planning_only"
SOURCE_CHAIN = "midplatform_decision_center_mount_planning_v1"

UPSTREAM_HANDOFF_DRYRUN_FINAL = HANDOFF_DRYRUN_FINAL_GO
UPSTREAM_HANDOFF_DRYRUN_NEXT = HANDOFF_DRYRUN_NEXT

FINAL_DECISION_GO = "MIDPLATFORM_DECISION_CENTER_MOUNT_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_DECISION_CENTER_MOUNT_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Decision-Center-Mount-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Decision-Center-Mount-Issue-Review-v1-001"

UPSTREAM_HANDOFF_DRYRUN_FILES: Tuple[str, ...] = (
    "handoff_dryrun_readiness_decision_v1.json",
    "summary.json",
    "verifier_report.json",
)

UPSTREAM_HANDOFF_PLANNING_FILES: Tuple[str, ...] = (
    "information_integration_foundation_version_tag_v1.json",
    "information_integration_frozen_type_interface_v1.json",
    "information_integration_frozen_function_interface_v1.json",
    "information_integration_frozen_validator_interface_v1.json",
    "information_integration_handoff_contract_v1.json",
    "information_integration_downstream_output_contract_v1.json",
    "information_integration_forbidden_mutation_policy_v1.json",
    "information_integration_change_control_policy_v1.json",
    "information_integration_boundary_freeze_v1.json",
    "information_integration_downstream_readiness_matrix_v1.json",
    "information_integration_route_decision_v1.json",
)

UPSTREAM_FREEZE_PLANNING_FILES: Tuple[str, ...] = (
    "micro_os_foundation_version_tag_v1.json",
    "micro_os_foundation_frozen_interface_v1.json",
    "micro_os_foundation_handoff_contract_v1.json",
)

II_FROZEN_OUTPUTS_CONSUMED: Tuple[str, ...] = (
    "decision_context_candidate",
    "live_world_state_candidate",
    "task_world_slice_candidate",
    "priority_attention_map_candidate",
    "information_allocation_candidate",
    "conflict_candidate",
    "gap_candidate",
    "required_observation_candidate",
)

INPUT_TYPES: Tuple[str, ...] = (
    "decision_context_candidate",
    "live_world_state_candidate_ref",
    "task_world_slice_candidate_ref",
    "priority_attention_map_candidate_ref",
    "information_allocation_candidate_ref",
    "conflict_candidate_refs",
    "gap_candidate_refs",
    "required_observation_candidate_refs",
    "health_refs",
    "governance_check_ref",
    "trace_ref",
)

INPUT_REQUIRED_FIELDS: Tuple[str, ...] = (
    "candidate_not_fact",
    "trace",
    "health_tag",
    "source_chain",
    "governance_ref_for_high_risk",
)

OUTPUT_CANDIDATES: Tuple[str, ...] = (
    "decision_candidate",
    "decision_readiness_candidate",
    "decision_block_candidate",
    "decision_explanation_candidate",
    "downstream_decision_handoff_candidate",
    "task_handoff_candidate",
    "output_handoff_candidate",
    "health_review_candidate",
    "required_observation_handoff_candidate",
    "memory_worldmodel_admission_review_candidate",
)

OUTPUT_IMMEDIATE: Tuple[str, ...] = (
    "decision_candidate",
    "decision_readiness_candidate",
    "decision_block_candidate",
    "decision_explanation_candidate",
    "downstream_decision_handoff_candidate",
)

OUTPUT_LATER: Tuple[str, ...] = (
    "task_handoff_candidate",
    "output_handoff_candidate",
    "health_review_candidate",
    "required_observation_handoff_candidate",
    "memory_worldmodel_admission_review_candidate",
)

PROCESSING_STEPS: Tuple[str, ...] = (
    "consume decision_context_candidate",
    "validate trace / health / governance / candidate_not_fact",
    "inspect readiness_status",
    "inspect conflict/gap lists",
    "inspect P0/P1 attention",
    "inspect health blockers",
    "classify decision state",
    "generate decision_candidate or block/hold candidate",
    "generate downstream handoff candidate",
)

DECISION_STATES: Tuple[str, ...] = (
    "received",
    "validating",
    "governance_pending",
    "health_pending",
    "conflict_review",
    "gap_review",
    "ready_for_candidate_decision",
    "decision_candidate_generated",
    "blocked",
    "not_ready",
    "hold",
    "requires_observation",
    "requires_health_review",
    "handoff_ready",
    "discarded_invalid",
)

READINESS_CLASSIFICATIONS: Tuple[str, ...] = (
    "ready",
    "not_ready",
    "blocked",
    "needs_observation",
    "needs_health_review",
)

MODEL_USES: Tuple[str, ...] = (
    "complex_explanation",
    "multi_constraint_decision_summary",
    "conflict_explanation",
    "decision_explanation_candidate_draft",
)

RULE_USES: Tuple[str, ...] = (
    "governance_gate",
    "candidate_fact_boundary",
    "high_risk_governance_required",
    "unresolved_conflict_blocks_readiness",
    "missing_health_blocks_readiness",
    "output_write_runtime_forbidden",
    "p0_safety_conservative_handling",
)

ALGORITHM_USES: Tuple[str, ...] = (
    "readiness_scoring",
    "conflict_severity_ranking",
    "gap_severity_ranking",
    "handoff_route_ranking",
    "decision_state_classification",
)

RESPONSIBILITIES: Tuple[str, ...] = (
    "consume decision_context_candidate",
    "check decision_context readiness",
    "check conflict / gap / health / governance",
    "classify ready / not_ready / blocked / needs_observation / needs_health_review",
    "generate decision_candidate",
    "generate decision_readiness_candidate",
    "generate decision_block_candidate",
    "generate decision_explanation_candidate",
    "generate downstream_decision_handoff_candidate",
    "no task execution",
    "no user output",
    "no Memory / WorldModel write",
    "no model/provider invocation",
    "no Governance Gate bypass",
    "never treat candidate as fact or final action",
)

DOWNSTREAM_HANDOFFS: Tuple[Dict[str, Any], ...] = (
    {"target": "task_manager", "payload": "task_handoff_candidate", "also": "decision_candidate", "mount_now": False},
    {"target": "output_gate", "payload": "output_handoff_candidate", "mount_now": False},
    {"target": "health_watchdog", "payload": "health_review_candidate", "mount_now": False},
    {"target": "module_adapter", "payload": "required_observation_handoff_candidate", "mount_now": False},
    {"target": "worldmodel_memory_bridge", "payload": "memory_worldmodel_admission_review_candidate", "mount_now": False},
    {"target": "governance_gate", "payload": "governance_pending_or_blocked_candidate", "mount_now": False},
)

SAMPLE_FLOWS: Tuple[Dict[str, Any], ...] = (
    {
        "flow_id": "ready_navigation_decision_context_to_decision_candidate",
        "inputs": ["decision_context_candidate", "priority_attention_map_candidate_ref", "governance_check_ref"],
        "processing": ["validate", "inspect readiness", "classify ready", "generate decision_candidate"],
        "outputs": ["decision_candidate", "decision_readiness_candidate", "downstream_decision_handoff_candidate"],
        "blocked_paths": ["task_execution", "user_output", "memory_write"],
    },
    {
        "flow_id": "conflict_blocks_decision_candidate",
        "inputs": ["decision_context_candidate", "conflict_candidate_refs"],
        "processing": ["conflict_review", "classify blocked"],
        "outputs": ["decision_block_candidate", "decision_readiness_candidate"],
        "blocked_paths": ["decision_candidate as final action", "task_execution"],
    },
    {
        "flow_id": "gap_requires_observation_candidate",
        "inputs": ["decision_context_candidate", "gap_candidate_refs"],
        "processing": ["gap_review", "classify requires_observation"],
        "outputs": ["required_observation_handoff_candidate", "decision_readiness_candidate"],
        "blocked_paths": ["decision_candidate without observation", "user_output"],
    },
    {
        "flow_id": "health_fault_routes_to_health_review_candidate",
        "inputs": ["decision_context_candidate", "health_refs"],
        "processing": ["health_pending", "classify needs_health_review"],
        "outputs": ["health_review_candidate", "decision_block_candidate"],
        "blocked_paths": ["real health runtime", "task_execution"],
    },
    {
        "flow_id": "high_risk_missing_governance_blocks",
        "inputs": ["decision_context_candidate", "priority_attention_map_candidate_ref"],
        "processing": ["governance_pending", "classify blocked"],
        "outputs": ["decision_block_candidate", "decision_readiness_candidate"],
        "blocked_paths": ["bypass governance gate", "decision_candidate as final action"],
    },
    {
        "flow_id": "output_attempt_before_output_gate_blocks",
        "inputs": ["decision_context_candidate", "output_handoff_candidate"],
        "processing": ["block output attempt", "classify blocked"],
        "outputs": ["decision_block_candidate"],
        "blocked_paths": ["user_output", "output_gate runtime", "final action"],
    },
)

FAILURE_ROUTES: Tuple[Dict[str, Any], ...] = (
    {"route_id": "missing_decision_context", "detection_signal": "decision_context_missing", "impact": "no_decision_basis", "default_response": "discarded_invalid", "hold_or_block_candidate": "decision_block_candidate", "forbidden_shortcut": "decide_without_context"},
    {"route_id": "decision_context_not_ready", "detection_signal": "readiness_not_ready", "impact": "premature_decision", "default_response": "not_ready", "hold_or_block_candidate": "decision_readiness_candidate", "forbidden_shortcut": "force_ready_decision"},
    {"route_id": "missing_trace", "detection_signal": "trace_missing", "impact": "untraceable_decision", "default_response": "blocked", "hold_or_block_candidate": "decision_block_candidate", "forbidden_shortcut": "decide_without_trace"},
    {"route_id": "missing_health_refs", "detection_signal": "health_refs_missing", "impact": "unsafe_decision", "default_response": "requires_health_review", "hold_or_block_candidate": "health_review_candidate", "forbidden_shortcut": "assume_healthy"},
    {"route_id": "missing_governance_for_high_risk", "detection_signal": "governance_missing_high_risk", "impact": "governance_violation", "default_response": "governance_pending", "hold_or_block_candidate": "decision_block_candidate", "forbidden_shortcut": "bypass_governance"},
    {"route_id": "unresolved_conflict", "detection_signal": "unresolved_conflict_count", "impact": "conflicting_decision", "default_response": "blocked", "hold_or_block_candidate": "decision_block_candidate", "forbidden_shortcut": "ignore_conflict"},
    {"route_id": "unresolved_gap", "detection_signal": "unresolved_gap_count", "impact": "incomplete_context", "default_response": "requires_observation", "hold_or_block_candidate": "required_observation_handoff_candidate", "forbidden_shortcut": "decide_with_gap"},
    {"route_id": "stale_context", "detection_signal": "stale_context_count", "impact": "outdated_decision", "default_response": "requires_observation", "hold_or_block_candidate": "required_observation_handoff_candidate", "forbidden_shortcut": "treat_stale_as_fresh"},
    {"route_id": "output_attempted_before_output_gate", "detection_signal": "premature_output_attempt", "impact": "unauthorized_output", "default_response": "blocked", "hold_or_block_candidate": "decision_block_candidate", "forbidden_shortcut": "direct_user_output"},
    {"route_id": "task_execution_attempted", "detection_signal": "task_execution_attempt", "impact": "unauthorized_execution", "default_response": "blocked", "hold_or_block_candidate": "decision_block_candidate", "forbidden_shortcut": "execute_task_from_decision_center"},
    {"route_id": "memory_write_attempted", "detection_signal": "memory_write_attempt", "impact": "unauthorized_persistence", "default_response": "blocked", "hold_or_block_candidate": "decision_block_candidate", "forbidden_shortcut": "direct_memory_write"},
    {"route_id": "worldmodel_write_attempted", "detection_signal": "worldmodel_write_attempt", "impact": "unauthorized_persistence", "default_response": "blocked", "hold_or_block_candidate": "decision_block_candidate", "forbidden_shortcut": "direct_worldmodel_write"},
    {"route_id": "model_invocation_attempted_now", "detection_signal": "model_invoked_now", "impact": "runtime_violation", "default_response": "hold_planning", "hold_or_block_candidate": "decision_block_candidate", "forbidden_shortcut": "invoke_model_in_mount_planning"},
    {"route_id": "provider_invocation_attempted_now", "detection_signal": "provider_invoked_now", "impact": "runtime_violation", "default_response": "hold_planning", "hold_or_block_candidate": "decision_block_candidate", "forbidden_shortcut": "invoke_provider_in_mount_planning"},
)

HEALTH_METRICS: Tuple[str, ...] = (
    "decision_context_input_count",
    "ready_context_count",
    "not_ready_context_count",
    "blocked_context_count",
    "conflict_block_count",
    "gap_block_count",
    "health_review_candidate_count",
    "governance_pending_count",
    "decision_candidate_count",
    "handoff_candidate_count",
    "output_attempt_block_count",
    "write_attempt_block_count",
    "stale_context_count",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Mount Planning ≠ Decision Center implemented",
    "Mount Planning ≠ mounted now",
    "Mount Planning ≠ runtime enabled",
    "Mount Planning ≠ model invoked",
    "Mount Planning ≠ final decision action",
    "Mount Planning ≠ task execution",
    "Mount Planning ≠ Output Gate ready",
    "Mount Planning ≠ user output",
    "Mount Planning ≠ Memory / WorldModel write",
    "Mount Planning ≠ full decision pipeline",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_decision_center_mount_planning_only",
    "mount_planning_only",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "decision_center_mounted_now",
    "decision_center_runtime_enabled_now",
    "model_invoked_now",
    "provider_invoked_now",
    "runtime_enabled_now",
    "task_execution_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "output_gate_mounted_now",
    "task_manager_mounted_now",
    "health_watchdog_mounted_now",
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
)

DEFAULT_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_HANDOFF_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_foundation_handoff_planning"
)
DEFAULT_POST_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_FREEZE_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_FREEZE_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_planning"
)
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_mount_planning"


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "foundation_id": "midplatform_information_integration_foundation_v1",
        "depends_on": "midplatform_micro_os_foundation_v1",
        "foundation_version": "1.0.0-skeleton",
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


def _build_mount_contract(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "contract_id": "decision_center_mount_contract_v1",
        "module_identity": {
            "module_id": "decision_center",
            "module_name": "Decision Center",
            "layer": "L7",
            "role": "candidate decision arbitration layer — not executor, not output layer",
        },
        "upstream_sources": {
            "sources": ["information_integration"],
            "foundation_id": "midplatform_information_integration_foundation_v1",
            "depends_on": "midplatform_micro_os_foundation_v1",
            "frozen_outputs_consumed": list(II_FROZEN_OUTPUTS_CONSUMED),
        },
        "downstream_targets": {
            "targets": ["task_manager", "output_gate", "health_watchdog", "module_adapter", "worldmodel_memory_bridge", "governance_gate"],
            "candidate_only": True,
            "direct_mount": False,
        },
        "input_contract": {
            "input_types": list(INPUT_TYPES),
            "required_fields": list(INPUT_REQUIRED_FIELDS),
            "core_input": "decision_context_candidate",
            "frozen_ii_outputs": list(II_FROZEN_OUTPUTS_CONSUMED),
        },
        "processing_scope": {
            "steps": list(PROCESSING_STEPS),
            "responsibilities": list(RESPONSIBILITIES),
            "planning_only": True,
            "runtime_execution": False,
            "decision_execution": False,
        },
        "output_contract": {
            "output_types": list(OUTPUT_CANDIDATES),
            "immediate_outputs": list(OUTPUT_IMMEDIATE),
            "later_outputs": list(OUTPUT_LATER),
            "all_candidate": True,
            "fact_status": "candidate_only",
            "final_action": False,
            "write_allowed": False,
            "user_output_allowed": False,
        },
        "module_principles": [
            "consume frozen Information Integration candidate outputs only",
            "never redefine Information Integration",
            "all outputs are decision candidates — not final actions",
            "never promote candidate to fact",
            "never bypass Governance Gate",
            "never execute tasks or produce user output",
            "never write Memory or WorldModel",
        ],
        "external_constraints": {
            "l0_governance": True,
            "ii_handoff_contract": True,
            "ii_forbidden_mutation_policy": True,
            "ii_change_control_policy": True,
        },
        "runtime_boundaries": {f: False for f in BOUNDARY_FALSE},
        "failure_and_traceability": {
            "failure_route_count": len(FAILURE_ROUTES),
            "trace_required": True,
            "audit_required": True,
        },
        **meta,
    }


def run_midplatform_decision_center_mount_planning_v1(
    *,
    midplatform_information_integration_foundation_handoff_dryrun_and_review_root: str,
    midplatform_information_integration_foundation_handoff_planning_root: str,
    midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_planning_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    handoff_dr = Path(midplatform_information_integration_foundation_handoff_dryrun_and_review_root).expanduser().resolve()
    handoff_plan = Path(midplatform_information_integration_foundation_handoff_planning_root).expanduser().resolve()
    post_dr = Path(midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review_root).expanduser().resolve()
    freeze_dr = Path(midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root).expanduser().resolve()
    freeze_plan = Path(
        midplatform_micro_os_foundation_freeze_and_handoff_planning_root or DEFAULT_FREEZE_PLANNING_ROOT
    ).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "output_root": str(out_root),
        "upstream_handoff_dryrun_root": str(handoff_dr),
        "upstream_handoff_planning_root": str(handoff_plan),
        "upstream_post_dryrun_root": str(post_dr),
        "upstream_freeze_dryrun_root": str(freeze_dr),
        "upstream_freeze_planning_root": str(freeze_plan),
    }

    handoff_dr_vr = _try_read_json(handoff_dr / "verifier_report.json") or {}
    handoff_dr_sm = _try_read_json(handoff_dr / "summary.json") or {}
    handoff_ready = _try_read_json(handoff_dr / "handoff_dryrun_readiness_decision_v1.json") or {}

    if handoff_dr_vr.get("verifier") != "GO":
        blockers.append("upstream handoff dryrun verifier must be GO")
    if handoff_dr_sm.get("final_decision") != UPSTREAM_HANDOFF_DRYRUN_FINAL:
        blockers.append("upstream handoff dryrun final_decision mismatch")
    if handoff_ready.get("dryrun_pass") is not True:
        blockers.append("upstream handoff_dryrun_readiness must pass")

    upstream: Dict[str, Any] = {}
    for fname in UPSTREAM_HANDOFF_DRYRUN_FILES:
        data = _try_read_json(handoff_dr / fname)
        if data is None:
            blockers.append(f"missing upstream handoff dryrun: {fname}")
        upstream[fname.replace("_v1.json", "").replace(".json", "")] = data

    for fname in UPSTREAM_HANDOFF_PLANNING_FILES:
        data = _try_read_json(handoff_plan / fname)
        if data is None:
            blockers.append(f"missing upstream handoff planning: {fname}")
        upstream[fname.replace("_v1.json", "")] = data

    for fname in UPSTREAM_FREEZE_PLANNING_FILES:
        data = _try_read_json(freeze_plan / fname)
        if data is None:
            blockers.append(f"missing upstream freeze planning: {fname}")
        upstream[fname.replace("_v1.json", "")] = data

    ii_version = upstream.get("information_integration_foundation_version_tag") or {}
    ii_route = upstream.get("information_integration_route_decision") or {}
    ii_output_contract = upstream.get("information_integration_downstream_output_contract") or {}
    micro_version = upstream.get("micro_os_foundation_version_tag") or {}

    if ii_version.get("foundation_id") != "midplatform_information_integration_foundation_v1":
        blockers.append("information_integration foundation_id mismatch")
    if ii_version.get("depends_on") != "midplatform_micro_os_foundation_v1":
        blockers.append("depends_on must be midplatform_micro_os_foundation_v1")
    if ii_version.get("runtime_status") != "not_enabled":
        blockers.append("information_integration runtime must be not_enabled")
    if ii_route.get("primary_next_phase") != "Phase-Midplatform-Decision-Center-Mount-Planning-v1-001":
        blockers.append("Decision Center must be primary route after II handoff")
    if micro_version.get("foundation_id") != "midplatform_micro_os_foundation_v1":
        blockers.append("micro_os foundation_id mismatch")

    dc_consumer = next(
        (e for e in ii_output_contract.get("entries") or [] if e.get("consumer") == "decision_center"),
        {},
    )
    if "decision_context_candidate" not in (dc_consumer.get("consumes") or []):
        blockers.append("II downstream contract must include decision_context_candidate for decision_center")

    mount_scope = {
        "scope_id": "decision_center_mount_scope_v1",
        "layer": "L7",
        "module_id": "decision_center",
        "role": "candidate decision arbitration — not executor, not output layer",
        "ii_frozen_outputs_consumed": list(II_FROZEN_OUTPUTS_CONSUMED),
        "responsibilities": list(RESPONSIBILITIES),
        "must_not_redefine_information_integration": True,
        "mount_planning_only": True,
        "direct_mount_executed": False,
        **meta,
    }

    mount_contract = _build_mount_contract(meta)

    input_contract = {
        "contract_id": "decision_center_input_contract_v1",
        "input_types": list(INPUT_TYPES),
        "required_fields": list(INPUT_REQUIRED_FIELDS),
        "core_input": "decision_context_candidate",
        "ii_frozen_outputs": list(II_FROZEN_OUTPUTS_CONSUMED),
        **meta,
    }

    output_contract = {
        "contract_id": "decision_center_output_contract_v1",
        "outputs": list(OUTPUT_CANDIDATES),
        "immediate_outputs": list(OUTPUT_IMMEDIATE),
        "later_outputs": list(OUTPUT_LATER),
        "all_candidate": True,
        "decision_candidate_is_not_final_action": True,
        "decision_candidate_is_not_user_output": True,
        "forbidden_outputs": ["final_action", "runtime_command", "user_output", "fact", "memory_write", "worldmodel_write"],
        **meta,
    }

    processing_model = {
        "model_id": "decision_center_processing_model_v1",
        "steps": list(PROCESSING_STEPS),
        "readiness_classifications": list(READINESS_CLASSIFICATIONS),
        "planning_only": True,
        "runtime_decision_execution": False,
        **meta,
    }

    decision_state_machine = {
        "machine_id": "decision_center_decision_state_machine_v1",
        "states": list(DECISION_STATES),
        "state_count": len(DECISION_STATES),
        "all_candidate_level": True,
        "transitions_planning_only": True,
        **meta,
    }

    mra_placement = {
        "placement_id": "decision_center_model_rule_algorithm_placement_v1",
        "model_uses": list(MODEL_USES),
        "rule_uses": list(RULE_USES),
        "algorithm_uses": list(ALGORITHM_USES),
        "state_machine_uses": list(DECISION_STATES),
        "model_invoked_now": False,
        "no_model_in_mount_planning_now": True,
        "no_runtime_now": True,
        **meta,
    }

    governance_boundary = {
        "boundary_id": "decision_center_governance_boundary_v1",
        "rules": [
            "do not bypass L0 Governance Gate",
            "high-risk decision_candidate must carry governance_check_ref",
            "unresolved conflict must not generate ready decision",
            "output/write/runtime attempts blocked",
            "decision_candidate ≠ final decision action",
            "decision_candidate ≠ user output",
            "Decision Center must not enter TTS / Output Gate runtime directly",
        ],
        **meta,
    }

    health_boundary = {
        "boundary_id": "decision_center_health_boundary_v1",
        "rules": [
            "missing health_refs → not_ready / health_review_candidate",
            "stale context → requires_observation",
            "low confidence → not_ready / requires_observation",
            "P0 safety unresolved → blocked or hold",
            "health_fault context → handoff to Health Watchdog later",
            "no real health runtime enabled",
        ],
        **meta,
    }

    ii_dependency_boundary = {
        "boundary_id": "decision_center_information_integration_dependency_boundary_v1",
        "rules": [
            "Decision Center may only consume midplatform_information_integration_foundation_v1 frozen candidate outputs",
            "must not redefine Information Integration",
            "must not modify Information Integration candidate types",
            "must not treat decision_context_candidate as final decision",
            "must not require Information Integration to enable runtime",
            "new fields require change_control via information_integration_change_control_policy",
        ],
        **meta,
    }

    downstream_handoff = {
        "matrix_id": "decision_center_downstream_handoff_matrix_v1",
        "handoffs": list(DOWNSTREAM_HANDOFFS),
        "direct_mount_executed": False,
        **meta,
    }

    sample_flow_plan = {
        "plan_id": "decision_center_sample_flow_plan_v1",
        "flows": list(SAMPLE_FLOWS),
        "flow_count": len(SAMPLE_FLOWS),
        **meta,
    }

    failure_matrix = {
        "matrix_id": "decision_center_failure_route_matrix_v1",
        "routes": list(FAILURE_ROUTES),
        "route_count": len(FAILURE_ROUTES),
        **meta,
    }

    health_metric_scope = {
        "scope_id": "decision_center_mount_health_metric_scope_v1",
        "metrics": list(HEALTH_METRICS),
        "metric_count": len(HEALTH_METRICS),
        "real_health_runtime_enabled": False,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "decision_center_boundary_matrix_v1",
        "global_boundaries": {f: False for f in BOUNDARY_FALSE},
        **meta,
    }

    mount_non_claims = {
        "register_id": "decision_center_mount_non_claims_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    planning_pass = len(blockers) == 0
    readiness = {
        "decision_id": "decision_center_mount_readiness_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "ii_foundation_consumed": True,
        "must_not_redefine_ii": True,
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
        "module_id": "decision_center",
        "layer": "L7",
        **meta,
    }

    return {
        "summary": summary,
        "decision_center_mount_scope": mount_scope,
        "decision_center_mount_contract": mount_contract,
        "decision_center_input_contract": input_contract,
        "decision_center_output_contract": output_contract,
        "decision_center_processing_model": processing_model,
        "decision_center_decision_state_machine": decision_state_machine,
        "decision_center_model_rule_algorithm_placement": mra_placement,
        "decision_center_governance_boundary": governance_boundary,
        "decision_center_health_boundary": health_boundary,
        "decision_center_information_integration_dependency_boundary": ii_dependency_boundary,
        "decision_center_downstream_handoff_matrix": downstream_handoff,
        "decision_center_sample_flow_plan": sample_flow_plan,
        "decision_center_failure_route_matrix": failure_matrix,
        "decision_center_mount_health_metric_scope": health_metric_scope,
        "decision_center_boundary_matrix": boundary_matrix,
        "decision_center_mount_non_claims": mount_non_claims,
        "decision_center_mount_readiness_decision": readiness,
    }
