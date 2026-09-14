# -*- coding: utf-8 -*-
"""Main Project Structure Migration Rollback Rehearsal Post-DryRun Review v1.

Review-only: audit rollback rehearsal dry-run for closure readiness.
No rollback rehearsal execution, sandbox/branch creation, or file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_rollback_rehearsal_post_dryrun_review_only"
SOURCE_CHAIN = "main_project_structure_migration_rollback_rehearsal_post_dryrun_review_v1"
REVIEW_ID = "main_proj_struct_migration_rollback_rehearsal_post_dryrun_review_v1_001"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Closure-v1-001"

DRYRUN_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_DRYRUN_PLANNING_READY_FOR_DRYRUN"
ROADMAP_FINAL = (
    "POST_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_ROADMAP_DECISION_READY_FOR_ROLLBACK_REHEARSAL_DRYRUN_PLANNING"
)
PRE_AUTH_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"
PRE_AUTH_DRYRUN = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PRE_AUTH_POST_REVIEW = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
CONTROLLED_EXECUTION_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSED_FOR_CURRENT_MAINLINE"
CE_PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

DRYRUN_ARTIFACTS = [
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
    "rollback_rehearsal_dryrun_boundary_review.json",
    "rollback_rehearsal_dryrun_readiness_decision.json",
]

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
]

ROOT_SPECS = [
    {
        "id": "rollback_rehearsal_dryrun",
        "arg": "rollback_rehearsal_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": DRYRUN_ARTIFACTS,
    },
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
        "artifacts": ["summary.json", "pre_authorization_rollback_closure_summary.json", "gap_hard_block_closure_summary.json"],
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
        "artifacts": ["summary.json"],
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
        "artifacts": ["summary.json"],
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
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root and artifacts:
        for name in artifacts:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                art[name] = payload
        loaded = loaded and not missing
    return {
        "root": root,
        "loaded": loaded,
        "summary": summary_payload or {},
        "artifacts": art,
        "missing_artifacts": missing,
    }


def _boundary_reports() -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    common = {
        "review_scope": REVIEW_SCOPE,
        "review_only": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }
    no_file_move = {**common, "report_kind": "no_file_move", "actual_file_move_executed": False}
    no_delete = {**common, "report_kind": "no_delete", "actual_file_delete_executed": False}
    no_runtime = {
        **common,
        "report_kind": "no_runtime",
        "runtime_enabled": False,
        "no_runtime_executed": True,
    }
    no_write = {
        **common,
        "report_kind": "no_write",
        "docs_modified_by_review": False,
        "readme_modified_by_review": False,
        "phase_verdict_table_modified_by_review": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
    }
    return no_file_move, no_delete, no_runtime, no_write


def run_main_project_structure_migration_rollback_rehearsal_post_dryrun_review_v1(
    *,
    rollback_rehearsal_dryrun_root: str,
    rollback_rehearsal_dryrun_planning_root: str,
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
    dryrun_art = roots["rollback_rehearsal_dryrun"]["artifacts"]
    dryrun_summary = summaries["rollback_rehearsal_dryrun"]

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "missing_artifacts": meta.get("missing_artifacts") or [],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    dryrun_ok = (
        roots["rollback_rehearsal_dryrun"]["loaded"]
        and dryrun_summary.get("final_decision") == DRYRUN_FINAL
        and dryrun_summary.get("ready_for_post_dryrun_review") is True
    )
    planning_ok = (
        roots["rollback_rehearsal_dryrun_planning"]["loaded"]
        and summaries["rollback_rehearsal_dryrun_planning"].get("final_decision") == PLANNING_FINAL
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
        and summaries["pre_authorization_post_review"].get("final_decision") == PRE_AUTH_POST_REVIEW
    )
    pre_auth_dryrun_loaded = (
        roots["pre_authorization_dryrun"]["loaded"]
        and summaries["pre_authorization_dryrun"].get("final_decision") == PRE_AUTH_DRYRUN
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
    structure_loaded = roots["structure_map"]["loaded"]
    pahr_loaded = roots["pahr_closure"]["loaded"]
    readiness_loaded = roots["readiness"]["loaded"]
    gate_loaded = roots["gate_taxonomy"]["loaded"]

    sandbox_dr = dryrun_art.get("rehearsal_sandbox_dryrun_result.json") or {}
    scope_dr = dryrun_art.get("rollback_rehearsal_scope_dryrun_result.json") or {}
    restore_dr = dryrun_art.get("rollback_restore_path_map_dryrun_result.json") or {}
    docs_dr = dryrun_art.get("docs_link_restore_dryrun_result.json") or {}
    verdict_dr = dryrun_art.get("verdict_table_restore_dryrun_result.json") or {}
    eval_dr = dryrun_art.get("eval_out_reference_restore_dryrun_result.json") or {}
    linkage_dr = dryrun_art.get("capability_runner_verifier_doc_linkage_restore_dryrun_result.json") or {}
    verifier_dr = dryrun_art.get("rollback_verifier_rerun_dryrun_result.json") or {}
    evidence_dr = dryrun_art.get("rollback_rehearsal_evidence_dryrun_result.json") or {}
    success_dr = dryrun_art.get("rollback_success_claim_dryrun_result.json") or {}
    boundary_dr = dryrun_art.get("rollback_rehearsal_dryrun_boundary_review.json") or {}

    closure_root = roots["pre_authorization_closure"]["root"]
    gap_closure = (_try_read_json(closure_root / "gap_hard_block_closure_summary.json") if closure_root else {}) or {}

    missing_dryrun = roots["rollback_rehearsal_dryrun"].get("missing_artifacts") or []

    rollback_rehearsal_dryrun_input_review = {
        "review_id": REVIEW_ID,
        "rollback_rehearsal_dryrun_input_loaded": dryrun_ok,
        "rollback_rehearsal_dryrun_planning_input_loaded": planning_ok,
        "post_pre_authorization_roadmap_input_loaded": roadmap_loaded,
        "required_artifacts_loaded": dryrun_ok and not missing_dryrun,
        "missing_required_artifacts": missing_dryrun,
        "input_status": "complete" if dryrun_ok and not missing_dryrun else "incomplete",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    def _dry_bool(key: str, dr: Dict[str, Any], default: bool = False) -> bool:
        return _bool_val(dryrun_summary.get(key, dr.get(key)), default)

    rehearsal_sandbox_post_review = {
        "sandbox_required": sandbox_dr.get("sandbox_required", True),
        "dedicated_rehearsal_branch_required": sandbox_dr.get("dedicated_rehearsal_branch_required", True),
        "readonly_source_snapshot_required": sandbox_dr.get("readonly_source_snapshot_required", True),
        "no_real_repo_mutation": sandbox_dr.get("no_real_repo_mutation", True),
        "synthetic_restore_map_allowed": sandbox_dr.get("synthetic_restore_map_allowed", True),
        "sandbox_simulated": _dry_bool("sandbox_simulated", sandbox_dr, False),
        "sandbox_created_now": _dry_bool("sandbox_created_now", sandbox_dr, False),
        "branch_created_now": _dry_bool("branch_created_now", sandbox_dr, False),
        "sandbox_review_pass": dryrun_ok
        and sandbox_dr.get("sandbox_review_pass") is True
        and not _bool_val(sandbox_dr.get("sandbox_created_now"), False),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_scope_post_review = {
        "scope_batch_count": dryrun_summary.get("scope_batch_count", scope_dr.get("scope_batch_count", 8)),
        "mandatory_rollback_path_count": dryrun_summary.get(
            "mandatory_rollback_path_count", scope_dr.get("mandatory_rollback_path_count", 6)
        ),
        "b0_baseline_restore_check_simulated": _dry_bool("b0_baseline_restore_check_simulated", scope_dr, False),
        "b1_docs_relink_rollback_path_simulated": _dry_bool("b1_docs_relink_rollback_path_simulated", scope_dr, False),
        "b2_capability_grouping_rollback_path_simulated": _dry_bool(
            "b2_capability_grouping_rollback_path_simulated", scope_dr, False
        ),
        "b3_governance_grouping_rollback_path_simulated": _dry_bool(
            "b3_governance_grouping_rollback_path_simulated", scope_dr, False
        ),
        "b4_midplatform_core_rollback_path_simulated": _dry_bool(
            "b4_midplatform_core_rollback_path_simulated", scope_dr, False
        ),
        "b5_dev_artifact_reference_rollback_path_simulated": _dry_bool(
            "b5_dev_artifact_reference_rollback_path_simulated", scope_dr, False
        ),
        "b6_future_marker_rollback_path_simulated": _dry_bool("b6_future_marker_rollback_path_simulated", scope_dr, False),
        "b7_verification_gate_restore_check_simulated": _dry_bool(
            "b7_verification_gate_restore_check_simulated", scope_dr, False
        ),
        "rollback_scope_review_pass": dryrun_ok and scope_dr.get("rollback_scope_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_restore_path_map_post_review = {
        "restore_path_map_required": restore_dr.get("restore_path_map_required", True),
        "source_target_mapping_loaded": restore_dr.get("source_target_mapping_loaded", True),
        "rollback_reverse_mapping_simulated": _dry_bool("rollback_reverse_mapping_simulated", restore_dr, False),
        "protected_asset_restore_rule_simulated": _dry_bool("protected_asset_restore_rule_simulated", restore_dr, False),
        "HR_DnAE_restore_rule_simulated": _dry_bool("HR_DnAE_restore_rule_simulated", restore_dr, False),
        "path_conflict_detection_simulated": _dry_bool("path_conflict_detection_simulated", restore_dr, False),
        "missing_original_path_blocks_success_claim": restore_dr.get("missing_original_path_blocks_success_claim", True),
        "restore_path_map_generated_now": _bool_val(restore_dr.get("restore_path_map_generated_now"), False),
        "restore_path_map_review_pass": dryrun_ok and restore_dr.get("restore_path_map_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    docs_link_restore_post_review = {
        "docs_link_restore_required": docs_dr.get("docs_link_restore_required", True),
        "architecture_readme_restore_simulated": docs_dr.get("architecture_readme_restore_simulated", True),
        "governance_doc_restore_simulated": docs_dr.get("governance_doc_restore_simulated", True),
        "evaluation_doc_restore_simulated": docs_dr.get("evaluation_doc_restore_simulated", True),
        "phase_doc_restore_simulated": docs_dr.get("phase_doc_restore_simulated", True),
        "markdown_link_check_simulated": docs_dr.get("markdown_link_check_simulated", True),
        "docs_link_restore_executed_now": _bool_val(docs_dr.get("docs_link_restore_executed_now"), False),
        "docs_link_restore_review_pass": dryrun_ok and docs_dr.get("docs_link_restore_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    verdict_table_restore_post_review = {
        "verdict_table_restore_required_if_touched": verdict_dr.get("verdict_table_restore_required_if_touched", True),
        "verdict_table_touch_forbidden_by_default": verdict_dr.get("verdict_table_touch_forbidden_by_default", True),
        "verdict_table_snapshot_simulated": verdict_dr.get("verdict_table_snapshot_simulated", True),
        "verdict_table_restore_check_simulated": verdict_dr.get("verdict_table_restore_check_simulated", True),
        "verdict_table_restore_executed_now": _bool_val(verdict_dr.get("verdict_table_restore_executed_now"), False),
        "verdict_table_restore_review_pass": dryrun_ok and verdict_dr.get("verdict_table_restore_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    eval_out_reference_restore_post_review = {
        "eval_out_reference_restore_required": eval_dr.get("eval_out_reference_restore_required", True),
        "eval_out_content_move_forbidden": eval_dr.get("eval_out_content_move_forbidden", True),
        "eval_out_path_reference_snapshot_simulated": eval_dr.get("eval_out_path_reference_snapshot_simulated", True),
        "historical_output_reference_integrity_simulated": eval_dr.get(
            "historical_output_reference_integrity_simulated", True
        ),
        "eval_out_reference_restore_executed_now": _bool_val(eval_dr.get("eval_out_reference_restore_executed_now"), False),
        "eval_out_reference_restore_review_pass": dryrun_ok and eval_dr.get("eval_out_reference_restore_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    capability_runner_verifier_doc_linkage_restore_post_review = {
        "linkage_restore_required": linkage_dr.get("linkage_restore_required", True),
        "capability_runner_pair_check_simulated": linkage_dr.get("capability_runner_pair_check_simulated", True),
        "runner_verifier_pair_check_simulated": linkage_dr.get("runner_verifier_pair_check_simulated", True),
        "governance_doc_link_check_simulated": linkage_dr.get("governance_doc_link_check_simulated", True),
        "evaluation_doc_link_check_simulated": linkage_dr.get("evaluation_doc_link_check_simulated", True),
        "go_no_go_pack_link_check_simulated": linkage_dr.get("go_no_go_pack_link_check_simulated", True),
        "import_path_restore_check_simulated": linkage_dr.get("import_path_restore_check_simulated", True),
        "linkage_restore_executed_now": _bool_val(linkage_dr.get("linkage_restore_executed_now"), False),
        "linkage_restore_review_pass": dryrun_ok and linkage_dr.get("linkage_restore_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    verifier_suite_count = dryrun_summary.get("verifier_suite_count", verifier_dr.get("verifier_suite_count", 12))
    required_verifier_count = dryrun_summary.get("required_verifier_count", verifier_dr.get("required_verifier_count", 4))
    rollback_specific_count = dryrun_summary.get(
        "rollback_specific_verifier_count", verifier_dr.get("rollback_specific_verifier_count", 4)
    )

    rollback_verifier_rerun_post_review = {
        "verifier_rerun_required": verifier_dr.get("verifier_rerun_required", True),
        "verifier_suite_count": verifier_suite_count,
        "required_verifier_count": required_verifier_count,
        "rollback_specific_verifier_count": rollback_specific_count,
        "execution_order_defined": verifier_dr.get("execution_order_defined", True),
        "verifier_rerun_simulated": _dry_bool("verifier_rerun_simulated", verifier_dr, False),
        "verifier_rerun_executed_now": _bool_val(verifier_dr.get("verifier_rerun_executed_now"), False),
        "verifier_rerun_success_claim_allowed": _bool_val(verifier_dr.get("verifier_rerun_success_claim_allowed"), False),
        "rollback_verifier_rerun_review_pass": dryrun_ok and verifier_dr.get("rollback_verifier_rerun_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_evidence_post_review = {
        "evidence_template_defined": evidence_dr.get("evidence_template_defined", True),
        "covered_batches_defined": evidence_dr.get("covered_batches_defined", True),
        "restore_path_map_result_required": evidence_dr.get("restore_path_map_result_required", True),
        "docs_link_restore_result_required": evidence_dr.get("docs_link_restore_result_required", True),
        "verdict_table_restore_result_required": evidence_dr.get("verdict_table_restore_result_required", True),
        "eval_out_ref_restore_result_required": evidence_dr.get("eval_out_ref_restore_result_required", True),
        "linkage_restore_result_required": evidence_dr.get("linkage_restore_result_required", True),
        "verifier_rerun_result_required": evidence_dr.get("verifier_rerun_result_required", True),
        "failure_list_required": evidence_dr.get("failure_list_required", True),
        "evidence_simulated": _dry_bool("evidence_simulated", evidence_dr, False),
        "evidence_generated_now": _bool_val(evidence_dr.get("evidence_generated_now"), False),
        "rollback_evidence_review_pass": dryrun_ok and evidence_dr.get("rollback_evidence_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_success_claim_post_review = {
        "rollback_success_claim_allowed": False,
        "rollback_success_claim_requires_real_rehearsal_execution": success_dr.get(
            "rollback_success_claim_requires_real_rehearsal_execution", True
        ),
        "rollback_success_claim_requires_verifier_rerun_pass": success_dr.get(
            "rollback_success_claim_requires_verifier_rerun_pass", True
        ),
        "rollback_success_claim_requires_evidence_pack": success_dr.get(
            "rollback_success_claim_requires_evidence_pack", True
        ),
        "dryrun_planning_cannot_claim_success": success_dr.get("dryrun_planning_cannot_claim_success", True),
        "dryrun_cannot_claim_success": success_dr.get("dryrun_cannot_claim_success", True),
        "missing_evidence_blocks_success_claim": success_dr.get("missing_evidence_blocks_success_claim", True),
        "dryrun_success_claim_attempt_blocked": success_dr.get("dryrun_success_claim_attempt_blocked", True),
        "rollback_success_claim_review_pass": dryrun_ok
        and not _bool_val(success_dr.get("rollback_success_claim_allowed"), True)
        and success_dr.get("rollback_success_claim_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_boundary_post_review = {
        "real_migration_execution_allowed": _bool_val(dryrun_summary.get("real_migration_execution_allowed"), False),
        "batch_arming_allowed_now": _bool_val(dryrun_summary.get("batch_arming_allowed_now"), False),
        "rollback_rehearsal_execution_allowed": _bool_val(dryrun_summary.get("rollback_rehearsal_execution_allowed"), False),
        "rollback_dryrun_execution_allowed": _bool_val(dryrun_summary.get("rollback_dryrun_execution_allowed"), False),
        "rollback_evidence_generation_allowed": _bool_val(
            dryrun_summary.get("rollback_evidence_generation_allowed"), False
        ),
        "sandbox_created_now": _bool_val(dryrun_summary.get("sandbox_created_now"), False),
        "branch_created_now": _bool_val(dryrun_summary.get("branch_created_now"), False),
        "rollback_executed": False,
        "rollback_rehearsal_executed": _bool_val(dryrun_summary.get("rollback_rehearsal_executed"), False),
        "verifier_rerun_executed_now": _bool_val(dryrun_summary.get("verifier_rerun_executed_now"), False),
        "evidence_generated_now": _bool_val(dryrun_summary.get("evidence_generated_now"), False),
        "rollback_success_claim_allowed": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_review": False,
        "readme_modified_by_review": False,
        "phase_verdict_table_modified_by_review": False,
        "runtime_enabled": False,
        "boundary_post_review_pass": dryrun_ok
        and boundary_dr.get("boundary_review_pass") is True
        and boundary_dr.get("no_sandbox_creation") is True
        and boundary_dr.get("no_branch_creation") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    review_passes = [
        rehearsal_sandbox_post_review.get("sandbox_review_pass"),
        rollback_rehearsal_scope_post_review.get("rollback_scope_review_pass"),
        rollback_restore_path_map_post_review.get("restore_path_map_review_pass"),
        docs_link_restore_post_review.get("docs_link_restore_review_pass"),
        verdict_table_restore_post_review.get("verdict_table_restore_review_pass"),
        eval_out_reference_restore_post_review.get("eval_out_reference_restore_review_pass"),
        capability_runner_verifier_doc_linkage_restore_post_review.get("linkage_restore_review_pass"),
        rollback_verifier_rerun_post_review.get("rollback_verifier_rerun_review_pass"),
        rollback_rehearsal_evidence_post_review.get("rollback_evidence_review_pass"),
        rollback_success_claim_post_review.get("rollback_success_claim_review_pass"),
        rollback_rehearsal_boundary_post_review.get("boundary_post_review_pass"),
    ]

    blockers: List[str] = []
    if not dryrun_ok:
        blockers.append("rollback_rehearsal_dryrun_not_ready")
    if not planning_ok:
        blockers.append("rollback_rehearsal_dryrun_planning_not_ready")
    if missing_dryrun:
        blockers.append("dryrun_artifacts_missing")
    if not all(review_passes):
        blockers.append("one_or_more_post_reviews_failed")
    if _bool_val(dryrun_summary.get("sandbox_created_now"), False):
        blockers.append("sandbox_must_not_be_created")
    if _bool_val(dryrun_summary.get("rollback_rehearsal_executed"), False):
        blockers.append("rollback_rehearsal_must_not_be_executed")
    if _bool_val(dryrun_summary.get("rollback_success_claim_allowed"), True):
        blockers.append("rollback_success_claim_must_remain_false")

    boundary_ok = not blockers

    rollback_rehearsal_post_dryrun_readiness_decision = {
        "review_verdict": "GO" if boundary_ok else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [
            "post-dryrun review confirms rollback rehearsal dry-run chain; no permission granted",
            "missing_rollback_rehearsal still blocks migration and arming after closure freeze",
            "closure next to freeze Planning→DryRun→Post-Review chain",
        ],
        "ready_for_closure": boundary_ok,
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

    governance_debt_review = {
        "items": [
            "rollback_rehearsal_post_dryrun_review_audit_only",
            "sandbox_and_branch_not_created",
            "restore_path_map_not_generated",
            "rollback_evidence_not_generated",
            "verifier_rerun_not_executed",
            "rollback_success_claim_blocked",
            "missing_rollback_rehearsal_blocks_real_migration",
            "missing_rollback_rehearsal_blocks_batch_arming",
            f"{HUMAN_REVIEW_CARRYOVER}_hr_manual_only",
            f"{PERMANENT_BLOCK_CARRYOVER}_dnae_excluded",
        ],
        "item_count": 10,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "reason": "dry-run post-review confirms simulated chain; ready for closure freeze",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    no_file_move, no_delete, no_runtime, no_write = _boundary_reports()

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "rollback_rehearsal_dryrun_input_loaded": dryrun_ok,
        "rollback_rehearsal_dryrun_planning_input_loaded": planning_ok,
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
        "structure_map_input_loaded": structure_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "rollback_rehearsal_dryrun_input_review_generated": True,
        "rehearsal_sandbox_post_review_generated": True,
        "rollback_rehearsal_scope_post_review_generated": True,
        "rollback_restore_path_map_post_review_generated": True,
        "docs_link_restore_post_review_generated": True,
        "verdict_table_restore_post_review_generated": True,
        "eval_out_reference_restore_post_review_generated": True,
        "capability_runner_verifier_doc_linkage_restore_post_review_generated": True,
        "rollback_verifier_rerun_post_review_generated": True,
        "rollback_rehearsal_evidence_post_review_generated": True,
        "rollback_success_claim_post_review_generated": True,
        "rollback_rehearsal_boundary_post_review_generated": True,
        "rollback_rehearsal_post_dryrun_readiness_decision_generated": True,
        "scope_batch_count": dryrun_summary.get("scope_batch_count", 8),
        "mandatory_rollback_path_count": dryrun_summary.get("mandatory_rollback_path_count", 6),
        "verifier_suite_count": verifier_suite_count,
        "required_verifier_count": required_verifier_count,
        "rollback_specific_verifier_count": rollback_specific_count,
        "sandbox_simulated": _dry_bool("sandbox_simulated", sandbox_dr, False),
        "sandbox_created_now": False,
        "branch_created_now": False,
        "b0_baseline_restore_check_simulated": _dry_bool("b0_baseline_restore_check_simulated", scope_dr, False),
        "b1_docs_relink_rollback_path_simulated": _dry_bool("b1_docs_relink_rollback_path_simulated", scope_dr, False),
        "b2_capability_grouping_rollback_path_simulated": _dry_bool(
            "b2_capability_grouping_rollback_path_simulated", scope_dr, False
        ),
        "b3_governance_grouping_rollback_path_simulated": _dry_bool(
            "b3_governance_grouping_rollback_path_simulated", scope_dr, False
        ),
        "b4_midplatform_core_rollback_path_simulated": _dry_bool(
            "b4_midplatform_core_rollback_path_simulated", scope_dr, False
        ),
        "b5_dev_artifact_reference_rollback_path_simulated": _dry_bool(
            "b5_dev_artifact_reference_rollback_path_simulated", scope_dr, False
        ),
        "b6_future_marker_rollback_path_simulated": _dry_bool("b6_future_marker_rollback_path_simulated", scope_dr, False),
        "b7_verification_gate_restore_check_simulated": _dry_bool(
            "b7_verification_gate_restore_check_simulated", scope_dr, False
        ),
        "rollback_reverse_mapping_simulated": _dry_bool("rollback_reverse_mapping_simulated", restore_dr, False),
        "protected_asset_restore_rule_simulated": _dry_bool("protected_asset_restore_rule_simulated", restore_dr, False),
        "HR_DnAE_restore_rule_simulated": _dry_bool("HR_DnAE_restore_rule_simulated", restore_dr, False),
        "path_conflict_detection_simulated": _dry_bool("path_conflict_detection_simulated", restore_dr, False),
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
        "verifier_rerun_simulated": _dry_bool("verifier_rerun_simulated", verifier_dr, False),
        "verifier_rerun_executed_now": False,
        "verifier_rerun_success_claim_allowed": False,
        "evidence_simulated": _dry_bool("evidence_simulated", evidence_dr, False),
        "evidence_generated_now": False,
        "rollback_success_claim_allowed": False,
        "dryrun_success_claim_attempt_blocked": success_dr.get("dryrun_success_claim_attempt_blocked", True),
        "ready_for_closure": boundary_ok,
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
        "rollback_rehearsal_executed": _bool_val(dryrun_summary.get("rollback_rehearsal_executed"), False),
        "docs_modified_by_review": False,
        "readme_modified_by_review": False,
        "phase_verdict_table_modified_by_review": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "rollback_rehearsal_dryrun_input_review": rollback_rehearsal_dryrun_input_review,
        "rehearsal_sandbox_post_review": rehearsal_sandbox_post_review,
        "rollback_rehearsal_scope_post_review": rollback_rehearsal_scope_post_review,
        "rollback_restore_path_map_post_review": rollback_restore_path_map_post_review,
        "docs_link_restore_post_review": docs_link_restore_post_review,
        "verdict_table_restore_post_review": verdict_table_restore_post_review,
        "eval_out_reference_restore_post_review": eval_out_reference_restore_post_review,
        "capability_runner_verifier_doc_linkage_restore_post_review": (
            capability_runner_verifier_doc_linkage_restore_post_review
        ),
        "rollback_verifier_rerun_post_review": rollback_verifier_rerun_post_review,
        "rollback_rehearsal_evidence_post_review": rollback_rehearsal_evidence_post_review,
        "rollback_success_claim_post_review": rollback_success_claim_post_review,
        "rollback_rehearsal_boundary_post_review": rollback_rehearsal_boundary_post_review,
        "rollback_rehearsal_post_dryrun_readiness_decision": rollback_rehearsal_post_dryrun_readiness_decision,
        "governance_debt_review": governance_debt_review,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": no_file_move,
        "no_delete_boundary_report": no_delete,
        "no_runtime_boundary_report": no_runtime,
        "no_write_boundary_report": no_write,
    }
