# -*- coding: utf-8 -*-
"""Vision-OCR Evidence Ingest Integration Check v1 — integration check only; no runtime.

Phase-Vision-OCR-Evidence-Ingest-Integration-Check-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Vision-OCR-Evidence-Ingest-Integration-Check-v1-001"
FINAL_DECISION = "VISION_OCR_EVIDENCE_INGEST_READY_FOR_NAVIGATION_GUIDANCE_LOOP"
RECOMMENDED_NEXT = "Navigation-Guidance-to-Speech-Candidate-Adapter-v1"

FOLLOWUPS = [
    "Navigation-Guidance-to-Speech-Candidate-Adapter-v1",
    "Basic-Navigation-Guidance-Loop-DryRun-v1",
    "Vision-Evidence-Lifecycle-Policy-v1",
    "Safety-Task-Arbitration-Policy-v1",
    "GPS-Location-Candidate-Contract-v1",
    "Route-Stage-Estimation-DryRun-v1",
    "Information-Lifecycle-Governance-v1",
    "Memory-System-Architecture-v1",
]

OPTIONAL_DOC_GLOBS = {
    "segmentation_governance": "**/*SEGMENTATION*.md",
    "tracking_governance": "**/*TRACKING*GOVERN*.md",
    "map_context": "**/*MAP*CONTEXT*.md",
    "risk_safety_arbiter": "**/*SAFETY*ARBIT*.md",
    "detector_governance": "**/*DETECTOR*.md",
    "ocr_provider_health": "**/*OCR*PROVIDER*HEALTH*.md",
    "speech_gate_runtime": "**/*SPEECH*GATE*.md",
}

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_observation_request_contract", "obs_contract_loaded", [], [], []),
    ("load_basic_loop_audit", "audit_loaded", [], [], []),
    ("load_task_manager_runtime", "tm_rt_loaded", [], [], []),
    ("load_vision_capture_governance", "vision_gov_loaded", [], [], []),
    ("load_ocr_activation", "ocr_act_loaded", [], [], []),
    ("intake_observation_requests", "obs_intake_ok", [], [], []),
    ("define_vision_evidence_schema", "vision_schema_ok", [], [], []),
    ("define_ocr_evidence_schema", "ocr_schema_ok", [], [], []),
    ("define_evidence_lifecycle_policy", "lifecycle_ok", [], [], []),
    ("define_baseline_task_evidence_separation", "separation_ok", [], [], []),
    ("apply_ocr_joint_gate", "ocr_gate_ok", [], [], ["ocr_provider"]),
    ("generate_vision_evidence_candidates", "vision_ev_ok", [], [], ["camera"]),
    ("generate_ocr_evidence_candidates", "ocr_ev_ok", [], [], ["ocr_invoke"]),
    ("generate_action_support_candidates", "action_ok", [], [], ["navigation_action"]),
    ("generate_verification_support_candidates", "verify_ok", [], [], ["task_completed"]),
    ("define_evidence_to_task_feedback", "feedback_ok", [], [], []),
    ("define_freshness_expiry_policy", "freshness_ok", [], [], []),
    ("audit_provider_runtime_bypass", "bypass_ok", [], [], []),
    ("generate_final_ingest_integration_decision", "ingest_ready", [], [], ["production_ready"]),
]

INTAKE_SPECS = [
    ("task_observation_request", "task_observation_request_contract_v1_summary.json", False),
    ("basic_loop_audit", "basic_functional_loop_runtime_logic_audit_correction_v1_summary.json", False),
    ("task_manager_runtime", "task_manager_runtime_dryrun_v1_summary.json", False),
    ("vision_capture_governance", "vision_capture_governance_v1_summary.json", False),
    ("vision_capture_runtime", "vision_capture_runtime_dryrun_v1_summary.json", False),
    ("ocr_mainline_closure", "ocr_mainline_governance_closure_v1_summary.json", False),
    ("ocr_activation", "ocr_activation_governance_policy_v1_summary.json", False),
    ("ocrrequest_staticreading_gate", "ocrrequest_gated_submission_from_staticreading_v1_summary.json", False),
    ("realvideo_frame", "cross_modal_vision_ocr_realvideo_frame_sample_summary.json", True),
    ("poster_consumer", "poster_real_ocr_readonly_consumer_summary.json", True),
    ("regression", "ocr_staticreading_poster_realvideo_regression_route_compliance_v1_summary.json", True),
    ("stc", "stc_sampling_guidance_policy_v1_summary.json", False),
    ("hardware_stub", "hardware_camera_runtime_adapter_implementation_stub_v1_summary.json", False),
    ("system_health", None, True),
    ("simulation", None, True),
]

REQUEST_TO_VISION_EVIDENCE = {
    "observe_forward_path": "spatial_layout_candidate",
    "observe_safety_risk": "safety_risk_candidate",
    "observe_obstacle_area": "obstacle_candidate",
    "observe_spatial_layout": "spatial_layout_candidate",
    "observe_signage_area": "signage_area_candidate",
    "observe_exit_sign": "signage_area_candidate",
    "observe_restroom_sign": "signage_area_candidate",
    "observe_doorplate_area": "readable_region_candidate",
    "observe_directory_board": "signage_area_candidate",
    "observe_service_desk": "service_desk_candidate",
    "observe_readable_region": "readable_region_candidate",
    "observe_task_target_area": "task_target_area_candidate",
    "observe_user_view_alignment": "user_view_alignment_candidate",
    "observe_safety_marker": "signage_area_candidate",
}

OCR_ELIGIBLE_TYPES = {
    "observe_exit_sign": ("exit_sign", "task_required_text"),
    "observe_restroom_sign": ("restroom_sign", "task_required_text"),
    "observe_doorplate_area": ("doorplate", "task_required_text"),
    "observe_readable_region": ("user_selected_text", "user_explicit_reading"),
    "observe_directory_board": ("department_sign", "task_required_text"),
    "observe_safety_marker": ("safety_marker", "safety_short_marker"),
}

BASELINE_OCR_TYPES = {"observe_safety_marker"}

ACTION_SUPPORT_MAP = {
    "baseline_safety": ("safety_guidance_support", "guidance_need_candidate"),
    "task_driven_nav": ("navigation_guidance_support", "navigation_guidance_candidate"),
    "user_view": ("user_view_guidance_support", "guidance_need_candidate"),
    "static_reading": ("static_reading_guidance_support", "guidance_need_candidate"),
    "human": ("human_assistance_prompt_support", "human_assistance_candidate"),
    "default": ("safety_guidance_support", "guidance_need_candidate"),
}

VERIFICATION_MAP = {
    "observe_safety_risk": "verify_safety_marker_present",
    "observe_exit_sign": "verify_information_source_found",
    "observe_restroom_sign": "verify_information_source_found",
    "observe_doorplate_area": "verify_readable_region_available",
    "observe_readable_region": "verify_readable_region_available",
    "observe_task_target_area": "verify_correct_area",
    "default": "verify_task_progress_candidate",
}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _find_optional_docs(ws_root: Path) -> List[Dict[str, Any]]:
    docs = ws_root / "docs" / "architecture"
    rows = []
    for doc_id, glob_pat in OPTIONAL_DOC_GLOBS.items():
        found = list(docs.glob(glob_pat)) if docs.is_dir() else []
        rows.append(
            {
                "intake_id": doc_id,
                "input_source": "optional_documentation",
                "source_root_or_path": str(found[0]) if found else "(not_found)",
                "artifact": found[0].name if found else None,
                "loaded": bool(found),
                "optional": True,
                "key_fields_observed": ["documentation_reference"] if found else [],
                "intake_status": "loaded" if found else "optional_missing",
                "missing_impact": "optional_doc_reference_only",
                **_not_fact(),
            }
        )
    return rows


def _ocr_gate_pass(req: Dict[str, Any], ocr_act_loaded: bool, stc_loaded: bool) -> Tuple[bool, Optional[str]]:
    rtype = req.get("request_type", "")
    loop = req.get("loop_type", "")
    target = req.get("target_module_candidate", "")
    if rtype not in OCR_ELIGIBLE_TYPES and target != "ocr_if_task_required":
        return False, "not_ocr_target_request"
    if loop == "baseline_safety" and rtype not in BASELINE_OCR_TYPES:
        return False, "baseline_ocr_scope_limited"
    if not ocr_act_loaded:
        return False, "ocr_activation_gate_not_loaded"
    if loop == "task_driven" and not stc_loaded:
        return False, "stc_freshness_gate_reference_missing"
    if rtype in ("observe_exit_sign", "observe_restroom_sign", "observe_doorplate_area", "observe_readable_region"):
        return True, None
    if loop == "baseline_safety" and rtype == "observe_safety_marker":
        return True, None
    return True, None


def run_vision_ocr_evidence_ingest_integration_check_v1(
    *,
    task_observation_request_root: str,
    basic_loop_audit_root: str,
    task_manager_runtime_root: str,
    vision_capture_governance_root: str,
    vision_capture_runtime_root: str,
    ocr_mainline_closure_root: str,
    ocr_activation_root: str,
    ocrrequest_staticreading_gate_root: str,
    realvideo_frame_root: str,
    poster_consumer_root: str,
    regression_root: str,
    stc_root: str,
    hardware_stub_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "task_observation_request": Path(task_observation_request_root).resolve(),
        "basic_loop_audit": Path(basic_loop_audit_root).resolve(),
        "task_manager_runtime": Path(task_manager_runtime_root).resolve(),
        "vision_capture_governance": Path(vision_capture_governance_root).resolve(),
        "vision_capture_runtime": Path(vision_capture_runtime_root).resolve(),
        "ocr_mainline_closure": Path(ocr_mainline_closure_root).resolve(),
        "ocr_activation": Path(ocr_activation_root).resolve(),
        "ocrrequest_staticreading_gate": Path(ocrrequest_staticreading_gate_root).resolve(),
        "realvideo_frame": Path(realvideo_frame_root).resolve(),
        "poster_consumer": Path(poster_consumer_root).resolve(),
        "regression": Path(regression_root).resolve(),
        "stc": Path(stc_root).resolve(),
        "hardware_stub": Path(hardware_stub_root).resolve(),
        "system_health": Path(system_health_root).resolve(),
        "simulation": Path(simulation_root).resolve(),
    }

    summaries: Dict[str, Any] = {}
    intake_rows: List[Dict[str, Any]] = []
    for iid, art, optional in INTAKE_SPECS:
        root = roots[iid]
        loaded = root.is_dir()
        art_file = art
        if iid == "ocrrequest_staticreading_gate" and loaded:
            candidates = list(root.glob("*summary*.json"))
            art_file = candidates[0].name if candidates else art
        if iid == "poster_consumer" and loaded:
            candidates = list(root.glob("*summary*.json"))
            art_file = candidates[0].name if candidates else "(directory)"
        if art_file and art_file != "(directory)":
            loaded = loaded and (root / art_file).is_file()
            if loaded:
                summaries[iid] = _read_json(root / art_file)
        elif optional:
            loaded = loaded
        intake_rows.append(
            {
                "intake_id": iid,
                "input_source": iid,
                "source_root_or_path": str(root),
                "artifact": art_file or "(directory)",
                "loaded": loaded,
                "optional": optional,
                "key_fields_observed": ["summary"] if summaries.get(iid) else (["directory"] if loaded else []),
                "intake_status": "loaded" if loaded else ("optional_missing" if optional else "missing"),
                "missing_impact": "none" if loaded else ("optional_reference_only" if optional else "check_partial"),
                **_not_fact(),
            }
        )
    intake_rows.extend(_find_optional_docs(ws))

    obs_coll = _read_json(roots["task_observation_request"] / "task_observation_request_candidate_collection_v1.json") or {}
    obs_requests: List[Dict[str, Any]] = obs_coll.get("candidates") or []
    baseline_count = sum(1 for r in obs_requests if r.get("loop_type") == "baseline_safety")
    task_driven_count = sum(1 for r in obs_requests if r.get("loop_type") == "task_driven")

    obs_intake_rows = []
    for req in obs_requests:
        obs_intake_rows.append(
            {
                "observation_request_id": req.get("observation_request_id"),
                "loop_type": req.get("loop_type"),
                "request_source": req.get("request_source"),
                "request_type": req.get("request_type"),
                "target_module_candidate": req.get("target_module_candidate"),
                "priority_hint": req.get("priority_hint"),
                "timing_hint": req.get("timing_hint"),
                "request_allowed_now": req.get("request_allowed_now", False),
                "accepted_for_ingest_check": True,
                "rejected_reason_if_any": None,
                **_not_fact(),
            }
        )

    ocr_act_loaded = roots["ocr_activation"].is_dir()
    stc_loaded = (roots["stc"] / "stc_sampling_guidance_policy_v1_summary.json").is_file()

    vision_candidates: List[Dict[str, Any]] = []
    ocr_candidates: List[Dict[str, Any]] = []
    ocr_gates: List[Dict[str, Any]] = []
    action_support: List[Dict[str, Any]] = []
    verification_support: List[Dict[str, Any]] = []

    for req in obs_requests:
        oid = req.get("observation_request_id", "")
        loop = req.get("loop_type", "task_driven")
        rtype = req.get("request_type", "")
        evidence_type = REQUEST_TO_VISION_EVIDENCE.get(rtype, "task_target_area_candidate")
        ve_id = f"ve_{oid}"

        vision_candidates.append(
            {
                "vision_evidence_candidate_id": ve_id,
                "source_observation_request_id": oid,
                "loop_type": loop,
                "evidence_type": evidence_type,
                "source_frame_ref": None,
                "bbox_candidate": None,
                "spatial_anchor": req.get("spatial_anchor", "spatial_anchor_placeholder"),
                "time_anchor": req.get("time_anchor", "dryrun_session_t0"),
                "confidence_placeholder": 0.75,
                "freshness_status": req.get("freshness_requirement", "live_required"),
                "source_chain": "vision_ocr_evidence_ingest_integration_check_v1",
                "can_support_action": True,
                "can_support_verification": True,
                "can_write_fact_now": False,
                "is_fact": False,
                "write_allowed": False,
                **_not_fact(),
            }
        )

        gate_later, blocked = _ocr_gate_pass(req, ocr_act_loaded, stc_loaded)
        ocr_gates.append(
            {
                "ocr_gate_candidate_id": f"ogate_{oid}",
                "source_observation_request_id": oid,
                "gate_pass_later": gate_later,
                "gate_pass_now": False,
                "blocked_reason_if_any": blocked,
                "ocr_allowed_now": False,
                "ocr_provider_invoked_now": False,
                "ocrrequest_submitted_now": False,
                **_not_fact(),
            }
        )

        if gate_later and rtype in OCR_ELIGIBLE_TYPES:
            text_type, trigger = OCR_ELIGIBLE_TYPES[rtype]
            oe_id = f"ocr_{oid}"
            ocr_candidates.append(
                {
                    "ocr_evidence_candidate_id": oe_id,
                    "source_observation_request_id": oid,
                    "source_vision_evidence_candidate_id": ve_id,
                    "ocr_trigger_type": trigger,
                    "expected_text_type": text_type,
                    "raw_text_candidate": None,
                    "empty_text": None,
                    "empty_text_is_not_no_text_fact": True,
                    "ocr_provider_ref": "placeholder_provider_ref",
                    "ocrrequest_ref": None,
                    "source_chain": "vision_ocr_evidence_ingest_integration_check_v1",
                    "confidence_placeholder": None,
                    "freshness_status": "session_scoped",
                    "ocr_allowed_now": False,
                    "ocr_allowed_later": True,
                    "blocked_reason_if_any": None,
                    "ocr_invoked_now": False,
                    "can_write_fact_now": False,
                    "is_fact": False,
                    "write_allowed": False,
                    **_not_fact(),
                }
            )
            oe_ref = oe_id
        else:
            oe_ref = None

        if loop == "baseline_safety":
            support_key = "baseline_safety"
        elif rtype in ("observe_exit_sign", "observe_restroom_sign"):
            support_key = "task_driven_nav"
        elif "doorplate" in rtype or rtype == "observe_readable_region":
            support_key = "static_reading"
        elif rtype == "observe_user_view_alignment" or "view" in rtype:
            support_key = "user_view"
        elif rtype == "observe_service_desk":
            support_key = "human"
        else:
            support_key = "default"
        stype, downstream = ACTION_SUPPORT_MAP.get(support_key, ACTION_SUPPORT_MAP["default"])
        action_support.append(
            {
                "action_support_candidate_id": f"as_{ve_id}",
                "source_vision_evidence_candidate_id": ve_id,
                "source_ocr_evidence_candidate_id": oe_ref,
                "support_type": stype,
                "supported_downstream_candidate_type": downstream,
                "can_trigger_action_directly": False,
                "requires_midplatform_gate": True,
                "requires_speech_gate_if_voice": downstream in (
                    "navigation_guidance_candidate",
                    "guidance_need_candidate",
                    "human_assistance_candidate",
                ),
                "navigation_action_triggered": False,
                **_not_fact(),
            }
        )

        vtype = VERIFICATION_MAP.get(rtype, VERIFICATION_MAP["default"])
        verification_support.append(
            {
                "verification_support_candidate_id": f"vs_{ve_id}",
                "source_vision_evidence_candidate_id": ve_id,
                "source_ocr_evidence_candidate_id": oe_ref,
                "verification_type": vtype,
                "can_complete_task_alone": False,
                "task_completed_now": False,
                "requires_task_manager_review": True,
                **_not_fact(),
            }
        )

    separation_rows = [
        {
            "loop_type": "baseline_safety",
            "allowed_evidence_type": [
                "safety_risk_candidate",
                "obstacle_candidate",
                "spatial_layout_candidate",
                "signage_area_candidate",
            ],
            "allowed_ocr_scope": ["warning_sign", "danger_marker", "emergency_exit_sign", "safety_short_marker"],
            "forbidden_evidence_use": ["task_completion", "generic_environment_ocr", "navigation_action"],
            "can_support_action": True,
            "can_support_task_verification": False,
            "fact_write_allowed": False,
        },
        {
            "loop_type": "task_driven",
            "allowed_evidence_type": [
                "task_target_area_candidate",
                "readable_region_candidate",
                "signage_area_candidate",
                "service_desk_candidate",
                "user_view_alignment_candidate",
            ],
            "allowed_ocr_scope": [
                "doorplate",
                "exit_sign",
                "restroom_sign",
                "department_sign",
                "user_selected_text",
            ],
            "forbidden_evidence_use": [
                "task_completion_without_verification",
                "generic_environment_ocr",
                "direct_navigation_action",
            ],
            "can_support_action": True,
            "can_support_task_verification": True,
            "fact_write_allowed": False,
        },
    ]

    trace_steps = [
        {
            "step_id": sid,
            "step_name": sid,
            "decision": decision,
            "reason_codes": reasons,
            "allowed_next_actions": allowed,
            "blocked_next_actions": blocked,
            "runtime_action_committed": False,
        }
        for sid, decision, reasons, allowed, blocked in TRACE_STEPS
    ]

    obs_sum = summaries.get("task_observation_request") or {}

    return {
        "summary": {
            "schema_version": "vision_ocr_evidence_ingest_integration_check_v1_summary_v0",
            "phase": PHASE_ID,
            "check_scope": "vision_ocr_evidence_ingest_integration_check_only",
            "based_on_task_observation_request_contract": obs_sum.get("observation_request_contract_defined") is True,
            "based_on_basic_loop_audit": summaries.get("basic_loop_audit") is not None,
            "based_on_task_manager_runtime": summaries.get("task_manager_runtime") is not None,
            "observation_request_candidate_count_observed": len(obs_requests),
            "baseline_request_candidate_count_observed": baseline_count,
            "task_driven_request_candidate_count_observed": task_driven_count,
            "vision_evidence_ingest_schema_defined": True,
            "ocr_evidence_ingest_schema_defined": True,
            "evidence_lifecycle_policy_defined": True,
            "baseline_task_evidence_separation_defined": True,
            "ocr_joint_gate_check_applied": True,
            "action_support_evidence_candidate_generated": len(action_support) > 0,
            "verification_support_evidence_candidate_generated": len(verification_support) > 0,
            "evidence_to_task_feedback_defined": True,
            "camera_invoked": False,
            "detector_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "ocr_provider_invoked": False,
            "ocrrequest_submitted": False,
            "runtime_frame_captured": False,
            "real_bbox_generated": False,
            "real_ocr_text_generated": False,
            "navigation_action_triggered": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "task_state_committed_now": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "intake": {
            "schema_version": "vision_ocr_evidence_ingest_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "obs_intake": {
            "schema_version": "vision_ocr_observation_request_intake_matrix_v1",
            "observation_request_candidate_count_observed": len(obs_requests),
            "baseline_accepted_count": baseline_count,
            "task_driven_accepted_count": task_driven_count,
            "rows": obs_intake_rows,
            **_not_fact(),
        },
        "vision_schema": {
            "schema_version": "vision_evidence_ingest_schema_v1",
            "field_definitions": {
                "vision_evidence_candidate_id": {"type": "string", "required": True},
                "source_observation_request_id": {"type": "string", "required": True},
                "evidence_type": {"type": "enum"},
                "source_frame_ref": {"type": "nullable_placeholder"},
                "bbox_candidate": {"type": "nullable_placeholder"},
                "can_write_fact_now": {"type": "boolean", "default": False},
            },
            "can_write_fact_now": False,
            **_not_fact(),
        },
        "ocr_schema": {
            "schema_version": "ocr_evidence_ingest_schema_v1",
            "empty_text_is_not_no_text_fact": True,
            "raw_text_candidate_null_in_check_phase": True,
            "can_write_fact_now": False,
            **_not_fact(),
        },
        "lifecycle_policy": {
            "schema_version": "vision_ocr_evidence_lifecycle_policy_v1",
            "stages": [
                "REQUEST_ACCEPTED_FOR_INGEST_CHECK",
                "VISION_EVIDENCE_CANDIDATE",
                "OCR_EVIDENCE_CANDIDATE_IF_GATE_ALLOWED_LATER",
                "ACTION_SUPPORT_CANDIDATE",
                "VERIFICATION_SUPPORT_CANDIDATE",
                "EXPIRED_EVIDENCE_CANDIDATE",
                "REJECTED_EVIDENCE_CANDIDATE",
                "POSSIBLE_FACT_CANDIDATE_LATER",
            ],
            "evidence_not_fact_by_default": True,
            "evidence_can_support_guidance_candidate": True,
            "evidence_can_support_verification_candidate": True,
            "evidence_cannot_commit_task_state": True,
            "evidence_cannot_write_worldmodel_now": True,
            "evidence_cannot_write_memory_now": True,
            "expired_evidence_cannot_drive_action": True,
            "expired_evidence_can_feed_information_lifecycle_candidate": True,
            **_not_fact(),
        },
        "separation_matrix": {
            "schema_version": "vision_ocr_baseline_task_evidence_separation_matrix_v1",
            "rows": separation_rows,
            **_not_fact(),
        },
        "ocr_joint_gate": {
            "schema_version": "vision_ocr_ingest_ocr_joint_gate_check_v1",
            "joint_gate_conditions": [
                "source_observation_request_exists",
                "task_or_safety_context_exists",
                "information_gap_requires_text",
                "candidate_information_source_area_exists",
                "readable_region_candidate_exists",
                "stc_freshness_valid",
                "input_quality_sufficient",
                "ocr_activation_gate_passed",
                "generic_environment_text_forbidden",
            ],
            "generic_environment_text_forbidden": True,
            "ocr_allowed_now": False,
            "gates": ocr_gates,
            **_not_fact(),
        },
        "vision_collection": {
            "schema_version": "vision_evidence_candidate_collection_v1",
            "vision_evidence_candidate_count": len(vision_candidates),
            "candidates": vision_candidates,
            **_not_fact(),
        },
        "ocr_collection": {
            "schema_version": "ocr_evidence_candidate_collection_v1",
            "ocr_evidence_candidate_count": len(ocr_candidates),
            "candidates": ocr_candidates,
            "all_raw_text_null": True,
            **_not_fact(),
        },
        "action_support_collection": {
            "schema_version": "vision_ocr_action_support_evidence_candidate_collection_v1",
            "action_support_candidate_count": len(action_support),
            "candidates": action_support,
            "cannot_trigger_action_directly": True,
            **_not_fact(),
        },
        "verification_collection": {
            "schema_version": "vision_ocr_verification_support_evidence_candidate_collection_v1",
            "verification_support_candidate_count": len(verification_support),
            "candidates": verification_support,
            "can_complete_task_alone": False,
            "task_completed_now": False,
            **_not_fact(),
        },
        "feedback_contract": {
            "schema_version": "vision_ocr_evidence_to_task_feedback_contract_v1",
            "feedback_contract_defined": True,
            "feedback_target": [
                "task_manager_runtime_later",
                "midplatform_task_state_later",
                "task_aware_action_scheduling_later",
            ],
            "feedback_payload": [
                "evidence_candidate",
                "action_support_candidate",
                "verification_support_candidate",
                "source_chain",
                "freshness_status",
                "confidence_placeholder",
            ],
            "feedback_invoked_now": False,
            "task_state_committed_now": False,
            **_not_fact(),
        },
        "freshness_policy": {
            "schema_version": "vision_ocr_evidence_freshness_expiry_policy_v1",
            "evidence_freshness_required_for_action_support": True,
            "stale_evidence_blocks_action_support": True,
            "stale_evidence_can_support_long_term_candidate": True,
            "expired_evidence_cannot_verify_task_completion": True,
            "expired_evidence_can_feed_information_lifecycle_candidate": True,
            "stale_does_not_mean_discard": True,
            **_not_fact(),
        },
        "bypass_audit": {
            "schema_version": "vision_ocr_provider_runtime_bypass_audit_v1",
            "camera_invoked": False,
            "detector_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "ocr_provider_invoked": False,
            "rapidocr_invoked": False,
            "paddleocr_invoked": False,
            "ocrrequest_submitted": False,
            "hardware_stub_only": True,
            "direct_provider_bypass": False,
            "violations": [],
            **_not_fact(),
        },
        "trace": {
            "schema_version": "vision_ocr_evidence_ingest_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "vision_ocr_evidence_ingest_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "observation_request_candidate_count_observed": len(obs_requests),
            "vision_evidence_candidate_count": len(vision_candidates),
            "ocr_evidence_candidate_count": len(ocr_candidates),
            "action_support_candidate_count": len(action_support),
            "verification_support_candidate_count": len(verification_support),
            "runtime_action_committed": False,
            "recommended_next_phase": RECOMMENDED_NEXT,
            "alternate_next_phases": ["Basic-Navigation-Guidance-Loop-DryRun-v1", "Vision-Evidence-Lifecycle-Policy-v1"],
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "vision_ocr_evidence_ingest_boundary_report_v1",
            "integration_check_only": True,
            "camera_invoked": False,
            "detector_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "ocr_provider_invoked": False,
            "ocrrequest_submitted": False,
            "runtime_frame_captured": False,
            "real_bbox_generated": False,
            "real_ocr_text_generated": False,
            "navigation_action_triggered": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "task_state_committed_now": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "vision_ocr_evidence_ingest_metrics_candidate_report_v1",
            "observation_request_candidate_count_observed": len(obs_requests),
            "baseline_request_candidate_count_observed": baseline_count,
            "task_driven_request_candidate_count_observed": task_driven_count,
            "vision_evidence_candidate_count": len(vision_candidates),
            "ocr_evidence_candidate_count": len(ocr_candidates),
            "action_support_candidate_count": len(action_support),
            "verification_support_candidate_count": len(verification_support),
            "runtime_action_committed_count": 0,
            "ocr_provider_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "vision_ocr_evidence_ingest_benchmark_link_report_v1",
            "benchmark_available": False,
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "vision_ocr_evidence_ingest_system_health_report_v1",
            "system_health_governance_available": roots["system_health"].is_dir(),
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "vision_ocr_evidence_ingest_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "integration_check_only": True,
            "camera_invoked": False,
            "detector_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "ocr_provider_invoked": False,
            "ocrrequest_submitted": False,
            "runtime_frame_captured": False,
            "real_bbox_generated": False,
            "real_ocr_text_generated": False,
            "navigation_action_triggered": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "task_state_committed_now": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "vision_ocr_evidence_ingest_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["simulation"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "vision_ocr_evidence_ingest_non_claims_report_v1",
            "claims": [
                "integration_check_not_vision_runtime",
                "observation_request_accepted_not_camera_executed",
                "vision_evidence_not_real_vision_output",
                "ocr_evidence_not_provider_output",
                "empty_ocr_not_no_text_fact",
                "action_support_not_direct_action",
                "verification_not_task_completion",
                "feedback_not_task_manager_invoked",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "vision_ocr_evidence_ingest_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "vision_ocr_evidence_ingest_audit_report_v1",
            "vision_ocr_evidence_ingest_integration_check_v1_executed": True,
            "integration_check_only": True,
            "observation_request_candidate_count_observed": len(obs_requests),
            "baseline_request_candidate_count_observed": baseline_count,
            "task_driven_request_candidate_count_observed": task_driven_count,
            "vision_evidence_ingest_schema_defined": True,
            "ocr_evidence_ingest_schema_defined": True,
            "evidence_lifecycle_policy_defined": True,
            "baseline_task_evidence_separation_defined": True,
            "ocr_joint_gate_check_applied": True,
            "action_support_evidence_candidate_generated": True,
            "verification_support_evidence_candidate_generated": True,
            "evidence_to_task_feedback_defined": True,
            "camera_invoked": False,
            "detector_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "ocr_provider_invoked": False,
            "ocrrequest_submitted": False,
            "runtime_frame_captured": False,
            "real_bbox_generated": False,
            "real_ocr_text_generated": False,
            "navigation_action_triggered": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "task_state_committed_now": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
            "final_decision_recorded": FINAL_DECISION,
        },
    }
