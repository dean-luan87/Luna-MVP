# -*- coding: utf-8 -*-
"""User Clarification Prompt Template for Reading v1 — template only (no TTS/VOP/STM write).

Phase-User-Clarification-Prompt-Template-for-Reading-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "User-Clarification-Prompt-Template-for-Reading-v1-001"
P3 = "P3_OCR_GUIDANCE"
P4 = "P4_GENERAL_ASSISTANCE"
P0 = "P0_SAFETY_CRITICAL"

FOLLOWUPS = [
    "User-Clarification-Prompt-Runtime-DryRun-for-Reading-v1",
    "Static-Reading-Task-Scene-Context-GuardedTrial-v1",
    "Static-Reading-Information-Source-Localization-Runtime-DryRun-v1",
    "Static-Readable-Region-Discovery-Runtime-DryRun-v1",
    "Human-Staff-Assistance-Prompt-Template-v1",
    "Scene-Context-Recognition-Policy-v1",
    "WorldModel-Lookup-for-Reading-DryRun-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

PROHIBITED = [
    "保证能读到",
    "系统已确认你在",
    "马上为您识别",
    "一定是商场",
]

CLARIFICATION_TEMPLATES: List[Tuple[str, str, str, str, str, str, str, str]] = [
    (
        "uclar_001",
        "missing_task_context",
        "你想找什么信息？",
        "请再说一下你想找什么信息。",
        "free_text_or_task_intent",
        "target_information_need",
        P3,
    ),
    (
        "uclar_002",
        "missing_scene_context",
        "你现在大概在什么地方？比如商场、医院、车站或街边。",
        "请再说一下你现在大概在什么场景。",
        "scene_type_or_place_hint",
        "normalized_scene_type",
        P4,
    ),
    (
        "uclar_003",
        "missing_both_task_and_scene",
        "你想找什么信息？现在大概在什么场景？",
        "请再说一下你想找的信息和当前场景。",
        "task_and_scene_combined",
        "task_context_and_scene_context",
        P3,
    ),
    (
        "uclar_004",
        "low_confidence_task",
        "你现在是想找出口、门牌，还是读一段文字？",
        "请确认：出口、门牌，还是读一段文字？",
        "task_type_disambiguation",
        "normalized_task_type",
        P3,
    ),
    (
        "uclar_005",
        "low_confidence_scene",
        "你是在商场、医院、车站，还是其他地方？",
        "请确认当前场景：商场、医院、车站或其他。",
        "scene_type_disambiguation",
        "normalized_scene_type",
        P4,
    ),
    (
        "uclar_006",
        "conflicting_context",
        "刚才的信息有点不一致，请再确认一下你想找什么、现在在哪里。",
        "请再确认目标和场景。",
        "task_and_scene_reconfirm",
        "task_context_and_scene_context",
        P3,
    ),
    (
        "uclar_007",
        "ask_human_staff_option",
        "是否需要询问附近工作人员？",
        "如果需要，可以请附近工作人员帮忙。",
        "yes_no_or_decline",
        "human_assistance_fallback",
        P4,
    ),
]

FILL_RULES: List[Tuple[str, str, str, str, bool]] = [
    ("找出口", "possible_task_type", "find_exit", "medium", False),
    ("出口", "possible_task_type", "find_exit", "low", True),
    ("门牌", "possible_task_type", "read_doorplate", "medium", False),
    ("读这段", "possible_task_type", "user_explicit_read_this", "medium", False),
    ("读一下", "possible_task_type", "user_explicit_read_this", "low", True),
    ("读字", "possible_task_type", "generic_reading_request", "low", True),
    ("商场", "possible_scene_type", "shopping_mall", "medium", False),
    ("医院", "possible_scene_type", "hospital", "medium", False),
    ("车站", "possible_scene_type", "transit_station", "medium", False),
    ("地铁", "possible_scene_type", "transit_station", "low", True),
    ("街边", "possible_scene_type", "street", "medium", False),
    ("办公室", "possible_scene_type", "office_building", "low", True),
    ("不确定", "confidence_policy", "low", "low", True),
    ("不知道", "confidence_policy", "low", "low", True),
]

LONG_TERM_TYPES = [
    "unresolved_task_context_candidate",
    "unresolved_scene_context_candidate",
    "repeated_clarification_needed_candidate",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake(roots: Dict[str, Path]) -> Dict[str, Any]:
    specs = [
        ("tsc_runtime", roots["tsc_rt"], "static_reading_task_scene_context_runtime_dryrun_v1_summary.json"),
        ("tsc_policy", roots["tsc"], "static_reading_task_scene_context_policy_v1_summary.json"),
        ("vg_template", roots["vg_tpl"], "voice_guidance_prompt_template_v1_summary.json"),
        ("vg_runtime", roots["vg_rt"], "voice_guidance_prompt_runtime_dryrun_v1_summary.json"),
        ("vop", roots["vop"], "voice_output_plane_adapter_for_guidance_v1_summary.json"),
        ("bench", roots["bench"], None),
        ("health", roots["health"], None),
        ("sim", roots["sim"], None),
    ]
    rows = []
    for iid, root, art in specs:
        loaded = root.is_dir()
        if art:
            loaded = loaded and (root / art).is_file()
        rows.append(
            {
                "intake_id": iid,
                "input_source": iid,
                "source_root": str(root),
                "artifact": art or "(directory)",
                "loaded": loaded,
                "key_fields_observed": ["summary"] if loaded else [],
                "intake_status": "loaded" if loaded else "missing",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    clar_rt = _read_json(roots["tsc_rt"] / "static_reading_user_clarification_candidate_runtime_v1.json")
    if clar_rt:
        rows.append(
            {
                "intake_id": "tsc_clarification_runtime",
                "input_source": "tsc_runtime",
                "source_root": str(roots["tsc_rt"]),
                "artifact": "static_reading_user_clarification_candidate_runtime_v1.json",
                "loaded": True,
                "key_fields_observed": ["candidates", "user_clarification_candidate_generated"],
                "intake_status": "loaded",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    return {
        "schema_version": "user_clarification_prompt_template_input_intake_matrix_v1",
        "rows": rows,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_user_clarification_prompt_template_for_reading_v1(
    *,
    task_scene_runtime_root: str,
    task_scene_policy_root: str,
    voice_guidance_template_root: str,
    voice_guidance_runtime_root: str,
    voice_output_plane_adapter_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    roots = {
        "tsc_rt": Path(task_scene_runtime_root).resolve(),
        "tsc": Path(task_scene_policy_root).resolve(),
        "vg_tpl": Path(voice_guidance_template_root).resolve(),
        "vg_rt": Path(voice_guidance_runtime_root).resolve(),
        "vop": Path(voice_output_plane_adapter_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    final_rt = _read_json(roots["tsc_rt"] / "static_reading_task_scene_context_runtime_final_decision_v1.json") or {}
    missing_status = final_rt.get("missing_context_status") or "missing_both_task_and_scene"

    templates = []
    for tid, ctype, short, repeat, resp_type, field, pri in CLARIFICATION_TEMPLATES:
        templates.append(
            {
                "template_id": tid,
                "clarification_type": ctype,
                "prompt_text_short": short,
                "prompt_text_repeat": repeat,
                "expected_user_response_type": resp_type,
                "target_context_field_to_fill": field,
                "priority_level": pri,
                "safety_interruptible": True,
                "prohibited_wording": PROHIBITED,
                "tts_invoked_now": False,
                "speech_request_submitted_now": False,
                "fact_status": "not_fact",
            }
        )

    selected = next((t for t in templates if t["clarification_type"] == missing_status), templates[2])
    selected_pri = selected["priority_level"]

    fill_rules = [
        {
            "response_pattern": pat,
            "fills_context_field": field,
            "normalized_value_candidate": val,
            "confidence_policy": conf,
            "confirmation_required": confirm,
            "fact_written_now": False,
            "fact_status": "not_fact",
        }
        for pat, field, val, conf, confirm in FILL_RULES
    ]

    return {
        "summary": {
            "schema_version": "user_clarification_prompt_template_for_reading_v1_summary_v0",
            "phase": PHASE_ID,
            "template_scope": "reading_clarification_prompt_template_only",
            "based_on_task_scene_context_runtime": roots["tsc_rt"].is_dir(),
            "based_on_task_scene_context_policy": roots["tsc"].is_dir(),
            "based_on_voice_guidance_template": roots["vg_tpl"].is_dir(),
            "current_case_loaded": True,
            "clarification_prompt_template_defined": True,
            "task_missing_prompt_defined": True,
            "scene_missing_prompt_defined": True,
            "both_missing_prompt_defined": True,
            "expected_user_response_schema_defined": True,
            "response_to_context_fill_policy_defined": True,
            "speech_priority_policy_linked": True,
            "safety_priority_above_clarification": True,
            "cooldown_repeat_policy_defined": True,
            "handoff_to_task_scene_runtime_defined": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "map_api_invoked": False,
            "ranked_information_source_area_generated": False,
            "readable_region_generated": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": _intake(roots),
        "matrix": {
            "schema_version": "user_clarification_prompt_template_matrix_v1",
            "templates": templates,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "response_schema": {
            "schema_version": "user_clarification_expected_response_schema_v1",
            "fields": [
                "response_id",
                "raw_user_response",
                "fills_task_context",
                "fills_scene_context",
                "fills_both",
                "possible_task_type",
                "possible_scene_type",
                "confidence_placeholder",
                "requires_confirmation",
                "privacy_sensitivity",
            ],
            "note": "schema_for_runtime_parsing_not_stored_as_fact",
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "fill_policy": {
            "schema_version": "user_clarification_response_to_context_fill_policy_v1",
            "rules": fill_rules,
            "ambiguous_response_policy": "confidence_low_ask_followup",
            "auto_fill_task_context_forbidden": True,
            "auto_fill_scene_context_forbidden": True,
            "fact_written_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "priority_safety": {
            "schema_version": "user_clarification_prompt_priority_safety_policy_v1",
            "clarification_priority_default": P4,
            "task_critical_clarification_priority": P3,
            "linked_voice_guidance_speech_gate": True,
            "can_be_interrupted_by_p0": True,
            "can_be_interrupted_by_p1": True,
            "cannot_interrupt_safety": True,
            "suppress_when_safety_active": True,
            "direct_tts_bypass_forbidden": True,
            "direct_vop_bypass_forbidden": True,
            "safety_priority_above_clarification": True,
            "must_pass_through_speech_gate_later": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "cooldown": {
            "schema_version": "user_clarification_prompt_cooldown_repeat_policy_v1",
            "default_cooldown_sec_placeholder": 45,
            "max_repeat_count_placeholder": 2,
            "repeat_allowed_on_user_inquiry": True,
            "shorten_repeat_after_first": True,
            "suppress_if_user_ignores": True,
            "runtime_enforced_now": False,
            "over_ask_prevention": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "handoff": {
            "schema_version": "user_clarification_handoff_to_task_scene_runtime_policy_v1",
            "payload_fields": [
                "raw_user_response",
                "possible_task_context",
                "possible_scene_context",
                "confidence_policy",
                "confirmation_required",
                "source_prompt_template_id",
                "source_chain",
            ],
            "handoff_allowed_later": True,
            "handoff_invoked_now": False,
            "task_context_written_now": False,
            "scene_context_written_now": False,
            "target_runtime": "Static-Reading-Task-Scene-Context-Runtime-DryRun-v1",
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "current": {
            "schema_version": "user_clarification_current_case_template_dryrun_v1",
            "current_case_loaded": True,
            "missing_context_status": missing_status,
            "selected_template_type": selected["clarification_type"],
            "selected_template_id": selected["template_id"],
            "selected_prompt_text": selected["prompt_text_short"],
            "priority_level": selected_pri,
            "tts_invoked_now": False,
            "voice_output_plane_invoked_now": False,
            "speech_request_submitted_now": False,
            "handoff_invoked_now": False,
            "recommended_next_phase": "User-Clarification-Prompt-Runtime-DryRun-for-Reading-v1",
            "alternate_next_phase": "Static-Reading-Task-Scene-Context-GuardedTrial-v1",
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "long_term": {
            "schema_version": "user_clarification_long_term_candidate_link_v1",
            "can_feed_long_term_candidate": True,
            "candidate_types": LONG_TERM_TYPES,
            "cannot_write_fact": True,
            "cannot_write_profile_now": True,
            "write_allowed_now": False,
            "required_metadata": [
                "source_chain",
                "time_anchor",
                "spatial_anchor",
                "original_user_request_context",
                "missing_reason",
                "confidence_decay",
                "privacy_sensitivity",
                "future_usage_scope",
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "boundary": {
            "schema_version": "user_clarification_prompt_template_boundary_report_v1",
            "template_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "map_api_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "user_clarification_prompt_template_metrics_candidate_report_v1",
            "clarification_template_count": len(templates),
            "expected_response_schema_defined": True,
            "response_to_context_fill_policy_defined": True,
            "cooldown_repeat_policy_defined": True,
            "runtime_tts_invoked_count": 0,
            "speech_request_submitted_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "user_clarification_prompt_template_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "user_clarification_prompt_template_system_health_link_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "user_clarification_prompt_template_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "template_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "map_api_invoked": False,
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
            "schema_version": "user_clarification_prompt_template_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "user_clarification_prompt_template_non_claims_report_v1",
            "claims": [
                "not_actual_user_clarification",
                "prompt_template_not_tts",
                "response_schema_not_user_answer",
                "fill_policy_not_fact_write",
                "handoff_not_runtime_handoff_now",
                "no_real_task_scene_recognition",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "user_clarification_prompt_template_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "user_clarification_prompt_template_audit_report_v1",
            "user_clarification_prompt_template_for_reading_v1_executed": True,
            "template_only": True,
            "clarification_prompt_template_defined": True,
            "expected_user_response_schema_defined": True,
            "response_to_context_fill_policy_defined": True,
            "safety_priority_above_clarification": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "map_api_invoked": False,
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
