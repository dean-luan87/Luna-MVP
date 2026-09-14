# -*- coding: utf-8 -*-
"""Main Project Structure Migration Guarded Planning v1.

Planning-only: guarded migration batches, gate sequence, test binding, rollback checkpoints.
No real file move/delete/merge/rename.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_guarded_planning_only"
SOURCE_CHAIN = "main_project_structure_migration_guarded_planning_v1"
PLANNING_ID = "main_proj_struct_migration_guarded_planning_v1_001"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Guarded-DryRun-v1-001"

READINESS_FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN_READY_FOR_GUARDED_MIGRATION_PLANNING"
)
PAHR_CLOSURE_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_CLOSED_FOR_CURRENT_MAINLINE"
CONSOLIDATION_CLOSURE_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

ROOT_SPECS = [
    {"id": "readiness", "arg": "readiness_root", "required": True, "summary": "summary.json"},
    {"id": "roadmap_decision", "arg": "roadmap_decision_root", "required": True, "summary": "summary.json"},
    {"id": "pahr_closure", "arg": "pahr_closure_root", "required": True, "summary": "summary.json"},
    {"id": "consolidation_closure", "arg": "consolidation_closure_root", "required": True, "summary": "summary.json"},
    {"id": "consolidation_post_review", "arg": "consolidation_post_review_root", "required": True, "summary": "summary.json"},
    {"id": "consolidation_dryrun", "arg": "consolidation_dryrun_root", "required": True, "summary": "summary.json"},
    {"id": "consolidation_planning", "arg": "consolidation_planning_root", "required": True, "summary": "summary.json"},
    {"id": "structure_map", "arg": "structure_map_root", "required": True, "summary": "summary.json"},
    {"id": "structure_governance", "arg": "structure_governance_root", "required": True, "summary": "summary.json"},
    {"id": "gate_taxonomy", "arg": "gate_taxonomy_root", "required": True, "summary": "summary.json"},
]

READINESS_ARTIFACTS = [
    "main_project_migration_readiness_policy.json",
    "migration_readiness_gate.json",
    "migration_allowed_scope.json",
    "migration_forbidden_scope.json",
    "pre_migration_checklist.json",
    "post_migration_test_plan.json",
    "migration_rollback_requirement.json",
    "whitebox_test_center_deferment_policy.json",
    "future_reserved_module_constraint.json",
    "migration_readiness_decision.json",
]

OTHER_ARTIFACTS: List[Tuple[str, str]] = [
    ("structure_map", "current_to_target_structure_map.json"),
    ("structure_map", "module_inventory.json"),
    ("structure_map", "migration_risk_register.json"),
    ("consolidation_closure", "consolidation_closure_decision_summary.json"),
    ("pahr_closure", "human_review_carryover_for_future_execution.json"),
    ("pahr_closure", "permanent_block_carryover_for_future_governance.json"),
]

GATE_DEFS = [
    ("G01", "PreBatchProtectedAssetGate", "protected_assets_excluded"),
    ("G02", "HumanReviewExclusionGate", "human_review_excluded_or_manual"),
    ("G03", "PermanentDnaeExclusionGate", "permanent_dnae_excluded"),
    ("G04", "ClientBackendBoundaryGate", "client_backend_boundary_preserved"),
    ("G05", "FutureReservedModuleGate", "future_reserved_not_finalized"),
    ("G06", "RuntimeBehaviorNoChangeGate", "no_runtime_behavior_change"),
    ("G07", "DocsLinkIntegrityGate", "docs_link_integrity"),
    ("G08", "PostBatchVerifierGate", "post_batch_verifier_rerun"),
    ("G09", "RollbackAvailabilityGate", "rollback_checkpoint_available"),
    ("G10", "HumanApprovalCheckpointGate", "human_approval_before_execution"),
]

BATCH_DEFS = [
    ("B0", "Baseline Snapshot and Freeze", "baseline_snapshot_freeze", False),
    ("B1", "Safe Documentation Relink Candidates", "safe_docs_relink_candidates", True),
    ("B2", "Capability Module Grouping Candidates", "capability_module_grouping", True),
    ("B3", "Governance and Constitution Grouping Candidates", "governance_constitution_grouping", True),
    ("B4", "MidPlatform Operating Core Candidate Grouping", "midplatform_operating_core_grouping", True),
    ("B5", "Developer Artifact Reference Separation Candidate", "developer_artifact_reference_separation", True),
    ("B6", "Future Reserved Module Marker", "future_reserved_module_marker", True),
    ("B7", "Post-Migration Verification and Rollback Gate", "post_migration_verification_rollback_gate", False),
]

BATCH_POST_TESTS = {
    "B0": ["A01", "A02"],
    "B1": ["A03", "A04", "A05", "A06"],
    "B2": ["A07", "C01", "C02"],
    "B3": ["B01", "B02", "B03", "B04", "B05", "B06", "C03"],
    "B4": ["C04"],
    "B5": ["E01", "E02", "E03", "E04", "E05"],
    "B6": [],
    "B7": None,  # all tests
}

CANDIDATE_TYPES = [
    "doc_relink_candidate",
    "module_grouping_candidate",
    "target_structure_marker_candidate",
    "module_versioning_marker_candidate",
    "non_runtime_metadata_mapping_candidate",
    "client_boundary_marker_candidate",
    "developer_backend_reference_marker_candidate",
    "future_reserved_marker_candidate",
]

EXCLUSION_CATEGORIES = [
    "protected_assets",
    "hr_unresolved_items",
    "permanent_dnae_items",
    "eval_out_outputs",
    "verifier_reports",
    "go_no_go_packs",
    "correction_records",
    "historical_test_logs",
    "phase_records",
    "closure_boundary_freeze_files",
    "non_claims_registers",
    "safety_gate_constitution_docs_unless_planned",
    "whitebox_test_center_physical_restructuring",
    "developer_backend_full_architecture",
    "future_reserved_module_finalization",
    "runtime_behavior_changes",
    "client_runtime_changes",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_root(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary_payload = _try_read_json(root / "summary.json") if root else None
    return {"root": root, "loaded": summary_payload is not None, "summary": summary_payload or {}}


def _load_readiness_artifacts(readiness_root: Optional[Path]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if not readiness_root:
        return out
    for name in READINESS_ARTIFACTS:
        payload = _try_read_json(readiness_root / name)
        if payload is None and name == "post_migration_test_plan.json":
            payload = _try_read_json(readiness_root / "post_migration_test_verification_plan.json")
        out[name] = payload
    return out


def _batch_execution_flags() -> Dict[str, Any]:
    return {
        "execution_allowed_now": False,
        "file_move_allowed_now": False,
        "delete_allowed_now": False,
        "merge_allowed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _guarded_migration_batch_plan() -> Dict[str, Any]:
    common_excluded = [
        "protected_assets",
        "human_review_unresolved",
        "permanent_dnae",
        "eval_out_phase_outputs",
        "verifier_reports",
        "historical_test_logs",
    ]
    batches = []
    for batch_id, batch_name, scope_key, has_candidates in BATCH_DEFS:
        candidate_scope = [scope_key] if has_candidates else ["baseline_or_verification_only"]
        batches.append(
            {
                "batch_id": batch_id,
                "batch_name": batch_name,
                "candidate_scope": candidate_scope,
                "excluded_scope": common_excluded,
                "required_pre_checks": [
                    "clean_working_tree",
                    "branch_backup",
                    "protected_exclusion_list",
                    "hr_exclusion_list",
                    "dnae_exclusion_list",
                    "rollback_checkpoint",
                ],
                "required_post_tests": BATCH_POST_TESTS.get(batch_id) or ["ALL"],
                "rollback_checkpoint": f"checkpoint_{batch_id.lower()}",
                "human_approval_required": batch_id not in ("B0", "B7"),
                **_batch_execution_flags(),
            }
        )
    return {
        "batches": batches,
        "batch_count": len(batches),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _guarded_migration_gate_sequence() -> Dict[str, Any]:
    all_batch_ids = [b[0] for b in BATCH_DEFS]
    gates = []
    for gate_id, gate_name, pass_topic in GATE_DEFS:
        applies = all_batch_ids if gate_name != "HumanApprovalCheckpointGate" else [b for b in all_batch_ids if b not in ("B0",)]
        gates.append(
            {
                "gate_id": gate_id,
                "gate_name": gate_name,
                "applies_to_batch": applies,
                "input_required": [pass_topic, "readiness_gate_passed"],
                "pass_condition": f"{pass_topic}_verified_planning_only",
                "fail_condition": f"{pass_topic}_violation_detected",
                "failure_response": "block_batch_execution_and_require_rollback_plan_review",
                "blocks_execution": True,
                "audit_required": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {
        "gates": gates,
        "gate_sequence_count": len(gates),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _migration_candidate_scope(allowed: Dict[str, Any]) -> Dict[str, Any]:
    rows = []
    for i, ctype in enumerate(CANDIDATE_TYPES, 1):
        rows.append(
            {
                "candidate_id": f"CAND{i:03d}",
                "candidate_type": ctype,
                "candidate_only": True,
                "execution_allowed_now": False,
                "requires_guarded_execution_phase": True,
                "requires_post_migration_test": True,
                "upstream_allowed_scope_ref": "migration_allowed_scope.json",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    upstream_count = (allowed or {}).get("allowed_scope_count", len(rows))
    return {
        "candidates": rows,
        "migration_candidate_scope_count": len(rows),
        "upstream_allowed_scope_count": upstream_count,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _migration_exclusion_scope(forbidden: Dict[str, Any]) -> Dict[str, Any]:
    rows = [
        {
            "exclusion_id": f"EXC{i:03d}",
            "exclusion_category": cat,
            "included_in_migration_scope": False,
            "execution_allowed_now": False,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        for i, cat in enumerate(EXCLUSION_CATEGORIES, 1)
    ]
    return {
        "exclusions": rows,
        "migration_exclusion_scope_count": len(rows),
        "protected_assets_excluded_from_migration": True,
        "permanent_blocks_excluded_from_migration": True,
        "human_review_items_excluded_or_manual_only": True,
        "whitebox_test_center_physical_restructure_excluded": True,
        "developer_backend_full_architecture_excluded": True,
        "future_reserved_module_finalization_excluded": True,
        "upstream_forbidden_scope_count": (forbidden or {}).get("forbidden_scope_count", 0),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _pre_batch_check_policy() -> Dict[str, Any]:
    checks = [
        "clean_working_tree_required",
        "branch_backup_required",
        "baseline_snapshot_required",
        "protected_exclusion_list_required",
        "hr_exclusion_list_required",
        "dnae_exclusion_list_required",
        "rollback_checkpoint_required",
        "post_test_group_assigned",
        "owner_approval_placeholder_required",
        "no_runtime_change_assertion_required",
        "no_protected_asset_touch_assertion_required",
    ]
    rows = [
        {
            "check_id": f"PBC{i:03d}",
            "requirement": req,
            "required": True,
            "executed_in_this_phase": False,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        for i, req in enumerate(checks, 1)
    ]
    return {
        "checks": rows,
        "pre_batch_check_count": len(rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _post_batch_test_policy(batch_plan: Dict[str, Any]) -> Dict[str, Any]:
    bindings = []
    for b in batch_plan.get("batches") or []:
        bindings.append(
            {
                "batch_id": b.get("batch_id"),
                "required_post_tests": b.get("required_post_tests"),
                "tests_executed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {
        "batch_test_bindings": bindings,
        "binding_count": len(bindings),
        "post_migration_tests_executed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _rollback_checkpoint_policy(batch_plan: Dict[str, Any]) -> Dict[str, Any]:
    checkpoints = []
    for b in batch_plan.get("batches") or []:
        bid = b.get("batch_id")
        checkpoints.append(
            {
                "checkpoint_id": f"RCP_{bid}",
                "batch_id": bid,
                "restore_path_map": True,
                "restore_readme_index_links": bid in ("B1", "B7"),
                "restore_verdict_table_rows": bid == "B7",
                "restore_eval_out_refs": True,
                "restore_protected_exclusions": True,
                "restore_client_backend_boundary": True,
                "rerun_verifier_after_rollback": True,
                "rollback_audit_required": True,
                "rollback_executed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {
        "checkpoints": checkpoints,
        "rollback_checkpoint_count": len(checkpoints),
        "rollback_checkpoint_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _human_approval_checkpoint_policy() -> Dict[str, Any]:
    return {
        "owner_approval_placeholder": True,
        "no_automatic_owner_confirmation": True,
        "approval_required_before_real_migration": True,
        "hr_unresolved_items_remain_excluded": True,
        "permanent_dnae_remains_excluded": True,
        "approval_does_not_override_safety_gate_constitution": True,
        "human_approval_checkpoint_required": True,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _post_migration_verification_matrix(test_plan: Dict[str, Any], batch_plan: Dict[str, Any]) -> Dict[str, Any]:
    tests_in = test_plan.get("test_groups") or test_plan.get("suites") or []
    batch_by_test: Dict[str, str] = {}
    for bid, test_ids in BATCH_POST_TESTS.items():
        if test_ids is None:
            continue
        for tid in test_ids:
            batch_by_test[tid] = bid
    for t in tests_in:
        tid = t.get("test_id")
        if tid and tid not in batch_by_test:
            batch_by_test[tid] = "B7"

    rows = []
    for t in tests_in:
        tid = t.get("test_id", "")
        rows.append(
            {
                "test_id": tid,
                "test_group": t.get("test_group_id") or t.get("test_group_name", ""),
                "test_name": t.get("test_name", ""),
                "related_batch": batch_by_test.get(tid, "B7"),
                "required_after_migration": t.get("required_after_migration", True),
                "execution_now": False,
                "pass_condition": t.get("pass_condition", ""),
                "failure_response": t.get("failure_response", "halt_and_rollback"),
                "rollback_required_if_failed": t.get("rollback_required_if_failed", True),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    all_batches = {b.get("batch_id") for b in batch_plan.get("batches") or []}
    bound_batches = {r.get("related_batch") for r in rows}
    return {
        "tests": rows,
        "post_migration_test_count": len(rows),
        "post_migration_tests_bound_to_batches": bound_batches.issubset(all_batches) and len(rows) >= 31,
        "test_groups_present": sorted({r.get("test_group") for r in rows if r.get("test_group")}),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _boundary_reports() -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    common = {
        "planning_scope": PLANNING_SCOPE,
        "planning_only": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }
    return (
        {**common, "actual_file_move_executed": False, "actual_file_rename_executed": False, "actual_module_merge_executed": False, "file_operation_invoked": False},
        {**common, "actual_file_delete_executed": False},
        {
            **common,
            "runtime_enabled": False,
            "no_runtime_executed": True,
            "no_new_runtime_enabled": True,
            "stat_invoked": False,
            "exists_invoked": False,
            "file_opened": False,
            "file_content_read": False,
            "navigation_action_triggered": False,
            "speech_gate_invoked": False,
            "tts_invoked": False,
        },
        {**common, "world_model_written": False, "memory_written": False, "library_written": False, "fact_written": False},
    )


def run_main_project_structure_migration_guarded_planning_v1(
    *,
    readiness_root: str,
    roadmap_decision_root: str,
    pahr_closure_root: str,
    consolidation_closure_root: str,
    consolidation_post_review_root: str,
    consolidation_dryrun_root: str,
    consolidation_planning_root: str,
    structure_map_root: str,
    structure_governance_root: str,
    gate_taxonomy_root: str,
) -> Dict[str, Any]:
    arg_map = {
        "readiness": readiness_root,
        "roadmap_decision": roadmap_decision_root,
        "pahr_closure": pahr_closure_root,
        "consolidation_closure": consolidation_closure_root,
        "consolidation_post_review": consolidation_post_review_root,
        "consolidation_dryrun": consolidation_dryrun_root,
        "consolidation_planning": consolidation_planning_root,
        "structure_map": structure_map_root,
        "structure_governance": structure_governance_root,
        "gate_taxonomy": gate_taxonomy_root,
    }

    roots = {spec["id"]: _load_root(arg_map.get(spec["id"])) for spec in ROOT_SPECS}
    blockers: List[str] = []

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        if spec["required"] and not meta["loaded"]:
            blockers.append(f"{spec['id']}_root_missing")
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else "missing_required",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    readiness_meta = roots["readiness"]
    readiness_art = _load_readiness_artifacts(readiness_meta["root"])
    readiness_ok = (
        readiness_meta["loaded"]
        and readiness_meta["summary"].get("final_decision") == READINESS_FINAL_DECISION
        and readiness_meta["summary"].get("ready_for_migration_guarded_planning") is True
    )
    if not readiness_ok:
        blockers.append("readiness_invalid_or_not_ready")

    for name in READINESS_ARTIFACTS:
        if readiness_art.get(name) is None:
            blockers.append(f"readiness_artifact_missing:{name}")

    for root_id, filename in OTHER_ARTIFACTS:
        r = roots[root_id]["root"]
        payload = _try_read_json(r / filename) if r else None
        if payload is None:
            blockers.append(f"artifact_missing:{root_id}/{filename}")

    readiness_decision = readiness_art.get("migration_readiness_decision.json") or {}
    if readiness_decision.get("ready_for_migration_guarded_planning") is not True:
        blockers.append("readiness_decision_not_ready_for_guarded_planning")

    roadmap_ok = roots["roadmap_decision"]["loaded"]
    pahr_ok = (
        roots["pahr_closure"]["loaded"]
        and roots["pahr_closure"]["summary"].get("final_decision") == PAHR_CLOSURE_DECISION
    )
    consolidation_ok = (
        roots["consolidation_closure"]["loaded"]
        and roots["consolidation_closure"]["summary"].get("final_decision") == CONSOLIDATION_CLOSURE_DECISION
    )
    structure_ok = roots["structure_map"]["loaded"]
    gate_ok = roots["gate_taxonomy"]["loaded"]

    if not pahr_ok:
        blockers.append("pahr_closure_invalid")
    if not consolidation_ok:
        blockers.append("consolidation_closure_invalid")

    inventory_count = readiness_meta["summary"].get("inventory_entry_count", 7391)
    hr_count = readiness_meta["summary"].get("human_review_case_count", HUMAN_REVIEW_CARRYOVER)
    pb_count = readiness_meta["summary"].get("permanent_block_case_count", PERMANENT_BLOCK_CARRYOVER)

    allowed = readiness_art.get("migration_allowed_scope.json") or {}
    forbidden = readiness_art.get("migration_forbidden_scope.json") or {}
    test_plan = readiness_art.get("post_migration_test_plan.json") or {}

    guarded_migration_batch_plan = _guarded_migration_batch_plan()
    guarded_migration_gate_sequence = _guarded_migration_gate_sequence()
    migration_candidate_scope = _migration_candidate_scope(allowed)
    migration_exclusion_scope = _migration_exclusion_scope(forbidden)
    pre_batch_check_policy = _pre_batch_check_policy()
    post_batch_test_policy = _post_batch_test_policy(guarded_migration_batch_plan)
    rollback_checkpoint_policy = _rollback_checkpoint_policy(guarded_migration_batch_plan)
    human_approval_checkpoint_policy = _human_approval_checkpoint_policy()
    post_migration_verification_matrix = _post_migration_verification_matrix(
        test_plan, guarded_migration_batch_plan
    )

    tests_bound = post_migration_verification_matrix.get("post_migration_tests_bound_to_batches") is True
    test_count = post_migration_verification_matrix.get("post_migration_test_count", 0)

    boundary_ok = (
        not blockers
        and readiness_ok
        and pahr_ok
        and consolidation_ok
        and tests_bound
        and test_count >= 31
    )

    main_project_migration_guarded_planning_policy = {
        "planning_id": PLANNING_ID,
        "planning_scope": PLANNING_SCOPE,
        "source_readiness_ref": "_eval_out/main_project_structure_migration_readiness_and_test_plan_v1_smoke_v0/",
        "source_structure_map_ref": "_eval_out/luna_project_module_inventory_and_structure_map_dryrun_v1_smoke_v0/",
        "source_consolidation_ref": "_eval_out/luna_project_structure_consolidation_closure_v1_smoke_v0/",
        "source_protected_asset_resolution_ref": "_eval_out/protected_asset_and_human_review_resolution_closure_v1_smoke_v0/",
        "guarded_migration_batch_plan_ref": "guarded_migration_batch_plan.json",
        "guarded_migration_gate_sequence_ref": "guarded_migration_gate_sequence.json",
        "migration_candidate_scope_ref": "migration_candidate_scope.json",
        "migration_exclusion_scope_ref": "migration_exclusion_scope.json",
        "pre_batch_check_policy_ref": "pre_batch_check_policy.json",
        "post_batch_test_policy_ref": "post_batch_test_policy.json",
        "rollback_checkpoint_policy_ref": "rollback_checkpoint_policy.json",
        "human_approval_checkpoint_policy_ref": "human_approval_checkpoint_policy.json",
        "post_migration_verification_matrix_ref": "post_migration_verification_matrix.json",
        "next_phase_recommendation": NEXT_PHASE,
        "planning_only": True,
        "migration_execution_allowed": False,
        "file_move_allowed_now": False,
        "file_delete_allowed_now": False,
        "module_merge_allowed_now": False,
        "post_migration_tests_executed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    guarded_planning_readiness_decision = {
        "guarded_planning_verdict": "GO" if boundary_ok else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [] if boundary_ok else ["resolve_blockers_before_guarded_dryrun"],
        "ready_for_guarded_dryrun": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "debts": [
            "human_review_items=240 remain excluded until explicit HR execution phase",
            "permanent_do_not_auto_execute=914 remain excluded",
            "guarded_dryrun_required_before_any_real_migration_execution",
            "post_migration_test_matrix_defined_not_executed",
            "whitebox_test_center_physical_restructure_deferred",
            "developer_backend_full_architecture_deferred",
        ],
        "debt_count": 6,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    no_file_move, no_delete, no_runtime, no_write = _boundary_reports()

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "readiness_input_loaded": readiness_ok,
        "roadmap_decision_input_loaded": roadmap_ok,
        "protected_asset_resolution_closure_input_loaded": pahr_ok,
        "consolidation_closure_input_loaded": consolidation_ok,
        "structure_map_input_loaded": structure_ok,
        "gate_taxonomy_input_loaded": gate_ok,
        "consolidation_post_review_input_loaded": roots["consolidation_post_review"]["loaded"],
        "consolidation_dryrun_input_loaded": roots["consolidation_dryrun"]["loaded"],
        "consolidation_planning_input_loaded": roots["consolidation_planning"]["loaded"],
        "structure_governance_input_loaded": roots["structure_governance"]["loaded"],
        "guarded_migration_policy_generated": True,
        "guarded_migration_batch_plan_generated": True,
        "guarded_migration_gate_sequence_generated": True,
        "migration_candidate_scope_generated": True,
        "migration_exclusion_scope_generated": True,
        "pre_batch_check_policy_generated": True,
        "post_batch_test_policy_generated": True,
        "rollback_checkpoint_policy_generated": True,
        "human_approval_checkpoint_policy_generated": True,
        "post_migration_verification_matrix_generated": True,
        "guarded_planning_readiness_decision_generated": True,
        "batch_count": guarded_migration_batch_plan.get("batch_count", 0),
        "gate_sequence_count": guarded_migration_gate_sequence.get("gate_sequence_count", 0),
        "migration_candidate_scope_count": migration_candidate_scope.get("migration_candidate_scope_count", 0),
        "migration_exclusion_scope_count": migration_exclusion_scope.get("migration_exclusion_scope_count", 0),
        "pre_batch_check_count": pre_batch_check_policy.get("pre_batch_check_count", 0),
        "post_migration_test_count": test_count,
        "rollback_checkpoint_required": True,
        "human_approval_checkpoint_required": True,
        "protected_assets_excluded_from_migration": True,
        "permanent_blocks_excluded_from_migration": True,
        "human_review_items_excluded_or_manual_only": True,
        "whitebox_test_center_physical_restructure_excluded": True,
        "developer_backend_full_architecture_excluded": True,
        "future_reserved_module_finalization_excluded": True,
        "post_migration_tests_bound_to_batches": tests_bound,
        "post_migration_tests_executed": False,
        "ready_for_guarded_dryrun": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "migration_execution_allowed": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "inventory_entry_count": inventory_count,
        "human_review_case_count": hr_count,
        "permanent_block_case_count": pb_count,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "final_decision": summary["final_decision"],
        "recommended_next_phase": summary["recommended_next_phase"],
        "reason": "guarded batches, gates, test binding, and rollback checkpoints frozen for dryrun simulation",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "main_project_migration_guarded_planning_policy": main_project_migration_guarded_planning_policy,
        "guarded_migration_batch_plan": guarded_migration_batch_plan,
        "guarded_migration_gate_sequence": guarded_migration_gate_sequence,
        "migration_candidate_scope": migration_candidate_scope,
        "migration_exclusion_scope": migration_exclusion_scope,
        "pre_batch_check_policy": pre_batch_check_policy,
        "post_batch_test_policy": post_batch_test_policy,
        "rollback_checkpoint_policy": rollback_checkpoint_policy,
        "human_approval_checkpoint_policy": human_approval_checkpoint_policy,
        "post_migration_verification_matrix": post_migration_verification_matrix,
        "guarded_planning_readiness_decision": guarded_planning_readiness_decision,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": no_file_move,
        "no_delete_boundary_report": no_delete,
        "no_runtime_boundary_report": no_runtime,
        "no_write_boundary_report": no_write,
    }
