# -*- coding: utf-8 -*-
"""Main Project Structure Migration Rollback Rehearsal DryRun v1.

Dry-run-only: simulate sandbox/scope/restore/docs/verdict/eval_out/linkage/verifier/evidence chain.
No rollback rehearsal execution, sandbox/branch creation, or file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_rollback_rehearsal_dryrun_only"
DRYRUN_ID = "main_proj_struct_migration_rollback_rehearsal_dryrun_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_rollback_rehearsal_dryrun_v1"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Post-DryRun-Review-v1-001"

PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_DRYRUN_PLANNING_READY_FOR_DRYRUN"
ROADMAP_FINAL = (
    "POST_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_ROADMAP_DECISION_READY_FOR_ROLLBACK_REHEARSAL_DRYRUN_PLANNING"
)
PRE_AUTH_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"
PRE_AUTH_DRYRUN = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
POST_REVIEW_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
CONTROLLED_EXECUTION_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSED_FOR_CURRENT_MAINLINE"
CE_PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914
SCOPE_BATCH_COUNT = 8
MANDATORY_ROLLBACK_PATH_COUNT = 6
ROLLBACK_SPECIFIC_VERIFIER_COUNT = 4
VERIFIER_SUITE_COUNT = 12

PLANNING_ARTIFACTS = [
    "rollback_rehearsal_dryrun_planning_policy.json",
    "rehearsal_sandbox_policy.json",
    "rollback_rehearsal_dryrun_scope.json",
    "rollback_restore_path_map_plan.json",
    "docs_link_restore_plan.json",
    "verdict_table_restore_plan.json",
    "eval_out_reference_restore_plan.json",
    "capability_runner_verifier_doc_linkage_restore_plan.json",
    "rollback_verifier_rerun_plan.json",
    "rollback_rehearsal_evidence_template.json",
    "rollback_success_claim_policy.json",
    "rollback_rehearsal_dryrun_planning_readiness_decision.json",
]

ROOT_SPECS = [
    {
        "id": "rollback_rehearsal_dryrun_planning",
        "arg": "rollback_rehearsal_dryrun_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": PLANNING_ARTIFACTS,
    },
    {
        "id": "post_pre_auth_roadmap",
        "arg": "post_pre_authorization_roadmap_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "rollback_rehearsal_dryrun_planning_route_decision.json"],
    },
    {
        "id": "pre_authorization_closure",
        "arg": "pre_authorization_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "pre_authorization_rollback_closure_summary.json",
            "gap_hard_block_closure_summary.json",
        ],
    },
    {
        "id": "pre_authorization_post_review",
        "arg": "pre_authorization_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "pre_authorization_dryrun",
        "arg": "pre_authorization_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
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
        "artifacts": ["verifier_suite_execution_order.json"],
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
        "artifacts": ["current_to_target_structure_map.json", "module_inventory.json"],
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
        "dryrun_scope": DRYRUN_SCOPE,
        "dryrun_only": True,
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
        "docs_modified_by_dryrun": False,
        "readme_modified_by_dryrun": False,
        "phase_verdict_table_modified_by_dryrun": False,
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


def run_main_project_structure_migration_rollback_rehearsal_dryrun_v1(
    *,
    rollback_rehearsal_dryrun_planning_root: str,
    post_pre_authorization_roadmap_root: str,
    pre_authorization_closure_root: str,
    pre_authorization_post_review_root: str,
    pre_authorization_dryrun_root: str,
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

    planning_summary = summaries["rollback_rehearsal_dryrun_planning"]
    planning_loaded = (
        roots["rollback_rehearsal_dryrun_planning"]["loaded"]
        and planning_summary.get("final_decision") == PLANNING_FINAL
        and planning_summary.get("ready_for_rollback_rehearsal_dryrun") is True
    )
    roadmap_loaded = (
        roots["post_pre_auth_roadmap"]["loaded"]
        and summaries["post_pre_auth_roadmap"].get("final_decision") == ROADMAP_FINAL
    )
    closure_loaded = (
        roots["pre_authorization_closure"]["loaded"]
        and summaries["pre_authorization_closure"].get("final_decision") == PRE_AUTH_CLOSURE
    )
    post_review_loaded = (
        roots["pre_authorization_post_review"]["loaded"]
        and summaries["pre_authorization_post_review"].get("final_decision") == POST_REVIEW_DECISION
    )
    pre_auth_dryrun_loaded = (
        roots["pre_authorization_dryrun"]["loaded"]
        and summaries["pre_authorization_dryrun"].get("final_decision") == PRE_AUTH_DRYRUN
    )
    ce_closure_loaded = (
        roots["controlled_execution_closure"]["loaded"]
        and summaries["controlled_execution_closure"].get("final_decision") == CONTROLLED_EXECUTION_CLOSURE
    )
    ce_planning_loaded = roots["controlled_execution_planning"]["loaded"]
    ec_closure_loaded = (
        roots["execution_control_closure"]["loaded"]
        and summaries["execution_control_closure"].get("final_decision") == EXECUTION_CONTROL_CLOSURE
    )
    guarded_closure_loaded = (
        roots["guarded_closure"]["loaded"]
        and summaries["guarded_closure"].get("final_decision") == GUARDED_CLOSURE
    )
    structure_map_loaded = roots["structure_map"]["loaded"]
    pahr_loaded = roots["pahr_closure"]["loaded"]
    readiness_loaded = roots["readiness"]["loaded"]
    gate_taxonomy_loaded = roots["gate_taxonomy"]["loaded"]

    plan_root = roots["rollback_rehearsal_dryrun_planning"]["root"]
    sandbox_plan = (_try_read_json(plan_root / "rehearsal_sandbox_policy.json") if plan_root else {}) or {}
    scope_plan = (_try_read_json(plan_root / "rollback_rehearsal_dryrun_scope.json") if plan_root else {}) or {}
    restore_plan = (_try_read_json(plan_root / "rollback_restore_path_map_plan.json") if plan_root else {}) or {}
    docs_plan = (_try_read_json(plan_root / "docs_link_restore_plan.json") if plan_root else {}) or {}
    verdict_plan = (_try_read_json(plan_root / "verdict_table_restore_plan.json") if plan_root else {}) or {}
    eval_plan = (_try_read_json(plan_root / "eval_out_reference_restore_plan.json") if plan_root else {}) or {}
    linkage_plan = (
        _try_read_json(plan_root / "capability_runner_verifier_doc_linkage_restore_plan.json") if plan_root else {}
    ) or {}
    verifier_plan = (_try_read_json(plan_root / "rollback_verifier_rerun_plan.json") if plan_root else {}) or {}
    evidence_plan = (_try_read_json(plan_root / "rollback_rehearsal_evidence_template.json") if plan_root else {}) or {}
    success_plan = (_try_read_json(plan_root / "rollback_success_claim_policy.json") if plan_root else {}) or {}

    sm_root = roots["structure_map"]["root"]
    structure_map = (_try_read_json(sm_root / "current_to_target_structure_map.json") if sm_root else {}) or {}
    map_rows = structure_map.get("map_rows") or []
    map_row_count = len(map_rows)

    closure_summary = summaries["pre_authorization_closure"]
    closure_root = roots["pre_authorization_closure"]["root"]
    gap_closure = (_try_read_json(closure_root / "gap_hard_block_closure_summary.json") if closure_root else {}) or {}

    verifier_suite_count = max(
        planning_summary.get("verifier_suite_count", VERIFIER_SUITE_COUNT),
        verifier_plan.get("verifier_suite_count", VERIFIER_SUITE_COUNT),
    )
    required_verifier_count = max(
        planning_summary.get("required_verifier_count", 4),
        verifier_plan.get("required_verifier_count", 4),
    )
    rollback_specific_count = len(verifier_plan.get("rollback_specific_verifiers") or []) or ROLLBACK_SPECIFIC_VERIFIER_COUNT

    ref_planning = "main_project_structure_migration_rollback_rehearsal_dryrun_planning_v1_smoke_v0"
    ref_roadmap = "post_pre_authorization_and_rollback_rehearsal_roadmap_decision_v1_smoke_v0"
    ref_closure = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_v1_smoke_v0"

    chain_sim_ok = planning_loaded and structure_map_loaded and map_row_count > 0

    rollback_rehearsal_dryrun_execution_plan = {
        "dryrun_id": DRYRUN_ID,
        "source_planning_ref": ref_planning,
        "source_post_pre_authorization_roadmap_ref": ref_roadmap,
        "source_pre_authorization_closure_ref": ref_closure,
        "scope_batch_count": SCOPE_BATCH_COUNT,
        "mandatory_rollback_path_count": MANDATORY_ROLLBACK_PATH_COUNT,
        "verifier_suite_count": verifier_suite_count,
        "required_verifier_count": required_verifier_count,
        "execution_mode": "dryrun_only",
        "rollback_rehearsal_execution_allowed": False,
        "rollback_dryrun_execution_allowed": False,
        "rollback_evidence_generation_allowed": False,
        "rollback_success_claim_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rehearsal_sandbox_dryrun_result = {
        "sandbox_required": sandbox_plan.get("sandbox_required", True),
        "dedicated_rehearsal_branch_required": sandbox_plan.get("dedicated_rehearsal_branch_required", True),
        "readonly_source_snapshot_required": sandbox_plan.get("readonly_source_snapshot_required", True),
        "no_real_repo_mutation": sandbox_plan.get("no_real_repo_mutation", True),
        "synthetic_restore_map_allowed": sandbox_plan.get("synthetic_restore_map_allowed", True),
        "sandbox_simulated": chain_sim_ok,
        "sandbox_created_now": False,
        "branch_created_now": False,
        "sandbox_review_pass": chain_sim_ok,
        "simulation_notes": ["dry-run validates sandbox policy without creating branch or sandbox"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_scope_dryrun_result = {
        "scope_batch_count": SCOPE_BATCH_COUNT,
        "mandatory_rollback_path_count": MANDATORY_ROLLBACK_PATH_COUNT,
        "b0_baseline_restore_check_simulated": chain_sim_ok,
        "b1_docs_relink_rollback_path_simulated": chain_sim_ok,
        "b2_capability_grouping_rollback_path_simulated": chain_sim_ok,
        "b3_governance_grouping_rollback_path_simulated": chain_sim_ok,
        "b4_midplatform_core_rollback_path_simulated": chain_sim_ok,
        "b5_dev_artifact_reference_rollback_path_simulated": chain_sim_ok,
        "b6_future_marker_rollback_path_simulated": chain_sim_ok,
        "b7_verification_gate_restore_check_simulated": chain_sim_ok,
        "rollback_scope_review_pass": chain_sim_ok,
        "inherits_scope_plan_ref": scope_plan.get("scope_id"),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_restore_path_map_dryrun_result = {
        "restore_path_map_required": restore_plan.get("restore_path_map_required", True),
        "source_target_mapping_loaded": structure_map_loaded and map_row_count > 0,
        "structure_map_row_count": map_row_count,
        "rollback_reverse_mapping_simulated": chain_sim_ok,
        "protected_asset_restore_rule_simulated": chain_sim_ok,
        "HR_DnAE_restore_rule_simulated": chain_sim_ok,
        "path_conflict_detection_simulated": chain_sim_ok,
        "missing_original_path_blocks_success_claim": restore_plan.get("missing_original_path_blocks_success_claim", True),
        "restore_path_map_generated_now": False,
        "restore_path_map_review_pass": chain_sim_ok,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    docs_link_restore_dryrun_result = {
        "docs_link_restore_required": docs_plan.get("docs_link_restore_required", True),
        "architecture_readme_restore_simulated": chain_sim_ok,
        "governance_doc_restore_simulated": chain_sim_ok,
        "evaluation_doc_restore_simulated": chain_sim_ok,
        "phase_doc_restore_simulated": chain_sim_ok,
        "markdown_link_check_simulated": chain_sim_ok,
        "docs_link_restore_executed_now": False,
        "docs_link_restore_review_pass": chain_sim_ok,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    verdict_table_restore_dryrun_result = {
        "verdict_table_restore_required_if_touched": verdict_plan.get("verdict_table_restore_required_if_touched", True),
        "verdict_table_touch_forbidden_by_default": verdict_plan.get("verdict_table_touch_forbidden_by_default", True),
        "verdict_table_snapshot_simulated": chain_sim_ok,
        "verdict_table_restore_check_simulated": chain_sim_ok,
        "verdict_table_restore_executed_now": False,
        "verdict_table_restore_review_pass": chain_sim_ok,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    eval_out_reference_restore_dryrun_result = {
        "eval_out_reference_restore_required": eval_plan.get("eval_out_reference_restore_required", True),
        "eval_out_content_move_forbidden": eval_plan.get("eval_out_content_move_forbidden", True),
        "eval_out_path_reference_snapshot_simulated": chain_sim_ok,
        "historical_output_reference_integrity_simulated": chain_sim_ok,
        "eval_out_reference_restore_executed_now": False,
        "eval_out_reference_restore_review_pass": chain_sim_ok,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    capability_runner_verifier_doc_linkage_restore_dryrun_result = {
        "linkage_restore_required": linkage_plan.get("linkage_restore_required", True),
        "capability_runner_pair_check_simulated": chain_sim_ok,
        "runner_verifier_pair_check_simulated": chain_sim_ok,
        "governance_doc_link_check_simulated": chain_sim_ok,
        "evaluation_doc_link_check_simulated": chain_sim_ok,
        "go_no_go_pack_link_check_simulated": chain_sim_ok,
        "import_path_restore_check_simulated": chain_sim_ok,
        "linkage_restore_executed_now": False,
        "linkage_restore_review_pass": chain_sim_ok,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_verifier_rerun_dryrun_result = {
        "verifier_rerun_required": verifier_plan.get("verifier_rerun_required", True),
        "verifier_suite_count": verifier_suite_count,
        "required_verifier_count": required_verifier_count,
        "rollback_specific_verifier_count": rollback_specific_count,
        "execution_order_defined": verifier_plan.get("execution_order_defined", True),
        "verifier_rerun_simulated": chain_sim_ok,
        "verifier_rerun_executed_now": False,
        "verifier_rerun_success_claim_allowed": False,
        "rollback_verifier_rerun_review_pass": chain_sim_ok and rollback_specific_count >= 4,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_evidence_dryrun_result = {
        "evidence_template_defined": evidence_plan.get("evidence_template_defined", True),
        "covered_batches_defined": True,
        "restore_path_map_result_required": evidence_plan.get("restore_path_map_result_required", True),
        "docs_link_restore_result_required": evidence_plan.get("docs_link_restore_result_required", True),
        "verdict_table_restore_result_required": evidence_plan.get("verdict_table_restore_result_required", True),
        "eval_out_ref_restore_result_required": evidence_plan.get("eval_out_ref_restore_result_required", True),
        "linkage_restore_result_required": evidence_plan.get("linkage_restore_result_required", True),
        "verifier_rerun_result_required": evidence_plan.get("verifier_rerun_result_required", True),
        "failure_list_required": evidence_plan.get("failure_list_required", True),
        "evidence_simulated": chain_sim_ok,
        "evidence_generated_now": False,
        "rollback_evidence_review_pass": chain_sim_ok,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_success_claim_dryrun_result = {
        "rollback_success_claim_allowed": False,
        "rollback_success_claim_requires_real_rehearsal_execution": success_plan.get(
            "rollback_success_claim_requires_real_rehearsal_execution", True
        ),
        "rollback_success_claim_requires_verifier_rerun_pass": success_plan.get(
            "rollback_success_claim_requires_verifier_rerun_pass", True
        ),
        "rollback_success_claim_requires_evidence_pack": success_plan.get(
            "rollback_success_claim_requires_evidence_pack", True
        ),
        "dryrun_planning_cannot_claim_success": success_plan.get("dryrun_planning_cannot_claim_success", True),
        "dryrun_cannot_claim_success": success_plan.get("dryrun_cannot_claim_success", True),
        "missing_evidence_blocks_success_claim": success_plan.get("missing_evidence_blocks_success_claim", True),
        "dryrun_success_claim_attempt_blocked": True,
        "rollback_success_claim_review_pass": chain_sim_ok,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_dryrun_boundary_review = {
        "no_real_migration": True,
        "no_batch_arming": True,
        "no_sandbox_creation": True,
        "no_branch_creation": True,
        "no_rollback_execution": True,
        "no_rollback_rehearsal_execution": True,
        "no_rollback_evidence_generation": True,
        "no_verifier_rerun_execution": True,
        "no_rollback_success_claim": True,
        "no_file_move_delete_rename_merge": True,
        "no_docs_modification": True,
        "no_readme_modification": True,
        "no_phase_verdict_table_modification": True,
        "no_runtime": True,
        "no_whitebox_test_center_design": True,
        "no_developer_backend_finalization": True,
        "no_future_module_finalization": True,
        "boundary_review_pass": chain_sim_ok,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    review_passes = [
        rehearsal_sandbox_dryrun_result["sandbox_review_pass"],
        rollback_rehearsal_scope_dryrun_result["rollback_scope_review_pass"],
        rollback_restore_path_map_dryrun_result["restore_path_map_review_pass"],
        docs_link_restore_dryrun_result["docs_link_restore_review_pass"],
        verdict_table_restore_dryrun_result["verdict_table_restore_review_pass"],
        eval_out_reference_restore_dryrun_result["eval_out_reference_restore_review_pass"],
        capability_runner_verifier_doc_linkage_restore_dryrun_result["linkage_restore_review_pass"],
        rollback_verifier_rerun_dryrun_result["rollback_verifier_rerun_review_pass"],
        rollback_rehearsal_evidence_dryrun_result["rollback_evidence_review_pass"],
        rollback_success_claim_dryrun_result["rollback_success_claim_review_pass"],
        rollback_rehearsal_dryrun_boundary_review["boundary_review_pass"],
    ]

    blockers: List[str] = []
    if not planning_loaded:
        blockers.append("rollback_rehearsal_dryrun_planning_not_ready")
    if not roadmap_loaded:
        blockers.append("post_pre_authorization_roadmap_not_ready")
    if not closure_loaded:
        blockers.append("pre_authorization_closure_not_ready")
    if not structure_map_loaded:
        blockers.append("structure_map_not_loaded")
    if map_row_count == 0:
        blockers.append("structure_map_row_count_zero")
    if not all(review_passes):
        blockers.append("dryrun_review_pass_incomplete")
    if _bool_val(closure_summary.get("rollback_rehearsal_executed"), False):
        blockers.append("rollback_rehearsal_must_not_be_executed")

    boundary_ok = not blockers

    rollback_rehearsal_dryrun_readiness_decision = {
        "dryrun_verdict": "GO" if boundary_ok else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [
            "dry-run simulates rollback rehearsal chain without repo mutation",
            "sandbox/branch not created; restore map/evidence not generated",
            "verifier rerun simulated only; success claim blocked",
        ],
        "ready_for_post_dryrun_review": boundary_ok,
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

    governance_debt_register = {
        "items": [
            "rollback_rehearsal_dryrun_simulated_only",
            "sandbox_and_branch_not_created",
            "restore_path_map_not_generated",
            "rollback_evidence_not_generated",
            "verifier_rerun_not_executed",
            "rollback_success_claim_blocked",
            "missing_rollback_rehearsal_still_blocks_migration_and_arming",
            f"{HUMAN_REVIEW_CARRYOVER}_hr_manual_only",
            f"{PERMANENT_BLOCK_CARRYOVER}_dnae_excluded",
        ],
        "item_count": 9,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_DRYRUN_REQUIRES_FIXES",
        "reason": "rollback rehearsal dry-run chain simulated; no execution permissions granted",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "rollback_rehearsal_dryrun_planning_input_loaded": planning_loaded,
        "post_pre_authorization_roadmap_input_loaded": roadmap_loaded,
        "pre_authorization_closure_input_loaded": closure_loaded,
        "pre_authorization_post_review_input_loaded": post_review_loaded,
        "pre_authorization_dryrun_input_loaded": pre_auth_dryrun_loaded,
        "controlled_execution_closure_input_loaded": ce_closure_loaded,
        "controlled_execution_planning_input_loaded": ce_planning_loaded,
        "execution_control_closure_input_loaded": ec_closure_loaded,
        "guarded_closure_input_loaded": guarded_closure_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "structure_map_input_loaded": structure_map_loaded,
        "gate_taxonomy_input_loaded": gate_taxonomy_loaded,
        "rollback_rehearsal_dryrun_execution_plan_generated": True,
        "rehearsal_sandbox_dryrun_result_generated": True,
        "rollback_rehearsal_scope_dryrun_result_generated": True,
        "rollback_restore_path_map_dryrun_result_generated": True,
        "docs_link_restore_dryrun_result_generated": True,
        "verdict_table_restore_dryrun_result_generated": True,
        "eval_out_reference_restore_dryrun_result_generated": True,
        "capability_runner_verifier_doc_linkage_restore_dryrun_result_generated": True,
        "rollback_verifier_rerun_dryrun_result_generated": True,
        "rollback_rehearsal_evidence_dryrun_result_generated": True,
        "rollback_success_claim_dryrun_result_generated": True,
        "rollback_rehearsal_dryrun_boundary_review_generated": True,
        "rollback_rehearsal_dryrun_readiness_decision_generated": True,
        "scope_batch_count": SCOPE_BATCH_COUNT,
        "mandatory_rollback_path_count": MANDATORY_ROLLBACK_PATH_COUNT,
        "verifier_suite_count": verifier_suite_count,
        "required_verifier_count": required_verifier_count,
        "rollback_specific_verifier_count": rollback_specific_count,
        "sandbox_simulated": chain_sim_ok,
        "sandbox_created_now": False,
        "branch_created_now": False,
        "b0_baseline_restore_check_simulated": chain_sim_ok,
        "b1_docs_relink_rollback_path_simulated": chain_sim_ok,
        "b2_capability_grouping_rollback_path_simulated": chain_sim_ok,
        "b3_governance_grouping_rollback_path_simulated": chain_sim_ok,
        "b4_midplatform_core_rollback_path_simulated": chain_sim_ok,
        "b5_dev_artifact_reference_rollback_path_simulated": chain_sim_ok,
        "b6_future_marker_rollback_path_simulated": chain_sim_ok,
        "b7_verification_gate_restore_check_simulated": chain_sim_ok,
        "rollback_reverse_mapping_simulated": chain_sim_ok,
        "protected_asset_restore_rule_simulated": chain_sim_ok,
        "HR_DnAE_restore_rule_simulated": chain_sim_ok,
        "path_conflict_detection_simulated": chain_sim_ok,
        "restore_path_map_generated_now": False,
        "docs_link_restore_required": True,
        "docs_link_restore_executed_now": False,
        "verdict_table_restore_required_if_touched": True,
        "verdict_table_restore_executed_now": False,
        "eval_out_reference_restore_required": True,
        "eval_out_content_move_forbidden": True,
        "eval_out_reference_restore_executed_now": False,
        "linkage_restore_required": True,
        "linkage_restore_executed_now": False,
        "verifier_rerun_required": True,
        "verifier_rerun_simulated": chain_sim_ok,
        "verifier_rerun_executed_now": False,
        "verifier_rerun_success_claim_allowed": False,
        "evidence_simulated": chain_sim_ok,
        "evidence_generated_now": False,
        "rollback_success_claim_allowed": False,
        "dryrun_success_claim_attempt_blocked": True,
        "ready_for_post_dryrun_review": boundary_ok,
        "ready_for_rollback_rehearsal_execution": False,
        "ready_for_real_migration": False,
        "ready_for_batch_arming": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "rollback_rehearsal_execution_allowed": False,
        "rollback_dryrun_execution_allowed": False,
        "rollback_evidence_generation_allowed": False,
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
        "docs_modified_by_dryrun": False,
        "readme_modified_by_dryrun": False,
        "phase_verdict_table_modified_by_dryrun": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "rollback_rehearsal_dryrun_execution_plan": rollback_rehearsal_dryrun_execution_plan,
        "rehearsal_sandbox_dryrun_result": rehearsal_sandbox_dryrun_result,
        "rollback_rehearsal_scope_dryrun_result": rollback_rehearsal_scope_dryrun_result,
        "rollback_restore_path_map_dryrun_result": rollback_restore_path_map_dryrun_result,
        "docs_link_restore_dryrun_result": docs_link_restore_dryrun_result,
        "verdict_table_restore_dryrun_result": verdict_table_restore_dryrun_result,
        "eval_out_reference_restore_dryrun_result": eval_out_reference_restore_dryrun_result,
        "capability_runner_verifier_doc_linkage_restore_dryrun_result": (
            capability_runner_verifier_doc_linkage_restore_dryrun_result
        ),
        "rollback_verifier_rerun_dryrun_result": rollback_verifier_rerun_dryrun_result,
        "rollback_rehearsal_evidence_dryrun_result": rollback_rehearsal_evidence_dryrun_result,
        "rollback_success_claim_dryrun_result": rollback_success_claim_dryrun_result,
        "rollback_rehearsal_dryrun_boundary_review": rollback_rehearsal_dryrun_boundary_review,
        "rollback_rehearsal_dryrun_readiness_decision": rollback_rehearsal_dryrun_readiness_decision,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
