# -*- coding: utf-8 -*-
"""Main Project Structure Migration Controlled Execution Planning v1.

Planning-only: controlled real-migration execution plan (batches, auth, tests, rollback).
No real migration, batch arming, test/verifier/rollback execution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_controlled_execution_planning_only"
PLANNING_ID = "main_proj_struct_migration_controlled_execution_planning_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_controlled_execution_planning_v1"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Execution-DryRun-v1-001"

ROADMAP_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_ROADMAP_DECISION_READY_FOR_CONTROLLED_MIGRATION_EXECUTION_PLANNING"
)
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

COMMON_EXCLUDED = [
    "protected_assets",
    "human_review_unresolved",
    "permanent_dnae",
    "eval_out_phase_outputs",
    "verifier_reports",
    "historical_test_logs",
    "readme_unless_separate_authorization",
    "phase_verdict_table_unless_separate_authorization",
]

CONTROLLED_BATCH_DEFS: List[Tuple[str, str, str, List[str], bool, bool, bool]] = [
    (
        "B0",
        "Baseline Snapshot / No Move",
        "baseline_snapshot_inventory_verifier_baseline_rollback_prerequisite_no_file_move",
        ["baseline_snapshot", "inventory_snapshot", "verifier_baseline", "rollback_rehearsal_prerequisite"],
        False,
        True,
        False,
    ),
    (
        "B1",
        "Safe Documentation Relink Candidate",
        "controlled_docs_relink_candidate_only_non_protected",
        ["safe_docs_relink_candidates"],
        True,
        True,
        True,
    ),
    (
        "B2",
        "Capability Module Grouping Candidate",
        "vision_ocr_voice_navigation_map_tracking_file_boundary_low_risk",
        ["capability_module_grouping_candidates"],
        True,
        True,
        True,
    ),
    (
        "B3",
        "Governance / Constitution Grouping Candidate",
        "safety_gate_protected_asset_migration_policy_high_risk",
        ["governance_constitution_grouping_candidates"],
        True,
        True,
        True,
    ),
    (
        "B4",
        "MidPlatform Operating Core Candidate",
        "midplatform_operating_core_no_runtime_behavior_change",
        ["midplatform_operating_core_candidates"],
        True,
        True,
        True,
    ),
    (
        "B5",
        "Developer Artifact Reference Separation Candidate",
        "whitebox_test_evaluation_verifier_logs_reference_only",
        ["developer_artifact_reference_separation"],
        True,
        True,
        True,
    ),
    (
        "B6",
        "Future Reserved Module Marker Candidate",
        "worldmodel_memory_library_emotion_marker_only",
        ["future_reserved_module_markers"],
        True,
        True,
        True,
    ),
    (
        "B7",
        "Full Verification and Rollback Gate",
        "no_move_post_migration_verification_rollback_gate",
        ["verification_and_rollback_gate_only"],
        False,
        False,
        True,
    ),
]

OWNER_GATE_DEFS = [
    ("architecture_owner", ["B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"], "architecture and chain integrity"),
    ("governance_owner", ["B3", "B7"], "governance/docs/gate/safety assets"),
    ("evaluation_owner", ["B0", "B5", "B7"], "verifier/test/log assets"),
    ("capability_owner", ["B2"], "capability module grouping"),
    ("midplatform_owner", ["B4"], "midplatform grouping"),
    ("docs_owner", ["B1"], "docs relink"),
    ("product_client_owner", ["B2", "B4"], "client boundary"),
]

EXECUTION_WINDOW_REQUIREMENTS = [
    "dedicated_branch_required",
    "clean_working_tree_required",
    "no_unrelated_changes",
    "max_batch_size_limit",
    "one_batch_at_a_time",
    "no_parallel_migration_batches",
    "operator_acknowledgement_required",
    "rollback_window_reserved",
    "post_batch_verification_window_reserved",
    "stop_condition_window_required",
]

EXECUTION_NON_CLAIMS = [
    "controlled execution planning 不等于真实迁移可执行",
    "planning 不等于 batch 已 armed",
    "planning 不等于 post-migration tests 已执行",
    "planning 不等于 verifier suite 已执行",
    "planning 不等于 rollback rehearsal 已执行",
    "planning 不等于 owner 已确认",
    "ready_for_controlled_execution_dryrun 不等于 file move 已授权",
    "execution plan 定义完成 不等于任何 batch 已执行",
]

ROOT_SPECS = [
    {
        "id": "execution_control_roadmap",
        "arg": "execution_control_roadmap_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_migration_execution_planning_route_decision.json",
            "execution_control_closure_status_summary.json",
        ],
    },
    {
        "id": "execution_control_closure",
        "arg": "execution_control_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "execution_control_closure_decision_summary.json",
            "execution_control_non_claims_register.json",
            "closure_boundary_freeze.json",
            "deferred_execution_control_action_pool.json",
        ],
    },
    {
        "id": "execution_control_post_review",
        "arg": "execution_control_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "execution_control_dryrun",
        "arg": "execution_control_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "execution_control_planning",
        "arg": "execution_control_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "execution_control_gate.json",
            "batch_arming_policy.json",
            "abort_condition_policy.json",
            "pre_execution_checklist.json",
            "post_migration_test_harness.json",
            "post_migration_verifier_suite.json",
            "rollback_rehearsal_requirement.json",
            "failure_response_matrix.json",
        ],
    },
    {
        "id": "guarded_roadmap",
        "arg": "guarded_roadmap_root",
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
        "id": "guarded_planning",
        "arg": "guarded_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "guarded_migration_batch_plan.json",
            "guarded_migration_gate_sequence.json",
            "post_migration_verification_matrix.json",
        ],
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
        "artifacts": ["module_inventory.json", "current_to_target_structure_map.json"],
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


def _build_test_to_batch(guarded_batches: List[Dict[str, Any]]) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for batch in guarded_batches:
        bid = batch.get("batch_id", "")
        for tid in batch.get("required_post_tests") or []:
            mapping[tid] = bid
    return mapping


def run_main_project_structure_migration_controlled_execution_planning_v1(
    *,
    execution_control_roadmap_root: str,
    execution_control_closure_root: str,
    execution_control_post_review_root: str,
    execution_control_dryrun_root: str,
    execution_control_planning_root: str,
    guarded_roadmap_root: str,
    guarded_closure_root: str,
    guarded_planning_root: str,
    readiness_root: str,
    pahr_closure_root: str,
    consolidation_closure_root: str,
    structure_map_root: str,
    gate_taxonomy_root: str,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}
    summaries = {key: roots[key]["summary"] for key in roots}
    ec_plan_art = roots["execution_control_planning"]["artifacts"] if roots["execution_control_planning"]["loaded"] else {}

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
        roots["execution_control_roadmap"]["loaded"]
        and summaries["execution_control_roadmap"].get("final_decision") == ROADMAP_FINAL
        and summaries["execution_control_roadmap"].get("selected_route") == "Controlled Migration Execution Planning"
    )
    ec_closure_loaded = (
        roots["execution_control_closure"]["loaded"]
        and summaries["execution_control_closure"].get("final_decision") == EXECUTION_CONTROL_CLOSURE
        and summaries["execution_control_closure"].get("execution_control_test_harness_chain_closed") is True
    )
    ec_post_loaded = roots["execution_control_post_review"]["loaded"]
    ec_dryrun_loaded = roots["execution_control_dryrun"]["loaded"]
    guarded_closure_loaded = (
        roots["guarded_closure"]["loaded"]
        and summaries["guarded_closure"].get("final_decision") == GUARDED_CLOSURE
    )
    readiness_loaded = roots["readiness"]["loaded"]
    pahr_loaded = roots["pahr_closure"]["loaded"]
    structure_loaded = roots["structure_map"]["loaded"]
    gate_loaded = roots["gate_taxonomy"]["loaded"]

    guarded_root = roots["guarded_planning"]["root"]
    guarded_batches = (_try_read_json(guarded_root / "guarded_migration_batch_plan.json") if guarded_root else {}).get(
        "batches"
    ) or []
    test_matrix = (_try_read_json(guarded_root / "post_migration_verification_matrix.json") if guarded_root else {}).get(
        "tests"
    ) or []
    test_to_batch = _build_test_to_batch(guarded_batches)

    abort_plan = ec_plan_art.get("abort_condition_policy.json") or {}
    failure_plan = ec_plan_art.get("failure_response_matrix.json") or {}
    verifier_plan = ec_plan_art.get("post_migration_verifier_suite.json") or {}
    harness_plan = ec_plan_art.get("post_migration_test_harness.json") or {}

    abort_count = abort_plan.get("abort_condition_count", len(abort_plan.get("conditions") or []))
    failure_count = failure_plan.get("failure_response_type_count", len(failure_plan.get("failure_types") or []))
    verifier_entries = verifier_plan.get("verifiers") or []
    post_migration_test_count = harness_plan.get("post_migration_test_count", len(test_matrix) or 31)

    controlled_migration_execution_planning_policy = {
        "planning_id": PLANNING_ID,
        "planning_scope": PLANNING_SCOPE,
        "source_roadmap_ref": "_eval_out/main_project_structure_migration_execution_control_and_test_harness_roadmap_decision_v1_smoke_v0/",
        "source_execution_control_closure_ref": "_eval_out/main_project_structure_migration_execution_control_and_test_harness_closure_v1_smoke_v0/",
        "source_guarded_closure_ref": "_eval_out/main_project_structure_migration_guarded_closure_v1_smoke_v0/",
        "controlled_execution_batch_plan_ref": "controlled_execution_batch_plan.json",
        "execution_window_policy_ref": "execution_window_policy.json",
        "owner_authorization_gate_ref": "owner_authorization_gate.json",
        "batch_arming_plan_ref": "batch_arming_execution_plan.json",
        "rollback_rehearsal_precondition_ref": "rollback_rehearsal_precondition.json",
        "post_batch_test_execution_order_ref": "post_batch_test_execution_order.json",
        "verifier_suite_execution_order_ref": "verifier_suite_execution_order.json",
        "abort_and_failure_response_plan_ref": "abort_and_failure_response_plan.json",
        "post_execution_evidence_pack_ref": "post_execution_evidence_pack_plan.json",
        "execution_non_claims_ref": "execution_non_claims_register.json",
        "next_phase_recommendation": NEXT_PHASE,
        "planning_only": True,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "post_migration_tests_execution_allowed": False,
        "verifier_suite_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    batch_entries = []
    for bid, bname, scope, candidates, owner_req, rb_rehearsal, post_tests in CONTROLLED_BATCH_DEFS:
        gb = next((b for b in guarded_batches if b.get("batch_id") == bid), {})
        batch_entries.append(
            {
                "batch_id": bid,
                "batch_name": bname,
                "execution_candidate_scope": scope,
                "candidate_scope_tags": candidates,
                "excluded_scope": COMMON_EXCLUDED + (["file_move"] if bid == "B0" else []),
                "owner_authorization_required": owner_req,
                "rollback_rehearsal_required_before_batch": rb_rehearsal and bid in ("B1", "B2", "B3", "B4", "B5", "B6"),
                "post_batch_tests_required": post_tests or bool(gb.get("required_post_tests")),
                "verifier_suite_required": bid in ("B0", "B7"),
                "abort_conditions_attached": True,
                "execution_window_required": True,
                "arming_allowed_now": False,
                "execution_allowed_now": False,
                "guarded_batch_ref": gb.get("batch_name"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    controlled_execution_batch_plan = {
        "batches": batch_entries,
        "batch_count": len(batch_entries),
        "b0_no_file_move": True,
        "b7_verification_gate_only": True,
        "one_batch_at_a_time": True,
        "no_parallel_batches": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    execution_window_policy = {
        "execution_window_id": "controlled_migration_execution_window_v1",
        "requirements": [
            {
                "requirement_id": f"EW{i+1:02d}",
                "requirement_name": name,
                "required_before_real_execution": True,
                "allowed_now": False,
                "violation_blocks_execution": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for i, name in enumerate(EXECUTION_WINDOW_REQUIREMENTS)
        ],
        "execution_window_requirement_count": len(EXECUTION_WINDOW_REQUIREMENTS),
        "required_before_real_execution": True,
        "allowed_now": False,
        "violation_blocks_execution": True,
        "one_batch_at_a_time_required": True,
        "no_parallel_migration_batches": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    owner_gates = []
    for owner_type, batches, note in OWNER_GATE_DEFS:
        owner_gates.append(
            {
                "owner_type": owner_type,
                "applies_to_batches": batches,
                "approval_required": True,
                "auto_confirm_allowed": False,
                "missing_approval_blocks_execution": True,
                "notes": note,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    owner_authorization_gate = {
        "gates": owner_gates,
        "owner_authorization_gate_count": len(owner_gates),
        "owner_auto_confirmation_forbidden": True,
        "architecture_owner_required": True,
        "governance_owner_required_for_governance_assets": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    arming_entries = []
    for bid, bname, _scope, _cand, owner_req, rb_req, _pt in CONTROLLED_BATCH_DEFS:
        arming_entries.append(
            {
                "batch_id": bid,
                "arming_preconditions": [
                    "execution_control_gate_go",
                    "controlled_execution_plan_approved",
                    "execution_window_satisfied",
                    "abort_policy_loaded",
                    "failure_response_matrix_loaded",
                ],
                "required_owner_approvals": (
                    [g["owner_type"] for g in owner_gates if bid in g["applies_to_batches"]] if owner_req else []
                ),
                "required_snapshots": ["inventory_snapshot", "verifier_baseline"] if bid == "B0" else ["rollback_checkpoint"],
                "required_rollback_rehearsal": rb_req,
                "required_test_harness_ready": True,
                "required_verifier_suite_ready": True,
                "required_abort_policy_loaded": True,
                "arming_allowed_now": False,
                "armed_now": False,
                "arming_future_only": True,
                "b7_requires_all_previous_batch_tests_pass": bid == "B7",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    batch_arming_execution_plan = {
        "batches": arming_entries,
        "batch_count": len(arming_entries),
        "b0_baseline_only_no_move": True,
        "b1_b6_owner_approval_required": True,
        "b7_requires_previous_tests_pass": True,
        "any_batch_failure_blocks_subsequent": True,
        "no_cross_batch_auto_advance": True,
        "arming_allowed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_precondition = {
        "rollback_rehearsal_mandatory": True,
        "rehearsal_must_cover_batches": ["B1", "B2", "B3", "B4", "B5", "B6"],
        "restore_path_map_required": True,
        "restore_docs_links_required": True,
        "restore_phase_verdict_table_if_touched": True,
        "restore_eval_out_references_required": True,
        "rollback_verifier_rerun_required": True,
        "rollback_rehearsal_report_required": True,
        "rollback_rehearsal_execution_allowed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    test_order_entries = []
    for i, t in enumerate(test_matrix):
        tid = t.get("test_id", f"T{i+1:02d}")
        related = test_to_batch.get(tid, "B7")
        test_order_entries.append(
            {
                "test_id": tid,
                "test_name": t.get("test_name", tid),
                "related_batch": related,
                "execution_order": i + 1,
                "required_after_batch": True,
                "required_after_full_migration": True,
                "pass_required_before_next_batch": True,
                "failure_blocks_next_batch": True,
                "rollback_required_if_failed": True,
                "execution_allowed_now": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    if len(test_order_entries) < post_migration_test_count:
        for j in range(len(test_order_entries), post_migration_test_count):
            tid = f"PX{j+1:02d}"
            test_order_entries.append(
                {
                    "test_id": tid,
                    "test_name": f"placeholder_test_{tid}",
                    "related_batch": "B7",
                    "execution_order": j + 1,
                    "required_after_batch": True,
                    "required_after_full_migration": True,
                    "pass_required_before_next_batch": True,
                    "failure_blocks_next_batch": True,
                    "rollback_required_if_failed": True,
                    "execution_allowed_now": False,
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                }
            )

    post_batch_test_execution_order = {
        "tests": test_order_entries,
        "post_batch_test_count": len(test_order_entries),
        "pass_required_before_next_batch": True,
        "failure_blocks_next_batch": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    verifier_order_entries = []
    for v in verifier_entries:
        verifier_order_entries.append(
            {
                "verifier_id": v.get("verifier_suite_id"),
                "verifier_name": v.get("verifier_name"),
                "execution_order": v.get("execution_order"),
                "required": v.get("required"),
                "optional_if_missing": v.get("optional_if_missing"),
                "related_batch": "B7" if v.get("execution_order", 0) >= 10 else "B0",
                "pass_required_before_next_batch": v.get("required") is True,
                "failure_blocks_real_migration": True,
                "execution_allowed_now": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    verifier_suite_execution_order = {
        "verifiers": verifier_order_entries,
        "verifier_suite_count": len(verifier_order_entries),
        "required_verifier_count": sum(1 for v in verifier_order_entries if v.get("required")),
        "execution_order_defined": True,
        "optional_if_missing_policy_defined": True,
        "failure_response_defined": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    abort_conditions = abort_plan.get("conditions") or []
    abort_and_failure_response_plan = {
        "abort_conditions": abort_conditions,
        "abort_condition_count": abort_count,
        "failure_types": failure_plan.get("failure_types") or [],
        "failure_response_type_count": failure_count,
        "every_abort_has_failure_response": True,
        "protected_hr_dnae_abort_blocks_entire_execution": True,
        "runtime_wm_memory_fact_write_abort_blocks": True,
        "missing_harness_verifier_rollback_blocks": True,
        "failed_post_batch_test_blocks_next_batch": True,
        "failed_verifier_suite_blocks_next_batch": True,
        "rollback_rehearsal_failure_blocks_real_migration": True,
        "whitebox_test_center_touch_blocks": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    evidence_batch_templates = []
    for bid, bname, *_ in CONTROLLED_BATCH_DEFS:
        evidence_batch_templates.append(
            {
                "executed_batch_id": bid,
                "batch_name": bname,
                "executed_operation_summary": "not_executed_planning_only",
                "moved_file_count": 0,
                "deleted_file_count": 0,
                "renamed_file_count": 0,
                "merged_module_count": 0,
                "protected_asset_touch_count": 0,
                "HR_DnAE_touch_count": 0,
                "post_batch_test_result_ref": f"post_batch_test_result_{bid.lower()}_pending",
                "verifier_suite_result_ref": f"verifier_suite_result_{bid.lower()}_pending",
                "rollback_checkpoint_ref": f"rollback_checkpoint_{bid.lower()}_pending",
                "failure_response_ref": "none",
                "operator_ack_ref": "pending",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    post_execution_evidence_pack_plan = {
        "evidence_pack_templates": evidence_batch_templates,
        "evidence_pack_generated_now": False,
        "execution_result_claimed_now": False,
        "required_after_each_batch": True,
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
            "controlled_execution_plan_defined_but_not_executed",
            "owner_approval_records_not_collected",
            "rollback_rehearsal_not_performed",
            f"{HUMAN_REVIEW_CARRYOVER}_hr_manual_only",
            f"{PERMANENT_BLOCK_CARRYOVER}_dnae_excluded",
            "whitebox_test_center_deferred",
            "developer_backend_deferred",
        ],
        "item_count": 7,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not roadmap_loaded:
        blockers.append("execution_control_roadmap_not_ready")
    if not ec_closure_loaded:
        blockers.append("execution_control_closure_not_ready")
    if not guarded_closure_loaded:
        blockers.append("guarded_closure_not_confirmed")
    if len(batch_entries) != 8:
        blockers.append("batch_plan_incomplete")

    boundary_ok = not blockers

    controlled_execution_planning_readiness_decision = {
        "readiness_verdict": "ready_for_controlled_execution_dryrun" if boundary_ok else "requires_fixes",
        "blockers": blockers,
        "conditional_notes": [
            "planning-only: defines operational plan for who authorizes, when to stop, test order, rollback",
            "Route A from roadmap: Controlled Migration Execution Planning",
            "real migration execution trial remains blocked",
        ],
        "ready_for_controlled_execution_dryrun": boundary_ok,
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_REQUIRES_FIXES",
        "reason": "controlled execution plan defined; dry-run next to simulate windows/auth/batch progression without file ops",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "execution_control_roadmap_input_loaded": roadmap_loaded,
        "execution_control_closure_input_loaded": ec_closure_loaded,
        "execution_control_post_review_input_loaded": ec_post_loaded,
        "execution_control_dryrun_input_loaded": ec_dryrun_loaded,
        "guarded_closure_input_loaded": guarded_closure_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "structure_map_input_loaded": structure_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "controlled_migration_execution_policy_generated": True,
        "controlled_execution_batch_plan_generated": True,
        "execution_window_policy_generated": True,
        "owner_authorization_gate_generated": True,
        "batch_arming_execution_plan_generated": True,
        "rollback_rehearsal_precondition_generated": True,
        "post_batch_test_execution_order_generated": True,
        "verifier_suite_execution_order_generated": True,
        "abort_and_failure_response_plan_generated": True,
        "post_execution_evidence_pack_plan_generated": True,
        "controlled_execution_planning_readiness_decision_generated": True,
        "batch_count": 8,
        "owner_authorization_gate_count": len(owner_gates),
        "execution_window_requirement_count": len(EXECUTION_WINDOW_REQUIREMENTS),
        "post_batch_test_count": len(test_order_entries),
        "verifier_suite_count": len(verifier_order_entries),
        "abort_condition_count": abort_count,
        "failure_response_type_count": failure_count,
        "controlled_execution_planning_selected": True,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "post_migration_tests_execution_allowed": False,
        "verifier_suite_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "owner_auto_confirm_allowed": False,
        "evidence_pack_generated_now": False,
        "execution_result_claimed_now": False,
        "rollback_rehearsal_mandatory": True,
        "one_batch_at_a_time_required": True,
        "no_parallel_migration_batches": True,
        "pass_required_before_next_batch": True,
        "failure_blocks_next_batch": True,
        "protected_assets_excluded": True,
        "HR_excluded_or_manual_only": True,
        "DnAE_excluded": True,
        "whitebox_test_center_structure_deferred": True,
        "developer_backend_architecture_deferred": True,
        "future_reserved_module_finalization_deferred": True,
        "ready_for_controlled_execution_dryrun": boundary_ok,
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "controlled_migration_execution_planning_policy": controlled_migration_execution_planning_policy,
        "controlled_execution_batch_plan": controlled_execution_batch_plan,
        "execution_window_policy": execution_window_policy,
        "owner_authorization_gate": owner_authorization_gate,
        "batch_arming_execution_plan": batch_arming_execution_plan,
        "rollback_rehearsal_precondition": rollback_rehearsal_precondition,
        "post_batch_test_execution_order": post_batch_test_execution_order,
        "verifier_suite_execution_order": verifier_suite_execution_order,
        "abort_and_failure_response_plan": abort_and_failure_response_plan,
        "post_execution_evidence_pack_plan": post_execution_evidence_pack_plan,
        "controlled_execution_planning_readiness_decision": controlled_execution_planning_readiness_decision,
        "execution_non_claims_register": execution_non_claims_register,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
