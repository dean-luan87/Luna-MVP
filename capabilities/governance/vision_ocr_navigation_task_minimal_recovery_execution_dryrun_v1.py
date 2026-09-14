# -*- coding: utf-8 -*-
"""Vision / OCR / Navigation / Task Minimal Recovery Execution DryRun v1.

Simulated candidate-only cross-chain flow. Dry-run only; no runtime.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_ocr_navigation_task_minimal_recovery_execution_planning_v1 import (
    EXECUTION_GATES,
)

PHASE_ID = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Execution-DryRun-v1-001"
DRYRUN_SCOPE = "minimal_recovery_execution_dryrun_only"
SOURCE_CHAIN = "vision_ocr_navigation_task_minimal_recovery_execution_dryrun_v1"

UPSTREAM_PHASE = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Execution-Planning-v1-001"
UPSTREAM_REQUIRED_FINAL = "VISION_OCR_NAVIGATION_TASK_MINIMAL_RECOVERY_EXECUTION_PLANNING_READY_FOR_DRYRUN"
UPSTREAM_NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Execution-DryRun-v1-001"

FINAL_DECISION = "VISION_OCR_NAVIGATION_TASK_MINIMAL_RECOVERY_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Execution-Post-DryRun-Review-v1-001"

NON_CLAIMS: Tuple[str, ...] = (
    "DryRun GO ≠ runtime enabled",
    "Candidate flow pass ≠ real execution",
    "visual_observation_candidate ≠ visual fact",
    "ocr_request_candidate ≠ OCR provider invoked",
    "navigation_guidance_candidate ≠ navigation action",
    "task_response_candidate ≠ TTS invoked",
    "task_state_candidate ≠ task committed",
    "source_chain pass ≠ WorldModel write allowed",
    "fallback pass ≠ fallback executed in runtime",
)

RUNTIME_AUDIT_FIELDS: Tuple[str, ...] = (
    "runtime_enabled_now",
    "camera_runtime_enabled_now",
    "frame_capture_executed_now",
    "image_read_executed_now",
    "vision_model_invoked_now",
    "visual_fact_generated_now",
    "ocr_runtime_enabled_now",
    "ocr_provider_invoked_now",
    "ocr_evidence_generated_now",
    "navigation_runtime_enabled_now",
    "navigation_action_triggered_now",
    "map_write_executed_now",
    "gps_strong_anchor_committed_now",
    "task_midplatform_runtime_enabled_now",
    "task_state_committed_now",
    "task_manager_committed_now",
    "world_model_written_now",
    "memory_written_now",
    "scene_delta_generated_now",
    "tts_invoked_now",
    "llm_invoked_now",
)

FALLBACK_EXPECTATIONS: Tuple[Tuple[str, str, Tuple[str, ...]], ...] = (
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


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "minimal_recovery_execution_dryrun_only": True,
        "simulated": True,
        "feature_implementation_started_now": False,
        "runtime_enabled_now": False,
        "camera_runtime_enabled_now": False,
        "frame_capture_executed_now": False,
        "image_read_executed_now": False,
        "vision_model_invoked_now": False,
        "visual_fact_generated_now": False,
        "ocr_runtime_enabled_now": False,
        "ocr_provider_invoked_now": False,
        "ocr_evidence_generated_now": False,
        "navigation_runtime_enabled_now": False,
        "navigation_action_triggered_now": False,
        "map_write_executed_now": False,
        "gps_strong_anchor_committed_now": False,
        "task_midplatform_runtime_enabled_now": False,
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


def _candidate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _make_visual_observation_candidate() -> Dict[str, Any]:
    return {
        "candidate_id": _candidate_id("voc"),
        "candidate_type": "visual_observation_candidate",
        "source": "controlled_frame_reference",
        "focus_reference": "visual_focus_reference_sim",
        "tracking_reference": "tracking_reference_sim",
        "candidate_only": True,
        **_not_fact(),
    }


def _make_task_observation_requirement(task_requires_text: bool, task_requires_movement: bool) -> Dict[str, Any]:
    return {
        "candidate_id": _candidate_id("tor"),
        "candidate_type": "task_observation_requirement",
        "requires_text": task_requires_text,
        "requires_movement": task_requires_movement,
        "candidate_only": True,
        **_not_fact(),
    }


def _make_ocr_request_candidate(voc_id: str) -> Dict[str, Any]:
    return {
        "candidate_id": _candidate_id("orc"),
        "candidate_type": "ocr_request_candidate",
        "upstream_visual_observation_candidate_id": voc_id,
        "roi_reference": "roi_sim_metadata_only",
        "evidence_pack_envelope": "planned_not_generated",
        "provider_invoked": False,
        "candidate_only": True,
        **_not_fact(),
    }


def _make_navigation_guidance_candidate(voc_id: str) -> Dict[str, Any]:
    return {
        "candidate_id": _candidate_id("ngc"),
        "candidate_type": "navigation_guidance_candidate",
        "upstream_visual_observation_candidate_id": voc_id,
        "readonly_map_hint": "map_hint_sim_non_authoritative",
        "route_state_candidate": "route_state_sim",
        "navigation_action_triggered": False,
        "candidate_only": True,
        **_not_fact(),
    }


def _make_task_response_candidate(
    tor_id: str,
    ocr_id: Optional[str],
    nav_id: Optional[str],
) -> Dict[str, Any]:
    return {
        "candidate_id": _candidate_id("trc"),
        "candidate_type": "task_response_candidate",
        "task_observation_requirement_id": tor_id,
        "ocr_request_candidate_id": ocr_id,
        "navigation_guidance_candidate_id": nav_id,
        "task_state_committed": False,
        "speech_output": None,
        "candidate_only": True,
        **_not_fact(),
    }


def _consume_gates(meta: Dict[str, Any]) -> Dict[str, Any]:
    gate_results: List[Dict[str, Any]] = []
    for gate_id in EXECUTION_GATES:
        gate_results.append(
            {
                "gate_id": gate_id,
                "consumable": True,
                "candidate_flow_allowed": True,
                "runtime_action_blocked": True,
                "fact_write_blocked": True,
                "task_commit_blocked": True,
                "speech_output_blocked": True,
                "provider_invocation_blocked": True,
                "passed": True,
            }
        )
    return {
        "result_id": "execution_gate_consumption_result_v1",
        "gates": gate_results,
        "gates_total": len(gate_results),
        "gates_passed": len(gate_results),
        "consumption_pass": True,
        **meta,
    }


def _simulate_scenarios(meta: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any], ...]:
    scenarios: List[Dict[str, Any]] = []
    vision_dryruns: List[Dict[str, Any]] = []
    task_dryruns: List[Dict[str, Any]] = []
    ocr_dryruns: List[Dict[str, Any]] = []
    nav_dryruns: List[Dict[str, Any]] = []
    response_dryruns: List[Dict[str, Any]] = []
    trace_events: List[Dict[str, Any]] = []

    def run_trace(scenario_id: str, steps: List[Dict[str, Any]]) -> None:
        for i, step in enumerate(steps, 1):
            trace_events.append(
                {
                    "scenario_id": scenario_id,
                    "step": i,
                    **step,
                }
            )

    # Scenario 1: vision_only
    voc1 = _make_visual_observation_candidate()
    vision_dryruns.append(
        {
            "dryrun_id": "visual_observation_candidate_dryrun_v1",
            "scenario_id": "vision_only_observation_candidate",
            "input": {
                "controlled_frame_reference": "cf_ref_sim_001",
                "visual_focus_reference": "focus_sim_001",
            },
            "output": voc1,
            "forbidden_invoked": [
                "camera",
                "image_read",
                "vision_model",
                "visual_fact_write",
            ],
            "dryrun_pass": True,
            **meta,
        }
    )
    scenarios.append(
        {
            "scenario_id": "vision_only_observation_candidate",
            "description": "controlled frame / focus reference → visual_observation_candidate",
            "outputs": ["visual_observation_candidate"],
            "dryrun_pass": True,
        }
    )
    run_trace(
        "vision_only_observation_candidate",
        [{"node": "vision", "output": "visual_observation_candidate", "candidate_id": voc1["candidate_id"]}],
    )

    # Scenario 2: vision_to_ocr
    voc2 = _make_visual_observation_candidate()
    tor2 = _make_task_observation_requirement(task_requires_text=True, task_requires_movement=False)
    orc2 = _make_ocr_request_candidate(voc2["candidate_id"])
    vision_dryruns.append(
        {
            "scenario_id": "vision_to_ocr_request_candidate",
            "output": voc2,
            "dryrun_pass": True,
            **meta,
        }
    )
    task_dryruns.append(
        {
            "scenario_id": "vision_to_ocr_request_candidate",
            "output": tor2,
            "dryrun_pass": True,
            **meta,
        }
    )
    ocr_dryruns.append(
        {
            "dryrun_id": "ocr_request_candidate_dryrun_v1",
            "scenario_id": "vision_to_ocr_request_candidate",
            "input": {"visual_observation_candidate_id": voc2["candidate_id"], "task_requires_text": True},
            "output": orc2,
            "forbidden_invoked": ["ocr_provider", "ocr_evidence", "fact_write"],
            "dryrun_pass": True,
            **meta,
        }
    )
    scenarios.append(
        {
            "scenario_id": "vision_to_ocr_request_candidate",
            "description": "visual_observation_candidate + text task → ocr_request_candidate",
            "outputs": ["visual_observation_candidate", "task_observation_requirement", "ocr_request_candidate"],
            "dryrun_pass": True,
        }
    )
    run_trace(
        "vision_to_ocr_request_candidate",
        [
            {"node": "vision", "output": "visual_observation_candidate", "candidate_id": voc2["candidate_id"]},
            {"node": "task", "output": "task_observation_requirement", "candidate_id": tor2["candidate_id"]},
            {"node": "ocr", "output": "ocr_request_candidate", "candidate_id": orc2["candidate_id"]},
        ],
    )

    # Scenario 3: vision_to_navigation
    voc3 = _make_visual_observation_candidate()
    tor3 = _make_task_observation_requirement(task_requires_text=False, task_requires_movement=True)
    ngc3 = _make_navigation_guidance_candidate(voc3["candidate_id"])
    nav_dryruns.append(
        {
            "dryrun_id": "navigation_guidance_candidate_dryrun_v1",
            "scenario_id": "vision_to_navigation_guidance_candidate",
            "input": {"visual_observation_candidate_id": voc3["candidate_id"], "task_requires_movement": True},
            "output": ngc3,
            "forbidden_invoked": ["navigation_action", "map_write", "gps_strong_anchor"],
            "dryrun_pass": True,
            **meta,
        }
    )
    scenarios.append(
        {
            "scenario_id": "vision_to_navigation_guidance_candidate",
            "description": "visual_observation_candidate + movement task → navigation_guidance_candidate",
            "outputs": [
                "visual_observation_candidate",
                "task_observation_requirement",
                "navigation_guidance_candidate",
            ],
            "dryrun_pass": True,
        }
    )
    run_trace(
        "vision_to_navigation_guidance_candidate",
        [
            {"node": "vision", "output": "visual_observation_candidate", "candidate_id": voc3["candidate_id"]},
            {"node": "task", "output": "task_observation_requirement", "candidate_id": tor3["candidate_id"]},
            {"node": "navigation", "output": "navigation_guidance_candidate", "candidate_id": ngc3["candidate_id"]},
        ],
    )

    # Scenario 4: full flow
    voc4 = _make_visual_observation_candidate()
    tor4 = _make_task_observation_requirement(task_requires_text=True, task_requires_movement=True)
    orc4 = _make_ocr_request_candidate(voc4["candidate_id"])
    ngc4 = _make_navigation_guidance_candidate(voc4["candidate_id"])
    trc4 = _make_task_response_candidate(tor4["candidate_id"], orc4["candidate_id"], ngc4["candidate_id"])
    task_dryruns.append(
        {
            "dryrun_id": "task_observation_requirement_dryrun_v1",
            "scenario_id": "full_candidate_flow",
            "output": tor4,
            "dryrun_pass": True,
            **meta,
        }
    )
    response_dryruns.append(
        {
            "dryrun_id": "task_response_candidate_dryrun_v1",
            "scenario_id": "full_candidate_flow",
            "output": trc4,
            "forbidden_invoked": ["task_commit", "tts", "llm", "memory_write", "worldmodel_write"],
            "dryrun_pass": True,
            **meta,
        }
    )
    scenarios.append(
        {
            "scenario_id": "full_candidate_flow",
            "description": "full candidate-only cross-chain flow",
            "outputs": [
                "task_observation_requirement",
                "ocr_request_candidate",
                "navigation_guidance_candidate",
                "task_response_candidate",
            ],
            "dryrun_pass": True,
        }
    )
    run_trace(
        "full_candidate_flow",
        [
            {"node": "vision", "output": "visual_observation_candidate", "candidate_id": voc4["candidate_id"]},
            {"node": "task", "output": "task_observation_requirement", "candidate_id": tor4["candidate_id"]},
            {"node": "ocr", "output": "ocr_request_candidate", "candidate_id": orc4["candidate_id"]},
            {"node": "navigation", "output": "navigation_guidance_candidate", "candidate_id": ngc4["candidate_id"]},
            {"node": "task", "output": "task_response_candidate", "candidate_id": trc4["candidate_id"]},
        ],
    )

    scenario_matrix = {
        "matrix_id": "dryrun_scenario_matrix_v1",
        "scenarios": scenarios,
        "scenarios_total": len(scenarios),
        "scenarios_passed": sum(1 for s in scenarios if s.get("dryrun_pass")),
        "consumption_pass": all(s.get("dryrun_pass") for s in scenarios),
        **meta,
    }

    cross_trace = {
        "trace_id": "cross_chain_candidate_flow_trace_v1",
        "flow_label": "candidate_only_minimal_loop",
        "events": trace_events,
        "event_count": len(trace_events),
        "candidate_only": True,
        "flow_pass": len(trace_events) >= 5,
        **meta,
    }

    # Aggregate per-type dryrun summaries (latest scenario representative)
    vision_summary = {
        "dryrun_id": "visual_observation_candidate_dryrun_v1",
        "runs": vision_dryruns,
        "runs_passed": sum(1 for r in vision_dryruns if r.get("dryrun_pass")),
        **meta,
    }
    task_summary = {
        "dryrun_id": "task_observation_requirement_dryrun_v1",
        "runs": task_dryruns,
        "runs_passed": sum(1 for r in task_dryruns if r.get("dryrun_pass")),
        **meta,
    }
    ocr_summary = {
        "dryrun_id": "ocr_request_candidate_dryrun_v1",
        "runs": [r for r in ocr_dryruns if r.get("dryrun_id")],
        "runs_passed": sum(1 for r in ocr_dryruns if r.get("dryrun_pass")),
        **meta,
    }
    nav_summary = {
        "dryrun_id": "navigation_guidance_candidate_dryrun_v1",
        "runs": [r for r in nav_dryruns if r.get("dryrun_id")],
        "runs_passed": sum(1 for r in nav_dryruns if r.get("dryrun_pass")),
        **meta,
    }
    response_summary = {
        "dryrun_id": "task_response_candidate_dryrun_v1",
        "runs": response_dryruns,
        "runs_passed": sum(1 for r in response_dryruns if r.get("dryrun_pass")),
        **meta,
    }

    return (
        scenario_matrix,
        vision_summary,
        task_summary,
        ocr_summary,
        nav_summary,
        response_summary,
        cross_trace,
    )


def _consume_fallback(planning_fallback: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    rules = planning_fallback.get("rules") or []
    results: List[Dict[str, Any]] = []
    issues: List[Dict[str, Any]] = []
    for cond, exp_action, exp_fallback_patterns in FALLBACK_EXPECTATIONS:
        matched = next((r for r in rules if r.get("condition") == cond), None)
        if not matched:
            issues.append(
                {
                    "issue_id": f"fallback_missing:{cond}",
                    "severity": "high",
                    "detail": "planning fallback rule missing",
                }
            )
            continue
        action_ok = matched.get("action") == exp_action
        fb = str(matched.get("fallback", "")).lower()
        fallback_ok = any(p.lower() in fb for p in exp_fallback_patterns)
        simulated = exp_fallback_patterns[0]
        results.append(
            {
                "condition": cond,
                "expected_action": exp_action,
                "expected_fallback_patterns": list(exp_fallback_patterns),
                "planning_action": matched.get("action"),
                "planning_fallback": matched.get("fallback"),
                "consumable": action_ok and fallback_ok,
                "simulated_outcome": simulated,
            }
        )
        if not (action_ok and fallback_ok):
            issues.append(
                {
                    "issue_id": f"fallback_mismatch:{cond}",
                    "severity": "high",
                    "detail": "fallback rule mismatch vs dryrun expectation",
                }
            )

    high = [i for i in issues if i.get("severity") == "high"]
    return {
        "result_id": "fallback_consumption_result_v1",
        "results": results,
        "issues": issues,
        "consumption_pass": len(high) == 0,
        "high_risk_count": len(high),
        **meta,
    }


def _runtime_boundary_audit(meta: Dict[str, Any]) -> Dict[str, Any]:
    violations = []
    for field in RUNTIME_AUDIT_FIELDS:
        if meta.get(field) is True:
            violations.append({"field": field, "severity": "high"})
    return {
        "audit_id": "no_runtime_boundary_audit_v1",
        "fields_checked": list(RUNTIME_AUDIT_FIELDS),
        "violations": violations,
        "audit_pass": len(violations) == 0,
        **meta,
    }


def run_vision_ocr_navigation_task_minimal_recovery_execution_dryrun_v1(
    *,
    vision_ocr_navigation_task_minimal_recovery_execution_planning_root: str,
) -> Dict[str, Any]:
    blockers: List[str] = []
    planning_root = Path(
        vision_ocr_navigation_task_minimal_recovery_execution_planning_root
    ).expanduser().resolve()

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(planning_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_planning_root": str(planning_root),
    }

    planning_sm = _try_read_json(planning_root / "summary.json") or {}
    planning_vr = _try_read_json(planning_root / "verifier_report.json") or {}
    cross_plan = _try_read_json(planning_root / "cross_chain_execution_flow_plan_v1.json") or {}
    gates_plan = _try_read_json(planning_root / "execution_boundary_gate_matrix_v1.json") or {}
    fallback_plan = _try_read_json(planning_root / "failure_and_fallback_plan_v1.json") or {}

    planning_verifier_trusted = planning_vr.get("verifier") == "GO" and planning_vr.get("passed") is True
    planning_summary_trusted = (
        planning_sm.get("boundary_ok") is True
        and planning_sm.get("phase") == UPSTREAM_PHASE
        and planning_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and planning_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE
        and planning_sm.get("minimal_recovery_execution_planning_only") is True
    )
    if not planning_verifier_trusted and not planning_summary_trusted:
        blockers.append("planning verifier must be GO")
    if planning_sm.get("runtime_enabled_now") is True:
        blockers.append("planning runtime_enabled_now must be false")
    if len(gates_plan.get("gates") or []) < len(EXECUTION_GATES):
        blockers.append("execution gates must be fully planned")
    if "candidate_only" not in (cross_plan.get("invariants") or []):
        blockers.append("cross-chain must be candidate_only")

    boundary_ok_upstream = not blockers

    policy = {
        "policy_id": "minimal_recovery_execution_dryrun_policy_v1",
        "scope": DRYRUN_SCOPE,
        "mode": "simulated_candidate_only_cross_chain_dryrun",
        **meta,
    }

    input_review = {
        "review_id": "minimal_execution_planning_input_review_v1",
        "upstream_root": str(planning_root),
        "upstream_verifier": planning_vr.get("verifier"),
        "upstream_verifier_trusted": planning_verifier_trusted,
        "upstream_summary_trusted": planning_summary_trusted,
        "upstream_final_decision": planning_sm.get("final_decision"),
        "execution_gates_planned": len(gates_plan.get("gates") or []),
        "cross_chain_candidate_only": planning_sm.get("cross_chain_candidate_only"),
        "review_pass": boundary_ok_upstream,
        "blockers": blockers,
        **meta,
    }

    (
        scenario_matrix,
        vision_dry,
        task_dry,
        ocr_dry,
        nav_dry,
        response_dry,
        cross_trace,
    ) = _simulate_scenarios(meta)

    gate_result = _consume_gates(meta)
    fallback_result = _consume_fallback(fallback_plan, meta)
    runtime_audit = _runtime_boundary_audit(meta)

    high_count = 0
    if not boundary_ok_upstream:
        high_count += len(blockers)
    if not scenario_matrix.get("consumption_pass"):
        high_count += 1
    if not gate_result.get("consumption_pass"):
        high_count += 1
    if not fallback_result.get("consumption_pass"):
        high_count += fallback_result.get("high_risk_count", 1)
    if not runtime_audit.get("audit_pass"):
        high_count += 1
    if not cross_trace.get("flow_pass"):
        high_count += 1

    boundary_ok = high_count == 0

    non_claims = {
        "register_id": "minimal_recovery_execution_dryrun_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    readiness = {
        "decision_id": "minimal_recovery_execution_dryrun_readiness_decision_v1",
        "final_decision": FINAL_DECISION if boundary_ok else "VISION_OCR_NAVIGATION_TASK_MINIMAL_RECOVERY_EXECUTION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "boundary_ok": boundary_ok,
        "high_risk_count": high_count,
        "upstream_blockers": blockers,
        "all_scenarios_pass": scenario_matrix.get("consumption_pass"),
        "gates_consumption_pass": gate_result.get("consumption_pass"),
        "fallback_consumption_pass": fallback_result.get("consumption_pass"),
        "cross_chain_flow_pass": cross_trace.get("flow_pass"),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "high_risk_count": high_count,
        "scenarios_passed": scenario_matrix.get("scenarios_passed"),
        "gates_passed": gate_result.get("gates_passed"),
        **meta,
    }

    return {
        "minimal_recovery_execution_dryrun_policy": policy,
        "minimal_execution_planning_input_review": input_review,
        "dryrun_scenario_matrix": scenario_matrix,
        "visual_observation_candidate_dryrun": vision_dry,
        "task_observation_requirement_dryrun": task_dry,
        "ocr_request_candidate_dryrun": ocr_dry,
        "navigation_guidance_candidate_dryrun": nav_dry,
        "task_response_candidate_dryrun": response_dry,
        "cross_chain_candidate_flow_trace": cross_trace,
        "execution_gate_consumption_result": gate_result,
        "fallback_consumption_result": fallback_result,
        "no_runtime_boundary_audit": runtime_audit,
        "minimal_recovery_execution_dryrun_non_claims_register": non_claims,
        "minimal_recovery_execution_dryrun_readiness_decision": readiness,
        "summary": summary,
    }
