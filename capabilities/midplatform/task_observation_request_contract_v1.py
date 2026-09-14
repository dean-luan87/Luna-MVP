# -*- coding: utf-8 -*-
"""Task Observation Request Contract v1 — contract only; no camera/OCR/detector runtime.

Phase-Task-Observation-Request-Contract-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Task-Observation-Request-Contract-v1-001"
FINAL_DECISION = "TASK_OBSERVATION_REQUEST_CONTRACT_READY_FOR_VISION_OCR_INGEST"
RECOMMENDED_NEXT = "Vision-OCR-Evidence-Ingest-Integration-Check-v1"

FOLLOWUPS = [
    "Vision-OCR-Evidence-Ingest-Integration-Check-v1",
    "Basic-Navigation-Guidance-Loop-DryRun-v1",
    "Navigation-Guidance-to-Speech-Candidate-Adapter-v1",
    "Safety-Task-Arbitration-Policy-v1",
    "Vision-Evidence-Lifecycle-Policy-v1",
    "Information-Lifecycle-Governance-v1",
    "Memory-System-Architecture-v1",
    "GPS-Location-Candidate-Contract-v1",
    "Route-Stage-Estimation-DryRun-v1",
]

OPTIONAL_DOC_GLOBS = {
    "risk_safety_arbiter": "**/*SAFETY*ARBIT*.md",
    "navigation_policy": "**/*NAVIGATION*POLICY*.md",
    "map_context": "**/*MAP*CONTEXT*.md",
    "gps_context": "**/*GPS*.md",
    "segmentation_governance": "**/*SEGMENTATION*.md",
    "tracking_governance": "**/*TRACKING*GOVERN*.md",
    "memory_governance": "**/*MEMORY*GOVERN*.md",
    "speech_gate_runtime": "**/*SPEECH*GATE*.md",
}

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_basic_loop_audit", "audit_loaded", [], [], []),
    ("load_task_manager_runtime", "tm_rt_loaded", [], [], []),
    ("load_vision_capture_governance", "vision_gov_loaded", [], [], []),
    ("load_ocr_activation", "ocr_act_loaded", [], [], []),
    ("define_observation_request_schema", "schema_defined", [], [], []),
    ("define_request_source_policy", "source_policy_defined", [], [], []),
    ("define_baseline_safety_request_policy", "baseline_policy_defined", [], [], []),
    ("define_task_driven_request_policy", "task_driven_policy_defined", [], [], []),
    ("define_target_module_routing", "routing_defined", [], [], []),
    ("define_request_gate_policy", "gate_policy_defined", [], [], []),
    ("define_priority_timing_freshness_policy", "ptf_defined", [], [], []),
    ("generate_observation_request_candidates", "candidates_generated", [], [], ["camera", "ocr"]),
    ("define_ocr_request_subpolicy", "ocr_subpolicy_defined", [], [], ["ocr_invoke"]),
    ("define_user_guidance_request_subpolicy", "guidance_subpolicy_defined", [], [], ["tts"]),
    ("define_human_assistance_request_subpolicy", "human_subpolicy_defined", [], [], []),
    ("define_vision_ocr_ingest_handoff", "handoff_defined", [], [], []),
    ("define_request_lifecycle_policy", "lifecycle_defined", [], [], []),
    ("define_safety_task_request_separation", "separation_defined", [], [], []),
    ("generate_final_contract_decision", "contract_ready", [], [], ["production_ready"]),
]

INTAKE_SPECS = [
    ("basic_loop_audit", "basic_functional_loop_runtime_logic_audit_correction_v1_summary.json", False),
    ("task_manager_runtime", "task_manager_runtime_dryrun_v1_summary.json", False),
    ("task_manager_contract", "task_manager_contract_v1_summary.json", False),
    ("midplatform_task_state_runtime", "midplatform_task_state_runtime_dryrun_v1_summary.json", False),
    ("vision_capture_governance", "vision_capture_governance_v1_summary.json", False),
    ("vision_capture_runtime", "vision_capture_runtime_dryrun_v1_summary.json", False),
    ("ocr_activation", "ocr_activation_governance_policy_v1_summary.json", False),
    ("stc", "stc_sampling_guidance_policy_v1_summary.json", False),
    ("voice_guidance_runtime", "voice_guidance_prompt_runtime_dryrun_v1_summary.json", False),
    ("vop_adapter", "voice_output_plane_adapter_for_guidance_v1_summary.json", False),
    ("hardware_stub", "hardware_camera_runtime_adapter_implementation_stub_v1_summary.json", False),
    ("system_health", None, True),
    ("simulation", None, True),
]

REQUEST_SOURCES = [
    "baseline_safety_loop",
    "task_manager_action_schedule",
    "midplatform_task_state",
    "task_context_enrichment",
    "user_guidance_recovery",
    "safety_task_arbitration",
]

REQUEST_TYPES = [
    "observe_forward_path",
    "observe_safety_risk",
    "observe_obstacle_area",
    "observe_spatial_layout",
    "observe_signage_area",
    "observe_exit_sign",
    "observe_restroom_sign",
    "observe_doorplate_area",
    "observe_directory_board",
    "observe_service_desk",
    "observe_readable_region",
    "observe_task_target_area",
    "observe_user_view_alignment",
    "observe_safety_marker",
]

BASELINE_STUBS = [
    ("obs_req_baseline_001", "observe_forward_path", "vision", "P0_safety_immediate", "immediate"),
    ("obs_req_baseline_002", "observe_safety_risk", "vision", "P0_safety_immediate", "immediate"),
    ("obs_req_baseline_003", "observe_obstacle_area", "vision", "P0_safety_immediate", "immediate"),
    ("obs_req_baseline_004", "observe_safety_marker", "ocr_if_task_required", "P0_safety_immediate", "immediate"),
]

TARGET_ROUTES = [
    ("vision", ["observe_forward_path", "observe_safety_risk", "observe_spatial_layout", "observe_task_target_area", "observe_signage_area", "observe_obstacle_area"], ["safety_gate", "vision_capture_gate"]),
    ("ocr_if_task_required", ["observe_readable_region", "observe_doorplate_area", "observe_exit_sign", "observe_restroom_sign", "observe_directory_board", "observe_safety_marker"], ["ocr_activation_gate", "stc_freshness_gate", "task_context_gate"]),
    ("user_guidance", ["observe_user_view_alignment"], ["speech_gate", "task_context_gate"]),
    ("human_assistance", ["observe_service_desk"], ["speech_gate", "human_confirmation_gate"]),
    ("map_reference", [], ["route_context_gate"]),
    ("memory_reference", [], ["memory_reference_gate"]),
]

OBS_TYPE_TO_MODULE = {
    "observe_forward_path": "vision",
    "observe_exit_sign": "ocr_if_task_required",
    "observe_restroom_sign": "ocr_if_task_required",
    "observe_doorplate_area": "ocr_if_task_required",
    "observe_floor_or_wall_sign": "vision",
    "observe_user_view_alignment": "user_guidance",
    "ask_user_to_turn_or_center_view": "user_guidance",
    "ask_user_to_stop_for_static_reading": "user_guidance",
    "observe_service_desk": "human_assistance",
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


def _normalize_request_type(obs_type: str) -> str:
    mapping = {
        "observe_floor_or_wall_sign": "observe_signage_area",
        "ask_user_to_turn_or_center_view": "observe_user_view_alignment",
        "ask_user_to_stop_for_static_reading": "observe_user_view_alignment",
    }
    if obs_type in REQUEST_TYPES:
        return obs_type
    return mapping.get(obs_type, obs_type if obs_type.startswith("observe_") else "observe_task_target_area")


def _candidates_from_tm_runtime(tm_root: Path) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    task_driven: List[Dict[str, Any]] = []
    schedules_by_tobj: Dict[str, str] = {}

    sched_coll = _read_json(tm_root / "task_manager_runtime_action_schedule_candidate_v1.json") or {}
    for s in sched_coll.get("candidates") or []:
        tobj = s.get("source_task_object_candidate_id", "")
        if tobj:
            schedules_by_tobj[tobj] = s.get("action_schedule_candidate_id", "")

    plans = _read_json(tm_root / "task_manager_runtime_task_aware_observation_plan_v1.json") or {}
    for plan in plans.get("candidates") or []:
        obs_type = _normalize_request_type(plan.get("observation_target_type", "observe_task_target_area"))
        sr_id = plan.get("source_spatial_relation_candidate_id", "")
        tobj_ref = sr_id.replace("sr_", "") if sr_id.startswith("sr_") else ""
        gap_id = plan.get("source_information_gap_id", "")
        caps = plan.get("required_sensor_or_capability") or ["vision"]
        target = "ocr_if_task_required" if "ocr_if_task_required" in caps else OBS_TYPE_TO_MODULE.get(obs_type, "vision")
        req_id = f"obs_req_td_{plan.get('observation_plan_candidate_id', 'unknown')}"
        task_driven.append(
            {
                "observation_request_id": req_id,
                "loop_type": "task_driven",
                "request_source": "task_manager_action_schedule",
                "request_type": obs_type,
                "target_module_candidate": target,
                "source_task_object_ref": tobj_ref or None,
                "source_gap_ref": gap_id,
                "source_action_schedule_ref": schedules_by_tobj.get(tobj_ref, ""),
                "source_spatial_relation_ref": sr_id,
                "time_anchor": "dryrun_session_t0",
                "spatial_anchor": "spatial_anchor_dryrun_session",
                "freshness_requirement": "live_required",
                "priority_hint": plan.get("priority_hint", "P1_task_critical"),
                "timing_hint": plan.get("timing_hint", "immediate"),
                "safety_priority_state": "normal",
                "source_chain": "task_observation_request_contract_v1",
                "gate_status": "REQUEST_BLOCKED_BY_GATE",
                "request_allowed_now": False,
                "request_allowed_later": True,
                "camera_invoked_now": False,
                "ocr_invoked_now": False,
                "runtime_action_committed": False,
                **_not_fact(),
            }
        )

    ocr_needs = _read_json(tm_root / "task_manager_runtime_ocr_activation_need_candidate_v1.json") or {}
    for ocr in ocr_needs.get("candidates") or []:
        tobj = ocr.get("source_task_object_candidate_id", "")
        task_driven.append(
            {
                "observation_request_id": f"obs_req_td_ocr_{tobj}",
                "loop_type": "task_driven",
                "request_source": "task_manager_action_schedule",
                "request_type": "observe_readable_region",
                "target_module_candidate": "ocr_if_task_required",
                "source_task_object_ref": tobj,
                "source_gap_ref": ocr.get("source_information_gap_id"),
                "source_action_schedule_ref": schedules_by_tobj.get(tobj, ""),
                "source_spatial_relation_ref": f"sr_{tobj}" if tobj else None,
                "time_anchor": "dryrun_session_t0",
                "spatial_anchor": "spatial_anchor_dryrun_session",
                "freshness_requirement": "live_required",
                "priority_hint": "P3_ocr_guidance",
                "timing_hint": "when_near_target",
                "safety_priority_state": "normal",
                "source_chain": "task_observation_request_contract_v1",
                "gate_status": "REQUEST_READY_LATER",
                "request_allowed_now": False,
                "request_allowed_later": ocr.get("ocr_allowed_later", True),
                "camera_invoked_now": False,
                "ocr_invoked_now": False,
                "runtime_action_committed": False,
                **_not_fact(),
            }
        )

    human_needs = _read_json(tm_root / "task_manager_runtime_human_assistance_need_candidate_v1.json") or {}
    for h in human_needs.get("candidates") or []:
        tobj = h.get("source_task_object_candidate_id", "")
        task_driven.append(
            {
                "observation_request_id": f"obs_req_td_human_{tobj}",
                "loop_type": "task_driven",
                "request_source": "task_manager_action_schedule",
                "request_type": "observe_service_desk",
                "target_module_candidate": "human_assistance",
                "source_task_object_ref": tobj,
                "source_gap_ref": None,
                "source_action_schedule_ref": schedules_by_tobj.get(tobj, ""),
                "source_spatial_relation_ref": f"sr_{tobj}" if tobj else None,
                "time_anchor": "dryrun_session_t0",
                "spatial_anchor": "spatial_anchor_dryrun_session",
                "freshness_requirement": "recent_allowed",
                "priority_hint": "P4_clarification",
                "timing_hint": "after_user_confirmation",
                "safety_priority_state": "normal",
                "source_chain": "task_observation_request_contract_v1",
                "gate_status": "REQUEST_BLOCKED_BY_GATE",
                "request_allowed_now": False,
                "request_allowed_later": True,
                "camera_invoked_now": False,
                "ocr_invoked_now": False,
                "runtime_action_committed": False,
                **_not_fact(),
            }
        )

    return task_driven, list(schedules_by_tobj.values())


def run_task_observation_request_contract_v1(
    *,
    basic_loop_audit_root: str,
    task_manager_runtime_root: str,
    task_manager_contract_root: str,
    midplatform_task_state_root: str,
    vision_capture_governance_root: str,
    vision_capture_runtime_root: str,
    ocr_activation_root: str,
    stc_root: str,
    voice_guidance_runtime_root: str,
    vop_adapter_root: str,
    hardware_stub_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "basic_loop_audit": Path(basic_loop_audit_root).resolve(),
        "task_manager_runtime": Path(task_manager_runtime_root).resolve(),
        "task_manager_contract": Path(task_manager_contract_root).resolve(),
        "midplatform_task_state_runtime": Path(midplatform_task_state_root).resolve(),
        "vision_capture_governance": Path(vision_capture_governance_root).resolve(),
        "vision_capture_runtime": Path(vision_capture_runtime_root).resolve(),
        "ocr_activation": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_root).resolve(),
        "voice_guidance_runtime": Path(voice_guidance_runtime_root).resolve(),
        "vop_adapter": Path(vop_adapter_root).resolve(),
        "hardware_stub": Path(hardware_stub_root).resolve(),
        "system_health": Path(system_health_root).resolve(),
        "simulation": Path(simulation_root).resolve(),
    }

    summaries: Dict[str, Any] = {}
    intake_rows: List[Dict[str, Any]] = []
    for iid, art, optional in INTAKE_SPECS:
        root = roots[iid]
        loaded = root.is_dir()
        if art:
            loaded = loaded and (root / art).is_file()
            if loaded:
                summaries[iid] = _read_json(root / art)
        intake_rows.append(
            {
                "intake_id": iid,
                "input_source": iid,
                "source_root_or_path": str(root),
                "artifact": art or "(directory)",
                "loaded": loaded,
                "optional": optional,
                "key_fields_observed": ["summary"] if loaded and art else [],
                "intake_status": "loaded" if loaded else ("optional_missing" if optional else "missing"),
                "missing_impact": "none" if loaded else ("optional_reference_only" if optional else "contract_partial"),
                **_not_fact(),
            }
        )
    intake_rows.extend(_find_optional_docs(ws))

    audit_sum = summaries.get("basic_loop_audit") or {}
    tm_rt_sum = summaries.get("task_manager_runtime") or {}

    task_driven, _ = _candidates_from_tm_runtime(roots["task_manager_runtime"])

    baseline_candidates = [
        {
            "observation_request_id": rid,
            "loop_type": "baseline_safety",
            "request_source": "baseline_safety_loop",
            "request_type": rtype,
            "target_module_candidate": target,
            "source_task_object_ref": None,
            "source_gap_ref": None,
            "source_action_schedule_ref": None,
            "source_spatial_relation_ref": None,
            "time_anchor": "dryrun_session_t0",
            "spatial_anchor": "spatial_anchor_baseline_session",
            "freshness_requirement": "live_required",
            "priority_hint": pri,
            "timing_hint": timing,
            "safety_priority_state": "baseline_active",
            "source_chain": "task_observation_request_contract_v1",
            "gate_status": "REQUEST_READY_LATER",
            "request_allowed_now": False,
            "request_allowed_later": True,
            "camera_invoked_now": False,
            "ocr_invoked_now": False,
            "runtime_action_committed": False,
            **_not_fact(),
        }
        for rid, rtype, target, pri, timing in BASELINE_STUBS
    ]

    all_candidates = baseline_candidates + task_driven
    baseline_count = len(baseline_candidates)
    task_driven_count = len(task_driven)

    schema = {
        "schema_version": "task_observation_request_schema_v1",
        "field_definitions": {
            "observation_request_id": {"type": "string", "required": True},
            "request_source": {"type": "enum", "values": REQUEST_SOURCES},
            "loop_type": {"type": "enum", "values": ["baseline_safety", "task_driven"]},
            "request_type": {"type": "enum", "values": REQUEST_TYPES},
            "target_module_candidate": {
                "type": "enum",
                "values": ["vision", "ocr_if_task_required", "user_guidance", "human_assistance", "map_reference", "memory_reference"],
            },
            "time_anchor": {"type": "string"},
            "spatial_anchor": {"type": "string"},
            "freshness_requirement": {"type": "enum", "values": ["live_required", "recent_allowed", "stale_blocks_action"]},
            "priority_hint": {"type": "string"},
            "timing_hint": {"type": "string"},
            "safety_priority_state": {"type": "string"},
            "source_chain": {"type": "string", "required": True},
            "request_allowed_now": {"type": "boolean", "default": False},
            "request_allowed_later": {"type": "boolean"},
            "runtime_action_committed": {"type": "boolean", "default": False},
        },
        "example_candidate": all_candidates[0] if all_candidates else {},
        "request_allowed_now": False,
        **_not_fact(),
    }

    routing_rows = [
        {
            "target_module": mod,
            "supported_request_types": types,
            "required_gate": gates,
            "invoked_now": False,
            **_not_fact(),
        }
        for mod, types, gates in TARGET_ROUTES
    ]

    separation_rows = [
        {
            "baseline_request_type": "observe_forward_path",
            "task_driven_request_type": "observe_task_target_area",
            "allowed_without_task": True,
            "requires_task_context": False,
            "allowed_ocr_scope": "safety_short_marker_only",
            "forbidden_use": "task_goal_execution_without_task",
            "safety_priority_above_task": True,
        },
        {
            "baseline_request_type": "observe_safety_risk",
            "task_driven_request_type": "observe_readable_region",
            "allowed_without_task": True,
            "requires_task_context": True,
            "allowed_ocr_scope": "task_or_safety_marker",
            "forbidden_use": "generic_environment_ocr_without_task",
            "safety_priority_above_task": True,
        },
        {
            "baseline_request_type": "observe_safety_marker",
            "task_driven_request_type": "observe_doorplate_area",
            "allowed_without_task": True,
            "requires_task_context": True,
            "allowed_ocr_scope": "limited_safety_or_task_text",
            "forbidden_use": "navigation_action_from_request",
            "safety_priority_above_task": True,
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

    return {
        "summary": {
            "schema_version": "task_observation_request_contract_v1_summary_v0",
            "phase": PHASE_ID,
            "contract_scope": "task_observation_request_contract_only",
            "based_on_basic_loop_audit_correction": audit_sum.get("observation_request_gap_identified") is True,
            "based_on_task_manager_runtime": tm_rt_sum.get("task_aware_action_scheduling_candidates_generated") is True,
            "observation_request_contract_defined": True,
            "observation_request_schema_defined": True,
            "baseline_safety_request_policy_defined": True,
            "task_driven_request_policy_defined": True,
            "target_module_routing_policy_defined": True,
            "request_gate_policy_defined": True,
            "priority_timing_policy_defined": True,
            "vision_ocr_ingest_handoff_defined": True,
            "future_runtime_dryrun_entrypoint_defined": True,
            "camera_invoked": False,
            "ocr_invoked": False,
            "detector_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "map_api_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "navigation_action_triggered": False,
            "task_state_committed_now": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "intake": {
            "schema_version": "task_observation_request_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "schema": schema,
        "source_policy": {
            "schema_version": "task_observation_request_source_policy_v1",
            "baseline_safety_loop_can_generate_request_without_task": True,
            "task_manager_can_generate_task_driven_request": True,
            "midplatform_can_forward_request_candidate": True,
            "voice_cannot_generate_observation_request_directly": True,
            "navigation_guidance_cannot_generate_camera_request_directly": True,
            "memory_reference_cannot_generate_observation_request_directly": True,
            "worldmodel_reference_cannot_generate_observation_request_directly": True,
            "request_requires_source_chain": True,
            **_not_fact(),
        },
        "baseline_policy": {
            "schema_version": "task_observation_baseline_safety_request_policy_v1",
            "baseline_safety_request_allowed_without_task": True,
            "allowed_request_types": [
                "observe_forward_path",
                "observe_safety_risk",
                "observe_obstacle_area",
                "observe_spatial_layout",
                "observe_safety_marker",
            ],
            "limited_safety_ocr_request_allowed_later": True,
            "limited_safety_ocr_scope": [
                "warning_sign",
                "danger_marker",
                "emergency_exit_sign",
                "safety_short_marker",
            ],
            "generic_text_observation_forbidden_without_task": True,
            "task_target_search_forbidden_without_task": True,
            "navigation_action_triggered": False,
            **_not_fact(),
        },
        "task_driven_policy": {
            "schema_version": "task_observation_task_driven_request_policy_v1",
            "task_driven_request_requires_task_context": True,
            "task_driven_request_requires_information_gap": True,
            "task_driven_request_requires_spatial_relation_or_scene_context": True,
            "request_can_target_information_source_area": True,
            "request_can_target_readable_region": True,
            "request_can_target_task_destination_area": True,
            "ocr_target_requires_ocr_activation_gate": True,
            "human_assistance_requires_confirmation": True,
            "safety_gate_required": True,
            "request_allowed_now": False,
            **_not_fact(),
        },
        "routing_policy": {
            "schema_version": "task_observation_target_module_routing_policy_v1",
            "routes": routing_rows,
            **_not_fact(),
        },
        "gate_policy": {
            "schema_version": "task_observation_request_gate_policy_v1",
            "joint_gates": [
                "source_chain_valid",
                "loop_type_valid",
                "safety_gate_pass_or_not_required",
                "task_context_present_if_task_driven",
                "information_gap_present_if_task_driven",
                "stc_freshness_requirement_defined",
                "input_quality_requirement_defined",
                "ocr_activation_gate_required_if_ocr",
                "speech_gate_required_if_user_guidance",
                "human_confirmation_required_if_human_assistance",
                "runtime_adapter_required_if_camera",
            ],
            "request_allowed_now": False,
            **_not_fact(),
        },
        "ptf_policy": {
            "schema_version": "task_observation_priority_timing_freshness_policy_v1",
            "priorities": [
                "P0_safety_immediate",
                "P1_task_critical",
                "P2_navigation_guidance",
                "P3_ocr_guidance",
                "P4_clarification",
                "P5_low_priority",
            ],
            "timing_hints": [
                "immediate",
                "near_target",
                "after_user_confirmation",
                "after_safety_clear",
                "after_task_commit",
                "deferred",
            ],
            "freshness_rules": {
                "live_required": "primary_observation_path",
                "recent_allowed": "secondary_context",
                "stale_blocks_action": True,
                "stale_allows_long_term_candidate": True,
            },
            "safety_priority_above_task": True,
            "stale_request_cannot_drive_action": True,
            "stale_request_can_feed_long_term_candidate": True,
            "request_allowed_now": False,
            **_not_fact(),
        },
        "candidates": {
            "schema_version": "task_observation_request_candidate_collection_v1",
            "observation_request_candidate_count": len(all_candidates),
            "baseline_request_candidate_count": baseline_count,
            "task_driven_request_candidate_count": task_driven_count,
            "request_allowed_now_count": 0,
            "candidates": all_candidates,
            **_not_fact(),
        },
        "ocr_subpolicy": {
            "schema_version": "task_observation_ocr_request_subpolicy_v1",
            "ocr_request_can_only_be_candidate": True,
            "ocr_requires_task_or_safety_short_marker": True,
            "task_ocr_requires_information_gap_text": True,
            "task_ocr_requires_readable_region_candidate": True,
            "task_ocr_requires_stc_freshness": True,
            "task_ocr_requires_input_quality": True,
            "generic_environment_ocr_forbidden": True,
            "ocr_allowed_now": False,
            "ocr_invoked_now": False,
            **_not_fact(),
        },
        "guidance_subpolicy": {
            "schema_version": "task_observation_user_guidance_request_subpolicy_v1",
            "user_guidance_request_allowed_for_view_alignment": True,
            "user_guidance_request_allowed_for_static_reading_posture": True,
            "user_guidance_request_allowed_for_missing_scene_or_target": True,
            "all_user_guidance_output_requires_speech_gate": True,
            "direct_tts_bypass_forbidden": True,
            "tts_invoked_now": False,
            "vop_invoked_now": False,
            **_not_fact(),
        },
        "human_subpolicy": {
            "schema_version": "task_observation_human_assistance_request_subpolicy_v1",
            "human_assistance_request_allowed_as_candidate": True,
            "confirmation_required": True,
            "allowed_assistance_types": [
                "ask_staff_for_location",
                "ask_nearby_person_to_read",
                "ask_user_to_confirm_with_staff",
                "manual_input_by_user",
            ],
            "action_committed_now": False,
            "speech_gate_required": True,
            **_not_fact(),
        },
        "handoff": {
            "schema_version": "task_observation_vision_ocr_ingest_handoff_contract_v1",
            "handoff_defined": True,
            "handoff_target_phase": "Vision-OCR-Evidence-Ingest-Integration-Check-v1",
            "handoff_payload": [
                "observation_request_candidate",
                "loop_type",
                "source_chain",
                "task_context_ref",
                "information_gap_ref",
                "target_module_candidate",
                "priority_hint",
                "timing_hint",
                "freshness_requirement",
                "ocr_subpolicy_ref",
                "safety_state_ref",
            ],
            "handoff_invoked_now": False,
            "vision_runtime_invoked_now": False,
            "ocr_runtime_invoked_now": False,
            **_not_fact(),
        },
        "lifecycle_policy": {
            "schema_version": "task_observation_request_lifecycle_policy_v1",
            "states": [
                "REQUEST_CANDIDATE",
                "REQUEST_BLOCKED_BY_GATE",
                "REQUEST_READY_LATER",
                "REQUEST_EXPIRED",
                "REQUEST_REPLACED_BY_NEWER_REQUEST",
                "REQUEST_CANCELLED_BY_TASK_CHANGE",
                "REQUEST_ROUTED_TO_LONG_TERM_CANDIDATE",
            ],
            "request_not_executed_in_this_phase": True,
            "expired_request_cannot_drive_action": True,
            "expired_request_can_feed_information_lifecycle_candidate": True,
            "duplicate_request_should_be_coalesced": True,
            "request_count_must_be_bounded_later": True,
            **_not_fact(),
        },
        "separation_matrix": {
            "schema_version": "task_observation_safety_task_request_separation_matrix_v1",
            "rows": separation_rows,
            "safety_priority_above_task": True,
            **_not_fact(),
        },
        "trace": {
            "schema_version": "task_observation_request_contract_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "task_observation_request_contract_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "observation_request_contract_defined": True,
            "observation_request_candidate_count": len(all_candidates),
            "baseline_request_candidate_count": baseline_count,
            "task_driven_request_candidate_count": task_driven_count,
            "request_allowed_now_count": 0,
            "recommended_next_phase": RECOMMENDED_NEXT,
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "task_observation_request_boundary_report_v1",
            "contract_only": True,
            "camera_invoked": False,
            "ocr_invoked": False,
            "detector_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "map_api_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "navigation_action_triggered": False,
            "task_state_committed_now": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "task_observation_request_metrics_candidate_report_v1",
            "observation_request_candidate_count": len(all_candidates),
            "baseline_request_candidate_count": baseline_count,
            "task_driven_request_candidate_count": task_driven_count,
            "target_module_count": len(TARGET_ROUTES),
            "request_type_count": len(REQUEST_TYPES),
            "request_allowed_now_count": 0,
            "runtime_action_committed_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "task_observation_request_benchmark_link_report_v1",
            "benchmark_available": False,
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "task_observation_request_system_health_report_v1",
            "system_health_governance_available": roots["system_health"].is_dir(),
            "health_runtime_checked": False,
            "recovery_action_committed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "task_observation_request_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "contract_only": True,
            "camera_invoked": False,
            "ocr_invoked": False,
            "detector_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "map_api_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "navigation_action_triggered": False,
            "task_state_committed_now": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "task_observation_request_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["simulation"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "task_observation_request_non_claims_report_v1",
            "claims": [
                "observation_request_contract_not_runtime",
                "observation_request_not_camera_call",
                "ocr_request_not_ocr_invoke",
                "baseline_defined_not_safety_runtime_complete",
                "task_driven_defined_not_navigation_complete",
                "vision_ocr_handoff_not_ingest_complete",
                "request_allowed_later_not_allowed_now",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "task_observation_request_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "task_observation_request_audit_report_v1",
            "task_observation_request_contract_v1_executed": True,
            "contract_only": True,
            "observation_request_contract_defined": True,
            "observation_request_schema_defined": True,
            "baseline_safety_request_policy_defined": True,
            "task_driven_request_policy_defined": True,
            "target_module_routing_policy_defined": True,
            "request_gate_policy_defined": True,
            "priority_timing_policy_defined": True,
            "vision_ocr_ingest_handoff_defined": True,
            "future_runtime_dryrun_entrypoint_defined": True,
            "camera_invoked": False,
            "ocr_invoked": False,
            "detector_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "map_api_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "navigation_action_triggered": False,
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
