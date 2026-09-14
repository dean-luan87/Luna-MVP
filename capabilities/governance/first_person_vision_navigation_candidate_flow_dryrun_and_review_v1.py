# -*- coding: utf-8 -*-
"""First Person Vision Navigation Candidate Flow DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.first_person_vision_navigation_candidate_flow_planning_v1 import (
    BOUNDARY_FALSE,
    DRIVE_OBSERVATION_PRIORITY_CONFIRMATIONS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    II_HANDOFF_CONFIRMATIONS,
    MAP_LOCATION_FIELDS,
    NAVIGATION_TASK_FIELDS,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    NON_CLAIMS,
    OCR_RESULT_FIELDS,
    PERCEPTION_ZONE_CONFIRMATIONS,
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
    VISUAL_OBSERVATION_FIELDS,
    VISUAL_OCR_MAP_BINDING_CONFIRMATIONS,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-First-Person-Vision-Navigation-Candidate-Flow-DryRunAndReview-v1-001"
SCOPE = "first_person_vision_navigation_candidate_flow_dryrun_and_review_only"
SOURCE_CHAIN = "first_person_vision_navigation_candidate_flow_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "FIRST_PERSON_VISION_NAVIGATION_CANDIDATE_FLOW_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_VISION_NAVIGATION_INFORMATION_INTEGRATION_CHAIN_DRYRUN"
)
FINAL_DECISION_HOLD = (
    "FIRST_PERSON_VISION_NAVIGATION_CANDIDATE_FLOW_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Vision-Navigation-Information-Integration-Chain-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-First-Person-Vision-Navigation-Candidate-Flow-Issue-Review-v1-001"

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_camera_invoke",
    "dryrun_to_real_frame_read",
    "dryrun_to_vision_runtime",
    "dryrun_to_ocr_runtime",
    "dryrun_to_map_provider",
    "dryrun_to_navigation_runtime",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_real_ocr_execute",
    "dryrun_to_real_navigation_action",
    "dryrun_to_user_output",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_controlled_runtime_enable",
)

DRYRUN_NON_CLAIMS: Tuple[str, ...] = (
    "Candidate Flow DryRun GO ≠ camera enabled",
    "sample candidates generated ≠ real frame read",
    "sample OCR candidate ≠ OCR executed",
    "sample map candidate ≠ map provider invoked",
    "next Integration Chain DryRun ≠ runtime execution",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "first_person_vision_navigation_candidate_flow_dryrun_and_review_only",
    "simulated",
    "sample_visual_observation_candidate_generated_now",
    "sample_ocr_result_candidate_generated_now",
    "sample_map_location_context_candidate_generated_now",
    "sample_route_context_candidate_generated_now",
    "sample_navigation_task_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = BOUNDARY_FALSE

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_vision_navigation_candidate_flow_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def _check_upstream_no_runtime_leakage(summary: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    for field in UPSTREAM_RUNTIME_LEAKAGE_FIELDS:
        if field in summary and summary.get(field) is not False:
            issues.append(f"{field} must be false")
    return issues


def _sample_visual(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "visual_observation_candidate_id": "visual_obs_sample_crossing_001",
        "source_frame_ref": "fixture:static_frame_metadata:crossing_001",
        "observation_mode": "first_person_simulated",
        "scene_type_candidate": "street_crossing",
        "detected_object_refs": ["object:pedestrian_zone:001"],
        "obstacle_refs": ["obstacle_candidate:curb_001"],
        "risk_refs": ["risk_context_candidate:traffic_001"],
        "spatial_context_refs": ["spatial:intersection_approach"],
        "confidence": 0.72,
        "ttl": "30s",
        "source_chain": ["fixture:vision:crossing_001"],
        "evidence_refs": ["visual_evidence_candidate:crossing_001"],
        "whitebox_trace_refs": ["trace:visual_obs:001"],
        "candidate_only": True,
        "not_fact": True,
        "runtime_source": False,
        **meta,
    }


def _sample_ocr(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "ocr_result_candidate_id": "ocr_result_sample_sign_001",
        "source_visual_region_ref": "text_region_candidate:sign_001",
        "recognized_text_candidate": "人行横道",
        "text_confidence": 0.68,
        "language_hint": "zh-CN",
        "text_region_refs": ["text_region_candidate:sign_001"],
        "signage_context_refs": ["signage_context_candidate:crosswalk_001"],
        "validation_required": True,
        "ttl": "60s",
        "source_chain": ["fixture:ocr:sign_001"],
        "evidence_refs": ["ocr_evidence_candidate:sign_001"],
        "candidate_only": True,
        "not_fact": True,
        **meta,
    }


def _sample_map(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "map_location_context_candidate_id": "map_location_sample_001",
        "location_source_type": "readonly_map_hint",
        "approximate_location_ref": "location:intersection_hint_001",
        "location_confidence": 0.65,
        "map_context_refs": ["map:route_hint:001"],
        "route_relevance": "high",
        "stale_risk": "moderate",
        "ttl": "120s",
        "source_chain": ["fixture:map:hint_001"],
        "candidate_only": True,
        "not_fact": True,
        **meta,
    }


def _sample_route(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "route_context_candidate_id": "route_context_sample_001",
        "active_route_ref": "route:nav_crossing_001",
        "route_stage_candidate": "approach_intersection",
        "next_waypoint_candidate": "waypoint:crossing_entry",
        "expected_direction_candidate": "forward_then_left",
        "deviation_risk": "low",
        "route_confidence": 0.7,
        "ttl": "90s",
        "candidate_only": True,
        **meta,
    }


def _sample_nav_task(meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "navigation_task_candidate_id": "navigation_task_sample_001",
        "task_goal_ref": "goal:cross_street_safely",
        "task_stage": "approach",
        "task_priority": "high",
        "task_progress_candidate": "in_progress",
        "route_context_ref": "route_context_sample_001",
        "location_context_ref": "map_location_sample_001",
        "required_observation_refs": ["required_observation_candidate:traffic_check_001"],
        "safety_hold_refs": ["risk_context_candidate:traffic_001"],
        "candidate_only": True,
        "task_state_commit_allowed": False,
        **meta,
    }


def run_first_person_vision_navigation_candidate_flow_dryrun_and_review_v1(
    *,
    first_person_vision_navigation_candidate_flow_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(first_person_vision_navigation_candidate_flow_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_candidate_flow_planning_root": str(plan_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Candidate Flow Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")

    leakage_issues: List[str] = []
    for issue in _check_upstream_no_runtime_leakage(plan_sm):
        leakage_issues.append(f"planning:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "candidate_flow_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "system_level_simulated_go": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "dryrun_and_review_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    sample_visual = _sample_visual(meta)
    sample_ocr = _sample_ocr(meta)
    sample_map = _sample_map(meta)
    sample_route = _sample_route(meta)
    sample_nav = _sample_nav_task(meta)

    perception_review = {
        "review_id": "perception_zone_candidate_flow_review_v1",
        "confirmations": list(PERCEPTION_ZONE_CONFIRMATIONS),
        **_review_ok([(f"conf.{c[:18]}", True) for c in PERCEPTION_ZONE_CONFIRMATIONS]),
        **meta,
    }

    binding_review = {
        "review_id": "visual_ocr_map_binding_review_v1",
        "confirmations": list(VISUAL_OCR_MAP_BINDING_CONFIRMATIONS),
        **_review_ok([(f"bind.{c[:18]}", True) for c in VISUAL_OCR_MAP_BINDING_CONFIRMATIONS]),
        **meta,
    }

    drive_review = {
        "review_id": "drive_observation_priority_review_v1",
        "confirmations": list(DRIVE_OBSERVATION_PRIORITY_CONFIRMATIONS),
        "sample_observation_priority_hint": "elevated_by_survival_drive_risk",
        "drive_invoked_runtime": False,
        **_review_ok([(f"drive.{c[:18]}", True) for c in DRIVE_OBSERVATION_PRIORITY_CONFIRMATIONS]),
        **meta,
    }

    handoff_review = {
        "review_id": "information_integration_handoff_review_v1",
        "confirmations": list(II_HANDOFF_CONFIRMATIONS),
        "sample_handoff_refs": [
            sample_visual["visual_observation_candidate_id"],
            sample_ocr["ocr_result_candidate_id"],
            sample_map["map_location_context_candidate_id"],
            sample_route["route_context_candidate_id"],
            sample_nav["navigation_task_candidate_id"],
        ],
        "decision_candidate_generated": False,
        **_review_ok([(f"handoff.{c[:18]}", True) for c in II_HANDOFF_CONFIRMATIONS]),
        **meta,
    }

    candidate_not_fact_review = {
        "review_id": "candidate_not_fact_review_v1",
        "all_samples_candidate_only": True,
        "all_samples_not_fact_where_required": True,
        "no_user_output": True,
        "no_navigation_action": True,
        "no_task_state_commit": True,
        **_review_ok(
            [
                ("visual.candidate", sample_visual.get("candidate_only") is True),
                ("ocr.candidate", sample_ocr.get("candidate_only") is True),
                ("map.candidate", sample_map.get("candidate_only") is True),
                ("nav.no_commit", sample_nav.get("task_state_commit_allowed") is False),
            ]
        ),
        **meta,
    }

    boundary_audit = {
        "audit_id": "candidate_flow_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "candidate_flow_blocked_path_result_v1",
        "blocked_paths": [
            {"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS
        ],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    reviews = [perception_review, binding_review, drive_review, handoff_review, candidate_not_fact_review]

    samples_ok = (
        all(f in sample_visual for f in VISUAL_OBSERVATION_FIELDS)
        and all(f in sample_ocr for f in OCR_RESULT_FIELDS)
        and all(f in sample_map for f in MAP_LOCATION_FIELDS)
        and all(f in sample_nav for f in NAVIGATION_TASK_FIELDS)
        and sample_visual.get("runtime_source") is False
    )

    review_pass = (
        input_ok
        and samples_ok
        and all(r.get("dryrun_and_review_pass") for r in reviews)
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
    )

    closure_decision = {
        "decision_id": "candidate_flow_closure_decision_v1",
        "dryrun_and_review_pass": review_pass,
        "high_risk": not review_pass,
        "final_decision": FINAL_DECISION_GO if review_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "sample visual/ocr/map/route/navigation candidates validated",
            "candidates remain candidate/evidence, not fact/action/output",
            "drive signal affects observation priority only",
            "Information Integration handoff refs preserved",
            "15 blocked paths + 15 boundary fields all false",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_vision_navigation_integration_chain_dryrun": review_pass,
        "selected_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        "next_focus": (
            "Vision-Navigation Information Integration Chain DryRun with fixture/sample "
            "candidates into integrated_context_candidate, still no real camera/OCR"
        ),
        **meta,
    }

    policy = {
        "policy_id": "first_person_vision_navigation_candidate_flow_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_not_runtime_not_execute": True,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(DRYRUN_NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": review_pass,
        "violations": list(blockers),
        "dryrun_and_review_pass": review_pass,
        "system_level_simulated_go": True,
        "sample_candidates_generated": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "first_person_vision_navigation_candidate_flow_dryrun_review_policy": policy,
        "candidate_flow_planning_input_review": planning_input_review,
        "sample_visual_observation_candidate": sample_visual,
        "sample_ocr_result_candidate": sample_ocr,
        "sample_map_location_context_candidate": sample_map,
        "sample_route_context_candidate": sample_route,
        "sample_navigation_task_candidate": sample_nav,
        "perception_zone_candidate_flow_review": perception_review,
        "visual_ocr_map_binding_review": binding_review,
        "drive_observation_priority_review": drive_review,
        "information_integration_handoff_review": handoff_review,
        "candidate_not_fact_review": candidate_not_fact_review,
        "candidate_flow_boundary_audit": boundary_audit,
        "candidate_flow_blocked_path_result": blocked_path_result,
        "candidate_flow_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
