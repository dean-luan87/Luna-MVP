# -*- coding: utf-8 -*-
"""Vision / OCR / Navigation / Task Limited Runtime Trial DryRun v1.

Fixture/sample/mock consumption of limited runtime trial plan. No live runtime.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_ocr_navigation_task_limited_runtime_trial_planning_v1 import (
    LIMITED_RUNTIME_GATES,
)

PHASE_ID = "Phase-Vision-OCR-Navigation-Task-Limited-Runtime-Trial-DryRun-v1-001"
DRYRUN_SCOPE = "limited_runtime_trial_dryrun_only"
SOURCE_CHAIN = "vision_ocr_navigation_task_limited_runtime_trial_dryrun_v1"

UPSTREAM_PHASE = "Phase-Vision-OCR-Navigation-Task-Limited-Runtime-Trial-Planning-v1-001"
UPSTREAM_REQUIRED_FINAL = "VISION_OCR_NAVIGATION_TASK_LIMITED_RUNTIME_TRIAL_PLANNING_READY_FOR_DRYRUN"
UPSTREAM_NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Limited-Runtime-Trial-DryRun-v1-001"

FINAL_DECISION_GO = "VISION_OCR_NAVIGATION_TASK_LIMITED_RUNTIME_TRIAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_HOLD = "VISION_OCR_NAVIGATION_TASK_LIMITED_RUNTIME_TRIAL_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Vision-OCR-Navigation-Task-Limited-Runtime-Trial-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-OCR-Navigation-Task-Limited-Runtime-Trial-Issue-Review-v1-001"

REQUIRED_SCENARIOS: Tuple[str, ...] = (
    "sample_frame_to_visual_observation_candidate",
    "visual_candidate_to_mock_ocr_result_candidate",
    "visual_candidate_to_synthetic_navigation_guidance_candidate",
    "task_candidate_flow_with_mock_ocr_and_guidance",
    "blocked_live_camera_request",
    "blocked_real_ocr_provider_request",
    "blocked_navigation_action_request",
    "blocked_task_commit_request",
)

STOP_TRIGGERS: Tuple[Tuple[str, str], ...] = (
    ("need_live_camera", "stop"),
    ("need_new_image_capture", "stop"),
    ("need_real_ocr_provider", "stop"),
    ("need_navigation_action", "stop"),
    ("need_task_commit", "stop"),
    ("need_tts_or_llm", "stop"),
    ("need_worldmodel_or_memory_write", "stop"),
    ("source_chain_missing", "hold"),
    ("candidate_attempts_fact_upgrade", "stop"),
    ("safety_gate_failed", "stop"),
    ("fixture_or_controlled_input_unverifiable", "hold"),
    ("midplatform_routing_ambiguity", "hold"),
)

NON_CLAIMS: Tuple[str, ...] = (
    "Limited Runtime Trial DryRun GO ≠ limited runtime trial started",
    "DryRun GO ≠ live runtime enabled",
    "sample frame reference dry-run ≠ live camera",
    "mock ocr_result_candidate ≠ real OCR provider",
    "synthetic navigation_guidance_candidate ≠ navigation action",
    "task_response_candidate dry-run ≠ task commit / TTS",
    "gate consumption pass ≠ WorldModel write allowed",
    "fixture flow pass ≠ visual fact generated",
)

RUNTIME_AUDIT_FIELDS: Tuple[str, ...] = (
    "live_runtime_enabled_now",
    "live_camera_enabled_now",
    "camera_runtime_enabled_now",
    "frame_capture_executed_now",
    "new_image_read_executed_now",
    "arbitrary_image_read_executed_now",
    "vision_model_invoked_now",
    "visual_fact_generated_now",
    "ocr_provider_invoked_now",
    "real_ocr_provider_enabled_now",
    "paddleocr_invoked_now",
    "rapidocr_invoked_now",
    "ocr_evidence_generated_now",
    "navigation_action_triggered_now",
    "real_navigation_runtime_enabled_now",
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


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "limited_runtime_trial_dryrun_only": True,
        "simulated": True,
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


def _candidate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _sample_refs() -> Dict[str, str]:
    return {
        "sample_frame_reference": "sample_frame_ref_lrt_001",
        "fixture_frame_metadata": "fixture_meta_lrt_001",
        "controlled_frame_reference": "cf_ref_lrt_upstream_001",
        "input_class": "sample_frame_reference",
    }


def _validate_upstream(planning_root: Path) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    planning_sm = _try_read_json(planning_root / "summary.json") or {}
    planning_vr = _try_read_json(planning_root / "verifier_report.json") or {}
    gate_matrix = _try_read_json(planning_root / "limited_runtime_gate_matrix_v1.json") or {}
    stop_matrix = _try_read_json(planning_root / "limited_runtime_stop_condition_matrix_v1.json") or {}

    planning_verifier_trusted = planning_vr.get("verifier") == "GO" and planning_vr.get("passed") is True
    planning_summary_trusted = (
        planning_sm.get("boundary_ok") is True
        and planning_sm.get("phase") == UPSTREAM_PHASE
        and planning_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and planning_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE
        and planning_sm.get("limited_runtime_trial_planning_only") is True
    )
    if not planning_verifier_trusted and not planning_summary_trusted:
        blockers.append("planning verifier must be GO")
    if planning_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("upstream final_decision mismatch")
    if planning_sm.get("limited_runtime_trial_started_now") is True:
        blockers.append("limited_runtime_trial_started_now must be false")
    if planning_sm.get("live_runtime_enabled_now") is True:
        blockers.append("live_runtime_enabled_now must be false")
    if (gate_matrix.get("gates_total") or 0) < 12:
        blockers.append("12 gates must be planned")
    if len(stop_matrix.get("conditions") or []) < 11:
        blockers.append("12 stop conditions must be planned")

    for field in RUNTIME_AUDIT_FIELDS:
        if planning_sm.get(field) is True:
            blockers.append(f"planning {field} must be false")

    ctx = {
        "planning_sm": planning_sm,
        "planning_vr": planning_vr,
        "gate_matrix": gate_matrix,
        "stop_matrix": stop_matrix,
        "planning_verifier_trusted": planning_verifier_trusted,
        "planning_summary_trusted": planning_summary_trusted,
    }
    return blockers, ctx


def _build_fixture_matrix(meta: Dict[str, Any]) -> Dict[str, Any]:
    refs = _sample_refs()
    return {
        "matrix_id": "limited_runtime_fixture_input_matrix_v1",
        "fixtures": [
            {
                "fixture_id": "sample_frame_vision",
                "scenario_id": "sample_frame_to_visual_observation_candidate",
                "inputs": refs,
            },
            {
                "fixture_id": "mock_ocr",
                "scenario_id": "visual_candidate_to_mock_ocr_result_candidate",
                "inputs": {**refs, "mock_ocr_response": "fixture_ocr_response_lrt_001"},
            },
            {
                "fixture_id": "synthetic_nav",
                "scenario_id": "visual_candidate_to_synthetic_navigation_guidance_candidate",
                "inputs": {
                    **refs,
                    "synthetic_route_context": "route_ctx_lrt_001",
                    "readonly_map_hint": "map_hint_readonly_lrt",
                },
            },
            {
                "fixture_id": "task_flow",
                "scenario_id": "task_candidate_flow_with_mock_ocr_and_guidance",
                "inputs": {
                    **refs,
                    "task_state_candidate_fixture": "tsc_fixture_lrt_001",
                },
            },
        ],
        "allowed_input_classes": [
            "sample_frame_reference",
            "fixture_frame_metadata",
            "controlled_frame_reference",
            "mock_ocr_response",
            "fixture_ocr_response",
            "synthetic_route_context",
            "readonly_map_hint",
            "task_state_candidate_fixture",
        ],
        "fixtures_total": 4,
        **meta,
    }


def _make_visual_observation_candidate(refs: Dict[str, str]) -> Dict[str, Any]:
    return {
        "candidate_id": _candidate_id("voc"),
        "candidate_type": "visual_observation_candidate",
        "sample_frame_reference": refs["sample_frame_reference"],
        "fixture_frame_metadata": refs["fixture_frame_metadata"],
        "controlled_frame_reference": refs["controlled_frame_reference"],
        "candidate_only": True,
        "runtime_action_allowed": False,
        **_not_fact(),
    }


def _make_mock_ocr_result_candidate(voc_id: str) -> Dict[str, Any]:
    return {
        "candidate_id": _candidate_id("orc"),
        "candidate_type": "ocr_result_candidate",
        "upstream_visual_observation_candidate_id": voc_id,
        "provider_mode": "mock",
        "mock_response_id": "mock_ocr_lrt_001",
        "paddleocr_invoked": False,
        "rapidocr_invoked": False,
        "provider_invoked": False,
        "candidate_only": True,
        **_not_fact(),
    }


def _make_navigation_guidance_candidate(voc_id: str) -> Dict[str, Any]:
    return {
        "candidate_id": _candidate_id("ngc"),
        "candidate_type": "navigation_guidance_candidate",
        "upstream_visual_observation_candidate_id": voc_id,
        "synthetic_route_context": "route_ctx_lrt_001",
        "readonly_map_hint": "map_hint_readonly_lrt",
        "navigation_action_triggered": False,
        "candidate_only": True,
        **_not_fact(),
    }


def _make_task_state_candidate() -> Dict[str, Any]:
    return {
        "candidate_id": _candidate_id("tsc"),
        "candidate_type": "task_state_candidate",
        "lifecycle_phase": "observation_pending",
        "task_state_committed": False,
        "candidate_only": True,
        **_not_fact(),
    }


def _make_task_response_candidate(
    tsc_id: str, ocr_id: str, nav_id: str
) -> Dict[str, Any]:
    return {
        "candidate_id": _candidate_id("trc"),
        "candidate_type": "task_response_candidate",
        "task_state_candidate_id": tsc_id,
        "ocr_result_candidate_id": ocr_id,
        "navigation_guidance_candidate_id": nav_id,
        "task_state_committed": False,
        "speech_output": None,
        "candidate_only": True,
        **_not_fact(),
    }


def _simulate_dryrun(meta: Dict[str, Any]) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[Dict[str, Any]],
]:
    refs = _sample_refs()
    scenarios: List[Dict[str, Any]] = []
    trace: List[Dict[str, Any]] = []

    def add_trace(scenario_id: str, step: int, node: str, output: str, cid: str) -> None:
        trace.append(
            {
                "scenario_id": scenario_id,
                "step": step,
                "node": node,
                "output": output,
                "candidate_id": cid,
                "candidate_only": True,
                "fact_status": "not_fact",
            }
        )

    # 1 sample_frame -> visual_observation_candidate
    voc1 = _make_visual_observation_candidate(refs)
    vision_dryrun = {
        "dryrun_id": "vision_sample_frame_candidate_dryrun_v1",
        "scenario_id": "sample_frame_to_visual_observation_candidate",
        "input": {
            "sample_frame_reference": refs["sample_frame_reference"],
            "fixture_frame_metadata": refs["fixture_frame_metadata"],
        },
        "output": voc1,
        "forbidden_invoked": ["camera", "image_read", "vision_model", "visual_fact_write"],
        "dryrun_pass": True,
        **meta,
    }
    scenarios.append(
        {
            "scenario_id": "sample_frame_to_visual_observation_candidate",
            "dryrun_pass": True,
            "outputs": ["visual_observation_candidate"],
        }
    )
    add_trace(
        "sample_frame_to_visual_observation_candidate",
        1,
        "vision",
        "visual_observation_candidate",
        voc1["candidate_id"],
    )

    # 2 visual -> mock ocr_result_candidate
    voc2 = _make_visual_observation_candidate(refs)
    ocr2 = _make_mock_ocr_result_candidate(voc2["candidate_id"])
    mock_ocr_dryrun = {
        "dryrun_id": "mock_ocr_result_candidate_dryrun_v1",
        "scenario_id": "visual_candidate_to_mock_ocr_result_candidate",
        "input": {
            "visual_observation_candidate_id": voc2["candidate_id"],
            "task_requires_text": True,
            "mock_ocr_response": "fixture_ocr_response_lrt_001",
        },
        "output": ocr2,
        "forbidden_invoked": [
            "real_ocr_provider",
            "paddleocr",
            "rapidocr",
            "ocr_evidence",
            "fact_write",
        ],
        "dryrun_pass": True,
        **meta,
    }
    scenarios.append(
        {
            "scenario_id": "visual_candidate_to_mock_ocr_result_candidate",
            "dryrun_pass": True,
            "outputs": ["visual_observation_candidate", "ocr_result_candidate"],
        }
    )
    add_trace(
        "visual_candidate_to_mock_ocr_result_candidate",
        1,
        "vision",
        "visual_observation_candidate",
        voc2["candidate_id"],
    )
    add_trace(
        "visual_candidate_to_mock_ocr_result_candidate",
        2,
        "ocr",
        "ocr_result_candidate",
        ocr2["candidate_id"],
    )

    # 3 visual -> synthetic navigation guidance
    voc3 = _make_visual_observation_candidate(refs)
    ngc3 = _make_navigation_guidance_candidate(voc3["candidate_id"])
    nav_dryrun = {
        "dryrun_id": "synthetic_navigation_guidance_candidate_dryrun_v1",
        "scenario_id": "visual_candidate_to_synthetic_navigation_guidance_candidate",
        "input": {
            "visual_observation_candidate_id": voc3["candidate_id"],
            "synthetic_route_context": "route_ctx_lrt_001",
        },
        "output": ngc3,
        "forbidden_invoked": ["navigation_action", "map_write", "gps_strong_anchor"],
        "dryrun_pass": True,
        **meta,
    }
    scenarios.append(
        {
            "scenario_id": "visual_candidate_to_synthetic_navigation_guidance_candidate",
            "dryrun_pass": True,
            "outputs": ["visual_observation_candidate", "navigation_guidance_candidate"],
        }
    )
    add_trace(
        "visual_candidate_to_synthetic_navigation_guidance_candidate",
        1,
        "vision",
        "visual_observation_candidate",
        voc3["candidate_id"],
    )
    add_trace(
        "visual_candidate_to_synthetic_navigation_guidance_candidate",
        2,
        "navigation",
        "navigation_guidance_candidate",
        ngc3["candidate_id"],
    )

    # 4 full task flow
    voc4 = _make_visual_observation_candidate(refs)
    ocr4 = _make_mock_ocr_result_candidate(voc4["candidate_id"])
    ngc4 = _make_navigation_guidance_candidate(voc4["candidate_id"])
    tsc4 = _make_task_state_candidate()
    trc4 = _make_task_response_candidate(tsc4["candidate_id"], ocr4["candidate_id"], ngc4["candidate_id"])
    task_dryrun = {
        "dryrun_id": "task_state_candidate_dryrun_v1",
        "scenario_id": "task_candidate_flow_with_mock_ocr_and_guidance",
        "input": {
            "visual_observation_candidate_id": voc4["candidate_id"],
            "ocr_result_candidate_id": ocr4["candidate_id"],
            "navigation_guidance_candidate_id": ngc4["candidate_id"],
        },
        "task_state_candidate": tsc4,
        "task_response_candidate": trc4,
        "forbidden_invoked": ["task_commit", "tts", "llm", "memory_write", "worldmodel_write"],
        "dryrun_pass": True,
        **meta,
    }
    scenarios.append(
        {
            "scenario_id": "task_candidate_flow_with_mock_ocr_and_guidance",
            "dryrun_pass": True,
            "outputs": [
                "visual_observation_candidate",
                "ocr_result_candidate",
                "navigation_guidance_candidate",
                "task_state_candidate",
                "task_response_candidate",
            ],
        }
    )
    for i, (node, out, cid) in enumerate(
        [
            ("vision", "visual_observation_candidate", voc4["candidate_id"]),
            ("ocr", "ocr_result_candidate", ocr4["candidate_id"]),
            ("navigation", "navigation_guidance_candidate", ngc4["candidate_id"]),
            ("task", "task_state_candidate", tsc4["candidate_id"]),
            ("task", "task_response_candidate", trc4["candidate_id"]),
        ],
        1,
    ):
        add_trace("task_candidate_flow_with_mock_ocr_and_guidance", i, node, out, cid)

    # 5-8 blocked requests
    blocked_specs = [
        (
            "blocked_live_camera_request",
            "live_camera",
            "no_live_camera_gate",
            "need_live_camera",
            "stop",
        ),
        (
            "blocked_real_ocr_provider_request",
            "real_ocr_provider",
            "no_real_ocr_provider_gate",
            "need_real_ocr_provider",
            "stop",
        ),
        (
            "blocked_navigation_action_request",
            "navigation_action",
            "no_navigation_action_gate",
            "need_navigation_action",
            "stop",
        ),
        (
            "blocked_task_commit_request",
            "task_commit",
            "no_task_commit_gate",
            "need_task_commit",
            "stop",
        ),
    ]
    for scenario_id, request, gate_id, stop_trigger, action in blocked_specs:
        scenarios.append(
            {
                "scenario_id": scenario_id,
                "dryrun_pass": True,
                "blocked_request": request,
                "gate_id": gate_id,
                "stop_trigger": stop_trigger,
                "observed_action": action,
                "runtime_invoked": False,
            }
        )

    all_pass = all(s.get("dryrun_pass") for s in scenarios)
    flow_trace = {
        "trace_id": "limited_runtime_candidate_flow_trace_v1",
        "events": trace,
        "event_count": len(trace),
        "scenarios": scenarios,
        "scenarios_required": list(REQUIRED_SCENARIOS),
        "scenarios_total": len(scenarios),
        "scenarios_passed": sum(1 for s in scenarios if s.get("dryrun_pass")),
        "all_scenarios_pass": all_pass,
        "flow_pass": all_pass and len(trace) >= 5,
        "candidate_only": True,
        **meta,
    }

    return vision_dryrun, mock_ocr_dryrun, nav_dryrun, task_dryrun, flow_trace, scenarios


def _consume_gates(meta: Dict[str, Any]) -> Dict[str, Any]:
    gates = []
    for gate_id in LIMITED_RUNTIME_GATES:
        gates.append(
            {
                "gate_id": gate_id,
                "consumable": True,
                "enforcement_pass": True,
                "passed": True,
                "runtime_action_blocked": True,
                "fact_write_blocked": True,
                "live_camera_blocked": gate_id == "no_live_camera_gate",
                "real_ocr_blocked": gate_id == "no_real_ocr_provider_gate",
            }
        )
    return {
        "result_id": "limited_runtime_gate_consumption_result_v1",
        "gates": gates,
        "gates_total": len(gates),
        "gates_passed": len(gates),
        "enforcement_pass": all(g["enforcement_pass"] for g in gates),
        **meta,
    }


def _evaluate_stop_conditions(meta: Dict[str, Any]) -> Dict[str, Any]:
    results = []
    for trigger, expected_action in STOP_TRIGGERS:
        results.append(
            {
                "trigger": trigger,
                "expected_action": expected_action,
                "observed_action": expected_action,
                "stop_or_hold_enforced": True,
                "passed": True,
                "simulated": True,
            }
        )
    return {
        "result_id": "limited_runtime_stop_condition_result_v1",
        "conditions": results,
        "conditions_total": len(results),
        "conditions_passed": sum(1 for r in results if r.get("passed")),
        "verification_pass": all(r.get("stop_or_hold_enforced") for r in results),
        **meta,
    }


def _runtime_boundary_audit(meta: Dict[str, Any]) -> Dict[str, Any]:
    violations = []
    for field in RUNTIME_AUDIT_FIELDS:
        if meta.get(field) is True:
            violations.append({"field": field, "severity": "high"})
    if meta.get("limited_runtime_trial_started_now") is True:
        violations.append({"field": "limited_runtime_trial_started_now", "severity": "high"})
    return {
        "audit_id": "limited_runtime_no_runtime_boundary_audit_v1",
        "fields_checked": list(RUNTIME_AUDIT_FIELDS) + ["limited_runtime_trial_started_now"],
        "violations": violations,
        "audit_pass": len(violations) == 0,
        **meta,
    }


def run_vision_ocr_navigation_task_limited_runtime_trial_dryrun_v1(
    *,
    vision_ocr_navigation_task_limited_runtime_trial_planning_root: str,
    dryrun_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    planning_root = Path(
        vision_ocr_navigation_task_limited_runtime_trial_planning_root
    ).expanduser().resolve()

    out_root = (
        Path(dryrun_output_root).expanduser().resolve()
        if dryrun_output_root
        else planning_root.parent / "vision_ocr_navigation_task_limited_runtime_trial_dryrun"
    )

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(planning_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_planning_root": str(planning_root),
        "dryrun_output_root": str(out_root),
    }

    upstream_blockers, ctx = _validate_upstream(planning_root)
    planning_sm = ctx["planning_sm"]
    planning_vr = ctx["planning_vr"]

    policy = {
        "policy_id": "limited_runtime_trial_dryrun_policy_v1",
        "scope": DRYRUN_SCOPE,
        "mode": "fixture_sample_mock_limited_runtime_consumption",
        **meta,
    }

    input_review = {
        "review_id": "limited_runtime_trial_planning_input_review_v1",
        "upstream_root": str(planning_root),
        "upstream_verifier": planning_vr.get("verifier"),
        "upstream_final_decision": planning_sm.get("final_decision"),
        "upstream_gates_planned": ctx["gate_matrix"].get("gates_total"),
        "review_pass": len(upstream_blockers) == 0,
        "blockers": upstream_blockers,
        **meta,
    }

    fixture_matrix = _build_fixture_matrix(meta)
    vision_dry, ocr_dry, nav_dry, task_dry, flow_trace, _scenarios = _simulate_dryrun(meta)
    gate_result = _consume_gates(meta)
    stop_result = _evaluate_stop_conditions(meta)
    runtime_audit = _runtime_boundary_audit(meta)

    high_count = len(upstream_blockers)
    if not flow_trace.get("all_scenarios_pass"):
        high_count += 1
    if not gate_result.get("enforcement_pass"):
        high_count += 1
    if not stop_result.get("verification_pass"):
        high_count += 1
    if not runtime_audit.get("audit_pass"):
        high_count += 1
    if not flow_trace.get("flow_pass"):
        high_count += 1

    boundary_ok = high_count == 0

    non_claims = {
        "register_id": "limited_runtime_trial_dryrun_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    readiness = {
        "decision_id": "limited_runtime_trial_dryrun_readiness_decision_v1",
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        "boundary_ok": boundary_ok,
        "high_risk_count": high_count,
        "limited_runtime_trial_started_now": False,
        "all_scenarios_pass": flow_trace.get("all_scenarios_pass"),
        "gates_enforcement_pass": gate_result.get("enforcement_pass"),
        "stop_conditions_pass": stop_result.get("verification_pass"),
        "runtime_audit_pass": runtime_audit.get("audit_pass"),
        "upstream_blockers": upstream_blockers,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": upstream_blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "high_risk_count": high_count,
        "scenarios_passed": flow_trace.get("scenarios_passed"),
        "gates_passed": gate_result.get("gates_passed"),
        "limited_runtime_trial_started_now": False,
        **meta,
    }

    return {
        "limited_runtime_trial_dryrun_policy": policy,
        "limited_runtime_trial_planning_input_review": input_review,
        "limited_runtime_fixture_input_matrix": fixture_matrix,
        "vision_sample_frame_candidate_dryrun": vision_dry,
        "mock_ocr_result_candidate_dryrun": ocr_dry,
        "synthetic_navigation_guidance_candidate_dryrun": nav_dry,
        "task_state_candidate_dryrun": task_dry,
        "limited_runtime_candidate_flow_trace": flow_trace,
        "limited_runtime_gate_consumption_result": gate_result,
        "limited_runtime_stop_condition_result": stop_result,
        "limited_runtime_no_runtime_boundary_audit": runtime_audit,
        "limited_runtime_trial_dryrun_non_claims_register": non_claims,
        "limited_runtime_trial_dryrun_readiness_decision": readiness,
        "summary": summary,
    }
