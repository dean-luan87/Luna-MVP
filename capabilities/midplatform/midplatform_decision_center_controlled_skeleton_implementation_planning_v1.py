# -*- coding: utf-8 -*-
"""Luna Midplatform Decision Center Controlled Skeleton Implementation Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_decision_center_mount_dryrun_and_review_v1 import (
    DECISION_STATES,
    FINAL_DECISION_GO as MOUNT_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as MOUNT_DRYRUN_NEXT,
    PROCESSING_STEPS,
    READINESS_CLASSIFICATIONS,
    SAMPLE_FLOWS,
)

PHASE_ID = "Phase-Midplatform-Decision-Center-Controlled-Skeleton-Implementation-Planning-v1-001"
SCOPE = "midplatform_decision_center_controlled_skeleton_implementation_planning_only"
SOURCE_CHAIN = "midplatform_decision_center_controlled_skeleton_implementation_planning_v1"

UPSTREAM_MOUNT_DRYRUN_FINAL = MOUNT_DRYRUN_FINAL_GO
UPSTREAM_MOUNT_DRYRUN_NEXT = MOUNT_DRYRUN_NEXT

FINAL_DECISION_GO = (
    "MIDPLATFORM_DECISION_CENTER_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING_"
    "READY_FOR_IMPLEMENTATION_DRYRUN"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_DECISION_CENTER_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING_"
    "HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Decision-Center-Controlled-Skeleton-Implementation-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Decision-Center-Controlled-Skeleton-Issue-Review-v1-001"

UPSTREAM_MOUNT_DRYRUN_FILES: Tuple[str, ...] = (
    "mount_dryrun_readiness_decision_v1.json",
    "upstream_mount_contract_consumability_review_v1.json",
    "information_integration_frozen_dependency_review_v1.json",
    "mount_contract_10_section_review_v1.json",
    "input_contract_dryrun_v1.json",
    "output_contract_dryrun_v1.json",
    "processing_model_dryrun_v1.json",
    "decision_state_machine_dryrun_v1.json",
    "model_rule_algorithm_placement_review_v1.json",
    "governance_boundary_dryrun_v1.json",
    "health_boundary_dryrun_v1.json",
    "downstream_handoff_matrix_review_v1.json",
    "sample_flow_dryrun_v1.json",
    "failure_route_dryrun_review_v1.json",
    "mount_health_metric_scope_review_v1.json",
    "boundary_matrix_review_v1.json",
    "non_claims_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

UPSTREAM_II_HANDOFF_FILES: Tuple[str, ...] = (
    "information_integration_foundation_version_tag_v1.json",
    "information_integration_frozen_type_interface_v1.json",
    "information_integration_handoff_contract_v1.json",
)

II_FROZEN_OUTPUTS_REUSE: Tuple[str, ...] = (
    "DecisionContextCandidate",
    "ConflictCandidate",
    "GapCandidate",
    "RequiredObservationCandidate",
    "PriorityAttentionMapCandidate",
    "InformationAllocationCandidate",
    "TaskWorldSliceCandidate",
    "LiveWorldStateCandidate",
)

SKELETON_FILE_PLAN: Tuple[Dict[str, Any], ...] = (
    {
        "path": "capabilities/midplatform/core/decision_center_types_v1.py",
        "purpose": "DecisionState, DecisionReadiness enums and 5 core decision candidate dataclass types",
        "create_in_this_phase": False,
    },
    {
        "path": "capabilities/midplatform/core/decision_center_skeleton_v1.py",
        "purpose": "pure function candidate generators: validate, classify, evaluate, build decision candidates",
        "create_in_this_phase": False,
    },
    {
        "path": "capabilities/midplatform/core/decision_center_static_validators_v1.py",
        "purpose": "static validators for input/output/boundary/governance/II dependency",
        "create_in_this_phase": False,
    },
)

DECISION_STATE_ENUM: Tuple[str, ...] = DECISION_STATES

DECISION_READINESS_ENUM: Tuple[str, ...] = READINESS_CLASSIFICATIONS

REQUIRED_CANDIDATE_BASE_FIELDS: Tuple[str, ...] = ("candidate_id", "trace_ref", "fact_status")

CANDIDATE_TYPES: Tuple[Dict[str, Any], ...] = (
    {
        "type_name": "DecisionCandidate",
        "fields": (
            "candidate_id",
            "decision_context_ref",
            "readiness",
            "decision_state",
            "decision_summary",
            "recommended_handoff",
            "governance_check_ref",
            "health_refs",
            "conflict_refs",
            "gap_refs",
            "trace_ref",
            "fact_status",
            "final_action",
            "user_output",
        ),
        "fact_status_default": "not_fact",
        "final_action_default": False,
        "user_output_default": False,
    },
    {
        "type_name": "DecisionReadinessCandidate",
        "fields": (
            "candidate_id",
            "decision_context_ref",
            "readiness",
            "readiness_reason",
            "blocker_refs",
            "required_observation_refs",
            "health_review_refs",
            "governance_pending",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "DecisionBlockCandidate",
        "fields": (
            "candidate_id",
            "block_type",
            "block_reason",
            "blocked_refs",
            "forbidden_route",
            "recovery_or_hold_candidate",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "DecisionExplanationCandidate",
        "fields": (
            "candidate_id",
            "decision_candidate_ref",
            "explanation_summary",
            "evidence_refs",
            "conflict_summary",
            "gap_summary",
            "health_summary",
            "governance_summary",
            "trace_ref",
            "fact_status",
        ),
        "fact_status_default": "not_fact",
    },
    {
        "type_name": "DownstreamDecisionHandoffCandidate",
        "fields": (
            "candidate_id",
            "decision_candidate_ref",
            "task_manager_refs",
            "output_gate_refs",
            "health_watchdog_refs",
            "module_adapter_refs",
            "worldmodel_memory_bridge_refs",
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
        "function_name": "validate_decision_context_input",
        "inputs": ["DecisionContextCandidate", "guards"],
        "output": "validation_candidate",
        "checks": ["trace", "health", "candidate_not_fact", "governance_requirement"],
        "forbidden": ["runtime_execution", "final_action"],
    },
    {
        "function_name": "classify_decision_readiness",
        "inputs": ["DecisionContextCandidate", "conflicts", "gaps", "health_refs", "governance_ref"],
        "output": "DecisionReadinessCandidate",
        "forbidden": ["real_decision_execution"],
    },
    {
        "function_name": "evaluate_conflict_block_candidate",
        "inputs": ["DecisionContextCandidate", "conflicts"],
        "output": "DecisionBlockCandidate",
        "condition": "unresolved_conflict",
    },
    {
        "function_name": "evaluate_gap_observation_candidate",
        "inputs": ["DecisionContextCandidate", "gaps"],
        "output": "needs_observation / required_observation_handoff_candidate",
        "condition": "unresolved_gap",
    },
    {
        "function_name": "evaluate_health_review_candidate",
        "inputs": ["DecisionContextCandidate", "health_refs"],
        "output": "needs_health_review",
        "condition": "health_fault_or_missing_health",
    },
    {
        "function_name": "evaluate_governance_pending_candidate",
        "inputs": ["DecisionContextCandidate", "governance_ref"],
        "output": "blocked / governance_pending",
        "condition": "high_risk_missing_governance_ref",
    },
    {
        "function_name": "build_decision_candidate",
        "inputs": ["DecisionContextCandidate", "DecisionReadinessCandidate", "governance_ref"],
        "output": "DecisionCandidate",
        "final_action": False,
        "user_output": False,
    },
    {
        "function_name": "build_decision_explanation_candidate",
        "inputs": ["DecisionCandidate", "context"],
        "output": "DecisionExplanationCandidate",
        "forbidden": ["model_invocation"],
    },
    {
        "function_name": "build_downstream_decision_handoff_candidate",
        "inputs": ["DecisionCandidate", "DecisionReadinessCandidate", "routes"],
        "output": "DownstreamDecisionHandoffCandidate",
        "direct_mount": False,
    },
    {
        "function_name": "validate_decision_center_candidate",
        "inputs": ["candidate_object"],
        "output": "ValidationResult",
        "checks": ["candidate_not_fact", "trace", "health", "governance", "no_output", "no_action", "no_write"],
    },
)

STATIC_VALIDATORS: Tuple[str, ...] = (
    "validate_dc_input_contract",
    "validate_dc_output_candidate_only",
    "validate_dc_decision_not_final_action",
    "validate_dc_no_task_execution",
    "validate_dc_no_user_output",
    "validate_dc_no_memory_worldmodel_write",
    "validate_dc_governance_required_for_high_risk",
    "validate_dc_health_required",
    "validate_dc_no_information_integration_redefinition",
    "validate_dc_boundary_matrix",
)

PROCESSING_CHAIN: Tuple[str, ...] = (
    "validate_decision_context_input",
    "classify_decision_readiness",
    "evaluate_conflict_block_candidate",
    "evaluate_gap_observation_candidate",
    "evaluate_health_review_candidate",
    "evaluate_governance_pending_candidate",
    "build_decision_candidate",
    "build_decision_explanation_candidate",
    "build_downstream_decision_handoff_candidate",
)

GOVERNANCE_GUARD_RULES: Tuple[str, ...] = (
    "high_risk_decision_without_governance_check_ref must be blocked or governance_pending or not_ready",
    "unresolved conflict must not generate ready decision_candidate",
    "output routes remain forbidden in skeleton",
    "memory routes remain forbidden in skeleton",
    "worldmodel routes remain forbidden in skeleton",
    "runtime routes remain forbidden in skeleton",
    "decision_candidate is not final decision action",
    "decision_candidate is not user output",
    "do not bypass L0 Governance Gate",
    "do not redefine Information Integration",
)

HEALTH_GUARD_RULES: Tuple[str, ...] = (
    "missing health_refs → not_ready / health_review_candidate",
    "stale context → requires_observation",
    "low confidence → not_ready / requires_observation",
    "P0 safety unresolved → blocked or hold",
    "health_fault context → handoff to Health Watchdog later",
    "no real health runtime enabled",
)

II_DEPENDENCY_GUARD_RULES: Tuple[str, ...] = (
    "only consume midplatform_information_integration_foundation_v1 frozen candidate outputs",
    "must not redefine Information Integration",
    "must not modify Information Integration candidate types",
    "must not treat decision_context_candidate as final decision",
    "must not require Information Integration to enable runtime",
    "new fields require change_control via information_integration_change_control_policy",
)

SKELETON_SAMPLES: Tuple[Dict[str, Any], ...] = tuple(
    {
        "sample_id": flow["flow_id"],
        "description": f"DryRun sample for {flow['flow_id']}",
        "terminal": flow.get("outputs", ["decision_candidate"])[0],
    }
    for flow in SAMPLE_FLOWS
)

TEST_PLAN_CATEGORIES: Tuple[str, ...] = (
    "type_completeness",
    "candidate_not_fact",
    "decision_candidate_not_final_action",
    "no_user_output",
    "no_task_execution",
    "no_memory_worldmodel_write",
    "governance_required_for_high_risk",
    "health_required",
    "ii_frozen_dependency",
    "readiness_classification",
    "state_machine",
    "boundary_matrix",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Skeleton Planning ≠ skeleton implementation",
    "Skeleton Planning ≠ Decision Center mounted",
    "Skeleton Planning ≠ runtime enabled",
    "Skeleton Planning ≠ model invoked",
    "Skeleton Planning ≠ provider invoked",
    "Skeleton Planning ≠ final decision action",
    "Skeleton Planning ≠ task execution",
    "Skeleton Planning ≠ Output Gate ready",
    "Skeleton Planning ≠ user output",
    "Skeleton Planning ≠ Memory / WorldModel write",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_decision_center_controlled_skeleton_implementation_planning_only",
    "skeleton_plan_only",
    "decision_center_files_not_created_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "decision_center_files_created_now",
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
)

DEFAULT_MOUNT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_mount_dryrun_and_review"
)
DEFAULT_MOUNT_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_mount_planning"
)
DEFAULT_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_HANDOFF_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_foundation_handoff_planning"
)
DEFAULT_FREEZE_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_controlled_skeleton_implementation_planning"
)


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
        "ii_foundation_reuse_confirmed": True,
        "must_not_redefine_information_integration": True,
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


def run_midplatform_decision_center_controlled_skeleton_implementation_planning_v1(
    *,
    midplatform_decision_center_mount_dryrun_and_review_root: str,
    midplatform_decision_center_mount_planning_root: str,
    midplatform_information_integration_foundation_handoff_dryrun_and_review_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root: str,
    midplatform_information_integration_foundation_handoff_planning_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    mount_dr = Path(midplatform_decision_center_mount_dryrun_and_review_root).expanduser().resolve()
    mount_plan = Path(midplatform_decision_center_mount_planning_root).expanduser().resolve()
    handoff_dr = Path(midplatform_information_integration_foundation_handoff_dryrun_and_review_root).expanduser().resolve()
    handoff_plan = Path(
        midplatform_information_integration_foundation_handoff_planning_root or DEFAULT_HANDOFF_PLANNING_ROOT
    ).expanduser().resolve()
    freeze_dr = Path(midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = {
        **_planning_meta(),
        "output_root": str(out_root),
        "upstream_mount_dryrun_root": str(mount_dr),
        "upstream_mount_planning_root": str(mount_plan),
        "upstream_handoff_dryrun_root": str(handoff_dr),
        "upstream_handoff_planning_root": str(handoff_plan),
        "upstream_freeze_dryrun_root": str(freeze_dr),
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

    handoff_dr_vr = _try_read_json(handoff_dr / "verifier_report.json") or {}
    if handoff_dr_vr.get("verifier") != "GO":
        blockers.append("upstream II handoff dryrun verifier must be GO")

    freeze_dr_vr = _try_read_json(freeze_dr / "verifier_report.json") or {}
    if freeze_dr_vr.get("verifier") != "GO":
        blockers.append("upstream micro-os freeze dryrun verifier must be GO")

    upstream_dr: Dict[str, Any] = {}
    for fname in UPSTREAM_MOUNT_DRYRUN_FILES:
        data = _try_read_json(mount_dr / fname)
        if data is None:
            blockers.append(f"missing mount dryrun upstream: {fname}")
        upstream_dr[fname.replace("_v1.json", "").replace(".json", "")] = data

    upstream_ii: Dict[str, Any] = {}
    for fname in UPSTREAM_II_HANDOFF_FILES:
        data = _try_read_json(handoff_plan / fname)
        if data is None:
            blockers.append(f"missing II handoff upstream: {fname}")
        upstream_ii[fname.replace("_v1.json", "")] = data

    ii_version = upstream_ii.get("information_integration_foundation_version_tag") or {}
    ii_dep_review = upstream_dr.get("information_integration_frozen_dependency_review") or {}

    if ii_version.get("foundation_id") != "midplatform_information_integration_foundation_v1":
        blockers.append("II foundation_id mismatch")
    if ii_version.get("runtime_status") != "not_enabled":
        blockers.append("II runtime must be not_enabled")
    if ii_dep_review.get("ii_foundation_mutation_required") is True:
        blockers.append("II foundation mutation must not be required")

    dc_files_exist = any((repo_root / f["path"]).is_file() for f in SKELETON_FILE_PLAN)
    if dc_files_exist:
        blockers.append("decision center skeleton files must not exist in this phase")

    skeleton_scope = {
        "scope_id": "decision_center_skeleton_scope_v1",
        "module_id": "decision_center",
        "layer": "L7",
        "allowed": [
            "dataclass",
            "enum",
            "pure_function",
            "static_validator",
            "candidate_generator",
            "in_memory_stub",
        ],
        "forbidden": [
            "real_decision_center_runtime",
            "model_invocation",
            "provider_invocation",
            "task_execution",
            "memory_write",
            "worldmodel_write",
            "user_output",
            "final_action",
            "direct_mount",
            "information_integration_redefinition",
        ],
        "reuse_ii_frozen_outputs": list(II_FROZEN_OUTPUTS_REUSE),
        "must_not_redefine_information_integration": True,
        **meta,
    }

    skeleton_file_plan = {
        "plan_id": "decision_center_skeleton_file_plan_v1",
        "files": list(SKELETON_FILE_PLAN),
        "file_count": len(SKELETON_FILE_PLAN),
        "create_in_this_phase": False,
        "decision_center_files_created_now": False,
        **meta,
    }

    type_contract = {
        "contract_id": "decision_center_type_contract_v1",
        "enums": {
            "DecisionState": list(DECISION_STATE_ENUM),
            "DecisionReadiness": list(DECISION_READINESS_ENUM),
        },
        "candidate_types": list(CANDIDATE_TYPES),
        "type_count": len(CANDIDATE_TYPES),
        "required_base_fields": list(REQUIRED_CANDIDATE_BASE_FIELDS),
        "all_fact_status_not_fact": True,
        **meta,
    }

    function_contract = {
        "contract_id": "decision_center_function_contract_v1",
        "functions": list(PURE_FUNCTIONS),
        "function_count": len(PURE_FUNCTIONS),
        "reuse_ii_types": list(II_FROZEN_OUTPUTS_REUSE),
        "candidate_only_outputs": True,
        **meta,
    }

    static_validator_contract = {
        "contract_id": "decision_center_static_validator_contract_v1",
        "validators": list(STATIC_VALIDATORS),
        "validator_count": len(STATIC_VALIDATORS),
        **meta,
    }

    processing_chain_contract = {
        "contract_id": "decision_center_processing_chain_contract_v1",
        "chain": list(PROCESSING_CHAIN),
        "chain_count": len(PROCESSING_CHAIN),
        "candidate_only": True,
        "aligns_with_mount_processing_steps": list(PROCESSING_STEPS),
        **meta,
    }

    governance_guard_plan = {
        "plan_id": "decision_center_governance_guard_plan_v1",
        "rules": list(GOVERNANCE_GUARD_RULES),
        "rule_count": len(GOVERNANCE_GUARD_RULES),
        **meta,
    }

    health_guard_plan = {
        "plan_id": "decision_center_health_guard_plan_v1",
        "rules": list(HEALTH_GUARD_RULES),
        "rule_count": len(HEALTH_GUARD_RULES),
        **meta,
    }

    ii_dependency_guard_plan = {
        "plan_id": "decision_center_information_integration_dependency_guard_plan_v1",
        "rules": list(II_DEPENDENCY_GUARD_RULES),
        "rule_count": len(II_DEPENDENCY_GUARD_RULES),
        **meta,
    }

    sample_plan = {
        "plan_id": "decision_center_sample_plan_v1",
        "samples": list(SKELETON_SAMPLES),
        "sample_count": len(SKELETON_SAMPLES),
        **meta,
    }

    test_plan = {
        "plan_id": "decision_center_test_plan_v1",
        "categories": list(TEST_PLAN_CATEGORIES),
        "category_count": len(TEST_PLAN_CATEGORIES),
        "execution_phase": "Implementation DryRun",
        "tests": [{"test_id": f"test_{cat}", "category": cat} for cat in TEST_PLAN_CATEGORIES],
        **meta,
    }

    skeleton_boundary_matrix = {
        "matrix_id": "decision_center_skeleton_boundary_matrix_v1",
        "global_boundaries": {f: False for f in BOUNDARY_FALSE},
        **meta,
    }

    skeleton_non_claims = {
        "register_id": "decision_center_skeleton_non_claims_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    planning_pass = len(blockers) == 0
    readiness = {
        "decision_id": "decision_center_skeleton_planning_readiness_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "skeleton_scope_defined": True,
        "file_plan_defined": True,
        "decision_center_files_created_now": False,
        "ii_foundation_reuse_confirmed": True,
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
        "decision_center_skeleton_scope": skeleton_scope,
        "decision_center_skeleton_file_plan": skeleton_file_plan,
        "decision_center_type_contract": type_contract,
        "decision_center_function_contract": function_contract,
        "decision_center_static_validator_contract": static_validator_contract,
        "decision_center_processing_chain_contract": processing_chain_contract,
        "decision_center_governance_guard_plan": governance_guard_plan,
        "decision_center_health_guard_plan": health_guard_plan,
        "decision_center_information_integration_dependency_guard_plan": ii_dependency_guard_plan,
        "decision_center_sample_plan": sample_plan,
        "decision_center_test_plan": test_plan,
        "decision_center_skeleton_boundary_matrix": skeleton_boundary_matrix,
        "decision_center_skeleton_non_claims": skeleton_non_claims,
        "decision_center_skeleton_planning_readiness_decision": readiness,
    }
