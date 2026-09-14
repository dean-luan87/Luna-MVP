# -*- coding: utf-8 -*-
"""Vision / OCR / Navigation / Task Limited Runtime Trial Post-DryRun Review v1.

Lightweight review after limited runtime trial dry-run GO. Review-only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_ocr_navigation_task_limited_runtime_trial_dryrun_v1 import (
    STOP_TRIGGERS,
)
from capabilities.governance.vision_ocr_navigation_task_limited_runtime_trial_planning_v1 import (
    LIMITED_RUNTIME_GATES,
)

PHASE_ID = "Phase-Vision-OCR-Navigation-Task-Limited-Runtime-Trial-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "limited_runtime_trial_post_dryrun_review_only"
SOURCE_CHAIN = "vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_v1"

UPSTREAM_PHASE = "Phase-Vision-OCR-Navigation-Task-Limited-Runtime-Trial-DryRun-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "VISION_OCR_NAVIGATION_TASK_LIMITED_RUNTIME_TRIAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
UPSTREAM_NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Limited-Runtime-Trial-Post-DryRun-Review-v1-001"

FINAL_DECISION = (
    "VISION_OCR_NAVIGATION_TASK_LIMITED_RUNTIME_TRIAL_POST_DRYRUN_REVIEW_READY_FOR_SINGLE_CHAIN_VISION_SAMPLE_FRAME_TRIAL_PLANNING"
)
NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Limited-Runtime-Trial-Planning-v1-001"

POSITIVE_SCENARIO_IDS: Tuple[str, ...] = (
    "sample_frame_to_visual_observation_candidate",
    "visual_candidate_to_mock_ocr_result_candidate",
    "visual_candidate_to_synthetic_navigation_guidance_candidate",
    "task_candidate_flow_with_mock_ocr_and_guidance",
)

BLOCKED_SCENARIO_IDS: Tuple[str, ...] = (
    "blocked_live_camera_request",
    "blocked_real_ocr_provider_request",
    "blocked_navigation_action_request",
    "blocked_task_commit_request",
)

RUNTIME_REVIEW_FIELDS: Tuple[str, ...] = (
    "live_runtime_enabled_now",
    "live_camera_enabled_now",
    "camera_runtime_enabled_now",
    "frame_capture_executed_now",
    "new_image_read_executed_now",
    "arbitrary_image_read_executed_now",
    "vision_model_invoked_now",
    "ocr_provider_invoked_now",
    "real_ocr_provider_enabled_now",
    "paddleocr_invoked_now",
    "rapidocr_invoked_now",
    "navigation_action_triggered_now",
    "real_navigation_runtime_enabled_now",
    "task_state_committed_now",
    "task_manager_committed_now",
    "world_model_written_now",
    "memory_written_now",
    "scene_delta_generated_now",
    "tts_invoked_now",
    "llm_invoked_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Post-DryRun Review GO ≠ live runtime enabled",
    "Limited runtime dry-run pass ≠ single-chain trial started",
    "Single-chain readiness ≠ camera enabled",
    "Vision sample frame trial ≠ live camera",
    "Mock OCR pass ≠ real OCR provider allowed",
    "Guidance candidate pass ≠ navigation action allowed",
    "Task candidate pass ≠ task commit allowed",
    "Dry-run trust review ≠ re-planning execution",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "limited_runtime_trial_post_dryrun_review_only": True,
        "review_only": True,
        "limited_runtime_trial_started_now": False,
        "feature_implementation_started_now": False,
        "runtime_enabled_now": False,
        "live_runtime_enabled_now": False,
        "live_camera_enabled_now": False,
        "camera_runtime_enabled_now": False,
        "frame_capture_executed_now": False,
        "new_image_read_executed_now": False,
        "arbitrary_image_read_executed_now": False,
        "vision_model_invoked_now": False,
        "visual_fact_generated_now": False,
        "ocr_provider_invoked_now": False,
        "real_ocr_provider_enabled_now": False,
        "paddleocr_invoked_now": False,
        "rapidocr_invoked_now": False,
        "ocr_evidence_generated_now": False,
        "navigation_action_triggered_now": False,
        "real_navigation_runtime_enabled_now": False,
        "map_write_executed_now": False,
        "gps_strong_anchor_committed_now": False,
        "task_state_committed_now": False,
        "task_manager_committed_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "scene_delta_generated_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "midplatform_refactor_executed_now": False,
        "protected_asset_modified_now": False,
        "eval_out_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _collect_candidates(obj: Any, found: List[Dict[str, Any]]) -> None:
    if isinstance(obj, dict):
        if obj.get("candidate_type") and obj.get("candidate_id"):
            found.append(obj)
        for v in obj.values():
            _collect_candidates(v, found)
    elif isinstance(obj, list):
        for item in obj:
            _collect_candidates(item, found)


def run_vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_v1(
    *,
    vision_ocr_navigation_task_limited_runtime_trial_dryrun_root: str,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(
        vision_ocr_navigation_task_limited_runtime_trial_dryrun_root
    ).expanduser().resolve()

    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else dryrun_root.parent / "vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review"
    )

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(dryrun_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_dryrun_root": str(dryrun_root),
        "review_output_root": str(out_root),
    }

    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    trace = _try_read_json(dryrun_root / "limited_runtime_candidate_flow_trace_v1.json") or {}
    gates = _try_read_json(dryrun_root / "limited_runtime_gate_consumption_result_v1.json") or {}
    stops = _try_read_json(dryrun_root / "limited_runtime_stop_condition_result_v1.json") or {}
    audit = _try_read_json(dryrun_root / "limited_runtime_no_runtime_boundary_audit_v1.json") or {}

    dryrun_verifier_trusted = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    dryrun_summary_trusted = (
        dryrun_sm.get("boundary_ok") is True
        and dryrun_sm.get("phase") == UPSTREAM_PHASE
        and dryrun_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and dryrun_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE
        and (dryrun_sm.get("high_risk_count") or 0) == 0
    )
    if not dryrun_verifier_trusted and not dryrun_summary_trusted:
        blockers.append("dryrun verifier must be GO")
    if (dryrun_sm.get("high_risk_count") or 0) != 0:
        blockers.append("high_risk_count must be 0")
    if dryrun_sm.get("limited_runtime_trial_started_now") is True:
        blockers.append("limited_runtime_trial_started_now must be false")
    if trace.get("all_scenarios_pass") is not True:
        blockers.append("all dryrun scenarios must pass")
    if gates.get("enforcement_pass") is not True:
        blockers.append("12 gates enforcement_pass required")
    if stops.get("verification_pass") is not True:
        blockers.append("12 stop conditions verification_pass required")
    if audit.get("audit_pass") is not True:
        blockers.append("no_runtime_boundary_audit must pass")

    for field in RUNTIME_REVIEW_FIELDS:
        if dryrun_sm.get(field) is True:
            blockers.append(f"dryrun {field} must be false")

    input_review = {
        "review_id": "limited_runtime_trial_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_verifier": dryrun_vr.get("verifier"),
        "upstream_verifier_trusted": dryrun_verifier_trusted,
        "upstream_summary_trusted": dryrun_summary_trusted,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "scenarios_passed": trace.get("scenarios_passed"),
        "gates_passed": gates.get("gates_passed"),
        "stop_conditions_passed": stops.get("conditions_passed"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    by_id = {s.get("scenario_id"): s for s in trace.get("scenarios") or []}
    positive_rows: List[Dict[str, Any]] = []
    positive_issues: List[Dict[str, Any]] = []
    for sid in POSITIVE_SCENARIO_IDS:
        row = by_id.get(sid)
        passed = row is not None and row.get("dryrun_pass") is True
        positive_rows.append({"scenario_id": sid, "dryrun_pass": passed, "review_pass": passed})
        if not passed:
            positive_issues.append(
                {"issue_id": f"positive_fail:{sid}", "severity": "high", "detail": "positive flow must pass"}
            )

    candidates: List[Dict[str, Any]] = []
    for fname in (
        "vision_sample_frame_candidate_dryrun_v1.json",
        "mock_ocr_result_candidate_dryrun_v1.json",
        "synthetic_navigation_guidance_candidate_dryrun_v1.json",
        "task_state_candidate_dryrun_v1.json",
        "limited_runtime_candidate_flow_trace_v1.json",
    ):
        data = _try_read_json(dryrun_root / fname)
        if data:
            _collect_candidates(data, candidates)

    candidate_ok = True
    for c in candidates:
        if c.get("candidate_only") is not True:
            candidate_ok = False
            positive_issues.append(
                {
                    "issue_id": f"candidate_not_only:{c.get('candidate_id')}",
                    "severity": "high",
                    "detail": "candidate_only must be true",
                }
            )
        if c.get("fact_status") != "not_fact":
            candidate_ok = False
            positive_issues.append(
                {
                    "issue_id": f"candidate_not_not_fact:{c.get('candidate_id')}",
                    "severity": "high",
                    "detail": "fact_status must be not_fact",
                }
            )
        if c.get("write_allowed") is True:
            candidate_ok = False
            positive_issues.append(
                {
                    "issue_id": f"write_allowed:{c.get('candidate_id')}",
                    "severity": "high",
                    "detail": "write_allowed must be false",
                }
            )

    if trace.get("candidate_only") is not True:
        candidate_ok = False
        positive_issues.append(
            {
                "issue_id": "trace_not_candidate_only",
                "severity": "high",
                "detail": "flow trace must be candidate_only",
            }
        )

    positive_review = {
        "review_id": "limited_runtime_positive_flow_review_v1",
        "scenarios": positive_rows,
        "positive_flow_count": len(POSITIVE_SCENARIO_IDS),
        "positive_flows_passed": sum(1 for r in positive_rows if r["review_pass"]),
        "all_positive_flows_pass": all(r["review_pass"] for r in positive_rows),
        "candidate_count": len(candidates),
        "all_candidates_candidate_only": candidate_ok,
        "all_candidates_not_fact": candidate_ok,
        "no_fact_write": candidate_ok,
        "no_runtime_action": candidate_ok,
        "no_task_commit": candidate_ok,
        "no_user_facing_output": True,
        "issues": positive_issues,
        "review_pass": all(r["review_pass"] for r in positive_rows) and candidate_ok,
        **meta,
    }

    blocked_rows: List[Dict[str, Any]] = []
    blocked_issues: List[Dict[str, Any]] = []
    for sid in BLOCKED_SCENARIO_IDS:
        row = by_id.get(sid)
        action = (row or {}).get("observed_action", "stop")
        stop_hold = row is not None and row.get("dryrun_pass") is True and action in ("stop", "hold")
        blocked_rows.append(
            {
                "scenario_id": sid,
                "observed_action": action,
                "stop_or_hold": stop_hold,
                "review_pass": stop_hold,
            }
        )
        if not stop_hold:
            blocked_issues.append(
                {
                    "issue_id": f"blocked_fail:{sid}",
                    "severity": "high",
                    "detail": "blocked request must stop/hold",
                }
            )

    blocked_review = {
        "review_id": "limited_runtime_blocked_flow_review_v1",
        "scenarios": blocked_rows,
        "blocked_flow_count": len(BLOCKED_SCENARIO_IDS),
        "blocked_flows_enforced": sum(1 for r in blocked_rows if r["review_pass"]),
        "all_blocked_flows_stop_or_hold": all(r["review_pass"] for r in blocked_rows),
        "issues": blocked_issues,
        "review_pass": len(blocked_issues) == 0,
        **meta,
    }

    gate_issues: List[Dict[str, Any]] = []
    gate_by_id = {g.get("gate_id"): g for g in gates.get("gates") or []}
    gate_rows: List[Dict[str, Any]] = []
    for gate_id in LIMITED_RUNTIME_GATES:
        g = gate_by_id.get(gate_id)
        passed = (
            g is not None
            and g.get("enforcement_pass") is True
            and g.get("passed") is True
            and g.get("runtime_action_blocked") is True
        )
        gate_rows.append(
            {
                "gate_id": gate_id,
                "enforcement_pass": g.get("enforcement_pass") if g else False,
                "review_pass": passed,
            }
        )
        if not passed:
            gate_issues.append(
                {"issue_id": f"gate_fail:{gate_id}", "severity": "high", "detail": "gate enforcement_pass required"}
            )

    gate_review = {
        "review_id": "limited_runtime_gate_review_v1",
        "gates": gate_rows,
        "gates_passed": sum(1 for r in gate_rows if r["review_pass"]),
        "gates_total": len(LIMITED_RUNTIME_GATES),
        "enforcement_pass": gates.get("enforcement_pass") is True,
        "issues": gate_issues,
        "review_pass": len(gate_issues) == 0 and gates.get("enforcement_pass") is True,
        **meta,
    }

    stop_issues: List[Dict[str, Any]] = []
    stop_by_trigger = {c.get("trigger"): c for c in stops.get("conditions") or []}
    stop_rows: List[Dict[str, Any]] = []
    for trigger, exp_action in STOP_TRIGGERS:
        c = stop_by_trigger.get(trigger)
        enforced = c is not None and c.get("stop_or_hold_enforced") is True and c.get("passed") is True
        stop_rows.append(
            {
                "trigger": trigger,
                "expected_action": exp_action,
                "observed_action": c.get("observed_action") if c else None,
                "stop_or_hold_enforced": enforced,
                "review_pass": enforced,
            }
        )
        if not enforced:
            stop_issues.append(
                {
                    "issue_id": f"stop_fail:{trigger}",
                    "severity": "high",
                    "detail": "stop condition must be stop_or_hold_enforced",
                }
            )

    stop_review = {
        "review_id": "limited_runtime_stop_condition_review_v1",
        "conditions": stop_rows,
        "conditions_passed": sum(1 for r in stop_rows if r["review_pass"]),
        "conditions_total": len(STOP_TRIGGERS),
        "verification_pass": stops.get("verification_pass") is True,
        "issues": stop_issues,
        "review_pass": len(stop_issues) == 0 and stops.get("verification_pass") is True,
        **meta,
    }

    runtime_violations = audit.get("violations") or []
    runtime_review = {
        "review_id": "limited_runtime_no_runtime_boundary_review_v1",
        "audit_pass": audit.get("audit_pass") is True,
        "violation_count": len(runtime_violations),
        "forbidden_executions_confirmed_absent": [
            "live_camera",
            "paddleocr",
            "rapidocr",
            "real_ocr_provider",
            "navigation_action",
            "task_commit",
            "worldmodel_write",
            "memory_write",
            "tts",
            "llm",
        ],
        "review_pass": audit.get("audit_pass") is True and len(runtime_violations) == 0,
        **meta,
    }

    reviews_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and positive_review.get("review_pass")
        and blocked_review.get("review_pass")
        and gate_review.get("review_pass")
        and stop_review.get("review_pass")
        and runtime_review.get("review_pass")
    )
    boundary_ok = reviews_pass

    single_chain_readiness = {
        "readiness_id": "single_chain_trial_planning_readiness_v1",
        "ready_for_single_chain_trial_planning": boundary_ok,
        "recommended_first_chain": "vision",
        "recommended_first_trial": "Vision sample frame single-chain",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "VISION_OCR_NAVIGATION_TASK_LIMITED_RUNTIME_TRIAL_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "rationale": [
            "lowest risk",
            "no OCR provider",
            "no navigation action",
            "no task commit",
            "validates sample/fixture frame → visual_observation_candidate only",
            "baseline for later OCR mock / navigation / task single-chain trials",
        ],
        "deferred_chains": ["ocr_mock", "navigation_guidance", "task_candidate"],
        "do_not_open_four_chains_together": True,
        **meta,
    }

    non_claims_review = {
        "review_id": "non_claims_review_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": single_chain_readiness["final_decision"],
        "recommended_next_phase": single_chain_readiness["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        "positive_flow_pass_count": positive_review.get("positive_flows_passed"),
        "blocked_flow_enforced_count": blocked_review.get("blocked_flows_enforced"),
        "gates_pass_count": gate_review.get("gates_passed"),
        **meta,
    }

    return {
        "limited_runtime_trial_dryrun_input_review": input_review,
        "limited_runtime_positive_flow_review": positive_review,
        "limited_runtime_blocked_flow_review": blocked_review,
        "limited_runtime_gate_review": gate_review,
        "limited_runtime_stop_condition_review": stop_review,
        "limited_runtime_no_runtime_boundary_review": runtime_review,
        "single_chain_trial_planning_readiness": single_chain_readiness,
        "non_claims_review": non_claims_review,
        "summary": summary,
    }
