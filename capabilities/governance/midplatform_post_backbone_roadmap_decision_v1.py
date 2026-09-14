# -*- coding: utf-8 -*-
"""Midplatform Post-Backbone Roadmap Decision v1 — route selection only, no implementation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_minimal_backbone_dryrun_v1 import BLOCK_CHECKS
from capabilities.governance.midplatform_minimal_backbone_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as POST_REVIEW_NEXT_PHASE,
    PHASE_ID as POST_REVIEW_PHASE,
    PREFERRED_ROUTE,
    ROUTE_OPTION_A,
    ROUTE_OPTION_B,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Post-Backbone-Roadmap-Decision-v1-001"
SCOPE = "midplatform_post_backbone_roadmap_decision_only"
SOURCE_CHAIN = "midplatform_post_backbone_roadmap_decision_v1"

UPSTREAM_REQUIRED_FINAL = POST_REVIEW_FINAL_GO
UPSTREAM_NEXT_PHASE = POST_REVIEW_NEXT_PHASE

FINAL_DECISION_GO = "MIDPLATFORM_POST_BACKBONE_ROADMAP_DECISION_READY_FOR_TASK_RESPONSE_CANDIDATE_INTEGRATION_PLANNING"
FINAL_DECISION_HOLD = "MIDPLATFORM_POST_BACKBONE_ROADMAP_DECISION_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Task-Response-Candidate-Midplatform-Integration-Planning-v1-001"

SELECTED_ROUTE = "Route A — Task response candidate Midplatform Integration"
DEFERRED_ROUTE = "Route B — Model Management Layer Recovery Planning"

ROUTE_A_FORBIDDEN: Tuple[str, ...] = (
    "task_commit",
    "task_manager_runtime_action",
    "tts",
    "user_facing_output",
    "memory_write",
    "world_model_write",
    "navigation_action",
    "model_runtime_invocation",
)

ROUTE_A_REASONS: Tuple[str, ...] = (
    "Minimal Backbone already consumes visual_observation_candidate / ocr_result_candidate / navigation_guidance_candidate",
    "Midplatform has dryrun skeleton: intake / evidence / constitution / guidance queue / arbitration / runtime boundary",
    "Next step validates organizing input candidates into task_response_candidate",
    "Moves midplatform from perception-candidate hub toward task-candidate hub",
)

ROUTE_B_DEFER_REASONS: Tuple[str, ...] = (
    "Model layer optimization depends on stable midplatform output chain",
    "task_response_candidate integration not yet completed",
    "Model outputs still lack task-response handoff if B runs first",
    "Route B starts after Task response candidate midplatform integration",
)

BOUNDARY_FALSE_FIELDS: Tuple[str, ...] = (
    "runtime_enabled_now",
    "task_state_committed_now",
    "task_manager_committed_now",
    "tts_invoked_now",
    "llm_invoked_now",
    "user_facing_output_generated_now",
    "navigation_action_triggered_now",
    "model_runtime_invoked_now",
    "world_model_written_now",
    "memory_written_now",
    "library_write_executed_now",
    "hive_sync_executed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Decision GO ≠ task_response_candidate implementation started",
    "Route A selected ≠ task commit or user-facing output allowed",
    "Route B deferred ≠ model management recovery planning started",
    "Integration planning next ≠ answering end users",
    "task_response_candidate must remain candidate_only and not_fact in planning",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_post_backbone_roadmap_decision"
)


def _not_fact() -> Dict[str, Any]:
    return {
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "task_commit_allowed": False,
        "user_facing_output_allowed": False,
        "tts_allowed": False,
    }


def _boundary_meta() -> Dict[str, Any]:
    return {
        "midplatform_post_backbone_roadmap_decision_only": True,
        "task_response_candidate_started_now": False,
        "model_management_recovery_started_now": False,
        "runtime_enabled_now": False,
        "task_state_committed_now": False,
        "task_manager_committed_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "user_facing_output_generated_now": False,
        "navigation_action_triggered_now": False,
        "model_runtime_invoked_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "library_write_executed_now": False,
        "hive_sync_executed_now": False,
        "task_response_candidate_chain_deferred_now": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_midplatform_post_backbone_roadmap_decision_v1(
    *,
    midplatform_minimal_backbone_post_dryrun_review_root: str,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    review_root = Path(midplatform_minimal_backbone_post_dryrun_review_root).expanduser().resolve()
    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else review_root.parent / "midplatform_post_backbone_roadmap_decision"
    )

    meta = {
        **_boundary_meta(),
        "upstream_post_dryrun_review_root": str(review_root),
        "output_root": str(out_root),
    }

    summary = _try_read_json(review_root / "summary.json") or {}
    vr = _try_read_json(review_root / "verifier_report.json") or {}
    next_route = _try_read_json(review_root / "next_route_readiness_decision_v1.json") or {}
    flow_review = _try_read_json(review_root / "flow_abc_review_v1.json") or {}
    blocked_review = _try_read_json(review_root / "blocked_path_review_v1.json") or {}
    dryrun_root = Path(summary.get("upstream_dryrun_root") or review_root.parent / "midplatform_minimal_backbone_dryrun")
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}

    verifier_go = vr.get("verifier") == "GO" and vr.get("passed") is True
    if not verifier_go:
        blockers.append("post-dryrun review verifier must be GO")
    if summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("post-review final_decision mismatch")
    if summary.get("recommended_next_phase") != UPSTREAM_NEXT_PHASE:
        blockers.append("post-review recommended_next_phase mismatch")
    if summary.get("three_candidate_flows_trusted") is not True:
        blockers.append("three_candidate_flows_trusted required")
    if summary.get("ten_blocks_all_blocked") is not True:
        blockers.append("ten_blocks_all_blocked required")
    if flow_review.get("flows_all_pass") is not True:
        blockers.append("Flow A/B/C must all pass")
    if blocked_review.get("all_ten_blocks_blocked") is not True:
        blockers.append("ten block checks must be blocked")
    if next_route.get("preferred_route") != PREFERRED_ROUTE:
        blockers.append("preferred_route must be A")
    if next_route.get("do_not_open_task_response_directly") is not True:
        blockers.append("do_not_open_task_response_directly must be true")
    if summary.get("task_response_candidate_chain_deferred_now") is not True:
        blockers.append("task_response_candidate must remain deferred")

    for field in BOUNDARY_FALSE_FIELDS:
        if summary.get(field) is True or dryrun_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    input_review = {
        "review_id": "minimal_backbone_post_review_input_review_v1",
        "upstream_root": str(review_root),
        "upstream_verifier": vr.get("verifier"),
        "upstream_verifier_go": verifier_go,
        "upstream_final_decision": summary.get("final_decision"),
        "upstream_recommended_next_phase": summary.get("recommended_next_phase"),
        "upstream_boundary_ok": summary.get("boundary_ok"),
        "three_candidate_flows_trusted": summary.get("three_candidate_flows_trusted"),
        "ten_blocks_all_blocked": summary.get("ten_blocks_all_blocked"),
        "minimal_backbone_dryrun_closed": summary.get("minimal_backbone_dryrun_closed"),
        "preferred_route": next_route.get("preferred_route"),
        "do_not_open_task_response_directly": next_route.get("do_not_open_task_response_directly"),
        "task_response_candidate_deferred": summary.get("task_response_candidate_chain_deferred_now"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_task_response_candidate_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_OPTION_A,
        "status": "selected",
        "selection_reasons": list(ROUTE_A_REASONS),
        "still_forbidden": list(ROUTE_A_FORBIDDEN),
        "target_candidate_type": "task_response_candidate",
        "planning_goal": "midplatform generates task_response_candidate without answering users",
        "required_invariants": {
            "candidate_only": True,
            "fact_status": "not_fact",
            "task_commit_allowed": False,
            "user_facing_output_allowed": False,
            "tts_allowed": False,
        },
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_model_management_recovery_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_OPTION_B,
        "status": "deferred",
        "defer_reasons": list(ROUTE_B_DEFER_REASONS),
        "resume_after": "Task response candidate midplatform integration planning and validation",
        **meta,
    }

    selection_matrix = {
        "matrix_id": "route_selection_matrix_v1",
        "routes": [
            {"route_id": "A", "label": SELECTED_ROUTE, "status": "selected", "score": "preferred"},
            {"route_id": "B", "label": DEFERRED_ROUTE, "status": "deferred", "score": "after_A"},
        ],
        "selected_route": SELECTED_ROUTE,
        "deferred_route": DEFERRED_ROUTE,
        "decision_basis": [
            "post-dryrun review GO",
            "three perception/guidance flows trusted",
            "ten blocks enforced",
            "user preference route A",
        ],
        **meta,
    }

    route_a_preconditions = {
        "preconditions_id": "route_a_execution_preconditions_v1",
        "route": SELECTED_ROUTE,
        "preconditions_met": input_review.get("review_pass") is True,
        "requires": [
            "post_dryrun_review GO",
            "roadmap decision selects A",
            "integration planning only next",
        ],
        "must_remain_false_until_later_phases": list(ROUTE_A_FORBIDDEN),
        "next_phase": NEXT_PHASE_GO,
        **meta,
    }

    route_b_defer = {
        "defer_id": "route_b_defer_reason_v1",
        "route": DEFERRED_ROUTE,
        "status": "deferred",
        "reasons": list(ROUTE_B_DEFER_REASONS),
        "earliest_resume_phase": ROUTE_OPTION_B,
        **meta,
    }

    decision_ok = input_review.get("review_pass") is True

    next_phase_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_task_response_integration_planning": decision_ok,
        "selected_route": SELECTED_ROUTE,
        "deferred_route": DEFERRED_ROUTE,
        "recommended_next_phase": NEXT_PHASE_GO if decision_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if decision_ok else FINAL_DECISION_HOLD,
        "task_response_candidate_still_deferred_until_planning": True,
        **meta,
    }

    policy = {
        "policy_id": "post_backbone_roadmap_decision_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "principles": [
            "decision_only_no_implementation",
            "route_A_selected_route_B_deferred",
            "no_runtime_no_commit",
        ],
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary_out = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": decision_ok,
        "violations": blockers,
        "final_decision": next_phase_readiness["final_decision"],
        "recommended_next_phase": next_phase_readiness["recommended_next_phase"],
        "selected_route": SELECTED_ROUTE,
        "deferred_route": DEFERRED_ROUTE,
        "high_risk_count": 0 if decision_ok else 1,
        **meta,
    }

    return {
        "post_backbone_roadmap_decision_policy": policy,
        "minimal_backbone_post_review_input_review": input_review,
        "route_a_task_response_candidate_assessment": route_a,
        "route_b_model_management_recovery_assessment": route_b,
        "route_selection_matrix": selection_matrix,
        "route_a_execution_preconditions": route_a_preconditions,
        "route_b_defer_reason": route_b_defer,
        "next_phase_readiness_decision": next_phase_readiness,
        "non_claims_register": non_claims,
        "summary": summary_out,
    }
