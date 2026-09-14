# -*- coding: utf-8 -*-
"""Luna Project Structure Consolidation Roadmap Decision v1.

Roadmap decision only: select next governance track without real migration.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Luna-Project-Structure-Consolidation-Roadmap-Decision-v1-001"
DECISION_SCOPE = "luna_project_structure_consolidation_roadmap_decision_only"
DECISION_ID = "lpsc_roadmap_decision_v1_001"
SOURCE_CHAIN = "luna_project_structure_consolidation_roadmap_decision_v1"
FINAL_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_ROADMAP_DECISION_READY_FOR_PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING"
NEXT_PHASE = "Phase-Protected-Asset-and-Human-Review-Resolution-Planning-v1-001"
SELECTED_ROUTE = "Protected Asset and Human Review Resolution Planning"

CLOSURE_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSED_FOR_CURRENT_MAINLINE"
POST_REVIEW_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_PLANNING_READY_FOR_CONSOLIDATION_DRYRUN"
STRUCTURE_MAP_DECISION = "LUNA_PROJECT_MODULE_INVENTORY_AND_STRUCTURE_MAP_DRYRUN_READY_FOR_CONSOLIDATION_PLANNING"
GOVERNANCE_DECISION = "LUNA_PROJECT_STRUCTURE_GOVERNANCE_AND_MODULARIZATION_PLANNING_READY_FOR_STRUCTURE_MAP_DRYRUN"

ROUTE_OPTIONS = [
    {
        "route_id": "A",
        "route_name": "Protected Asset and Human Review Resolution Planning",
        "route_type": "protected_asset_human_review_planning",
        "readiness_level": "high",
        "dependency": ["consolidation closed", "human_review=240", "permanent_block=914"],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "defines protected asset types, human review resolution rules, DNAE policy before any migration",
        "recommended_priority": "P0",
        "selected_now": True,
        "defer_reason": "",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "B",
        "route_name": "Developer Backend Extraction Planning",
        "route_type": "developer_backend_extraction_planning",
        "readiness_level": "medium",
        "dependency": ["protected asset policy defined", "human review rules defined"],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "low",
        "write_risk": "medium",
        "governance_debt_impact": "whitebox/test_center/simulation_lab/evaluation/verifier backend extraction plan",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "requires protected asset and human review rules first",
        "recommended_phase_name": "Phase-Developer-Backend-Extraction-Planning-v1-001",
    },
    {
        "route_id": "C",
        "route_name": "Docs Reorganization Planning",
        "route_type": "docs_reorganization_planning",
        "readiness_level": "medium",
        "dependency": ["protected asset policy defined"],
        "risk_level": "medium",
        "expected_value": "medium",
        "runtime_risk": "none",
        "write_risk": "medium",
        "governance_debt_impact": "docs/modules/phases/evaluation/governance/version_logs structure plan",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "should not precede protected asset policy",
        "recommended_phase_name": "Phase-Docs-Reorganization-Planning-v1-001",
    },
    {
        "route_id": "D",
        "route_name": "MidPlatform Physical Modularization Planning",
        "route_type": "midplatform_modularization_planning",
        "readiness_level": "medium",
        "dependency": ["protected asset policy", "human review rules"],
        "risk_level": "high",
        "expected_value": "high",
        "runtime_risk": "medium",
        "write_risk": "high",
        "governance_debt_impact": "midplatform operating core/resource/privacy/handoff physical split",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "real structural change unsafe before protected asset resolution",
        "recommended_phase_name": "Phase-MidPlatform-Physical-Modularization-Planning-v1-001",
    },
    {
        "route_id": "E",
        "route_name": "Client / Developer Backend Boundary Hardening Planning",
        "route_type": "client_backend_boundary_planning",
        "readiness_level": "medium",
        "dependency": ["developer backend extraction planning or parallel"],
        "risk_level": "medium",
        "expected_value": "medium",
        "runtime_risk": "low",
        "write_risk": "low",
        "governance_debt_impact": "freeze client from whitebox/test/evaluation/verifier/debug overlay",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "can parallel developer backend extraction after Route A",
        "recommended_phase_name": "Phase-Client-Developer-Backend-Boundary-Hardening-Planning-v1-001",
    },
    {
        "route_id": "F",
        "route_name": "Human Review Execution Trial",
        "route_type": "human_review_execution",
        "readiness_level": "low",
        "dependency": ["human review resolution planning complete"],
        "risk_level": "high",
        "expected_value": "medium",
        "runtime_risk": "low",
        "write_risk": "high",
        "governance_debt_impact": "process 240 human review items",
        "recommended_priority": "P3",
        "selected_now": False,
        "defer_reason": "requires resolution planning before execution trial",
        "recommended_phase_name": "Phase-Human-Review-Execution-Trial-v1-001",
    },
    {
        "route_id": "G",
        "route_name": "Real Structure Migration Guarded Planning",
        "route_type": "real_migration_planning",
        "readiness_level": "blocked",
        "dependency": ["human review resolved", "permanent block policy", "protected asset policy"],
        "risk_level": "critical",
        "expected_value": "high",
        "runtime_risk": "high",
        "write_risk": "critical",
        "governance_debt_impact": "real file move/delete/merge planning",
        "recommended_priority": "blocked",
        "selected_now": False,
        "defer_reason": "permanent block=914 and human_review=240 unresolved",
        "recommended_phase_name": "Phase-Real-Structure-Migration-Guarded-Planning-v1-001",
    },
    {
        "route_id": "H",
        "route_name": "Legacy Archive Planning",
        "route_type": "legacy_archive_planning",
        "readiness_level": "low",
        "dependency": ["protected asset policy", "human review rules"],
        "risk_level": "high",
        "expected_value": "medium",
        "runtime_risk": "low",
        "write_risk": "high",
        "governance_debt_impact": "legacy sprawl archive without harming active/protected assets",
        "recommended_priority": "P3",
        "selected_now": False,
        "defer_reason": "risk of mis-archiving active/protected assets",
        "recommended_phase_name": "Phase-Legacy-Archive-Planning-v1-001",
    },
    {
        "route_id": "I",
        "route_name": "Return to Mainline Capability Development",
        "route_type": "mainline_return",
        "readiness_level": "medium",
        "dependency": ["structure governance debt acceptable"],
        "risk_level": "low",
        "expected_value": "medium",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "pause structure governance for capability building",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "human review/protected asset debt still open",
        "recommended_phase_name": "Phase-Return-to-Mainline-Capability-Development-v1-001",
    },
    {
        "route_id": "J",
        "route_name": "Protected Asset Policy",
        "route_type": "protected_asset_policy",
        "readiness_level": "high",
        "dependency": ["consolidation closed"],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "none",
        "write_risk": "none",
        "governance_debt_impact": "merged into Route A as dedicated protected asset type definitions",
        "recommended_priority": "P0",
        "selected_now": False,
        "defer_reason": "merged into Route A Protected Asset and Human Review Resolution Planning",
        "recommended_phase_name": NEXT_PHASE,
    },
]

NON_CLAIMS = [
    "roadmap decision 不等于真实迁移可执行",
    "roadmap decision 不等于 human review 已处理",
    "roadmap decision 不等于 protected assets 已归档或移动",
    "roadmap decision 不等于 developer backend 已抽离",
    "roadmap decision 不等于 docs 已重组",
    "roadmap decision 不等于 midplatform 已物理拆分",
    "roadmap decision 不等于 production structure ready",
    "selected route 仍是 planning-only，不执行文件操作",
]

GOVERNANCE_DEBT = [
    "human_review_items=240 unresolved",
    "permanent_do_not_auto_execute=914 unresolved",
    "protected_eval_out_verifier_gonogo_phase_records require policy",
    "future_placeholder_current_code=35 require review rules",
    "high_risk_merge=5 require resolution planning",
    "developer_backend_extraction not yet planned",
    "docs_reorganization not yet planned",
    "midplatform_physical_modularization not yet planned",
    "real_structure_migration blocked until debt resolved",
]

ROOT_SPECS = [
    {
        "id": "consolidation_closure",
        "arg": "consolidation_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "consolidation_closure_decision_summary.json",
            "human_review_carryover_register.json",
            "permanent_do_not_auto_execute_carryover.json",
            "deferred_consolidation_action_pool.json",
            "closure_boundary_freeze.json",
            "consolidation_non_claims_register.json",
        ],
    },
    {
        "id": "consolidation_post_review",
        "arg": "consolidation_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "consolidation_post_dryrun_review_decision.json"],
    },
    {
        "id": "consolidation_dryrun",
        "arg": "consolidation_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "consolidation_planning",
        "arg": "consolidation_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "structure_map_dryrun",
        "arg": "structure_map_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "project_structure_governance_planning",
        "arg": "project_structure_governance_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
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
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "actual_consolidation_execution": False,
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


def run_luna_project_structure_consolidation_roadmap_decision_v1(
    *,
    consolidation_closure_root: str,
    consolidation_post_review_root: str,
    consolidation_dryrun_root: str,
    consolidation_planning_root: str,
    structure_map_dryrun_root: str,
    project_structure_governance_planning_root: str,
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
        roots["consolidation_closure"]["loaded"]
        and summaries["consolidation_closure"].get("final_decision") == CLOSURE_DECISION
        and summaries["consolidation_closure"].get("consolidation_closed") is True
    )
    post_review_loaded = roots["consolidation_post_review"]["loaded"] and summaries["consolidation_post_review"].get(
        "final_decision"
    ) == POST_REVIEW_DECISION
    dryrun_loaded = roots["consolidation_dryrun"]["loaded"] and summaries["consolidation_dryrun"].get("final_decision") == DRYRUN_DECISION
    planning_loaded = roots["consolidation_planning"]["loaded"] and summaries["consolidation_planning"].get(
        "final_decision"
    ) == PLANNING_DECISION
    structure_loaded = roots["structure_map_dryrun"]["loaded"] and summaries["structure_map_dryrun"].get(
        "final_decision"
    ) == STRUCTURE_MAP_DECISION
    governance_loaded = roots["project_structure_governance_planning"]["loaded"] and summaries[
        "project_structure_governance_planning"
    ].get("final_decision") == GOVERNANCE_DECISION
    gate_loaded = roots["gate_taxonomy_planning"]["loaded"]

    closure_root = roots["consolidation_closure"]["root"]
    closure_summary = summaries["consolidation_closure"]
    decision_summary = _try_read_json(closure_root / "consolidation_closure_decision_summary.json") if closure_root else {}
    human_carry = _try_read_json(closure_root / "human_review_carryover_register.json") if closure_root else {}
    permanent_carry = _try_read_json(closure_root / "permanent_do_not_auto_execute_carryover.json") if closure_root else {}
    deferred_pool = _try_read_json(closure_root / "deferred_consolidation_action_pool.json") if closure_root else {}
    closure_freeze = _try_read_json(closure_root / "closure_boundary_freeze.json") if closure_root else {}

    plan_revision = closure_summary.get("plan_revision_required", decision_summary.get("plan_revision_required", 0))
    human_review = closure_summary.get("human_review_required", human_carry.get("human_review_required_count", 240))
    permanent_block = closure_summary.get(
        "permanent_do_not_auto_execute", permanent_carry.get("permanent_do_not_auto_execute_count", 914)
    )
    real_migration_allowed = False

    consolidation_closure_status_summary = {
        "consolidation_closed": closure_loaded,
        "closure_final_decision": CLOSURE_DECISION,
        "plan_revision_required": plan_revision,
        "human_review_required": human_review,
        "permanent_do_not_auto_execute": permanent_block,
        "total_inventory_entries": closure_summary.get("total_inventory_entries", 7391),
        "total_conflict_count": closure_summary.get("total_conflict_count", 1830),
        "acceptable_conflicts": closure_summary.get("acceptable_conflicts", 1382),
        "real_migration_allowed": real_migration_allowed,
        "deferred_action_count": deferred_pool.get("deferred_action_count", 15),
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
            {"rank": 2, "route_id": "B", "route_name": "Developer Backend Extraction Planning", "priority": "P1", "selected_now": False},
            {"rank": 3, "route_id": "E", "route_name": "Client / Developer Backend Boundary Hardening Planning", "priority": "P1", "selected_now": False},
            {"rank": 4, "route_id": "C", "route_name": "Docs Reorganization Planning", "priority": "P2", "selected_now": False},
            {"rank": 5, "route_id": "D", "route_name": "MidPlatform Physical Modularization Planning", "priority": "P2", "selected_now": False},
            {"rank": 6, "route_id": "I", "route_name": "Return to Mainline Capability Development", "priority": "P2", "selected_now": False},
            {"rank": 7, "route_id": "F", "route_name": "Human Review Execution Trial", "priority": "P3", "selected_now": False},
            {"rank": 8, "route_id": "H", "route_name": "Legacy Archive Planning", "priority": "P3", "selected_now": False},
            {"rank": 9, "route_id": "G", "route_name": "Real Structure Migration Guarded Planning", "priority": "blocked", "selected_now": False},
            {"rank": 10, "route_id": "J", "route_name": "Protected Asset Policy", "priority": "P0", "selected_now": False, "merged_into": "A"},
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    selection_rationale = [
        "plan_revision_required=0; no return to consolidation planning needed",
        f"human_review_required={human_review}; resolution planning required before migration",
        f"permanent_do_not_auto_execute={permanent_block}; protected asset policy required",
        "developer backend extraction / docs reorg / midplatform modularization unsafe without Route A",
        "Route A is planning-only; no real migration",
    ]

    recommended_next_phase_decision = {
        "selected_route": SELECTED_ROUTE,
        "selected_route_id": "A",
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "selection_rationale": selection_rationale,
        "real_migration_deferred": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    protected_asset_and_human_review_route_decision = {
        "route_name": SELECTED_ROUTE,
        "route_id": "A",
        "selected_now": True,
        "recommended_next_phase": NEXT_PHASE,
        "protected_asset_policy_required": True,
        "human_review_resolution_required": True,
        "permanent_block_resolution_required": True,
        "human_review_count": human_review,
        "permanent_block_count": permanent_block,
        "protected_conflict_count": permanent_carry.get("protected_conflict_count", 448),
        "high_risk_merge_items": human_carry.get("high_risk_merge_items", 5),
        "future_placeholder_current_code_items": human_carry.get("future_placeholder_current_code_items", 35),
        "planning_only": True,
        "auto_execute_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_real_migration_register = {
        "deferred": True,
        "reason": "permanent_block=914 and human_review=240 unresolved",
        "blocked_routes": ["G"],
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_developer_backend_extraction_register = {
        "deferred": True,
        "reason": "requires protected asset and human review rules first",
        "recommended_after": NEXT_PHASE,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_docs_reorganization_register = {
        "deferred": True,
        "reason": "should not precede protected asset policy",
        "recommended_after": NEXT_PHASE,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_midplatform_modularization_register = {
        "deferred": True,
        "reason": "real structural change unsafe before protected asset resolution",
        "recommended_after": NEXT_PHASE,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_mainline_return_register = {
        "deferred": True,
        "reason": "human review/protected asset debt still open",
        "alternative_when_debt_resolved": "Phase-Return-to-Mainline-Capability-Development-v1-001",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary_freeze = {
        **(closure_freeze or {}),
        "no-real-migration": True,
        "no-human-review-execution": True,
        "no-protected-asset-handling": True,
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
        ("consolidation_closure_input_loaded", closure_loaded),
        ("consolidation_post_review_input_loaded", post_review_loaded),
        ("consolidation_dryrun_input_loaded", dryrun_loaded),
        ("consolidation_planning_input_loaded", planning_loaded),
        ("structure_map_dryrun_input_loaded", structure_loaded),
        ("project_structure_governance_planning_input_loaded", governance_loaded),
        ("gate_taxonomy_input_loaded", gate_loaded),
    ):
        if not loaded:
            blockers.append(flag_name)

    boundary_ok = not blockers
    final_decision = FINAL_DECISION if boundary_ok else "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_ROADMAP_DECISION_REQUIRES_FIXES"
    next_phase = NEXT_PHASE if boundary_ok else PHASE_ID

    next_phase_recommendation = {
        "recommended_next_phase": next_phase,
        "final_decision": final_decision,
        "selected_route": SELECTED_ROUTE,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "consolidation_closure_input_loaded": closure_loaded,
        "consolidation_post_review_input_loaded": post_review_loaded,
        "consolidation_dryrun_input_loaded": dryrun_loaded,
        "consolidation_planning_input_loaded": planning_loaded,
        "structure_map_dryrun_input_loaded": structure_loaded,
        "project_structure_governance_planning_input_loaded": governance_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "closure_status_summary_generated": True,
        "route_option_matrix_generated": True,
        "priority_ranking_generated": True,
        "recommended_next_phase_decision_generated": True,
        "protected_asset_and_human_review_route_decision_generated": True,
        "deferred_real_migration_register_generated": True,
        "boundary_freeze_generated": True,
        "governance_debt_roadmap_register_generated": True,
        "non_claims_register_generated": True,
        "route_option_count": len(ROUTE_OPTIONS),
        "selected_route": SELECTED_ROUTE,
        "consolidation_closed": closure_loaded,
        "plan_revision_required": plan_revision,
        "human_review_required": human_review,
        "permanent_do_not_auto_execute": permanent_block,
        "real_migration_allowed": False,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "protected_asset_policy_required": True,
        "human_review_resolution_required": True,
        "permanent_block_resolution_required": True,
        "developer_backend_extraction_deferred": True,
        "docs_reorganization_deferred": True,
        "midplatform_physical_modularization_deferred": True,
        "real_structure_migration_deferred": True,
        "return_to_mainline_deferred": True,
        "actual_consolidation_execution": False,
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
        "consolidation_closure_status_summary": consolidation_closure_status_summary,
        "route_option_matrix": route_option_matrix,
        "priority_ranking": priority_ranking,
        "recommended_next_phase_decision": recommended_next_phase_decision,
        "protected_asset_and_human_review_route_decision": protected_asset_and_human_review_route_decision,
        "deferred_real_migration_register": deferred_real_migration_register,
        "deferred_developer_backend_extraction_register": deferred_developer_backend_extraction_register,
        "deferred_docs_reorganization_register": deferred_docs_reorganization_register,
        "deferred_midplatform_modularization_register": deferred_midplatform_modularization_register,
        "deferred_mainline_return_register": deferred_mainline_return_register,
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
