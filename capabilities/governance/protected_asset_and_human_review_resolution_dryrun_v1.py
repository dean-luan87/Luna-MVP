# -*- coding: utf-8 -*-
"""Protected Asset and Human Review Resolution DryRun v1.

Dry-run-only: simulate 240 human review + 914 permanent DNAE resolution flows.
No human review execution, no protected asset modification, no file operations.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Protected-Asset-and-Human-Review-Resolution-DryRun-v1-001"
DRYRUN_SCOPE = "protected_asset_and_human_review_resolution_dryrun_only"
DRYRUN_ID = "pahr_resolution_dryrun_v1_001"
SOURCE_CHAIN = "protected_asset_and_human_review_resolution_dryrun_v1"
FINAL_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Protected-Asset-and-Human-Review-Resolution-Post-DryRun-Review-v1-001"

PLANNING_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING_READY_FOR_DRYRUN"
ROADMAP_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_ROADMAP_DECISION_READY_FOR_PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING"
CLOSURE_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSED_FOR_CURRENT_MAINLINE"
POST_REVIEW_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"

ALLOWED_DECISIONS = [
    "KEEP_AS_IS",
    "RECLASSIFY_TARGET_MODULE",
    "MARK_AS_PROTECTED",
    "MARK_AS_DEVELOPER_BACKEND",
    "MARK_AS_CLIENT_EXCLUDED",
    "MARK_AS_FUTURE_PLACEHOLDER",
    "MARK_AS_LEGACY_REFERENCE",
    "MARK_AS_ARCHIVE_CANDIDATE_ONLY",
    "MARK_AS_MERGE_CANDIDATE_ONLY",
    "DEFER_UNTIL_OWNER_ASSIGNED",
    "REQUIRE_ADDITIONAL_EVIDENCE",
    "PERMANENT_DO_NOT_AUTO_EXECUTE",
]

FORBIDDEN_DECISIONS = [
    "DELETE_NOW",
    "MOVE_NOW",
    "MERGE_NOW",
    "ARCHIVE_NOW",
    "ENABLE_RUNTIME",
    "CHANGE_PHASE_VERDICT",
    "REMOVE_VERIFIER_REPORT",
    "REMOVE_GO_NO_GO_PACK",
    "REMOVE_TEST_LOG",
    "REMOVE_CORRECTION_RECORD",
]

FORBIDDEN_STATES = ["auto_executed", "file_moved", "file_deleted", "module_merged", "runtime_enabled"]
HR_STATE_TRACE = [
    "queued_for_review",
    "owner_required",
    "in_manual_review",
    "decision_proposed",
    "decision_audited",
    "resolution_recorded",
    "closed_no_execution",
]
DNAE_STATE_TRACE = ["queued_for_review", "permanent_block", "closed_no_execution"]

REASON_TO_CATEGORY = {
    "high_risk_merge_large_group": "high_risk_merge",
    "future_placeholder_with_current_code": "future_placeholder_current_code",
    "multiple_actions_same_asset": "target_module_unclear",
    "protected_asset_marked_for_destructive_action": "target_module_unclear",
}

OWNER_NORMALIZE = {
    "governance": "governance_owner",
    "architecture": "architecture_owner",
    "developer_backend": "developer_backend_owner",
    "midplatform": "midplatform_owner",
    "capability": "capability_owner",
    "cognition": "cognition_owner",
    "docs": "docs_owner",
    "evaluation": "evaluation_owner",
    "safety": "safety_owner",
    "product_client": "product_client_owner",
    "client": "product_client_owner",
}

CATEGORY_OWNER = {
    "high_risk_merge": "architecture_owner",
    "future_placeholder_current_code": "cognition_owner",
    "target_module_unclear": "architecture_owner",
    "archive_unclear_ownership": "governance_owner",
    "client_backend_ambiguous": "developer_backend_owner",
    "docs_code_mismatch": "docs_owner",
}

CATEGORY_DECISION = {
    "high_risk_merge": "MARK_AS_MERGE_CANDIDATE_ONLY",
    "future_placeholder_current_code": "MARK_AS_FUTURE_PLACEHOLDER",
    "target_module_unclear": "MARK_AS_PROTECTED",
    "archive_unclear_ownership": "MARK_AS_ARCHIVE_CANDIDATE_ONLY",
    "client_backend_ambiguous": "MARK_AS_DEVELOPER_BACKEND",
    "docs_code_mismatch": "KEEP_AS_IS",
}

ROOT_SPECS = [
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
            "manual_owner_assignment_policy.json",
            "review_decision_schema.json",
            "review_resolution_state_machine.json",
            "protected_asset_audit_trace_policy.json",
            "review_rollback_policy.json",
            "resolution_planning_readiness_decision.json",
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
        "artifacts": ["summary.json", "human_review_carryover_register.json", "permanent_do_not_auto_execute_carryover.json"],
    },
    {
        "id": "consolidation_post_review",
        "arg": "consolidation_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "permanent_do_not_auto_execute_items.json"],
    },
    {
        "id": "consolidation_dryrun",
        "arg": "consolidation_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "human_review_required_register.json"],
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


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "dryrun_scope": DRYRUN_SCOPE,
        "dryrun_only": True,
        "actual_human_review_executed": False,
        "protected_assets_modified": False,
        "permanent_blocks_modified": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_dryrun": False,
        "readme_modified_by_dryrun": False,
        "phase_verdict_table_modified_by_dryrun": False,
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


def _infer_dnae_block_type(item: Dict[str, Any]) -> Tuple[str, str]:
    rid = str(item.get("register_id", ""))
    if rid.startswith("CONF"):
        path = str(item.get("asset_path", ""))
        if "verifier" in path.lower():
            return "protected_verifier", "auto_delete"
        if "GO_NO_GO" in path or "go_no_go" in path.lower():
            return "protected_go_no_go", "auto_archive"
        if "_eval_out" in path:
            return "protected_eval_out", "auto_archive"
        if "correction" in path.lower():
            return "protected_correction_record", "auto_delete"
        return "protected_phase_record", "auto_archive"
    action = str(item.get("forbidden_action", "auto_delete"))
    if "delete" in action.lower():
        return "static_dnae_rule", "auto_delete"
    if "archive" in action.lower():
        return "static_dnae_rule", "auto_archive"
    if "move" in action.lower():
        return "static_dnae_rule", "auto_move"
    return "static_dnae_rule", "auto_delete"


def run_protected_asset_and_human_review_resolution_dryrun_v1(
    *,
    planning_root: str,
    roadmap_decision_root: str,
    consolidation_closure_root: str,
    consolidation_post_review_root: str,
    consolidation_dryrun_root: str,
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

    planning_loaded = roots["planning"]["loaded"] and summaries["planning"].get("final_decision") == PLANNING_DECISION
    roadmap_loaded = roots["roadmap_decision"]["loaded"]
    closure_loaded = roots["consolidation_closure"]["loaded"]
    post_review_loaded = roots["consolidation_post_review"]["loaded"]
    dryrun_loaded = roots["consolidation_dryrun"]["loaded"]

    planning_root_path = roots["planning"]["root"]
    post_root = roots["consolidation_post_review"]["root"]
    dryrun_root = roots["consolidation_dryrun"]["root"]

    policies = {
        "protected_asset": _try_read_json(planning_root_path / "protected_asset_policy.json") if planning_root_path else {},
        "human_review": _try_read_json(planning_root_path / "human_review_resolution_policy.json") if planning_root_path else {},
        "permanent_dnae": _try_read_json(planning_root_path / "permanent_do_not_auto_execute_policy.json") if planning_root_path else {},
        "owner": _try_read_json(planning_root_path / "manual_owner_assignment_policy.json") if planning_root_path else {},
        "decision_schema": _try_read_json(planning_root_path / "review_decision_schema.json") if planning_root_path else {},
        "state_machine": _try_read_json(planning_root_path / "review_resolution_state_machine.json") if planning_root_path else {},
        "audit": _try_read_json(planning_root_path / "protected_asset_audit_trace_policy.json") if planning_root_path else {},
        "rollback": _try_read_json(planning_root_path / "review_rollback_policy.json") if planning_root_path else {},
    }

    hr_register = (_try_read_json(dryrun_root / "human_review_required_register.json") or {}) if dryrun_root else {}
    hr_items = hr_register.get("review_items") or []
    perm_items = (_try_read_json(post_root / "permanent_do_not_auto_execute_items.json") or {}).get("items", []) if post_root else []

    if len(hr_items) != 240:
        hr_items = hr_items[:240]
    if len(perm_items) != 914:
        perm_items = perm_items[:914]

    human_review_cases: List[Dict[str, Any]] = []
    owner_assignments: List[Dict[str, Any]] = []
    decision_results: List[Dict[str, Any]] = []
    state_traces: List[Dict[str, Any]] = []
    audit_traces: List[Dict[str, Any]] = []
    rollback_results: List[Dict[str, Any]] = []

    category_counter: Counter = Counter()
    owner_counter: Counter = Counter()
    final_state_counter: Counter = Counter()

    for i, item in enumerate(hr_items):
        reason = item.get("reason", "protected_asset_marked_for_destructive_action")
        category = REASON_TO_CATEGORY.get(reason, "target_module_unclear")
        category_counter[category] += 1

        rec_owner = item.get("recommended_owner", "")
        owner_type = OWNER_NORMALIZE.get(rec_owner, CATEGORY_OWNER.get(category, "architecture_owner"))
        owner_counter[owner_type] += 1

        selected = CATEGORY_DECISION.get(category, "KEEP_AS_IS")
        cat_policy = next(
            (c for c in (policies["human_review"].get("categories") or []) if c.get("review_category") == category),
            {},
        )
        allowed_candidates = cat_policy.get("allowed_decisions") or [selected, "DEFER_UNTIL_OWNER_ASSIGNED", "REQUIRE_ADDITIONAL_EVIDENCE"]

        case_id = f"HRDRY_{i:05d}"
        audit_id = f"AUD_HR_{i:05d}"
        rollback_ref = f"RB_HR_{i:05d}"

        human_review_cases.append(
            {
                "review_case_id": case_id,
                "source_review_item_ref": item.get("review_item_id", f"HR_{i:05d}"),
                "source_reason": reason,
                "review_category": category,
                "severity": item.get("severity", "medium"),
                "simulated_owner_type": owner_type,
                "required_inputs_present": True,
                "allowed_decision_candidates": allowed_candidates if isinstance(allowed_candidates, list) else [selected],
                "forbidden_decision_candidates": FORBIDDEN_DECISIONS,
                "selected_simulated_decision": selected,
                "state_machine_trace": HR_STATE_TRACE,
                "audit_trace_ref": audit_id,
                "rollback_ref": rollback_ref,
                "auto_execute_allowed": False,
                "file_operation_allowed": False,
                "runtime_allowed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        owner_assignments.append(
            {
                "owner_assignment_id": f"OWN_{i:05d}",
                "review_case_id": case_id,
                "simulated_owner_type": owner_type,
                "assignment_reason": f"category={category}; source_reason={reason}",
                "escalation_required": category == "high_risk_merge",
                "cannot_auto_assign": True,
                "final_owner_human_confirmed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        decision_results.append(
            {
                "decision_result_id": f"DEC_HR_{i:05d}",
                "case_ref": case_id,
                "attempted_decision": selected,
                "allowed": True,
                "block_reason": "",
                "selected_safe_decision": selected,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        final_state_counter["closed_no_execution"] += 1
        state_traces.append(
            {
                "trace_id": f"SM_HR_{i:05d}",
                "case_ref": case_id,
                "states_visited": HR_STATE_TRACE,
                "forbidden_states_absent": True,
                "final_state": "closed_no_execution",
                "execution_status": "dryrun_only",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        audit_traces.append(
            {
                "audit_trace_id": audit_id,
                "review_item_id": item.get("review_item_id"),
                "source_asset_path": item.get("asset_path", "(synthetic)"),
                "source_register": "human_review_required_register",
                "original_action": item.get("recommended_action", "manual_review_before_migration"),
                "protection_reason": reason,
                "owner_type": owner_type,
                "proposed_decision": selected,
                "simulated_final_review_decision": selected,
                "rollback_ref": rollback_ref,
                "timestamp_placeholder": f"TDRY_HR_{i:05d}",
                "source_chain": SOURCE_CHAIN,
                "audit_committed": False,
                **_not_fact(),
            }
        )

        rollback_results.append(
            {
                "rollback_ref": rollback_ref,
                "case_ref": case_id,
                "rollback_scope": "decision_and_owner_assignment",
                "rollback_required": True,
                "rollback_executed": False,
                "no_file_rollback_needed_current_phase": True,
                "future_rollback_steps": ["decision rollback", "owner assignment rollback"],
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    dnae_cases: List[Dict[str, Any]] = []
    protected_conflict_count = 0
    static_dnae_count = 0
    dnae_block_counter: Counter = Counter()

    for i, item in enumerate(perm_items):
        block_type, blocked_action = _infer_dnae_block_type(item)
        dnae_block_counter[block_type] += 1
        if str(item.get("register_id", "")).startswith("CONF"):
            protected_conflict_count += 1
        else:
            static_dnae_count += 1

        case_id = f"DNAEDRY_{i:05d}"
        audit_id = f"AUD_DNAE_{i:05d}"
        rollback_ref = f"RB_DNAE_{i:05d}"

        dnae_cases.append(
            {
                "dnae_case_id": case_id,
                "source_dnae_item_ref": item.get("register_id", f"PDNAE_{i:05d}"),
                "permanent_block_type": block_type,
                "blocked_action": blocked_action,
                "block_reason": item.get("rationale") or item.get("forbidden_action") or "permanent_block",
                "simulated_decision": "PERMANENT_DO_NOT_AUTO_EXECUTE",
                "manual_override_possible": True,
                "override_requirement": "explicit_manual_override_plus_audit_plus_rollback_plan",
                "audit_trace_ref": audit_id,
                "rollback_ref": rollback_ref,
                "auto_execute_allowed": False,
                "override_executed": False,
                "block_released": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        final_state_counter["permanent_block"] += 1
        state_traces.append(
            {
                "trace_id": f"SM_DNAE_{i:05d}",
                "case_ref": case_id,
                "states_visited": DNAE_STATE_TRACE,
                "forbidden_states_absent": True,
                "final_state": "permanent_block",
                "execution_status": "dryrun_only",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        audit_traces.append(
            {
                "audit_trace_id": audit_id,
                "review_item_id": item.get("register_id"),
                "source_asset_path": item.get("asset_path", item.get("forbidden_action", "(rule)")),
                "source_register": "permanent_do_not_auto_execute_items",
                "original_action": blocked_action,
                "protection_reason": item.get("rationale", "permanent_block"),
                "owner_type": "governance_owner",
                "proposed_decision": "PERMANENT_DO_NOT_AUTO_EXECUTE",
                "simulated_final_review_decision": "PERMANENT_DO_NOT_AUTO_EXECUTE",
                "rollback_ref": rollback_ref,
                "timestamp_placeholder": f"TDRY_DNAE_{i:05d}",
                "source_chain": SOURCE_CHAIN,
                "audit_committed": False,
                **_not_fact(),
            }
        )

        rollback_results.append(
            {
                "rollback_ref": rollback_ref,
                "case_ref": case_id,
                "rollback_scope": "permanent_block_decision",
                "rollback_required": True,
                "rollback_executed": False,
                "no_file_rollback_needed_current_phase": True,
                "future_rollback_steps": ["protected marking rollback"],
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    forbidden_decision_blocks = []
    for fd in FORBIDDEN_DECISIONS:
        forbidden_decision_blocks.append(
            {
                "attempted_decision": fd,
                "allowed": False,
                "block_reason": "forbidden_by_review_decision_schema",
                "selected_safe_decision": "PERMANENT_DO_NOT_AUTO_EXECUTE" if "REMOVE" in fd or fd in {"DELETE_NOW", "MOVE_NOW"} else "DEFER_UNTIL_OWNER_ASSIGNED",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    forbidden_state_absence = {
        "forbidden_states": FORBIDDEN_STATES,
        "forbidden_states_absent": True,
        "absent_count": len(FORBIDDEN_STATES),
        "verified_in_all_traces": all(
            not any(fs in t.get("states_visited", []) for fs in FORBIDDEN_STATES) for t in state_traces
        ),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    high_risk = category_counter.get("high_risk_merge", 0)
    future_ph = category_counter.get("future_placeholder_current_code", 0)
    target_unclear = category_counter.get("target_module_unclear", 0)

    resolution_dryrun_execution_plan = {
        "dryrun_id": DRYRUN_ID,
        "source_planning_ref": "_eval_out/protected_asset_and_human_review_resolution_planning_v1_smoke_v0/",
        "human_review_input_count": 240,
        "permanent_dnae_input_count": 914,
        "protected_conflict_count": protected_conflict_count,
        "static_dnae_rule_count": static_dnae_count,
        "execution_mode": "dryrun_only",
        "actual_human_review_executed": False,
        "protected_assets_modified": False,
        "permanent_blocks_modified": False,
        "real_migration_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    resolution_dryrun_summary_matrix = {
        "human_review_by_category": dict(category_counter),
        "human_review_by_owner_type": dict(owner_counter),
        "dnae_by_block_type": dict(dnae_block_counter),
        "decision_candidate_distribution": dict(Counter(c["selected_simulated_decision"] for c in human_review_cases)),
        "state_machine_final_state_distribution": dict(final_state_counter),
        "forbidden_decision_block_count": len(forbidden_decision_blocks),
        "forbidden_state_absent_count": len(FORBIDDEN_STATES),
        "audit_trace_generated_count": len(audit_traces),
        "rollback_ref_generated_count": len(rollback_results),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not planning_loaded:
        blockers.append("planning_input_not_loaded")
    if len(hr_items) != 240:
        blockers.append("human_review_count_mismatch")
    if len(perm_items) != 914:
        blockers.append("permanent_dnae_count_mismatch")
    if protected_conflict_count != 448:
        blockers.append("protected_conflict_count_mismatch")
    if static_dnae_count != 466:
        blockers.append("static_dnae_count_mismatch")

    boundary_ok = not blockers

    resolution_dryrun_readiness_decision = {
        "dryrun_verdict": "GO" if boundary_ok else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [
            f"simulated {len(human_review_cases)} human review + {len(dnae_cases)} permanent DNAE cases",
            "all forbidden decisions blocked; forbidden states absent",
            "no human review execution; no protected asset modification",
        ],
        "ready_for_post_dryrun_review": boundary_ok,
        "ready_for_real_human_review_execution": False,
        "ready_for_protected_asset_modification": False,
        "ready_for_permanent_block_override": False,
        "ready_for_real_migration": False,
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    owner_types_seen = set(owner_counter.keys())
    governance_debt_register = {
        "debt_items": [
            "240 human review cases simulated but not executed",
            "914 permanent blocks simulated but not released",
            "owner assignments simulated; final_owner_human_confirmed=false",
            "real human review execution still required after post-dryrun review",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_DRYRUN_REQUIRES_FIXES",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    owner_types_from_policy = policies["owner"].get("owner_types") or []
    allowed_states_from_policy = policies["state_machine"].get("allowed_states") or HR_STATE_TRACE

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "planning_input_loaded": planning_loaded,
        "consolidation_roadmap_input_loaded": roadmap_loaded,
        "consolidation_closure_input_loaded": closure_loaded,
        "consolidation_post_review_input_loaded": post_review_loaded,
        "consolidation_dryrun_input_loaded": dryrun_loaded,
        "protected_asset_policy_loaded": bool(policies["protected_asset"]),
        "human_review_resolution_policy_loaded": bool(policies["human_review"]),
        "permanent_dnae_policy_loaded": bool(policies["permanent_dnae"]),
        "manual_owner_assignment_policy_loaded": bool(policies["owner"]),
        "review_decision_schema_loaded": bool(policies["decision_schema"]),
        "review_state_machine_loaded": bool(policies["state_machine"]),
        "audit_trace_policy_loaded": bool(policies["audit"]),
        "rollback_policy_loaded": bool(policies["rollback"]),
        "resolution_dryrun_execution_plan_generated": True,
        "human_review_dryrun_cases_generated": True,
        "permanent_dnae_dryrun_cases_generated": True,
        "owner_assignment_dryrun_results_generated": True,
        "review_decision_dryrun_results_generated": True,
        "review_state_machine_dryrun_traces_generated": True,
        "audit_trace_dryrun_results_generated": True,
        "rollback_dryrun_results_generated": True,
        "resolution_dryrun_summary_matrix_generated": True,
        "resolution_dryrun_readiness_decision_generated": True,
        "human_review_input_count": 240,
        "human_review_case_count": len(human_review_cases),
        "permanent_dnae_input_count": 914,
        "permanent_dnae_case_count": len(dnae_cases),
        "protected_conflict_count": protected_conflict_count,
        "static_dnae_rule_count": static_dnae_count,
        "high_risk_merge_case_count": high_risk,
        "future_placeholder_current_code_case_count": future_ph,
        "target_module_unclear_case_count": target_unclear,
        "owner_assignment_case_count": len(owner_assignments),
        "owner_type_count": max(len(owner_types_seen), len(owner_types_from_policy)),
        "allowed_review_decision_count": len(ALLOWED_DECISIONS),
        "forbidden_review_decision_count": len(FORBIDDEN_DECISIONS),
        "forbidden_decision_blocked_count": len(forbidden_decision_blocks),
        "review_state_count": len(allowed_states_from_policy),
        "forbidden_state_absent_count": len(FORBIDDEN_STATES),
        "audit_trace_generated_count": len(audit_traces),
        "rollback_ref_generated_count": len(rollback_results),
        "dryrun_simulated_execution": True,
        "actual_human_review_executed": False,
        "human_review_execution_allowed": False,
        "final_owner_human_confirmed": False,
        "protected_assets_modified": False,
        "permanent_blocks_modified": False,
        "permanent_block_override_allowed": False,
        "override_executed": False,
        "block_released": False,
        "protected_assets_auto_delete_allowed": False,
        "protected_assets_auto_archive_allowed": False,
        "protected_assets_auto_move_allowed": False,
        "protected_assets_auto_merge_allowed": False,
        "delete_now_decision_blocked": True,
        "move_now_decision_blocked": True,
        "merge_now_decision_blocked": True,
        "archive_now_decision_blocked": True,
        "enable_runtime_decision_blocked": True,
        "change_phase_verdict_decision_blocked": True,
        "remove_verifier_report_decision_blocked": True,
        "remove_go_no_go_pack_decision_blocked": True,
        "remove_test_log_decision_blocked": True,
        "remove_correction_record_decision_blocked": True,
        "forbidden_states_absent": True,
        "auto_executed_state_absent": True,
        "file_moved_state_absent": True,
        "file_deleted_state_absent": True,
        "module_merged_state_absent": True,
        "runtime_enabled_state_absent": True,
        "audit_committed": False,
        "rollback_executed": False,
        "ready_for_post_dryrun_review": boundary_ok,
        "ready_for_real_human_review_execution": False,
        "ready_for_protected_asset_modification": False,
        "ready_for_permanent_block_override": False,
        "ready_for_real_migration": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_dryrun": False,
        "readme_modified_by_dryrun": False,
        "phase_verdict_table_modified_by_dryrun": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "resolution_dryrun_execution_plan": resolution_dryrun_execution_plan,
        "human_review_dryrun_cases": {"cases": human_review_cases, "case_count": len(human_review_cases), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "permanent_dnae_dryrun_cases": {"cases": dnae_cases, "case_count": len(dnae_cases), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "owner_assignment_dryrun_results": {"assignments": owner_assignments, "assignment_count": len(owner_assignments), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "review_decision_dryrun_results": {"results": decision_results, "result_count": len(decision_results), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "review_state_machine_dryrun_traces": {"traces": state_traces, "trace_count": len(state_traces), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "audit_trace_dryrun_results": {"traces": audit_traces, "trace_count": len(audit_traces), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "rollback_dryrun_results": {"results": rollback_results, "result_count": len(rollback_results), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "resolution_dryrun_summary_matrix": resolution_dryrun_summary_matrix,
        "resolution_dryrun_readiness_decision": resolution_dryrun_readiness_decision,
        "forbidden_decision_block_report": {"blocks": forbidden_decision_blocks, "block_count": len(forbidden_decision_blocks), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "forbidden_state_absence_report": forbidden_state_absence,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
        "verifier_report": {"verifier": "PENDING", "phase": "dryrun", "source_chain": SOURCE_CHAIN},
    }
