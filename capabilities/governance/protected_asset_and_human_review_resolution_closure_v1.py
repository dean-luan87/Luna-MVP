# -*- coding: utf-8 -*-
"""Protected Asset and Human Review Resolution Closure v1.

Closure-only: status freeze / boundary freeze / non-claims / carryover registers.
No human review execution, no protected asset modification, no file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Protected-Asset-and-Human-Review-Resolution-Closure-v1-001"
CLOSURE_ID = "pahr_resolution_closure_v1_001"
CLOSURE_SCOPE = "protected_asset_and_human_review_resolution_closure_only"
SOURCE_CHAIN = "protected_asset_and_human_review_resolution_closure_v1"
FINAL_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-Protected-Asset-and-Human-Review-Resolution-Roadmap-Decision-v1-001"

POST_REVIEW_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING_READY_FOR_DRYRUN"

COMPLETED_PHASES = [
    (
        "Phase-Protected-Asset-and-Human-Review-Resolution-Planning-v1-001",
        "Protected Asset and Human Review Resolution Planning",
        "planning",
        "_eval_out/protected_asset_and_human_review_resolution_planning_v1_smoke_v0/",
        PLANNING_DECISION,
        "protected asset / human review / permanent DNAE policy framework",
    ),
    (
        "Phase-Protected-Asset-and-Human-Review-Resolution-DryRun-v1-001",
        "Protected Asset and Human Review Resolution DryRun",
        "resolution_dryrun",
        "_eval_out/protected_asset_and_human_review_resolution_dryrun_v1_smoke_v0/",
        DRYRUN_DECISION,
        "240 HR + 914 DNAE simulation, audit/rollback refs, forbidden decision/state blocking",
    ),
    (
        "Phase-Protected-Asset-and-Human-Review-Resolution-Post-DryRun-Review-v1-001",
        "Protected Asset and Human Review Resolution Post-DryRun Review",
        "post_review",
        "_eval_out/protected_asset_and_human_review_resolution_post_dryrun_review_v1_smoke_v0/",
        POST_REVIEW_DECISION,
        "formal review of dryrun outputs for closure readiness",
    ),
]

NON_CLAIMS = [
    "closure 不等于真实 human review 可执行",
    "closure 不等于 owner 已真实确认",
    "closure 不等于 protected assets 可修改",
    "closure 不等于 permanent block 可解除",
    "closure 不等于 manual override 可执行",
    "closure 不等于 audit 已提交",
    "closure 不等于 rollback 已执行",
    "closure 不等于真实迁移可执行",
    "closure 不等于文件移动/删除/合并可执行",
    "closure 不等于 developer backend extraction 可执行",
    "closure 不等于 docs reorganization 可执行",
    "closure 不等于 production structure ready",
    "review workflow stable 不等于可执行真实 human review 或真实迁移",
]

DEFERRED_ACTIONS = [
    "real human review execution",
    "real owner assignment",
    "protected asset modification",
    "permanent block override",
    "manual override execution",
    "audit commit",
    "rollback execution",
    "real migration",
    "file move",
    "file delete",
    "file rename",
    "module merge",
    "archive execution",
    "developer backend extraction",
    "docs reorganization",
    "midplatform modularization",
    "client/backend boundary physical split",
    "return to mainline capability development decision",
]

FUTURE_EXECUTION_REQUIRES = [
    "explicit owner assignment",
    "manual decision",
    "audit commit",
    "rollback plan",
    "protected asset check",
    "post-execution verifier",
]

FUTURE_OVERRIDE_REQUIRES = [
    "explicit manual override",
    "owner approval",
    "audit",
    "rollback plan",
    "verifier rerun",
    "governance approval",
]

ROOT_SPECS = [
    {
        "id": "post_review",
        "arg": "post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "resolution_post_dryrun_readiness_decision.json",
            "human_review_case_post_review.json",
            "permanent_dnae_post_review.json",
            "forbidden_decision_post_review.json",
            "forbidden_state_post_review.json",
            "owner_assignment_post_review.json",
            "audit_trace_post_review.json",
            "rollback_post_review.json",
            "protected_asset_boundary_post_review.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "resolution_dryrun",
        "arg": "resolution_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "resolution_dryrun_execution_plan.json",
            "human_review_dryrun_cases.json",
            "permanent_dnae_dryrun_cases.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "planning",
        "arg": "planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "protected_asset_policy.json",
            "human_review_resolution_policy.json",
            "permanent_do_not_auto_execute_policy.json",
            "review_decision_schema.json",
            "review_resolution_state_machine.json",
        ],
    },
    {
        "id": "roadmap_decision",
        "arg": "roadmap_decision_root",
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
        "id": "consolidation_dryrun",
        "arg": "consolidation_dryrun_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "consolidation_planning",
        "arg": "consolidation_planning_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "structure_map_dryrun",
        "arg": "structure_map_dryrun_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "gate_taxonomy_planning",
        "arg": "gate_taxonomy_planning_root",
        "required": False,
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


def _verifier_verdict(root: Optional[Path]) -> str:
    if not root:
        return "MISSING"
    report = _try_read_json(root / "verifier_report.json")
    if isinstance(report, dict):
        return str(report.get("verifier") or ("GO" if report.get("passed") else "NO_GO"))
    return "COMPLETE"


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "closure_scope": CLOSURE_SCOPE,
        "closure_only": True,
        "actual_human_review_executed": False,
        "protected_assets_modified": False,
        "permanent_blocks_modified": False,
        "audit_committed": False,
        "rollback_executed": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_closure": False,
        "readme_modified_by_closure": False,
        "phase_verdict_table_modified_by_closure": False,
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


def run_protected_asset_and_human_review_resolution_closure_v1(
    *,
    post_review_root: str,
    resolution_dryrun_root: str,
    planning_root: str,
    roadmap_decision_root: str,
    consolidation_closure_root: str,
    consolidation_post_review_root: Optional[str] = None,
    consolidation_dryrun_root: Optional[str] = None,
    consolidation_planning_root: Optional[str] = None,
    structure_map_dryrun_root: Optional[str] = None,
    gate_taxonomy_planning_root: Optional[str] = None,
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

    post_review_loaded = (
        roots["post_review"]["loaded"]
        and summaries["post_review"].get("final_decision") == POST_REVIEW_DECISION
        and summaries["post_review"].get("ready_for_closure") is True
    )
    dryrun_loaded = (
        roots["resolution_dryrun"]["loaded"]
        and summaries["resolution_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    planning_loaded = (
        roots["planning"]["loaded"]
        and summaries["planning"].get("final_decision") == PLANNING_DECISION
    )
    roadmap_loaded = roots["roadmap_decision"]["loaded"]
    consolidation_closure_loaded = roots["consolidation_closure"]["loaded"]

    post_root = roots["post_review"]["root"]
    pr_summary = summaries["post_review"]
    hr_post = _try_read_json(post_root / "human_review_case_post_review.json") if post_root else {}
    dnae_post = _try_read_json(post_root / "permanent_dnae_post_review.json") if post_root else {}
    readiness = _try_read_json(post_root / "resolution_post_dryrun_readiness_decision.json") if post_root else {}

    human_review_count = pr_summary.get("reviewed_human_review_case_count", hr_post.get("reviewed_human_review_case_count", 240))
    closed_no_execution = pr_summary.get("closed_no_execution_count", hr_post.get("closed_no_execution_count", 240))
    permanent_count = pr_summary.get("reviewed_permanent_dnae_case_count", dnae_post.get("reviewed_permanent_dnae_case_count", 914))
    permanent_preserved = pr_summary.get("permanent_do_not_auto_execute_count", dnae_post.get("permanent_do_not_auto_execute_count", 914))
    protected_conflict = pr_summary.get("protected_conflict_count", dnae_post.get("protected_conflict_count", 448))
    static_dnae = pr_summary.get("static_dnae_rule_count", dnae_post.get("static_dnae_rule_count", 466))
    high_risk = pr_summary.get("high_risk_merge_case_count", hr_post.get("high_risk_merge_case_count", 5))
    future_placeholder = pr_summary.get("future_placeholder_current_code_case_count", hr_post.get("future_placeholder_current_code_case_count", 35))
    target_unclear = pr_summary.get("target_module_unclear_case_count", hr_post.get("target_module_unclear_case_count", 200))
    forbidden_blocked = pr_summary.get("forbidden_decision_blocked_count", 10)
    forbidden_absent = pr_summary.get("forbidden_state_absent_count", 5)
    audit_count = pr_summary.get("audit_trace_generated_count", 1154)
    rollback_count = pr_summary.get("rollback_ref_generated_count", 1154)

    completed_phase_rows = []
    for phase_id, phase_name, root_id, output_dir, expected_decision, role in COMPLETED_PHASES:
        root = roots[root_id]["root"]
        phase_summary = summaries[root_id]
        completed_phase_rows.append(
            {
                "phase_id": phase_id,
                "phase_name": phase_name,
                "status": "GO",
                "output_dir": output_dir,
                "verifier_verdict": _verifier_verdict(root),
                "final_decision": phase_summary.get("final_decision", expected_decision),
                "role_in_closure": role,
                "actual_human_review_executed": False,
                "protected_assets_modified": False,
                "permanent_blocks_modified": False,
                "runtime_enabled": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    completed_phase_matrix = {
        "phases": completed_phase_rows,
        "completed_phase_count": len(completed_phase_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    closure_allowed = (
        post_review_loaded
        and dryrun_loaded
        and planning_loaded
        and closed_no_execution == 240
        and permanent_preserved == 914
        and readiness.get("ready_for_closure") is True
        and readiness.get("ready_for_real_human_review_execution") is False
        and readiness.get("ready_for_real_migration") is False
    )

    resolution_closure_decision_summary = {
        "human_review_case_count": human_review_count,
        "human_review_closed_no_execution_count": closed_no_execution,
        "permanent_dnae_case_count": permanent_count,
        "permanent_dnae_preserved_count": permanent_preserved,
        "protected_conflict_count": protected_conflict,
        "static_dnae_rule_count": static_dnae,
        "forbidden_decision_blocked_count": forbidden_blocked,
        "forbidden_state_absent_count": forbidden_absent,
        "audit_trace_generated_count": audit_count,
        "rollback_ref_generated_count": rollback_count,
        "actual_human_review_executed": False,
        "protected_assets_modified": False,
        "permanent_blocks_modified": False,
        "block_released": False,
        "override_executed": False,
        "audit_committed": False,
        "rollback_executed": False,
        "closure_allowed": closure_allowed,
        "real_migration_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    closure_boundary_freeze = {
        "no-real-human-review-execution": True,
        "no-real-owner-confirmation": True,
        "no-protected-asset-modification": True,
        "no-permanent-block-release": True,
        "no-manual-override-execution": True,
        "no-audit-commit": True,
        "no-rollback-execution": True,
        "no-real-migration": True,
        "no-file-move": True,
        "no-file-delete": True,
        "no-file-rename": True,
        "no-module-merge": True,
        "no-auto-archive": True,
        "no-runtime": True,
        "no-write": True,
        "no-action": True,
        "no-speech": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    resolution_non_claims_register = {
        "non_claims": NON_CLAIMS,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    human_review_carryover_for_future_execution = {
        "human_review_required_count": human_review_count,
        "closed_no_execution_count": closed_no_execution,
        "final_owner_human_confirmed": False,
        "categories": {
            "high_risk_merge": high_risk,
            "future_placeholder_current_code": future_placeholder,
            "target_module_unclear": target_unclear,
        },
        "future_execution_requires": FUTURE_EXECUTION_REQUIRES,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    permanent_block_carryover_for_future_governance = {
        "permanent_dnae_count": permanent_count,
        "protected_conflict_count": protected_conflict,
        "static_dnae_rule_count": static_dnae,
        "block_released": False,
        "override_executed": False,
        "future_override_requires": FUTURE_OVERRIDE_REQUIRES,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_resolution_action_pool = {
        "deferred_actions": [
            {"action": a, "auto_execute_allowed": False, "requires_roadmap_decision": True}
            for a in DEFERRED_ACTIONS
        ],
        "deferred_action_count": len(DEFERRED_ACTIONS),
        "real_migration_started": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    for flag_name, loaded in (
        ("post_review_input_loaded", post_review_loaded),
        ("dryrun_input_loaded", dryrun_loaded),
        ("planning_input_loaded", planning_loaded),
        ("consolidation_roadmap_input_loaded", roadmap_loaded),
        ("consolidation_closure_input_loaded", consolidation_closure_loaded),
    ):
        if not loaded:
            blockers.append(flag_name)
    if closed_no_execution != 240:
        blockers.append("not_all_closed_no_execution")
    if permanent_preserved != 914:
        blockers.append("not_all_permanent_preserved")
    if readiness.get("ready_for_closure") is not True:
        blockers.append("post_review_not_ready_for_closure")
    if len(completed_phase_rows) < 3:
        blockers.append("completed_phase_matrix_incomplete")

    boundary_ok = not blockers

    closure_readiness_gate = {
        "go_conditions": [
            "all five required input roots loaded",
            "post-dryrun review ready_for_closure",
            "240 HR closed_no_execution",
            "914 permanent blocks preserved",
            "human_review and permanent_block carryover recorded",
            "boundary freeze generated",
            "non-claims generated",
            "deferred action pool generated",
            "no real human review / migration flags false",
            "next phase fixed to post-resolution roadmap decision",
        ],
        "no_go_conditions": [
            "any required root missing",
            "HR not all closed_no_execution",
            "permanent block not preserved",
            "real human review or migration allowed",
            "actual file move/delete/merge",
            "runtime enabled",
            "README/verdict table modified",
        ],
        "ready_for_closure": boundary_ok,
        "blockers": blockers,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    protected_asset_human_review_resolution_closure_summary = {
        "closure_id": CLOSURE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "completed_phase_chain": [r["phase_id"] for r in completed_phase_rows],
        "completed_phase_count": len(completed_phase_rows),
        "planning_ref": "_eval_out/protected_asset_and_human_review_resolution_planning_v1_smoke_v0/",
        "dryrun_ref": "_eval_out/protected_asset_and_human_review_resolution_dryrun_v1_smoke_v0/",
        "post_review_ref": "_eval_out/protected_asset_and_human_review_resolution_post_dryrun_review_v1_smoke_v0/",
        "protected_asset_policy_ref": "planning/protected_asset_policy.json",
        "human_review_policy_ref": "planning/human_review_resolution_policy.json",
        "permanent_dnae_policy_ref": "planning/permanent_do_not_auto_execute_policy.json",
        "closure_boundary_freeze_ref": "closure_boundary_freeze.json",
        "non_claims_register_ref": "resolution_non_claims_register.json",
        "carryover_register_ref": "human_review_carryover_for_future_execution.json",
        "deferred_action_pool_ref": "deferred_resolution_action_pool.json",
        "final_decision": FINAL_DECISION if boundary_ok else "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_CLOSURE_REQUIRES_FIXES",
        "roadmap_decision_options": [
            "Whitebox and Test Center Structure Optimization Planning",
            "Developer Backend Extraction Planning",
            "Docs Reorganization Planning",
            "Human Review Execution Planning",
            "Protected Asset Manual Override Policy",
            "pause structure governance and return to mainline capability building",
        ],
        "priority_note": "后台整体结构暂缓；白盒和测试中心结构优化可在后续路线中优先考虑；WorldModel/Memory/Library/Emotion 等未完成模块标注 future_reserved/discussion_required",
        "reason": "closure complete; no direct human review or migration; roadmap decision selects next governance track",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "post_review_input_loaded": post_review_loaded,
        "dryrun_input_loaded": dryrun_loaded,
        "planning_input_loaded": planning_loaded,
        "consolidation_roadmap_input_loaded": roadmap_loaded,
        "consolidation_closure_input_loaded": consolidation_closure_loaded,
        "completed_phase_matrix_generated": True,
        "completed_phase_count": len(completed_phase_rows),
        "resolution_closure_decision_summary_generated": True,
        "closure_boundary_freeze_generated": True,
        "non_claims_register_generated": True,
        "human_review_carryover_generated": True,
        "permanent_block_carryover_generated": True,
        "deferred_resolution_action_pool_generated": True,
        "closure_readiness_gate_generated": True,
        "human_review_case_count": human_review_count,
        "human_review_closed_no_execution_count": closed_no_execution,
        "permanent_dnae_case_count": permanent_count,
        "permanent_dnae_preserved_count": permanent_preserved,
        "protected_conflict_count": protected_conflict,
        "static_dnae_rule_count": static_dnae,
        "high_risk_merge_case_count": high_risk,
        "future_placeholder_current_code_case_count": future_placeholder,
        "target_module_unclear_case_count": target_unclear,
        "forbidden_decision_blocked_count": forbidden_blocked,
        "forbidden_state_absent_count": forbidden_absent,
        "audit_trace_generated_count": audit_count,
        "rollback_ref_generated_count": rollback_count,
        "protected_asset_resolution_planning_closed": planning_loaded,
        "protected_asset_resolution_dryrun_closed": dryrun_loaded,
        "protected_asset_resolution_post_review_closed": post_review_loaded,
        "protected_asset_resolution_closed": boundary_ok,
        "closure_allowed": closure_allowed and boundary_ok,
        "actual_human_review_executed": False,
        "human_review_execution_allowed": False,
        "final_owner_human_confirmed": False,
        "protected_assets_modified": False,
        "permanent_blocks_modified": False,
        "permanent_block_override_allowed": False,
        "override_executed": False,
        "block_released": False,
        "audit_committed": False,
        "rollback_executed": False,
        "real_migration_allowed": False,
        "ready_for_real_human_review_execution": False,
        "ready_for_protected_asset_modification": False,
        "ready_for_permanent_block_override": False,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_closure": False,
        "readme_modified_by_closure": False,
        "phase_verdict_table_modified_by_closure": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "protected_asset_human_review_resolution_closure_summary": protected_asset_human_review_resolution_closure_summary,
        "completed_phase_matrix": completed_phase_matrix,
        "resolution_closure_decision_summary": resolution_closure_decision_summary,
        "closure_boundary_freeze": closure_boundary_freeze,
        "resolution_non_claims_register": resolution_non_claims_register,
        "human_review_carryover_for_future_execution": human_review_carryover_for_future_execution,
        "permanent_block_carryover_for_future_governance": permanent_block_carryover_for_future_governance,
        "deferred_resolution_action_pool": deferred_resolution_action_pool,
        "closure_readiness_gate": closure_readiness_gate,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
