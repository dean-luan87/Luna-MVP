# -*- coding: utf-8 -*-
"""Luna Midplatform Information Integration Mount Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_module_definition_template_v1 import TEMPLATE_SECTIONS
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FREEZE_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as FREEZE_DRYRUN_NEXT,
)
from capabilities.midplatform.midplatform_micro_os_foundation_freeze_and_handoff_planning_v1 import (
    FROZEN_INTERFACE_FUNCTIONS,
    FROZEN_TYPES,
)

PHASE_ID = "Phase-Midplatform-Information-Integration-Mount-Planning-v1-001"
SCOPE = "midplatform_information_integration_mount_planning_only"
SOURCE_CHAIN = "midplatform_information_integration_mount_planning_v1"

UPSTREAM_FREEZE_DRYRUN_FINAL = FREEZE_DRYRUN_FINAL_GO
UPSTREAM_FREEZE_DRYRUN_NEXT = FREEZE_DRYRUN_NEXT

FINAL_DECISION_GO = "MIDPLATFORM_INFORMATION_INTEGRATION_MOUNT_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_INFORMATION_INTEGRATION_MOUNT_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Information-Integration-Mount-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Information-Integration-Mount-Issue-Review-v1-001"

UPSTREAM_FREEZE_DRYRUN_FILES: Tuple[str, ...] = (
    "freeze_dryrun_readiness_decision_v1.json",
    "summary.json",
    "verifier_report.json",
)

UPSTREAM_FREEZE_PLANNING_FILES: Tuple[str, ...] = (
    "micro_os_foundation_version_tag_v1.json",
    "micro_os_foundation_frozen_interface_v1.json",
    "micro_os_foundation_handoff_contract_v1.json",
    "micro_os_foundation_allowed_mount_points_v1.json",
    "micro_os_foundation_forbidden_mutation_policy_v1.json",
    "micro_os_foundation_change_control_policy_v1.json",
    "micro_os_foundation_downstream_readiness_matrix_v1.json",
    "micro_os_foundation_health_and_boundary_freeze_v1.json",
    "micro_os_foundation_route_decision_v1.json",
)

FROZEN_INTERFACE_CONSUMED: Tuple[str, ...] = (
    "Event",
    "EventType",
    "EventState",
    "WorkingMemoryEntry",
    "WorkingMemoryEntryState",
    "PriorityClass",
    "SchedulingRequest",
    "SchedulingDecisionCandidate",
    "normalize_event",
    "validate_event_schema",
    "create_working_memory_entry",
    "validate_wm_entry",
    "assign_priority_candidate",
    "produce_scheduling_decision_candidate",
    "validate_no_runtime_flags",
    "validate_candidate_not_fact",
    "validate_required_trace",
    "validate_required_health_tag",
    "validate_required_ttl",
    "validate_governance_guard",
)

INPUT_TYPES: Tuple[str, ...] = (
    "Event",
    "WorkingMemoryEntry",
    "SchedulingDecisionCandidate",
    "spatiotemporal_slot_ref",
    "task_state_snapshot",
    "drive_signal_candidate",
    "health_report_candidate",
    "resource_state_candidate",
    "worldmodel_recall_context",
    "memory_recall_context",
    "governance_check_ref",
    "trace_ref",
)

INPUT_REQUIRED_FIELDS: Tuple[str, ...] = (
    "trace",
    "health_tag",
    "ttl",
    "source_chain",
    "candidate_not_fact",
)

OUTPUT_CANDIDATES: Tuple[str, ...] = (
    "live_world_state_candidate",
    "task_world_slice_candidate",
    "priority_attention_map_candidate",
    "information_allocation_candidate",
    "conflict_candidate",
    "gap_candidate",
    "required_observation_candidate",
    "decision_context_candidate",
    "frontend_guidance_candidate",
    "memory_admission_candidate",
    "worldmodel_admission_candidate",
    "downstream_handoff_candidate",
)

PROCESSING_STEPS: Tuple[str, ...] = (
    "collect eligible working memory entries",
    "group by spatiotemporal slot",
    "apply task / drive relevance",
    "apply health / governance filters",
    "detect conflict / gap",
    "build live world state candidate",
    "extract task world slice candidate",
    "allocate information to downstream paths",
    "produce decision context candidate",
)

INTEGRATION_STATES: Tuple[str, ...] = (
    "integration_candidate",
    "pending_confirmation",
    "blocked",
    "invalid",
    "ready_for_decision_context",
)

MODEL_USES: Tuple[str, ...] = (
    "complex_semantic_integration",
    "task_relevance_explanation",
    "conflict_gap_semantic_explanation",
    "task_world_slice_candidate_generation",
    "decision_context_candidate_draft",
)

RULE_USES: Tuple[str, ...] = (
    "candidate_fact_boundary",
    "p0_p1_hard_priority",
    "no_output_no_write_no_runtime",
    "governance_guard",
    "health_missing_conservative",
    "ttl_missing_block",
    "recall_must_not_override_realtime_safety",
)

ALGORITHM_USES: Tuple[str, ...] = (
    "relevance_scoring",
    "confidence_aggregation",
    "freshness_ttl",
    "conflict_detection",
    "slot_grouping",
    "allocation_ranking",
)

DOWNSTREAM_HANDOFFS: Tuple[Dict[str, Any], ...] = (
    {"target": "decision_center", "payload": "decision_context_candidate", "mount_now": False},
    {"target": "task_manager", "payload": "task_world_slice_candidate", "mount_now": False},
    {"target": "task_manager", "payload": "required_observation_candidate", "mount_now": False},
    {"target": "drive_manager", "payload": "priority_attention_map", "mount_now": False},
    {"target": "output_gate", "payload": "output_candidate", "mount_now": False},
    {"target": "health_watchdog", "payload": "health_issue_candidate", "mount_now": False},
    {"target": "worldmodel_memory_bridge", "payload": "admission_candidate", "mount_now": False},
    {"target": "module_adapter", "payload": "frontend_guidance_candidate", "mount_now": False},
)

SAMPLE_FLOWS: Tuple[Dict[str, Any], ...] = (
    {
        "flow_id": "navigation_information_integration_flow",
        "inputs": ["Event", "WorkingMemoryEntry", "SchedulingDecisionCandidate"],
        "outputs": ["task_world_slice_candidate", "decision_context_candidate"],
        "blocked_paths": ["user_output", "memory_write", "runtime_execution"],
    },
    {
        "flow_id": "ocr_reading_information_integration_flow",
        "inputs": ["Event", "WorkingMemoryEntry"],
        "outputs": ["required_observation_candidate", "decision_context_candidate"],
        "blocked_paths": ["direct_output", "fact_promotion"],
    },
    {
        "flow_id": "health_fault_information_integration_flow",
        "inputs": ["health_report_candidate", "WorkingMemoryEntry"],
        "outputs": ["priority_attention_map_candidate", "conflict_candidate"],
        "blocked_paths": ["task_execution", "runtime_bypass"],
    },
    {
        "flow_id": "memory_recall_reuse_flow",
        "inputs": ["memory_recall_context", "WorkingMemoryEntry"],
        "outputs": ["live_world_state_candidate", "memory_admission_candidate"],
        "blocked_paths": ["worldmodel_write", "safety_override"],
    },
    {
        "flow_id": "conflict_gap_detection_flow",
        "inputs": ["WorkingMemoryEntry", "SchedulingDecisionCandidate"],
        "outputs": ["conflict_candidate", "gap_candidate", "required_observation_candidate"],
        "blocked_paths": ["decision_without_resolution", "user_output"],
    },
)

FAILURE_ROUTES: Tuple[Dict[str, Any], ...] = (
    {"route_id": "missing_trace", "detection_signal": "missing_trace_count", "default_response": "block_entry", "recovery_or_hold_candidate": "trace_repair", "forbidden_shortcut": "process_without_trace"},
    {"route_id": "missing_health_tag", "detection_signal": "health_tag_missing_count", "default_response": "health_issue_candidate", "recovery_or_hold_candidate": "health_retag", "forbidden_shortcut": "assume_healthy"},
    {"route_id": "ttl_missing", "detection_signal": "ttl_violation_count", "default_response": "block_entry", "recovery_or_hold_candidate": "enforce_ttl", "forbidden_shortcut": "infinite_ttl"},
    {"route_id": "stale_working_memory_entry", "detection_signal": "stale_entry_count", "default_response": "reobserve_candidate", "recovery_or_hold_candidate": "re_ingest", "forbidden_shortcut": "treat_stale_as_fresh"},
    {"route_id": "unresolved_conflict", "detection_signal": "unresolved_conflict_count", "default_response": "hold", "recovery_or_hold_candidate": "conflict_resolution", "forbidden_shortcut": "force_decision"},
    {"route_id": "low_confidence_input", "detection_signal": "low_confidence_count", "default_response": "pending_confirmation", "recovery_or_hold_candidate": "required_observation", "forbidden_shortcut": "auto_confirm"},
    {"route_id": "governance_ref_missing_for_high_risk", "detection_signal": "governance_missing", "default_response": "blocked", "recovery_or_hold_candidate": "governance_check", "forbidden_shortcut": "bypass_governance"},
    {"route_id": "worldmodel_recall_conflicts_with_realtime_safety", "detection_signal": "recall_safety_conflict", "default_response": "prefer_realtime", "recovery_or_hold_candidate": "reobserve", "forbidden_shortcut": "recall_overrides_p0"},
    {"route_id": "output_route_attempted_before_decision", "detection_signal": "premature_output", "default_response": "block_output", "recovery_or_hold_candidate": "decision_context_first", "forbidden_shortcut": "direct_user_output"},
    {"route_id": "memory_write_attempted", "detection_signal": "memory_write_attempt", "default_response": "block_write", "recovery_or_hold_candidate": "admission_candidate_only", "forbidden_shortcut": "direct_memory_write"},
    {"route_id": "worldmodel_write_attempted", "detection_signal": "worldmodel_write_attempt", "default_response": "block_write", "recovery_or_hold_candidate": "admission_candidate_only", "forbidden_shortcut": "direct_worldmodel_write"},
    {"route_id": "model_invocation_attempted_now", "detection_signal": "model_invoked_now", "default_response": "hold_planning", "recovery_or_hold_candidate": "mount_dryrun_first", "forbidden_shortcut": "invoke_model_in_mount_planning"},
)

HEALTH_METRICS: Tuple[str, ...] = (
    "integration_input_count",
    "eligible_entry_count",
    "blocked_entry_count",
    "stale_entry_count",
    "missing_health_tag_count",
    "missing_trace_count",
    "conflict_candidate_count",
    "unresolved_conflict_count",
    "gap_candidate_count",
    "decision_context_candidate_count",
    "integration_latency_candidate",
    "allocation_candidate_count",
    "reobserve_candidate_count",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Mount Planning ≠ Information Integration implemented",
    "Mount Planning ≠ mounted now",
    "Mount Planning ≠ runtime enabled",
    "Mount Planning ≠ model invoked",
    "Mount Planning ≠ Decision Center ready",
    "Mount Planning ≠ Task Manager ready",
    "Mount Planning ≠ Output allowed",
    "Mount Planning ≠ Memory / WorldModel write",
    "Mount Planning ≠ full information integration pipeline",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_information_integration_mount_planning_only",
    "mount_planning_only",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "information_integration_mounted_now",
    "information_integration_runtime_enabled_now",
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
    "model_invoked_now",
    "provider_invoked_now",
    "runtime_enabled_now",
    "task_execution_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "output_gate_mounted_now",
    "decision_center_mounted_now",
    "health_watchdog_mounted_now",
)

DEFAULT_FREEZE_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_FREEZE_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_planning"
)
DEFAULT_POST_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_mount_planning"


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "foundation_id": "midplatform_micro_os_foundation_v1",
        "foundation_version": "1.0.0-skeleton",
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
    contract: Dict[str, Any] = {
        "contract_id": "information_integration_mount_contract_v1",
        "module_identity": {
            "module_id": "information_integration",
            "module_name": "Information Integration",
            "layer": "L6",
            "role": "information integration and allocation planning layer",
        },
        "upstream_sources": {
            "sources": ["event_bus", "working_memory", "scheduler", "module_adapter", "health_resource_manager", "worldmodel_memory_bridge"],
            "foundation_id": "midplatform_micro_os_foundation_v1",
        },
        "downstream_targets": {
            "targets": ["decision_center", "task_manager", "drive_manager", "output_gate", "health_watchdog", "worldmodel_memory_bridge", "module_adapter"],
            "candidate_only": True,
        },
        "input_contract": {
            "input_types": list(INPUT_TYPES),
            "required_fields": list(INPUT_REQUIRED_FIELDS),
            "frozen_interface_refs": list(FROZEN_INTERFACE_CONSUMED),
        },
        "processing_scope": {
            "steps": list(PROCESSING_STEPS),
            "planning_only": True,
            "runtime_execution": False,
        },
        "output_contract": {
            "output_types": list(OUTPUT_CANDIDATES),
            "all_candidate": True,
            "fact_status": "candidate_only",
            "write_allowed": False,
            "user_output_allowed": False,
        },
        "module_principles": [
            "consume frozen foundation interfaces only",
            "all outputs are candidates",
            "never promote candidate to fact",
            "never bypass Scheduler or Governance Gate",
        ],
        "external_constraints": {
            "l0_governance": True,
            "foundation_handoff_contract": True,
            "forbidden_mutation_policy": True,
        },
        "runtime_boundaries": {f: False for f in BOUNDARY_FALSE},
        "failure_and_traceability": {
            "failure_route_count": len(FAILURE_ROUTES),
            "trace_required": True,
            "audit_required": True,
        },
        **meta,
    }
    return contract


def run_midplatform_information_integration_mount_planning_v1(
    *,
    midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_planning_root: str,
    midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    freeze_dr = Path(midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root).expanduser().resolve()
    freeze_plan = Path(midplatform_micro_os_foundation_freeze_and_handoff_planning_root).expanduser().resolve()
    post_dr = Path(midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "output_root": str(out_root),
        "upstream_freeze_dryrun_root": str(freeze_dr),
        "upstream_freeze_planning_root": str(freeze_plan),
        "upstream_post_dryrun_root": str(post_dr),
    }

    freeze_dr_vr = _try_read_json(freeze_dr / "verifier_report.json") or {}
    freeze_dr_sm = _try_read_json(freeze_dr / "summary.json") or {}
    freeze_ready = _try_read_json(freeze_dr / "freeze_dryrun_readiness_decision_v1.json") or {}

    if freeze_dr_vr.get("verifier") != "GO":
        blockers.append("upstream freeze dryrun verifier must be GO")
    if freeze_dr_sm.get("final_decision") != UPSTREAM_FREEZE_DRYRUN_FINAL:
        blockers.append("upstream freeze dryrun final_decision mismatch")
    if freeze_ready.get("dryrun_pass") is not True:
        blockers.append("upstream freeze_dryrun_readiness must pass")

    upstream: Dict[str, Any] = {}
    for fname in UPSTREAM_FREEZE_DRYRUN_FILES + UPSTREAM_FREEZE_PLANNING_FILES:
        root = freeze_dr if fname in UPSTREAM_FREEZE_DRYRUN_FILES else freeze_plan
        data = _try_read_json(root / fname)
        if data is None:
            blockers.append(f"missing upstream: {fname}")
        upstream[fname.replace("_v1.json", "").replace(".json", "")] = data

    version_tag = upstream.get("micro_os_foundation_version_tag") or {}
    route_dec = upstream.get("micro_os_foundation_route_decision") or {}
    frozen_iface = upstream.get("micro_os_foundation_frozen_interface") or {}

    if version_tag.get("foundation_id") != "midplatform_micro_os_foundation_v1":
        blockers.append("foundation_id mismatch")
    if version_tag.get("runtime_status") != "not_enabled":
        blockers.append("foundation runtime must be not_enabled")
    if route_dec.get("primary_next_phase") != "Phase-Midplatform-Information-Integration-Mount-Planning-v1-001":
        blockers.append("Information Integration must be primary route")

    mount_scope = {
        "scope_id": "information_integration_mount_scope_v1",
        "layer": "L6",
        "module_id": "information_integration",
        "frozen_interface_consumed": list(FROZEN_INTERFACE_CONSUMED),
        "frozen_types_consumed": [t for t in FROZEN_INTERFACE_CONSUMED if t[0].isupper()],
        "mount_planning_only": True,
        "direct_mount_executed": False,
        **meta,
    }

    mount_contract = _build_mount_contract(meta)

    input_contract = {
        "contract_id": "information_integration_input_contract_v1",
        "input_types": list(INPUT_TYPES),
        "required_fields": list(INPUT_REQUIRED_FIELDS),
        "core_inputs": ["Event", "WorkingMemoryEntry", "SchedulingDecisionCandidate"],
        **meta,
    }

    output_contract = {
        "contract_id": "information_integration_output_contract_v1",
        "outputs": list(OUTPUT_CANDIDATES),
        "all_candidate": True,
        "forbidden_outputs": ["fact", "runtime_action", "user_output", "memory_write", "worldmodel_write"],
        **meta,
    }

    processing_model = {
        "model_id": "information_integration_processing_model_v1",
        "steps": list(PROCESSING_STEPS),
        "state_machine_states": list(INTEGRATION_STATES),
        "planning_only": True,
        **meta,
    }

    mra_placement = {
        "placement_id": "information_integration_model_rule_algorithm_placement_v1",
        "model_uses": list(MODEL_USES),
        "rule_uses": list(RULE_USES),
        "algorithm_uses": list(ALGORITHM_USES),
        "state_machine_uses": list(INTEGRATION_STATES),
        "no_model_in_mount_planning_now": True,
        "no_runtime_now": True,
        **meta,
    }

    governance_boundary = {
        "boundary_id": "information_integration_governance_boundary_v1",
        "rules": [
            "do not bypass L0",
            "do not bypass Scheduler",
            "do not bypass Working Memory",
            "do not treat candidate as fact",
            "do not write Memory directly",
            "do not write WorldModel directly",
            "do not output directly",
            "do not execute task directly",
            "do not invoke provider/model/runtime in mount planning",
            "high-risk decision_context_candidate requires governance_check_ref",
        ],
        **meta,
    }

    health_boundary = {
        "boundary_id": "information_integration_health_boundary_v1",
        "rules": [
            "missing health_tag → blocked or health_issue_candidate",
            "missing timestamp → invalid or blocked",
            "missing source_chain → invalid or blocked",
            "ttl_missing → blocked",
            "stale candidate → degraded or reobserve candidate",
            "low confidence → pending_confirmation or required_observation_candidate",
            "unresolved conflict → hold or decision_readiness_not_ready",
        ],
        **meta,
    }

    wm_memory_feedback = {
        "boundary_id": "information_integration_worldmodel_memory_feedback_boundary_v1",
        "rules": [
            "recall_context as hint / known_state_candidate / change_detection_reference only",
            "must not override realtime safety information",
            "must not replace required current observation",
            "may reduce duplicate collection",
            "may mark change points",
            "may generate worldmodel_admission_candidate later",
            "may generate memory_admission_candidate later",
        ],
        **meta,
    }

    downstream_handoff = {
        "matrix_id": "information_integration_downstream_handoff_matrix_v1",
        "handoffs": list(DOWNSTREAM_HANDOFFS),
        "direct_mount_executed": False,
        **meta,
    }

    sample_flow_plan = {
        "plan_id": "information_integration_sample_flow_plan_v1",
        "flows": list(SAMPLE_FLOWS),
        "flow_count": len(SAMPLE_FLOWS),
        **meta,
    }

    failure_matrix = {
        "matrix_id": "information_integration_failure_route_matrix_v1",
        "routes": list(FAILURE_ROUTES),
        "route_count": len(FAILURE_ROUTES),
        **meta,
    }

    health_metric_scope = {
        "scope_id": "information_integration_mount_health_metric_scope_v1",
        "metrics": list(HEALTH_METRICS),
        "metric_count": len(HEALTH_METRICS),
        "real_health_runtime_enabled": False,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "information_integration_boundary_matrix_v1",
        "global_boundaries": {f: False for f in BOUNDARY_FALSE},
        **meta,
    }

    mount_non_claims = {
        "register_id": "information_integration_mount_non_claims_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    planning_pass = len(blockers) == 0
    readiness = {
        "decision_id": "information_integration_mount_readiness_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "foundation_consumed": True,
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
        "module_id": "information_integration",
        "layer": "L6",
        **meta,
    }

    return {
        "summary": summary,
        "information_integration_mount_scope": mount_scope,
        "information_integration_mount_contract": mount_contract,
        "information_integration_input_contract": input_contract,
        "information_integration_output_contract": output_contract,
        "information_integration_processing_model": processing_model,
        "information_integration_model_rule_algorithm_placement": mra_placement,
        "information_integration_governance_boundary": governance_boundary,
        "information_integration_health_boundary": health_boundary,
        "information_integration_worldmodel_memory_feedback_boundary": wm_memory_feedback,
        "information_integration_downstream_handoff_matrix": downstream_handoff,
        "information_integration_sample_flow_plan": sample_flow_plan,
        "information_integration_failure_route_matrix": failure_matrix,
        "information_integration_mount_health_metric_scope": health_metric_scope,
        "information_integration_boundary_matrix": boundary_matrix,
        "information_integration_mount_non_claims": mount_non_claims,
        "information_integration_mount_readiness_decision": readiness,
    }
