# -*- coding: utf-8 -*-
"""Luna Midplatform Decision Center Foundation Handoff Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_decision_center_controlled_skeleton_implementation_dryrun_v1 import (
    SKELETON_FUNCTIONS,
)
from capabilities.midplatform.midplatform_decision_center_controlled_skeleton_implementation_planning_v1 import (
    CANDIDATE_TYPES,
    DECISION_READINESS_ENUM,
    DECISION_STATE_ENUM,
    PROCESSING_CHAIN,
    SKELETON_FILE_PLAN,
    STATIC_VALIDATORS,
)
from capabilities.midplatform.midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as POST_DRYRUN_NEXT,
)

PHASE_ID = "Phase-Midplatform-Decision-Center-Foundation-Handoff-Planning-v1-001"
SCOPE = "midplatform_decision_center_foundation_handoff_planning_only"
SOURCE_CHAIN = "midplatform_decision_center_foundation_handoff_planning_v1"

UPSTREAM_POST_DRYRUN_FINAL = POST_DRYRUN_FINAL_GO
UPSTREAM_POST_DRYRUN_NEXT = POST_DRYRUN_NEXT

FINAL_DECISION_GO = "MIDPLATFORM_DECISION_CENTER_FOUNDATION_HANDOFF_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_DECISION_CENTER_FOUNDATION_HANDOFF_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Decision-Center-Foundation-Handoff-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Decision-Center-Foundation-Handoff-Issue-Review-v1-001"

UPSTREAM_POST_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "skeleton_file_integrity_review_v1.json",
    "forbidden_runtime_import_review_v1.json",
    "pure_function_boundary_review_v1.json",
    "type_contract_review_v1.json",
    "function_contract_review_v1.json",
    "static_validator_review_v1.json",
    "sample_dryrun_output_review_v1.json",
    "processing_chain_review_v1.json",
    "governance_guard_review_v1.json",
    "health_guard_review_v1.json",
    "information_integration_dependency_review_v1.json",
    "downstream_readiness_review_v1.json",
    "boundary_matrix_post_review_v1.json",
    "post_dryrun_issue_register_v1.json",
    "post_dryrun_readiness_decision_v1.json",
    "summary.json",
    "verifier_report.json",
)

FROZEN_SKELETON_FILES: Tuple[str, ...] = tuple(f["path"] for f in SKELETON_FILE_PLAN)

FROZEN_ENUM_TYPES: Tuple[str, ...] = ("DecisionState", "DecisionReadiness")

FROZEN_CANDIDATE_TYPES: Tuple[str, ...] = tuple(t["type_name"] for t in CANDIDATE_TYPES)

FROZEN_FUNCTIONS: Tuple[str, ...] = SKELETON_FUNCTIONS

FROZEN_VALIDATORS: Tuple[str, ...] = STATIC_VALIDATORS

REQUIRED_TYPE_BASE_FIELDS: Tuple[str, ...] = (
    "candidate_id",
    "trace_ref",
    "fact_status",
)

HANDOFF_RULES: Tuple[str, ...] = (
    "downstream may only import decision candidate types",
    "downstream may only import pure functions",
    "downstream may only import validators",
    "downstream may only consume candidate outputs",
    "downstream must not require Decision Center runtime",
    "downstream must not treat decision_candidate as final action",
    "downstream must not treat decision_candidate as task execution",
    "downstream must not treat decision_candidate as user output",
    "downstream must not bypass Governance Gate",
    "downstream must not write Memory or WorldModel directly",
    "downstream must not mount Output Gate runtime directly",
)

DOWNSTREAM_OUTPUT_CONTRACT: Tuple[Dict[str, Any], ...] = (
    {
        "consumer": "health_watchdog",
        "consumes": ["health_review_candidate", "blocked", "hold", "stale", "unresolved_safety_refs"],
        "timing": "later",
    },
    {
        "consumer": "task_manager",
        "consumes": ["task_handoff_candidate", "decision_candidate"],
        "timing": "later",
    },
    {
        "consumer": "output_gate",
        "consumes": ["output_handoff_candidate"],
        "timing": "after_output_gate_mount_and_output_readiness",
    },
    {
        "consumer": "module_adapter",
        "consumes": ["required_observation_handoff_candidate"],
        "timing": "later",
    },
    {
        "consumer": "worldmodel_memory_bridge",
        "consumes": ["admission_review_candidate"],
        "timing": "after_admission_policy_later",
    },
    {
        "consumer": "governance_gate",
        "consumes": ["governance_pending", "blocked_candidate"],
        "timing": "boundary_consumer",
    },
)

FORBIDDEN_MUTATIONS: Tuple[str, ...] = (
    "modify_decision_candidate_final_action_false_semantics",
    "modify_decision_candidate_user_output_false_semantics",
    "modify_downstream_handoff_direct_mount_false_semantics",
    "remove_candidate_id_or_trace_ref_or_fact_status",
    "turn_pure_function_into_runtime_function",
    "introduce_model_invocation_in_skeleton",
    "introduce_provider_invocation_in_skeleton",
    "execute_task_chain_in_skeleton",
    "write_memory_or_worldmodel_in_skeleton",
    "generate_user_output_in_skeleton",
    "let_task_manager_treat_decision_candidate_as_executed_task",
    "let_output_gate_consume_output_handoff_before_mount",
    "let_health_watchdog_trigger_real_recovery",
    "let_decision_center_redefine_information_integration",
)

CHANGE_CONTROL_STEPS: Tuple[str, ...] = (
    "change_request_candidate",
    "compatibility_impact_review",
    "affected_downstream_consumer_matrix",
    "decision_candidate_contract_update_review",
    "verifier_update_required",
    "foundation_version_bump_required",
    "no_direct_mutation_allowed",
)

DOWNSTREAM_READINESS: Tuple[Dict[str, Any], ...] = (
    {"module": "health_watchdog_mount_planning", "readiness": "primary_next_ready"},
    {"module": "task_manager_mount_planning", "readiness": "secondary_after_health_watchdog_or_parallel_later"},
    {"module": "output_gate_mount_planning", "readiness": "not_ready_until_output_handoff_contract_review"},
    {"module": "worldmodel_memory_bridge_mount_planning", "readiness": "ready_after_admission_review_policy"},
    {"module": "module_adapter_feedback_mount_planning", "readiness": "ready_after_required_observation_handoff_review"},
    {"module": "governance_gate_review", "readiness": "ready_as_boundary_consumer"},
)

NON_CLAIMS: Tuple[str, ...] = (
    "Decision Center Foundation Handoff ≠ runtime enabled",
    "Decision Center Foundation Handoff ≠ Decision Center mounted",
    "Decision Center Foundation Handoff ≠ final action",
    "Decision Center Foundation Handoff ≠ task execution",
    "Decision Center Foundation Handoff ≠ user output",
    "Decision Center Foundation Handoff ≠ Output Gate ready",
    "Decision Center Foundation Handoff ≠ Task Manager mounted",
    "Decision Center Foundation Handoff ≠ Health Watchdog active",
    "Decision Center Foundation Handoff ≠ model/provider invocation",
    "Decision Center Foundation Handoff ≠ Memory / WorldModel write",
    "Decision Center Foundation Handoff ≠ full decision pipeline",
)

ROUTE_RATIONALE: Tuple[str, ...] = (
    "Decision Center already generates blocked / not_ready / health_review / hold candidate",
    "Health Watchdog is the most natural safety supervision downstream",
    "Task Manager needs decision_candidate but should wait for health/watchdog boundary",
    "Output Gate must wait until task and decision boundaries are more stable",
    "WorldModel-Memory Bridge and Module Adapter remain deferred until admission/observation contracts mature",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_decision_center_foundation_handoff_planning_only",
    "decision_center_foundation_frozen_for_handoff_planning",
    "decision_center_files_created_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "decision_center_runtime_enabled_now",
    "decision_center_mounted_now",
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
    "direct_downstream_mount_executed_now",
)

DEFAULT_POST_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_SKELETON_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_decision_center_controlled_skeleton_implementation_dryrun"
)
DEFAULT_MOUNT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_mount_dryrun_and_review"
)
DEFAULT_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_foundation_handoff_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "module_id": "decision_center",
        "layer": "L7",
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


def run_midplatform_decision_center_foundation_handoff_planning_v1(
    *,
    midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review_root: str,
    midplatform_decision_center_controlled_skeleton_implementation_dryrun_root: str,
    midplatform_decision_center_mount_dryrun_and_review_root: str,
    midplatform_information_integration_foundation_handoff_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    post_dr = Path(midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review_root).expanduser().resolve()
    sk_dr = Path(midplatform_decision_center_controlled_skeleton_implementation_dryrun_root).expanduser().resolve()
    mount_dr = Path(midplatform_decision_center_mount_dryrun_and_review_root).expanduser().resolve()
    handoff_dr = Path(midplatform_information_integration_foundation_handoff_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = {
        **_planning_meta(),
        "output_root": str(out_root),
        "upstream_post_dryrun_root": str(post_dr),
        "upstream_skeleton_dryrun_root": str(sk_dr),
        "upstream_mount_dryrun_root": str(mount_dr),
        "upstream_ii_handoff_dryrun_root": str(handoff_dr),
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

    handoff_vr = _try_read_json(handoff_dr / "verifier_report.json") or {}
    if handoff_vr.get("verifier") != "GO":
        blockers.append("upstream II foundation handoff dryrun verifier must be GO")

    upstream: Dict[str, Any] = {}
    for fname in UPSTREAM_POST_DRYRUN_ARTIFACTS:
        data = _try_read_json(post_dr / fname)
        if data is None:
            blockers.append(f"missing upstream artifact: {fname}")
        upstream[fname.replace("_v1.json", "").replace(".json", "")] = data

    for rel in FROZEN_SKELETON_FILES:
        if not (repo_root / rel).is_file():
            blockers.append(f"missing frozen skeleton file: {rel}")

    handoff_scope = {
        "scope_id": "decision_center_foundation_handoff_scope_v1",
        "frozen_enums": list(FROZEN_ENUM_TYPES),
        "frozen_candidate_types": list(FROZEN_CANDIDATE_TYPES),
        "frozen_functions": list(FROZEN_FUNCTIONS),
        "frozen_validators": list(FROZEN_VALIDATORS),
        "frozen_skeleton_files": list(FROZEN_SKELETON_FILES),
        "processing_chain": list(PROCESSING_CHAIN),
        "guards": ["governance_guard", "health_guard", "information_integration_dependency_guard"],
        "downstream_readiness_included": True,
        "handoff_not_runtime_enabled": True,
        **meta,
    }

    version_tag = {
        "tag_id": "decision_center_foundation_version_tag_v1",
        "foundation_id": "midplatform_decision_center_foundation_v1",
        "depends_on": "midplatform_information_integration_foundation_v1",
        "also_depends_on": "midplatform_micro_os_foundation_v1",
        "version": "1.0.0-skeleton",
        "status": "frozen_for_downstream_mount_planning",
        "runtime_status": "not_enabled",
        "compatibility_scope": "planning_and_static_dryrun_only",
        "allowed_consumers": [
            "health_watchdog",
            "task_manager",
            "output_gate",
            "module_adapter",
            "worldmodel_memory_bridge",
            "governance_gate",
        ],
        **meta,
    }

    type_field_map: Dict[str, List[str]] = {}
    for t in CANDIDATE_TYPES:
        type_field_map[t["type_name"]] = list(t["fields"])

    frozen_type_interface = {
        "interface_id": "decision_center_frozen_type_interface_v1",
        "enums": {
            "DecisionState": list(DECISION_STATE_ENUM),
            "DecisionReadiness": list(DECISION_READINESS_ENUM),
        },
        "types": list(FROZEN_CANDIDATE_TYPES),
        "type_count": len(FROZEN_CANDIDATE_TYPES),
        "enum_count": len(FROZEN_ENUM_TYPES),
        "required_base_fields": list(REQUIRED_TYPE_BASE_FIELDS),
        "fact_status_default": "not_fact",
        "fact_status_semantics_immutable": True,
        "decision_candidate_final_action_default": False,
        "decision_candidate_user_output_default": False,
        "downstream_handoff_direct_mount_default": False,
        "type_fields": type_field_map,
        **meta,
    }

    frozen_function_interface = {
        "interface_id": "decision_center_frozen_function_interface_v1",
        "functions": list(FROZEN_FUNCTIONS),
        "function_count": len(FROZEN_FUNCTIONS),
        "candidate_only_outputs": True,
        "runtime_execution": False,
        "task_execution": False,
        "user_output": False,
        **meta,
    }

    frozen_validator_interface = {
        "interface_id": "decision_center_frozen_validator_interface_v1",
        "validators": list(FROZEN_VALIDATORS),
        "validator_count": len(FROZEN_VALIDATORS),
        "reusable_by_downstream": True,
        **meta,
    }

    handoff_contract = {
        "contract_id": "decision_center_handoff_contract_v1",
        "rules": list(HANDOFF_RULES),
        "rule_count": len(HANDOFF_RULES),
        **meta,
    }

    downstream_output_contract = {
        "contract_id": "decision_center_downstream_output_contract_v1",
        "entries": list(DOWNSTREAM_OUTPUT_CONTRACT),
        "entry_count": len(DOWNSTREAM_OUTPUT_CONTRACT),
        "output_gate_ready": False,
        "task_manager_ready": False,
        "health_watchdog_ready": False,
        **meta,
    }

    forbidden_mutation_policy = {
        "policy_id": "decision_center_forbidden_mutation_policy_v1",
        "forbidden_mutations": list(FORBIDDEN_MUTATIONS),
        "mutation_count": len(FORBIDDEN_MUTATIONS),
        **meta,
    }

    change_control_policy = {
        "policy_id": "decision_center_change_control_policy_v1",
        "steps": list(CHANGE_CONTROL_STEPS),
        "step_count": len(CHANGE_CONTROL_STEPS),
        "change_executed_in_this_phase": False,
        **meta,
    }

    boundary_freeze = {
        "freeze_id": "decision_center_boundary_freeze_v1",
        "global_boundaries": {
            **{f: False for f in BOUNDARY_FALSE},
            "decision_center_files_created_now": True,
        },
        **meta,
    }

    downstream_readiness_matrix = {
        "matrix_id": "decision_center_downstream_readiness_matrix_v1",
        "entries": list(DOWNSTREAM_READINESS),
        "entry_count": len(DOWNSTREAM_READINESS),
        **meta,
    }

    non_claims = {
        "register_id": "decision_center_non_claims_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    route_decision = {
        "decision_id": "decision_center_route_decision_v1",
        "primary_next_phase": "Phase-Midplatform-Health-Watchdog-Mount-Planning-v1-001",
        "secondary_next_phase": "Phase-Midplatform-Task-Manager-Mount-Planning-v1-001",
        "deferred": [
            "Output Gate Mount Planning",
            "WorldModel-Memory Bridge Mount Planning",
            "Module Adapter Feedback Mount Planning",
        ],
        "rationale": list(ROUTE_RATIONALE),
        **meta,
    }

    planning_pass = len(blockers) == 0
    readiness = {
        "decision_id": "decision_center_foundation_handoff_readiness_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "foundation_frozen": True,
        "foundation_id": version_tag["foundation_id"],
        "depends_on": version_tag["depends_on"],
        "also_depends_on": version_tag["also_depends_on"],
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "primary_route_after_handoff": route_decision["primary_next_phase"],
        "non_claims": list(NON_CLAIMS),
        "foundation_id": version_tag["foundation_id"],
        "foundation_version": version_tag["version"],
        "depends_on": version_tag["depends_on"],
        "also_depends_on": version_tag["also_depends_on"],
        "runtime_status": version_tag["runtime_status"],
        **meta,
    }

    return {
        "summary": summary,
        "decision_center_foundation_handoff_scope": handoff_scope,
        "decision_center_foundation_version_tag": version_tag,
        "decision_center_frozen_type_interface": frozen_type_interface,
        "decision_center_frozen_function_interface": frozen_function_interface,
        "decision_center_frozen_validator_interface": frozen_validator_interface,
        "decision_center_handoff_contract": handoff_contract,
        "decision_center_downstream_output_contract": downstream_output_contract,
        "decision_center_forbidden_mutation_policy": forbidden_mutation_policy,
        "decision_center_change_control_policy": change_control_policy,
        "decision_center_boundary_freeze": boundary_freeze,
        "decision_center_downstream_readiness_matrix": downstream_readiness_matrix,
        "decision_center_non_claims": non_claims,
        "decision_center_route_decision": route_decision,
        "decision_center_foundation_handoff_readiness_decision": readiness,
    }
