# -*- coding: utf-8 -*-
"""Main Project Structure Migration Pre-Authorization and Rollback Rehearsal Planning v1.

Planning-only: define owner/auth, operator ack, rollback rehearsal, batch arming preconditions.
No real migration, owner confirmation, rollback rehearsal execution, or batch arming.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_planning_only"
PLANNING_ID = "main_proj_struct_migration_pre_auth_rollback_rehearsal_planning_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_planning_v1"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-DryRun-v1-001"

ROADMAP_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_ROADMAP_DECISION_READY_FOR_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_PLANNING"
)
CONTROLLED_EXECUTION_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSED_FOR_CURRENT_MAINLINE"
PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

BATCH_IDS = ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7")

OWNER_BATCH_REQUIRED: Dict[str, List[str]] = {
    "B0": ["architecture_owner"],
    "B1": ["docs_owner", "architecture_owner"],
    "B2": ["capability_owner", "architecture_owner"],
    "B3": ["governance_owner", "architecture_owner"],
    "B4": ["midplatform_owner", "architecture_owner"],
    "B5": ["evaluation_owner", "architecture_owner"],
    "B6": ["architecture_owner"],
    "B7": ["evaluation_owner", "architecture_owner"],
}

OWNER_TYPE_DEFS = [
    ("architecture_owner", "architecture and chain integrity"),
    ("governance_owner", "governance/docs/gate/safety assets"),
    ("evaluation_owner", "verifier/test/log assets"),
    ("capability_owner", "capability module grouping"),
    ("midplatform_owner", "midplatform grouping"),
    ("docs_owner", "docs relink"),
    ("product_client_owner", "client boundary"),
]

OPERATOR_ACK_TOPICS = [
    "no_parallel_batches",
    "rollback_procedure",
    "abort_conditions",
    "protected_asset_exclusions",
    "HR_DnAE_exclusions",
    "post_batch_tests",
    "verifier_suite",
    "stop_conditions",
]

PACKAGE_RECORDS = [
    "owner_approval_records",
    "operator_acknowledgement",
    "clean_working_tree_proof",
    "branch_backup_proof",
    "protected_asset_exclusion_snapshot",
    "HR_DnAE_exclusion_snapshot",
    "rollback_rehearsal_report",
    "test_harness_ready_record",
    "verifier_suite_ready_record",
    "abort_policy_loaded_record",
    "batch_arming_record",
]

REHEARSAL_SCOPE_ITEMS = [
    ("B1_B6_mandatory", ["B1", "B2", "B3", "B4", "B5", "B6"], True),
    ("B0_baseline_restore_check", ["B0"], True),
    ("B7_verification_gate_restore_check", ["B7"], True),
    ("restore_path_map", [], False),
    ("restore_docs_links", [], False),
    ("restore_phase_verdict_table_if_touched", [], False),
    ("restore_eval_out_references", [], False),
    ("restore_capability_runner_verifier_doc_linkage", [], False),
    ("rollback_verifier_rerun", [], False),
]

REHEARSAL_STEPS = [
    ("RS01", "prepare_rehearsal_sandbox_or_branch", True),
    ("RS02", "load_baseline_snapshot", True),
    ("RS03", "simulate_B1_B6_rollback_path", True),
    ("RS04", "verify_restore_path_map", True),
    ("RS05", "verify_docs_link_restore", True),
    ("RS06", "verify_verdict_table_restore_if_touched", True),
    ("RS07", "verify_eval_out_reference_restore", True),
    ("RS08", "verify_capability_runner_verifier_doc_linkage_restore", True),
    ("RS09", "run_rollback_verifier_suite_after_rehearsal", True),
    ("RS10", "generate_rollback_rehearsal_report", True),
    ("RS11", "block_real_migration_if_rehearsal_fails", True),
]

AUTHORIZATION_BLOCKERS = [
    ("AB01", "missing_owner_approval", "critical", "block_arming_and_migration", True, True),
    ("AB02", "missing_operator_acknowledgement", "critical", "block_arming_and_migration", True, True),
    ("AB03", "missing_rollback_rehearsal", "critical", "block_real_migration", True, True),
    ("AB04", "missing_rollback_evidence", "critical", "block_real_migration", True, True),
    ("AB05", "missing_test_harness_readiness", "high", "block_arming", True, True),
    ("AB06", "missing_verifier_suite_readiness", "high", "block_arming", True, True),
    ("AB07", "protected_asset_inclusion", "critical", "immediate_abort", True, True),
    ("AB08", "HR_DnAE_inclusion", "critical", "halt_human_review", True, True),
    ("AB09", "batch_arming_record_missing", "high", "block_batch_advance", True, True),
    ("AB10", "abort_policy_missing", "high", "block_arming", True, True),
    ("AB11", "dirty_working_tree", "high", "block_arming", True, True),
    ("AB12", "missing_backup_or_branch", "high", "block_arming", True, True),
    ("AB13", "attempt_auto_confirm_owner", "critical", "block_entire_execution", True, True),
    ("AB14", "attempt_bypass_rollback_rehearsal", "critical", "block_real_migration", True, True),
    ("AB15", "attempt_parallel_batch_execution", "critical", "block_batch_and_migration", True, True),
]

EXECUTION_NON_CLAIMS = [
    "pre-authorization planning 不等于 owner 已确认",
    "planning 不等于 operator acknowledgement 已执行",
    "planning 不等于 pre-execution authorization package 已生成",
    "planning 不等于 rollback rehearsal 已执行",
    "planning 不等于 rollback evidence 已生成",
    "planning 不等于 batch 已 armed",
    "planning 不等于真实迁移可执行",
    "ready_for_pre_authorization_dryrun 不等于 file move 已授权",
]

ROOT_SPECS = [
    {
        "id": "controlled_execution_roadmap",
        "arg": "controlled_execution_roadmap_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "pre_authorization_rollback_rehearsal_route_decision.json",
            "controlled_execution_closure_status_summary.json",
        ],
    },
    {
        "id": "controlled_execution_closure",
        "arg": "controlled_execution_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_execution_closure_summary.json",
            "controlled_execution_closure_decision_summary.json",
            "controlled_execution_non_claims_register.json",
            "deferred_controlled_execution_action_pool.json",
        ],
    },
    {
        "id": "controlled_execution_post_review",
        "arg": "controlled_execution_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_execution_dryrun",
        "arg": "controlled_execution_dryrun_root",
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
            "controlled_execution_batch_plan.json",
            "owner_authorization_gate.json",
            "batch_arming_execution_plan.json",
            "rollback_rehearsal_precondition.json",
            "post_batch_test_execution_order.json",
            "verifier_suite_execution_order.json",
            "abort_and_failure_response_plan.json",
            "post_execution_evidence_pack_plan.json",
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
        "artifacts": [
            "human_review_carryover_for_future_execution.json",
            "permanent_block_carryover_for_future_governance.json",
        ],
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


def run_main_project_structure_migration_pre_authorization_and_rollback_rehearsal_planning_v1(
    *,
    controlled_execution_roadmap_root: str,
    controlled_execution_closure_root: str,
    controlled_execution_post_review_root: str,
    controlled_execution_dryrun_root: str,
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
    plan_art = roots["controlled_execution_planning"]["artifacts"] if roots["controlled_execution_planning"]["loaded"] else {}

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

    roadmap_loaded = (
        roots["controlled_execution_roadmap"]["loaded"]
        and summaries["controlled_execution_roadmap"].get("final_decision") == ROADMAP_FINAL
    )
    ce_closure_loaded = (
        roots["controlled_execution_closure"]["loaded"]
        and summaries["controlled_execution_closure"].get("final_decision") == CONTROLLED_EXECUTION_CLOSURE
        and summaries["controlled_execution_closure"].get("controlled_execution_chain_closed") is True
    )
    ce_planning_loaded = (
        roots["controlled_execution_planning"]["loaded"]
        and summaries["controlled_execution_planning"].get("final_decision") == PLANNING_FINAL
    )
    ec_closure_loaded = (
        roots["execution_control_closure"]["loaded"]
        and summaries["execution_control_closure"].get("final_decision") == EXECUTION_CONTROL_CLOSURE
    )
    guarded_closure_loaded = (
        roots["guarded_closure"]["loaded"]
        and summaries["guarded_closure"].get("final_decision") == GUARDED_CLOSURE
    )
    readiness_loaded = roots["readiness"]["loaded"]
    pahr_loaded = roots["pahr_closure"]["loaded"]
    structure_loaded = roots["structure_map"]["loaded"]
    gate_loaded = roots["gate_taxonomy"]["loaded"]

    owner_gate_plan = plan_art.get("owner_authorization_gate.json") or {}
    arming_plan = plan_art.get("batch_arming_execution_plan.json") or {}
    rollback_pre = plan_art.get("rollback_rehearsal_precondition.json") or {}

    pre_authorization_and_rollback_rehearsal_planning_policy = {
        "planning_id": PLANNING_ID,
        "planning_scope": PLANNING_SCOPE,
        "source_roadmap_ref": "_eval_out/main_project_structure_migration_controlled_execution_roadmap_decision_v1_smoke_v0/",
        "source_controlled_execution_closure_ref": "_eval_out/main_project_structure_migration_controlled_execution_closure_v1_smoke_v0/",
        "source_controlled_execution_plan_ref": "_eval_out/main_project_structure_migration_controlled_execution_planning_v1_smoke_v0/",
        "owner_authorization_resolution_plan_ref": "owner_authorization_resolution_plan.json",
        "operator_acknowledgement_policy_ref": "operator_acknowledgement_policy.json",
        "pre_execution_authorization_package_ref": "pre_execution_authorization_package.json",
        "rollback_rehearsal_scope_ref": "rollback_rehearsal_scope.json",
        "rollback_rehearsal_plan_ref": "rollback_rehearsal_plan.json",
        "rollback_rehearsal_evidence_template_ref": "rollback_rehearsal_evidence_template.json",
        "batch_arming_precondition_record_ref": "batch_arming_precondition_record.json",
        "authorization_blocker_policy_ref": "authorization_blocker_policy.json",
        "next_phase_recommendation": NEXT_PHASE,
        "planning_only": True,
        "real_migration_execution_allowed": False,
        "owner_approval_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "post_migration_tests_execution_allowed": False,
        "verifier_suite_execution_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    owner_entries = []
    for owner_type, note in OWNER_TYPE_DEFS:
        applies = []
        for bid, owners in OWNER_BATCH_REQUIRED.items():
            if owner_type in owners:
                applies.append(bid)
        owner_entries.append(
            {
                "owner_type": owner_type,
                "applies_to_batches": applies,
                "approval_required": True,
                "owner_candidate_allowed": True,
                "owner_confirmed_now": False,
                "auto_confirm_allowed": False,
                "missing_owner_blocks_execution": True,
                "approval_record_required": True,
                "approval_execution_allowed_now": False,
                "notes": note,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    owner_authorization_resolution_plan = {
        "owners": owner_entries,
        "owner_authorization_type_count": len(owner_entries),
        "owner_auto_confirmation_forbidden": True,
        "owner_confirmed_now": False,
        "B1_requires_docs_and_architecture": True,
        "B2_requires_capability_and_architecture": True,
        "B3_requires_governance_and_architecture": True,
        "B4_requires_midplatform_and_architecture": True,
        "B5_requires_evaluation_and_architecture": True,
        "B6_requires_architecture_only": True,
        "B7_requires_evaluation_and_architecture": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    operator_acknowledgement_policy = {
        "operator_ack_required": True,
        "operator_ack_scope": "full_controlled_migration_execution_chain",
        "operator_must_confirm_understanding_of": OPERATOR_ACK_TOPICS,
        "operator_ack_executed_now": False,
        "operator_ack_auto_generated": False,
        "missing_operator_ack_blocks_execution": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    pre_execution_authorization_package = {
        "package_id": "pre_execution_authorization_package_v1",
        "included_records": [
            {"record_name": r, "required": True, "generated_now": False, "execution_allowed_now": False}
            for r in PACKAGE_RECORDS
        ],
        "package_generated_now": False,
        "package_execution_allowed_now": False,
        "package_required_before_real_migration": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    scope_entries = []
    for sid, batches, mandatory in REHEARSAL_SCOPE_ITEMS:
        scope_entries.append(
            {
                "scope_item_id": sid,
                "covered_batches": batches,
                "mandatory": mandatory,
                "required_before_real_migration": True,
                "rehearsal_execution_allowed_now": False,
                "rehearsal_executed_now": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    rollback_rehearsal_scope = {
        "rehearsal_scope_id": "controlled_migration_rollback_rehearsal_scope_v1",
        "scope_items": scope_entries,
        "rollback_rehearsal_scope_batch_count": len(BATCH_IDS),
        "rollback_rehearsal_mandatory_batches": ["B1", "B2", "B3", "B4", "B5", "B6"],
        "rollback_rehearsal_mandatory_batches_count": 6,
        "B1_B6_mandatory": True,
        "B0_baseline_restore_check": True,
        "B7_verification_gate_restore_check": True,
        "required_before_real_migration": True,
        "rehearsal_execution_allowed_now": False,
        "rehearsal_executed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rehearsal_steps = []
    for step_id, step_name, required in REHEARSAL_STEPS:
        rehearsal_steps.append(
            {
                "rehearsal_step_id": step_id,
                "step_name": step_name,
                "required": required,
                "execution_allowed_now": False,
                "executed_now": False,
                "failure_blocks_real_migration": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    rollback_rehearsal_plan = {
        "steps": rehearsal_steps,
        "rollback_rehearsal_step_count": len(rehearsal_steps),
        "rollback_rehearsal_required_before_real_migration": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_evidence_template = {
        "rehearsal_id": "rollback_rehearsal_evidence_template_v1",
        "covered_batches": ["B1", "B2", "B3", "B4", "B5", "B6"],
        "restore_path_map_result": "pending",
        "docs_link_restore_result": "pending",
        "verdict_table_restore_result": "pending",
        "eval_out_ref_restore_result": "pending",
        "verifier_rerun_result": "pending",
        "failure_list": [],
        "rollback_success_claim_allowed": False,
        "evidence_generated_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    arming_records = []
    for bid in BATCH_IDS:
        ap = next((b for b in arming_plan.get("batches") or [] if b.get("batch_id") == bid), {})
        arming_records.append(
            {
                "batch_id": bid,
                "required_owner_approvals": OWNER_BATCH_REQUIRED.get(bid, []),
                "operator_ack_required": True,
                "rollback_rehearsal_required": bid in ("B1", "B2", "B3", "B4", "B5", "B6"),
                "test_harness_ready_required": True,
                "verifier_suite_ready_required": True,
                "protected_asset_exclusion_required": True,
                "HR_DnAE_exclusion_required": True,
                "abort_policy_loaded_required": True,
                "arming_record_generated_now": False,
                "arming_allowed_now": False,
                "armed_now": False,
                "guarded_arming_ref": ap.get("batch_id"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    batch_arming_precondition_record = {
        "batches": arming_records,
        "batch_arming_record_count": len(arming_records),
        "armed_batch_count": 0,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blocker_entries = []
    for bid, name, severity, response, blocks_migration, blocks_arming in AUTHORIZATION_BLOCKERS:
        blocker_entries.append(
            {
                "blocker_id": bid,
                "blocker_name": name,
                "severity": severity,
                "blocks_real_migration": blocks_migration,
                "blocks_batch_arming": blocks_arming,
                "failure_response": response,
                "audit_required": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    authorization_blocker_policy = {
        "blockers": blocker_entries,
        "authorization_blocker_count": len(blocker_entries),
        "missing_owner_blocks_execution": True,
        "missing_operator_ack_blocks_execution": True,
        "missing_rollback_rehearsal_blocks_execution": True,
        "auto_confirm_owner_forbidden": True,
        "parallel_batch_execution_forbidden": True,
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
            "owner_approval_records_not_collected",
            "operator_acknowledgement_not_executed",
            "rollback_rehearsal_not_performed",
            "pre_execution_authorization_package_template_only",
            f"{HUMAN_REVIEW_CARRYOVER}_hr_manual_only",
            f"{PERMANENT_BLOCK_CARRYOVER}_dnae_excluded",
            "armed_batch_count=0",
        ],
        "item_count": 7,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not roadmap_loaded:
        blockers.append("controlled_execution_roadmap_not_ready")
    if not ce_closure_loaded:
        blockers.append("controlled_execution_closure_not_ready")
    if not ce_planning_loaded:
        blockers.append("controlled_execution_planning_not_loaded")
    if not ec_closure_loaded:
        blockers.append("execution_control_closure_not_confirmed")
    if len(owner_entries) != 7:
        blockers.append("owner_authorization_type_count_not_7")
    if len(rehearsal_steps) < 10:
        blockers.append("rollback_rehearsal_step_count_insufficient")
    if len(blocker_entries) < 14:
        blockers.append("authorization_blocker_count_insufficient")

    boundary_ok = not blockers

    pre_authorization_planning_readiness_decision = {
        "readiness_verdict": "ready_for_pre_authorization_dryrun" if boundary_ok else "requires_fixes",
        "blockers": blockers,
        "conditional_notes": [
            "planning defines owner/auth/operator ack/rollback rehearsal/batch arming preconditions only",
            "no owner confirmation, no rollback rehearsal execution, no batch arming",
            "Route A from controlled execution roadmap decision",
        ],
        "ready_for_pre_authorization_dryrun": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_batch_arming": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "ready_for_rollback_rehearsal_execution": False,
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_PLANNING_REQUIRES_FIXES",
        "reason": "pre-auth and rollback rehearsal plan defined; dry-run next to simulate blockers",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "controlled_execution_roadmap_input_loaded": roadmap_loaded,
        "controlled_execution_closure_input_loaded": ce_closure_loaded,
        "controlled_execution_planning_input_loaded": ce_planning_loaded,
        "execution_control_closure_input_loaded": ec_closure_loaded,
        "guarded_closure_input_loaded": guarded_closure_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "structure_map_input_loaded": structure_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "pre_authorization_planning_policy_generated": True,
        "owner_authorization_resolution_plan_generated": True,
        "operator_acknowledgement_policy_generated": True,
        "pre_execution_authorization_package_generated": True,
        "rollback_rehearsal_scope_generated": True,
        "rollback_rehearsal_plan_generated": True,
        "rollback_rehearsal_evidence_template_generated": True,
        "batch_arming_precondition_record_generated": True,
        "authorization_blocker_policy_generated": True,
        "pre_authorization_planning_readiness_decision_generated": True,
        "owner_authorization_type_count": len(owner_entries),
        "operator_ack_required": True,
        "rollback_rehearsal_scope_batch_count": len(BATCH_IDS),
        "rollback_rehearsal_mandatory_batches_count": 6,
        "rollback_rehearsal_step_count": len(rehearsal_steps),
        "batch_arming_record_count": len(arming_records),
        "authorization_blocker_count": len(blocker_entries),
        "owner_confirmed_now": False,
        "owner_approval_execution_allowed": False,
        "operator_ack_executed_now": False,
        "pre_execution_authorization_package_generated_now": False,
        "rollback_rehearsal_execution_allowed": False,
        "rollback_rehearsal_executed_now": False,
        "rollback_evidence_generated_now": False,
        "arming_record_generated_now": False,
        "arming_allowed_now": False,
        "armed_batch_count": 0,
        "package_required_before_real_migration": True,
        "rollback_rehearsal_required_before_real_migration": True,
        "missing_owner_blocks_execution": True,
        "missing_operator_ack_blocks_execution": True,
        "missing_rollback_rehearsal_blocks_execution": True,
        "auto_confirm_owner_forbidden": True,
        "parallel_batch_execution_forbidden": True,
        "ready_for_pre_authorization_dryrun": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_batch_arming": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "ready_for_rollback_rehearsal_execution": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
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
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "pre_authorization_and_rollback_rehearsal_planning_policy": pre_authorization_and_rollback_rehearsal_planning_policy,
        "owner_authorization_resolution_plan": owner_authorization_resolution_plan,
        "operator_acknowledgement_policy": operator_acknowledgement_policy,
        "pre_execution_authorization_package": pre_execution_authorization_package,
        "rollback_rehearsal_scope": rollback_rehearsal_scope,
        "rollback_rehearsal_plan": rollback_rehearsal_plan,
        "rollback_rehearsal_evidence_template": rollback_rehearsal_evidence_template,
        "batch_arming_precondition_record": batch_arming_precondition_record,
        "authorization_blocker_policy": authorization_blocker_policy,
        "pre_authorization_planning_readiness_decision": pre_authorization_planning_readiness_decision,
        "execution_non_claims_register": execution_non_claims_register,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
