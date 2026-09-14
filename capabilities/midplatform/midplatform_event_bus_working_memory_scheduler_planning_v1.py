# -*- coding: utf-8 -*-
"""Luna Midplatform Micro-OS Event Bus / Working Memory / Scheduler Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_micro_os_architecture_planning_v1 import HEALTH_METRICS, PRIORITY_LEVELS
from capabilities.midplatform.midplatform_micro_os_core_component_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CORE_COMPONENT_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as CORE_COMPONENT_DRYRUN_NEXT,
)

PHASE_ID = "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Planning-v1-001"
SCOPE = "midplatform_event_bus_working_memory_scheduler_planning_only"
SOURCE_CHAIN = "midplatform_event_bus_working_memory_scheduler_planning_v1"

UPSTREAM_CORE_DRYRUN_FINAL = CORE_COMPONENT_DRYRUN_FINAL_GO
UPSTREAM_CORE_DRYRUN_NEXT = CORE_COMPONENT_DRYRUN_NEXT

FINAL_DECISION_GO = "MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Issue-Review-v1-001"

EVENT_BUS_FIELDS: Tuple[str, ...] = (
    "event_id", "event_type", "source_module", "source_chain", "timestamp",
    "spatial_anchor_ref", "missing_spatial_anchor", "candidate_payload_ref",
    "health_tag", "priority_hint", "ttl_hint", "governance_required",
    "routing_targets", "event_state", "trace_id",
)

WORKING_MEMORY_FIELDS: Tuple[str, ...] = (
    "working_memory_entry_id", "event_ref", "candidate_ref", "task_ref",
    "spatiotemporal_slot_ref", "priority_class", "state", "ttl", "freshness_status",
    "confirmation_status", "conflict_refs", "gap_refs", "health_refs",
    "downstream_refs", "admission_candidate_refs", "cleanup_policy", "trace_id",
)

SCHEDULER_FIELDS: Tuple[str, ...] = (
    "scheduling_request_id", "event_ref", "working_memory_entry_ref", "priority_class",
    "task_relevance", "survival_relevance", "health_status", "resource_status",
    "ttl_status", "blockage_status", "preemption_allowed", "defer_allowed",
    "drop_allowed", "routing_decision", "scheduling_state", "trace_id",
)

EVENT_TYPES: Tuple[str, ...] = (
    "module_candidate_event",
    "user_goal_event",
    "drive_signal_event",
    "health_report_event",
    "resource_state_event",
    "worldmodel_recall_event",
    "memory_recall_event",
    "output_candidate_event",
    "recovery_candidate_event",
    "governance_check_event",
    "ttl_expiry_event",
    "task_state_event",
)

EVENT_STATES: Tuple[str, ...] = (
    "received", "normalized", "governance_pending", "health_pending", "queued",
    "stored_in_working_memory", "scheduled", "routed", "completed",
    "expired", "discarded", "blocked", "failed",
)

WM_ENTRY_STATES: Tuple[str, ...] = (
    "new", "active", "pending_confirmation", "integrated", "allocated",
    "waiting_downstream", "stale", "expired", "discarded", "confirmed",
    "admission_candidate_generated", "blocked",
)

TTL_POLICIES: Tuple[Dict[str, Any], ...] = (
    {"priority": "P0", "name": "safety", "ttl": "very_short", "on_expire": "re_observe_required"},
    {"priority": "P1", "name": "active_task", "ttl": "short", "on_expire": "task_phase_revalidate"},
    {"priority": "P2", "name": "conversation", "ttl": "short_medium", "on_expire": "discard_or_reconfirm"},
    {"priority": "P3", "name": "scene_continuity", "ttl": "medium", "on_expire": "stale_then_reobserve"},
    {"priority": "P4", "name": "memory_worldmodel_candidate", "ttl": "task_level", "on_expire": "admission_later_or_discard"},
    {"priority": "P5", "name": "background", "ttl": "low", "on_expire": "discard_or_compress"},
)

FAILURE_ROUTES: Tuple[Dict[str, Any], ...] = (
    {"route_id": "event_schema_invalid", "component": "event_bus", "detection_signal": "schema_invalid_count", "default_response": "discard_event", "recovery_candidate": "governance_revalidate"},
    {"route_id": "event_missing_source_chain", "component": "event_bus", "detection_signal": "missing_source_chain", "default_response": "block_event", "recovery_candidate": "adapter_reemit"},
    {"route_id": "event_missing_timestamp", "component": "event_bus", "detection_signal": "missing_timestamp", "default_response": "block_event", "recovery_candidate": "clock_sync_hint"},
    {"route_id": "event_missing_health_tag", "component": "event_bus", "detection_signal": "health_tag_missing_count", "default_response": "hold_or_degraded", "recovery_candidate": "health_retag"},
    {"route_id": "event_bus_queue_backlog", "component": "event_bus", "detection_signal": "queue_backlog", "default_response": "drop_p5_defer_p3_p4", "recovery_candidate": "queue_drain"},
    {"route_id": "working_memory_ttl_missing", "component": "working_memory", "detection_signal": "ttl_violation_count", "default_response": "reject_entry", "recovery_candidate": "enforce_ttl_policy"},
    {"route_id": "working_memory_entry_stale", "component": "working_memory", "detection_signal": "stale_candidate_count", "default_response": "mark_stale_expire", "recovery_candidate": "re_ingest"},
    {"route_id": "working_memory_long_pending", "component": "working_memory", "detection_signal": "long_pending_candidate", "default_response": "hold_review", "recovery_candidate": "watchdog_escalation"},
    {"route_id": "scheduler_priority_conflict", "component": "scheduler", "detection_signal": "priority_conflict", "default_response": "governance_arbitrate", "recovery_candidate": "reschedule"},
    {"route_id": "scheduler_p0_starvation_forbidden", "component": "scheduler", "detection_signal": "p0_starvation_risk", "default_response": "force_p0_preempt", "recovery_candidate": "watchdog_alert"},
    {"route_id": "scheduler_resource_overload", "component": "scheduler", "detection_signal": "resource_overload", "default_response": "degraded_mode", "recovery_candidate": "health_clearance"},
    {"route_id": "scheduler_routing_failed", "component": "scheduler", "detection_signal": "routing_failed", "default_response": "hold_mode", "recovery_candidate": "kernel_reorchestrate"},
)

HEALTH_METRIC_EB_WM_SCHED_MAP: Dict[str, str] = {
    "core_bus_operational": "event_bus",
    "event_loop_active": "event_bus",
    "queue_processing_active": "event_bus+scheduler",
    "queue_backlog": "event_bus+scheduler",
    "pending_candidate_count": "working_memory",
    "stale_candidate_count": "working_memory",
    "ttl_violation_count": "working_memory",
    "long_pending_task_count": "scheduler",
    "health_tag_missing_count": "event_bus+health_manager",
    "schema_invalid_count": "event_bus+governance_gate",
    "latency": "event_bus",
    "fallback_trigger_count": "scheduler+health_manager",
    "degraded_mode_active": "scheduler+watchdog",
}

SAMPLE_FLOWS: Tuple[Dict[str, Any], ...] = (
    {
        "flow_id": "navigation_safety_preemption_flow",
        "priority": "P0",
        "states": [
            {"component": "event_bus", "state": "received"},
            {"component": "event_bus", "state": "governance_pending"},
            {"component": "working_memory", "state": "new"},
            {"component": "scheduler", "state": "preemption_allowed"},
            {"component": "event_bus", "state": "routed"},
        ],
    },
    {
        "flow_id": "ocr_pending_confirmation_flow",
        "priority": "P2",
        "states": [
            {"component": "event_bus", "state": "normalized"},
            {"component": "working_memory", "state": "pending_confirmation"},
            {"component": "scheduler", "state": "defer_allowed"},
            {"component": "working_memory", "state": "confirmed"},
        ],
    },
    {
        "flow_id": "health_fault_degraded_flow",
        "priority": "P0",
        "states": [
            {"component": "event_bus", "state": "health_pending"},
            {"component": "working_memory", "state": "blocked"},
            {"component": "scheduler", "state": "drop_allowed"},
            {"component": "scheduler", "routing": "recovery_candidate"},
        ],
    },
    {
        "flow_id": "memory_recall_reuse_flow",
        "priority": "P4",
        "states": [
            {"component": "event_bus", "event_type": "memory_recall_event"},
            {"component": "working_memory", "state": "active"},
            {"component": "scheduler", "state": "defer_allowed"},
            {"component": "working_memory", "state": "admission_candidate_generated"},
        ],
    },
)

NON_CLAIMS: Tuple[str, ...] = (
    "EB/WM/Scheduler Planning ≠ real Event Bus enabled",
    "EB/WM/Scheduler Planning ≠ real Working Memory enabled",
    "EB/WM/Scheduler Planning ≠ real Scheduler enabled",
    "EB/WM/Scheduler Planning ≠ runtime enabled",
    "EB/WM/Scheduler Planning ≠ model invoked",
    "EB/WM/Scheduler Planning ≠ provider invoked",
    "EB/WM/Scheduler Planning ≠ task execution",
    "EB/WM/Scheduler Planning ≠ Memory / WorldModel write",
    "EB/WM/Scheduler Planning ≠ user output",
    "EB/WM/Scheduler Planning ≠ real recovery executed",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("midplatform_event_bus_working_memory_scheduler_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
    "runtime_enabled_now",
    "model_invoked_now",
    "provider_invoked_now",
    "task_execution_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "real_health_monitoring_enabled_now",
    "recovery_executed_now",
    "module_runtime_modified_now",
)

ARCH_UPSTREAM_FILES: Tuple[str, ...] = (
    "midplatform_micro_os_layer_architecture_v1.json",
    "midplatform_information_lifecycle_v1.json",
    "midplatform_priority_and_scheduling_policy_v1.json",
    "midplatform_working_memory_policy_v1.json",
    "midplatform_health_metric_scope_v1.json",
    "midplatform_failure_mode_matrix_v1.json",
    "midplatform_degraded_and_recovery_mode_policy_v1.json",
)

CORE_UPSTREAM_FILES: Tuple[str, ...] = (
    "midplatform_core_component_contract_collection_v1.json",
    "midplatform_core_component_upstream_downstream_matrix_v1.json",
    "midplatform_core_component_information_contract_v1.json",
    "midplatform_core_component_management_logic_v1.json",
    "midplatform_core_component_model_rule_algorithm_map_v1.json",
    "midplatform_core_component_failure_route_matrix_v1.json",
    "midplatform_core_component_health_metric_mapping_v1.json",
)

DEFAULT_ARCH_PLANNING = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_architecture_planning"
DEFAULT_ARCH_DRYRUN = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_architecture_dryrun_and_review"
DEFAULT_CORE_PLANNING = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_core_component_planning"
DEFAULT_CORE_DRYRUN = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_core_component_dryrun_and_review"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_event_bus_working_memory_scheduler_planning"


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
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


def run_midplatform_event_bus_working_memory_scheduler_planning_v1(
    *,
    midplatform_micro_os_architecture_planning_root: str,
    midplatform_micro_os_architecture_dryrun_and_review_root: str,
    midplatform_micro_os_core_component_planning_root: str,
    midplatform_micro_os_core_component_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    arch_plan = Path(midplatform_micro_os_architecture_planning_root).expanduser().resolve()
    arch_dr = Path(midplatform_micro_os_architecture_dryrun_and_review_root).expanduser().resolve()
    core_plan = Path(midplatform_micro_os_core_component_planning_root).expanduser().resolve()
    core_dr = Path(midplatform_micro_os_core_component_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "output_root": str(out_root),
        "upstream_architecture_planning_root": str(arch_plan),
        "upstream_architecture_dryrun_root": str(arch_dr),
        "upstream_core_component_planning_root": str(core_plan),
        "upstream_core_component_dryrun_root": str(core_dr),
    }

    arch_vr = _try_read_json(arch_plan / "verifier_report.json") or {}
    arch_dr_vr = _try_read_json(arch_dr / "verifier_report.json") or {}
    core_vr = _try_read_json(core_plan / "verifier_report.json") or {}
    core_dr_vr = _try_read_json(core_dr / "verifier_report.json") or {}
    core_dr_sm = _try_read_json(core_dr / "summary.json") or {}
    core_dr_ready = _try_read_json(core_dr / "core_component_dryrun_readiness_decision_v1.json") or {}

    if arch_vr.get("verifier") != "GO":
        blockers.append("architecture planning verifier must be GO")
    if arch_dr_vr.get("verifier") != "GO":
        blockers.append("architecture dryrun verifier must be GO")
    if core_vr.get("verifier") != "GO":
        blockers.append("core component planning verifier must be GO")
    if core_dr_vr.get("verifier") != "GO":
        blockers.append("core component dryrun verifier must be GO")
    if core_dr_sm.get("final_decision") != UPSTREAM_CORE_DRYRUN_FINAL:
        blockers.append("core component dryrun final_decision mismatch")
    if core_dr_ready.get("dryrun_pass") is not True:
        blockers.append("core_component_dryrun_readiness must pass")

    for fname in ARCH_UPSTREAM_FILES:
        if _try_read_json(arch_plan / fname) is None:
            blockers.append(f"missing architecture upstream: {fname}")
    for fname in CORE_UPSTREAM_FILES:
        if _try_read_json(core_plan / fname) is None:
            blockers.append(f"missing core component upstream: {fname}")

    event_bus_contract = {
        "contract_id": "event_bus_contract_v1",
        "component_id": "event_bus",
        "layer": "L3",
        "required_fields": list(EVENT_BUS_FIELDS),
        "inputs": ["standardized_candidate", "signal", "health_report", "feedback"],
        "outputs": ["event", "working_memory_entry_ref", "scheduler_notification", "health_notification"],
        "responsibilities": [
            "receive and normalize events",
            "route to Working Memory and Scheduler",
            "notify Health & Resource Manager",
            "preserve trace_id",
        ],
        "forbidden": [
            "semantic arbitration",
            "rewrite candidate content",
            "generate facts",
            "bypass governance",
        ],
        **meta,
    }

    event_type_registry = {
        "registry_id": "event_type_registry_v1",
        "event_types": list(EVENT_TYPES),
        "event_type_count": len(EVENT_TYPES),
        **meta,
    }

    event_state_machine = {
        "machine_id": "event_state_machine_v1",
        "states": list(EVENT_STATES),
        "state_count": len(EVENT_STATES),
        "initial_state": "received",
        "terminal_states": ["completed", "expired", "discarded", "failed"],
        **meta,
    }

    working_memory_contract = {
        "contract_id": "working_memory_contract_v1",
        "component_id": "working_memory",
        "layer": "L3",
        "required_fields": list(WORKING_MEMORY_FIELDS),
        "working_memory_is_not_memory": True,
        "working_memory_is_not_worldmodel": True,
        "responsibilities": [
            "store runtime candidates and task/world snapshots",
            "track pending/conflict/gap/health entries",
            "support TTL stale expired discarded confirmed states",
            "support task switch/resume short-term reads",
        ],
        "forbidden": ["long_term_deposit", "write_fact", "substitute_memory_or_worldmodel"],
        **meta,
    }

    wm_entry_state_machine = {
        "machine_id": "working_memory_entry_state_machine_v1",
        "states": list(WM_ENTRY_STATES),
        "state_count": len(WM_ENTRY_STATES),
        "initial_state": "new",
        **meta,
    }

    wm_ttl_policy = {
        "policy_id": "working_memory_ttl_and_cleanup_policy_v1",
        "no_ttl_forbidden": True,
        "priority_ttl_policies": list(TTL_POLICIES),
        "cleanup_rules": ["expire_by_ttl", "compress_p5", "admission_candidate_on_confirm", "never_write_fact"],
        **meta,
    }

    scheduler_contract = {
        "contract_id": "scheduler_contract_v1",
        "component_id": "scheduler",
        "layers": ["L5", "L6"],
        "required_fields": list(SCHEDULER_FIELDS),
        "responsibilities": [
            "assign P0-P5 priority",
            "P0 preempts P1-P5",
            "P1 not blocked by P3/P4/P5",
            "P5 discard or defer",
            "P0/P1 long pending triggers watchdog",
            "route to Task Manager / Integration / Output Bridge / Watchdog",
        ],
        "forbidden": ["direct_task_execution", "direct_runtime_call", "direct_user_output"],
        **meta,
    }

    priority_queue_policy = {
        "policy_id": "priority_queue_policy_v1",
        "queues": list(PRIORITY_LEVELS),
        "queue_count": len(PRIORITY_LEVELS),
        **meta,
    }

    preemption_policy = {
        "policy_id": "preemption_and_deferral_policy_v1",
        "rules": [
            "P0 preempts all",
            "P1 protected from P3/P4/P5 blocking",
            "P3/P4 defer under load",
            "P5 discard first",
            "health_unknown conservative default",
            "resource_overload degraded mode",
            "cloud_unavailable local takeover",
            "model_unavailable fallback or hold",
        ],
        **meta,
    }

    interaction_model = {
        "model_id": "event_bus_working_memory_scheduler_interaction_model_v1",
        "cycle": [
            "Module Adapter → Event Bus (standardized_candidate)",
            "Event Bus → Working Memory (working_memory_entry)",
            "Event Bus → Scheduler (scheduling_request)",
            "Scheduler → Task Manager / Integration / Output Bridge / Watchdog",
            "Watchdog → Scheduler (recovery_candidate)",
            "Event Bus retains trace loop",
        ],
        "edges": [
            {"from": "event_bus", "to": "working_memory", "payload": "event"},
            {"from": "event_bus", "to": "scheduler", "payload": "priority_hint"},
            {"from": "working_memory", "to": "scheduler", "payload": "working_memory_entry_ref"},
            {"from": "scheduler", "to": "event_bus", "payload": "routing_decision"},
        ],
        **meta,
    }

    health_mapping = {
        "mapping_id": "eb_wm_scheduler_health_metric_mapping_v1",
        "metric_to_component": HEALTH_METRIC_EB_WM_SCHED_MAP,
        "covers_event_bus": True,
        "covers_working_memory": True,
        "covers_scheduler": True,
        "scheduler_queue_processing_shared": True,
        **meta,
    }

    failure_matrix = {
        "matrix_id": "eb_wm_scheduler_failure_route_matrix_v1",
        "routes": list(FAILURE_ROUTES),
        "route_count": len(FAILURE_ROUTES),
        **meta,
    }

    governance_boundary = {
        "boundary_id": "eb_wm_scheduler_governance_boundary_v1",
        "rules": [
            "Event Bus blocks high-risk events without governance clearance",
            "Working Memory never promotes candidate to fact",
            "Scheduler never bypasses Governance Gate",
            "Scheduler never directly executes runtime",
            "output/memory/worldmodel writes only via L7 Gate/Admission",
            "L0 constrains all three foundation components",
        ],
        "l0_global_constraint": True,
        **meta,
    }

    sample_flow_plan = {
        "plan_id": "eb_wm_scheduler_sample_flow_plan_v1",
        "flows": list(SAMPLE_FLOWS),
        "flow_count": len(SAMPLE_FLOWS),
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "eb_wm_scheduler_boundary_matrix_v1",
        "foundation_components": {
            "event_bus": {f: False for f in BOUNDARY_FALSE},
            "working_memory": {f: False for f in BOUNDARY_FALSE},
            "scheduler": {f: False for f in BOUNDARY_FALSE},
        },
        "global_boundaries": {f: False for f in BOUNDARY_FALSE},
        **meta,
    }

    planning_pass = len(blockers) == 0
    readiness = {
        "decision_id": "eb_wm_scheduler_planning_readiness_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "foundation_triad_complete": True,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "foundation_components": ["event_bus", "working_memory", "scheduler"],
        "planning_pass": planning_pass,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    return {
        "summary": summary,
        "event_bus_contract": event_bus_contract,
        "event_type_registry": event_type_registry,
        "event_state_machine": event_state_machine,
        "working_memory_contract": working_memory_contract,
        "working_memory_entry_state_machine": wm_entry_state_machine,
        "working_memory_ttl_and_cleanup_policy": wm_ttl_policy,
        "scheduler_contract": scheduler_contract,
        "priority_queue_policy": priority_queue_policy,
        "preemption_and_deferral_policy": preemption_policy,
        "event_bus_working_memory_scheduler_interaction_model": interaction_model,
        "eb_wm_scheduler_health_metric_mapping": health_mapping,
        "eb_wm_scheduler_failure_route_matrix": failure_matrix,
        "eb_wm_scheduler_governance_boundary": governance_boundary,
        "eb_wm_scheduler_sample_flow_plan": sample_flow_plan,
        "eb_wm_scheduler_boundary_matrix": boundary_matrix,
        "eb_wm_scheduler_planning_readiness_decision": readiness,
        "eb_wm_scheduler_non_claims_register": {
            "register_id": "eb_wm_scheduler_non_claims_register_v1",
            "non_claims": list(NON_CLAIMS),
            **meta,
        },
    }
