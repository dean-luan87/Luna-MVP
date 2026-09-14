# -*- coding: utf-8 -*-
"""Main Project Structure Migration Rollback Rehearsal Execution Planning v1.

Planning-only: define real rollback rehearsal execution gates, sandbox/branch rules,
owner/operator approval, execution window, restore permissions, verifier rerun, evidence, failure response.
No rollback rehearsal execution, sandbox/branch creation, or file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_rollback_rehearsal_execution_planning_only"
PLANNING_ID = "main_proj_struct_migration_rollback_rehearsal_execution_planning_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_rollback_rehearsal_execution_planning_v1"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-DryRun-v1-001"

ROADMAP_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_ROADMAP_DECISION_READY_FOR_ROLLBACK_REHEARSAL_EXECUTION_PLANNING"
)
ROLLBACK_CLOSURE_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"
POST_REVIEW_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
DRYRUN_PLANNING_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_DRYRUN_PLANNING_READY_FOR_DRYRUN"
PRE_AUTH_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"
CONTROLLED_EXECUTION_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSED_FOR_CURRENT_MAINLINE"
CE_PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914
VERIFIER_SUITE_COUNT = 12
ROLLBACK_SPECIFIC_VERIFIER_COUNT = 4

EXECUTION_GATE_ITEMS: List[Tuple[str, str]] = [
    ("G01", "rollback_rehearsal_closure_closed"),
    ("G02", "pre_authorization_closure_closed"),
    ("G03", "dedicated_rehearsal_sandbox_approved"),
    ("G04", "dedicated_rehearsal_branch_approved"),
    ("G05", "owner_approval_required"),
    ("G06", "operator_acknowledgement_required"),
    ("G07", "authorization_package_required"),
    ("G08", "restore_path_map_plan_approved"),
    ("G09", "docs_verdict_evalout_linkage_restore_plan_approved"),
    ("G10", "verifier_rerun_plan_approved"),
    ("G11", "evidence_template_approved"),
    ("G12", "success_claim_gate_loaded"),
    ("G13", "failure_response_loaded"),
    ("G14", "protected_HR_DnAE_exclusion_snapshot_loaded"),
    ("G15", "rollback_rehearsal_dryrun_chain_reviewed"),
    ("G16", "structure_map_baseline_loaded"),
]

EXECUTION_WINDOW_REQUIREMENTS = [
    "clean_working_tree_proof",
    "dedicated_branch_proof",
    "backup_snapshot_proof",
    "no_unrelated_changes",
    "no_parallel_rehearsal",
    "one_rehearsal_scenario_at_a_time",
    "stop_condition_window",
    "rollback_verifier_rerun_window",
    "evidence_review_window",
]

FAILURE_RESPONSE_TYPES: List[Tuple[str, str, str]] = [
    ("sandbox_creation_failure", "high", "halt_rehearsal; do not proceed without isolated sandbox"),
    ("branch_creation_failure", "high", "halt_rehearsal; dedicated branch required"),
    ("restore_map_conflict", "critical", "halt_rehearsal; resolve path conflicts before restore"),
    ("docs_link_restore_failure", "high", "record_failure; blocks_success_claim"),
    ("verdict_table_restore_failure", "high", "record_failure; blocks_success_claim"),
    ("eval_out_ref_restore_failure", "high", "record_failure; blocks_success_claim"),
    ("linkage_restore_failure", "high", "record_failure; blocks_success_claim"),
    ("verifier_rerun_failure", "critical", "halt_rehearsal; blocks_success_claim"),
    ("evidence_generation_failure", "critical", "halt_rehearsal; blocks_success_claim"),
    ("protected_asset_touched", "critical", "halt_rehearsal; manual_override_required"),
    ("HR_DnAE_touched", "critical", "halt_rehearsal; excluded_from_automation"),
    ("unexpected_file_mutation", "critical", "halt_rehearsal; rollback rehearsal invalid"),
    ("runtime_enabled", "critical", "halt_rehearsal; boundary violation"),
    ("success_claim_without_evidence", "critical", "block_success_claim; audit_required"),
]

EXECUTION_NON_CLAIMS = [
    "rollback rehearsal execution planning 不等于 sandbox/branch 已创建",
    "planning 不等于 rollback rehearsal 已执行",
    "planning 不等于 restore path map 已生成（真实）",
    "planning 不等于 restore 操作已执行",
    "planning 不等于 verifier rerun 已执行",
    "planning 不等于 rollback evidence 已生成",
    "planning 不等于 rollback success 可声明",
    "ready_for_rollback_rehearsal_execution_dryrun 不等于 rehearsal execution 已授权",
    "execution_planning_cannot_claim_success=true",
]

ROOT_SPECS = [
    {
        "id": "rollback_rehearsal_roadmap",
        "arg": "rollback_rehearsal_roadmap_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "rollback_rehearsal_execution_planning_route_decision.json",
            "rollback_rehearsal_closure_status_summary.json",
        ],
    },
    {
        "id": "rollback_rehearsal_closure",
        "arg": "rollback_rehearsal_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "rollback_rehearsal_closure_summary.json",
            "rollback_rehearsal_closure_decision_summary.json",
            "closure_boundary_freeze.json",
            "rollback_rehearsal_non_claims_register.json",
            "deferred_rollback_rehearsal_action_pool.json",
            "completed_phase_matrix.json",
        ],
    },
    {
        "id": "rollback_rehearsal_post_review",
        "arg": "rollback_rehearsal_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "rollback_rehearsal_post_dryrun_readiness_decision.json"],
    },
    {
        "id": "rollback_rehearsal_dryrun",
        "arg": "rollback_rehearsal_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "rollback_rehearsal_dryrun_execution_plan.json",
            "rehearsal_sandbox_dryrun_result.json",
            "rollback_rehearsal_scope_dryrun_result.json",
            "rollback_restore_path_map_dryrun_result.json",
            "docs_link_restore_dryrun_result.json",
            "verdict_table_restore_dryrun_result.json",
            "eval_out_reference_restore_dryrun_result.json",
            "capability_runner_verifier_doc_linkage_restore_dryrun_result.json",
            "rollback_verifier_rerun_dryrun_result.json",
            "rollback_rehearsal_evidence_dryrun_result.json",
            "rollback_success_claim_dryrun_result.json",
        ],
    },
    {
        "id": "rollback_rehearsal_dryrun_planning",
        "arg": "rollback_rehearsal_dryrun_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "rollback_success_claim_policy.json",
            "rollback_rehearsal_evidence_template.json",
            "rollback_verifier_rerun_plan.json",
            "rollback_restore_path_map_plan.json",
            "docs_link_restore_plan.json",
            "verdict_table_restore_plan.json",
            "eval_out_reference_restore_plan.json",
            "capability_runner_verifier_doc_linkage_restore_plan.json",
        ],
    },
    {
        "id": "pre_authorization_closure",
        "arg": "pre_authorization_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "gap_hard_block_closure_summary.json"],
    },
    {
        "id": "controlled_execution_closure",
        "arg": "controlled_execution_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_execution_planning",
        "arg": "controlled_execution_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "verifier_suite_execution_order.json"],
    },
    {
        "id": "execution_control_closure",
        "arg": "execution_control_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "guarded_closure",
        "arg": "guarded_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "readiness",
        "arg": "readiness_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "pahr_closure",
        "arg": "pahr_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "consolidation_closure",
        "arg": "consolidation_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "structure_map",
        "arg": "structure_map_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "current_to_target_structure_map.json"],
    },
    {
        "id": "gate_taxonomy",
        "arg": "gate_taxonomy_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _bool_val(val: Any, default: bool = False) -> bool:
    if val is None:
        return default
    return bool(val)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary_payload = _try_read_json(root / summary_file) if root else None
    loaded = summary_payload is not None
    if root and artifacts:
        missing = [a for a in artifacts if _try_read_json(root / a) is None]
        loaded = loaded and not missing
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}}


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "planning_scope": PLANNING_SCOPE,
        "planning_only": True,
        "boundary_ok": True,
        "violations": [],
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "post_migration_tests_executed": False,
        "verifier_suite_executed": False,
        "rollback_executed": False,
        "rollback_rehearsal_executed": False,
        "docs_modified_by_planning": False,
        "readme_modified_by_planning": False,
        "phase_verdict_table_modified_by_planning": False,
        "existing_phase_result_changed": False,
        "runtime_enabled": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "file_operation_invoked": False,
        "stat_invoked": False,
        "exists_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "navigation_action_triggered": False,
        "speech_gate_invoked": False,
        "tts_invoked": False,
        "report_kind": kind,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_main_project_structure_migration_rollback_rehearsal_execution_planning_v1(
    *,
    rollback_rehearsal_roadmap_root: str,
    rollback_rehearsal_closure_root: str,
    rollback_rehearsal_post_review_root: str,
    rollback_rehearsal_dryrun_root: str,
    rollback_rehearsal_dryrun_planning_root: str,
    pre_authorization_closure_root: str,
    controlled_execution_closure_root: str,
    controlled_execution_planning_root: str,
    execution_control_closure_root: str,
    guarded_closure_root: str,
    readiness_root: str,
    pahr_closure_root: str,
    consolidation_closure_root: str,
    structure_map_root: str,
    gate_taxonomy_root: str,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}
    summaries = {key: roots[key]["summary"] for key in roots}

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    roadmap_summary = summaries["rollback_rehearsal_roadmap"]
    closure_summary = summaries["rollback_rehearsal_closure"]
    roadmap_loaded = (
        roots["rollback_rehearsal_roadmap"]["loaded"]
        and roadmap_summary.get("final_decision") == ROADMAP_FINAL
        and roadmap_summary.get("rollback_rehearsal_execution_planning_selected") is True
    )
    closure_loaded = (
        roots["rollback_rehearsal_closure"]["loaded"]
        and closure_summary.get("final_decision") == ROLLBACK_CLOSURE_DECISION
        and closure_summary.get("rollback_rehearsal_chain_closed") is True
    )
    post_review_loaded = (
        roots["rollback_rehearsal_post_review"]["loaded"]
        and summaries["rollback_rehearsal_post_review"].get("final_decision") == POST_REVIEW_DECISION
    )
    dryrun_loaded = (
        roots["rollback_rehearsal_dryrun"]["loaded"]
        and summaries["rollback_rehearsal_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    dryrun_planning_loaded = (
        roots["rollback_rehearsal_dryrun_planning"]["loaded"]
        and summaries["rollback_rehearsal_dryrun_planning"].get("final_decision") == DRYRUN_PLANNING_DECISION
    )
    pre_auth_closure_loaded = (
        roots["pre_authorization_closure"]["loaded"]
        and summaries["pre_authorization_closure"].get("final_decision") == PRE_AUTH_CLOSURE
    )
    ce_closure_loaded = (
        roots["controlled_execution_closure"]["loaded"]
        and summaries["controlled_execution_closure"].get("final_decision") == CONTROLLED_EXECUTION_CLOSURE
    )
    ce_planning_loaded = (
        roots["controlled_execution_planning"]["loaded"]
        and summaries["controlled_execution_planning"].get("final_decision") == CE_PLANNING_FINAL
    )
    ec_closure_loaded = (
        roots["execution_control_closure"]["loaded"]
        and summaries["execution_control_closure"].get("final_decision") == EXECUTION_CONTROL_CLOSURE
    )
    guarded_closure_loaded = (
        roots["guarded_closure"]["loaded"]
        and summaries["guarded_closure"].get("final_decision") == GUARDED_CLOSURE
    )
    pahr_loaded = roots["pahr_closure"]["loaded"]
    readiness_loaded = roots["readiness"]["loaded"]
    structure_map_loaded = roots["structure_map"]["loaded"]
    gate_taxonomy_loaded = roots["gate_taxonomy"]["loaded"]

    dp_root = roots["rollback_rehearsal_dryrun_planning"]["root"]
    success_claim_policy = (_try_read_json(dp_root / "rollback_success_claim_policy.json") if dp_root else {}) or {}
    verifier_rerun_plan = (_try_read_json(dp_root / "rollback_verifier_rerun_plan.json") if dp_root else {}) or {}
    evidence_template = (_try_read_json(dp_root / "rollback_rehearsal_evidence_template.json") if dp_root else {}) or {}

    ce_plan_root = roots["controlled_execution_planning"]["root"]
    verifier_order = (_try_read_json(ce_plan_root / "verifier_suite_execution_order.json") if ce_plan_root else {}) or {}
    ce_verifiers = verifier_order.get("verifiers") or []
    verifier_suite_count = len(ce_verifiers) if ce_verifiers else VERIFIER_SUITE_COUNT

    pre_auth_root = roots["pre_authorization_closure"]["root"]
    gap_closure = (_try_read_json(pre_auth_root / "gap_hard_block_closure_summary.json") if pre_auth_root else {}) or {}

    ref_roadmap = "main_project_structure_migration_rollback_rehearsal_roadmap_decision_v1_smoke_v0"
    ref_rollback_closure = "main_project_structure_migration_rollback_rehearsal_closure_v1_smoke_v0"
    ref_pre_auth_closure = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_v1_smoke_v0"
    ref_dryrun_planning = "main_project_structure_migration_rollback_rehearsal_dryrun_planning_v1_smoke_v0"

    gate_items = []
    for gate_id, gate_name in EXECUTION_GATE_ITEMS:
        gate_items.append(
            {
                "gate_item_id": gate_id,
                "gate_name": gate_name,
                "required": True,
                "satisfied_now": False,
                "blocks_rehearsal_execution": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    rehearsal_execution_gate = {
        "gate_id": "rehearsal_execution_gate_v1",
        "gate_items": gate_items,
        "gate_item_count": len(gate_items),
        "all_gates_must_pass_before_execution": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rehearsal_sandbox_execution_policy = {
        "sandbox_required": True,
        "dedicated_rehearsal_branch_required": True,
        "sandbox_creation_requires_owner_approval": True,
        "branch_creation_requires_operator_ack": True,
        "sandbox_must_be_isolated_from_main": True,
        "no_real_repo_mutation_until_execution_phase": True,
        "sandbox_created_now": False,
        "branch_created_now": False,
        "sandbox_creation_allowed_now": False,
        "branch_creation_allowed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    owner_requirements = [
        ("owner_approval_required", True),
        ("operator_ack_required", True),
        ("architecture_owner_required", True),
        ("governance_owner_required", True),
        ("evaluation_owner_required", True),
        ("capability_owner_required_if_capability_paths_touched", True),
        ("midplatform_owner_required_if_midplatform_paths_touched", True),
        ("docs_owner_required_if_docs_paths_touched", True),
    ]
    rehearsal_owner_operator_approval_policy = {
        **{k: v for k, v in owner_requirements},
        "owner_operator_approval_requirement_count": len(owner_requirements),
        "owner_approval_executed_now": False,
        "operator_ack_executed_now": False,
        "auto_confirm_allowed": False,
        "missing_approval_blocks_rehearsal_execution": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    window_items = []
    for req in EXECUTION_WINDOW_REQUIREMENTS:
        window_items.append(
            {
                "requirement_id": req,
                "required": True,
                "satisfied_now": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    rehearsal_execution_window_policy = {
        "requirements": window_items,
        "execution_window_requirement_count": len(window_items),
        "execution_window_required": True,
        "execution_window_opened_now": False,
        "execution_window_allowed_now": False,
        "missing_window_blocks_rehearsal_execution": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    restore_map_generation_permission_policy = {
        "restore_map_generation_required_before_rehearsal": True,
        "source_target_mapping_required": True,
        "reverse_mapping_required": True,
        "protected_asset_restore_rule_required": True,
        "HR_DnAE_restore_rule_required": True,
        "conflict_detection_required": True,
        "restore_map_plan_ref": f"{ref_dryrun_planning}/rollback_restore_path_map_plan.json",
        "restore_map_generation_allowed_now": False,
        "restore_map_generated_now": False,
        "missing_restore_map_blocks_rehearsal_execution": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    restore_operation_permission_policy = {
        "docs_link_restore_permission_required": True,
        "verdict_table_restore_permission_required_if_touched": True,
        "eval_out_reference_restore_permission_required": True,
        "linkage_restore_permission_required": True,
        "file_content_restore_forbidden_by_default": True,
        "protected_asset_restore_requires_manual_override": True,
        "restore_operation_allowed_now": False,
        "restore_operation_executed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_verifier_rerun_execution_policy = {
        "verifier_rerun_required": True,
        "verifier_suite_count": max(verifier_suite_count, VERIFIER_SUITE_COUNT),
        "rollback_specific_verifier_count": ROLLBACK_SPECIFIC_VERIFIER_COUNT,
        "execution_order_defined": verifier_rerun_plan.get("execution_order_defined", True),
        "verifier_rerun_execution_requires_sandbox": True,
        "verifier_rerun_execution_requires_restore_map": True,
        "verifier_rerun_execution_allowed_now": False,
        "verifier_rerun_executed_now": False,
        "verifier_rerun_failure_blocks_success_claim": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_evidence_generation_policy = {
        "rollback_evidence_required": True,
        "evidence_generation_requires_real_rehearsal_execution": True,
        "evidence_generation_requires_verifier_rerun_result": True,
        "evidence_generation_requires_failure_list": True,
        "evidence_template_ref": f"{ref_dryrun_planning}/rollback_rehearsal_evidence_template.json",
        "evidence_generation_allowed_now": False,
        "evidence_generated_now": False,
        "evidence_missing_blocks_success_claim": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    failure_entries = []
    for failure_type, severity, required_response in FAILURE_RESPONSE_TYPES:
        failure_entries.append(
            {
                "failure_type": failure_type,
                "severity": severity,
                "blocks_rehearsal_success": True,
                "blocks_real_migration": True,
                "required_response": required_response,
                "audit_required": severity in ("critical", "high"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    rollback_failure_response_policy = {
        "failure_responses": failure_entries,
        "failure_response_type_count": len(failure_entries),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_success_claim_gate = {
        "rollback_success_claim_allowed": False,
        "success_claim_requires_rehearsal_execution": True,
        "success_claim_requires_sandbox_branch_record": True,
        "success_claim_requires_restore_map_result": True,
        "success_claim_requires_docs_verdict_evalout_linkage_results": True,
        "success_claim_requires_verifier_rerun_pass": True,
        "success_claim_requires_evidence_pack": True,
        "success_claim_requires_no_boundary_violation": True,
        "success_claim_attempt_now_blocked": True,
        "inherits_dryrun_policy_ref": success_claim_policy.get("semantic_clarification"),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_execution_planning_policy = {
        "planning_id": PLANNING_ID,
        "planning_scope": PLANNING_SCOPE,
        "source_roadmap_ref": ref_roadmap,
        "source_rollback_rehearsal_closure_ref": ref_rollback_closure,
        "source_pre_authorization_closure_ref": ref_pre_auth_closure,
        "rehearsal_execution_gate_ref": "rehearsal_execution_gate.json",
        "rehearsal_sandbox_execution_policy_ref": "rehearsal_sandbox_execution_policy.json",
        "rehearsal_owner_operator_approval_policy_ref": "rehearsal_owner_operator_approval_policy.json",
        "rehearsal_execution_window_policy_ref": "rehearsal_execution_window_policy.json",
        "restore_map_generation_permission_policy_ref": "restore_map_generation_permission_policy.json",
        "restore_operation_permission_policy_ref": "restore_operation_permission_policy.json",
        "rollback_verifier_rerun_execution_policy_ref": "rollback_verifier_rerun_execution_policy.json",
        "rollback_evidence_generation_policy_ref": "rollback_evidence_generation_policy.json",
        "rollback_failure_response_policy_ref": "rollback_failure_response_policy.json",
        "rollback_success_claim_gate_ref": "rollback_success_claim_gate.json",
        "next_phase_recommendation": NEXT_PHASE,
        "planning_only": True,
        "rollback_rehearsal_execution_allowed": False,
        "sandbox_creation_allowed_now": False,
        "branch_creation_allowed_now": False,
        "restore_map_generation_allowed_now": False,
        "restore_operation_allowed_now": False,
        "verifier_rerun_execution_allowed_now": False,
        "rollback_evidence_generation_allowed_now": False,
        "rollback_success_claim_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    execution_non_claims_register = {
        "non_claims": EXECUTION_NON_CLAIMS,
        "non_claim_count": len(EXECUTION_NON_CLAIMS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "items": [
            "rollback_rehearsal_execution_planning_complete_but_rehearsal_not_executed",
            "sandbox_created_now=false; branch_created_now=false",
            "owner_approval_executed_now=false; operator_ack_executed_now=false",
            "restore_map_generated_now=false; evidence_generated_now=false",
            "missing_rollback_rehearsal_blocks_real_migration",
            "missing_rollback_rehearsal_blocks_batch_arming",
            f"{HUMAN_REVIEW_CARRYOVER}_hr_manual_only",
            f"{PERMANENT_BLOCK_CARRYOVER}_dnae_excluded",
            "rollback_success_claim_allowed=false",
        ],
        "item_count": 9,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not roadmap_loaded:
        blockers.append("rollback_rehearsal_roadmap_not_ready")
    if not closure_loaded:
        blockers.append("rollback_rehearsal_closure_not_ready")
    if not post_review_loaded:
        blockers.append("rollback_rehearsal_post_review_not_loaded")
    if not dryrun_loaded:
        blockers.append("rollback_rehearsal_dryrun_not_loaded")
    if not dryrun_planning_loaded:
        blockers.append("rollback_rehearsal_dryrun_planning_not_loaded")
    if not pre_auth_closure_loaded:
        blockers.append("pre_authorization_closure_not_confirmed")
    if not structure_map_loaded:
        blockers.append("structure_map_not_loaded")
    if not ce_planning_loaded:
        blockers.append("controlled_execution_planning_not_loaded")
    if len(gate_items) < 14:
        blockers.append("rehearsal_execution_gate_item_count_insufficient")
    if len(owner_requirements) < 8:
        blockers.append("owner_operator_approval_requirement_count_insufficient")
    if len(window_items) < 8:
        blockers.append("execution_window_requirement_count_insufficient")
    if len(failure_entries) < 12:
        blockers.append("failure_response_type_count_insufficient")
    if _bool_val(closure_summary.get("rollback_rehearsal_executed"), False):
        blockers.append("rollback_rehearsal_must_not_be_executed_yet")
    if _bool_val(closure_summary.get("sandbox_created_now"), False):
        blockers.append("sandbox_must_not_be_created_in_planning")
    if _bool_val(closure_summary.get("rollback_success_claim_allowed"), False):
        blockers.append("rollback_success_claim_must_remain_false")

    boundary_ok = not blockers

    rollback_rehearsal_execution_planning_readiness_decision = {
        "readiness_verdict": "ready_for_rollback_rehearsal_execution_dryrun" if boundary_ok else "requires_fixes",
        "blockers": blockers,
        "conditional_notes": [
            "defines real rollback rehearsal execution preconditions without executing rehearsal",
            "sandbox/branch/restore/verifier/evidence permissions planned only",
            "owner/operator approval and execution window required before future execution",
        ],
        "ready_for_rollback_rehearsal_execution_dryrun": boundary_ok,
        "ready_for_rollback_rehearsal_execution": False,
        "ready_for_real_migration": False,
        "ready_for_batch_arming": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "rollback_rehearsal_roadmap_input_loaded": roadmap_loaded,
        "rollback_rehearsal_closure_input_loaded": closure_loaded,
        "rollback_rehearsal_post_review_input_loaded": post_review_loaded,
        "rollback_rehearsal_dryrun_input_loaded": dryrun_loaded,
        "rollback_rehearsal_dryrun_planning_input_loaded": dryrun_planning_loaded,
        "pre_authorization_closure_input_loaded": pre_auth_closure_loaded,
        "controlled_execution_closure_input_loaded": ce_closure_loaded,
        "controlled_execution_planning_input_loaded": ce_planning_loaded,
        "execution_control_closure_input_loaded": ec_closure_loaded,
        "guarded_closure_input_loaded": guarded_closure_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "structure_map_input_loaded": structure_map_loaded,
        "gate_taxonomy_input_loaded": gate_taxonomy_loaded,
        "rollback_rehearsal_execution_policy_generated": True,
        "rehearsal_execution_gate_generated": True,
        "rehearsal_sandbox_execution_policy_generated": True,
        "rehearsal_owner_operator_approval_policy_generated": True,
        "rehearsal_execution_window_policy_generated": True,
        "restore_map_generation_permission_policy_generated": True,
        "restore_operation_permission_policy_generated": True,
        "rollback_verifier_rerun_execution_policy_generated": True,
        "rollback_evidence_generation_policy_generated": True,
        "rollback_failure_response_policy_generated": True,
        "rollback_success_claim_gate_generated": True,
        "rollback_rehearsal_execution_planning_readiness_decision_generated": True,
        "rehearsal_execution_gate_item_count": len(gate_items),
        "owner_operator_approval_requirement_count": len(owner_requirements),
        "execution_window_requirement_count": len(window_items),
        "failure_response_type_count": len(failure_entries),
        "verifier_suite_count": max(verifier_suite_count, VERIFIER_SUITE_COUNT),
        "rollback_specific_verifier_count": ROLLBACK_SPECIFIC_VERIFIER_COUNT,
        "rollback_rehearsal_execution_allowed": False,
        "sandbox_creation_allowed_now": False,
        "branch_creation_allowed_now": False,
        "sandbox_created_now": False,
        "branch_created_now": False,
        "owner_approval_executed_now": False,
        "operator_ack_executed_now": False,
        "auto_confirm_allowed": False,
        "execution_window_opened_now": False,
        "execution_window_allowed_now": False,
        "restore_map_generation_allowed_now": False,
        "restore_map_generated_now": False,
        "restore_operation_allowed_now": False,
        "restore_operation_executed_now": False,
        "verifier_rerun_execution_allowed_now": False,
        "verifier_rerun_executed_now": False,
        "evidence_generation_allowed_now": False,
        "evidence_generated_now": False,
        "rollback_success_claim_allowed": False,
        "success_claim_attempt_now_blocked": True,
        "ready_for_rollback_rehearsal_execution_dryrun": boundary_ok,
        "ready_for_rollback_rehearsal_execution": False,
        "ready_for_real_migration": False,
        "ready_for_batch_arming": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "rollback_rehearsal_executed": _bool_val(closure_summary.get("rollback_rehearsal_executed"), False),
        "missing_rollback_rehearsal_blocks_real_migration": gap_closure.get(
            "missing_rollback_rehearsal_blocks_real_migration", True
        ),
        "missing_rollback_rehearsal_blocks_batch_arming": gap_closure.get(
            "missing_rollback_rehearsal_blocks_batch_arming", True
        ),
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "post_migration_tests_executed": False,
        "verifier_suite_executed": False,
        "rollback_executed": False,
        "docs_modified_by_planning": False,
        "readme_modified_by_planning": False,
        "phase_verdict_table_modified_by_planning": False,
        "existing_phase_result_changed": False,
        "runtime_enabled": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "file_operation_invoked": False,
        "stat_invoked": False,
        "exists_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "navigation_action_triggered": False,
        "speech_gate_invoked": False,
        "tts_invoked": False,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_EXECUTION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_EXECUTION_PLANNING_REQUIRES_FIXES",
        "reason": "execution planning complete; simulate real rehearsal execution gates in dry-run",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "rollback_rehearsal_execution_planning_policy": rollback_rehearsal_execution_planning_policy,
        "rehearsal_execution_gate": rehearsal_execution_gate,
        "rehearsal_sandbox_execution_policy": rehearsal_sandbox_execution_policy,
        "rehearsal_owner_operator_approval_policy": rehearsal_owner_operator_approval_policy,
        "rehearsal_execution_window_policy": rehearsal_execution_window_policy,
        "restore_map_generation_permission_policy": restore_map_generation_permission_policy,
        "restore_operation_permission_policy": restore_operation_permission_policy,
        "rollback_verifier_rerun_execution_policy": rollback_verifier_rerun_execution_policy,
        "rollback_evidence_generation_policy": rollback_evidence_generation_policy,
        "rollback_failure_response_policy": rollback_failure_response_policy,
        "rollback_success_claim_gate": rollback_success_claim_gate,
        "rollback_rehearsal_execution_planning_readiness_decision": rollback_rehearsal_execution_planning_readiness_decision,
        "execution_non_claims_register": execution_non_claims_register,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
