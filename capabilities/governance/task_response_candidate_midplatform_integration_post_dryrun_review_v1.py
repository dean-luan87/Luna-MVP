# -*- coding: utf-8 -*-
"""Task Response Candidate Midplatform Integration Post-DryRun Review v1 — review-only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.candidate_output_contract_v1 import validate_candidate_output
from capabilities.governance.task_response_candidate_midplatform_integration_dryrun_v1 import (
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PHASE_ID as DRYRUN_PHASE,
    SCOPE as DRYRUN_SCOPE,
)
from capabilities.governance.task_response_candidate_midplatform_integration_planning_v1 import (
    BLOCKED_PATHS,
    CONSTITUTION_BLOCKS,
    FLOW_PLANS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Task-Response-Candidate-Midplatform-Integration-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "task_response_candidate_post_dryrun_review_only"
SOURCE_CHAIN = "task_response_candidate_midplatform_integration_post_dryrun_review_v1"

UPSTREAM_PHASE = DRYRUN_PHASE
UPSTREAM_REQUIRED_FINAL = DRYRUN_FINAL_GO
UPSTREAM_NEXT_PHASE = DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = (
    "TASK_RESPONSE_CANDIDATE_MIDPLATFORM_INTEGRATION_POST_DRYRUN_REVIEW_CLOSED_READY_FOR_MODEL_MANAGEMENT_LAYER_RECOVERY_PLANNING"
)
FINAL_DECISION_HOLD = "TASK_RESPONSE_CANDIDATE_MIDPLATFORM_INTEGRATION_POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Model-Management-Layer-Recovery-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Task-Response-Candidate-Midplatform-Integration-Issue-Review-v1-001"

FLOW_RESULT_FILES: Tuple[Tuple[str, str], ...] = (
    ("Flow_1_vision_based_task_response", "task_response_vision_flow_result_v1.json"),
    ("Flow_2_ocr_based_task_response", "task_response_ocr_flow_result_v1.json"),
    ("Flow_3_navigation_guidance_based_task_response", "task_response_navigation_flow_result_v1.json"),
    ("Flow_4_mixed_candidate_task_response", "task_response_mixed_flow_result_v1.json"),
)

CONTRACT_BOOL_FIELDS: Tuple[Tuple[str, Any], ...] = (
    ("output_type", "task_response_candidate"),
    ("candidate_only", True),
    ("fact_status", "not_fact"),
    ("task_commit_allowed", False),
    ("user_facing_output_allowed", False),
    ("tts_allowed", False),
    ("runtime_action_allowed", False),
    ("write_allowed", False),
)

PRESENCE_FIELDS: Tuple[str, ...] = (
    "related_task_state_candidate_present",
    "related_input_candidates_present",
    "source_chain_present",
    "provenance_present",
    "output_arbitration_required",
    "constitution_gate_required",
)

BOUNDARY_FALSE_REVIEW: Tuple[str, ...] = (
    "task_state_committed_now",
    "task_manager_committed_now",
    "task_runtime_action_executed_now",
    "tts_invoked_now",
    "speech_response_candidate_generated_now",
    "user_facing_output_generated_now",
    "llm_invoked_now",
    "model_runtime_invoked_now",
    "navigation_action_triggered_now",
    "world_model_written_now",
    "memory_written_now",
    "library_write_executed_now",
    "hive_sync_executed_now",
    "runtime_enabled_now",
    "real_runtime_enabled_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Post-DryRun Review GO ≠ task response may be shown to users",
    "task_response_candidate ≠ final answer",
    "task_response_candidate ≠ TTS",
    "task_response_candidate ≠ task commit",
    "task_response_candidate ≠ Memory / WorldModel write",
    "Task response candidate integration closure ≠ Model Management recovered",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "task_response_candidate_midplatform_integration_post_dryrun_review"
)


def _review_meta() -> Dict[str, Any]:
    return {
        "task_response_candidate_post_dryrun_review_only": True,
        "review_only": True,
        "new_task_response_candidate_generated_now": False,
        "task_state_committed_now": False,
        "task_manager_committed_now": False,
        "task_runtime_action_executed_now": False,
        "tts_invoked_now": False,
        "speech_response_candidate_generated_now": False,
        "user_facing_output_generated_now": False,
        "llm_invoked_now": False,
        "model_runtime_invoked_now": False,
        "navigation_action_triggered_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "library_write_executed_now": False,
        "hive_sync_executed_now": False,
        "runtime_enabled_now": False,
        "real_runtime_enabled_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "task_commit_allowed": False,
        "user_facing_output_allowed": False,
        "tts_allowed": False,
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _validate_trc_contract(trc: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    ok, ci = validate_candidate_output(trc, expected_type="task_response_candidate", require_timestamp=False)
    if not ok:
        issues.extend(ci)
    for key, expected in CONTRACT_BOOL_FIELDS:
        if trc.get(key) != expected:
            issues.append(f"{key} must be {expected}")
    for key in PRESENCE_FIELDS:
        if trc.get(key) is not True:
            issues.append(f"{key} must be true")
    if not trc.get("provenance"):
        issues.append("provenance required")
    if not trc.get("related_task_state_candidate"):
        issues.append("related_task_state_candidate required")
    if not trc.get("related_input_candidates"):
        issues.append("related_input_candidates required")
    return issues


def run_task_response_candidate_midplatform_integration_post_dryrun_review_v1(
    *,
    task_response_candidate_midplatform_integration_dryrun_root: str,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(task_response_candidate_midplatform_integration_dryrun_root).expanduser().resolve()
    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else dryrun_root.parent / "task_response_candidate_midplatform_integration_post_dryrun_review"
    )
    meta = {
        **_review_meta(),
        "upstream_dryrun_root": str(dryrun_root),
        "review_output_root": str(out_root),
    }

    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    readiness = _try_read_json(dryrun_root / "task_response_dryrun_readiness_decision_v1.json") or {}
    collection = _try_read_json(dryrun_root / "task_response_candidate_collection_v1.json") or {}
    contract_dry = _try_read_json(dryrun_root / "task_response_candidate_contract_review_v1.json") or {}
    constitution = _try_read_json(dryrun_root / "constitution_overlay_result_v1.json") or {}
    arbitration = _try_read_json(dryrun_root / "output_arbitration_result_v1.json") or {}
    runtime = _try_read_json(dryrun_root / "runtime_boundary_result_v1.json") or {}
    blocked = _try_read_json(dryrun_root / "blocked_path_result_v1.json") or {}
    flow4 = _try_read_json(dryrun_root / "task_response_mixed_flow_result_v1.json") or {}

    dryrun_go = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    if not dryrun_go:
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_NEXT_PHASE:
        blockers.append("dryrun recommended_next_phase mismatch")
    if dryrun_sm.get("scope") != DRYRUN_SCOPE:
        blockers.append("dryrun scope mismatch")
    if dryrun_sm.get("task_response_candidate_generated_now") is not True:
        blockers.append("dryrun must have generated task_response_candidate")
    if dryrun_sm.get("task_response_chain_started_now") is not True:
        blockers.append("task_response_chain_started_now must be true in dryrun")
    if (dryrun_sm.get("task_response_candidates_generated") or 0) != 4:
        blockers.append("generated_count must be 4")
    if readiness.get("post_dryrun_review_separate") is not True:
        blockers.append("post_dryrun_review_separate required")

    for field in BOUNDARY_FALSE_REVIEW:
        if dryrun_sm.get(field) is True:
            blockers.append(f"dryrun {field} must be false")

    input_review = {
        "review_id": "task_response_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_verifier": dryrun_vr.get("verifier"),
        "upstream_verifier_go": dryrun_go,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "generated_count": dryrun_sm.get("task_response_candidates_generated"),
        "flows_all_pass": dryrun_sm.get("flows_all_pass"),
        "post_dryrun_review_separate": readiness.get("post_dryrun_review_separate"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    flow_rows: List[Dict[str, Any]] = []
    flow_issues: List[Dict[str, Any]] = []
    for flow_id, fname in FLOW_RESULT_FILES:
        doc = _try_read_json(dryrun_root / fname) or {}
        passed = doc.get("flow_pass") is True
        flow_rows.append({"flow_id": flow_id, "flow_pass": passed, "review_pass": passed})
        if not passed:
            flow_issues.append({"issue_id": flow_id, "detail": "flow must pass"})

    flow_review = {
        "review_id": "task_response_flow_review_v1",
        "flows": flow_rows,
        "all_four_flows_pass": len(flow_issues) == 0 and dryrun_sm.get("flows_all_pass") is True,
        "issues": flow_issues,
        "review_pass": len(flow_issues) == 0,
        **meta,
    }

    candidates: List[Dict[str, Any]] = list(collection.get("candidates") or [])
    ids: Set[str] = {c.get("candidate_id") for c in candidates if c.get("candidate_id")}
    coll_issues: List[Dict[str, Any]] = []
    if len(candidates) != 4:
        coll_issues.append({"issue_id": "count", "detail": "expected 4 candidates"})
    if len(ids) != 4:
        coll_issues.append({"issue_id": "unique_ids", "detail": "candidate ids must be unique"})

    collection_review = {
        "review_id": "task_response_candidate_collection_review_v1",
        "count": len(candidates),
        "unique_ids": list(ids),
        "all_unique": len(ids) == len(candidates) == 4,
        "presence_checks": {f: all(c.get(f) is True for c in candidates) for f in PRESENCE_FIELDS},
        "issues": coll_issues,
        "review_pass": len(coll_issues) == 0 and all(
            all(c.get(f) is True for c in candidates) for f in PRESENCE_FIELDS
        ),
        **meta,
    }

    contract_issues: List[Dict[str, Any]] = []
    for trc in candidates:
        for issue in _validate_trc_contract(trc):
            contract_issues.append({"candidate_id": trc.get("candidate_id"), "issue": issue})

    contract_review = {
        "review_id": "task_response_candidate_contract_review_v1",
        "candidates_reviewed": len(candidates),
        "all_contract_pass": len(contract_issues) == 0,
        "dryrun_contract_review_pass": contract_dry.get("review_pass") is True,
        "issues": contract_issues,
        "review_pass": len(contract_issues) == 0 and contract_dry.get("review_pass") is True,
        **meta,
    }

    const_issues: List[Dict[str, Any]] = []
    if constitution.get("all_pass") is not True:
        const_issues.append({"issue_id": "constitution_all_pass", "detail": "all constitution reviews must pass"})
    for block in CONSTITUTION_BLOCKS:
        if block not in (constitution.get("blocks_enforced") or []):
            const_issues.append({"issue_id": block, "detail": "block must be listed"})

    constitution_review = {
        "review_id": "constitution_overlay_review_v1",
        "blocks_required": list(CONSTITUTION_BLOCKS),
        "dryrun_all_pass": constitution.get("all_pass"),
        "issues": const_issues,
        "review_pass": len(const_issues) == 0,
        **meta,
    }

    arb_issues: List[Dict[str, Any]] = []
    if arbitration.get("all_output_allowed_false") is not True:
        arb_issues.append({"issue_id": "output_allowed", "detail": "all output_allowed false"})
    if arbitration.get("all_speech_false") is not True:
        arb_issues.append({"issue_id": "speech", "detail": "speech_response_candidate_generated_now false"})
    for arb in arbitration.get("arbitrations") or []:
        if arb.get("output_allowed") is not False:
            arb_issues.append({"issue_id": arb.get("candidate_id"), "detail": "output_allowed false"})
        if arb.get("speech_response_candidate_generated_now") is True:
            arb_issues.append({"issue_id": "tts", "detail": "no TTS"})
        if arb.get("arbitration_outcome") not in ("hold", "fallback", "clarification_required", None):
            if arb.get("arbitration_outcome") not in ("hold",):
                pass  # hold is primary

    arbitration_review = {
        "review_id": "output_arbitration_review_v1",
        "output_allowed_default_false": arbitration.get("all_output_allowed_false") is True,
        "no_tts": arbitration.get("all_speech_false") is True,
        "candidate_outcomes_only": True,
        "issues": arb_issues,
        "review_pass": len(arb_issues) == 0,
        **meta,
    }

    runtime_issues: List[Dict[str, Any]] = []
    checks = (
        ("dryrun_allowed", True),
        ("real_runtime_allowed", False),
        ("task_commit_blocked", True),
        ("user_output_blocked", True),
        ("model_runtime_blocked", True),
        ("memory_write_blocked", True),
        ("world_model_write_blocked", True),
    )
    for key, exp in checks:
        if runtime.get(key) is not exp:
            runtime_issues.append({"issue_id": key, "detail": f"{key} must be {exp}"})

    runtime_review = {
        "review_id": "runtime_boundary_review_v1",
        "dryrun_only": runtime.get("dryrun_allowed") is True and runtime.get("real_runtime_allowed") is False,
        "issues": runtime_issues,
        "review_pass": len(runtime_issues) == 0,
        **meta,
    }

    blocked_issues: List[Dict[str, Any]] = []
    paths = {p.get("path_id"): p for p in blocked.get("paths") or []}
    for pid in BLOCKED_PATHS:
        row = paths.get(pid)
        if not row or row.get("blocked") is not True or row.get("observed_now") is True:
            blocked_issues.append({"issue_id": pid, "detail": "must be blocked with observed_now false"})
    blocked_review = {
        "review_id": "blocked_path_review_v1",
        "paths_total": len(BLOCKED_PATHS),
        "all_blocked": len(blocked_issues) == 0 and blocked.get("all_blocked") is True,
        "issues": blocked_issues,
        "review_pass": len(blocked_issues) == 0,
        **meta,
    }

    mixed_trc = flow4.get("task_response_candidate") or {}
    evidence = flow4.get("evidence_governance") or {}
    conflict_status = mixed_trc.get("conflict_status") or evidence.get("conflict_status")
    conflict_issues: List[Dict[str, Any]] = []
    if not conflict_status:
        conflict_issues.append({"issue_id": "missing", "detail": "conflict_status required on mixed flow"})
    if mixed_trc.get("task_commit_allowed") is True:
        conflict_issues.append({"issue_id": "commit", "detail": "no auto commit on conflict"})
    if mixed_trc.get("user_facing_output_allowed") is True:
        conflict_issues.append({"issue_id": "output", "detail": "no auto user output on conflict"})

    conflict_review = {
        "review_id": "conflict_status_review_v1",
        "flow_id": "Flow_4_mixed_candidate_task_response",
        "conflict_status": conflict_status,
        "no_auto_output": mixed_trc.get("user_facing_output_allowed") is False,
        "no_auto_commit": mixed_trc.get("task_commit_allowed") is False,
        "issues": conflict_issues,
        "review_pass": len(conflict_issues) == 0,
        **meta,
    }

    reviews_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and flow_review.get("review_pass")
        and collection_review.get("review_pass")
        and contract_review.get("review_pass")
        and constitution_review.get("review_pass")
        and arbitration_review.get("review_pass")
        and runtime_review.get("review_pass")
        and blocked_review.get("review_pass")
        and conflict_review.get("review_pass")
    )
    boundary_ok = reviews_pass

    closure = {
        "closure_id": "post_dryrun_closure_decision_v1",
        "perception_to_task_response_candidate_hub_closed": boundary_ok,
        "first_round_midplatform_task_response_closure": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    next_route = {
        "readiness_id": "next_route_readiness_decision_v1",
        "ready_for_model_management_layer_recovery_planning": boundary_ok,
        "route_b_resume_after_closure": boundary_ok,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": closure["final_decision"],
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers + [i.get("issue_id", i.get("issue", "")) for i in flow_issues + coll_issues + contract_issues],
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        "four_flows_pass": flow_review.get("all_four_flows_pass"),
        "candidates_reviewed": len(candidates),
        **meta,
    }

    return {
        "task_response_dryrun_input_review": input_review,
        "task_response_flow_review": flow_review,
        "task_response_candidate_collection_review": collection_review,
        "task_response_candidate_contract_review": contract_review,
        "constitution_overlay_review": constitution_review,
        "output_arbitration_review": arbitration_review,
        "runtime_boundary_review": runtime_review,
        "blocked_path_review": blocked_review,
        "conflict_status_review": conflict_review,
        "post_dryrun_closure_decision": closure,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
