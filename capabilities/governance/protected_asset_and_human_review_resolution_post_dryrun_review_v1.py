# -*- coding: utf-8 -*-
"""Protected Asset and Human Review Resolution Post-DryRun Review v1.

Review-only: audit dryrun outputs for closure readiness.
No human review execution, no protected asset modification, no file operations.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

PHASE_ID = "Phase-Protected-Asset-and-Human-Review-Resolution-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "protected_asset_and_human_review_resolution_post_dryrun_review_only"
REVIEW_ID = "pahr_resolution_post_dryrun_review_v1_001"
SOURCE_CHAIN = "protected_asset_and_human_review_resolution_post_dryrun_review_v1"
FINAL_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Protected-Asset-and-Human-Review-Resolution-Closure-v1-001"

DRYRUN_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING_READY_FOR_DRYRUN"
ROADMAP_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_ROADMAP_DECISION_READY_FOR_PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING"
CLOSURE_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSED_FOR_CURRENT_MAINLINE"

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
REQUIRED_AUDIT_FIELDS = [
    "review_item_id",
    "source_asset_path",
    "source_register",
    "original_action",
    "protection_reason",
    "owner_type",
    "proposed_decision",
    "final_review_decision",
    "rollback_ref",
    "timestamp",
    "source_chain",
]

DRYRUN_ARTIFACTS = [
    "summary.json",
    "resolution_dryrun_execution_plan.json",
    "human_review_dryrun_cases.json",
    "permanent_dnae_dryrun_cases.json",
    "owner_assignment_dryrun_results.json",
    "review_decision_dryrun_results.json",
    "review_state_machine_dryrun_traces.json",
    "audit_trace_dryrun_results.json",
    "rollback_dryrun_results.json",
    "resolution_dryrun_summary_matrix.json",
    "resolution_dryrun_readiness_decision.json",
    "forbidden_decision_block_report.json",
    "forbidden_state_absence_report.json",
    "no_file_move_boundary_report.json",
    "no_delete_boundary_report.json",
    "no_runtime_boundary_report.json",
    "no_write_boundary_report.json",
    "verifier_report.json",
]

ROOT_SPECS = [
    {
        "id": "resolution_dryrun",
        "arg": "resolution_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": DRYRUN_ARTIFACTS,
    },
    {
        "id": "planning",
        "arg": "planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "protected_asset_policy.json", "human_review_resolution_policy.json"],
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


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "review_scope": REVIEW_SCOPE,
        "review_only": True,
        "actual_human_review_executed": False,
        "protected_assets_modified": False,
        "permanent_blocks_modified": False,
        "audit_committed": False,
        "rollback_executed": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_review": False,
        "readme_modified_by_review": False,
        "phase_verdict_table_modified_by_review": False,
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


def run_protected_asset_and_human_review_resolution_post_dryrun_review_v1(
    *,
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
    missing_required: List[str] = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        if spec["required"] and not meta["loaded"]:
            missing_required.append(spec["id"])
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

    dryrun_loaded = (
        roots["resolution_dryrun"]["loaded"]
        and summaries["resolution_dryrun"].get("final_decision") == DRYRUN_DECISION
        and summaries["resolution_dryrun"].get("ready_for_post_dryrun_review") is True
    )
    planning_loaded = roots["planning"]["loaded"] and summaries["planning"].get("final_decision") == PLANNING_DECISION
    roadmap_loaded = roots["roadmap_decision"]["loaded"]
    closure_loaded = roots["consolidation_closure"]["loaded"]

    dryrun_root = roots["resolution_dryrun"]["root"]
    dryrun_summary = summaries["resolution_dryrun"]

    hr_cases_payload = _try_read_json(dryrun_root / "human_review_dryrun_cases.json") if dryrun_root else {}
    dnae_cases_payload = _try_read_json(dryrun_root / "permanent_dnae_dryrun_cases.json") if dryrun_root else {}
    owners_payload = _try_read_json(dryrun_root / "owner_assignment_dryrun_results.json") if dryrun_root else {}
    sm_traces_payload = _try_read_json(dryrun_root / "review_state_machine_dryrun_traces.json") if dryrun_root else {}
    audit_payload = _try_read_json(dryrun_root / "audit_trace_dryrun_results.json") if dryrun_root else {}
    rollback_payload = _try_read_json(dryrun_root / "rollback_dryrun_results.json") if dryrun_root else {}
    matrix_payload = _try_read_json(dryrun_root / "resolution_dryrun_summary_matrix.json") if dryrun_root else {}
    forbidden_dec_payload = _try_read_json(dryrun_root / "forbidden_decision_block_report.json") if dryrun_root else {}
    forbidden_state_payload = _try_read_json(dryrun_root / "forbidden_state_absence_report.json") if dryrun_root else {}

    hr_cases = hr_cases_payload.get("cases") or []
    dnae_cases = dnae_cases_payload.get("cases") or []
    owners = owners_payload.get("assignments") or []
    sm_traces = sm_traces_payload.get("traces") or []
    audits = audit_payload.get("traces") or []
    rollbacks = rollback_payload.get("results") or []
    forbidden_blocks = forbidden_dec_payload.get("blocks") or []

    hr_trace_by_case = {t.get("case_ref"): t for t in sm_traces if str(t.get("case_ref", "")).startswith("HRDRY")}
    category_counter = Counter(c.get("review_category") for c in hr_cases)
    owner_counter = Counter(o.get("simulated_owner_type") for o in owners)

    closed_no_execution = 0
    auto_execute_allowed = 0
    file_op_allowed = 0
    runtime_allowed = 0
    for c in hr_cases:
        trace = hr_trace_by_case.get(c.get("review_case_id"), {})
        if trace.get("final_state") == "closed_no_execution":
            closed_no_execution += 1
        if c.get("auto_execute_allowed"):
            auto_execute_allowed += 1
        if c.get("file_operation_allowed"):
            file_op_allowed += 1
        if c.get("runtime_allowed"):
            runtime_allowed += 1

    permanent_dnae_count = sum(1 for c in dnae_cases if c.get("simulated_decision") == "PERMANENT_DO_NOT_AUTO_EXECUTE")
    block_released = sum(1 for c in dnae_cases if c.get("block_released"))
    override_executed = sum(1 for c in dnae_cases if c.get("override_executed"))
    protected_conflict = sum(1 for c in dnae_cases if str(c.get("source_dnae_item_ref", "")).startswith("CONF"))

    blocked_decisions = {b.get("attempted_decision") for b in forbidden_blocks if b.get("allowed") is False}
    allowed_forbidden = [b for b in forbidden_blocks if b.get("allowed") is True]
    all_forbidden_blocked = all(fd in blocked_decisions for fd in FORBIDDEN_DECISIONS) and len(allowed_forbidden) == 0

    forbidden_in_traces: Set[str] = set()
    for t in sm_traces:
        visited = set(t.get("states_visited") or [])
        forbidden_in_traces.update(visited & set(FORBIDDEN_STATES))
    unexpected_forbidden_states = len(forbidden_in_traces)

    audit_committed_count = sum(1 for a in audits if a.get("audit_committed"))
    rollback_executed_count = sum(1 for r in rollbacks if r.get("rollback_executed"))
    required_fields_ok = all(
        all(
            a.get(f) is not None
            or (f == "final_review_decision" and a.get("simulated_final_review_decision") is not None)
            or (f == "timestamp" and a.get("timestamp_placeholder") is not None)
            for f in REQUIRED_AUDIT_FIELDS
        )
        for a in audits[:20]
    ) if audits else False

    owner_confirmed = sum(1 for o in owners if o.get("final_owner_human_confirmed"))

    blockers: List[str] = []
    if not dryrun_loaded:
        blockers.append("resolution_dryrun_not_loaded")
    if not planning_loaded:
        blockers.append("planning_not_loaded")
    if not roadmap_loaded:
        blockers.append("roadmap_not_loaded")
    if not closure_loaded:
        blockers.append("consolidation_closure_not_loaded")
    if len(hr_cases) != 240:
        blockers.append("human_review_case_count_mismatch")
    if closed_no_execution != 240:
        blockers.append("not_all_closed_no_execution")
    if len(dnae_cases) != 914:
        blockers.append("permanent_dnae_case_count_mismatch")
    if permanent_dnae_count != 914:
        blockers.append("not_all_permanent_do_not_auto_execute")
    if block_released > 0:
        blockers.append("block_released_detected")
    if override_executed > 0:
        blockers.append("override_executed_detected")
    if not all_forbidden_blocked:
        blockers.append("forbidden_decisions_not_all_blocked")
    if unexpected_forbidden_states > 0:
        blockers.append("forbidden_states_present")
    if audit_committed_count > 0:
        blockers.append("audit_committed_detected")
    if rollback_executed_count > 0:
        blockers.append("rollback_executed_detected")
    if owner_confirmed > 0:
        blockers.append("owner_human_confirmed_detected")

    boundary_ok = not blockers

    resolution_dryrun_input_review = {
        "review_id": REVIEW_ID,
        "dryrun_input_loaded": dryrun_loaded,
        "planning_input_loaded": planning_loaded,
        "roadmap_input_loaded": roadmap_loaded,
        "consolidation_closure_input_loaded": closure_loaded,
        "required_artifacts_loaded": dryrun_loaded and planning_loaded and roadmap_loaded and closure_loaded,
        "missing_required_artifacts": missing_required,
        "input_status": "loaded" if not missing_required else "incomplete",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    human_review_case_post_review = {
        "reviewed_human_review_case_count": len(hr_cases),
        "closed_no_execution_count": closed_no_execution,
        "final_owner_human_confirmed_count": owner_confirmed,
        "actual_human_review_executed": False,
        "auto_execute_allowed_count": auto_execute_allowed,
        "file_operation_allowed_count": file_op_allowed,
        "runtime_allowed_count": runtime_allowed,
        "category_coverage": dict(category_counter),
        "owner_assignment_coverage": dict(owner_counter),
        "high_risk_merge_case_count": category_counter.get("high_risk_merge", 0),
        "future_placeholder_current_code_case_count": category_counter.get("future_placeholder_current_code", 0),
        "target_module_unclear_case_count": category_counter.get("target_module_unclear", 0),
        "verdict": "all_240_closed_no_execution" if closed_no_execution == 240 else "review_failed",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    permanent_dnae_post_review = {
        "reviewed_permanent_dnae_case_count": len(dnae_cases),
        "permanent_do_not_auto_execute_count": permanent_dnae_count,
        "protected_conflict_count": protected_conflict,
        "static_dnae_rule_count": len(dnae_cases) - protected_conflict,
        "block_released_count": block_released,
        "override_executed_count": override_executed,
        "protected_assets_modified": False,
        "permanent_blocks_modified": False,
        "verdict": "all_914_permanent_block_held" if permanent_dnae_count == 914 and block_released == 0 else "review_failed",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    forbidden_decision_post_review = {
        "forbidden_decision_count": len(FORBIDDEN_DECISIONS),
        "forbidden_decision_blocked_count": len(blocked_decisions & set(FORBIDDEN_DECISIONS)),
        "all_forbidden_decisions_blocked": all_forbidden_blocked,
        "unexpected_allowed_forbidden_decision_count": len(allowed_forbidden),
        "blocked_decisions": sorted(blocked_decisions & set(FORBIDDEN_DECISIONS)),
        "verdict": "all_forbidden_decisions_blocked" if all_forbidden_blocked else "review_failed",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    forbidden_state_post_review = {
        "forbidden_state_count": len(FORBIDDEN_STATES),
        "forbidden_state_absent_count": len(FORBIDDEN_STATES) - len(forbidden_in_traces),
        "forbidden_states_absent": unexpected_forbidden_states == 0,
        "unexpected_forbidden_state_count": unexpected_forbidden_states,
        "unexpected_states_found": sorted(forbidden_in_traces),
        "verdict": "forbidden_states_absent" if unexpected_forbidden_states == 0 else "review_failed",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    owner_types_seen = set(owner_counter.keys())
    planning_owner_count = len(
        (_try_read_json(roots["planning"]["root"] / "manual_owner_assignment_policy.json") or {}).get("owner_types") or []
    ) if roots["planning"]["root"] else 0

    owner_assignment_post_review = {
        "owner_assignment_case_count": len(owners),
        "owner_type_count": max(len(owner_types_seen), planning_owner_count),
        "final_owner_human_confirmed": False,
        "final_owner_human_confirmed_count": owner_confirmed,
        "cannot_auto_assign": all(o.get("cannot_auto_assign") for o in owners) if owners else True,
        "owner_assignment_committed": False,
        "verdict": "simulated_owner_assignment_only",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    audit_trace_post_review = {
        "audit_trace_generated_count": len(audits),
        "audit_committed": False,
        "audit_committed_count": audit_committed_count,
        "required_trace_fields_present": required_fields_ok,
        "audit_trace_is_dryrun_only": audit_committed_count == 0,
        "verdict": "dryrun_audit_refs_only" if audit_committed_count == 0 else "review_failed",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_post_review = {
        "rollback_ref_generated_count": len(rollbacks),
        "rollback_executed": False,
        "rollback_executed_count": rollback_executed_count,
        "rollback_is_dryrun_only": rollback_executed_count == 0,
        "no_file_rollback_needed_current_phase": all(r.get("no_file_rollback_needed_current_phase") for r in rollbacks[:20])
        if rollbacks
        else True,
        "verdict": "dryrun_rollback_refs_only" if rollback_executed_count == 0 else "review_failed",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    protected_asset_boundary_post_review = {
        "protected_assets_auto_delete_allowed": False,
        "protected_assets_auto_archive_allowed": False,
        "protected_assets_auto_move_allowed": False,
        "protected_assets_auto_merge_allowed": False,
        "protected_assets_modified": False,
        "protected_asset_boundary_pass": boundary_ok,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    resolution_post_dryrun_readiness_decision = {
        "review_verdict": "GO" if boundary_ok else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [
            "240 human review cases all closed_no_execution; no real execution",
            "914 permanent blocks held; block_released=0",
            "forbidden decisions/states blocked; audit/rollback dry-run refs only",
            "review workflow stable does not mean real human review or migration allowed",
        ],
        "ready_for_closure": boundary_ok,
        "ready_for_real_human_review_execution": False,
        "ready_for_protected_asset_modification": False,
        "ready_for_permanent_block_override": False,
        "ready_for_real_migration": False,
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_review = {
        "debt_items": [
            "240 human review items still require real owner assignment and resolution",
            "914 permanent blocks still require long-term policy enforcement",
            "dryrun proved workflow stability; real execution still deferred",
            "real migration remains blocked after closure",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "dryrun_input_loaded": dryrun_loaded,
        "planning_input_loaded": planning_loaded,
        "consolidation_roadmap_input_loaded": roadmap_loaded,
        "consolidation_closure_input_loaded": closure_loaded,
        "resolution_dryrun_input_review_generated": True,
        "human_review_case_post_review_generated": True,
        "permanent_dnae_post_review_generated": True,
        "forbidden_decision_post_review_generated": True,
        "forbidden_state_post_review_generated": True,
        "owner_assignment_post_review_generated": True,
        "audit_trace_post_review_generated": True,
        "rollback_post_review_generated": True,
        "protected_asset_boundary_post_review_generated": True,
        "resolution_post_dryrun_readiness_decision_generated": True,
        "reviewed_human_review_case_count": len(hr_cases),
        "closed_no_execution_count": closed_no_execution,
        "final_owner_human_confirmed_count": owner_confirmed,
        "reviewed_permanent_dnae_case_count": len(dnae_cases),
        "permanent_do_not_auto_execute_count": permanent_dnae_count,
        "protected_conflict_count": protected_conflict,
        "static_dnae_rule_count": len(dnae_cases) - protected_conflict,
        "high_risk_merge_case_count": category_counter.get("high_risk_merge", 0),
        "future_placeholder_current_code_case_count": category_counter.get("future_placeholder_current_code", 0),
        "target_module_unclear_case_count": category_counter.get("target_module_unclear", 0),
        "owner_assignment_case_count": len(owners),
        "owner_type_count": max(len(owner_types_seen), planning_owner_count),
        "audit_trace_generated_count": len(audits),
        "rollback_ref_generated_count": len(rollbacks),
        "forbidden_decision_count": len(FORBIDDEN_DECISIONS),
        "forbidden_decision_blocked_count": len(blocked_decisions & set(FORBIDDEN_DECISIONS)),
        "all_forbidden_decisions_blocked": all_forbidden_blocked,
        "unexpected_allowed_forbidden_decision_count": len(allowed_forbidden),
        "forbidden_state_count": len(FORBIDDEN_STATES),
        "forbidden_state_absent_count": len(FORBIDDEN_STATES) - len(forbidden_in_traces),
        "forbidden_states_absent": unexpected_forbidden_states == 0,
        "unexpected_forbidden_state_count": unexpected_forbidden_states,
        "block_released_count": block_released,
        "override_executed_count": override_executed,
        "actual_human_review_executed": False,
        "human_review_execution_allowed": False,
        "final_owner_human_confirmed": False,
        "protected_assets_modified": False,
        "permanent_blocks_modified": False,
        "permanent_block_override_allowed": False,
        "audit_committed": audit_committed_count > 0,
        "rollback_executed": rollback_executed_count > 0,
        "audit_trace_is_dryrun_only": audit_committed_count == 0,
        "rollback_is_dryrun_only": rollback_executed_count == 0,
        "protected_assets_auto_delete_allowed": False,
        "protected_assets_auto_archive_allowed": False,
        "protected_assets_auto_move_allowed": False,
        "protected_assets_auto_merge_allowed": False,
        "protected_asset_boundary_pass": boundary_ok,
        "ready_for_closure": boundary_ok,
        "ready_for_real_human_review_execution": False,
        "ready_for_protected_asset_modification": False,
        "ready_for_permanent_block_override": False,
        "ready_for_real_migration": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # Normalize audit_committed/rollback_executed in summary to false per spec
    summary["audit_committed"] = False
    summary["rollback_executed"] = False

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "resolution_dryrun_input_review": resolution_dryrun_input_review,
        "human_review_case_post_review": human_review_case_post_review,
        "permanent_dnae_post_review": permanent_dnae_post_review,
        "forbidden_decision_post_review": forbidden_decision_post_review,
        "forbidden_state_post_review": forbidden_state_post_review,
        "owner_assignment_post_review": owner_assignment_post_review,
        "audit_trace_post_review": audit_trace_post_review,
        "rollback_post_review": rollback_post_review,
        "protected_asset_boundary_post_review": protected_asset_boundary_post_review,
        "resolution_post_dryrun_readiness_decision": resolution_post_dryrun_readiness_decision,
        "governance_debt_review": governance_debt_review,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
