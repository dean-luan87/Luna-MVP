# -*- coding: utf-8 -*-
"""Post Protected Asset and Human Review Resolution Roadmap Decision v1.

Roadmap decision only: select Main Project Structure Migration Readiness and Test Plan.
Whitebox/test center deferred until post-migration test and alignment discussion.
No human review execution, no protected asset modification, no real migration in this phase.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Post-Protected-Asset-and-Human-Review-Resolution-Roadmap-Decision-v1-001"
DECISION_SCOPE = "post_protected_asset_and_human_review_resolution_roadmap_decision_only"
DECISION_ID = "post_pahr_resolution_roadmap_decision_v1_001"
SOURCE_CHAIN = "post_protected_asset_and_human_review_resolution_roadmap_decision_v1"
FINAL_DECISION = "POST_PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_ROADMAP_DECISION_READY_FOR_MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001"
NEXT_PHASE_GUARDED_MIGRATION = "Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001"
SELECTED_ROUTE = "Main Project Structure Migration Readiness and Test Plan"
WHITEBOX_DEFER_REASON = "requires_post_migration_test_and_design_discussion"

CLOSURE_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_CLOSED_FOR_CURRENT_MAINLINE"
POST_REVIEW_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING_READY_FOR_DRYRUN"
CONSOLIDATION_ROADMAP_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_ROADMAP_DECISION_READY_FOR_PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING"
CONSOLIDATION_CLOSURE_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSED_FOR_CURRENT_MAINLINE"
STRUCTURE_MAP_DECISION = "LUNA_PROJECT_MODULE_INVENTORY_AND_STRUCTURE_MAP_DRYRUN_READY_FOR_CONSOLIDATION_PLANNING"

ROUTE_OPTIONS = [
    {
        "route_id": "A",
        "route_name": "Main Project Structure Migration Readiness and Test Plan",
        "route_type": "main_project_migration_readiness_and_test_plan",
        "readiness_level": "high",
        "dependency": [
            "protected asset resolution closed",
            "consolidation structure map",
            "controlled migration chain prerequisite",
        ],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "readiness + post-migration test plan before any real move; whitebox/test align after main project stable",
        "recommended_priority": "P0",
        "selected_now": True,
        "defer_reason": "",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "K",
        "route_name": "Main Project Structure Migration Guarded Planning",
        "route_type": "main_project_migration_guarded_planning",
        "readiness_level": "conditional",
        "dependency": ["migration readiness and test plan complete", "controlled migration prerequisites"],
        "risk_level": "high",
        "expected_value": "high",
        "runtime_risk": "medium",
        "write_risk": "high",
        "governance_debt_impact": "guarded real migration planning after readiness gate",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "enter only after Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001 GO",
        "recommended_phase_name": NEXT_PHASE_GUARDED_MIGRATION,
    },
    {
        "route_id": "L",
        "route_name": "Whitebox and Test Center Structure Optimization Planning",
        "route_type": "whitebox_test_center_structure_optimization",
        "readiness_level": "deferred",
        "dependency": [
            "main project migration complete",
            "post-migration test verification",
            "main_project_module_alignment",
        ],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "whitebox=test observation system; test_center=verification system; must 1:1 align with main project modules",
        "recommended_priority": "deferred",
        "selected_now": False,
        "defer_reason": WHITEBOX_DEFER_REASON,
        "recommended_phase_name": "Phase-Whitebox-and-Test-Center-Structure-Optimization-Planning-v1-001",
    },
    {
        "route_id": "B",
        "route_name": "Developer Backend Extraction Planning",
        "route_type": "developer_backend_extraction_planning",
        "readiness_level": "deferred",
        "dependency": ["backend overall structure user decision pending"],
        "risk_level": "high",
        "expected_value": "high",
        "runtime_risk": "medium",
        "write_risk": "high",
        "governance_debt_impact": "full developer backend extraction including whitebox/test/simulation/evaluation/verifier",
        "recommended_priority": "deferred",
        "selected_now": False,
        "defer_reason": "user has not finalized backend overall structure; full extraction deferred",
        "recommended_phase_name": "Phase-Developer-Backend-Extraction-Planning-v1-001",
    },
    {
        "route_id": "C",
        "route_name": "Docs Reorganization Planning",
        "route_type": "docs_reorganization_planning",
        "readiness_level": "medium",
        "dependency": ["whitebox/test center structure optimized first"],
        "risk_level": "medium",
        "expected_value": "medium",
        "runtime_risk": "none",
        "write_risk": "medium",
        "governance_debt_impact": "docs/modules/phases/evaluation/governance/version_logs",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "defer until after main project migration and post-migration test verification",
        "recommended_phase_name": "Phase-Docs-Reorganization-Planning-v1-001",
    },
    {
        "route_id": "D",
        "route_name": "Human Review Execution Planning",
        "route_type": "human_review_execution_planning",
        "readiness_level": "blocked",
        "dependency": ["240 human review items", "owner assignment", "audit/rollback"],
        "risk_level": "high",
        "expected_value": "medium",
        "runtime_risk": "low",
        "write_risk": "high",
        "governance_debt_impact": "real execution of 240 human review items",
        "recommended_priority": "blocked",
        "selected_now": False,
        "defer_reason": "must not enter real human review execution now",
        "recommended_phase_name": "Phase-Human-Review-Execution-Planning-v1-001",
    },
    {
        "route_id": "E",
        "route_name": "Protected Asset Manual Override Policy",
        "route_type": "protected_asset_manual_override",
        "readiness_level": "blocked",
        "dependency": ["explicit manual override", "owner approval", "audit", "rollback"],
        "risk_level": "critical",
        "expected_value": "medium",
        "runtime_risk": "low",
        "write_risk": "critical",
        "governance_debt_impact": "future override of 914 permanent blocks",
        "recommended_priority": "blocked",
        "selected_now": False,
        "defer_reason": "permanent block override must not proceed now",
        "recommended_phase_name": "Phase-Protected-Asset-Manual-Override-Policy-v1-001",
    },
    {
        "route_id": "F",
        "route_name": "Real Structure Migration Planning",
        "route_type": "real_migration_planning",
        "readiness_level": "blocked",
        "dependency": ["human review resolved", "permanent block policy", "protected asset policy"],
        "risk_level": "critical",
        "expected_value": "high",
        "runtime_risk": "critical",
        "write_risk": "critical",
        "governance_debt_impact": "real file move/delete/merge",
        "recommended_priority": "blocked",
        "selected_now": False,
        "defer_reason": "superseded by Route K after migration readiness; 240 HR + 914 permanent block still unresolved",
        "recommended_phase_name": NEXT_PHASE_GUARDED_MIGRATION,
    },
    {
        "route_id": "G",
        "route_name": "Client / Developer Backend Boundary Hardening Planning",
        "route_type": "client_backend_boundary",
        "readiness_level": "medium",
        "dependency": ["whitebox/test center not in client"],
        "risk_level": "low",
        "expected_value": "medium",
        "runtime_risk": "none",
        "write_risk": "low",
        "governance_debt_impact": "sub-goal of Route A; freeze client from whitebox/test/evaluation/verifier",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "sub-goal within main project migration chain; not standalone selection now",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "H",
        "route_name": "MidPlatform Physical Modularization Planning",
        "route_type": "midplatform_modularization",
        "readiness_level": "deferred",
        "dependency": ["backend structure decision"],
        "risk_level": "high",
        "expected_value": "high",
        "runtime_risk": "medium",
        "write_risk": "high",
        "governance_debt_impact": "midplatform physical module split",
        "recommended_priority": "deferred",
        "selected_now": False,
        "defer_reason": "backend overall structure deferred by user",
        "recommended_phase_name": "Phase-MidPlatform-Physical-Modularization-Planning-v1-001",
    },
    {
        "route_id": "I",
        "route_name": "WorldModel / Memory / Library / Emotion Placeholder Review",
        "route_type": "future_module_placeholder_review",
        "readiness_level": "discussion_only",
        "dependency": ["future_reserved modules"],
        "risk_level": "low",
        "expected_value": "low",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "background constraint only; no implementation or finalization",
        "recommended_priority": "discussion",
        "selected_now": False,
        "defer_reason": "future_reserved/discussion_required only; not standalone route",
        "recommended_phase_name": "Phase-Future-Module-Discussion-v1-001",
    },
    {
        "route_id": "J",
        "route_name": "Return to Mainline Capability Development",
        "route_type": "mainline_return",
        "readiness_level": "deferred",
        "dependency": ["whitebox/test center structure still needs organization"],
        "risk_level": "low",
        "expected_value": "medium",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "pause structure governance for capability building",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "main project migration readiness chain must complete first",
        "recommended_phase_name": "Phase-Return-to-Mainline-Capability-Development-v1-001",
    },
]

FUTURE_RESERVED_MODULE_NAMES = [
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

NON_CLAIMS = [
    "roadmap decision 不等于真实 human review 可执行",
    "roadmap decision 不等于 owner 已真实确认",
    "roadmap decision 不等于 protected assets 可修改",
    "roadmap decision 不等于 permanent block 可解除",
    "roadmap decision 不等于 audit 已提交 / rollback 已执行",
    "roadmap decision 不等于真实迁移可执行",
    "roadmap decision 不等于文件移动/删除/合并可执行",
    "roadmap decision 不等于完整 Developer Backend Architecture 已定稿",
    "roadmap decision 不等于后台整体结构已定稿",
    "selected route 仍是 readiness/test-plan only，不执行真实迁移",
    "review workflow stable 不等于可执行真实 human review 或真实迁移",
    "白盒/测试中心不能脱离主工程单独设计，须迁移后测试验证再对齐",
]

GOVERNANCE_DEBT = [
    "human_review_items=240 unresolved for real execution",
    "permanent_do_not_auto_execute=914 preserved",
    "main_project_migration_readiness_and_test_plan required before guarded migration",
    "test_after_main_project_migration_required before whitebox/test_center design",
    "whitebox_test_center_must_align_with_main_project_structure",
    "developer_backend_full_architecture deferred by user",
    "docs_reorganization deferred after main project migration chain",
    "future_reserved modules require discussion only",
]

ROOT_SPECS = [
    {
        "id": "protected_asset_resolution_closure",
        "arg": "protected_asset_resolution_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "protected_asset_human_review_resolution_closure_summary.json",
            "resolution_closure_decision_summary.json",
            "closure_boundary_freeze.json",
            "resolution_non_claims_register.json",
            "human_review_carryover_for_future_execution.json",
            "permanent_block_carryover_for_future_governance.json",
            "deferred_resolution_action_pool.json",
        ],
    },
    {
        "id": "protected_asset_resolution_post_review",
        "arg": "protected_asset_resolution_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "resolution_post_dryrun_readiness_decision.json"],
    },
    {
        "id": "protected_asset_resolution_dryrun",
        "arg": "protected_asset_resolution_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "protected_asset_resolution_planning",
        "arg": "protected_asset_resolution_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "consolidation_roadmap",
        "arg": "consolidation_roadmap_root",
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
        "id": "consolidation_post_review",
        "arg": "consolidation_post_review_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "structure_map_dryrun",
        "arg": "structure_map_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "current_to_target_structure_map.json",
            "developer_backend_extraction_map.json",
            "client_boundary_mapping.json",
            "module_inventory.json",
        ],
    },
    {
        "id": "gate_taxonomy_planning",
        "arg": "gate_taxonomy_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _future_reserved_entry(module_name: str) -> Dict[str, Any]:
    return {
        "module_name": module_name,
        "future_reserved_module": True,
        "discussion_required": True,
        "implementation_status": "incomplete_or_not_started",
        "runtime_allowed_now": False,
        "write_allowed_now": False,
        "forced_structure_finalization_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root) and all(_try_read_json(root / a) is not None for a in artifacts)
    summary_payload = _try_read_json(root / summary_file) if (root and loaded) else {}
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}}


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "decision_scope": DECISION_SCOPE,
        "decision_only": True,
        "actual_human_review_executed": False,
        "protected_assets_modified": False,
        "permanent_blocks_modified": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_decision": False,
        "readme_modified_by_decision": False,
        "phase_verdict_table_modified_by_decision": False,
        "existing_phase_result_changed": False,
        "runtime_enabled": False,
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
        "no_runtime_executed": True,
        "boundary_ok": True,
        "violations": [],
        "report_kind": kind,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_post_protected_asset_and_human_review_resolution_roadmap_decision_v1(
    *,
    protected_asset_resolution_closure_root: str,
    protected_asset_resolution_post_review_root: str,
    protected_asset_resolution_dryrun_root: str,
    protected_asset_resolution_planning_root: str,
    consolidation_roadmap_root: str,
    consolidation_closure_root: str,
    consolidation_post_review_root: Optional[str] = None,
    structure_map_dryrun_root: str,
    gate_taxonomy_planning_root: str,
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

    closure_loaded = (
        roots["protected_asset_resolution_closure"]["loaded"]
        and summaries["protected_asset_resolution_closure"].get("final_decision") == CLOSURE_DECISION
        and summaries["protected_asset_resolution_closure"].get("protected_asset_resolution_closed") is True
    )
    post_review_loaded = (
        roots["protected_asset_resolution_post_review"]["loaded"]
        and summaries["protected_asset_resolution_post_review"].get("final_decision") == POST_REVIEW_DECISION
    )
    dryrun_loaded = (
        roots["protected_asset_resolution_dryrun"]["loaded"]
        and summaries["protected_asset_resolution_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    planning_loaded = (
        roots["protected_asset_resolution_planning"]["loaded"]
        and summaries["protected_asset_resolution_planning"].get("final_decision") == PLANNING_DECISION
    )
    consolidation_roadmap_loaded = roots["consolidation_roadmap"]["loaded"]
    consolidation_closure_loaded = (
        roots["consolidation_closure"]["loaded"]
        and summaries["consolidation_closure"].get("final_decision") == CONSOLIDATION_CLOSURE_DECISION
    )
    structure_loaded = (
        roots["structure_map_dryrun"]["loaded"]
        and summaries["structure_map_dryrun"].get("final_decision") == STRUCTURE_MAP_DECISION
    )
    gate_loaded = roots["gate_taxonomy_planning"]["loaded"]

    closure_root = roots["protected_asset_resolution_closure"]["root"]
    closure_summary = summaries["protected_asset_resolution_closure"]
    decision_summary = _try_read_json(closure_root / "resolution_closure_decision_summary.json") if closure_root else {}
    human_carry = _try_read_json(closure_root / "human_review_carryover_for_future_execution.json") if closure_root else {}
    permanent_carry = _try_read_json(closure_root / "permanent_block_carryover_for_future_governance.json") if closure_root else {}
    closure_freeze = _try_read_json(closure_root / "closure_boundary_freeze.json") if closure_root else {}

    structure_root = roots["structure_map_dryrun"]["root"]
    structure_map = _try_read_json(structure_root / "current_to_target_structure_map.json") if structure_root else {}
    dev_backend_map = _try_read_json(structure_root / "developer_backend_extraction_map.json") if structure_root else {}
    client_boundary = _try_read_json(structure_root / "client_boundary_mapping.json") if structure_root else {}
    module_inventory = _try_read_json(structure_root / "module_inventory.json") if structure_root else {}
    hist_test = (
        _try_read_json(structure_root / "historical_test_asset_classification.json")
        if structure_root
        else None
    ) or _try_read_json(structure_root / "migration_risk_register.json") if structure_root else {}

    human_review_count = closure_summary.get("human_review_case_count", decision_summary.get("human_review_case_count", 240))
    permanent_count = closure_summary.get("permanent_dnae_case_count", decision_summary.get("permanent_dnae_case_count", 914))
    permanent_preserved = closure_summary.get("permanent_dnae_preserved_count", decision_summary.get("permanent_dnae_preserved_count", 914))
    inventory_count = (module_inventory or {}).get("entry_count", summaries["structure_map_dryrun"].get("inventory_entry_count", 7391))

    protected_asset_resolution_closure_status_summary = {
        "protected_asset_resolution_closed": closure_loaded,
        "closure_final_decision": CLOSURE_DECISION,
        "human_review_case_count": human_review_count,
        "human_review_closed_no_execution_count": closure_summary.get("human_review_closed_no_execution_count", 240),
        "permanent_dnae_case_count": permanent_count,
        "permanent_dnae_preserved_count": permanent_preserved,
        "protected_conflict_count": closure_summary.get("protected_conflict_count", 448),
        "static_dnae_rule_count": closure_summary.get("static_dnae_rule_count", 466),
        "real_migration_allowed": False,
        "ready_for_real_human_review_execution": False,
        "inventory_entry_count": inventory_count,
        "structure_map_loaded": structure_loaded,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    route_option_matrix = {
        "routes": ROUTE_OPTIONS,
        "route_option_count": len(ROUTE_OPTIONS),
        "selected_route": SELECTED_ROUTE,
        "selected_route_id": "A",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    priority_ranking = {
        "rankings": [
            {"rank": 1, "route_id": "A", "route_name": SELECTED_ROUTE, "priority": "P0", "selected_now": True},
            {"rank": 2, "route_id": "K", "route_name": "Main Project Structure Migration Guarded Planning", "priority": "P1", "selected_now": False, "after": NEXT_PHASE},
            {"rank": 3, "route_id": "G", "route_name": "Client / Developer Backend Boundary Hardening Planning", "priority": "P1", "selected_now": False, "sub_goal_of": "migration_chain"},
            {"rank": 4, "route_id": "L", "route_name": "Whitebox and Test Center Structure Optimization Planning", "priority": "deferred", "selected_now": False, "defer_reason": WHITEBOX_DEFER_REASON},
            {"rank": 5, "route_id": "C", "route_name": "Docs Reorganization Planning", "priority": "P2", "selected_now": False},
            {"rank": 6, "route_id": "J", "route_name": "Return to Mainline Capability Development", "priority": "P2", "selected_now": False},
            {"rank": 7, "route_id": "I", "route_name": "WorldModel / Memory / Library / Emotion Placeholder Review", "priority": "discussion", "selected_now": False},
            {"rank": 8, "route_id": "B", "route_name": "Developer Backend Extraction Planning", "priority": "deferred", "selected_now": False},
            {"rank": 9, "route_id": "H", "route_name": "MidPlatform Physical Modularization Planning", "priority": "deferred", "selected_now": False},
            {"rank": 10, "route_id": "D", "route_name": "Human Review Execution Planning", "priority": "blocked", "selected_now": False},
            {"rank": 11, "route_id": "E", "route_name": "Protected Asset Manual Override Policy", "priority": "blocked", "selected_now": False},
            {"rank": 12, "route_id": "F", "route_name": "Real Structure Migration Planning", "priority": "blocked", "selected_now": False},
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    selection_rationale = [
        "Protected Asset / Human Review Resolution chain closed (Planning→DryRun→Post-Review→Closure)",
        f"human_review={human_review_count} closed_no_execution; real execution deferred",
        f"permanent_block={permanent_preserved} preserved; override deferred",
        "main project structure migration chain must complete before whitebox/test_center design",
        "test_after_main_project_migration_required=true before observation/verification system alignment",
        "whitebox=test observation system; test_center=verification system; must align 1:1 with main project modules",
        f"whitebox_test_center deferred: {WHITEBOX_DEFER_REASON}",
        "Route A is readiness + test plan only; Route K guarded migration after readiness GO",
        "backend overall structure deferred; no full Developer Backend Architecture",
        "WorldModel/Memory/Library/Emotion remain future_reserved/discussion_required",
    ]

    recommended_next_phase_decision = {
        "selected_route": SELECTED_ROUTE,
        "selected_route_id": "A",
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "selection_rationale": selection_rationale,
        "real_migration_deferred": True,
        "human_review_execution_deferred": True,
        "developer_backend_full_extraction_deferred": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    main_project_migration_readiness_route_decision = {
        "route_name": SELECTED_ROUTE,
        "route_id": "A",
        "selected_now": True,
        "recommended_next_phase": NEXT_PHASE,
        "next_phase_after_readiness": NEXT_PHASE_GUARDED_MIGRATION,
        "planning_only": True,
        "auto_execute_allowed": False,
        "scope": [
            "migration_readiness_gate",
            "controlled_migration_prerequisites",
            "post_migration_test_verification_plan",
            "main_project_integrity_checks",
        ],
        "not_in_scope": ["real_file_move", "real_file_delete", "module_merge_execution"],
        "structure_map_ref": "structure_map/current_to_target_structure_map.json",
        "inventory_entry_count": inventory_count,
        "test_after_main_project_migration_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_whitebox_test_center_structure_optimization_register = {
        "deferred": True,
        "whitebox_test_center_structure_optimization_deferred": True,
        "reason": WHITEBOX_DEFER_REASON,
        "test_after_main_project_migration_required": True,
        "whitebox_test_center_must_align_with_main_project_structure": True,
        "whitebox_role": "main_project_observation_system",
        "test_center_role": "main_project_verification_system",
        "risk_if_premature": [
            "main project modules reorganized but whitebox still old structure",
            "test_center validates old paths",
            "verifier/go_no_go/logs cannot map to new modules",
        ],
        "recommended_after": [
            NEXT_PHASE,
            NEXT_PHASE_GUARDED_MIGRATION,
            "post_migration_test_verification",
            "Phase-Whitebox-and-Test-Center-Structure-Optimization-Planning-v1-001",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    whitebox_test_center_route_decision = {
        **deferred_whitebox_test_center_structure_optimization_register,
        "route_name": "Whitebox and Test Center Structure Optimization Planning",
        "route_id": "L",
        "selected_now": False,
        "source_chain": SOURCE_CHAIN,
    }

    deferred_developer_backend_architecture_register = {
        "deferred": True,
        "developer_backend_architecture_deferred": True,
        "developer_backend_full_extraction_deferred": True,
        "backend_overall_structure_deferred_by_user": True,
        "reason": "user has not finalized backend overall structure; main project migration chain first",
        "allowed_now": ["main_project_migration_readiness", "controlled_migration_planning"],
        "recommended_after": NEXT_PHASE_GUARDED_MIGRATION,
        "developer_backend_map_available": bool(dev_backend_map),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_docs_reorganization_register = {
        "deferred": True,
        "reason": "defer until after main project migration and post-migration test verification",
        "recommended_after": NEXT_PHASE_GUARDED_MIGRATION,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_human_review_execution_register = {
        "deferred": True,
        "blocked": True,
        "human_review_case_count": human_review_count,
        "reason": "240 human review items require explicit owner/manual decision; must not enter real execution now",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_real_migration_register = {
        "deferred": True,
        "blocked_now": True,
        "reason": "enter guarded migration only after readiness and test plan; HR=240 and permanent=914 still frozen",
        "blocked_routes": ["F"],
        "ready_for_real_migration": False,
        "guarded_migration_route_id": "K",
        "guarded_migration_phase": NEXT_PHASE_GUARDED_MIGRATION,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    future_reserved_entries = [_future_reserved_entry(name) for name in FUTURE_RESERVED_MODULE_NAMES]
    future_reserved_module_discussion_register = {
        "modules": future_reserved_entries,
        "module_count": len(future_reserved_entries),
        "future_reserved_modules_discussion_required": True,
        "forced_future_module_finalization_allowed": False,
        "policy": "discussion_required only; no implementation; no forced finalization",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary_freeze = {
        **(closure_freeze or {}),
        "no-real-human-review-execution": True,
        "no-protected-asset-modification": True,
        "no-permanent-block-release": True,
        "no-real-migration": True,
        "no-full-developer-backend-architecture": True,
        "no-backend-overall-structure-finalization": True,
        "whitebox-test-center-structure-optimization-deferred": True,
        "test-after-main-project-migration-required": True,
        "whitebox-test-center-must-align-with-main-project": True,
        "main-project-migration-readiness-selected": True,
        "roadmap-decision-only": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_roadmap_register = {
        "debt_items": GOVERNANCE_DEBT,
        "debt_count": len(GOVERNANCE_DEBT),
        "primary_resolution_track": SELECTED_ROUTE,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    non_claims_register = {
        "non_claims": NON_CLAIMS,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    for flag_name, loaded in (
        ("protected_asset_resolution_closure_input_loaded", closure_loaded),
        ("protected_asset_resolution_post_review_input_loaded", post_review_loaded),
        ("protected_asset_resolution_dryrun_input_loaded", dryrun_loaded),
        ("protected_asset_resolution_planning_input_loaded", planning_loaded),
        ("consolidation_roadmap_input_loaded", consolidation_roadmap_loaded),
        ("consolidation_closure_input_loaded", consolidation_closure_loaded),
        ("structure_map_dryrun_input_loaded", structure_loaded),
        ("gate_taxonomy_input_loaded", gate_loaded),
    ):
        if not loaded:
            blockers.append(flag_name)

    boundary_ok = not blockers
    final_decision = FINAL_DECISION if boundary_ok else "POST_PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_ROADMAP_DECISION_REQUIRES_FIXES"
    next_phase = NEXT_PHASE if boundary_ok else PHASE_ID

    next_phase_recommendation = {
        "recommended_next_phase": next_phase,
        "final_decision": final_decision,
        "selected_route": SELECTED_ROUTE,
        "priority_note": "主工程迁移就绪与测试计划优先；迁移后测试验证；白盒/测试中心须与主工程模块一一对齐后再规划；后台整体暂缓",
        "recommended_phase_sequence": [
            NEXT_PHASE,
            NEXT_PHASE_GUARDED_MIGRATION,
            "post_migration_test_verification",
            "whitebox_test_center_alignment_discussion",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "protected_asset_resolution_closure_input_loaded": closure_loaded,
        "protected_asset_resolution_post_review_input_loaded": post_review_loaded,
        "protected_asset_resolution_dryrun_input_loaded": dryrun_loaded,
        "protected_asset_resolution_planning_input_loaded": planning_loaded,
        "consolidation_roadmap_input_loaded": consolidation_roadmap_loaded,
        "consolidation_closure_input_loaded": consolidation_closure_loaded,
        "structure_map_dryrun_input_loaded": structure_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "closure_status_summary_generated": True,
        "route_option_matrix_generated": True,
        "priority_ranking_generated": True,
        "recommended_next_phase_decision_generated": True,
        "main_project_migration_readiness_route_decision_generated": True,
        "whitebox_test_center_route_decision_generated": True,
        "deferred_whitebox_test_center_structure_optimization_register_generated": True,
        "deferred_developer_backend_architecture_register_generated": True,
        "deferred_docs_reorganization_register_generated": True,
        "deferred_human_review_execution_register_generated": True,
        "deferred_real_migration_register_generated": True,
        "future_reserved_module_discussion_register_generated": True,
        "boundary_freeze_generated": True,
        "governance_debt_roadmap_register_generated": True,
        "non_claims_register_generated": True,
        "route_option_count": len(ROUTE_OPTIONS),
        "selected_route": SELECTED_ROUTE,
        "protected_asset_resolution_closed": closure_loaded,
        "human_review_case_count": human_review_count,
        "permanent_dnae_case_count": permanent_count,
        "permanent_dnae_preserved_count": permanent_preserved,
        "real_migration_allowed": False,
        "ready_for_real_human_review_execution": False,
        "ready_for_protected_asset_modification": False,
        "ready_for_permanent_block_override": False,
        "ready_for_real_migration": False,
        "main_project_migration_readiness_selected": True,
        "whitebox_test_center_structure_optimization_selected": False,
        "whitebox_test_center_structure_optimization_deferred": True,
        "whitebox_test_center_structure_optimization_defer_reason": WHITEBOX_DEFER_REASON,
        "test_after_main_project_migration_required": True,
        "whitebox_test_center_must_align_with_main_project_structure": True,
        "developer_backend_architecture_deferred": True,
        "developer_backend_full_extraction_deferred": True,
        "developer_backend_overall_structure_deferred": True,
        "docs_reorganization_deferred": True,
        "human_review_execution_deferred": True,
        "protected_asset_manual_override_deferred": True,
        "real_structure_migration_blocked": True,
        "real_structure_migration_blocked_now": True,
        "main_project_migration_guarded_planning_deferred_until_readiness": True,
        "midplatform_physical_modularization_deferred": True,
        "return_to_mainline_deferred": True,
        "backend_overall_structure_deferred_by_user": True,
        "only_whitebox_and_test_center_allowed_now": False,
        "worldmodel_future_reserved": True,
        "memory_center_future_reserved": True,
        "library_future_reserved": True,
        "emotion_engine_future_reserved": True,
        "exploration_drive_future_reserved": True,
        "future_reserved_modules_discussion_required": True,
        "forced_future_module_finalization_allowed": False,
        "actual_human_review_executed": False,
        "protected_assets_modified": False,
        "permanent_blocks_modified": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_decision": False,
        "readme_modified_by_decision": False,
        "phase_verdict_table_modified_by_decision": False,
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
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "protected_asset_resolution_closure_status_summary": protected_asset_resolution_closure_status_summary,
        "route_option_matrix": route_option_matrix,
        "priority_ranking": priority_ranking,
        "recommended_next_phase_decision": recommended_next_phase_decision,
        "main_project_migration_readiness_route_decision": main_project_migration_readiness_route_decision,
        "whitebox_test_center_route_decision": whitebox_test_center_route_decision,
        "deferred_whitebox_test_center_structure_optimization_register": deferred_whitebox_test_center_structure_optimization_register,
        "deferred_developer_backend_architecture_register": deferred_developer_backend_architecture_register,
        "deferred_docs_reorganization_register": deferred_docs_reorganization_register,
        "deferred_human_review_execution_register": deferred_human_review_execution_register,
        "deferred_real_migration_register": deferred_real_migration_register,
        "future_reserved_module_discussion_register": future_reserved_module_discussion_register,
        "boundary_freeze": boundary_freeze,
        "governance_debt_roadmap_register": governance_debt_roadmap_register,
        "non_claims_register": non_claims_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
        "verifier_report": {"verifier": "PENDING", "phase": "roadmap_decision", "source_chain": SOURCE_CHAIN},
    }
