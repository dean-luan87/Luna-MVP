# -*- coding: utf-8 -*-
"""Main Project Structure Migration Readiness and Test Plan v1.

Planning-only: readiness gate, pre-migration checks, post-migration test plan,
rollback requirements, allowed/forbidden scope — no real migration or file ops.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_readiness_and_test_plan_only"
SOURCE_CHAIN = "main_project_structure_migration_readiness_and_test_plan_v1"
PLANNING_ID = "main_proj_struct_migration_readiness_test_plan_v1_001"

FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN_READY_FOR_GUARDED_MIGRATION_PLANNING"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001"

POST_PAHR_ROADMAP_DECISION = (
    "POST_PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_ROADMAP_DECISION_READY_FOR_MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN"
)
PAHR_CLOSURE_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_CLOSED_FOR_CURRENT_MAINLINE"
CONSOLIDATION_CLOSURE_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914
WHITEBOX_DEFER_REASON = "requires_post_migration_test_and_design_discussion"

FUTURE_RESERVED_MODULES = [
    "WorldModel",
    "Memory Center",
    "Library",
    "Emotion Engine",
    "Emotion Map",
    "Exploration Drive",
    "Survival Drive",
    "Social Skill System",
    "Relationship Model",
    "Normative / Social Reasoning",
    "Offline Distributed MidPlatform",
    "Electronic Lifeform Architecture",
    "Self-Directed Capability Evolution",
    "Autopoietic Capability Formation",
]

ROOT_SPECS = [
    {"id": "roadmap_decision", "arg": "roadmap_decision_root", "required": True, "summary": "summary.json"},
    {"id": "pahr_closure", "arg": "pahr_closure_root", "required": True, "summary": "summary.json"},
    {"id": "pahr_post_review", "arg": "pahr_post_review_root", "required": True, "summary": "summary.json"},
    {"id": "pahr_dryrun", "arg": "pahr_dryrun_root", "required": True, "summary": "summary.json"},
    {"id": "pahr_planning", "arg": "pahr_planning_root", "required": True, "summary": "summary.json"},
    {"id": "consolidation_roadmap", "arg": "consolidation_roadmap_root", "required": True, "summary": "summary.json"},
    {"id": "consolidation_closure", "arg": "consolidation_closure_root", "required": True, "summary": "summary.json"},
    {"id": "consolidation_post_review", "arg": "consolidation_post_review_root", "required": True, "summary": "summary.json"},
    {"id": "consolidation_dryrun", "arg": "consolidation_dryrun_root", "required": True, "summary": "summary.json"},
    {"id": "consolidation_planning", "arg": "consolidation_planning_root", "required": True, "summary": "summary.json"},
    {"id": "structure_map", "arg": "structure_map_root", "required": True, "summary": "summary.json"},
    {"id": "structure_governance", "arg": "structure_governance_root", "required": True, "summary": "summary.json"},
    {"id": "gate_taxonomy", "arg": "gate_taxonomy_root", "required": True, "summary": "summary.json"},
]

REQUIRED_ARTIFACTS: List[Tuple[str, str]] = [
    ("roadmap_decision", "main_project_migration_readiness_route_decision.json"),
    ("roadmap_decision", "deferred_whitebox_test_center_structure_optimization_register.json"),
    ("pahr_closure", "protected_asset_human_review_resolution_closure_summary.json"),
    ("pahr_closure", "resolution_non_claims_register.json"),
    ("pahr_closure", "human_review_carryover_for_future_execution.json"),
    ("pahr_closure", "permanent_block_carryover_for_future_governance.json"),
    ("pahr_closure", "deferred_resolution_action_pool.json"),
    ("consolidation_closure", "luna_project_structure_consolidation_closure_summary.json"),
    ("consolidation_closure", "consolidation_non_claims_register.json"),
    ("consolidation_closure", "deferred_consolidation_action_pool.json"),
    ("structure_map", "current_to_target_structure_map.json"),
    ("structure_map", "module_inventory.json"),
    ("structure_map", "developer_backend_extraction_map.json"),
    ("structure_map", "client_boundary_mapping.json"),
    ("structure_map", "migration_risk_register.json"),
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_root(path_str: Optional[str], summary_file: str = "summary.json") -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary_payload = _try_read_json(root / summary_file) if root else None
    loaded = summary_payload is not None
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}}


def _load_artifacts(roots: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for root_id, filename in REQUIRED_ARTIFACTS:
        root = roots.get(root_id, {}).get("root")
        out[f"{root_id}/{filename}"] = _try_read_json(root / filename) if root else None
    sm_root = roots.get("structure_map", {}).get("root")
    hist = _try_read_json(sm_root / "historical_test_asset_classification.json") if sm_root else None
    if hist is None and sm_root:
        hist = _try_read_json(sm_root / "migration_risk_register.json")
    out["structure_map/historical_test_asset_classification.json"] = hist
    return out


def _disposition_counts(map_payload: Dict[str, Any]) -> Dict[str, Any]:
    rows = map_payload.get("map_rows") or []
    counts = Counter(r.get("disposition_action", "unknown") for r in rows)
    return {
        "inventory_entry_count": len(rows),
        "disposition_action_counts": dict(counts),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _migration_allowed_scope() -> Dict[str, Any]:
    candidates = [
        ("MAS001", "module_directory_relink", "module directory relink candidate"),
        ("MAS002", "docs_index_relink", "docs index relink candidate"),
        ("MAS003", "capability_module_grouping", "capability module grouping candidate"),
        ("MAS004", "non_protected_docs_grouping", "non-protected docs grouping candidate"),
        ("MAS005", "non_runtime_metadata_mapping", "non-runtime metadata mapping candidate"),
        ("MAS006", "future_module_placeholder_marker", "future module placeholder marker"),
        ("MAS007", "client_boundary_marker", "client boundary marker"),
        ("MAS008", "developer_backend_reference_marker", "developer backend reference marker"),
    ]
    rows = [
        {
            "allowed_scope_id": sid,
            "scope_type": stype,
            "description": desc,
            "candidate_only": True,
            "execution_allowed_now": False,
            "requires_guarded_planning": True,
            "requires_post_migration_test": True,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        for sid, stype, desc in candidates
    ]
    return {
        "allowed_scopes": rows,
        "allowed_scope_count": len(rows),
        "candidate_only": True,
        "execution_allowed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _migration_forbidden_scope() -> Dict[str, Any]:
    items = [
        "protected_assets",
        "eval_out_phase_outputs",
        "verifier_reports",
        "go_no_go_packs",
        "correction_records",
        "historical_test_logs",
        "phase_records",
        "closure_boundary_freeze_files",
        "non_claims_registers",
        "safety_gate_constitution_docs",
        "human_review_unresolved_items",
        "permanent_dnae_items",
        "whitebox_test_center_physical_restructuring",
        "developer_backend_full_architecture",
        "future_reserved_modules_finalization",
        "runtime_code_behavior_change",
        "client_runtime_behavior_change",
        "permanent_blocks_in_migration_scope",
        "protected_assets_in_migration_scope",
    ]
    rows = [
        {
            "forbidden_scope_id": f"F{i:03d}",
            "forbidden_category": cat,
            "included_in_migration_scope": False,
            "execution_allowed_now": False,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        for i, cat in enumerate(items, start=1)
    ]
    return {
        "forbidden_scopes": rows,
        "forbidden_scope_count": len(rows),
        "protected_assets_excluded_from_migration": True,
        "permanent_blocks_excluded_from_migration": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _pre_migration_checklist() -> Dict[str, Any]:
    checks = [
        ("PMC001", "clean_working_tree_required", True),
        ("PMC002", "branch_backup_required", True),
        ("PMC003", "source_inventory_snapshot_required", True),
        ("PMC004", "target_mapping_snapshot_required", True),
        ("PMC005", "protected_asset_exclusion_list_required", True),
        ("PMC006", "human_review_exclusion_list_required", True),
        ("PMC007", "permanent_block_exclusion_list_required", True),
        ("PMC008", "rollback_plan_required", True),
        ("PMC009", "verifier_baseline_snapshot_required", True),
        ("PMC010", "post_migration_test_plan_required", True),
        ("PMC011", "readme_verdict_relink_plan_required", True),
        ("PMC012", "cross_repo_input_root_handling_plan_required", True),
        ("PMC013", "no_runtime_change_assertion_required", True),
    ]
    rows = [
        {
            "check_id": cid,
            "requirement": req,
            "required": reqd,
            "executed_in_this_phase": False,
            "planning_only_definition": True,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        for cid, req, reqd in checks
    ]
    return {
        "checks": rows,
        "pre_migration_check_count": len(rows),
        "rollback_required": True,
        "post_migration_test_plan_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _post_migration_test_plan() -> Dict[str, Any]:
    groups: List[Dict[str, Any]] = []

    def _tests(group_id: str, group_name: str, tests: List[Tuple[str, str, str]]) -> None:
        for tid, tname, pass_cond in tests:
            groups.append(
                {
                    "test_group_id": group_id,
                    "test_group_name": group_name,
                    "test_id": tid,
                    "test_name": tname,
                    "required_after_migration": True,
                    "pass_condition": pass_cond,
                    "failure_response": "halt_migration_chain_and_initiate_rollback",
                    "rollback_required_if_failed": True,
                    "execution_status": "plan_defined_not_executed",
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                }
            )

    _tests(
        "A",
        "Structural Integrity Tests",
        [
            ("A01", "import_path_check", "all_capability_imports_resolve_after_relink"),
            ("A02", "module_path_mapping_check", "structure_map_paths_match_on_disk_layout"),
            ("A03", "readme_link_check", "architecture_readme_links_resolve"),
            ("A04", "docs_link_check", "governance_evaluation_doc_links_resolve"),
            ("A05", "phase_verdict_table_consistency", "verdict_rows_reference_valid_phase_ids"),
            ("A06", "eval_out_reference_consistency", "_eval_out_smoke_roots_addressable"),
            ("A07", "capability_runner_verifier_linkage", "runner_verifier_doc_triad_aligned"),
        ],
    )
    _tests(
        "B",
        "Governance Boundary Tests",
        [
            ("B01", "protected_asset_not_moved", "protected_asset_register_unchanged"),
            ("B02", "permanent_block_not_touched", "permanent_dnae_count_unchanged"),
            ("B03", "human_review_untouched", "hr_cases_closed_no_execution_unless_manual"),
            ("B04", "non_claims_preserved", "closure_non_claims_registers_intact"),
            ("B05", "closure_boundary_preserved", "boundary_freeze_artifacts_intact"),
            ("B06", "client_backend_boundary_preserved", "client_boundary_mapping_holds"),
        ],
    )
    _tests(
        "C",
        "Functional Smoke Tests",
        [
            ("C01", "gate_taxonomy_verifier_rerun", "verify_gate_taxonomy_planning_v1_passed"),
            ("C02", "structure_inventory_verifier_rerun", "verify_structure_map_dryrun_v1_passed"),
            ("C03", "consolidation_closure_verifier_rerun", "verify_consolidation_closure_v1_passed"),
            ("C04", "pahr_closure_verifier_rerun", "verify_pahr_closure_v1_passed"),
            ("C05", "minimal_runtime_integration_closure_rerun", "if_available_minimal_runtime_closure_GO"),
            ("C06", "ocr_mainline_closure_rerun", "if_available_ocr_closure_GO"),
            ("C07", "basic_navigation_closure_rerun", "if_available_navigation_closure_GO"),
        ],
    )
    _tests(
        "D",
        "No Runtime Regression Tests",
        [
            ("D01", "no_camera_invoked", "no_camera_runtime_in_migration_window"),
            ("D02", "no_ocr_provider_invoked", "no_ocr_provider_in_migration_window"),
            ("D03", "no_map_api_invoked", "no_map_api_in_migration_window"),
            ("D04", "no_tracking_runtime", "no_tracking_runtime_in_migration_window"),
            ("D05", "no_speech_tts", "no_speech_gate_tts_in_migration_window"),
            ("D06", "no_worldmodel_memory_fact_write", "no_wm_memory_fact_library_write"),
        ],
    )
    _tests(
        "E",
        "Developer Tooling Non-Execution Tests",
        [
            ("E01", "whitebox_not_restructured", "whitebox_paths_unchanged_until_alignment_phase"),
            ("E02", "test_center_not_restructured", "test_center_paths_unchanged_until_alignment_phase"),
            ("E03", "verifier_outputs_preserved", "verifier_report_paths_retained"),
            ("E04", "logs_preserved", "historical_test_logs_retained"),
            ("E05", "go_no_go_packs_preserved", "go_no_go_pack_docs_retained"),
        ],
    )

    group_ids = sorted({g["test_group_id"] for g in groups})
    return {
        "test_plan_id": "main_project_post_migration_test_v1",
        "planning_only": True,
        "tests_executed": False,
        "tests_passed": None,
        "test_groups": groups,
        "post_migration_test_group_count": len(group_ids),
        "post_migration_test_required": True,
        "test_after_main_project_migration_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _migration_rollback_requirement() -> Dict[str, Any]:
    return {
        "rollback_plan_id": "main_project_migration_rollback_v1",
        "rollback_batch_granularity": "per_guarded_planning_batch",
        "requirements": [
            {"requirement_id": "RB01", "topic": "restore_file_path", "required": True},
            {"requirement_id": "RB02", "topic": "restore_readme_links", "required": True},
            {"requirement_id": "RB03", "topic": "restore_verdict_table_rows", "required": True},
            {"requirement_id": "RB04", "topic": "restore_eval_out_references", "required": True},
            {"requirement_id": "RB05", "topic": "restore_module_mapping", "required": True},
            {"requirement_id": "RB06", "topic": "restore_client_backend_boundary", "required": True},
            {"requirement_id": "RB07", "topic": "restore_protected_asset_exclusions", "required": True},
            {"requirement_id": "RB08", "topic": "restore_test_logs", "required": True},
            {"requirement_id": "RB09", "topic": "rerun_verifier_after_rollback", "required": True},
            {"requirement_id": "RB10", "topic": "audit_rollback_record", "required": True},
        ],
        "rollback_required": True,
        "rollback_executed_in_this_phase": False,
        "audit_committed_in_this_phase": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _whitebox_test_center_deferment_policy(roadmap_summary: Dict[str, Any], whitebox_reg: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "whitebox_test_center_structure_optimization_deferred": True,
        "reason": whitebox_reg.get("defer_reason")
        or roadmap_summary.get("whitebox_test_center_structure_optimization_defer_reason")
        or WHITEBOX_DEFER_REASON,
        "whitebox_test_center_must_align_with_main_project_structure": roadmap_summary.get(
            "whitebox_test_center_must_align_with_main_project_structure", True
        ),
        "whitebox_structure_not_finalized_now": True,
        "test_center_structure_not_finalized_now": True,
        "developer_backend_overall_structure_deferred": roadmap_summary.get(
            "developer_backend_overall_structure_deferred", True
        ),
        "backend_architecture_not_finalized_now": True,
        "only_whitebox_and_test_center_allowed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _future_reserved_module_constraint() -> Dict[str, Any]:
    modules = [
        {
            "module_name": name,
            "future_reserved_module": True,
            "discussion_required": True,
            "implementation_status": "incomplete_or_not_started",
            "runtime_allowed_now": False,
            "write_allowed_now": False,
            "forced_structure_finalization_allowed": False,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        for name in FUTURE_RESERVED_MODULES
    ]
    return {
        "modules": modules,
        "future_reserved_module_count": len(modules),
        "forced_future_module_finalization_allowed": False,
        "worldmodel_future_reserved": True,
        "memory_center_future_reserved": True,
        "library_future_reserved": True,
        "emotion_engine_future_reserved": True,
        "exploration_drive_future_reserved": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _migration_readiness_gate(
    *,
    roots_loaded: Dict[str, bool],
    artifacts_ok: bool,
    hr_count: int,
    pb_count: int,
    inventory_count: int,
    forbidden: Dict[str, Any],
) -> Dict[str, Any]:
    go_conditions = {
        "consolidation_closure_loaded": roots_loaded.get("consolidation_closure", False),
        "protected_asset_resolution_closure_loaded": roots_loaded.get("pahr_closure", False),
        "human_review_carryover_loaded": hr_count == HUMAN_REVIEW_CARRYOVER,
        "permanent_block_carryover_loaded": pb_count == PERMANENT_BLOCK_CARRYOVER,
        "module_inventory_loaded": inventory_count >= 50,
        "target_structure_map_loaded": roots_loaded.get("structure_map", False),
        "protected_assets_not_in_migration_scope": forbidden.get("protected_assets_excluded_from_migration"),
        "permanent_blocks_excluded": forbidden.get("permanent_blocks_excluded_from_migration"),
        "human_review_items_excluded_or_marked_manual": True,
        "rollback_plan_required": True,
        "post_migration_test_plan_required": True,
        "whitebox_test_center_deferred": True,
        "developer_backend_overall_deferred": True,
        "roadmap_decision_loaded": roots_loaded.get("roadmap_decision", False),
        "gate_taxonomy_loaded": roots_loaded.get("gate_taxonomy", False),
        "required_artifacts_loaded": artifacts_ok,
    }
    nogo_triggers = [
        "protected_asset_included_in_migration_scope",
        "permanent_block_included_in_migration_scope",
        "human_review_included_without_manual_decision",
        "missing_rollback_plan",
        "missing_post_migration_test_plan",
        "move_delete_verifier_go_no_go_test_logs",
        "restructure_whitebox_test_center_before_main_migration",
        "finalize_developer_backend_architecture",
        "finalize_future_reserved_modules",
    ]
    all_go = all(go_conditions.values())
    return {
        "go_conditions": go_conditions,
        "go_condition_count": len(go_conditions),
        "all_go_conditions_met": all_go,
        "nogo_triggers": [{"trigger_id": f"NG{i:02d}", "trigger": t} for i, t in enumerate(nogo_triggers, 1)],
        "nogo_trigger_count": len(nogo_triggers),
        "readiness_verdict": "GO" if all_go else "NO_GO",
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
    no_file_move = {
        **common,
        "actual_file_move_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "file_operation_invoked": False,
    }
    no_delete = {**common, "actual_file_delete_executed": False}
    no_runtime = {
        **common,
        "runtime_enabled": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "stat_invoked": False,
        "exists_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "navigation_action_triggered": False,
        "speech_gate_invoked": False,
        "tts_invoked": False,
    }
    no_write = {
        **common,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
    }
    return no_file_move, no_delete, no_runtime, no_write


def run_main_project_structure_migration_readiness_and_test_plan_v1(
    *,
    roadmap_decision_root: str,
    pahr_closure_root: str,
    pahr_post_review_root: str,
    pahr_dryrun_root: str,
    pahr_planning_root: str,
    consolidation_roadmap_root: str,
    consolidation_closure_root: str,
    consolidation_post_review_root: str,
    consolidation_dryrun_root: str,
    consolidation_planning_root: str,
    structure_map_root: str,
    structure_governance_root: str,
    gate_taxonomy_root: str,
) -> Dict[str, Any]:
    arg_map = {
        "roadmap_decision": roadmap_decision_root,
        "pahr_closure": pahr_closure_root,
        "pahr_post_review": pahr_post_review_root,
        "pahr_dryrun": pahr_dryrun_root,
        "pahr_planning": pahr_planning_root,
        "consolidation_roadmap": consolidation_roadmap_root,
        "consolidation_closure": consolidation_closure_root,
        "consolidation_post_review": consolidation_post_review_root,
        "consolidation_dryrun": consolidation_dryrun_root,
        "consolidation_planning": consolidation_planning_root,
        "structure_map": structure_map_root,
        "structure_governance": structure_governance_root,
        "gate_taxonomy": gate_taxonomy_root,
    }

    roots: Dict[str, Dict[str, Any]] = {
        spec["id"]: _load_root(arg_map.get(spec["id"])) for spec in ROOT_SPECS
    }

    input_rows = []
    blockers: List[str] = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        ok_loaded = meta["loaded"]
        if spec["required"] and not ok_loaded:
            blockers.append(f"{spec['id']}_root_missing")
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": ok_loaded,
                "required": spec["required"],
                "status": "loaded" if ok_loaded else "missing_required",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    artifacts = _load_artifacts(roots)
    artifacts_ok = all(
        artifacts.get(f"{root_id}/{filename}") is not None for root_id, filename in REQUIRED_ARTIFACTS
    )
    if not artifacts_ok:
        blockers.append("required_artifact_missing")

    roadmap_summary = roots["roadmap_decision"]["summary"]
    roadmap_ok = (
        roots["roadmap_decision"]["loaded"]
        and roadmap_summary.get("final_decision") == POST_PAHR_ROADMAP_DECISION
        and roadmap_summary.get("main_project_migration_readiness_selected") is True
    )
    if not roadmap_ok:
        blockers.append("roadmap_decision_invalid")

    pahr_ok = (
        roots["pahr_closure"]["loaded"]
        and roots["pahr_closure"]["summary"].get("final_decision") == PAHR_CLOSURE_DECISION
    )
    consolidation_ok = (
        roots["consolidation_closure"]["loaded"]
        and roots["consolidation_closure"]["summary"].get("final_decision") == CONSOLIDATION_CLOSURE_DECISION
    )
    if not pahr_ok:
        blockers.append("pahr_closure_invalid")
    if not consolidation_ok:
        blockers.append("consolidation_closure_invalid")

    pahr_closure_art = artifacts.get("pahr_closure/protected_asset_human_review_resolution_closure_summary.json") or {}
    hr_carry = artifacts.get("pahr_closure/human_review_carryover_for_future_execution.json") or {}
    pb_carry = artifacts.get("pahr_closure/permanent_block_carryover_for_future_governance.json") or {}
    hr_count = int(
        hr_carry.get("case_count")
        or pahr_closure_art.get("human_review_case_count")
        or roots["pahr_closure"]["summary"].get("human_review_case_count")
        or HUMAN_REVIEW_CARRYOVER
    )
    pb_count = int(
        pb_carry.get("case_count")
        or pahr_closure_art.get("permanent_dnae_case_count")
        or roots["pahr_closure"]["summary"].get("permanent_dnae_case_count")
        or PERMANENT_BLOCK_CARRYOVER
    )

    map_payload = artifacts.get("structure_map/current_to_target_structure_map.json") or {}
    inventory = artifacts.get("structure_map/module_inventory.json") or {}
    disposition = _disposition_counts(map_payload)
    inventory_count = disposition.get("inventory_entry_count") or inventory.get("entry_count", 0)

    whitebox_reg = (
        artifacts.get("roadmap_decision/deferred_whitebox_test_center_structure_optimization_register.json") or {}
    )

    migration_allowed_scope = _migration_allowed_scope()
    migration_forbidden_scope = _migration_forbidden_scope()
    pre_migration_checklist = _pre_migration_checklist()
    post_migration_test_plan = _post_migration_test_plan()
    migration_rollback_requirement = _migration_rollback_requirement()
    whitebox_test_center_deferment_policy = _whitebox_test_center_deferment_policy(roadmap_summary, whitebox_reg)
    future_reserved_module_constraint = _future_reserved_module_constraint()

    roots_loaded = {spec["id"]: roots[spec["id"]]["loaded"] for spec in ROOT_SPECS}
    migration_readiness_gate = _migration_readiness_gate(
        roots_loaded=roots_loaded,
        artifacts_ok=artifacts_ok,
        hr_count=hr_count,
        pb_count=pb_count,
        inventory_count=inventory_count,
        forbidden=migration_forbidden_scope,
    )

    gate_go = migration_readiness_gate.get("all_go_conditions_met") is True
    boundary_ok = not blockers and gate_go

    main_project_migration_readiness_policy = {
        "planning_id": PLANNING_ID,
        "planning_scope": PLANNING_SCOPE,
        "source_roadmap_ref": "_eval_out/post_protected_asset_and_human_review_resolution_roadmap_decision_v1_smoke_v0/",
        "source_consolidation_closure_ref": "_eval_out/luna_project_structure_consolidation_closure_v1_smoke_v0/",
        "source_protected_asset_resolution_ref": "_eval_out/protected_asset_and_human_review_resolution_closure_v1_smoke_v0/",
        "migration_readiness_gate_ref": "migration_readiness_gate.json",
        "migration_allowed_scope_ref": "migration_allowed_scope.json",
        "migration_forbidden_scope_ref": "migration_forbidden_scope.json",
        "pre_migration_checklist_ref": "pre_migration_checklist.json",
        "post_migration_test_plan_ref": "post_migration_test_plan.json",
        "rollback_requirement_ref": "migration_rollback_requirement.json",
        "protected_asset_constraint_ref": "migration_forbidden_scope.json#protected_assets",
        "whitebox_test_center_deferment_ref": "whitebox_test_center_deferment_policy.json",
        "future_module_reserved_constraint_ref": "future_reserved_module_constraint.json",
        "next_phase_recommendation": NEXT_PHASE,
        "planning_only": True,
        "migration_execution_allowed": False,
        "file_move_allowed_now": False,
        "file_delete_allowed_now": False,
        "module_merge_allowed_now": False,
        "post_migration_test_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "debts": [
            "human_review_items=240 unresolved for real execution",
            "permanent_do_not_auto_execute=914 preserved",
            "guarded_migration_planning_required_before_any_real_move",
            "post_migration_test_required_before_whitebox_test_center_design",
            "developer_backend_overall_architecture_deferred_by_user",
            "future_reserved_modules_discussion_only",
        ],
        "debt_count": 6,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    migration_readiness_decision = {
        "readiness_verdict": "GO" if boundary_ok else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [] if boundary_ok else ["fix_input_or_artifact_blockers_before_guarded_planning"],
        "ready_for_migration_guarded_planning": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    no_file_move, no_delete, no_runtime, no_write = _boundary_reports()

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "roadmap_decision_input_loaded": roadmap_ok,
        "protected_asset_resolution_closure_input_loaded": pahr_ok,
        "consolidation_closure_input_loaded": consolidation_ok,
        "structure_map_input_loaded": roots["structure_map"]["loaded"],
        "gate_taxonomy_input_loaded": roots["gate_taxonomy"]["loaded"],
        "pahr_post_review_input_loaded": roots["pahr_post_review"]["loaded"],
        "pahr_dryrun_input_loaded": roots["pahr_dryrun"]["loaded"],
        "pahr_planning_input_loaded": roots["pahr_planning"]["loaded"],
        "consolidation_roadmap_input_loaded": roots["consolidation_roadmap"]["loaded"],
        "consolidation_post_review_input_loaded": roots["consolidation_post_review"]["loaded"],
        "consolidation_dryrun_input_loaded": roots["consolidation_dryrun"]["loaded"],
        "consolidation_planning_input_loaded": roots["consolidation_planning"]["loaded"],
        "structure_governance_input_loaded": roots["structure_governance"]["loaded"],
        "main_project_migration_readiness_policy_generated": True,
        "migration_readiness_gate_generated": True,
        "migration_allowed_scope_generated": True,
        "migration_forbidden_scope_generated": True,
        "pre_migration_checklist_generated": True,
        "post_migration_test_plan_generated": True,
        "migration_rollback_requirement_generated": True,
        "whitebox_test_center_deferment_policy_generated": True,
        "future_reserved_module_constraint_generated": True,
        "migration_readiness_decision_generated": True,
        "post_migration_test_group_count": post_migration_test_plan.get("post_migration_test_group_count", 0),
        "pre_migration_check_count": pre_migration_checklist.get("pre_migration_check_count", 0),
        "forbidden_scope_count": migration_forbidden_scope.get("forbidden_scope_count", 0),
        "future_reserved_module_count": future_reserved_module_constraint.get("future_reserved_module_count", 0),
        "protected_assets_excluded_from_migration": True,
        "permanent_blocks_excluded_from_migration": True,
        "human_review_items_excluded_or_manual_only": True,
        "post_migration_test_required": True,
        "rollback_required": True,
        "whitebox_test_center_structure_optimization_deferred": True,
        "whitebox_test_center_must_align_with_main_project_structure": True,
        "developer_backend_overall_structure_deferred": True,
        "backend_architecture_not_finalized_now": True,
        "worldmodel_future_reserved": True,
        "memory_center_future_reserved": True,
        "library_future_reserved": True,
        "emotion_engine_future_reserved": True,
        "exploration_drive_future_reserved": True,
        "forced_future_module_finalization_allowed": False,
        "ready_for_migration_guarded_planning": boundary_ok,
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_REQUIRES_FIXES",
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
        "reason": "readiness gate + post-migration test plan + rollback requirements frozen for guarded planning",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "main_project_migration_readiness_policy": main_project_migration_readiness_policy,
        "migration_readiness_gate": migration_readiness_gate,
        "migration_allowed_scope": migration_allowed_scope,
        "migration_forbidden_scope": migration_forbidden_scope,
        "pre_migration_checklist": pre_migration_checklist,
        "post_migration_test_plan": post_migration_test_plan,
        "migration_rollback_requirement": migration_rollback_requirement,
        "whitebox_test_center_deferment_policy": whitebox_test_center_deferment_policy,
        "future_reserved_module_constraint": future_reserved_module_constraint,
        "migration_readiness_decision": migration_readiness_decision,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": no_file_move,
        "no_delete_boundary_report": no_delete,
        "no_runtime_boundary_report": no_runtime,
        "no_write_boundary_report": no_write,
    }
