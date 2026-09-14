# -*- coding: utf-8 -*-
"""Luna Midplatform EB/WM/Scheduler Controlled Skeleton Implementation Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as DRYRUN_NEXT,
)
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_planning_v1 import (
    EVENT_BUS_FIELDS,
    EVENT_STATES,
    EVENT_TYPES,
    SCHEDULER_FIELDS,
    WM_ENTRY_STATES,
    WORKING_MEMORY_FIELDS,
)

PHASE_ID = (
    "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Controlled-Skeleton-Implementation-Planning-v1-001"
)
SCOPE = "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_only"
SOURCE_CHAIN = "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_v1"

UPSTREAM_DRYRUN_FINAL = DRYRUN_FINAL_GO
UPSTREAM_DRYRUN_NEXT = DRYRUN_NEXT

FINAL_DECISION_GO = (
    "MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING_"
    "READY_FOR_IMPLEMENTATION_DRYRUN"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING_"
    "HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Controlled-Skeleton-Implementation-DryRun-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Controlled-Skeleton-Issue-Review-v1-001"
)

UPSTREAM_PLANNING_FILES: Tuple[str, ...] = (
    "event_bus_contract_v1.json",
    "event_type_registry_v1.json",
    "event_state_machine_v1.json",
    "working_memory_contract_v1.json",
    "working_memory_entry_state_machine_v1.json",
    "working_memory_ttl_and_cleanup_policy_v1.json",
    "scheduler_contract_v1.json",
    "priority_queue_policy_v1.json",
    "preemption_and_deferral_policy_v1.json",
    "event_bus_working_memory_scheduler_interaction_model_v1.json",
    "eb_wm_scheduler_health_metric_mapping_v1.json",
    "eb_wm_scheduler_failure_route_matrix_v1.json",
    "eb_wm_scheduler_governance_boundary_v1.json",
    "eb_wm_scheduler_sample_flow_plan_v1.json",
    "eb_wm_scheduler_boundary_matrix_v1.json",
)

UPSTREAM_DRYRUN_FILES: Tuple[str, ...] = (
    "dryrun_readiness_decision_v1.json",
)

SKELETON_FILE_PLAN: Tuple[Dict[str, Any], ...] = (
    {
        "path": "capabilities/midplatform/core/micro_os_common_types_v1.py",
        "purpose": "shared dataclass / enum / TraceRef / HealthTag / GovernanceCheckRef",
        "create_in_this_phase": False,
    },
    {
        "path": "capabilities/midplatform/core/event_bus_skeleton_v1.py",
        "purpose": "Event schema, normalize/validate/route candidate, trace append, static transition validator",
        "create_in_this_phase": False,
    },
    {
        "path": "capabilities/midplatform/core/working_memory_skeleton_v1.py",
        "purpose": "WorkingMemoryEntry schema, TTL/cleanup candidate, stale/expired candidate",
        "create_in_this_phase": False,
    },
    {
        "path": "capabilities/midplatform/core/scheduler_skeleton_v1.py",
        "purpose": "SchedulingRequest schema, priority/preemption/deferral/drop candidate, decision candidate",
        "create_in_this_phase": False,
    },
    {
        "path": "capabilities/midplatform/core/micro_os_static_validators_v1.py",
        "purpose": "cross-component static validators for schema/state/governance/boundary",
        "create_in_this_phase": False,
    },
)

COMMON_TYPES: Tuple[str, ...] = (
    "Event",
    "EventType",
    "EventState",
    "WorkingMemoryEntry",
    "WorkingMemoryEntryState",
    "SchedulingRequest",
    "PriorityClass",
    "TraceRef",
    "HealthTag",
    "TTLPolicyCandidate",
    "GovernanceCheckRef",
    "SchedulingDecisionCandidate",
    "WorkingMemoryEntryCandidate",
    "RouteCandidate",
)

EVENT_BUS_SKELETON_FUNCTIONS: Tuple[str, ...] = (
    "normalize_event",
    "validate_event_schema",
    "route_event_candidate",
    "append_trace",
    "validate_event_state_transition",
)

EVENT_BUS_SKELETON_FORBIDDEN: Tuple[str, ...] = (
    "real_event_loop",
    "async_queue",
    "runtime_connection",
    "module_provider_call",
    "semantic_arbitration",
)

WM_SKELETON_FUNCTIONS: Tuple[str, ...] = (
    "create_working_memory_entry",
    "validate_wm_entry",
    "apply_ttl_policy_candidate",
    "mark_stale_or_expired_candidate",
    "generate_cleanup_plan_candidate",
)

WM_SKELETON_FORBIDDEN: Tuple[str, ...] = (
    "write_memory",
    "write_worldmodel",
    "long_term_persistence",
    "promote_candidate_to_fact",
    "real_cache_service",
)

SCHEDULER_SKELETON_FUNCTIONS: Tuple[str, ...] = (
    "assign_priority_candidate",
    "evaluate_preemption_candidate",
    "evaluate_deferral_or_drop_candidate",
    "produce_scheduling_decision_candidate",
)

SCHEDULER_SKELETON_FORBIDDEN: Tuple[str, ...] = (
    "direct_task_execution",
    "runtime_call",
    "user_output",
    "bypass_governance_gate",
    "worker_thread_async_task",
)

INTERACTION_STEPS: Tuple[str, ...] = (
    "Event received",
    "normalize_event()",
    "validate_event_schema()",
    "create_working_memory_entry() candidate",
    "apply_ttl_policy_candidate()",
    "assign_priority_candidate()",
    "evaluate_preemption_candidate()",
    "produce_scheduling_decision_candidate()",
    "candidate_only_no_real_dispatch",
)

GOVERNANCE_GUARD_RULES: Tuple[str, ...] = (
    "high_risk_event_without_governance_check_ref must produce blocked_candidate",
    "output routes remain forbidden in skeleton",
    "memory routes remain forbidden in skeleton",
    "worldmodel routes remain forbidden in skeleton",
    "runtime routes remain forbidden in skeleton",
    "candidate_fact_boundary enforced",
    "schema_invalid_event must be invalid_or_blocked_candidate",
    "L0 governance constraints apply to all skeleton functions",
)

HEALTH_GUARD_SIGNALS: Tuple[str, ...] = (
    "missing_health_tag",
    "missing_timestamp",
    "missing_source_chain",
    "ttl_missing",
    "priority_conflict",
    "long_pending_candidate",
    "queue_backlog_candidate",
)

SKELETON_SAMPLES: Tuple[Dict[str, Any], ...] = (
    {
        "sample_id": "valid_navigation_event_to_p1_schedule",
        "description": "Valid navigation module_candidate_event normalized and scheduled as P1 candidate",
        "priority": "P1",
        "terminal": "scheduling_decision_candidate",
    },
    {
        "sample_id": "p0_safety_event_preempts_p1_navigation",
        "description": "P0 safety event preempts active P1 navigation scheduling candidate",
        "priority": "P0",
        "terminal": "preemption_candidate",
    },
    {
        "sample_id": "ttl_missing_event_blocked",
        "description": "Event without TTL produces blocked WM entry candidate, no active processing",
        "priority": "P2",
        "terminal": "blocked_candidate",
    },
    {
        "sample_id": "p5_background_dropped_under_resource_overload",
        "description": "P5 background event dropped under resource_overload defer/drop candidate",
        "priority": "P5",
        "terminal": "drop_candidate",
    },
    {
        "sample_id": "memory_recall_event_reused_as_hint_not_fact",
        "description": "memory_recall_event reused as hint candidate, never promoted to fact",
        "priority": "P4",
        "terminal": "hint_candidate_only",
    },
)

TEST_PLAN_CATEGORIES: Tuple[str, ...] = (
    "enum_completeness_tests",
    "schema_validation_tests",
    "state_transition_tests",
    "ttl_policy_tests",
    "priority_assignment_tests",
    "preemption_tests",
    "governance_boundary_tests",
    "no_runtime_no_provider_no_write_tests",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Skeleton Planning ≠ skeleton implementation",
    "Skeleton Planning ≠ real Event Bus runtime",
    "Skeleton Planning ≠ real Working Memory service",
    "Skeleton Planning ≠ real Scheduler execution",
    "Skeleton Planning ≠ async/multithreading enabled",
    "Skeleton Planning ≠ model/provider invocation",
    "Skeleton Planning ≠ task execution",
    "Skeleton Planning ≠ Memory / WorldModel write",
    "Skeleton Planning ≠ user output",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_only",
    "skeleton_plan_only",
    "implementation_files_not_created_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
    "real_async_queue_enabled_now",
    "true_multithreading_enabled_now",
    "runtime_enabled_now",
    "model_invoked_now",
    "provider_invoked_now",
    "task_execution_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "real_health_monitoring_enabled_now",
    "recovery_executed_now",
    "implementation_files_created_now",
)

DEFAULT_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_event_bus_working_memory_scheduler_planning"
)
DEFAULT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_event_bus_working_memory_scheduler_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning"
)


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


def run_midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_v1(
    *,
    midplatform_event_bus_working_memory_scheduler_planning_root: str,
    midplatform_event_bus_working_memory_scheduler_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    plan_root = Path(midplatform_event_bus_working_memory_scheduler_planning_root).expanduser().resolve()
    dr_root = Path(midplatform_event_bus_working_memory_scheduler_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "output_root": str(out_root),
        "upstream_planning_root": str(plan_root),
        "upstream_dryrun_root": str(dr_root),
    }

    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    dr_vr = _try_read_json(dr_root / "verifier_report.json") or {}
    dr_sm = _try_read_json(dr_root / "summary.json") or {}
    dr_ready = _try_read_json(dr_root / "dryrun_readiness_decision_v1.json") or {}

    if plan_vr.get("verifier") != "GO":
        blockers.append("upstream planning verifier must be GO")
    if dr_vr.get("verifier") != "GO":
        blockers.append("upstream dryrun verifier must be GO")
    if dr_sm.get("final_decision") != UPSTREAM_DRYRUN_FINAL:
        blockers.append("upstream dryrun final_decision mismatch")
    if dr_ready.get("dryrun_pass") is not True:
        blockers.append("upstream dryrun_readiness must pass")

    upstream: Dict[str, Any] = {}
    for fname in UPSTREAM_PLANNING_FILES:
        data = _try_read_json(plan_root / fname)
        if data is None:
            blockers.append(f"missing planning upstream: {fname}")
        key = fname.replace("_v1.json", "")
        upstream[key] = data
    for fname in UPSTREAM_DRYRUN_FILES:
        data = _try_read_json(dr_root / fname)
        if data is None:
            blockers.append(f"missing dryrun upstream: {fname}")
        key = fname.replace("_v1.json", "")
        upstream[key] = data

    repo_root = Path(__file__).resolve().parents[2]
    skeleton_files_exist = any((repo_root / f["path"]).is_file() for f in SKELETON_FILE_PLAN)
    if skeleton_files_exist:
        blockers.append("skeleton implementation files must not exist in this phase")

    controlled_skeleton_scope = {
        "scope_id": "controlled_skeleton_scope_v1",
        "allowed": [
            "dataclass",
            "enum",
            "pure_function",
            "in_memory_stub",
            "static_validator",
            "candidate_only_output",
        ],
        "forbidden": [
            "real_event_bus_loop",
            "real_working_memory_runtime",
            "real_scheduler_worker",
            "real_multithreading",
            "real_async_queue",
            "provider_invocation",
            "model_invocation",
            "real_task_chain",
            "memory_write",
            "worldmodel_write",
            "user_output",
            "real_recovery",
        ],
        "boundary_from_runtime": "contract_level_skeleton_planning_only",
        **meta,
    }

    controlled_skeleton_file_plan = {
        "plan_id": "controlled_skeleton_file_plan_v1",
        "files": list(SKELETON_FILE_PLAN),
        "file_count": len(SKELETON_FILE_PLAN),
        "create_in_this_phase": False,
        "implementation_files_created_now": False,
        **meta,
    }

    controlled_skeleton_type_contract = {
        "contract_id": "controlled_skeleton_type_contract_v1",
        "types": list(COMMON_TYPES),
        "type_count": len(COMMON_TYPES),
        "event_fields": list(EVENT_BUS_FIELDS),
        "working_memory_entry_fields": list(WORKING_MEMORY_FIELDS),
        "scheduling_request_fields": list(SCHEDULER_FIELDS),
        "event_type_enum_values": list(EVENT_TYPES),
        "event_state_enum_values": list(EVENT_STATES),
        "wm_entry_state_enum_values": list(WM_ENTRY_STATES),
        "priority_class_enum_values": ["P0", "P1", "P2", "P3", "P4", "P5"],
        **meta,
    }

    event_bus_skeleton_contract = {
        "contract_id": "event_bus_skeleton_contract_v1",
        "component": "event_bus",
        "allowed_functions": list(EVENT_BUS_SKELETON_FUNCTIONS),
        "enums": ["EventType", "EventState"],
        "dataclass": "Event",
        "forbidden": list(EVENT_BUS_SKELETON_FORBIDDEN),
        "outputs": ["RouteCandidate", "normalized Event", "validation_result"],
        **meta,
    }

    working_memory_skeleton_contract = {
        "contract_id": "working_memory_skeleton_contract_v1",
        "component": "working_memory",
        "allowed_functions": list(WM_SKELETON_FUNCTIONS),
        "enums": ["WorkingMemoryEntryState"],
        "dataclass": "WorkingMemoryEntry",
        "forbidden": list(WM_SKELETON_FORBIDDEN),
        "outputs": ["WorkingMemoryEntryCandidate", "TTLPolicyCandidate", "cleanup_plan_candidate"],
        "working_memory_is_not_memory": True,
        "working_memory_is_not_worldmodel": True,
        **meta,
    }

    scheduler_skeleton_contract = {
        "contract_id": "scheduler_skeleton_contract_v1",
        "component": "scheduler",
        "allowed_functions": list(SCHEDULER_SKELETON_FUNCTIONS),
        "enums": ["PriorityClass"],
        "dataclass": "SchedulingRequest",
        "forbidden": list(SCHEDULER_SKELETON_FORBIDDEN),
        "outputs": ["SchedulingDecisionCandidate", "preemption_candidate", "defer_or_drop_candidate"],
        **meta,
    }

    controlled_skeleton_interaction_plan = {
        "plan_id": "controlled_skeleton_interaction_plan_v1",
        "steps": list(INTERACTION_STEPS),
        "candidate_only": True,
        "no_real_dispatch": True,
        "flow": "Event → normalize/validate → WM entry candidate → TTL candidate → scheduling request → decision candidate",
        **meta,
    }

    controlled_skeleton_governance_guard = {
        "guard_id": "controlled_skeleton_governance_guard_v1",
        "rules": list(GOVERNANCE_GUARD_RULES),
        "l0_constrained": True,
        **meta,
    }

    controlled_skeleton_health_guard = {
        "guard_id": "controlled_skeleton_health_guard_v1",
        "signals": list(HEALTH_GUARD_SIGNALS),
        "output_type": "health_issue_candidate",
        "real_health_runtime_enabled": False,
        **meta,
    }

    controlled_skeleton_sample_plan = {
        "plan_id": "controlled_skeleton_sample_plan_v1",
        "samples": list(SKELETON_SAMPLES),
        "sample_count": len(SKELETON_SAMPLES),
        **meta,
    }

    controlled_skeleton_test_plan = {
        "plan_id": "controlled_skeleton_test_plan_v1",
        "categories": list(TEST_PLAN_CATEGORIES),
        "category_count": len(TEST_PLAN_CATEGORIES),
        "execution_phase": "Implementation Execution or Implementation DryRun",
        "tests": [
            {"test_id": "test_event_type_enum_complete", "category": "enum_completeness_tests"},
            {"test_id": "test_event_schema_validation", "category": "schema_validation_tests"},
            {"test_id": "test_event_state_transition", "category": "state_transition_tests"},
            {"test_id": "test_wm_ttl_policy", "category": "ttl_policy_tests"},
            {"test_id": "test_priority_assignment_p0_p5", "category": "priority_assignment_tests"},
            {"test_id": "test_p0_preemption", "category": "preemption_tests"},
            {"test_id": "test_governance_blocked_candidate", "category": "governance_boundary_tests"},
            {"test_id": "test_no_runtime_no_write", "category": "no_runtime_no_provider_no_write_tests"},
        ],
        **meta,
    }

    controlled_skeleton_boundary_matrix = {
        "matrix_id": "controlled_skeleton_boundary_matrix_v1",
        "global_boundaries": {f: False for f in BOUNDARY_FALSE},
        "foundation_components": {
            comp: {f: False for f in BOUNDARY_FALSE}
            for comp in ("event_bus", "working_memory", "scheduler")
        },
        **meta,
    }

    controlled_skeleton_non_claims = {
        "register_id": "controlled_skeleton_non_claims_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    planning_pass = len(blockers) == 0
    readiness = {
        "decision_id": "controlled_skeleton_planning_readiness_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "skeleton_scope_defined": True,
        "file_plan_defined": True,
        "implementation_files_created_now": False,
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
        "foundation_components": ["event_bus", "working_memory", "scheduler"],
        **meta,
    }

    return {
        "summary": summary,
        "controlled_skeleton_scope": controlled_skeleton_scope,
        "controlled_skeleton_file_plan": controlled_skeleton_file_plan,
        "controlled_skeleton_type_contract": controlled_skeleton_type_contract,
        "event_bus_skeleton_contract": event_bus_skeleton_contract,
        "working_memory_skeleton_contract": working_memory_skeleton_contract,
        "scheduler_skeleton_contract": scheduler_skeleton_contract,
        "controlled_skeleton_interaction_plan": controlled_skeleton_interaction_plan,
        "controlled_skeleton_governance_guard": controlled_skeleton_governance_guard,
        "controlled_skeleton_health_guard": controlled_skeleton_health_guard,
        "controlled_skeleton_sample_plan": controlled_skeleton_sample_plan,
        "controlled_skeleton_test_plan": controlled_skeleton_test_plan,
        "controlled_skeleton_boundary_matrix": controlled_skeleton_boundary_matrix,
        "controlled_skeleton_non_claims": controlled_skeleton_non_claims,
        "controlled_skeleton_planning_readiness_decision": readiness,
    }
