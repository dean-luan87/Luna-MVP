# -*- coding: utf-8 -*-
"""Main Project Structure Migration Rollback Rehearsal DryRun Planning v1.

Planning-only: define rehearsal sandbox, B0–B7 restore paths, verifier rerun order, evidence template.
No rollback rehearsal execution, sandbox/branch creation, or file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_rollback_rehearsal_dryrun_planning_only"
PLANNING_ID = "main_proj_struct_migration_rollback_rehearsal_dryrun_planning_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_rollback_rehearsal_dryrun_planning_v1"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_DRYRUN_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-v1-001"

ROADMAP_FINAL = (
    "POST_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_ROADMAP_DECISION_READY_FOR_ROLLBACK_REHEARSAL_DRYRUN_PLANNING"
)
PRE_AUTH_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"
POST_REVIEW_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_PLANNING_READY_FOR_DRYRUN"
CONTROLLED_EXECUTION_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSED_FOR_CURRENT_MAINLINE"
CE_PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914
SCOPE_BATCH_COUNT = 8
MANDATORY_ROLLBACK_PATH_COUNT = 6
VERIFIER_SUITE_COUNT = 12
REQUIRED_VERIFIER_COUNT = 4

BATCH_ROLLBACK_PATHS = [
    ("B0", "baseline_restore_check", True),
    ("B1", "docs_relink_rollback_path", True),
    ("B2", "capability_grouping_rollback_path", True),
    ("B3", "governance_grouping_rollback_path", True),
    ("B4", "midplatform_core_rollback_path", True),
    ("B5", "developer_artifact_reference_rollback_path", True),
    ("B6", "future_marker_rollback_path", True),
    ("B7", "verification_gate_restore_check", True),
]

ROLLBACK_SPECIFIC_VERIFIERS = [
    ("RV01", "rollback_restore_path_map_verifier", 1),
    ("RV02", "rollback_docs_link_restore_verifier", 2),
    ("RV03", "rollback_eval_out_reference_restore_verifier", 3),
    ("RV04", "rollback_rehearsal_evidence_verifier", 4),
]

EXECUTION_NON_CLAIMS = [
    "rollback rehearsal dry-run planning 不等于 sandbox/branch 已创建",
    "planning 不等于 rollback rehearsal dry-run 已执行",
    "planning 不等于 rollback rehearsal 已执行",
    "planning 不等于 restore path map 已生成（真实）",
    "planning 不等于 rollback evidence 已生成",
    "planning 不等于 rollback success 可声明",
    "planning 不等于 verifier rerun 已执行",
    "ready_for_rollback_rehearsal_dryrun 不等于 file move 已授权",
    "dryrun_planning_cannot_claim_success=true",
]

ROOT_SPECS = [
    {
        "id": "post_pre_auth_roadmap",
        "arg": "post_pre_authorization_roadmap_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "rollback_rehearsal_dryrun_planning_route_decision.json",
            "pre_authorization_closure_status_summary.json",
        ],
    },
    {
        "id": "pre_authorization_closure",
        "arg": "pre_authorization_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "pre_authorization_rollback_closure_summary.json",
            "pre_authorization_closure_decision_summary.json",
            "gap_hard_block_closure_summary.json",
            "pre_authorization_non_claims_register.json",
            "semantic_clarification_record.json",
            "deferred_pre_authorization_action_pool.json",
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
        "id": "pre_authorization_planning",
        "arg": "pre_authorization_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "rollback_rehearsal_scope.json",
            "rollback_rehearsal_plan.json",
            "rollback_rehearsal_evidence_template.json",
            "batch_arming_precondition_record.json",
            "authorization_blocker_policy.json",
        ],
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
        "artifacts": [
            "summary.json",
            "controlled_execution_batch_plan.json",
            "post_batch_test_execution_order.json",
            "verifier_suite_execution_order.json",
        ],
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


def run_main_project_structure_migration_rollback_rehearsal_dryrun_planning_v1(
    *,
    post_pre_authorization_roadmap_root: str,
    pre_authorization_closure_root: str,
    pre_authorization_post_review_root: str,
    pre_authorization_dryrun_root: str,
    pre_authorization_planning_root: str,
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

    roadmap_summary = summaries["post_pre_auth_roadmap"]
    closure_summary = summaries["pre_authorization_closure"]
    roadmap_loaded = (
        roots["post_pre_auth_roadmap"]["loaded"]
        and roadmap_summary.get("final_decision") == ROADMAP_FINAL
        and roadmap_summary.get("rollback_rehearsal_dryrun_planning_selected") is True
    )
    closure_loaded = (
        roots["pre_authorization_closure"]["loaded"]
        and closure_summary.get("final_decision") == PRE_AUTH_CLOSURE
        and closure_summary.get("pre_authorization_rollback_rehearsal_chain_closed") is True
    )
    post_review_loaded = (
        roots["pre_authorization_post_review"]["loaded"]
        and summaries["pre_authorization_post_review"].get("final_decision") == POST_REVIEW_DECISION
    )
    dryrun_loaded = (
        roots["pre_authorization_dryrun"]["loaded"]
        and summaries["pre_authorization_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    planning_loaded = (
        roots["pre_authorization_planning"]["loaded"]
        and summaries["pre_authorization_planning"].get("final_decision") == PLANNING_DECISION
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
    structure_map_loaded = roots["structure_map"]["loaded"]
    pahr_loaded = roots["pahr_closure"]["loaded"]
    readiness_loaded = roots["readiness"]["loaded"]
    gate_taxonomy_loaded = roots["gate_taxonomy"]["loaded"]

    sm_root = roots["structure_map"]["root"]
    structure_map = (_try_read_json(sm_root / "current_to_target_structure_map.json") if sm_root else {}) or {}
    module_inventory = (_try_read_json(sm_root / "module_inventory.json") if sm_root else {}) or {}
    map_rows = structure_map.get("map_rows") or []
    map_row_count = len(map_rows)
    inventory_modules = module_inventory.get("modules") or module_inventory.get("module_entries") or []
    inventory_count = len(inventory_modules) if isinstance(inventory_modules, list) else module_inventory.get("module_count", 0)

    pa_plan_root = roots["pre_authorization_planning"]["root"]
    pa_scope = (_try_read_json(pa_plan_root / "rollback_rehearsal_scope.json") if pa_plan_root else {}) or {}
    pa_evidence_tpl = (_try_read_json(pa_plan_root / "rollback_rehearsal_evidence_template.json") if pa_plan_root else {}) or {}
    ce_plan_root = roots["controlled_execution_planning"]["root"]
    verifier_order = (_try_read_json(ce_plan_root / "verifier_suite_execution_order.json") if ce_plan_root else {}) or {}
    ce_verifiers = verifier_order.get("verifiers") or []
    verifier_suite_count = len(ce_verifiers) if ce_verifiers else VERIFIER_SUITE_COUNT

    closure_root = roots["pre_authorization_closure"]["root"]
    gap_closure = (_try_read_json(closure_root / "gap_hard_block_closure_summary.json") if closure_root else {}) or {}

    ref_roadmap = "post_pre_authorization_and_rollback_rehearsal_roadmap_decision_v1_smoke_v0"
    ref_closure = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_v1_smoke_v0"
    ref_ce_plan = "main_project_structure_migration_controlled_execution_planning_v1_smoke_v0"
    ref_structure_map = "luna_project_module_inventory_and_structure_map_dryrun_v1_smoke_v0"

    rehearsal_sandbox_policy = {
        "sandbox_required": True,
        "dedicated_rehearsal_branch_required": True,
        "no_real_repo_mutation": True,
        "no_file_move_allowed": True,
        "no_file_delete_allowed": True,
        "no_file_rename_allowed": True,
        "no_module_merge_allowed": True,
        "readonly_source_snapshot_required": True,
        "synthetic_restore_map_allowed": True,
        "sandbox_created_now": False,
        "branch_created_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    scope_batches = []
    for batch_id, path_name, mandatory in BATCH_ROLLBACK_PATHS:
        scope_batches.append(
            {
                "batch_id": batch_id,
                "rollback_path_name": path_name,
                "mandatory": mandatory,
                "dryrun_simulation_required": True,
                "execution_allowed_now": False,
                "simulated_now": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    rollback_rehearsal_dryrun_scope = {
        "scope_id": "rollback_rehearsal_dryrun_scope_v1",
        "batches": scope_batches,
        "scope_batch_count": SCOPE_BATCH_COUNT,
        "mandatory_rollback_path_count": MANDATORY_ROLLBACK_PATH_COUNT,
        "b1_b6_rollback_path_required": True,
        "b0_baseline_restore_check_required": True,
        "b7_verification_gate_restore_check_required": True,
        "scope_planning_only": True,
        "inherits_pre_auth_scope_ref": pa_scope.get("rehearsal_scope_id"),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_restore_path_map_plan = {
        "restore_path_map_required": True,
        "source_target_mapping_loaded": structure_map_loaded and map_row_count > 0,
        "current_to_target_structure_map_ref": ref_structure_map,
        "structure_map_row_count": map_row_count,
        "module_inventory_ref": ref_structure_map,
        "module_inventory_count": inventory_count,
        "rollback_reverse_mapping_required": True,
        "protected_asset_restore_rule_required": True,
        "HR_DnAE_restore_rule_required": True,
        "path_conflict_detection_required": True,
        "missing_original_path_blocks_success_claim": True,
        "restore_path_map_generated_now": False,
        "synthetic_reverse_map_allowed_in_dryrun": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    docs_link_restore_plan = {
        "docs_link_restore_required": True,
        "architecture_readme_restore_required": True,
        "governance_doc_restore_required": True,
        "evaluation_doc_restore_required": True,
        "phase_doc_restore_required": True,
        "markdown_link_check_required": True,
        "docs_link_restore_executed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    verdict_table_restore_plan = {
        "verdict_table_restore_required_if_touched": True,
        "verdict_table_touch_forbidden_by_default": True,
        "verdict_table_snapshot_required": True,
        "verdict_table_restore_check_required": True,
        "verdict_table_restore_executed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    eval_out_reference_restore_plan = {
        "eval_out_reference_restore_required": True,
        "eval_out_content_move_forbidden": True,
        "eval_out_path_reference_snapshot_required": True,
        "historical_output_reference_integrity_required": True,
        "eval_out_reference_restore_executed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    capability_runner_verifier_doc_linkage_restore_plan = {
        "linkage_restore_required": True,
        "capability_runner_pair_check_required": True,
        "runner_verifier_pair_check_required": True,
        "governance_doc_link_check_required": True,
        "evaluation_doc_link_check_required": True,
        "go_no_go_pack_link_check_required": True,
        "import_path_restore_check_required": True,
        "linkage_restore_executed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_verifier_entries = []
    for vid, vname, order in ROLLBACK_SPECIFIC_VERIFIERS:
        rollback_verifier_entries.append(
            {
                "verifier_id": vid,
                "verifier_name": vname,
                "execution_order": order,
                "rollback_specific": True,
                "required": True,
                "execution_allowed_now": False,
                "executed_now": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    rollback_verifier_rerun_plan = {
        "verifier_rerun_required": True,
        "verifier_suite_count": max(verifier_suite_count, VERIFIER_SUITE_COUNT),
        "required_verifier_count": REQUIRED_VERIFIER_COUNT,
        "rollback_specific_verifier_required": True,
        "rollback_specific_verifiers": rollback_verifier_entries,
        "controlled_execution_verifier_order_ref": ref_ce_plan,
        "execution_order_defined": True,
        "verifier_rerun_executed_now": False,
        "verifier_rerun_success_claim_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_evidence_template = {
        "evidence_template_defined": True,
        "rehearsal_id": "rollback_rehearsal_dryrun_evidence_v1",
        "covered_batches": ["B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"],
        "restore_path_map_result_required": True,
        "docs_link_restore_result_required": True,
        "verdict_table_restore_result_required": True,
        "eval_out_ref_restore_result_required": True,
        "linkage_restore_result_required": True,
        "verifier_rerun_result_required": True,
        "failure_list_required": True,
        "evidence_generated_now": False,
        "inherits_pre_auth_template_ref": pa_evidence_tpl.get("rehearsal_id"),
        "rollback_success_claim_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_success_claim_policy = {
        "rollback_success_claim_allowed": False,
        "rollback_success_claim_requires_real_rehearsal_execution": True,
        "rollback_success_claim_requires_verifier_rerun_pass": True,
        "rollback_success_claim_requires_evidence_pack": True,
        "dryrun_planning_cannot_claim_success": True,
        "dryrun_cannot_claim_success": True,
        "missing_evidence_blocks_success_claim": True,
        "semantic_clarification": "dryrun planning and dryrun execution cannot claim rollback success",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_dryrun_planning_policy = {
        "planning_id": PLANNING_ID,
        "planning_scope": PLANNING_SCOPE,
        "source_roadmap_ref": ref_roadmap,
        "source_pre_authorization_closure_ref": ref_closure,
        "source_controlled_execution_plan_ref": ref_ce_plan,
        "rehearsal_sandbox_policy_ref": "rehearsal_sandbox_policy.json",
        "rollback_rehearsal_dryrun_scope_ref": "rollback_rehearsal_dryrun_scope.json",
        "rollback_restore_path_map_plan_ref": "rollback_restore_path_map_plan.json",
        "docs_link_restore_plan_ref": "docs_link_restore_plan.json",
        "verdict_table_restore_plan_ref": "verdict_table_restore_plan.json",
        "eval_out_reference_restore_plan_ref": "eval_out_reference_restore_plan.json",
        "capability_runner_verifier_doc_linkage_restore_plan_ref": (
            "capability_runner_verifier_doc_linkage_restore_plan.json"
        ),
        "rollback_verifier_rerun_plan_ref": "rollback_verifier_rerun_plan.json",
        "rollback_rehearsal_evidence_template_ref": "rollback_rehearsal_evidence_template.json",
        "rollback_success_claim_policy_ref": "rollback_success_claim_policy.json",
        "next_phase_recommendation": NEXT_PHASE,
        "planning_only": True,
        "rollback_rehearsal_execution_allowed": False,
        "rollback_dryrun_execution_allowed": False,
        "rollback_evidence_generation_allowed": False,
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
            "rollback_rehearsal_dryrun_planning_complete_but_sandbox_not_created",
            "rollback_rehearsal_not_executed",
            "rollback_evidence_not_generated",
            "missing_rollback_rehearsal_blocks_real_migration",
            "missing_rollback_rehearsal_blocks_batch_arming",
            f"{HUMAN_REVIEW_CARRYOVER}_hr_manual_only",
            f"{PERMANENT_BLOCK_CARRYOVER}_dnae_excluded",
            "armed_batch_count=0",
            "rollback_success_claim_allowed=false",
        ],
        "item_count": 9,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not roadmap_loaded:
        blockers.append("post_pre_authorization_roadmap_not_ready")
    if not closure_loaded:
        blockers.append("pre_authorization_closure_not_ready")
    if not planning_loaded:
        blockers.append("pre_authorization_planning_not_loaded")
    if not structure_map_loaded:
        blockers.append("structure_map_not_loaded")
    if not ce_planning_loaded:
        blockers.append("controlled_execution_planning_not_loaded")
    if map_row_count == 0:
        blockers.append("structure_map_row_count_zero")
    if len(scope_batches) != SCOPE_BATCH_COUNT:
        blockers.append("scope_batch_count_mismatch")
    if _bool_val(closure_summary.get("rollback_rehearsal_executed"), False):
        blockers.append("rollback_rehearsal_must_not_be_executed_yet")

    boundary_ok = not blockers

    rollback_rehearsal_dryrun_planning_readiness_decision = {
        "readiness_verdict": "ready_for_rollback_rehearsal_dryrun" if boundary_ok else "requires_fixes",
        "blockers": blockers,
        "conditional_notes": [
            "defines how future rollback rehearsal dry-run will simulate restore without repo mutation",
            "sandbox/branch planned but not created",
            "B0–B7 restore paths, docs/verdict/eval_out/linkage/verifier rerun planned only",
        ],
        "ready_for_rollback_rehearsal_dryrun": boundary_ok,
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
        "post_pre_authorization_roadmap_input_loaded": roadmap_loaded,
        "pre_authorization_closure_input_loaded": closure_loaded,
        "pre_authorization_post_review_input_loaded": post_review_loaded,
        "pre_authorization_dryrun_input_loaded": dryrun_loaded,
        "pre_authorization_planning_input_loaded": planning_loaded,
        "controlled_execution_closure_input_loaded": ce_closure_loaded,
        "controlled_execution_planning_input_loaded": ce_planning_loaded,
        "execution_control_closure_input_loaded": ec_closure_loaded,
        "guarded_closure_input_loaded": guarded_closure_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "structure_map_input_loaded": structure_map_loaded,
        "gate_taxonomy_input_loaded": gate_taxonomy_loaded,
        "rollback_rehearsal_dryrun_planning_policy_generated": True,
        "rehearsal_sandbox_policy_generated": True,
        "rollback_rehearsal_dryrun_scope_generated": True,
        "rollback_restore_path_map_plan_generated": True,
        "docs_link_restore_plan_generated": True,
        "verdict_table_restore_plan_generated": True,
        "eval_out_reference_restore_plan_generated": True,
        "capability_runner_verifier_doc_linkage_restore_plan_generated": True,
        "rollback_verifier_rerun_plan_generated": True,
        "rollback_rehearsal_evidence_template_generated": True,
        "rollback_success_claim_policy_generated": True,
        "rollback_rehearsal_dryrun_planning_readiness_decision_generated": True,
        "scope_batch_count": SCOPE_BATCH_COUNT,
        "mandatory_rollback_path_count": MANDATORY_ROLLBACK_PATH_COUNT,
        "b1_b6_rollback_path_required": True,
        "b0_baseline_restore_check_required": True,
        "b7_verification_gate_restore_check_required": True,
        "sandbox_required": True,
        "dedicated_rehearsal_branch_required": True,
        "sandbox_created_now": False,
        "branch_created_now": False,
        "restore_path_map_required": True,
        "source_target_mapping_loaded": structure_map_loaded and map_row_count > 0,
        "rollback_reverse_mapping_required": True,
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
        "verifier_suite_count": max(verifier_suite_count, VERIFIER_SUITE_COUNT),
        "required_verifier_count": REQUIRED_VERIFIER_COUNT,
        "verifier_rerun_executed_now": False,
        "verifier_rerun_success_claim_allowed": False,
        "evidence_template_defined": True,
        "evidence_generated_now": False,
        "rollback_success_claim_allowed": False,
        "rollback_success_claim_requires_real_rehearsal_execution": True,
        "rollback_success_claim_requires_verifier_rerun_pass": True,
        "rollback_success_claim_requires_evidence_pack": True,
        "dryrun_planning_cannot_claim_success": True,
        "missing_evidence_blocks_success_claim": True,
        "ready_for_rollback_rehearsal_dryrun": boundary_ok,
        "ready_for_rollback_rehearsal_execution": False,
        "ready_for_real_migration": False,
        "ready_for_batch_arming": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "rollback_rehearsal_execution_allowed": False,
        "rollback_dryrun_execution_allowed": False,
        "rollback_evidence_generation_allowed": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_DRYRUN_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_DRYRUN_PLANNING_REQUIRES_FIXES",
        "reason": "rollback rehearsal dry-run planning complete; simulate sandbox/restore/verifier/evidence chain",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "rollback_rehearsal_dryrun_planning_policy": rollback_rehearsal_dryrun_planning_policy,
        "rehearsal_sandbox_policy": rehearsal_sandbox_policy,
        "rollback_rehearsal_dryrun_scope": rollback_rehearsal_dryrun_scope,
        "rollback_restore_path_map_plan": rollback_restore_path_map_plan,
        "docs_link_restore_plan": docs_link_restore_plan,
        "verdict_table_restore_plan": verdict_table_restore_plan,
        "eval_out_reference_restore_plan": eval_out_reference_restore_plan,
        "capability_runner_verifier_doc_linkage_restore_plan": capability_runner_verifier_doc_linkage_restore_plan,
        "rollback_verifier_rerun_plan": rollback_verifier_rerun_plan,
        "rollback_rehearsal_evidence_template": rollback_rehearsal_evidence_template,
        "rollback_success_claim_policy": rollback_success_claim_policy,
        "rollback_rehearsal_dryrun_planning_readiness_decision": rollback_rehearsal_dryrun_planning_readiness_decision,
        "execution_non_claims_register": execution_non_claims_register,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
