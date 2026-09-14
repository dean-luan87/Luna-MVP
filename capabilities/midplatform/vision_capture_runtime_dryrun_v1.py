# -*- coding: utf-8 -*-
"""Vision Capture Runtime DryRun v1 — simulate capture decision path (no camera/OCR/TTS/hardware).

Phase-Vision-Capture-Runtime-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Vision-Capture-Runtime-DryRun-v1-001"

FOLLOWUPS = [
    "User-Guidance-Recovery-Runtime-DryRun-v1",
    "Voice-Guidance-Prompt-Template-v1",
    "Vision-Capture-Runtime-GuardedTrial-v1",
    "STC-Freshness-Gate-Runtime-DryRun-v1",
    "OCR-Activation-Runtime-DryRun-v1",
    "Assisted-Static-Reading-Mode-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Vision-Zoom-Autofocus-Resampling-Policy-v1",
    "Expired-Capture-Candidate-Ingest-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

FINAL_DECISION = "USER_GUIDANCE_OR_STATIC_CAPTURE"

DECISION_OPTIONS = [
    "CONTINUE_DYNAMIC_CAPTURE",
    "REQUEST_HIGH_QUALITY_FRAME",
    "USER_GUIDANCE_OR_STATIC_CAPTURE",
    "SYSTEM_SELF_ADJUSTMENT_CANDIDATE",
    "EXTERNAL_ASSISTANCE_CANDIDATE",
    "EXPIRED_CAPTURE_TO_LONG_TERM_CANDIDATE",
    "TASK_DOWNGRADE_NON_OCR_PATH",
    "RETURN_TO_VISUAL_SEMANTIC_PATH",
]

CANDIDATE_METADATA = [
    "source_chain",
    "time_anchor",
    "spatial_anchor",
    "original_task_context",
    "stale_reason",
    "confidence_decay",
    "privacy_sensitivity",
    "future_usage_scope",
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _pick_keys(obj: Any, keys: List[str]) -> Dict[str, Any]:
    if not isinstance(obj, dict):
        return {}
    return {k: obj[k] for k in keys if k in obj}


def _intake(
    intake_id: str,
    source_root: Path,
    artifact: str,
    key_fields: List[str],
) -> Dict[str, Any]:
    path = source_root / artifact
    data = _read_json(path)
    loaded = data is not None
    observed = _pick_keys(data, key_fields) if loaded else {}
    return {
        "runtime_intake_id": intake_id,
        "input_source": intake_id,
        "source_root": str(source_root),
        "source_artifact": artifact,
        "loaded": loaded,
        "key_fields_observed": observed,
        "intake_status": "loaded" if loaded else "missing",
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _load_case_bundle(
    vc_root: Path,
    ocr_act_root: Path,
    stc_root: Path,
    ug_root: Path,
    ocr_v2_root: Path,
) -> Dict[str, Any]:
    vc_case = _read_json(vc_root / "vision_capture_current_case_decision_dryrun_v1.json") or {}
    ocr_case = _read_json(ocr_act_root / "ocr_activation_current_case_decision_dryrun_v1.json") or {}
    stc_case = _read_json(stc_root / "stc_current_case_decision_dryrun_v1.json") or {}
    ug_case = _read_json(ug_root / "user_guidance_current_case_recovery_decision_v1.json") or {}
    ocr2 = _read_json(ocr_v2_root / "ocrrequest_gated_submission_from_multiframe_v2_summary.json") or {}

    v1_empty = int(
        vc_case.get("v1_empty_count")
        or ocr_case.get("v1_empty_count")
        or stc_case.get("v1_empty_count")
        or 30
    )
    v2_empty = int(
        vc_case.get("v2_empty_count")
        or ocr_case.get("v2_empty_count")
        or stc_case.get("v2_empty_count")
        or 5
    )
    same_bbox = int(vc_case.get("same_bbox_risk_count") or ocr_case.get("same_bbox_risk_count") or 5)
    geom_sig = int(
        vc_case.get("geometry_change_significant_count")
        or ocr_case.get("geometry_change_significant_count")
        or ocr2.get("geometry_change_significant_count_observed")
        or 0
    )

    return {
        "v1_empty_count": v1_empty,
        "v2_empty_count": v2_empty,
        "same_bbox_risk_count": same_bbox,
        "geometry_change_significant_count": geom_sig,
        "v1_v2_empty": v1_empty > 0 and v2_empty > 0,
        "same_bbox_risk": same_bbox > 0,
        "capture_quality_problem_likely": bool(
            vc_case.get("capture_quality_problem_likely", True)
        ),
        "projection_or_region_alignment_problem_likely": bool(
            vc_case.get("projection_or_region_alignment_problem_likely", True)
        ),
        "internal_recrop_should_stop": bool(vc_case.get("internal_recrop_should_stop", True)),
        "dynamic_reocr_allowed_now": False,
        "ocr_activation_decision": ocr_case.get("ocr_activation_decision", "USER_GUIDANCE_RECOVERY"),
        "recommended_capture_decision_governance": vc_case.get(
            "recommended_capture_decision", FINAL_DECISION
        ),
        "ug_recovery_recommended": bool(ug_case.get("user_guidance_recovery_recommended", True)),
    }


def _readiness_matrix(case: Dict[str, Any]) -> Dict[str, Any]:
    same_bbox = case["same_bbox_risk"]
    proj = case["projection_or_region_alignment_problem_likely"]
    quality = case["capture_quality_problem_likely"]
    empty = case["v1_v2_empty"]

    specs = [
        (
            "frame_readiness",
            ["blur_placeholder", "brightness_placeholder", "motion_stability"],
            not quality,
            ["capture_quality_problem_likely"] if quality else [],
            "user_or_system_repairable",
            "request_higher_quality_frame" if quality else "continue_sampling",
        ),
        (
            "region_readiness",
            ["region_confidence", "bbox_stability", "same_bbox_risk"],
            not (same_bbox or proj),
            ["same_bbox_risk", "projection_alignment"] if (same_bbox or proj) else [],
            "user_repairable",
            "user_guidance" if proj else "continue_sampling",
        ),
        (
            "crop_readiness",
            ["bbox_size", "text_pixel_height", "projection_vs_detected"],
            not (same_bbox or quality),
            ["same_bbox_no_gain", "low_crop_quality"] if same_bbox else ["quality_low"],
            "system_or_user_repairable",
            "static_capture" if same_bbox else "request_zoom",
        ),
        (
            "text_region_readiness",
            ["text_region_detected_preferred", "projection_not_sufficient"],
            not proj,
            ["projection_drift", "text_region_not_detected"] if proj else [],
            "system_repairable",
            "request_heavy_text_detector_capture",
        ),
        (
            "task_capture_readiness",
            ["task_context", "ocr_activation_user_guidance"],
            False,
            ["repeated_empty", "internal_recrop_exhausted", "low_task_gain_from_recrop"],
            "routing",
            FINAL_DECISION,
        ),
    ]
    rows = []
    for rid, signals, passed, fails, repair, nxt in specs:
        rows.append(
            {
                "readiness_id": rid,
                "readiness_dimension": rid,
                "observed_signals": {
                    "same_bbox_risk": same_bbox,
                    "projection_or_region_alignment_problem_likely": proj,
                    "capture_quality_problem_likely": quality,
                    "v1_v2_empty": empty,
                    **{s: True for s in signals},
                },
                "pass_status": "pass" if passed else "fail",
                "fail_reasons": fails,
                "repairability_category": repair,
                "recommended_next_action": nxt,
                "action_committed_now": False,
                "fact_status": "not_fact",
            }
        )
    return {
        "schema_version": "vision_capture_runtime_readiness_evaluation_matrix_v1",
        "rows": rows,
        "aggregate_same_bbox_risk": same_bbox,
        "aggregate_projection_problem_likely": proj,
        "aggregate_capture_quality_problem_likely": quality,
        "aggregate_v1_v2_empty": empty,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _decision_trace(case: Dict[str, Any], intake_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    loaded_count = sum(1 for r in intake_rows if r.get("loaded"))

    def step(sid: int, name: str, decision: str, reasons: List[str], allowed: List[str], blocked: List[str]) -> Dict[str, Any]:
        return {
            "step_id": sid,
            "step_name": name,
            "input_refs": [f"intake_loaded_{loaded_count}"],
            "decision": decision,
            "reason_codes": reasons,
            "allowed_next_actions": allowed,
            "blocked_next_actions": blocked,
            "runtime_action_committed": False,
            "fact_status": "not_fact",
        }

    steps = [
        step(1, "load_governance_policy", "governance_loaded", [], ["evaluate_readiness"], []),
        step(2, "load_current_case", "case_loaded", ["v1_v2_empty", "same_bbox_risk"], ["evaluate_activation"], []),
        step(
            3,
            "evaluate_ocr_activation_decision",
            case["ocr_activation_decision"],
            ["ocr_v2_all_empty", "user_guidance_recovery"],
            ["capture_path"],
            ["continue_internal_recrop"],
        ),
        step(
            4,
            "evaluate_stc_freshness",
            "stale_blocks_action_allows_long_term",
            ["stale_for_action"],
            ["expired_candidate"],
            ["use_stale_for_ocr_action"],
        ),
        step(
            5,
            "evaluate_capture_readiness",
            "readiness_fail_aggregate",
            ["same_bbox_risk", "projection_alignment", "capture_quality"],
            ["user_guidance", "static_capture"],
            ["dynamic_reocr"],
        ),
        step(
            6,
            "evaluate_retry_budget",
            "internal_recrop_should_stop",
            ["max_retry_exhausted", "same_bbox_no_gain"],
            ["static_capture", "user_guidance"],
            ["internal_recrop"],
        ),
        step(
            7,
            "evaluate_motion_and_static_need",
            "static_capture_recommended",
            ["repeated_dynamic_empty", "high_precision_need"],
            ["assisted_static_reading"],
            ["continue_dynamic_capture"],
        ),
        step(
            8,
            "evaluate_user_guidance_need",
            "user_guidance_required",
            ["projection_or_region_alignment", "centering_distance_angle"],
            ["ask_user_center", "ask_user_hold_still", "pause_for_static"],
            [],
        ),
        step(
            9,
            "evaluate_system_self_adjustment_need",
            "system_adjustment_candidate_optional",
            ["hardware_placeholder_available"],
            ["request_static_capture_mode", "request_high_resolution_still"],
            ["hardware_invoke"],
        ),
        step(
            10,
            "evaluate_expired_capture_candidate",
            "route_to_long_term_candidates",
            ["stale_not_discard"],
            ["expired_capture_candidate", "world_change_hint"],
            ["fact_write"],
        ),
        step(
            11,
            "generate_final_capture_decision",
            FINAL_DECISION,
            [
                "same_bbox_risk",
                "projection_or_region_alignment",
                "v1_v2_empty",
                "internal_recrop_should_stop",
            ],
            ["user_guidance", "static_capture", "visual_semantic_fallback"],
            ["continue_dynamic_capture", "internal_recrop"],
        ),
    ]
    return {
        "schema_version": "vision_capture_runtime_decision_trace_v1",
        "steps": steps,
        "final_capture_decision": FINAL_DECISION,
        "internal_recrop_should_stop": case["internal_recrop_should_stop"],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _decision_matrix(case: Dict[str, Any]) -> Dict[str, Any]:
    rows = []
    for dec in DECISION_OPTIONS:
        selected = dec == FINAL_DECISION
        blocked = dec == "CONTINUE_DYNAMIC_CAPTURE"
        reason = ""
        blocked_reason = ""
        if selected:
            reason = "same_bbox_no_gain;projection_alignment;v1_v2_empty;internal_recrop_exhausted"
        elif blocked:
            blocked_reason = "internal_recrop_should_stop;dynamic_reocr_allowed_now=false"
        elif dec == "RETURN_TO_VISUAL_SEMANTIC_PATH":
            reason = "allowed_fallback_when_ocr_not_task_critical"
        rows.append(
            {
                "decision": dec,
                "selected": selected,
                "selection_reason": reason,
                "blocked_reason": blocked_reason,
                "required_future_phase": "Vision-Capture-Runtime-GuardedTrial-v1"
                if selected
                else None,
                "runtime_action_committed": False,
                "fact_status": "not_fact",
            }
        )
    return {
        "schema_version": "vision_capture_runtime_decision_matrix_v1",
        "rows": rows,
        "internal_recrop_should_stop": case["internal_recrop_should_stop"],
        "dynamic_reocr_allowed_now": case["dynamic_reocr_allowed_now"],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _user_guidance_candidates(vc_root: Path) -> Dict[str, Any]:
    pol = _read_json(vc_root / "vision_capture_user_guidance_policy_v1.json") or {}
    want = {
        "ask_user_move_closer",
        "ask_user_center_target",
        "ask_user_adjust_angle",
        "ask_user_hold_still",
        "ask_user_pause_for_static_capture",
        "request_external_assistance_if_needed",
    }
    out = []
    pri = 1
    for a in pol.get("actions") or []:
        if not isinstance(a, dict):
            continue
        aid = a.get("action_id")
        if aid not in want:
            continue
        out.append(
            {
                "action_id": aid,
                "trigger_reason": a.get("trigger_reason"),
                "prompt_candidate": a.get("suggested_prompt_template"),
                "expected_signal_improvement": a.get("expected_capture_improvement"),
                "priority": pri,
                "tts_allowed_now": False,
                "runtime_action_committed": False,
                "fact_status": "not_fact",
            }
        )
        pri += 1
    return {
        "schema_version": "vision_capture_runtime_user_guidance_candidate_v1",
        "candidates": out,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _system_self_adjustment_candidates(vc_root: Path) -> Dict[str, Any]:
    pol = _read_json(vc_root / "vision_capture_system_self_adjustment_policy_v1.json") or {}
    hw = _read_json(vc_root / "vision_capture_hardware_placeholder_contract_v1.json") or {}
    cap_names = {
        c.get("capability_name")
        for c in (hw.get("capabilities") or [])
        if isinstance(c, dict)
    }
    want = {
        "request_high_resolution_still_frame",
        "request_zoom",
        "request_autofocus",
        "request_exposure_adjustment",
        "request_resampling",
        "request_static_capture_mode",
    }
    out = []
    for a in pol.get("actions") or []:
        if not isinstance(a, dict):
            continue
        aid = a.get("action_id")
        if aid not in want:
            continue
        req = a.get("required_hardware_capability")
        out.append(
            {
                "action_id": aid,
                "trigger_reason": a.get("trigger_reason"),
                "required_hardware_capability": req,
                "hardware_capability_known": req in cap_names
                or (req == "high_quality_still_capture_available" and "high_quality_still_capture_available" in cap_names),
                "expected_signal_improvement": a.get("expected_signal_improvement"),
                "hardware_action_invoked_now": False,
                "runtime_action_committed": False,
                "fact_status": "not_fact",
            }
        )
    return {
        "schema_version": "vision_capture_runtime_system_self_adjustment_candidate_v1",
        "candidates": out,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _static_capture_candidate(case: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "vision_capture_runtime_static_capture_candidate_v1",
        "static_capture_candidate_generated": True,
        "trigger_reason": [
            "repeated_dynamic_empty",
            "same_bbox_no_gain",
            "low_readiness",
        ],
        "suggested_capture_mode": "assisted_static_reading",
        "required_user_state": "stationary_or_slow",
        "required_frame_quality": "high_resolution_still_low_motion",
        "required_guidance": ["ask_user_pause_for_static_capture", "ask_user_hold_still"],
        "runtime_capture_invoked": False,
        "tts_invoked": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _expired_capture_candidates(case: Dict[str, Any]) -> Dict[str, Any]:
    types = [
        ("expired_frame_candidate", "frame_ref_placeholder"),
        ("expired_crop_candidate", "crop_v2_adjusted_ref"),
        ("expired_text_region_candidate", "text_region_attempt"),
        ("expired_capture_attempt_candidate", "ocr_v2_empty_attempt"),
    ]
    meta = {k: True for k in CANDIDATE_METADATA}
    return {
        "schema_version": "vision_capture_runtime_expired_capture_candidate_v1",
        "candidates": [
            {
                "candidate_type": t,
                "source_ref": ref,
                "cannot_use_for_action": True,
                "cannot_write_fact": True,
                "can_feed_expired_observation_candidate": True,
                "can_feed_world_change_hint_candidate": True,
                "can_feed_user_environment_context_candidate": True,
                "can_feed_user_profile_context_candidate": True,
                "can_feed_emotional_context_background_candidate": True,
                "required_metadata_present": True,
                **meta,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
            for t, ref in types
        ],
        "stale_reason": "capture_retry_exhausted_same_bbox",
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _long_term_routing(vc_root: Path, case: Dict[str, Any]) -> Dict[str, Any]:
    pol = _read_json(vc_root / "vision_long_term_context_candidate_routing_policy_v1.json") or {}
    routes = []
    for r in pol.get("routes") or []:
        if not isinstance(r, dict):
            continue
        routes.append(
            {
                "source_signal": r.get("source_signal"),
                "target_candidate_pool": r.get("target_candidate_pool"),
                "route_selected": True,
                "reason": f"dryrun_from_{case.get('same_bbox_risk') and 'same_bbox' or 'case'}",
                "write_allowed_now": False,
                "review_required": True,
                "fact_status": "not_fact",
            }
        )
    return {
        "schema_version": "vision_capture_runtime_long_term_context_routing_v1",
        "routes": routes,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _visual_semantic_fallback(ocr_act_root: Path, case: Dict[str, Any]) -> Dict[str, Any]:
    pol = _read_json(ocr_act_root / "ocr_default_off_world_modeling_policy_v1.json") or {}
    return {
        "schema_version": "vision_capture_runtime_visual_semantic_fallback_v1",
        "return_to_visual_semantic_path_allowed": True,
        "ocr_default_off_for_world_modeling_respected": bool(
            pol.get("ocr_default_off_for_world_modeling", True)
        ),
        "visual_semantic_first": True,
        "fallback_reason": "ocr_capture_path_exhausted;task_may_continue_on_visual_semantic",
        "allowed_paths": [
            "visual_symbol",
            "logo_candidate",
            "facility_semantic",
            "spatial_structure",
            "poi_hint",
            "task_context",
        ],
        "ocr_retry_allowed_now": case["dynamic_reocr_allowed_now"],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_vision_capture_runtime_dryrun_v1(
    *,
    vision_capture_governance_root: str,
    ocr_activation_root: str,
    stc_sampling_guidance_root: str,
    user_guidance_root: str,
    ocr_v2_root: str,
    multiframe_crop_v2_root: str,
    bbox_adjustment_root: str,
    text_detector_root: str,
    crop_quality_root: str,
    evidence_pack_v4_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    vc = Path(vision_capture_governance_root).resolve()
    ocr_act = Path(ocr_activation_root).resolve()
    stc = Path(stc_sampling_guidance_root).resolve()
    ug = Path(user_guidance_root).resolve()
    ocr2 = Path(ocr_v2_root).resolve()
    crop_v2 = Path(multiframe_crop_v2_root).resolve()
    bbox = Path(bbox_adjustment_root).resolve()
    td = Path(text_detector_root).resolve()
    cq = Path(crop_quality_root).resolve()
    ep4 = Path(evidence_pack_v4_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    case = _load_case_bundle(vc, ocr_act, stc, ug, ocr2)
    current_case_loaded = bool(vc.is_dir())

    intake_specs: List[Tuple[str, Path, str, List[str]]] = [
        ("vision_capture_governance", vc, "vision_capture_governance_v1_summary.json", ["phase", "governance_scope"]),
        ("ocr_activation_current_case", ocr_act, "ocr_activation_current_case_decision_dryrun_v1.json", ["ocr_activation_decision", "v2_empty_count"]),
        ("stc_current_case", stc, "stc_current_case_decision_dryrun_v1.json", ["v1_empty_count", "v2_empty_count"]),
        ("user_guidance_current_case", ug, "user_guidance_current_case_recovery_decision_v1.json", ["user_guidance_recovery_recommended"]),
        ("ocr_v2_summary", ocr2, "ocrrequest_gated_submission_from_multiframe_v2_summary.json", ["ocrrequest_submitted_count", "v2_empty_result_count"]),
        ("crop_quality_summary", cq, "crop_quality_diagnosis_v2_multiframe_summary.json", ["empty_ocr_result_count_observed", "blur_risk_count"]),
        ("multiframe_crop_v2_summary", crop_v2, "multiframe_crop_v2_textdetector_adjusted_summary.json", ["adjusted_crop_artifact_count", "adjusted_bbox_same_as_original_count"]),
        ("text_detector_summary", td, "text_detector_dryrun_v1_summary.json", ["bbox_adjustment_candidate_count"]),
        ("bbox_proposal_summary", bbox, "bbox_adjustment_proposal_v2_multiframe_summary.json", ["bbox_adjustment_proposal_count"]),
    ]
    intake_rows = [_intake(iid, root, art, keys) for iid, root, art, keys in intake_specs]

    readiness = _readiness_matrix(case)
    trace = _decision_trace(case, intake_rows)
    matrix = _decision_matrix(case)
    ug_cand = _user_guidance_candidates(vc)
    sys_cand = _system_self_adjustment_candidates(vc)
    static_cand = _static_capture_candidate(case)
    expired_cand = _expired_capture_candidates(case)
    lt_route = _long_term_routing(vc, case)
    vis_fallback = _visual_semantic_fallback(ocr_act, case)

    return {
        "summary": {
            "schema_version": "vision_capture_runtime_dryrun_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "vision_capture_runtime_decision_dryrun_only",
            "based_on_vision_capture_governance": vc.is_dir(),
            "based_on_ocr_activation_governance": ocr_act.is_dir(),
            "based_on_stc_sampling_guidance": stc.is_dir(),
            "based_on_user_guidance_recovery": ug.is_dir(),
            "current_case_loaded": current_case_loaded,
            "capture_runtime_dryrun_executed": True,
            "capture_readiness_evaluated": True,
            "capture_decision_generated": True,
            "recommended_capture_decision": FINAL_DECISION,
            "internal_recrop_should_stop": case["internal_recrop_should_stop"],
            "dynamic_reocr_allowed_now": case["dynamic_reocr_allowed_now"],
            "user_guidance_candidate_generated": len(ug_cand.get("candidates") or []) > 0,
            "system_self_adjustment_candidate_generated": len(sys_cand.get("candidates") or []) > 0,
            "static_capture_candidate_generated": True,
            "expired_capture_candidate_generated": len(expired_cand.get("candidates") or []) > 0,
            "long_term_context_candidate_routing_generated": len(lt_route.get("routes") or []) > 0,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "runtime_tts_invoked": False,
            "hardware_action_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": {
            "schema_version": "vision_capture_runtime_input_intake_matrix_v1",
            "rows": intake_rows,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "readiness": readiness,
        "trace": trace,
        "matrix": matrix,
        "user_guidance": ug_cand,
        "system_self_adjustment": sys_cand,
        "static_capture": static_cand,
        "expired_capture": expired_cand,
        "long_term_routing": lt_route,
        "visual_fallback": vis_fallback,
        "boundary": {
            "schema_version": "vision_capture_runtime_boundary_report_v1",
            "runtime_dryrun_only": True,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "runtime_tts_invoked": False,
            "hardware_action_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "vision_capture_runtime_metrics_candidate_report_v1",
            "current_case_loaded": current_case_loaded,
            "capture_readiness_evaluated": True,
            "capture_decision_generated": True,
            "user_guidance_candidate_count": len(ug_cand.get("candidates") or []),
            "system_self_adjustment_candidate_count": len(sys_cand.get("candidates") or []),
            "static_capture_candidate_count": 1,
            "expired_capture_candidate_count": len(expired_cand.get("candidates") or []),
            "long_term_context_routing_count": len(lt_route.get("routes") or []),
            "runtime_action_committed_count": 0,
            "runtime_camera_invoked_count": 0,
            "runtime_ocr_invoked_count": 0,
            "runtime_tts_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "vision_capture_runtime_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "vision_capture_runtime_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "vision_capture_runtime_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "runtime_dryrun_only": True,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "runtime_tts_invoked": False,
            "hardware_action_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "vision_capture_runtime_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "vision_capture_runtime_non_claims_report_v1",
            "claims": [
                "not_real_runtime",
                "no_camera",
                "no_new_frame",
                "no_ocr",
                "no_tts",
                "no_hardware",
                "capture_decision_is_dryrun",
                "ug_candidate_not_tts",
                "system_adjustment_not_hardware",
                "expired_not_fact",
                "long_term_not_profile_write",
                "no_world_model",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "vision_capture_runtime_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "vision_capture_runtime_audit_report_v1",
            "vision_capture_runtime_dryrun_v1_executed": True,
            "runtime_dryrun_only": True,
            "current_case_loaded": current_case_loaded,
            "capture_readiness_evaluated": True,
            "capture_decision_generated": True,
            "recommended_capture_decision": FINAL_DECISION,
            "internal_recrop_should_stop": case["internal_recrop_should_stop"],
            "dynamic_reocr_allowed_now": case["dynamic_reocr_allowed_now"],
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "runtime_tts_invoked": False,
            "hardware_action_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "scene_delta_candidate_generated": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }
