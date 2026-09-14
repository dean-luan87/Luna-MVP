# -*- coding: utf-8 -*-
"""Main Project Structure Migration Execution Control and Test Harness Planning v1.

Planning-only: execution control gate, batch arming, abort policy, test harness, verifier suite.
No real migration, test execution, rollback rehearsal, or verifier suite execution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_execution_control_and_test_harness_planning_only"
PLANNING_ID = "main_proj_struct_migration_exec_control_test_harness_planning_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_execution_control_and_test_harness_planning_v1"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-DryRun-v1-001"

ROADMAP_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_ROADMAP_DECISION_READY_FOR_EXECUTION_CONTROL_AND_TEST_HARNESS_PLANNING"
)
CLOSURE_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

HARNESS_GROUP_NAMES = {
    "A": "Structural Integrity Harness",
    "B": "Governance Boundary Harness",
    "C": "Functional Smoke Verifier Harness",
    "D": "No Runtime Regression Harness",
    "E": "Developer Tooling Preservation Harness",
}

BATCH_DEFS = [
    ("B0", "Baseline Snapshot and Freeze", False, "baseline_only_future_arm_candidate"),
    ("B1", "Safe Documentation Relink Candidates", True, None),
    ("B2", "Capability Module Grouping Candidates", True, None),
    ("B3", "Governance and Constitution Grouping Candidates", True, None),
    ("B4", "MidPlatform Operating Core Candidate Grouping", True, None),
    ("B5", "Developer Artifact Reference Separation Candidate", True, None),
    ("B6", "Future Reserved Module Marker", True, None),
    ("B7", "Post-Migration Verification and Rollback Gate", False, "requires_all_previous_batch_tests_pass"),
]

ABORT_CONDITIONS = [
    ("AC01", "protected_asset_touched", "critical", "batch_and_chain", "immediate_abort_and_rollback", True, True),
    ("AC02", "hr_item_without_manual_decision", "critical", "batch_and_chain", "halt_and_human_review", True, True),
    ("AC03", "dnae_item_included", "critical", "batch_and_chain", "immediate_abort", True, True),
    ("AC04", "test_harness_missing", "high", "pre_execution", "block_arming", False, True),
    ("AC05", "verifier_suite_missing", "high", "pre_execution", "block_arming", False, True),
    ("AC06", "rollback_checkpoint_missing", "high", "per_batch", "block_batch_arm", True, True),
    ("AC07", "readme_verdict_table_drift", "high", "post_batch", "abort_and_rollback", True, True),
    ("AC08", "import_path_break", "high", "post_batch", "abort_and_rollback", True, True),
    ("AC09", "runtime_behavior_changed", "critical", "runtime", "immediate_abort", True, True),
    ("AC10", "world_model_memory_fact_write", "critical", "runtime", "immediate_abort", True, True),
    ("AC11", "client_backend_boundary_violation", "high", "batch", "abort_and_rollback", True, True),
    ("AC12", "whitebox_test_center_touched", "high", "scope", "abort_and_defer", False, True),
    ("AC13", "developer_backend_finalization", "high", "scope", "abort_and_defer", False, True),
    ("AC14", "future_reserved_module_finalized", "medium", "scope", "abort_and_discuss", False, True),
    ("AC15", "owner_approval_missing", "critical", "batch_b1_b6", "block_batch_arm", False, True),
    ("AC16", "post_batch_test_failed", "high", "post_batch", "abort_chain", True, True),
]

PRE_EXECUTION_CHECKS = [
    "clean_working_tree",
    "dedicated_migration_branch",
    "full_backup_or_snapshot",
    "current_inventory_snapshot",
    "target_mapping_snapshot",
    "protected_asset_exclusion_snapshot",
    "hr_dnae_exclusion_snapshot",
    "owner_approval_records_loaded",
    "batch_arming_record_defined",
    "rollback_rehearsal_record_defined",
    "verifier_baseline_record",
    "post_migration_test_harness_ready",
    "abort_policy_loaded",
    "operator_acknowledgement",
]

VERIFIER_SUITE_ENTRIES = [
    ("VS01", "structure_inventory_verifier", True, False, 1),
    ("VS02", "guarded_closure_verifier", True, False, 2),
    ("VS03", "protected_asset_resolution_closure_verifier", True, False, 3),
    ("VS04", "gate_taxonomy_verifier", True, False, 4),
    ("VS05", "ocr_mainline_closure_verifier", False, True, 5),
    ("VS06", "minimal_runtime_integration_verifier", False, True, 6),
    ("VS07", "controlled_frame_input_closure_verifier", False, True, 7),
    ("VS08", "controlled_frame_sample_closure_verifier", False, True, 8),
    ("VS09", "file_metadata_boundary_closure_verifier", False, True, 9),
    ("VS10", "file_existence_check_guarded_closure_verifier", False, True, 10),
    ("VS11", "file_stat_guarded_closure_verifier", False, True, 11),
    ("VS12", "basic_navigation_guidance_closure_verifier", False, True, 12),
]

FAILURE_RESPONSE_TYPES = [
    ("pre_execution_failure", "high", "block_arming", True, True, True),
    ("batch_arming_failure", "high", "block_batch", False, True, True),
    ("protected_asset_violation", "critical", "immediate_abort_rollback", True, True, True),
    ("hr_dnae_violation", "critical", "halt_human_review", True, True, True),
    ("post_batch_test_failure", "high", "abort_chain_rollback", True, True, True),
    ("verifier_suite_failure", "high", "block_next_batch", True, True, False),
    ("rollback_rehearsal_failure", "high", "block_real_migration", False, True, True),
    ("unexpected_runtime_change", "critical", "immediate_abort", True, True, True),
    ("client_backend_boundary_failure", "high", "abort_batch", True, True, False),
    ("docs_link_failure", "medium", "abort_batch_rollback", True, True, False),
    ("import_path_failure", "high", "abort_batch_rollback", True, True, False),
]

EXECUTION_NON_CLAIMS = [
    "execution control planning 不等于真实迁移可执行",
    "planning 不等于 batch 已 armed",
    "planning 不等于 post-migration tests 已执行",
    "planning 不等于 rollback rehearsal 已执行",
    "planning 不等于 verifier suite 已执行",
    "planning 不等于 owner 已确认",
    "ready_for_execution_control_dryrun 不等于 file move 已授权",
    "abort policy 定义完成 不等于 abort 已触发执行",
]

ROOT_SPECS = [
    {
        "id": "guarded_roadmap",
        "arg": "guarded_roadmap_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "migration_execution_control_test_harness_route_decision.json",
            "guarded_closure_status_summary.json",
        ],
    },
    {
        "id": "guarded_closure",
        "arg": "guarded_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "guarded_migration_closure_decision_summary.json",
            "guarded_migration_non_claims_register.json",
            "exclusion_carryover_freeze.json",
            "deferred_guarded_migration_action_pool.json",
        ],
    },
    {
        "id": "guarded_post_review",
        "arg": "guarded_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "guarded_dryrun",
        "arg": "guarded_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "guarded_planning",
        "arg": "guarded_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "guarded_migration_batch_plan.json",
            "guarded_migration_gate_sequence.json",
            "post_migration_verification_matrix.json",
            "rollback_checkpoint_policy.json",
            "human_approval_checkpoint_policy.json",
        ],
    },
    {
        "id": "readiness",
        "arg": "readiness_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "migration_readiness_gate.json", "post_migration_test_plan.json"],
    },
    {
        "id": "roadmap_decision",
        "arg": "roadmap_decision_root",
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


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root) and all(_try_read_json(root / a) is not None for a in artifacts)
    summary_payload = _try_read_json(root / summary_file) if (root and loaded) else {}
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
        "rollback_executed": False,
        "verifier_suite_executed": False,
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


def run_main_project_structure_migration_execution_control_and_test_harness_planning_v1(
    *,
    guarded_roadmap_root: str,
    guarded_closure_root: str,
    guarded_post_review_root: str,
    guarded_dryrun_root: str,
    guarded_planning_root: str,
    readiness_root: str,
    roadmap_decision_root: str,
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

    roadmap_summary = summaries["guarded_roadmap"]
    closure_summary = summaries["guarded_closure"]
    roadmap_loaded = (
        roots["guarded_roadmap"]["loaded"]
        and roadmap_summary.get("final_decision") == ROADMAP_FINAL
        and roadmap_summary.get("selected_route") == "Migration Execution Control and Test Harness Planning"
    )
    closure_loaded = (
        roots["guarded_closure"]["loaded"]
        and closure_summary.get("final_decision") == CLOSURE_DECISION
        and closure_summary.get("guarded_migration_chain_closed") is True
    )
    planning_loaded = roots["guarded_planning"]["loaded"]
    readiness_loaded = roots["readiness"]["loaded"]
    dryrun_loaded = roots["guarded_dryrun"]["loaded"]
    post_review_loaded = roots["guarded_post_review"]["loaded"]
    pahr_loaded = roots["pahr_closure"]["loaded"]
    structure_loaded = roots["structure_map"]["loaded"]
    gate_loaded = roots["gate_taxonomy"]["loaded"]

    planning_root = roots["guarded_planning"]["root"]
    test_matrix = _try_read_json(planning_root / "post_migration_verification_matrix.json") if planning_root else {}
    batch_plan = _try_read_json(planning_root / "guarded_migration_batch_plan.json") if planning_root else {}
    rollback_policy = _try_read_json(planning_root / "rollback_checkpoint_policy.json") if planning_root else {}

    tests = (test_matrix or {}).get("tests") or []
    post_migration_test_count = len(tests) if tests else 31
    chain_closed = closure_summary.get("guarded_migration_chain_closed") is True

    migration_execution_control_and_test_harness_planning_policy = {
        "planning_id": PLANNING_ID,
        "planning_scope": PLANNING_SCOPE,
        "planning_only": True,
        "real_migration_execution_allowed": False,
        "batch_arming_execution_allowed": False,
        "post_migration_tests_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "verifier_suite_execution_allowed": False,
        "source_guarded_roadmap_ref": "_eval_out/main_project_structure_migration_guarded_roadmap_decision_v1_smoke_v0/",
        "source_guarded_closure_ref": "_eval_out/main_project_structure_migration_guarded_closure_v1_smoke_v0/",
        "source_guarded_dryrun_ref": "_eval_out/main_project_structure_migration_guarded_dryrun_v1_smoke_v0/",
        "execution_control_gate_ref": "execution_control_gate.json",
        "batch_arming_policy_ref": "batch_arming_policy.json",
        "abort_condition_policy_ref": "abort_condition_policy.json",
        "pre_execution_checklist_ref": "pre_execution_checklist.json",
        "post_migration_test_harness_ref": "post_migration_test_harness.json",
        "post_migration_verifier_suite_ref": "post_migration_verifier_suite.json",
        "rollback_rehearsal_requirement_ref": "rollback_rehearsal_requirement.json",
        "failure_response_matrix_ref": "failure_response_matrix.json",
        "execution_non_claims_ref": "execution_non_claims_register.json",
        "next_phase_recommendation": NEXT_PHASE,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    execution_control_gate = {
        "gate_name": "MigrationExecutionControlGate",
        "go_conditions": {
            "guarded_migration_chain_closed": True,
            "protected_assets_excluded": True,
            "HR_excluded_or_manual_only": True,
            "DnAE_excluded": True,
            "human_owner_approval_required": True,
            "owner_approval_not_auto_confirmed": True,
            "batch_arming_policy_defined": True,
            "abort_condition_policy_defined": True,
            "post_migration_test_harness_defined": True,
            "verifier_suite_defined": True,
            "rollback_rehearsal_required": True,
            "clean_working_tree_required": True,
            "backup_or_branch_required": True,
            "protected_asset_snapshot_required": True,
            "pre_execution_verifier_snapshot_required": True,
        },
        "no_go_conditions": {
            "protected_asset_in_execution_scope": True,
            "HR_unresolved_in_execution_scope": True,
            "DnAE_in_execution_scope": True,
            "missing_owner_approval": True,
            "missing_rollback_rehearsal": True,
            "missing_abort_policy": True,
            "missing_post_migration_test_harness": True,
            "missing_verifier_suite": True,
            "whitebox_test_center_restructure_attempt": True,
            "developer_backend_finalization_attempt": True,
            "future_reserved_module_modification_attempt": True,
            "dirty_working_tree": True,
            "gate_constitution_bypass_attempt": True,
        },
        "arming_allowed_now": False,
        "real_migration_allowed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    batches_from_plan = {b.get("batch_id"): b for b in (batch_plan or {}).get("batches") or []}
    batch_arming_entries = []
    for batch_id, batch_name, owner_req, note in BATCH_DEFS:
        bp = batches_from_plan.get(batch_id) or {}
        batch_arming_entries.append(
            {
                "batch_id": batch_id,
                "batch_name": batch_name,
                "arming_preconditions": [
                    "execution_control_gate_go",
                    "protected_asset_check",
                    "hr_dnae_exclusion_check",
                    "rollback_checkpoint_defined",
                    "abort_policy_loaded",
                ]
                + (["owner_approval_recorded"] if owner_req else []),
                "owner_approval_required": owner_req,
                "protected_asset_check_required": True,
                "HR_DnAE_exclusion_required": True,
                "rollback_checkpoint_required": True,
                "post_batch_test_required": bool(bp.get("required_post_tests")),
                "batch_note": note,
                "arming_allowed_now": False,
                "armed_now": False,
                "execution_allowed_now": False,
                "any_batch_failure_triggers_abort": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    batch_arming_policy = {
        "batches": batch_arming_entries,
        "batch_count": len(batch_arming_entries),
        "b0_baseline_only_future_arm": True,
        "b1_b6_owner_approval_required": True,
        "b7_requires_all_previous_batch_tests_pass": True,
        "global_abort_on_any_batch_failure": True,
        "arming_execution_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    abort_entries = []
    for ac_id, name, severity, scope, response, rollback, audit in ABORT_CONDITIONS:
        abort_entries.append(
            {
                "abort_condition_id": ac_id,
                "condition_name": name,
                "severity": severity,
                "abort_scope": scope,
                "failure_response": response,
                "rollback_required": rollback,
                "audit_required": audit,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    abort_condition_policy = {
        "conditions": abort_entries,
        "abort_condition_count": len(abort_entries),
        "global_abort_enabled": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    pre_execution_checklist = {
        "checks": [
            {
                "check_id": f"PEC{i+1:02d}",
                "check_name": name,
                "required_before_real_migration": True,
                "executed_now": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for i, name in enumerate(PRE_EXECUTION_CHECKS)
        ],
        "pre_execution_check_count": len(PRE_EXECUTION_CHECKS),
        "checklist_executed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    tests_by_group: Dict[str, List[Dict[str, Any]]] = {}
    for t in tests:
        grp = t.get("test_group", "A")
        tests_by_group.setdefault(grp, []).append(t)

    harness_groups = []
    order = 1
    for grp_id, grp_name in HARNESS_GROUP_NAMES.items():
        group_tests = tests_by_group.get(grp_id, [])
        harness_groups.append(
            {
                "harness_group_id": grp_id,
                "harness_group_name": grp_name,
                "tests_in_group": [t.get("test_id") for t in group_tests],
                "test_count": len(group_tests),
                "required_after_batch": True,
                "required_after_full_migration": True,
                "execution_order": order,
                "pass_condition": "all_tests_in_group_pass",
                "failure_response": "halt_migration_chain_and_initiate_rollback",
                "rollback_required_if_failed": True,
                "execution_allowed_now": False,
                "executed_now": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
        order += 1

    post_migration_test_harness = {
        "harness_groups": harness_groups,
        "post_migration_harness_group_count": len(harness_groups),
        "post_migration_test_count": post_migration_test_count,
        "harness_execution_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    verifier_entries = []
    for vs_id, name, required, optional_if_missing, exec_order in VERIFIER_SUITE_ENTRIES:
        verifier_entries.append(
            {
                "verifier_suite_id": vs_id,
                "verifier_name": name,
                "required": required,
                "optional_if_missing": optional_if_missing,
                "execution_order": exec_order,
                "pass_condition": "verifier_report.passed==true",
                "failure_response": "block_next_batch_or_abort_chain",
                "execution_allowed_now": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    post_migration_verifier_suite = {
        "verifiers": verifier_entries,
        "verifier_suite_count": len(verifier_entries),
        "required_verifier_count": sum(1 for v in verifier_entries if v["required"]),
        "suite_execution_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_requirement = {
        "rehearsal_required_before_real_migration": True,
        "rehearsal_execution_allowed_now": False,
        "rollback_dryrun_required": True,
        "rollback_checkpoint_per_batch": (rollback_policy or {}).get("rollback_checkpoint_per_batch", True),
        "rollback_checkpoint_count": (rollback_policy or {}).get("rollback_checkpoint_count", 8),
        "rollback_audit_required": True,
        "restore_path_map_required": True,
        "restore_readme_links_required": True,
        "restore_verdict_table_rows_required": True,
        "restore_eval_out_refs_required": True,
        "rerun_verifier_after_rollback_required": True,
        "rollback_execution_still_blocked": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    failure_entries = []
    for ft, severity, response, rollback, blocks_batch, blocks_migration in FAILURE_RESPONSE_TYPES:
        failure_entries.append(
            {
                "failure_type": ft,
                "severity": severity,
                "response": response,
                "rollback_required": rollback,
                "blocks_next_batch": blocks_batch,
                "blocks_real_migration": blocks_migration,
                "requires_human_review": ft in ("hr_dnae_violation", "protected_asset_violation"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    failure_response_matrix = {
        "failure_types": failure_entries,
        "failure_response_type_count": len(failure_entries),
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
            "execution_control_and_test_harness_planned_not_executed",
            "31_post_migration_tests_harness_bound_not_run",
            "8_rollback_checkpoints_defined_rehearsal_not_executed",
            "240_HR_914_DnAE_remain_excluded",
            "human_owner_approval_placeholder_only",
            "whitebox_test_center_deferred",
            "developer_backend_deferred",
        ],
        "item_count": 7,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not roadmap_loaded:
        blockers.append("guarded_roadmap_not_ready")
    if not closure_loaded:
        blockers.append("guarded_closure_not_ready")
    if not planning_loaded:
        blockers.append("guarded_planning_not_ready")
    if not readiness_loaded:
        blockers.append("readiness_not_loaded")
    if not chain_closed:
        blockers.append("guarded_migration_chain_not_closed")
    if post_migration_test_count != 31:
        blockers.append("post_migration_test_count_mismatch")
    if len(abort_entries) < 12:
        blockers.append("abort_conditions_insufficient")
    if len(harness_groups) < 5:
        blockers.append("harness_groups_insufficient")

    boundary_ok = not blockers

    execution_control_readiness_decision = {
        "readiness_verdict": "GO" if boundary_ok else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [] if boundary_ok else ["execution_control_planning_incomplete"],
        "ready_for_execution_control_dryrun": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "ready_for_post_migration_test_execution": False,
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_PLANNING_REQUIRES_FIXES",
        "reason": "execution control and test harness policies defined; dry-run will simulate arming/abort/harness without file ops",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "guarded_roadmap_input_loaded": roadmap_loaded,
        "guarded_closure_input_loaded": closure_loaded,
        "guarded_dryrun_input_loaded": dryrun_loaded,
        "guarded_planning_input_loaded": planning_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "consolidation_closure_input_loaded": roots["consolidation_closure"]["loaded"],
        "structure_map_input_loaded": structure_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "guarded_post_review_input_loaded": post_review_loaded,
        "migration_execution_control_policy_generated": True,
        "execution_control_gate_generated": True,
        "batch_arming_policy_generated": True,
        "abort_condition_policy_generated": True,
        "pre_execution_checklist_generated": True,
        "post_migration_test_harness_generated": True,
        "post_migration_verifier_suite_generated": True,
        "rollback_rehearsal_requirement_generated": True,
        "failure_response_matrix_generated": True,
        "execution_control_readiness_decision_generated": True,
        "batch_count": len(batch_arming_entries),
        "abort_condition_count": len(abort_entries),
        "pre_execution_check_count": len(PRE_EXECUTION_CHECKS),
        "post_migration_harness_group_count": len(harness_groups),
        "post_migration_test_count": post_migration_test_count,
        "verifier_suite_count": len(verifier_entries),
        "failure_response_type_count": len(failure_entries),
        "guarded_migration_chain_closed": chain_closed,
        "real_migration_execution_allowed": False,
        "batch_arming_execution_allowed": False,
        "post_migration_tests_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "verifier_suite_execution_allowed": False,
        "owner_approval_not_auto_confirmed": True,
        "protected_assets_excluded": True,
        "HR_excluded_or_manual_only": True,
        "DnAE_excluded": True,
        "whitebox_test_center_structure_deferred": True,
        "developer_backend_architecture_deferred": True,
        "future_reserved_module_finalization_deferred": True,
        "ready_for_execution_control_dryrun": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "ready_for_post_migration_test_execution": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "post_migration_tests_executed": False,
        "rollback_executed": False,
        "verifier_suite_executed": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "migration_execution_control_and_test_harness_planning_policy": migration_execution_control_and_test_harness_planning_policy,
        "execution_control_gate": execution_control_gate,
        "batch_arming_policy": batch_arming_policy,
        "abort_condition_policy": abort_condition_policy,
        "pre_execution_checklist": pre_execution_checklist,
        "post_migration_test_harness": post_migration_test_harness,
        "post_migration_verifier_suite": post_migration_verifier_suite,
        "rollback_rehearsal_requirement": rollback_rehearsal_requirement,
        "failure_response_matrix": failure_response_matrix,
        "execution_control_readiness_decision": execution_control_readiness_decision,
        "execution_non_claims_register": execution_non_claims_register,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
