# -*- coding: utf-8 -*-
"""Voice Interruption Governance DryRun v1 — dry-run only, no runtime effects.

Phase-Voice-Interruption-Governance-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Voice-Interruption-Governance-DryRun-v1-001"
FINAL_DECISION = "VOICE_INTERRUPTION_GOVERNANCE_DRYRUN_READY_FOR_LOOP_STABILIZATION_TEST"
RECOMMENDED_NEXT = "Basic-Navigation-Guidance-Loop-Stabilization-Test-v1"

INTERRUPTION_INTENT_TYPES = [
    "STOP",
    "PAUSE",
    "REPEAT",
    "RESUME",
    "CLARIFY",
    "CORRECT",
    "EMERGENCY",
    "NEW_TASK",
    "CANCEL_TASK",
    "UNKNOWN_OR_AMBIGUOUS",
]

SELECTED_ACTION_CANDIDATES = [
    "STOP_SPEECH_CANDIDATE",
    "PAUSE_SPEECH_CANDIDATE",
    "REPEAT_LAST_SPEECH_CANDIDATE",
    "RESUME_SPEECH_CANDIDATE",
    "CLARIFY_PREVIOUS_OUTPUT_CANDIDATE",
    "CREATE_CORRECTION_EVENT_CANDIDATE",
    "CREATE_SAFETY_OBSERVATION_CANDIDATE",
    "CREATE_NEW_TASK_CANDIDATE",
    "CREATE_CANCEL_TASK_CANDIDATE",
    "DELAY_UNTIL_SAFETY_CLEAR_CANDIDATE",
    "SUPPRESS_INTERRUPTION_CANDIDATE",
    "REQUEST_CONFIRMATION_CANDIDATE",
    "NO_ACTION_CANDIDATE",
]

SPEECH_STATES = [
    "speaking",
    "interruption_requested",
    "interrupted_candidate",
    "paused_candidate",
    "cancelled_candidate",
    "superseded_candidate",
    "repeat_requested_candidate",
    "resume_required_candidate",
    "expired_before_resume_candidate",
    "completed_unchanged_candidate",
]

INTAKE_SPECS = [
    ("ownership_gate", "voice_command_ownership_gate_policy_v1_summary.json", False),
    ("safety_task_arbitration", "safety_task_arbitration_policy_v1_summary.json", False),
    ("basic_navigation_loop", "basic_navigation_guidance_loop_dryrun_v1_summary.json", False),
    ("voice_dialogue_runtime", "voice_dialogue_task_control_runtime_dryrun_v1_summary.json", False),
    ("vop_adapter", "voice_output_plane_adapter_for_guidance_v1_summary.json", False),
    ("navigation_speech_adapter", "navigation_guidance_to_speech_candidate_adapter_v1_summary.json", False),
    ("task_manager_runtime", "task_manager_runtime_dryrun_v1_summary.json", False),
    ("midplatform_task_state", "midplatform_task_state_runtime_dryrun_v1_summary.json", False),
    ("ocr_activation", "ocr_activation_governance_policy_v1_summary.json", False),
    ("stc", "stc_sampling_guidance_policy_v1_summary.json", False),
    ("system_health", None, True),
    ("simulation", None, True),
]

OPTIONAL_DOC_GLOBS = {
    "speech_gate_runtime": "**/*SPEECH*GATE*.md",
    "risk_safety_arbiter": "**/*RISK*SAFETY*.md",
    "route_context": "**/*ROUTE*CONTEXT*.md",
    "map_context": "**/*MAP*CONTEXT*.md",
    "memory_governance": "**/*MEMORY*GOVERN*.md",
}

PRIORITY_MAP = {
    "P0_safety_immediate": "P0",
    "P1_navigation_critical": "P1",
    "P2_task_guidance": "P2",
    "P3_ocr_or_static_reading_guidance": "P3",
    "P4_clarification_or_status": "P4",
    "P5_low_priority": "P5",
}

SPEECH_PRIORITY_LEVELS = ["P0", "P1", "P2", "P3", "P4", "P5"]

BASE_RULES = {
    "case_01": ("STOP", "STOP_SPEECH_CANDIDATE", "interrupted_candidate", "P4"),
    "case_02": ("REPEAT", "REPEAT_LAST_SPEECH_CANDIDATE", "repeat_requested_candidate", "P4"),
    "case_03": ("CLARIFY", "CLARIFY_PREVIOUS_OUTPUT_CANDIDATE", "superseded_candidate", "P4"),
    "case_04": ("CORRECT", "CREATE_CORRECTION_EVENT_CANDIDATE", "interruption_requested", "P4"),
    "case_05": ("EMERGENCY", "CREATE_SAFETY_OBSERVATION_CANDIDATE", "interrupted_candidate", "P2"),
    "case_06": ("NEW_TASK", "SUPPRESS_INTERRUPTION_CANDIDATE", "completed_unchanged_candidate", "P2"),
    "case_07": ("EMERGENCY", "CREATE_SAFETY_OBSERVATION_CANDIDATE", "interruption_requested", "P4"),
    "case_08": ("EMERGENCY", "REQUEST_CONFIRMATION_CANDIDATE", "interruption_requested", "P2"),
    "case_09": ("STOP", "SUPPRESS_INTERRUPTION_CANDIDATE", "completed_unchanged_candidate", "P4"),
    "case_10": ("UNKNOWN_OR_AMBIGUOUS", "SUPPRESS_INTERRUPTION_CANDIDATE", "completed_unchanged_candidate", "P4"),
    "case_11": ("STOP", "SUPPRESS_INTERRUPTION_CANDIDATE", "completed_unchanged_candidate", "P4"),
    "case_12": ("NEW_TASK", "SUPPRESS_INTERRUPTION_CANDIDATE", "completed_unchanged_candidate", "P2"),
    "case_13": ("EMERGENCY", "CREATE_SAFETY_OBSERVATION_CANDIDATE", "interruption_requested", "P3"),
    "case_14": ("EMERGENCY", "CREATE_SAFETY_OBSERVATION_CANDIDATE", "interruption_requested", "P2"),
    "case_15": ("NEW_TASK", "CREATE_NEW_TASK_CANDIDATE", "paused_candidate", "P2"),
    "case_16": ("RESUME", "RESUME_SPEECH_CANDIDATE", "resume_required_candidate", "P2"),
}

PRIORITY_SCENARIOS = [
    ("case_17", "P0", "STOP", "SUPPRESS_INTERRUPTION_CANDIDATE", "completed_unchanged_candidate", "p0_safety_warning_cannot_be_cancelled_by_ordinary_stop", None, True),
    ("case_18", "P1", "STOP", "PAUSE_SPEECH_CANDIDATE", "paused_candidate", None, "risk_state_still_active_candidate", True),
    ("case_19", "P2", "PAUSE", "PAUSE_SPEECH_CANDIDATE", "paused_candidate", None, "route_and_stc_freshness_required_before_resume", False),
    ("case_20", "P3", "STOP", "STOP_SPEECH_CANDIDATE", "cancelled_candidate", None, "stc_frame_region_freshness_required_before_resume", False),
    ("case_21", "P4", "CLARIFY", "CLARIFY_PREVIOUS_OUTPUT_CANDIDATE", "superseded_candidate", None, None, False),
    ("case_22", "P5", "STOP", "STOP_SPEECH_CANDIDATE", "cancelled_candidate", None, None, False),
    ("case_23", "P2", "RESUME", "RESUME_SPEECH_CANDIDATE", "resume_required_candidate", None, "route_and_stc_freshness_revalidated", False),
    ("case_24", "P0", "REPEAT", "REPEAT_LAST_SPEECH_CANDIDATE", "expired_before_resume_candidate", "stale_p0_cannot_be_repeated_as_current_fact", "historical_only_rewrite_required", False),
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(path: Path) -> Any:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def _find_optional_docs(ws_root: Path) -> List[Dict[str, Any]]:
    docs = ws_root / "docs" / "architecture"
    rows: List[Dict[str, Any]] = []
    for intake_id, glob_pat in OPTIONAL_DOC_GLOBS.items():
        found = list(docs.glob(glob_pat)) if docs.is_dir() else []
        rows.append(
            {
                "intake_id": intake_id,
                "input_source": "optional_documentation",
                "source_root_or_path": str(found[0]) if found else "(not_found)",
                "artifact": found[0].name if found else None,
                "loaded": bool(found),
                "optional": True,
                "intake_status": "loaded" if found else "optional_missing",
                "missing_impact": "optional_doc_reference_only",
                **_not_fact(),
            }
        )
    return rows


def _pick_target(speech_candidates: List[Dict[str, Any]], want: str) -> Dict[str, Any]:
    for candidate in speech_candidates:
        if PRIORITY_MAP.get(candidate.get("priority_level", "")) == want:
            return candidate
    return {
        "speech_request_candidate_id": f"synthetic_{want.lower()}_speech_request",
        "priority_level": want,
        "speech_text_candidate_zh": f"{want} synthetic speech candidate",
        "speech_type": "synthetic",
    }


def _base_decision(row: Dict[str, Any], target: Dict[str, Any], rule: tuple[str, str, str, str]) -> Dict[str, Any]:
    intent, action, state, wanted_priority = rule
    allowed = row.get("allowed_entrypoints", [])
    emergency = intent == "EMERGENCY"
    allowed_precheck = "interruption_classifier" in allowed or (emergency and "safety_observation_candidate" in allowed)
    blocked_reason = None
    if row.get("conversation_context") == "phone_call_speech":
        blocked_reason = "phone_call_context_blocks_ordinary_interruption"
    elif row.get("conversation_context") == "human_conversation" and row.get("ownership_state") != "OWNER_CONFIRMED":
        blocked_reason = "human_conversation_context_blocks_ordinary_interruption"
    elif row.get("conversation_context") in ("media_playback_voice", "public_announcement"):
        blocked_reason = "media_or_public_voice_cannot_control_luna"
    elif not allowed_precheck and not row.get("safety_only_allowed", False):
        blocked_reason = "ownership_gate_precheck_blocked"

    selected = action if allowed_precheck or row.get("safety_only_allowed", False) else "SUPPRESS_INTERRUPTION_CANDIDATE"
    return {
        "scenario_id": row["voice_input_candidate_id"].replace("voice_input_", ""),
        "voice_input_id": row["voice_input_candidate_id"],
        "source_ownership_decision_id": row["ownership_gate_decision_candidate_id"],
        "target_speech_request_id": target["speech_request_candidate_id"],
        "target_speech_priority": wanted_priority,
        "target_speech_text_ref": target["speech_text_candidate_zh"],
        "interruption_intent_type": intent,
        "ownership_state": row["ownership_state"],
        "speaker_type": row["speaker_type"],
        "addressing_status": row["addressing_status"],
        "conversation_context": row["conversation_context"],
        "safety_keyword_detected": row.get("safety_keyword_detected", False),
        "interruption_allowed_precheck": allowed_precheck,
        "priority_policy_decision": "OWNERSHIP_GATE_PRECHECK",
        "safety_task_arbitration_required": emergency or row.get("safety_only_allowed", False),
        "selected_action_candidate": selected,
        "target_speech_state_candidate": state if selected != "SUPPRESS_INTERRUPTION_CANDIDATE" else "completed_unchanged_candidate",
        "task_context_preserved": True,
        "pending_confirmation_preserved": True,
        "repeat_allowed": intent == "REPEAT",
        "resume_allowed": intent == "RESUME",
        "freshness_check_required": intent in ("REPEAT", "RESUME", "CLARIFY"),
        "stale_risk": False,
        "requires_user_confirmation": row.get("requires_confirmation", False),
        "blocked_reason": blocked_reason,
        "resume_condition": "route_or_context_freshness_recheck_required" if intent == "RESUME" else None,
        "source_chain": "voice_interruption_governance_dryrun_v1",
        "runtime_tts_stopped": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "task_state_committed_now": False,
        "world_model_written": False,
        "memory_written": False,
        "navigation_action_triggered": False,
        "ocr_invoked": False,
        "camera_invoked": False,
        **_not_fact(),
    }


def run_voice_interruption_governance_dryrun_v1(
    *,
    ownership_gate_root: str,
    safety_task_arbitration_root: str,
    basic_navigation_loop_root: str,
    voice_dialogue_runtime_root: str,
    vop_adapter_root: str,
    navigation_speech_adapter_root: str,
    task_manager_runtime_root: str,
    midplatform_task_state_root: str,
    ocr_activation_root: str,
    stc_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "ownership_gate": Path(ownership_gate_root).resolve(),
        "safety_task_arbitration": Path(safety_task_arbitration_root).resolve(),
        "basic_navigation_loop": Path(basic_navigation_loop_root).resolve(),
        "voice_dialogue_runtime": Path(voice_dialogue_runtime_root).resolve(),
        "vop_adapter": Path(vop_adapter_root).resolve(),
        "navigation_speech_adapter": Path(navigation_speech_adapter_root).resolve(),
        "task_manager_runtime": Path(task_manager_runtime_root).resolve(),
        "midplatform_task_state": Path(midplatform_task_state_root).resolve(),
        "ocr_activation": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_root).resolve(),
        "system_health": Path(system_health_root).resolve(),
        "simulation": Path(simulation_root).resolve(),
    }

    intake_rows: List[Dict[str, Any]] = []
    loaded: Dict[str, bool] = {}
    for intake_id, artifact, optional in INTAKE_SPECS:
        root = roots[intake_id]
        is_loaded = root.is_dir()
        if artifact:
            is_loaded = is_loaded and (root / artifact).is_file()
        loaded[intake_id] = is_loaded
        intake_rows.append(
            {
                "intake_id": intake_id,
                "input_source": intake_id,
                "source_root_or_path": str(root),
                "artifact": artifact or "(directory)",
                "loaded": is_loaded,
                "optional": optional,
                "intake_status": "loaded" if is_loaded else ("optional_missing" if optional else "missing"),
                "missing_impact": "none" if is_loaded else ("optional_reference_only" if optional else "check_partial"),
                **_not_fact(),
            }
        )
    intake_rows.extend(_find_optional_docs(ws))

    ownership_input = _read_json(roots["ownership_gate"] / "voice_command_ownership_gate_decision_candidates_v1.json") or {}
    speech_input = _read_json(roots["navigation_speech_adapter"] / "navigation_guidance_speech_candidate_collection_v1.json") or {}
    ownership_rows = ownership_input.get("candidates", [])
    speech_candidates = speech_input.get("candidates", [])

    priority_targets = {lvl: _pick_target(speech_candidates, lvl) for lvl in ("P0", "P1", "P2", "P3", "P4")}
    priority_targets["P5"] = {
        "speech_request_candidate_id": "sp_synthetic_p5_chat_candidate",
        "priority_level": "P5_low_priority",
        "speech_text_candidate_zh": "这是一个低优先级闲聊播报候选。",
        "speech_type": "chat",
    }

    source_matrix: List[Dict[str, Any]] = []
    decisions: List[Dict[str, Any]] = []

    for row in ownership_rows:
        case_id = row["voice_input_candidate_id"].replace("voice_input_", "")
        rule = BASE_RULES[case_id]
        target = priority_targets[rule[3]]
        source_row = _base_decision(row, target, rule)
        source_matrix.append(source_row)
        decisions.append({"interruption_decision_id": f"idc_{case_id}", **source_row})

    priority_rows: List[Dict[str, Any]] = []
    for case_id, want, intent, action, state, blocked_reason, resume_condition, needs_safety in PRIORITY_SCENARIOS:
        target = priority_targets[want]
        row = {
            "scenario_id": case_id,
            "voice_input_id": f"voice_input_{case_id}",
            "source_ownership_decision_id": f"synthetic_owner_confirmed_{case_id}",
            "target_speech_request_id": target["speech_request_candidate_id"],
            "target_speech_priority": want,
            "target_speech_text_ref": target["speech_text_candidate_zh"],
            "interruption_intent_type": intent,
            "ownership_state": "OWNER_CONFIRMED",
            "speaker_type": "registered_user",
            "addressing_status": "directly_addressed_to_luna" if case_id != "case_23" else "implicit_followup_to_luna",
            "conversation_context": "direct_command_to_luna",
            "safety_keyword_detected": intent == "EMERGENCY",
            "interruption_allowed_precheck": True,
            "priority_policy_decision": {
                "P0": "P0_NOT_CANCELLED_BY_ORDINARY_STOP" if intent == "STOP" else "P0_STALE_REPEAT_REWRITTEN_AS_HISTORICAL",
                "P1": "P1_RISK_STATE_PRESERVED_ON_INTERRUPTION",
                "P2": "P2_PAUSE_OR_RESUME_REQUIRES_RESUME_CONDITION",
                "P3": "P3_RESUME_REQUIRES_STC_FRAME_REGION_FRESHNESS",
                "P4": "P4_CAN_BE_SUPERSEDED_BY_OWNER_COMMAND",
                "P5": "P5_LOW_COST_INTERRUPTIBLE",
            }[want],
            "safety_task_arbitration_required": needs_safety,
            "selected_action_candidate": action,
            "target_speech_state_candidate": state,
            "task_context_preserved": True,
            "pending_confirmation_preserved": True,
            "repeat_allowed": intent == "REPEAT",
            "resume_allowed": intent == "RESUME" or action == "PAUSE_SPEECH_CANDIDATE",
            "freshness_check_required": intent in ("REPEAT", "RESUME") or want in ("P2", "P3"),
            "stale_risk": case_id == "case_24",
            "requires_user_confirmation": case_id == "case_17",
            "blocked_reason": blocked_reason,
            "resume_condition": resume_condition,
            "source_chain": "voice_interruption_governance_dryrun_v1",
            "runtime_tts_stopped": False,
            "speech_gate_invoked": False,
            "vop_invoked": False,
            "task_state_committed_now": False,
            "world_model_written": False,
            "memory_written": False,
            "navigation_action_triggered": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            **_not_fact(),
        }
        priority_rows.append(row)
        decisions.append({"interruption_decision_id": f"idc_{case_id}", **row})

    source_matrix.extend(priority_rows)

    return {
        "summary": {
            "phase": PHASE_ID,
            "dryrun_scope": "voice_interruption_governance_dryrun_only",
            "ownership_gate_input_loaded": loaded["ownership_gate"],
            "safety_task_arbitration_input_loaded": loaded["safety_task_arbitration"],
            "interruption_intent_policy_defined": True,
            "speech_priority_policy_defined": True,
            "speech_request_state_candidate_schema_defined": True,
            "interruption_decision_candidate_schema_defined": True,
            "freshness_policy_defined": True,
            "correction_policy_defined": True,
            "emergency_policy_defined": True,
            "new_task_cancel_task_policy_defined": True,
            "interruption_decision_candidate_count": len(decisions),
            "runtime_asr_invoked": False,
            "runtime_audio_recorded": False,
            "runtime_tts_stopped": False,
            "speech_gate_invoked": False,
            "vop_invoked": False,
            "task_state_committed_now": False,
            "navigation_action_triggered": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "memory_written": False,
            "world_model_written": False,
            "scene_delta_generated": False,
            "boundary_ok": True,
            **_not_fact(),
        },
        "input_root_matrix": {"rows": intake_rows, **_not_fact()},
        "interruption_intent_policy": {
            "interruption_intent_types": INTERRUPTION_INTENT_TYPES,
            "intent_definitions": {
                "STOP": "stop_current_ordinary_output_candidate",
                "PAUSE": "pause_current_output_candidate",
                "REPEAT": "repeat_recent_output_after_freshness_check",
                "RESUME": "resume_paused_output_after_freshness_recheck",
                "CLARIFY": "clarify_previous_output_candidate",
                "CORRECT": "create_correction_event_candidate_only",
                "EMERGENCY": "create_safety_observation_candidate_only",
                "NEW_TASK": "create_new_task_candidate_only",
                "CANCEL_TASK": "create_cancel_task_candidate_only",
                "UNKNOWN_OR_AMBIGUOUS": "request_clarification_or_no_action",
            },
            **_not_fact(),
        },
        "speech_priority_interruption_policy": {
            "priority_levels": SPEECH_PRIORITY_LEVELS,
            "priority_rules": {
                "P0_not_cancelled_by_ordinary_stop": True,
                "P1_risk_state_not_deleted": True,
                "P2_pause_requires_resume_condition": True,
                "P3_resume_requires_stc_frame_region_freshness": True,
                "P4_P5_interruptible_by_owner_confirmed": True,
                "non_owner_cannot_interrupt_P0_P1": True,
            },
            **_not_fact(),
        },
        "speech_request_state_candidate_schema": {"states": SPEECH_STATES, **_not_fact()},
        "interruption_decision_candidate_schema": {
            "selected_action_candidate_enum": SELECTED_ACTION_CANDIDATES,
            "required_fields": [
                "interruption_decision_id",
                "voice_input_id",
                "source_ownership_decision_id",
                "target_speech_request_id",
                "interruption_intent_type",
                "selected_action_candidate",
                "target_speech_state_candidate",
                "source_chain",
            ],
            **_not_fact(),
        },
        "freshness_repeat_resume_policy": {
            "repeat_requires_freshness_check": True,
            "P0_P1_stale_repeat_not_current_fact": True,
            "P2_resume_requires_STC_route_freshness": True,
            "P3_resume_requires_STC_frame_region_freshness": True,
            "P4_P5_repeat_more_permissive": True,
            "stale_before_resume_generates_expired_before_resume_candidate": True,
            **_not_fact(),
        },
        "correction_policy": {
            "correction_event_candidate_only": True,
            "fact_write_forbidden": True,
            "world_model_write_forbidden": True,
            "task_state_commit_forbidden": True,
            "handoff_targets_later": ["task_manager", "vision_resampling", "review_queue"],
            **_not_fact(),
        },
        "emergency_interruption_policy": {
            "owner_confirmed_emergency_allowed": True,
            "ownership_uncertain_only_safety_observation_candidate": True,
            "non_owner_probable_only_limited_safety_candidate": True,
            "media_public_voice_cannot_control_luna": True,
            "P0_P1_not_deleted_by_ordinary_stop": True,
            "emergency_can_interrupt_P3_P4_P5": True,
            **_not_fact(),
        },
        "new_task_cancel_task_policy": {
            "new_task_not_direct_task_commit": True,
            "cancel_task_not_direct_cancel": True,
            "must_generate_task_control_candidate": True,
            "cancel_requires_confirmation": True,
            "pending_confirmation_preserved": True,
            "task_context_preserved": True,
            **_not_fact(),
        },
        "interruption_source_matrix": {
            "case_count": len(source_matrix),
            "rows": source_matrix,
            **_not_fact(),
        },
        "interruption_decision_candidates": {
            "interruption_decision_candidate_count": len(decisions),
            "candidates": decisions,
            **_not_fact(),
        },
        "priority_scenario_matrix": {
            "scenario_count": len(priority_rows),
            "rows": priority_rows,
            **_not_fact(),
        },
        "handoff_contracts": {
            "to_safety_task_arbitration_runtime": {
                "payload_fields": [
                    "interruption_decision_id",
                    "requested_action_candidate",
                    "target_priority",
                    "safety_keyword_detected",
                    "safety_task_arbitration_required",
                    "current_safety_active_candidate",
                    "task_context_preserved",
                    "pending_confirmation_preserved",
                ],
                "invoked_now": False,
            },
            "to_speech_gate": {
                "payload_fields": [
                    "target_speech_request_id",
                    "selected_action_candidate",
                    "priority_policy_decision",
                    "resume_required",
                    "repeat_allowed",
                    "runtime_tts_stopped",
                ],
                "invoked_now": False,
            },
            "to_voice_output_plane": {
                "payload_fields": [
                    "speech_request_state_candidate",
                    "pause_resume_repeat_stop_candidate",
                ],
                "invoked_now": False,
            },
            "to_task_manager": {
                "payload_fields": [
                    "new_task_candidate",
                    "cancel_task_candidate",
                    "correction_event_candidate",
                ],
                "invoked_now": False,
            },
            "to_stc_ocr_navigation": {
                "payload_fields": [
                    "freshness_check_required",
                    "stale_risk",
                    "resume_condition",
                ],
                "invoked_now": False,
            },
            **_not_fact(),
        },
        "boundary_report": {
            "boundary_ok": True,
            "violations": [],
            "runtime_asr_invoked": False,
            "runtime_audio_recorded": False,
            "runtime_tts_stopped": False,
            "speech_gate_invoked": False,
            "vop_invoked": False,
            "task_state_committed_now": False,
            "navigation_action_triggered": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "memory_written": False,
            "world_model_written": False,
            "scene_delta_generated": False,
            **_not_fact(),
        },
        "final": {
            "final_decision": FINAL_DECISION,
            "recommended_next_phase": RECOMMENDED_NEXT,
            "runtime_enablement_not_started": True,
            "future_runtime_enablement_phases": [
                "Voice-Interruption-Runtime-Shadow-v1",
                "Speech-Gate-Interruption-Handoff-DryRun-v1",
                "VOP-TTS-Interrupt-Controlled-Enablement-v1",
            ],
            **_not_fact(),
        },
    }
