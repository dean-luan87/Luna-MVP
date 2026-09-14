# -*- coding: utf-8 -*-
"""Vision / OCR / Navigation / Task Minimal Recovery Execution Post-DryRun Review v1.

Lightweight review after minimal recovery execution dry-run GO. Review-only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_ocr_navigation_task_minimal_recovery_execution_planning_v1 import (
    EXECUTION_GATES,
)

PHASE_ID = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Execution-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "minimal_recovery_execution_post_dryrun_review_only"
SOURCE_CHAIN = "vision_ocr_navigation_task_minimal_recovery_execution_post_dryrun_review_v1"

UPSTREAM_PHASE = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Execution-DryRun-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "VISION_OCR_NAVIGATION_TASK_MINIMAL_RECOVERY_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
UPSTREAM_NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Execution-Post-DryRun-Review-v1-001"

FINAL_DECISION = (
    "VISION_OCR_NAVIGATION_TASK_MINIMAL_RECOVERY_EXECUTION_POST_DRYRUN_REVIEW_READY_FOR_CONTROLLED_TRIAL_PLANNING"
)
NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Controlled-Trial-Planning-v1-001"

REQUIRED_SCENARIO_IDS: Tuple[str, ...] = (
    "vision_only_observation_candidate",
    "vision_to_ocr_request_candidate",
    "vision_to_navigation_guidance_candidate",
    "full_candidate_flow",
)

RUNTIME_REVIEW_FIELDS: Tuple[str, ...] = (
    "runtime_enabled_now",
    "camera_runtime_enabled_now",
    "frame_capture_executed_now",
    "image_read_executed_now",
    "vision_model_invoked_now",
    "visual_fact_generated_now",
    "ocr_provider_invoked_now",
    "ocr_evidence_generated_now",
    "navigation_action_triggered_now",
    "map_write_executed_now",
    "gps_strong_anchor_committed_now",
    "task_state_committed_now",
    "task_manager_committed_now",
    "world_model_written_now",
    "memory_written_now",
    "scene_delta_generated_now",
    "tts_invoked_now",
    "llm_invoked_now",
)

FALLBACK_REVIEW_EXPECTATIONS: Tuple[Tuple[str, str, Tuple[str, ...]], ...] = (
    ("missing_vision_input", "hold", ("request_controlled_sample_later",)),
    ("ocr_provider_required", "blocked", ("blocked_until_ocr_runtime_phase", "defer_until_ocr_runtime_phase")),
    ("navigation_action_required", "candidate_only", ("no_action_execute",)),
    ("task_commit_required", "blocked", ("blocked_until_task_runtime_phase", "defer_until_task_runtime_phase")),
    (
        "midplatform_ambiguity",
        "defer",
        ("defer_to_midplatform_structure_cleanup", "midplatform-structure-cleanup"),
    ),
    (
        "user_facing_speech_required",
        "defer",
        ("defer_to_voice_interaction_runtime_planning", "voice-interaction-runtime"),
    ),
)

NON_CLAIMS: Tuple[str, ...] = (
    "Post-DryRun Review GO ≠ runtime enabled",
    "DryRun scenario pass ≠ real execution",
    "Candidate flow pass ≠ user-facing output",
    "visual_observation_candidate ≠ visual fact",
    "ocr_request_candidate ≠ OCR provider invoked",
    "navigation_guidance_candidate ≠ navigation action",
    "task_response_candidate ≠ TTS invoked",
    "task candidate ≠ task committed",
    "controlled trial planning readiness ≠ controlled trial started",
)

GATE_RESULT_FIELDS: Tuple[str, ...] = (
    "candidate_flow_allowed",
    "runtime_action_blocked",
    "fact_write_blocked",
    "task_commit_blocked",
    "speech_output_blocked",
    "provider_invocation_blocked",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "minimal_recovery_execution_post_dryrun_review_only": True,
        "review_only": True,
        "feature_implementation_started_now": False,
        "runtime_enabled_now": False,
        "camera_runtime_enabled_now": False,
        "frame_capture_executed_now": False,
        "image_read_executed_now": False,
        "vision_model_invoked_now": False,
        "visual_fact_generated_now": False,
        "ocr_provider_invoked_now": False,
        "ocr_evidence_generated_now": False,
        "navigation_action_triggered_now": False,
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


def run_vision_ocr_navigation_task_minimal_recovery_execution_post_dryrun_review_v1(
    *,
    vision_ocr_navigation_task_minimal_recovery_execution_dryrun_root: str,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(vision_ocr_navigation_task_minimal_recovery_execution_dryrun_root).expanduser().resolve()

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(dryrun_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_dryrun_root": str(dryrun_root),
    }

    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    scenarios = _try_read_json(dryrun_root / "dryrun_scenario_matrix_v1.json") or {}
    gates = _try_read_json(dryrun_root / "execution_gate_consumption_result_v1.json") or {}
    fallback = _try_read_json(dryrun_root / "fallback_consumption_result_v1.json") or {}
    audit = _try_read_json(dryrun_root / "no_runtime_boundary_audit_v1.json") or {}
    cross = _try_read_json(dryrun_root / "cross_chain_candidate_flow_trace_v1.json") or {}

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
    if scenarios.get("scenarios_passed", 0) != 4 or scenarios.get("scenarios_total", 0) != 4:
        blockers.append("scenario pass count must be 4/4")
    if audit.get("audit_pass") is not True:
        blockers.append("no_runtime_boundary_audit must pass")

    for field in RUNTIME_REVIEW_FIELDS:
        if dryrun_sm.get(field) is True:
            blockers.append(f"dryrun {field} must be false")

    input_review = {
        "review_id": "minimal_recovery_execution_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_verifier": dryrun_vr.get("verifier"),
        "upstream_verifier_trusted": dryrun_verifier_trusted,
        "upstream_summary_trusted": dryrun_summary_trusted,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "scenario_pass_count": scenarios.get("scenarios_passed"),
        "scenario_total_count": scenarios.get("scenarios_total"),
        "gates_passed": dryrun_sm.get("gates_passed"),
        "review_pass": not blockers,
        "blockers": blockers,
        **meta,
    }

    scenario_rows: List[Dict[str, Any]] = []
    scenario_issues: List[Dict[str, Any]] = []
    by_id = {s.get("scenario_id"): s for s in scenarios.get("scenarios") or []}
    for sid in REQUIRED_SCENARIO_IDS:
        row = by_id.get(sid)
        passed = row is not None and row.get("dryrun_pass") is True
        scenario_rows.append({"scenario_id": sid, "dryrun_pass": passed, "review_pass": passed})
        if not passed:
            scenario_issues.append(
                {"issue_id": f"scenario_fail:{sid}", "severity": "high", "detail": "scenario must pass"}
            )

    candidates: List[Dict[str, Any]] = []
    for fname in (
        "visual_observation_candidate_dryrun_v1.json",
        "task_observation_requirement_dryrun_v1.json",
        "ocr_request_candidate_dryrun_v1.json",
        "navigation_guidance_candidate_dryrun_v1.json",
        "task_response_candidate_dryrun_v1.json",
        "cross_chain_candidate_flow_trace_v1.json",
    ):
        data = _try_read_json(dryrun_root / fname)
        if data:
            _collect_candidates(data, candidates)

    candidate_ok = True
    for c in candidates:
        if c.get("candidate_only") is not True:
            candidate_ok = False
            scenario_issues.append(
                {
                    "issue_id": f"candidate_not_only:{c.get('candidate_id')}",
                    "severity": "high",
                    "detail": "candidate_only must be true",
                }
            )
        if c.get("fact_status") != "not_fact":
            candidate_ok = False
            scenario_issues.append(
                {
                    "issue_id": f"candidate_not_not_fact:{c.get('candidate_id')}",
                    "severity": "high",
                    "detail": "fact_status must be not_fact",
                }
            )

    if cross.get("candidate_only") is not True:
        candidate_ok = False
        scenario_issues.append(
            {
                "issue_id": "cross_chain_not_candidate_only",
                "severity": "high",
                "detail": "cross_chain must be candidate_only",
            }
        )

    scenario_review = {
        "review_id": "scenario_pass_review_v1",
        "scenarios": scenario_rows,
        "all_scenarios_pass": all(r["review_pass"] for r in scenario_rows),
        "candidate_count": len(candidates),
        "all_candidates_candidate_only": candidate_ok,
        "all_candidates_not_fact": candidate_ok,
        "issues": scenario_issues,
        "review_pass": all(r["review_pass"] for r in scenario_rows) and candidate_ok,
        **meta,
    }

    gate_issues: List[Dict[str, Any]] = []
    gate_by_id = {g.get("gate_id"): g for g in gates.get("gates") or []}
    gate_rows: List[Dict[str, Any]] = []
    for gate_id in EXECUTION_GATES:
        g = gate_by_id.get(gate_id)
        row_pass = g is not None and g.get("consumable") is True and g.get("passed") is True
        field_pass = True
        if g:
            for field in GATE_RESULT_FIELDS:
                if g.get(field) is not True:
                    field_pass = False
        else:
            field_pass = False
        passed = row_pass and field_pass
        gate_rows.append({"gate_id": gate_id, "review_pass": passed, "consumable": g.get("consumable") if g else False})
        if not passed:
            gate_issues.append(
                {"issue_id": f"gate_fail:{gate_id}", "severity": "high", "detail": "gate must be consumable with blocks"}
            )

    gate_review = {
        "review_id": "execution_gate_review_v1",
        "gates": gate_rows,
        "gates_passed": sum(1 for r in gate_rows if r["review_pass"]),
        "gates_total": len(EXECUTION_GATES),
        "consumption_pass": gates.get("consumption_pass") is True,
        "issues": gate_issues,
        "review_pass": len(gate_issues) == 0 and gates.get("consumption_pass") is True,
        **meta,
    }

    fallback_issues: List[Dict[str, Any]] = []
    fb_results = {r.get("condition"): r for r in fallback.get("results") or []}
    fb_rows: List[Dict[str, Any]] = []
    for cond, exp_action, patterns in FALLBACK_REVIEW_EXPECTATIONS:
        r = fb_results.get(cond)
        consumable = r is not None and r.get("consumable") is True
        fb_rows.append({"condition": cond, "consumable": consumable, "review_pass": consumable})
        if not consumable:
            fallback_issues.append(
                {"issue_id": f"fallback_fail:{cond}", "severity": "high", "detail": "fallback must be consumable"}
            )

    fallback_review = {
        "review_id": "fallback_review_v1",
        "rules": fb_rows,
        "consumption_pass": fallback.get("consumption_pass") is True,
        "issues": fallback_issues,
        "review_pass": len(fallback_issues) == 0 and fallback.get("consumption_pass") is True,
        **meta,
    }

    runtime_violations = audit.get("violations") or []
    runtime_review = {
        "review_id": "no_runtime_boundary_review_v1",
        "audit_pass": audit.get("audit_pass") is True,
        "violation_count": len(runtime_violations),
        "forbidden_executions_confirmed_absent": [
            "camera",
            "image_read",
            "vision_model",
            "ocr_provider",
            "navigation_action",
            "map_write",
            "gps_strong_anchor_commit",
            "task_commit",
            "worldmodel_write",
            "memory_write",
            "scene_delta",
            "tts",
            "llm",
            "midplatform_refactor",
        ],
        "review_pass": audit.get("audit_pass") is True and len(runtime_violations) == 0,
        **meta,
    }

    reviews_pass = (
        not blockers
        and scenario_review.get("review_pass")
        and gate_review.get("review_pass")
        and fallback_review.get("review_pass")
        and runtime_review.get("review_pass")
    )
    boundary_ok = reviews_pass

    trial_readiness = {
        "readiness_id": "controlled_trial_planning_readiness_v1",
        "ready_for_controlled_trial_planning": boundary_ok,
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "VISION_OCR_NAVIGATION_TASK_MINIMAL_RECOVERY_EXECUTION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "controlled_trial_note": (
            "Controlled Trial Planning still does not enable camera/OCR provider/navigation/task commit"
        ),
        "trial_scope_preview": {
            "inputs": "controlled references and candidate envelopes only",
            "gates": "inherit 11 execution gates + trial stop conditions",
            "stop_conditions": "any runtime gate breach → halt",
        },
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
        "final_decision": trial_readiness["final_decision"],
        "recommended_next_phase": trial_readiness["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        "scenario_pass_count": scenarios.get("scenarios_passed"),
        "scenario_total_count": scenarios.get("scenarios_total"),
        **meta,
    }

    return {
        "minimal_recovery_execution_dryrun_input_review": input_review,
        "scenario_pass_review": scenario_review,
        "execution_gate_review": gate_review,
        "fallback_review": fallback_review,
        "no_runtime_boundary_review": runtime_review,
        "controlled_trial_planning_readiness": trial_readiness,
        "non_claims_review": non_claims_review,
        "summary": summary,
    }
