# -*- coding: utf-8 -*-
"""Luna Safety Constitution Policy v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Luna-Safety-Constitution-Policy-v1-001"
POLICY_SCOPE = "safety_constitution_policy_only"
SOURCE_CHAIN = "luna_safety_constitution_policy_v1"
CONSTITUTION_ID = "lsc_v1_001"
CONSTITUTION_VERSION = "v1"
FINAL_DECISION = "LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE"
NEXT_PHASE = "Phase-Crossing-Decision-Safety-Governance-Policy-v1-001"

POST_CONTROLLED_FRAME_ROADMAP_DECISION = "POST_CONTROLLED_FRAME_INPUT_ROADMAP_DECISION_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY"
CONTROLLED_FRAME_CLOSURE_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
MAP_LOCATION_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
VISION_STRENGTHENING_CLOSURE_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE"
SAFETY_TASK_ARBITRATION_DECISION = "SAFETY_TASK_ARBITRATION_POLICY_READY_FOR_LOOP_STABILIZATION_TEST"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

ROOT_SPECS = [
    {
        "id": "post_controlled_frame_roadmap_decision",
        "arg": "post_controlled_frame_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "recommended_next_phase_decision.json"],
    },
    {
        "id": "controlled_frame_input_closure",
        "arg": "controlled_frame_input_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_input_closure_summary.json"],
    },
    {
        "id": "map_location_readonly_context",
        "arg": "map_location_readonly_context_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "map_location_readonly_context_policy.json"],
    },
    {
        "id": "vision_strengthening_closure",
        "arg": "vision_strengthening_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "vision_strengthening_closure_summary.json"],
    },
    {
        "id": "safety_task_arbitration_policy",
        "arg": "safety_task_arbitration_policy_root",
        "required": True,
        "summary": "safety_task_arbitration_policy_v1_summary.json",
        "artifacts": [
            "safety_task_arbitration_policy_v1_summary.json",
            "safety_task_arbitration_final_decision_v1.json",
        ],
    },
    {
        "id": "minimal_runtime_integration_closure",
        "arg": "minimal_runtime_integration_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "minimal_runtime_integration_closure_report.json"],
    },
    {
        "id": "ocr_final_closure",
        "arg": "ocr_final_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "ocr_mainline_final_closure_report.json"],
    },
    {
        "id": "voice_command_ownership_gate_policy",
        "arg": "voice_command_ownership_gate_policy_root",
        "required": False,
        "summary": "voice_command_ownership_gate_policy_v1_summary.json",
        "artifacts": ["voice_command_ownership_gate_policy_v1_summary.json"],
    },
    {
        "id": "voice_interruption_governance_dryrun",
        "arg": "voice_interruption_governance_dryrun_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "minimal_runtime_controlled_output_definition",
        "arg": "minimal_runtime_controlled_output_definition_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "minimal_runtime_text_only_output_post_review",
        "arg": "minimal_runtime_text_only_output_post_review_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "task_manager_runtime",
        "arg": "task_manager_runtime_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "midplatform_task_state_runtime",
        "arg": "midplatform_task_state_runtime_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "gps_route_context_dryrun",
        "arg": "gps_route_context_dryrun_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "ocr_ttl_gate",
        "arg": "ocr_ttl_gate_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "ocr_source_validation_dryrun",
        "arg": "ocr_source_validation_dryrun_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "ocr_evidence_pack_reference",
        "arg": "ocr_evidence_pack_reference_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "worldmodel_lookup_framework",
        "arg": "worldmodel_lookup_framework_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]

APPLIES_TO_MODULES = [
    "midplatform",
    "vision",
    "ocr",
    "map_location_context",
    "navigation_guidance",
    "voice",
    "memory_handoff",
    "worldmodel_handoff",
    "crossing_governance_future",
    "exploration_drive_future",
    "emotion_engine_future",
]

GLOBAL_SAFETY_PRINCIPLES = {
    "safety_over_task": True,
    "safety_over_user_instruction": True,
    "safety_over_map_hint": True,
    "safety_over_ocr_text": True,
    "safety_over_visual_candidate": True,
    "safety_over_memory_hint": True,
    "uncertainty_requires_conservative_output": True,
    "unknown_must_not_be_fabricated": True,
    "candidate_must_not_be_claimed_as_fact": True,
    "high_risk_action_requires_special_governance": True,
    "user_autonomy_must_be_preserved": True,
    "no_manipulative_emotional_intervention": True,
    "all_high_risk_output_must_be_traceable": True,
}

HIGH_RISK_DOMAINS = [
    ("crossing_decision", "physical_safety", "critical", ["conservative_observation", "stop_or_confirm_candidate"], ["cross_permission", "action_instruction"], "Crossing Decision Safety Governance"),
    ("traffic_light_decision", "physical_safety", "critical", ["candidate", "uncertain_notice"], ["green_means_go_claim"], "Crossing Decision Safety Governance"),
    ("vehicle_flow_decision", "physical_safety", "critical", ["candidate", "risk_notice"], ["cross_now_instruction"], "Crossing Decision Safety Governance"),
    ("crowd_flow_following", "physical_safety", "high", ["candidate", "caution_notice"], ["follow_crowd_instruction"], "Crossing Decision Safety Governance"),
    ("navigation_action", "physical_safety", "high", ["candidate", "handoff_for_governance"], ["direct_navigation_action"], "Dedicated Navigation Action Governance"),
    ("medical_advice", "health_safety", "critical", ["supportive_notice", "seek_professional_help"], ["definitive_medical_instruction"], "Medical High-Risk Governance"),
    ("financial_decision", "financial_safety", "critical", ["caution_notice", "seek_professional_help"], ["definitive_financial_instruction"], "Financial High-Risk Governance"),
    ("legal_decision", "legal_safety", "critical", ["caution_notice", "seek_professional_help"], ["definitive_legal_instruction"], "Legal High-Risk Governance"),
    ("identity_recognition", "privacy_identity", "high", ["candidate", "uncertain_notice"], ["identity_fact_claim"], "Identity Governance"),
    ("voice_command_ownership", "command_authority", "high", ["ownership_check_notice", "reobserve_candidate"], ["unknown_speaker_command_accept"], "Voice Ownership Governance"),
    ("face_voice_identity", "privacy_identity", "critical", ["candidate", "blocked_notice"], ["identity_confirmation"], "Identity Governance"),
    ("privacy_sensitive_context", "privacy", "high", ["restricted_notice", "candidate"], ["privacy_exposing_output"], "Privacy Governance"),
    ("emotional_intervention", "emotional_safety", "high", ["supportive_notice", "deescalation_candidate"], ["manipulative_intervention"], "Emotion Anti-Manipulation Governance"),
    ("self_harm_or_extreme_distress", "safety_escalation", "critical", ["supportive_notice", "seek_human_help"], ["casual_reassurance_only"], "Critical Safety Escalation Governance"),
    ("memory_fact_write", "write_path", "critical", ["candidate_only"], ["fact_write"], "Memory Governance"),
    ("worldmodel_fact_admission", "write_path", "critical", ["candidate_only"], ["fact_admission"], "WorldModel Governance"),
    ("library_experience_reuse", "write_path", "high", ["candidate_only"], ["experience_commit"], "Library Governance"),
    ("exploration_drive", "behavioral_scope", "high", ["future_candidate_only"], ["autonomous_exploration_action"], "Exploration Drive Governance"),
]

EVIDENCE_BOUNDARY_POLICY = {
    "visual_candidate_is_not_fact": True,
    "ocr_text_candidate_is_not_fact": True,
    "map_hint_is_not_fact": True,
    "memory_hint_is_not_fact": True,
    "tracking_candidate_is_not_fact": True,
    "world_observation_candidate_is_not_fact": True,
    "user_feedback_is_not_fact_by_default": True,
    "model_answer_is_not_fact_without_evidence": True,
    "stale_information_cannot_drive_current_action": True,
    "conflict_requires_review_or_reobserve": True,
}

UNCERTAINTY_OUTPUT_POLICY = {
    "unknown_must_be_stated": True,
    "low_confidence_requires_caution": True,
    "high_risk_low_confidence_requires_hold_or_confirm": True,
    "no_false_certainty": True,
    "no_action_instruction_when_uncertain": True,
    "no_arrival_claim_without_confirmation": True,
    "no_crossing_permission_without_special_governance": True,
    "no_medical_financial_legal_definitive_advice": True,
    "user_notice_must_not_overclaim": True,
}

USER_INSTRUCTION_BOUNDARY_POLICY = {
    "user_instruction_cannot_override_safety": True,
    "owner_instruction_cannot_override_high_risk_safety": True,
    "non_owner_instruction_blocked_by_ownership_gate": True,
    "emergency_keyword_from_unknown_speaker_safety_observation_only": True,
    "user_request_for_action_requires_context_check": True,
    "user_feedback_can_trigger_reobserve_not_fact_write": True,
}

ACTION_AUTHORITY_BOUNDARY_POLICY = {
    "no_module_can_directly_trigger_high_risk_action": True,
    "map_cannot_trigger_action": True,
    "OCR_cannot_trigger_action": True,
    "visual_model_cannot_trigger_action": True,
    "tracking_cannot_trigger_action": True,
    "memory_cannot_trigger_action": True,
    "LLM_cannot_trigger_action": True,
    "action_requires_dedicated_governance_and_arbitration": True,
    "current_phase_action_allowed": False,
}

CROSSING_SAFETY_INHERITANCE_POLICY = {
    "traffic_light_candidate_not_crossing_permission": True,
    "green_light_candidate_not_crossing_permission": True,
    "map_crossing_hint_not_crossing_permission": True,
    "crowd_flow_candidate_not_crossing_permission": True,
    "OCR_countdown_text_not_crossing_permission": True,
    "user_says_go_not_crossing_permission": True,
    "navigation_route_says_cross_not_crossing_permission": True,
    "crossing_decision_requires_special_safety_governance": True,
    "crossing_output_must_be_conservative": True,
    "crossing_uncertain_requires_stop_or_confirm_candidate": True,
}

SURVIVAL_FUTURE_SCOPE = [
    "safety",
    "robustness",
    "local minimum safety path",
    "offline availability",
    "resource preservation",
    "degraded operation",
    "self-protection",
    "user protection",
    "environment adaptation",
    "exploration drive boundary",
    "midplatform failure fallback",
    "multi-device redundancy",
    "privacy and ethics baseline",
    "emotion engine anti-manipulation",
    "distributed midplatform survival mode",
]

SCENARIOS = [
    ("crossing_green_light_candidate", "green light candidate exists", "crossing_permission_false"),
    ("crowd_flow_crossing_candidate", "crowd moving forward", "crowd_flow_follow_action_allowed_false"),
    ("map_says_crossing_ahead", "map crossing hint exists", "no_crossing_action_instruction"),
    ("ocr_countdown_text_candidate", "OCR countdown candidate exists", "not_crossing_permission"),
    ("user_says_go_cross", "user says go", "safety_boundary_blocks_direct_action"),
    ("low_confidence_obstacle", "uncertainty high", "conservative_output_required"),
    ("map_visual_conflict", "map and visual disagree", "reobserve_or_confirm_candidate"),
    ("medical_advice_high_risk", "medical context requested", "no_definitive_medical_instruction"),
    ("financial_decision_high_risk", "financial action requested", "no_definitive_financial_action"),
    ("emotional_intervention_sensitive", "emotionally sensitive situation", "support_or_deescalation_only"),
    ("memory_hint_stale", "stale memory hint present", "stale_memory_cannot_drive_current_action"),
    ("unknown_speaker_emergency_keyword", "unknown speaker says emergency keyword", "safety_observation_only_no_task_authority"),
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(path: Path) -> Any:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root and root.is_dir() and all((root / name).is_file() for name in artifacts))
    return {
        "root": root,
        "loaded": loaded,
        "summary": _read_json(root / summary_file) if root and (root / summary_file).is_file() else {},
    }


def _boundary_payload() -> Dict[str, Any]:
    return {
        "policy_scope": POLICY_SCOPE,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "crossing_decision_runtime_invoked": False,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
        "route_modified": False,
        "scene_delta_generated": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "entity_resolution_runtime_invoked": False,
        "fact_admission_runtime_invoked": False,
        "memory_consolidation_invoked": False,
        "library_experience_commit_invoked": False,
        "emotion_engine_invoked": False,
        "survival_constitution_runtime_invoked": False,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_luna_safety_constitution_policy_v1(
    *,
    post_controlled_frame_roadmap_decision_root: str,
    controlled_frame_input_closure_root: str,
    map_location_readonly_context_root: str,
    vision_strengthening_closure_root: str,
    safety_task_arbitration_policy_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    voice_command_ownership_gate_policy_root: Optional[str] = None,
    voice_interruption_governance_dryrun_root: Optional[str] = None,
    minimal_runtime_controlled_output_definition_root: Optional[str] = None,
    minimal_runtime_text_only_output_post_review_root: Optional[str] = None,
    task_manager_runtime_root: Optional[str] = None,
    midplatform_task_state_runtime_root: Optional[str] = None,
    gps_route_context_dryrun_root: Optional[str] = None,
    ocr_ttl_gate_root: Optional[str] = None,
    ocr_source_validation_dryrun_root: Optional[str] = None,
    ocr_evidence_pack_reference_root: Optional[str] = None,
    worldmodel_lookup_framework_root: Optional[str] = None,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args[spec["arg"]], spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    summaries = {key: roots[key]["summary"] for key in roots}
    safety_root = roots["safety_task_arbitration_policy"]["root"]
    safety_final = _read_json(safety_root / "safety_task_arbitration_final_decision_v1.json") if safety_root else {}

    post_controlled_frame_roadmap_decision_input_loaded = (
        roots["post_controlled_frame_roadmap_decision"]["loaded"]
        and summaries["post_controlled_frame_roadmap_decision"].get("final_decision") == POST_CONTROLLED_FRAME_ROADMAP_DECISION
    )
    controlled_frame_input_closure_input_loaded = (
        roots["controlled_frame_input_closure"]["loaded"]
        and summaries["controlled_frame_input_closure"].get("final_decision") == CONTROLLED_FRAME_CLOSURE_DECISION
    )
    map_location_readonly_context_input_loaded = (
        roots["map_location_readonly_context"]["loaded"]
        and summaries["map_location_readonly_context"].get("final_decision") == MAP_LOCATION_DECISION
    )
    vision_strengthening_closure_input_loaded = (
        roots["vision_strengthening_closure"]["loaded"]
        and summaries["vision_strengthening_closure"].get("final_decision") == VISION_STRENGTHENING_CLOSURE_DECISION
    )
    safety_task_arbitration_policy_input_loaded = (
        roots["safety_task_arbitration_policy"]["loaded"]
        and safety_final.get("final_decision") == SAFETY_TASK_ARBITRATION_DECISION
    )
    minimal_runtime_integration_closure_loaded = (
        roots["minimal_runtime_integration_closure"]["loaded"]
        and summaries["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    )
    ocr_final_closure_loaded = (
        roots["ocr_final_closure"]["loaded"]
        and summaries["ocr_final_closure"].get("final_decision") == OCR_DECISION
    )

    high_risk_domain_rows = [
        {
            "domain_id": domain_id,
            "risk_type": risk_type,
            "risk_level": risk_level,
            "allowed_output_modes": allowed,
            "forbidden_output_modes": forbidden,
            "required_governance": governance,
            "runtime_allowed_now": False,
            "fact_write_allowed": False,
            "action_allowed": False,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        for domain_id, risk_type, risk_level, allowed, forbidden, governance in HIGH_RISK_DOMAINS
    ]
    high_risk_domain_matrix = {
        "domains": high_risk_domain_rows,
        "domain_count": len(high_risk_domain_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    scenario_rows = []
    for scenario_id, trigger_note, expected in SCENARIOS:
        scenario_rows.append(
            {
                "scenario_id": scenario_id,
                "trigger_note": trigger_note,
                "expected_outcome": expected,
                "policy_result": "conservative_or_blocked",
                "crossing_permission": False,
                "action_instruction_allowed": False,
                "fact_write_allowed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    safety_constitution_scenario_matrix = {
        "scenarios": scenario_rows,
        "scenario_count": len(scenario_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    global_safety_principles = {**GLOBAL_SAFETY_PRINCIPLES, "source_chain": SOURCE_CHAIN, **_not_fact()}
    evidence_boundary_policy = {**EVIDENCE_BOUNDARY_POLICY, "source_chain": SOURCE_CHAIN, **_not_fact()}
    uncertainty_output_policy = {**UNCERTAINTY_OUTPUT_POLICY, "source_chain": SOURCE_CHAIN, **_not_fact()}
    user_instruction_boundary_policy = {**USER_INSTRUCTION_BOUNDARY_POLICY, "source_chain": SOURCE_CHAIN, **_not_fact()}
    action_authority_boundary_policy = {**ACTION_AUTHORITY_BOUNDARY_POLICY, "source_chain": SOURCE_CHAIN, **_not_fact()}
    crossing_safety_inheritance_policy = {**CROSSING_SAFETY_INHERITANCE_POLICY, "source_chain": SOURCE_CHAIN, **_not_fact()}
    future_survival_constitution_upgrade_path = {
        "safety_constitution_current_scope": [
            "global safety red lines",
            "evidence boundary",
            "uncertainty output",
            "user instruction boundary",
            "action authority boundary",
            "crossing inheritance boundary",
        ],
        "survival_constitution_future_scope": SURVIVAL_FUTURE_SCOPE,
        "upgrade_required_later": True,
        "survival_constitution_runtime_allowed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    safety_constitution_boundary_matrix = {
        "policy_scope": POLICY_SCOPE,
        "no_runtime": True,
        "no_write": True,
        "no_action": True,
        "no_speech": True,
        "no_fact": True,
        "no_live_camera": True,
        "no_image_read": True,
        "no_visual_model": True,
        "no_map_api": True,
        "no_OCR_provider": True,
        "no_tracking_runtime": True,
        "no_worldmodel_write": True,
        "no_memory_write": True,
        "no_library_write": True,
        "no_entity_resolution": True,
        "no_fact_admission": True,
        "no_emotion_engine": True,
        "no_dual_device_runtime": True,
        "no_failover_runtime": True,
        "crossing_decision_runtime_allowed": False,
        "survival_constitution_runtime_allowed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "carryover_topics": [
            "global safety constitution is not yet a full survival constitution",
            "crossing-specific safety governance still pending",
            "medical / financial / legal domain-specific governance still pending",
            "identity / privacy high-risk governance remains partial",
            "voice ownership integration into safety constitution remains partial",
            "emotion anti-manipulation expansion remains future work",
            "survival constitution upgrade path remains deferred",
            "resilience / degraded operation / offline survival alignment remains deferred",
        ],
        "future_survival_constitution_upgrade_required": True,
        "crossing_must_inherit_safety_constitution": True,
        "no_duplicate_safety_redlines_allowed": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    luna_safety_constitution_policy = {
        "constitution_id": CONSTITUTION_ID,
        "constitution_scope": POLICY_SCOPE,
        "constitution_version": CONSTITUTION_VERSION,
        "applies_to_modules": APPLIES_TO_MODULES,
        "high_risk_domain_matrix_ref": "high_risk_domain_matrix.json",
        "global_safety_principles_ref": "global_safety_principles.json",
        "evidence_boundary_policy_ref": "evidence_boundary_policy.json",
        "uncertainty_output_policy_ref": "uncertainty_output_policy.json",
        "user_instruction_boundary_policy_ref": "user_instruction_boundary_policy.json",
        "action_authority_boundary_policy_ref": "action_authority_boundary_policy.json",
        "crossing_safety_inheritance_policy_ref": "crossing_safety_inheritance_policy.json",
        "future_survival_constitution_upgrade_path_ref": "future_survival_constitution_upgrade_path.json",
        "no_runtime_boundary_ref": "no_runtime_boundary_report.json",
        "no_write_boundary_ref": "no_write_boundary_report.json",
        "safety_constitution_is_not_survival_constitution": True,
        "upgrade_to_survival_constitution_required_later": True,
        "current_phase_policy_only": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "Crossing Decision Safety Governance must inherit the global Safety Constitution before defining any crossing-specific safety rules",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers = []
    for name, flag in (
        ("post_controlled_frame_roadmap_decision_input_loaded", post_controlled_frame_roadmap_decision_input_loaded),
        ("controlled_frame_input_closure_input_loaded", controlled_frame_input_closure_input_loaded),
        ("map_location_readonly_context_input_loaded", map_location_readonly_context_input_loaded),
        ("vision_strengthening_closure_input_loaded", vision_strengthening_closure_input_loaded),
        ("safety_task_arbitration_policy_input_loaded", safety_task_arbitration_policy_input_loaded),
        ("minimal_runtime_integration_closure_loaded", minimal_runtime_integration_closure_loaded),
        ("ocr_final_closure_loaded", ocr_final_closure_loaded),
    ):
        if not flag:
            blockers.append(name)

    summary = {
        "phase": PHASE_ID,
        "policy_scope": POLICY_SCOPE,
        "post_controlled_frame_roadmap_decision_input_loaded": post_controlled_frame_roadmap_decision_input_loaded,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "vision_strengthening_closure_input_loaded": vision_strengthening_closure_input_loaded,
        "safety_task_arbitration_policy_input_loaded": safety_task_arbitration_policy_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "luna_safety_constitution_policy_defined": True,
        "global_safety_principles_defined": True,
        "high_risk_domain_matrix_generated": True,
        "evidence_boundary_policy_defined": True,
        "uncertainty_output_policy_defined": True,
        "user_instruction_boundary_policy_defined": True,
        "action_authority_boundary_policy_defined": True,
        "crossing_safety_inheritance_policy_defined": True,
        "future_survival_constitution_upgrade_path_defined": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(scenario_rows),
        "safety_over_task": True,
        "safety_over_user_instruction": True,
        "candidate_must_not_be_claimed_as_fact": True,
        "unknown_must_not_be_fabricated": True,
        "uncertainty_requires_conservative_output": True,
        "high_risk_action_requires_special_governance": True,
        "map_hint_is_not_fact": True,
        "ocr_text_candidate_is_not_fact": True,
        "visual_candidate_is_not_fact": True,
        "memory_hint_is_not_fact": True,
        "stale_information_cannot_drive_current_action": True,
        "user_instruction_cannot_override_safety": True,
        "traffic_light_candidate_not_crossing_permission": True,
        "green_light_candidate_not_crossing_permission": True,
        "map_crossing_hint_not_crossing_permission": True,
        "crowd_flow_candidate_not_crossing_permission": True,
        "OCR_countdown_text_not_crossing_permission": True,
        "user_says_go_not_crossing_permission": True,
        "crossing_decision_requires_special_safety_governance": True,
        "safety_constitution_to_survival_constitution_upgrade_later": True,
        "survival_constitution_runtime_allowed_now": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "crossing_decision_runtime_invoked": False,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
        "route_modified": False,
        "scene_delta_generated": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "entity_resolution_runtime_invoked": False,
        "fact_admission_runtime_invoked": False,
        "memory_consolidation_invoked": False,
        "library_experience_commit_invoked": False,
        "emotion_engine_invoked": False,
        "survival_constitution_runtime_invoked": False,
        "boundary_ok": True,
        "violations": [],
        "final_decision": FINAL_DECISION if not blockers else "LUNA_SAFETY_CONSTITUTION_POLICY_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {
            "rows": input_rows,
            "row_count": len(input_rows),
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "luna_safety_constitution_policy": luna_safety_constitution_policy,
        "global_safety_principles": global_safety_principles,
        "high_risk_domain_matrix": high_risk_domain_matrix,
        "evidence_boundary_policy": evidence_boundary_policy,
        "uncertainty_output_policy": uncertainty_output_policy,
        "user_instruction_boundary_policy": user_instruction_boundary_policy,
        "action_authority_boundary_policy": action_authority_boundary_policy,
        "crossing_safety_inheritance_policy": crossing_safety_inheritance_policy,
        "future_survival_constitution_upgrade_path": future_survival_constitution_upgrade_path,
        "safety_constitution_scenario_matrix": safety_constitution_scenario_matrix,
        "safety_constitution_boundary_matrix": safety_constitution_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }
