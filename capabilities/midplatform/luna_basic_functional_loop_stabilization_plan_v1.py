# -*- coding: utf-8 -*-
"""Luna Basic Functional Loop Stabilization Plan v1 — planning only; no runtime.

Phase-Luna-Basic-Functional-Loop-Stabilization-Plan-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Luna-Basic-Functional-Loop-Stabilization-Plan-v1-001"
FINAL_DECISION = "BASIC_FUNCTIONAL_LOOP_STABILIZATION_PLAN_READY"
RECOMMENDED_NEXT = "Voice-Dialogue-Task-Control-Contract-v1"

FOLLOWUPS = [
    "Voice-Dialogue-Task-Control-Contract-v1",
    "MidPlatform-Task-State-Runtime-DryRun-v1",
    "Vision-OCR-Evidence-Ingest-Integration-Check-v1",
    "Voice-Guidance-Runtime-GuardedTrial-v1",
    "Basic-Navigation-Guidance-Loop-DryRun-v1",
    "Dialogue-Driven-Task-Clarification-Runtime-v1",
    "Vision-Frame-Segmentation-Governance-v1",
    "Object-Tracking-Governance-v1",
    "Navigation-Map-Context-Contract-v1",
]

CAPABILITY_STATUS: List[Tuple[str, str, bool, bool, bool, Optional[str], str]] = [
    ("Vision Capture Governance", "closed_for_governance", False, False, True, None, "stabilization_verify"),
    ("Vision Capture Runtime DryRun", "dryrun_ready", False, False, True, None, "integration_check"),
    ("OCR Activation Governance", "closed_for_governance", False, False, True, None, "policy_review"),
    ("OCR Mainline Governance Closure", "closed_for_governance", False, False, False, "ocr_governance_closed", "maintain_closure"),
    ("StaticReading Gate", "frozen", False, False, True, "no_captured_frame", "guarded_trial_later"),
    ("User Guidance Runtime", "dryrun_ready", False, False, True, None, "task_chain_integration"),
    ("Voice Guidance Runtime", "dryrun_ready", False, False, True, None, "speech_gate_integration"),
    ("VOP Adapter for Guidance", "dryrun_ready", False, False, True, None, "guarded_trial_later"),
    ("Hardware Adapter Stub", "frozen", False, False, True, "hardware_chain_frozen", "guarded_trial_precheck"),
    ("Memory Handoff DryRun", "dryrun_ready", False, False, True, "memory_runtime_not_allowed", "runtime_later"),
    ("WorldModel Lookup Framework", "framework_ready", False, False, True, "worldmodel_runtime_unavailable", "dryrun_later"),
    ("System Health Governance", "dryrun_ready", False, False, True, None, "module_health_link"),
    ("Simulation Lab", "dryrun_ready", False, False, True, None, "profile_replay"),
]

LOOP_STEPS: List[Tuple[str, str, str, str, str, List[str], List[str], bool, bool]] = [
    ("1", "User Voice / Task Input", "Voice Input / Dialogue", "user_intent_candidate", "task_context_candidate", ["parse_intent"], ["write_fact"], False, True),
    ("2", "MidPlatform Task Context", "MidPlatform / Task Manager", "task_context_candidate", "task_state_update_candidate", ["bind_task"], ["bypass_midplatform"], False, True),
    ("3", "Vision Observation / OCR Candidate", "Vision / OCR", "vision_observation_candidate", "ocr_evidence_candidate", ["emit_candidate"], ["default_ocr", "write_fact"], False, True),
    ("4", "Evidence Intake / Governance", "MidPlatform", "evidence_candidate", "governed_evidence_candidate", ["gate_evidence"], ["direct_fact_write"], False, True),
    ("5", "Task State Update Candidate", "Task Manager", "governed_evidence_candidate", "task_state_candidate", ["update_state_candidate"], ["write_fact"], False, True),
    ("6", "Guidance Decision Candidate", "MidPlatform / Navigation Guidance", "task_state_candidate", "guidance_candidate", ["rank_guidance"], ["direct_tts"], False, True),
    ("7", "Speech Gate / VOP Candidate", "Voice Output / VOP", "guidance_candidate", "speech_request_candidate", ["admit_candidate"], ["bypass_speech_gate"], False, True),
    ("8", "User Guidance / Basic Navigation Prompt", "Navigation Guidance", "speech_request_candidate", "navigation_prompt_candidate", ["emit_prompt_candidate"], ["map_api_invoke"], False, True),
]

MODULES: List[Tuple[str, List[str], List[str], List[str], List[str]]] = [
    ("Vision", ["vision_observation_candidate"], ["task_context", "capture_governance"], ["region_candidate"], ["write_fact", "trigger_ocr_default"]),
    ("OCR", ["ocr_evidence_candidate"], ["vision_observation", "ocr_activation_policy"], ["text_evidence_candidate"], ["worldmodel_write", "default_scan"]),
    ("Voice Input", ["user_intent_candidate"], ["dialogue_state"], ["task_request_candidate"], ["write_fact"]),
    ("Voice Output", ["speech_request_candidate"], ["guidance_candidate", "speech_gate"], ["vop_payload_candidate"], ["direct_tts", "bypass_speech_gate"]),
    ("MidPlatform", ["governance_decisions", "task_context_binding"], ["all_candidates"], ["task_state_update_candidate"], ["write_fact", "bypass_gates"]),
    ("Task Manager", ["task_lifecycle"], ["task_context", "evidence_candidates"], ["task_state_candidate"], ["write_fact"]),
    ("Dialogue Manager", ["clarification_flow"], ["voice_input", "task_state"], ["dialogue_turn_candidate"], ["write_profile_fact"]),
    ("Navigation Guidance", ["navigation_prompt_candidate"], ["task_state", "vision_ocr_hints"], ["guidance_rank_candidate"], ["write_fact", "map_api_direct"]),
    ("System Health", ["health_signal_candidate"], ["module_status"], ["recovery_hint_candidate"], ["auto_recovery_commit"]),
    ("Hardware Adapter", ["capture_stub_response"], ["hardware_contract"], ["capture_status_candidate"], ["real_camera_default"]),
    ("Future Segmentation", ["segmentation_region_candidate"], ["frame_input"], ["region_candidate"], ["write_fact", "direct_ocr"]),
    ("Future Tracking", ["tracklet_candidate"], ["vision_observation"], ["tracking_hint_candidate"], ["identity_fact", "direct_nav_action"]),
    ("Future Map", ["map_context_candidate"], ["route_reference"], ["route_hint_candidate"], ["override_live_observation", "fact_write"]),
]

TASK_STATES: List[Tuple[str, str, List[str], List[str], bool, bool, str]] = [
    ("NO_ACTIVE_TASK", "no active task", ["voice_input"], ["task_context_candidate"], True, False, "TASK_CONTEXT_READY"),
    ("TASK_CLARIFICATION_NEEDED", "missing task/scene", ["voice_input"], ["clarification_prompt_candidate"], True, False, "TASK_CONTEXT_READY"),
    ("TASK_CONTEXT_READY", "task+scene ready", ["vision", "voice"], ["observation_candidate"], False, True, "OBSERVING_FOR_TASK"),
    ("OBSERVING_FOR_TASK", "collecting evidence", ["vision", "ocr_gated"], ["evidence_candidate"], False, True, "GUIDANCE_CANDIDATE_READY"),
    ("GUIDANCE_CANDIDATE_READY", "guidance ranked", ["midplatform"], ["speech_request_candidate"], True, False, "USER_GUIDANCE_WAITING"),
    ("USER_GUIDANCE_WAITING", "awaiting user", ["voice_input"], ["task_state_update"], True, False, "OBSERVING_FOR_TASK"),
    ("TASK_BLOCKED_BY_INPUT_QUALITY", "low quality capture", ["user_guidance"], ["ocr_submit"], True, False, "OBSERVING_FOR_TASK"),
    ("TASK_BLOCKED_BY_HARDWARE", "hardware frozen", ["voice_input"], ["camera_capture"], True, False, "NO_ACTIVE_TASK"),
    ("TASK_COMPLETED_CANDIDATE", "task done candidate", ["voice_input"], ["completion_ack_candidate"], True, False, "NO_ACTIVE_TASK"),
    ("TASK_ABORTED_CANDIDATE", "user aborted", ["voice_input"], ["abort_ack_candidate"], True, False, "NO_ACTIVE_TASK"),
]

VOICE_CAPABILITIES = [
    "user_initiates_task",
    "user_clarifies_task",
    "user_asks_current_status",
    "user_requests_repeat_prompt",
    "user_cancels_task",
    "user_pauses_task",
    "user_resumes_task",
    "system_requests_view_adjustment",
    "system_requests_scene_goal_confirmation",
    "system_gives_basic_navigation_prompt",
]

CLASSIFICATIONS: List[Tuple[str, str, List[str], List[str], bool, bool]] = [
    ("HIGH_VALUE_LOOKUP_CANDIDATE", "Strong hint for ISRC", ["feed_isrc"], ["submit_ocrrequest"], True, False),
    ("NEEDS_LIVE_VERIFICATION", "Requires capture/OCR gate later", ["prepare_static_capture"], ["write_worldmodel"], True, False),
    ("STALE_BUT_USEFUL", "May feed long-term candidate only", ["feed_long_term_candidate"], ["direct_action"], False, True),
    ("CONFLICTING_HINT", "Hold; user clarification", ["user_clarification"], ["auto_merge"], False, False),
    ("PRIVACY_SENSITIVE_REQUIRES_CONFIRMATION", "Privacy gate before use", ["privacy_confirm"], ["auto_use"], False, False),
    ("HUMAN_ASSISTANCE_RECOMMENDED", "Staff assistance path", ["human_assistance"], ["auto_ocr"], False, False),
    ("NOT_ENOUGH_CONTEXT", "Wait for task/scene", ["wait_task_scene"], ["feed_rrd"], False, False),
    ("DO_NOT_USE_FOR_ACTION", "Do not drive action", [], ["feed_isrc", "submit_ocrrequest", "write_fact"], False, False),
]

EVIDENCE_INGEST: List[Tuple[str, str, str, bool, List[str], List[str], bool]] = [
    ("vision_observation", "governance_defined", "vision_evidence_v1", True, ["midplatform_ingest", "task_relevance_gate"], ["worldmodel_write"], True),
    ("ocr_candidate", "closed_for_governance", "ocr_evidence_readonly", True, ["task_triggered_ocr_only", "evidence_pack_candidate"], ["default_ocr", "fact_from_empty"], True),
    ("segmentation_candidate", "future_entry", "region_candidate_v1", True, ["readable_region_ref"], ["direct_ocr", "fact_write"], False),
    ("tracking_candidate", "future_entry", "tracklet_candidate_v1", True, ["navigation_hint_ref"], ["identity_fact", "direct_action"], False),
]

NAV_GUIDANCE = [
    ("obstacle_ahead", "前方障碍提醒", True),
    ("stabilize_prompt", "停稳提示", True),
    ("centering_prompt", "靠近/居中/调整角度", True),
    ("direction_confirm", "方向确认", True),
    ("sign_seek", "门牌/出口/标识寻找", True),
    ("context_clarify", "上下文不足澄清", True),
    ("task_degrade", "任务阻断降级", True),
    ("safety_priority", "安全优先播报", True),
]

DEFERRED: List[Tuple[str, str, str, str]] = [
    ("WorldModel runtime", "worldmodel_not_built", "WorldModel-Core-Schema-Contract-v1", "no_wm_runtime_bypass"),
    ("Fragment Evidence Weaving runtime", "fragment_runtime_deferred", "Fragment-Evidence-Weaving-Governance-v1", "no_scenedelta_write"),
    ("Emotional Context runtime", "emotion_runtime_deferred", "Emotional-Context-Background-Candidate-DryRun-v1", "no_emotional_fact"),
    ("EP v5 StaticReading execution", "ep_v5_blocked", "Evidence-Pack-Adapter-v5-StaticReading", "no_ep_without_ocr"),
    ("Semantic v5 execution", "semantic_v5_blocked", "Semantic-Candidate-v5-StaticReading", "no_semantic_without_ep"),
    ("Source Validation v3 execution", "sv_v3_blocked", "Source-Validation-v3-StaticReading", "no_sv_without_ep"),
    ("Hardware GuardedTrial", "hardware_frozen", "Hardware-Camera-Control-GuardedTrial-Precheck-v1", "no_camera_default"),
    ("Real camera capture", "stub_only", "OCRRequest-Gated-Submission-GuardedTrial", "no_capture_bypass"),
    ("Real map API", "map_deferred", "Navigation-Map-Context-Contract-v1", "no_map_fact"),
    ("Real tracking runtime", "tracking_deferred", "Object-Tracking-Governance-v1", "no_tracker_identity_fact"),
    ("Real segmentation runtime", "segmentation_deferred", "Vision-Frame-Segmentation-Governance-v1", "no_seg_direct_ocr"),
]

STABILIZATION_TESTS = [
    ("vision_ocr_ingest_check", "Vision-OCR Evidence Ingest Integration Check", "evidence path stable", ["vision_smoke", "ocr_closure"], ["ingest_candidate_only"], True),
    ("voice_dialogue_dryrun", "Voice Dialogue Task Control DryRun", "dialogue+task binding", ["voice_runtime", "task_contract"], ["speech_request_candidate"], True),
    ("task_state_dryrun", "MidPlatform Task State Runtime DryRun", "FSM stable", ["task_state_policy"], ["state_candidate_only"], True),
    ("voice_guarded_trial", "Voice Output Guarded Trial DryRun", "Speech Gate+VOP", ["vop_adapter"], ["no_direct_tts"], True),
    ("nav_guidance_dryrun", "Basic Navigation Guidance Loop DryRun", "nav prompts", ["navigation_plan"], ["prompt_candidate_only"], True),
    ("seg_readiness", "Segmentation Governance Readiness Check", "future seg", ["frame_governance"], ["no_seg_runtime"], True),
    ("tracking_readiness", "Tracking Governance Readiness Check", "future tracking", ["tracklet_schema"], ["no_tracking_runtime"], True),
    ("map_readiness", "Map Context Contract Readiness Check", "future map", ["route_contract"], ["no_map_api"], True),
]

ROADMAP: List[Tuple[str, str, str, List[str], List[str], str, str]] = [
    ("Voice-Dialogue-Task-Control-Contract-v1", "P0", "dialogue+task contract", ["voice_guidance_chain", "ocr_closure"], [], "stable task control", "low"),
    ("MidPlatform-Task-State-Runtime-DryRun-v1", "P0", "task FSM dry-run", ["task_state_policy"], [], "state machine stable", "low"),
    ("Vision-OCR-Evidence-Ingest-Integration-Check-v1", "P0", "evidence ingest", ["vision_governance", "ocr_closure"], [], "ingest path clear", "medium"),
    ("Voice-Guidance-Runtime-GuardedTrial-v1", "P1", "guarded voice output", ["speech_gate", "vop_adapter"], ["hardware_frozen"], "voice loop trial", "medium"),
    ("Basic-Navigation-Guidance-Loop-DryRun-v1", "P1", "nav prompt loop", ["task_state", "voice_chain"], ["map_api"], "basic nav prompts", "medium"),
    ("Dialogue-Driven-Task-Clarification-Runtime-v1", "P1", "clarification runtime", ["dialogue_contract"], [], "clarify flow", "low"),
    ("Vision-Frame-Segmentation-Governance-v1", "P2", "seg governance", ["vision_input_governance"], ["seg_runtime"], "region candidates", "medium"),
    ("Object-Tracking-Governance-v1", "P2", "tracking governance", ["vision_evidence"], ["tracking_runtime"], "tracklet candidates", "medium"),
    ("Navigation-Map-Context-Contract-v1", "P2", "map context contract", ["route_governance"], ["map_api"], "map reference only", "high"),
    ("WorldModel runtime", "P3", "WM runtime deferred", ["wm_framework", "wm_core"], ["wm_not_built"], "lookup runtime", "high"),
    ("Fragment Evidence Weaving runtime", "P3", "fragment deferred", ["evidence_weaving_gov"], [], "weaving runtime", "high"),
    ("Emotional Context runtime", "P3", "emotion deferred", ["privacy_governance"], [], "emotion candidates", "medium"),
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_ocr_closure", "ocr_closure_loaded", [], [], ["enable_runtime_ocr"]),
    ("load_worldmodel_framework", "wm_framework_loaded", [], [], ["wm_runtime"]),
    ("load_voice_guidance_chain", "voice_chain_loaded", [], [], ["direct_tts"]),
    ("load_vision_ocr_chain", "vision_ocr_loaded", [], [], []),
    ("load_hardware_stub", "hw_loaded", [], [], ["camera"]),
    ("evaluate_current_capabilities", "capabilities_evaluated", [], [], []),
    ("define_basic_functional_loop", "loop_defined", [], [], []),
    ("define_module_boundaries", "boundaries_defined", [], [], ["bypass_midplatform"]),
    ("define_information_source_standard", "source_standard_ok", [], [], []),
    ("define_task_state_policy", "task_state_ok", [], [], []),
    ("define_voice_dialogue_minimal_plan", "voice_plan_ok", [], [], ["tts_bypass"]),
    ("define_vision_ocr_ingest_plan", "ingest_plan_ok", [], [], []),
    ("define_navigation_guidance_plan", "nav_plan_ok", [], [], ["map_api"]),
    ("define_future_segmentation_entry", "seg_entry_ok", [], [], ["seg_runtime"]),
    ("define_future_tracking_entry", "track_entry_ok", [], [], ["tracking_runtime"]),
    ("define_future_map_entry", "map_entry_ok", [], [], ["map_api"]),
    ("define_deferred_capabilities", "deferred_ok", [], [], []),
    ("generate_recommended_phase_roadmap", "roadmap_ok", [], [], []),
    ("generate_final_stabilization_decision", "plan_ready", [], [], ["production_ready"]),
]

OPTIONAL_DOC_GLOBS = {
    "vision_provider_input_governance": "**/*VISION*PROVIDER*INPUT*GOVERNANCE*.md",
    "roi_segmentation_stub": "**/*ROI*PROPOSAL*.md",
    "yolo_evaluation": "**/*YOLO*EVALUATION*.md",
    "tracking_bytetrack": "**/*BYTE*TRACK*.md",
    "navigation_map_governance": "**/*NAVIGATION*MAP*.md",
    "voice_mainline": "**/*VOICE*MAINLINE*.md",
    "taskchain_runtime": "**/*TASK*CHAIN*.md",
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
                "capability_area": "midplatform",
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


def run_luna_basic_functional_loop_stabilization_plan_v1(
    *,
    ocr_mainline_closure_root: str,
    worldmodel_framework_root: str,
    software_closure_root: str,
    ocr_activation_root: str,
    stc_root: str,
    vision_capture_governance_root: str,
    vision_capture_runtime_root: str,
    user_guidance_runtime_root: str,
    voice_guidance_runtime_root: str,
    vop_adapter_root: str,
    hardware_adapter_stub_root: str,
    realvideo_frame_sample_root: str,
    regression_route_root: str,
    system_health_root: str,
    simulation_root: str,
    benchmark_smoke_root: Optional[str] = None,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "ocr_closure": Path(ocr_mainline_closure_root).resolve(),
        "wm_fw": Path(worldmodel_framework_root).resolve(),
        "sw_closure": Path(software_closure_root).resolve(),
        "ocr_act": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_root).resolve(),
        "vision_gov": Path(vision_capture_governance_root).resolve(),
        "vision_rt": Path(vision_capture_runtime_root).resolve(),
        "user_guidance": Path(user_guidance_runtime_root).resolve(),
        "voice_guidance": Path(voice_guidance_runtime_root).resolve(),
        "vop": Path(vop_adapter_root).resolve(),
        "hw_stub": Path(hardware_adapter_stub_root).resolve(),
        "rv_frame": Path(realvideo_frame_sample_root).resolve(),
        "regression": Path(regression_route_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve() if benchmark_smoke_root else None,
    }

    ocr_cl = _read_json(roots["ocr_closure"] / "ocr_mainline_governance_closure_v1_summary.json") or {}
    wm_fw = _read_json(roots["wm_fw"] / "worldmodel_lookup_for_reading_framework_v1_summary.json") or {}

    intake_specs = [
        ("ocr_mainline_closure", "ocr", roots["ocr_closure"], "ocr_mainline_governance_closure_v1_summary.json", False),
        ("worldmodel_lookup_framework", "worldmodel_framework", roots["wm_fw"], "worldmodel_lookup_for_reading_framework_v1_summary.json", False),
        ("software_closure", "midplatform", roots["sw_closure"], "return_to_software_mainline_closure_v1_summary.json", False),
        ("ocr_activation", "ocr", roots["ocr_act"], "ocr_activation_governance_policy_v1_summary.json", False),
        ("stc_sampling", "midplatform", roots["stc"], "stc_sampling_guidance_policy_v1_summary.json", False),
        ("vision_capture_governance", "vision", roots["vision_gov"], "vision_capture_governance_v1_summary.json", False),
        ("vision_capture_runtime", "vision", roots["vision_rt"], "vision_capture_runtime_dryrun_v1_summary.json", False),
        ("user_guidance_runtime", "voice", roots["user_guidance"], "user_guidance_recovery_runtime_dryrun_v1_summary.json", False),
        ("voice_guidance_runtime", "voice", roots["voice_guidance"], "voice_guidance_prompt_runtime_dryrun_v1_summary.json", False),
        ("vop_adapter", "voice", roots["vop"], "voice_output_plane_adapter_for_guidance_v1_summary.json", False),
        ("hardware_stub", "hardware", roots["hw_stub"], "hardware_camera_runtime_adapter_implementation_stub_v1_summary.json", False),
        ("realvideo_frame_sample", "vision", roots["rv_frame"], "cross_modal_vision_ocr_realvideo_frame_sample_summary.json", False),
        ("regression_route_compliance", "ocr", roots["regression"], "ocr_staticreading_poster_realvideo_regression_route_compliance_v1_summary.json", False),
        ("system_health", "system_health", roots["health"], None, True),
        ("simulation", "simulation", roots["sim"], None, True),
    ]
    intake_rows = []
    for iid, area, root, art, optional in intake_specs:
        loaded = root.is_dir()
        if art:
            loaded = loaded and (root / art).is_file()
        intake_rows.append(
            {
                "intake_id": iid,
                "capability_area": area,
                "input_source": iid,
                "source_root_or_path": str(root),
                "artifact": art or "(directory)",
                "loaded": loaded,
                "optional": optional,
                "key_fields_observed": ["summary"] if loaded else [],
                "intake_status": "loaded" if loaded else ("optional_missing" if optional else "missing"),
                "missing_impact": "none" if loaded else ("optional_reference_only" if optional else "plan_partial"),
                **_not_fact(),
            }
        )
    intake_rows.extend(_find_optional_docs(ws))

    cap_rows = [
        {
            "capability_name": name,
            "current_status": status,
            "runtime_enabled_now": rt,
            "extension_allowed_now": ext_now,
            "extension_allowed_later": ext_later,
            "blocker_if_any": blocker,
            "next_required_step": step,
            **_not_fact(),
        }
        for name, status, rt, ext_now, ext_later, blocker, step in CAPABILITY_STATUS
    ]

    loop_rows = [
        {
            "loop_step_id": sid,
            "loop_step_name": sname,
            "owner_module": owner,
            "input_contract": inp,
            "output_contract": out,
            "allowed_actions": allowed,
            "forbidden_actions": forbidden,
            "runtime_enabled_now": rt,
            "stabilization_required": stab,
            **_not_fact(),
        }
        for sid, sname, owner, inp, out, allowed, forbidden, rt, stab in LOOP_STEPS
    ]

    module_rows = [
        {
            "module": mod,
            "owns": owns,
            "may_read": may_read,
            "may_emit_candidate": may_emit,
            "may_not_do": may_not,
            "write_fact_allowed_now": False,
            "bypass_forbidden": True,
            **_not_fact(),
        }
        for mod, owns, may_read, may_emit, may_not in MODULES
    ]

    source_types = [
        "vision_observation", "ocr_candidate", "voice_input", "task_context", "route_context",
        "user_guidance_state", "system_health_signal", "segmentation_candidate",
        "tracking_candidate", "map_context_candidate",
    ]

    task_rows = [
        {
            "state": state,
            "entry_condition": cond,
            "allowed_inputs": ain,
            "allowed_outputs": aout,
            "voice_prompt_allowed": vp,
            "observation_required": obs,
            "transition_guard": trans,
            "fact_write_allowed": False,
            **_not_fact(),
        }
        for state, cond, ain, aout, vp, obs, trans in TASK_STATES
    ]

    evidence_rows = [
        {
            "evidence_type": et,
            "current_status": st,
            "required_schema": schema,
            "gate_required": gate,
            "allowed_downstream": ad,
            "forbidden_downstream": fd,
            "stabilization_test_required": test,
            **_not_fact(),
        }
        for et, st, schema, gate, ad, fd, test in EVIDENCE_INGEST
    ]

    classification_rows = [
        {
            "classification": cls,
            "meaning": meaning,
            "allowed_next_action": allowed,
            "blocked_next_action": blocked,
            "can_feed_isrc": can_isrc,
            "can_feed_long_term_candidate": can_lt,
            **_not_fact(),
        }
        for cls, meaning, allowed, blocked, can_isrc, can_lt in CLASSIFICATIONS
    ]

    nav_rows = [
        {"guidance_id": gid, "description": desc, "safety_priority": sp, **_not_fact()}
        for gid, desc, sp in NAV_GUIDANCE
    ]

    deferred_rows = [
        {
            "capability": cap,
            "deferred_now": True,
            "reason": reason,
            "allowed_later_condition": later,
            "forbidden_bypass": bypass,
            **_not_fact(),
        }
        for cap, reason, later, bypass in DEFERRED
    ]

    test_rows = [
        {
            "test_id": tid,
            "test_name": tname,
            "purpose": purpose,
            "required_inputs": rin,
            "expected_outputs": rout,
            "no_write_boundary_required": nw,
            **_not_fact(),
        }
        for tid, tname, purpose, rin, rout, nw in STABILIZATION_TESTS
    ]

    roadmap_rows = [
        {
            "phase_name": pname,
            "priority": pri,
            "objective": obj,
            "prerequisites": pre,
            "blocked_by": blk,
            "expected_value": val,
            "risk": risk,
            **_not_fact(),
        }
        for pname, pri, obj, pre, blk, val, risk in ROADMAP
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
            "schema_version": "luna_basic_functional_loop_stabilization_plan_v1_summary_v0",
            "phase": PHASE_ID,
            "plan_scope": "basic_functional_loop_stabilization_plan_only",
            "based_on_ocr_mainline_closure": roots["ocr_closure"].is_dir(),
            "based_on_worldmodel_lookup_framework": roots["wm_fw"].is_dir(),
            "worldmodel_runtime_deferred": True,
            "fragment_weaving_deferred": True,
            "emotional_context_deferred": True,
            "ocr_mainline_closed_for_governance": ocr_cl.get("closed_for_governance", True),
            "hardware_chain_frozen": ocr_cl.get("hardware_chain_frozen", True),
            "basic_functional_loop_defined": True,
            "vision_input_stabilization_required": True,
            "ocr_as_task_capability_confirmed": True,
            "voice_dialogue_stabilization_required": True,
            "midplatform_task_chain_stabilization_required": True,
            "basic_navigation_guidance_loop_required": True,
            "segmentation_future_entry_defined": True,
            "object_tracking_future_entry_defined": True,
            "navigation_map_future_entry_defined": True,
            "runtime_action_committed": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "memory_system_invoked": False,
            "runtime_routing_changed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
            "recommended_next_phase": RECOMMENDED_NEXT,
        },
        "intake": {
            "schema_version": "luna_basic_loop_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "capability_matrix": {
            "schema_version": "luna_basic_loop_current_capability_status_matrix_v1",
            "capabilities": cap_rows,
            "capability_count": len(cap_rows),
            **_not_fact(),
        },
        "loop_definition": {
            "schema_version": "luna_basic_functional_loop_definition_v1",
            "loop_name": "Luna Basic Functional Loop v1",
            "steps": loop_rows,
            "step_count": len(loop_rows),
            **_not_fact(),
        },
        "module_boundary": {
            "schema_version": "luna_basic_loop_module_responsibility_boundary_v1",
            "modules": module_rows,
            "module_count": len(module_rows),
            **_not_fact(),
        },
        "info_source_standard": {
            "schema_version": "luna_basic_loop_information_source_standard_v1",
            "field_definitions": {
                "source_id": "string",
                "source_type": source_types,
                "source_chain": "list",
                "time_anchor": "timestamp_ref",
                "spatial_anchor": "anchor",
                "confidence": "number_or_null",
                "freshness": "enum",
                "privacy_sensitivity": "enum",
                "task_relevance": "enum",
            },
            "source_types": source_types,
            **_not_fact(),
        },
        "task_state_policy": {
            "schema_version": "luna_basic_loop_task_state_stabilization_policy_v1",
            "states": task_rows,
            "state_count": len(task_rows),
            **_not_fact(),
        },
        "voice_plan": {
            "schema_version": "luna_basic_loop_voice_dialogue_minimal_capability_plan_v1",
            "minimal_capabilities": VOICE_CAPABILITIES,
            "all_voice_output_requires_speech_gate": True,
            "direct_tts_bypass_forbidden": True,
            "vop_required": True,
            "short_term_memory_required_for_repeat": True,
            "runtime_tts_invoked_now": False,
            **_not_fact(),
        },
        "vision_ocr_ingest": {
            "schema_version": "luna_basic_loop_vision_ocr_evidence_ingest_plan_v1",
            "evidence_plans": evidence_rows,
            "ocr_not_default_world_modeling": True,
            "empty_ocr_not_no_text_fact": True,
            "low_quality_triggers_user_guidance": True,
            **_not_fact(),
        },
        "isrc_handoff": {
            "schema_version": "luna_basic_loop_isrc_handoff_policy_v1",
            "isrc_handoff_policy_defined": True,
            "worldmodel_lookup_candidate_can_feed_isrc": True,
            "isrc_runtime_invoked_now": False,
            "ranked_information_source_area_generated_now": False,
            "required_payload": [
                "task_context",
                "scene_context",
                "lookup_response_candidate",
                "source_chain",
                "freshness_status",
                "spatial_anchor",
                "privacy_sensitivity",
            ],
            "handoff_allowed_later": True,
            **_not_fact(),
        },
        "rrd_handoff": {
            "schema_version": "luna_basic_loop_rrd_handoff_policy_v1",
            "rrd_handoff_policy_defined": True,
            "isrc_ranked_source_required_before_rrd": True,
            "readable_region_discovery_invoked_now": False,
            "readable_region_candidate_generated_now": False,
            "ocrrequest_eligible_now": False,
            "required_before_rrd": [
                "information_source_candidate",
                "task_scene_context",
                "source_area_candidate",
                "safety_check",
                "stc_freshness",
            ],
            **_not_fact(),
        },
        "classification": {
            "schema_version": "luna_basic_loop_candidate_classification_policy_v1",
            "classifications": classification_rows,
            "classification_count": len(classification_rows),
            **_not_fact(),
        },
        "no_write_policy": {
            "schema_version": "luna_basic_loop_no_write_boundary_policy_v1",
            "worldmodel_lookup_framework_only": True,
            "worldmodel_lookup_invoked": False,
            "world_model_written": False,
            "worldmodel_fact_generated": False,
            "scene_delta_candidate_generated": False,
            "unresolved_slot_written_now": False,
            "world_change_hint_written_now": False,
            "midplatform_fact_written": False,
            "ocr_invoked": False,
            "ocrrequest_submitted": False,
            **_not_fact(),
        },
        "nav_plan": {
            "schema_version": "luna_basic_loop_navigation_guidance_plan_v1",
            "guidance_capabilities": nav_rows,
            "navigation_guidance_is_candidate": True,
            "safety_priority_above_guidance": True,
            "speech_gate_required": True,
            "map_dependency_required_now": False,
            "worldmodel_dependency_required_now": False,
            "fact_write_allowed": False,
            **_not_fact(),
        },
        "seg_policy": {
            "schema_version": "luna_basic_loop_future_segmentation_entry_policy_v1",
            "segmentation_allowed_now": False,
            "segmentation_allowed_later": True,
            "segmentation_must_pass_frame_input_governance": True,
            "segmentation_must_emit_region_candidate": True,
            "segmentation_cannot_write_fact": True,
            "segmentation_cannot_trigger_ocr_directly": True,
            "segmentation_cannot_bypass_midplatform": True,
            "future_phases": [
                "Vision-Frame-Segmentation-Governance-v1",
                "Vision-Region-Candidate-Adapter-v1",
                "Segmentation-to-ReadableRegion-Reference-DryRun-v1",
            ],
            **_not_fact(),
        },
        "tracking_policy": {
            "schema_version": "luna_basic_loop_future_object_tracking_entry_policy_v1",
            "tracking_allowed_now": False,
            "tracking_allowed_later": True,
            "tracker_id_is_not_identity_fact": True,
            "tracking_must_emit_tracklet_candidate": True,
            "tracking_cannot_write_worldmodel": True,
            "tracking_cannot_trigger_navigation_action_directly": True,
            "tracking_must_pass_task_relevance_gate": True,
            "future_phases": [
                "Object-Tracking-Governance-v1",
                "Tracklet-Evidence-Candidate-Schema-v1",
                "Tracking-to-Navigation-Guidance-DryRun-v1",
            ],
            **_not_fact(),
        },
        "map_policy": {
            "schema_version": "luna_basic_loop_future_navigation_map_entry_policy_v1",
            "map_integration_allowed_now": False,
            "map_integration_allowed_later": True,
            "map_context_is_reference_not_fact": True,
            "map_cannot_override_live_observation": True,
            "route_context_requires_freshness": True,
            "map_data_requires_source_chain": True,
            "map_must_pass_midplatform_task_gate": True,
            "future_phases": [
                "Navigation-Map-Context-Contract-v1",
                "Route-Context-Reference-DryRun-v1",
                "Map-Vision-Alignment-Governance-v1",
            ],
            **_not_fact(),
        },
        "deferred": {
            "schema_version": "luna_basic_loop_deferred_capability_matrix_v1",
            "deferred_capabilities": deferred_rows,
            "deferred_count": len(deferred_rows),
            **_not_fact(),
        },
        "test_plan": {
            "schema_version": "luna_basic_loop_stabilization_test_plan_v1",
            "tests": test_rows,
            "test_count": len(test_rows),
            **_not_fact(),
        },
        "roadmap": {
            "schema_version": "luna_basic_loop_recommended_phase_roadmap_v1",
            "phases": roadmap_rows,
            "p0_phases": [p["phase_name"] for p in roadmap_rows if p["priority"] == "P0"],
            **_not_fact(),
        },
        "trace": {
            "schema_version": "luna_basic_loop_stabilization_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "luna_basic_loop_stabilization_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "worldmodel_runtime_deferred": True,
            "ocr_mainline_closed_for_governance": True,
            "basic_loop_defined": True,
            "next_recommended_phase": RECOMMENDED_NEXT,
            "alternative_next_phases": [
                "MidPlatform-Task-State-Runtime-DryRun-v1",
                "Vision-OCR-Evidence-Ingest-Integration-Check-v1",
            ],
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "luna_basic_loop_stabilization_boundary_report_v1",
            "plan_only": True,
            "runtime_action_committed": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "map_api_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "luna_basic_loop_stabilization_metrics_candidate_report_v1",
            "capability_status_count": len(cap_rows),
            "loop_step_count": len(loop_rows),
            "module_boundary_count": len(module_rows),
            "task_state_count": len(task_rows),
            "voice_minimal_capability_count": len(VOICE_CAPABILITIES),
            "deferred_capability_count": len(deferred_rows),
            "roadmap_phase_count": len(roadmap_rows),
            "runtime_action_committed_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "luna_basic_loop_stabilization_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir() if roots["bench"] else False,
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "luna_basic_loop_stabilization_system_health_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_candidate_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "luna_basic_loop_stabilization_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "plan_only": True,
            "runtime_action_committed": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "map_api_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "luna_basic_loop_stabilization_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "luna_basic_loop_stabilization_non_claims_report_v1",
            "claims": [
                "stabilization_plan_not_runtime",
                "basic_loop_not_production_ready",
                "segmentation_tracking_map_future_only",
                "worldmodel_framework_not_runtime",
                "ocr_governance_closed_not_ocr_enabled",
                "voice_dialogue_plan_not_dialogue_complete",
                "navigation_plan_not_real_navigation",
                "no_model_invocation",
                "no_fact_write",
            ],
        },
        "followups": {
            "schema_version": "luna_basic_loop_stabilization_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "luna_basic_loop_stabilization_audit_report_v1",
            "luna_basic_functional_loop_stabilization_plan_v1_executed": True,
            "plan_only": True,
            "worldmodel_runtime_deferred": True,
            "fragment_weaving_deferred": True,
            "emotional_context_deferred": True,
            "basic_functional_loop_defined": True,
            "segmentation_future_entry_defined": True,
            "object_tracking_future_entry_defined": True,
            "navigation_map_future_entry_defined": True,
            "runtime_action_committed": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "segmentation_invoked": False,
            "tracking_invoked": False,
            "map_api_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
            "final_decision_recorded": FINAL_DECISION,
        },
    }
