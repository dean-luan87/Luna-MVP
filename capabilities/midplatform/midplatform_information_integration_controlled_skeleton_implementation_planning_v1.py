# -*- coding: utf-8 -*-
"""Luna Midplatform Information Integration Controlled Skeleton Implementation Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_information_integration_mount_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MOUNT_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as MOUNT_DRYRUN_NEXT,
)
from capabilities.midplatform.midplatform_information_integration_mount_planning_v1 import (
    PROCESSING_STEPS,
)

PHASE_ID = (
    "Phase-Midplatform-Information-Integration-Controlled-Skeleton-Implementation-Planning-v1-001"
)
SCOPE = "midplatform_information_integration_controlled_skeleton_implementation_planning_only"
SOURCE_CHAIN = "midplatform_information_integration_controlled_skeleton_implementation_planning_v1"

UPSTREAM_MOUNT_DRYRUN_FINAL = MOUNT_DRYRUN_FINAL_GO
UPSTREAM_MOUNT_DRYRUN_NEXT = MOUNT_DRYRUN_NEXT

FINAL_DECISION_GO = (
    "MIDPLATFORM_INFORMATION_INTEGRATION_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING_"
    "READY_FOR_IMPLEMENTATION_DRYRUN"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_INFORMATION_INTEGRATION_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING_"
    "HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Information-Integration-Controlled-Skeleton-Implementation-DryRun-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Information-Integration-Controlled-Skeleton-Issue-Review-v1-001"
)

UPSTREAM_MOUNT_DRYRUN_FILES: Tuple[str, ...] = (
    "mount_dryrun_readiness_decision_v1.json",
    "upstream_mount_contract_consumability_review_v1.json",
    "frozen_interface_consumption_review_v1.json",
    "mount_contract_10_section_review_v1.json",
    "input_contract_dryrun_v1.json",
    "output_contract_dryrun_v1.json",
    "processing_model_dryrun_v1.json",
    "model_rule_algorithm_placement_review_v1.json",
    "governance_boundary_dryrun_v1.json",
    "health_boundary_dryrun_v1.json",
    "worldmodel_memory_feedback_boundary_review_v1.json",
    "downstream_handoff_matrix_review_v1.json",
    "sample_flow_dryrun_v1.json",
    "failure_route_dryrun_review_v1.json",
    "mount_health_metric_scope_review_v1.json",
    "boundary_matrix_review_v1.json",
    "non_claims_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

UPSTREAM_FOUNDATION_FILES: Tuple[str, ...] = (
    "micro_os_foundation_version_tag_v1.json",
    "micro_os_foundation_frozen_interface_v1.json",
    "micro_os_foundation_handoff_contract_v1.json",
)

FROZEN_FOUNDATION_REUSE: Tuple[str, ...] = (
    "Event",
    "WorkingMemoryEntry",
    "SchedulingDecisionCandidate",
    "PriorityClass",
    "validate_no_runtime_flags",
    "validate_candidate_not_fact",
    "validate_required_trace",
    "validate_required_health_tag",
    "validate_required_ttl",
    "validate_governance_guard",
)

SKELETON_FILE_PLAN: Tuple[Dict[str, Any], ...] = (
    {
        "path": "capabilities/midplatform/core/information_integration_types_v1.py",
        "purpose": "8 core candidate dataclass types for Information Integration",
        "create_in_this_phase": False,
    },
    {
        "path": "capabilities/midplatform/core/information_integration_skeleton_v1.py",
        "purpose": "pure function candidate generators: collect, group, build, detect, allocate",
        "create_in_this_phase": False,
    },
    {
        "path": "capabilities/midplatform/core/information_integration_static_validators_v1.py",
        "purpose": "static validators for input/output/boundary/governance/recall",
        "create_in_this_phase": False,
    },
)

CANDIDATE_TYPES: Tuple[Dict[str, Any], ...] = (
    {
        "type_name": "LiveWorldStateCandidate",
        "fields": (
            "candidate_id",
            "source_entry_refs",
            "spatiotemporal_slot_ref",
            "observed_state_summary",
            "freshness_status",
            "confidence_summary",
            "conflict_refs",
            "gap_refs",
            "trace_ref",
            "health_refs",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "TaskWorldSliceCandidate",
        "fields": (
            "candidate_id",
            "task_ref",
            "relevant_entry_refs",
            "task_relevance_summary",
            "priority_class",
            "required_observation_refs",
            "blocked_reason",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "PriorityAttentionMapCandidate",
        "fields": (
            "candidate_id",
            "p0_refs",
            "p1_refs",
            "p2_refs",
            "p3_refs",
            "p4_refs",
            "p5_refs",
            "survival_relevance_summary",
            "task_relevance_summary",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "InformationAllocationCandidate",
        "fields": (
            "candidate_id",
            "decision_center_refs",
            "task_manager_refs",
            "health_watchdog_refs",
            "module_adapter_refs",
            "worldmodel_memory_bridge_refs",
            "hold_refs",
            "discard_refs",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "ConflictCandidate",
        "fields": (
            "candidate_id",
            "conflict_type",
            "involved_entry_refs",
            "conflict_summary",
            "severity",
            "requires_confirmation",
            "decision_readiness",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "GapCandidate",
        "fields": (
            "candidate_id",
            "gap_type",
            "missing_information",
            "affected_task_ref",
            "required_observation_candidate_ref",
            "severity",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "RequiredObservationCandidate",
        "fields": (
            "candidate_id",
            "observation_target",
            "requested_module",
            "reason",
            "priority_class",
            "ttl",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "DecisionContextCandidate",
        "fields": (
            "candidate_id",
            "live_world_state_ref",
            "task_world_slice_ref",
            "priority_attention_map_ref",
            "conflict_refs",
            "gap_refs",
            "required_observation_refs",
            "governance_check_ref",
            "health_refs",
            "readiness_status",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
)

PURE_FUNCTIONS: Tuple[Dict[str, Any], ...] = (
    {
        "function_name": "collect_eligible_entries",
        "inputs": ["WorkingMemoryEntry", "SchedulingDecisionCandidate"],
        "output": "eligible_entry_candidate_list",
        "filters": ["stale", "ttl_missing", "missing_health_tag", "governance_invalid"],
        "forbidden": ["promote_to_fact", "runtime_execution"],
    },
    {
        "function_name": "group_entries_by_spatiotemporal_slot",
        "inputs": ["WorkingMemoryEntry"],
        "output": "slot_group_candidate",
        "forbidden": ["generate_fact"],
    },
    {
        "function_name": "build_live_world_state_candidate",
        "inputs": ["slot_group", "context"],
        "output": "LiveWorldStateCandidate",
        "forbidden": ["write_worldmodel"],
    },
    {
        "function_name": "extract_task_world_slice_candidate",
        "inputs": ["WorkingMemoryEntry", "task_context"],
        "output": "TaskWorldSliceCandidate",
        "forbidden": ["execute_task"],
    },
    {
        "function_name": "build_priority_attention_map_candidate",
        "inputs": ["WorkingMemoryEntry", "SchedulingDecisionCandidate"],
        "output": "PriorityAttentionMapCandidate",
        "forbidden": ["rewrite_scheduler_decision"],
    },
    {
        "function_name": "detect_conflict_candidate",
        "inputs": ["WorkingMemoryEntry", "recall_context"],
        "output": "ConflictCandidate list",
        "recall_role": "hint_only",
    },
    {
        "function_name": "detect_gap_candidate",
        "inputs": ["WorkingMemoryEntry", "task_context"],
        "output": "GapCandidate list",
        "may_emit": "RequiredObservationCandidate",
    },
    {
        "function_name": "allocate_information_candidate",
        "inputs": [
            "LiveWorldStateCandidate",
            "TaskWorldSliceCandidate",
            "ConflictCandidate",
            "GapCandidate",
            "PriorityAttentionMapCandidate",
        ],
        "output": "InformationAllocationCandidate",
        "forbidden": ["direct_mount"],
    },
    {
        "function_name": "build_decision_context_candidate",
        "inputs": [
            "LiveWorldStateCandidate",
            "TaskWorldSliceCandidate",
            "PriorityAttentionMapCandidate",
            "InformationAllocationCandidate",
            "ConflictCandidate",
            "GapCandidate",
            "governance_ref",
        ],
        "output": "DecisionContextCandidate",
        "high_risk_without_governance": "blocked_or_not_ready",
    },
    {
        "function_name": "validate_information_integration_candidate",
        "inputs": ["candidate_object"],
        "output": "ValidationResult",
        "checks": ["candidate_not_fact", "trace", "health", "ttl", "governance_boundary"],
    },
)

STATIC_VALIDATORS: Tuple[str, ...] = (
    "validate_ii_input_contract",
    "validate_ii_output_candidate_only",
    "validate_ii_no_fact_write",
    "validate_ii_no_memory_worldmodel_write",
    "validate_ii_no_user_output",
    "validate_ii_recall_context_hint_only",
    "validate_ii_governance_required_for_high_risk",
    "validate_ii_health_required",
    "validate_ii_boundary_matrix",
)

PROCESSING_CHAIN: Tuple[str, ...] = (
    "collect_eligible_entries",
    "group_entries_by_spatiotemporal_slot",
    "build_live_world_state_candidate",
    "extract_task_world_slice_candidate",
    "build_priority_attention_map_candidate",
    "detect_conflict_candidate",
    "detect_gap_candidate",
    "allocate_information_candidate",
    "build_decision_context_candidate",
)

GOVERNANCE_GUARD_RULES: Tuple[str, ...] = (
    "high_risk_decision_context_without_governance_check_ref must be blocked or not_ready",
    "output routes remain forbidden in skeleton",
    "memory routes remain forbidden in skeleton",
    "worldmodel routes remain forbidden in skeleton",
    "runtime routes remain forbidden in skeleton",
    "candidate_fact_boundary enforced",
    "do not bypass frozen Micro-OS foundation",
    "L0 governance constraints apply to all skeleton functions",
)

HEALTH_GUARD_RULES: Tuple[str, ...] = (
    "missing_health_tag → blocked or health_issue_candidate",
    "missing_trace → invalid or blocked",
    "ttl_missing → blocked",
    "stale entry → degraded or reobserve candidate",
    "low confidence → pending_confirmation or required_observation_candidate",
    "unresolved conflict → hold or decision_readiness_not_ready",
)

RECALL_BOUNDARY_RULES: Tuple[str, ...] = (
    "recall_context as hint only",
    "recall_context as known_state_candidate only",
    "recall_context as change_detection_reference only",
    "must not override realtime safety information",
    "must not replace required current observation",
    "must not write Memory directly",
    "must not write WorldModel directly",
)

SKELETON_SAMPLES: Tuple[Dict[str, Any], ...] = (
    {
        "sample_id": "navigation_build_decision_context_candidate",
        "description": "Navigation WM entries produce decision_context_candidate without runtime",
        "terminal": "DecisionContextCandidate",
    },
    {
        "sample_id": "ocr_gap_generates_required_observation_candidate",
        "description": "OCR reading gap generates RequiredObservationCandidate, not user output",
        "terminal": "RequiredObservationCandidate",
    },
    {
        "sample_id": "health_fault_generates_hold_allocation_candidate",
        "description": "Health fault produces hold allocation candidate, no task execution",
        "terminal": "InformationAllocationCandidate",
    },
    {
        "sample_id": "memory_recall_used_as_hint_not_fact",
        "description": "Memory recall used as hint only, never promoted to fact",
        "terminal": "hint_candidate_only",
    },
    {
        "sample_id": "conflict_blocks_decision_readiness",
        "description": "Unresolved conflict blocks decision_readiness_not_ready",
        "terminal": "blocked_decision_context",
    },
)

TEST_PLAN_CATEGORIES: Tuple[str, ...] = (
    "type_completeness",
    "candidate_not_fact",
    "trace_health_ttl",
    "recall_hint_only",
    "conflict_gap_detection",
    "decision_context_readiness",
    "no_runtime_model_provider_write_output",
    "high_risk_governance_blocked",
    "boundary_matrix",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Skeleton Planning ≠ skeleton implementation",
    "Skeleton Planning ≠ Information Integration mounted",
    "Skeleton Planning ≠ runtime enabled",
    "Skeleton Planning ≠ model invoked",
    "Skeleton Planning ≠ provider invoked",
    "Skeleton Planning ≠ Decision Center ready",
    "Skeleton Planning ≠ Task Manager ready",
    "Skeleton Planning ≠ Memory / WorldModel write",
    "Skeleton Planning ≠ user output",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_information_integration_controlled_skeleton_implementation_planning_only",
    "skeleton_plan_only",
    "information_integration_files_not_created_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "information_integration_files_created_now",
    "information_integration_runtime_enabled_now",
    "information_integration_mounted_now",
    "model_invoked_now",
    "provider_invoked_now",
    "runtime_enabled_now",
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
    "task_execution_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "output_gate_mounted_now",
    "decision_center_mounted_now",
    "health_watchdog_mounted_now",
)

DEFAULT_MOUNT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_mount_dryrun_and_review"
)
DEFAULT_MOUNT_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_mount_planning"
)
DEFAULT_FREEZE_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_FREEZE_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_information_integration_controlled_skeleton_implementation_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "foundation_id": "midplatform_micro_os_foundation_v1",
        "foundation_version": "1.0.0-skeleton",
        "foundation_mutation_required": False,
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


def run_midplatform_information_integration_controlled_skeleton_implementation_planning_v1(
    *,
    midplatform_information_integration_mount_dryrun_and_review_root: str,
    midplatform_information_integration_mount_planning_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    mount_dr = Path(midplatform_information_integration_mount_dryrun_and_review_root).expanduser().resolve()
    mount_plan = Path(midplatform_information_integration_mount_planning_root).expanduser().resolve()
    freeze_dr = Path(midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root).expanduser().resolve()
    freeze_plan = Path(midplatform_micro_os_foundation_freeze_and_handoff_planning_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = {
        **_planning_meta(),
        "output_root": str(out_root),
        "upstream_mount_dryrun_root": str(mount_dr),
        "upstream_mount_planning_root": str(mount_plan),
        "upstream_freeze_dryrun_root": str(freeze_dr),
        "upstream_freeze_planning_root": str(freeze_plan),
    }

    mount_dr_vr = _try_read_json(mount_dr / "verifier_report.json") or {}
    mount_dr_sm = _try_read_json(mount_dr / "summary.json") or {}
    mount_dr_ready = _try_read_json(mount_dr / "mount_dryrun_readiness_decision_v1.json") or {}

    if mount_dr_vr.get("verifier") != "GO":
        blockers.append("upstream mount dryrun verifier must be GO")
    if mount_dr_sm.get("final_decision") != UPSTREAM_MOUNT_DRYRUN_FINAL:
        blockers.append("upstream mount dryrun final_decision mismatch")
    if mount_dr_ready.get("dryrun_pass") is not True:
        blockers.append("upstream mount_dryrun_readiness must pass")

    freeze_dr_vr = _try_read_json(freeze_dr / "verifier_report.json") or {}
    if freeze_dr_vr.get("verifier") != "GO":
        blockers.append("upstream foundation freeze dryrun verifier must be GO")

    upstream_dr: Dict[str, Any] = {}
    for fname in UPSTREAM_MOUNT_DRYRUN_FILES:
        if fname in ("summary.json", "verifier_report.json"):
            data = _try_read_json(mount_dr / fname)
        else:
            data = _try_read_json(mount_dr / fname)
        if data is None:
            blockers.append(f"missing mount dryrun upstream: {fname}")
        upstream_dr[fname.replace("_v1.json", "").replace(".json", "")] = data

    upstream_foundation: Dict[str, Any] = {}
    for fname in UPSTREAM_FOUNDATION_FILES:
        data = _try_read_json(freeze_plan / fname)
        if data is None:
            blockers.append(f"missing foundation upstream: {fname}")
        upstream_foundation[fname.replace("_v1.json", "")] = data

    version_doc = upstream_foundation.get("micro_os_foundation_version_tag") or {}
    interface_doc = upstream_foundation.get("micro_os_foundation_frozen_interface") or {}

    if version_doc.get("foundation_id") != "midplatform_micro_os_foundation_v1":
        blockers.append("foundation_id mismatch")
    if version_doc.get("runtime_status") != "not_enabled":
        blockers.append("foundation runtime must be not_enabled")

    ii_files_exist = any((repo_root / f["path"]).is_file() for f in SKELETON_FILE_PLAN)
    if ii_files_exist:
        blockers.append("information integration skeleton files must not exist in this phase")

    skeleton_scope = {
        "scope_id": "information_integration_skeleton_scope_v1",
        "module_id": "information_integration",
        "layer": "L6",
        "allowed": [
            "dataclass",
            "enum",
            "pure_function",
            "static_validator",
            "candidate_generator",
            "in_memory_stub",
        ],
        "forbidden": [
            "real_integration_runtime",
            "real_event_bus_loop",
            "real_working_memory_service",
            "real_scheduler_worker",
            "model_invocation",
            "provider_invocation",
            "task_execution",
            "memory_write",
            "worldmodel_write",
            "user_output",
            "direct_mount",
            "foundation_redefinition",
        ],
        "reuse_frozen_foundation": list(FROZEN_FOUNDATION_REUSE),
        **meta,
    }

    skeleton_file_plan = {
        "plan_id": "information_integration_skeleton_file_plan_v1",
        "files": list(SKELETON_FILE_PLAN),
        "file_count": len(SKELETON_FILE_PLAN),
        "create_in_this_phase": False,
        "information_integration_files_created_now": False,
        **meta,
    }

    type_contract = {
        "contract_id": "information_integration_type_contract_v1",
        "candidate_types": list(CANDIDATE_TYPES),
        "type_count": len(CANDIDATE_TYPES),
        "all_fact_status_not_fact": True,
        **meta,
    }

    function_contract = {
        "contract_id": "information_integration_function_contract_v1",
        "functions": list(PURE_FUNCTIONS),
        "function_count": len(PURE_FUNCTIONS),
        "reuse_frozen_types": ["Event", "WorkingMemoryEntry", "SchedulingDecisionCandidate", "PriorityClass"],
        **meta,
    }

    static_validator_contract = {
        "contract_id": "information_integration_static_validator_contract_v1",
        "validators": list(STATIC_VALIDATORS),
        "validator_count": len(STATIC_VALIDATORS),
        "reuse_foundation_validators": list(FROZEN_FOUNDATION_REUSE[4:]),
        **meta,
    }

    processing_chain_contract = {
        "contract_id": "information_integration_processing_chain_contract_v1",
        "chain": list(PROCESSING_CHAIN),
        "chain_count": len(PROCESSING_CHAIN),
        "candidate_only": True,
        "aligns_with_mount_processing_steps": list(PROCESSING_STEPS),
        **meta,
    }

    governance_guard_plan = {
        "plan_id": "information_integration_governance_guard_plan_v1",
        "rules": list(GOVERNANCE_GUARD_RULES),
        "rule_count": len(GOVERNANCE_GUARD_RULES),
        **meta,
    }

    health_guard_plan = {
        "plan_id": "information_integration_health_guard_plan_v1",
        "rules": list(HEALTH_GUARD_RULES),
        "rule_count": len(HEALTH_GUARD_RULES),
        **meta,
    }

    recall_boundary_plan = {
        "plan_id": "information_integration_recall_boundary_plan_v1",
        "rules": list(RECALL_BOUNDARY_RULES),
        "rule_count": len(RECALL_BOUNDARY_RULES),
        **meta,
    }

    sample_plan = {
        "plan_id": "information_integration_sample_plan_v1",
        "samples": list(SKELETON_SAMPLES),
        "sample_count": len(SKELETON_SAMPLES),
        **meta,
    }

    test_plan = {
        "plan_id": "information_integration_test_plan_v1",
        "categories": list(TEST_PLAN_CATEGORIES),
        "category_count": len(TEST_PLAN_CATEGORIES),
        "execution_phase": "Implementation DryRun",
        "tests": [
            {"test_id": f"test_{cat}", "category": cat} for cat in TEST_PLAN_CATEGORIES
        ],
        **meta,
    }

    skeleton_boundary_matrix = {
        "matrix_id": "information_integration_skeleton_boundary_matrix_v1",
        "global_boundaries": {f: False for f in BOUNDARY_FALSE},
        **meta,
    }

    skeleton_non_claims = {
        "register_id": "information_integration_skeleton_non_claims_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    planning_pass = len(blockers) == 0
    readiness = {
        "decision_id": "information_integration_skeleton_planning_readiness_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "skeleton_scope_defined": True,
        "file_plan_defined": True,
        "information_integration_files_created_now": False,
        "foundation_reuse_confirmed": True,
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
        "information_integration_skeleton_scope": skeleton_scope,
        "information_integration_skeleton_file_plan": skeleton_file_plan,
        "information_integration_type_contract": type_contract,
        "information_integration_function_contract": function_contract,
        "information_integration_static_validator_contract": static_validator_contract,
        "information_integration_processing_chain_contract": processing_chain_contract,
        "information_integration_governance_guard_plan": governance_guard_plan,
        "information_integration_health_guard_plan": health_guard_plan,
        "information_integration_recall_boundary_plan": recall_boundary_plan,
        "information_integration_sample_plan": sample_plan,
        "information_integration_test_plan": test_plan,
        "information_integration_skeleton_boundary_matrix": skeleton_boundary_matrix,
        "information_integration_skeleton_non_claims": skeleton_non_claims,
        "information_integration_skeleton_planning_readiness_decision": readiness,
    }
