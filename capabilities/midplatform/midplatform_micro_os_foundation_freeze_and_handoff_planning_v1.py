# -*- coding: utf-8 -*-
"""Luna Midplatform Micro-OS Foundation Freeze and Handoff Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_v1 import (
    EVENT_BUS_SKELETON_FUNCTIONS,
    SCHEDULER_SKELETON_FUNCTIONS,
    SKELETON_FILE_PLAN,
    WM_SKELETON_FUNCTIONS,
)
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as POST_DRYRUN_NEXT,
)

PHASE_ID = "Phase-Midplatform-Micro-OS-Foundation-Freeze-and-Handoff-Planning-v1-001"
SCOPE = "midplatform_micro_os_foundation_freeze_and_handoff_planning_only"
SOURCE_CHAIN = "midplatform_micro_os_foundation_freeze_and_handoff_planning_v1"

UPSTREAM_POST_DRYRUN_FINAL = POST_DRYRUN_FINAL_GO
UPSTREAM_POST_DRYRUN_NEXT = POST_DRYRUN_NEXT

FINAL_DECISION_GO = "MIDPLATFORM_MICRO_OS_FOUNDATION_FREEZE_AND_HANDOFF_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_MICRO_OS_FOUNDATION_FREEZE_AND_HANDOFF_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Micro-OS-Foundation-Freeze-and-Handoff-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Micro-OS-Foundation-Freeze-Issue-Review-v1-001"

UPSTREAM_POST_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "skeleton_file_integrity_review_v1.json",
    "forbidden_runtime_import_review_v1.json",
    "pure_function_boundary_review_v1.json",
    "event_bus_skeleton_review_v1.json",
    "working_memory_skeleton_review_v1.json",
    "scheduler_skeleton_review_v1.json",
    "static_validator_review_v1.json",
    "sample_dryrun_output_review_v1.json",
    "governance_guard_review_v1.json",
    "health_guard_review_v1.json",
    "boundary_matrix_post_review_v1.json",
    "downstream_mount_readiness_review_v1.json",
    "post_dryrun_issue_register_v1.json",
    "post_dryrun_readiness_decision_v1.json",
    "summary.json",
    "verifier_report.json",
)

FROZEN_SKELETON_FILES: Tuple[str, ...] = tuple(f["path"] for f in SKELETON_FILE_PLAN)

FROZEN_TYPES: Tuple[str, ...] = (
    "Event",
    "EventType",
    "EventState",
    "WorkingMemoryEntry",
    "WorkingMemoryEntryState",
    "PriorityClass",
    "SchedulingRequest",
    "SchedulingDecisionCandidate",
)

STATIC_VALIDATOR_FUNCTIONS: Tuple[str, ...] = (
    "validate_no_runtime_flags",
    "validate_candidate_not_fact",
    "validate_required_trace",
    "validate_required_health_tag",
    "validate_required_ttl",
    "validate_governance_guard",
)

WM_FROZEN_FUNCTIONS: Tuple[str, ...] = (
    *WM_SKELETON_FUNCTIONS,
    "validate_wm_state_transition",
)

FROZEN_INTERFACE_FUNCTIONS: Tuple[str, ...] = (
    *EVENT_BUS_SKELETON_FUNCTIONS,
    *WM_FROZEN_FUNCTIONS,
    *SCHEDULER_SKELETON_FUNCTIONS,
    *STATIC_VALIDATOR_FUNCTIONS,
)

MOUNT_POINTS: Tuple[Dict[str, Any], ...] = (
    {
        "consumer": "information_integration",
        "may_read": ["Event", "WorkingMemoryEntry", "SchedulingDecisionCandidate"],
        "mount_status": "readiness_only",
    },
    {
        "consumer": "task_manager",
        "may_consume": ["SchedulingDecisionCandidate", "task_state_event"],
        "mount_status": "readiness_only",
    },
    {
        "consumer": "drive_manager",
        "may_emit": ["drive_signal_event"],
        "mount_status": "readiness_only",
    },
    {
        "consumer": "health_watchdog",
        "may_consume": ["health_issue_candidate", "boundary_validator"],
        "mount_status": "readiness_only",
    },
    {
        "consumer": "module_adapter",
        "may_emit": ["standardized_candidate_to_event"],
        "mount_status": "readiness_only",
    },
    {
        "consumer": "worldmodel_memory_bridge",
        "may_consume": ["admission_candidate", "recall_context"],
        "mount_status": "readiness_only",
    },
)

FORBIDDEN_MUTATIONS: Tuple[str, ...] = (
    "modify_common_type_field_semantics",
    "remove_existing_enum",
    "change_candidate_not_fact_semantics",
    "turn_scheduler_decision_into_runtime_execution",
    "persist_working_memory_entry_as_memory_or_worldmodel_fact",
    "introduce_async_thread_provider_model_sdk",
    "bypass_static_validators",
)

CHANGE_CONTROL_STEPS: Tuple[str, ...] = (
    "change_request_candidate",
    "compatibility_impact_review",
    "upstream_contract_update_required",
    "downstream_consumer_impact_matrix",
    "verifier_update_required",
    "no_direct_mutation_allowed",
)

DOWNSTREAM_READINESS: Tuple[Dict[str, Any], ...] = (
    {"module": "information_integration_mount_planning", "readiness": "ready_as_next_primary_route"},
    {"module": "task_manager_mount_planning", "readiness": "ready_after_information_integration_or_parallel_later"},
    {"module": "drive_manager_mount_planning", "readiness": "ready_after_scheduler_handoff_review"},
    {"module": "health_watchdog_mount_planning", "readiness": "ready_after_foundation_freeze"},
    {"module": "module_adapter_mount_planning", "readiness": "ready_after_event_contract_review"},
    {"module": "worldmodel_memory_bridge_mount_planning", "readiness": "ready_after_information_integration_boundary_review"},
)

NON_CLAIMS: Tuple[str, ...] = (
    "Foundation Freeze ≠ runtime enabled",
    "Foundation Freeze ≠ real Event Bus service",
    "Foundation Freeze ≠ real Working Memory service",
    "Foundation Freeze ≠ real Scheduler execution",
    "Foundation Freeze ≠ Information Integration mounted",
    "Foundation Freeze ≠ Task Manager mounted",
    "Foundation Freeze ≠ Health Watchdog active",
    "Foundation Freeze ≠ model/provider invocation",
    "Foundation Freeze ≠ Memory / WorldModel write",
    "Foundation Freeze ≠ user output",
    "Foundation Freeze ≠ full Luna OS productization",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_micro_os_foundation_freeze_and_handoff_planning_only",
    "foundation_frozen_for_handoff_planning",
    "implementation_files_created_now",
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
    "direct_downstream_mount_executed_now",
)

DEFAULT_POST_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_SKELETON_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun"
)
DEFAULT_SKELETON_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning"
)
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_planning"


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


def run_midplatform_micro_os_foundation_freeze_and_handoff_planning_v1(
    *,
    midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_root: str,
    midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_root: str,
    midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    post_dr = Path(midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_root).expanduser().resolve()
    sk_dr = Path(midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_root).expanduser().resolve()
    sk_plan = Path(midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = {
        **_planning_meta(),
        "output_root": str(out_root),
        "upstream_post_dryrun_root": str(post_dr),
        "upstream_skeleton_dryrun_root": str(sk_dr),
        "upstream_skeleton_planning_root": str(sk_plan),
    }

    post_vr = _try_read_json(post_dr / "verifier_report.json") or {}
    post_sm = _try_read_json(post_dr / "summary.json") or {}
    post_ready = _try_read_json(post_dr / "post_dryrun_readiness_decision_v1.json") or {}

    if post_vr.get("verifier") != "GO":
        blockers.append("upstream post-dryrun verifier must be GO")
    if post_sm.get("final_decision") != UPSTREAM_POST_DRYRUN_FINAL:
        blockers.append("upstream post-dryrun final_decision mismatch")
    if post_ready.get("post_dryrun_review_pass") is not True:
        blockers.append("upstream post_dryrun_readiness must pass")

    upstream: Dict[str, Any] = {}
    for fname in UPSTREAM_POST_DRYRUN_ARTIFACTS:
        data = _try_read_json(post_dr / fname)
        if data is None:
            blockers.append(f"missing upstream artifact: {fname}")
        upstream[fname.replace("_v1.json", "").replace(".json", "")] = data

    for rel in FROZEN_SKELETON_FILES:
        if not (repo_root / rel).is_file():
            blockers.append(f"missing frozen skeleton file: {rel}")

    freeze_scope = {
        "scope_id": "micro_os_foundation_freeze_scope_v1",
        "frozen_types": list(FROZEN_TYPES),
        "frozen_skeleton_files": list(FROZEN_SKELETON_FILES),
        "event_bus_allowed_functions": list(EVENT_BUS_SKELETON_FUNCTIONS),
        "working_memory_allowed_functions": list(WM_FROZEN_FUNCTIONS),
        "scheduler_allowed_functions": list(SCHEDULER_SKELETON_FUNCTIONS),
        "static_validators": list(STATIC_VALIDATOR_FUNCTIONS),
        "freeze_not_runtime_ready": True,
        **meta,
    }

    frozen_interface = {
        "interface_id": "micro_os_foundation_frozen_interface_v1",
        "functions": list(FROZEN_INTERFACE_FUNCTIONS),
        "function_count": len(FROZEN_INTERFACE_FUNCTIONS),
        "modules": {
            "event_bus": list(EVENT_BUS_SKELETON_FUNCTIONS),
            "working_memory": list(WM_FROZEN_FUNCTIONS),
            "scheduler": list(SCHEDULER_SKELETON_FUNCTIONS),
            "static_validators": list(STATIC_VALIDATOR_FUNCTIONS),
        },
        **meta,
    }

    version_tag = {
        "tag_id": "micro_os_foundation_version_tag_v1",
        "foundation_id": "midplatform_micro_os_foundation_v1",
        "version": "1.0.0-skeleton",
        "status": "frozen_for_downstream_mount_planning",
        "runtime_status": "not_enabled",
        "compatibility_scope": "planning_and_static_dryrun_only",
        "allowed_consumers": [
            "information_integration",
            "task_manager",
            "drive_manager",
            "health_watchdog",
            "module_adapter",
            "worldmodel_memory_bridge",
        ],
        **meta,
    }

    handoff_contract = {
        "contract_id": "micro_os_foundation_handoff_contract_v1",
        "rules": [
            "downstream may only import types, enums, pure functions, validators",
            "downstream may only generate candidates",
            "downstream must not start Event Bus runtime",
            "downstream must not treat Working Memory as long-term Memory",
            "downstream must not bypass Scheduler",
            "downstream must not bypass Governance Gate",
            "downstream must not write Memory or WorldModel directly",
            "downstream must not produce user output directly",
        ],
        **meta,
    }

    allowed_mount_points = {
        "mount_id": "micro_os_foundation_allowed_mount_points_v1",
        "mount_points": list(MOUNT_POINTS),
        "direct_mount_executed": False,
        "mount_readiness_only": True,
        **meta,
    }

    forbidden_mutation_policy = {
        "policy_id": "micro_os_foundation_forbidden_mutation_policy_v1",
        "forbidden_mutations": list(FORBIDDEN_MUTATIONS),
        **meta,
    }

    change_control_policy = {
        "policy_id": "micro_os_foundation_change_control_policy_v1",
        "steps": list(CHANGE_CONTROL_STEPS),
        "change_executed_in_this_phase": False,
        **meta,
    }

    downstream_readiness_matrix = {
        "matrix_id": "micro_os_foundation_downstream_readiness_matrix_v1",
        "entries": list(DOWNSTREAM_READINESS),
        **meta,
    }

    health_boundary_freeze = {
        "freeze_id": "micro_os_foundation_health_and_boundary_freeze_v1",
        "global_boundaries": {**{f: False for f in BOUNDARY_FALSE}, "implementation_files_created_now": True},
        **meta,
    }

    non_claims = {
        "register_id": "micro_os_foundation_non_claims_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    route_decision = {
        "decision_id": "micro_os_foundation_route_decision_v1",
        "primary_next_phase": "Phase-Midplatform-Information-Integration-Mount-Planning-v1-001",
        "secondary_next_phase": "Phase-Midplatform-Health-Watchdog-Mount-Planning-v1-001",
        "deferred": [
            "Task Manager Mount Planning",
            "Drive Manager Mount Planning",
            "Module Adapter Mount Planning",
            "WorldModel-Memory Bridge Mount Planning",
        ],
        "rationale": [
            "Information Integration is the primary midplatform next route",
            "Health Watchdog may follow in parallel after freeze",
            "Task and Drive depend on Information Integration outputs",
            "Module Adapter and WorldModel-Memory Bridge after Integration boundary",
        ],
        **meta,
    }

    planning_pass = len(blockers) == 0
    readiness = {
        "decision_id": "micro_os_foundation_freeze_readiness_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "foundation_frozen": True,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "primary_route_after_freeze": route_decision["primary_next_phase"],
        "non_claims": list(NON_CLAIMS),
        "foundation_id": version_tag["foundation_id"],
        "foundation_version": version_tag["version"],
        **meta,
    }

    return {
        "summary": summary,
        "micro_os_foundation_freeze_scope": freeze_scope,
        "micro_os_foundation_frozen_interface": frozen_interface,
        "micro_os_foundation_version_tag": version_tag,
        "micro_os_foundation_handoff_contract": handoff_contract,
        "micro_os_foundation_allowed_mount_points": allowed_mount_points,
        "micro_os_foundation_forbidden_mutation_policy": forbidden_mutation_policy,
        "micro_os_foundation_change_control_policy": change_control_policy,
        "micro_os_foundation_downstream_readiness_matrix": downstream_readiness_matrix,
        "micro_os_foundation_health_and_boundary_freeze": health_boundary_freeze,
        "micro_os_foundation_non_claims": non_claims,
        "micro_os_foundation_route_decision": route_decision,
        "micro_os_foundation_freeze_readiness_decision": readiness,
    }
