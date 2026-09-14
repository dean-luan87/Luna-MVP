# -*- coding: utf-8 -*-
"""Voice Command Ownership Gate Policy v1 — policy only; no ASR/voiceprint/runtime.

Phase-Voice-Command-Ownership-Gate-Policy-v1-001
Future relocation note: evaluation runners live under tools/evaluation/voice/.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

PHASE_ID = "Voice-Command-Ownership-Gate-Policy-v1-001"
FINAL_DECISION = "VOICE_COMMAND_OWNERSHIP_GATE_POLICY_READY_FOR_INTERRUPTION_GOVERNANCE"
RECOMMENDED_NEXT = "Voice-Interruption-Governance-DryRun-v1"

FOLLOWUPS = [
    "Voice-Interruption-Governance-DryRun-v1",
    "Basic-Navigation-Guidance-Loop-Stabilization-Test-v1",
    "Safety-Task-Arbitration-Runtime-DryRun-v1",
    "Voiceprint-Enrollment-Governance-v1",
    "Emotional-Context-Candidate-Contract-v1",
]

OWNERSHIP_STATES = [
    "OWNER_CONFIRMED",
    "OWNER_PROBABLE",
    "OWNER_UNCERTAIN",
    "NON_OWNER_PROBABLE",
    "NON_OWNER_CONFIRMED",
]

SPEAKER_TYPES = [
    "registered_user",
    "authorized_helper",
    "household_member_candidate",
    "unknown_person",
    "background_voice",
    "media_playback_voice",
    "phone_call_remote_voice",
    "system_generated_voice",
    "synthetic_or_replayed_voice_candidate",
]

ADDRESSING_STATUSES = [
    "directly_addressed_to_luna",
    "wake_context_active",
    "implicit_followup_to_luna",
    "ambiguous_addressing",
    "addressed_to_other_human",
    "not_addressed_to_luna",
]

CONVERSATION_CONTEXTS = [
    "direct_command_to_luna",
    "phone_call_speech",
    "human_conversation",
    "background_speech",
    "media_playback_voice",
    "public_announcement",
    "unknown_speech_context",
]

ENTRYPOINTS = [
    "interruption_classifier",
    "safety_observation_candidate",
    "clarification_candidate",
    "task_control_candidate",
    "repeat_request_candidate",
    "correction_candidate",
    "human_assistance_candidate",
    "task_commit",
    "memory_write",
    "world_model_write",
    "navigation_action",
    "speech_gate_runtime",
    "vop_runtime",
    "tts_stop_runtime",
]

SAFETY_KEYWORDS = ["停", "危险", "小心", "车来了", "有人", "别动", "等一下"]

RUNTIME_BLOCKED: Set[str] = {
    "task_commit",
    "memory_write",
    "world_model_write",
    "navigation_action",
    "speech_gate_runtime",
    "vop_runtime",
    "tts_stop_runtime",
}

INTAKE_SPECS = [
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
    "voice_dialogue_contract": "**/LUNA_VOICE_DIALOGUE*.md",
}

# 16 dry-run cases: (case_id, utterance_zh, speaker_type, addressing, context, ownership, safety_kw)
CASES: List[Tuple[str, str, str, str, str, str, bool]] = [
    ("case_01", "停一下", "registered_user", "directly_addressed_to_luna", "direct_command_to_luna", "OWNER_CONFIRMED", False),
    ("case_02", "重新说一遍", "registered_user", "directly_addressed_to_luna", "direct_command_to_luna", "OWNER_CONFIRMED", False),
    ("case_03", "刚才你说什么", "registered_user", "implicit_followup_to_luna", "direct_command_to_luna", "OWNER_CONFIRMED", False),
    ("case_04", "不对，你看错了", "registered_user", "directly_addressed_to_luna", "direct_command_to_luna", "OWNER_CONFIRMED", False),
    ("case_05", "危险，车来了", "registered_user", "directly_addressed_to_luna", "direct_command_to_luna", "OWNER_CONFIRMED", True),
    ("case_06", "往左走", "unknown_person", "not_addressed_to_luna", "human_conversation", "NON_OWNER_PROBABLE", False),
    ("case_07", "停一下", "unknown_person", "not_addressed_to_luna", "human_conversation", "NON_OWNER_PROBABLE", True),
    ("case_08", "Luna，帮他停一下", "authorized_helper", "directly_addressed_to_luna", "direct_command_to_luna", "OWNER_PROBABLE", True),
    ("case_09", "别说了", "registered_user", "not_addressed_to_luna", "phone_call_speech", "OWNER_UNCERTAIN", False),
    ("case_10", "等一下", "registered_user", "not_addressed_to_luna", "human_conversation", "OWNER_UNCERTAIN", False),
    ("case_11", "停", "media_playback_voice", "not_addressed_to_luna", "media_playback_voice", "NON_OWNER_CONFIRMED", True),
    ("case_12", "请往左走", "background_voice", "not_addressed_to_luna", "public_announcement", "NON_OWNER_CONFIRMED", False),
    ("case_13", "危险", "unknown_person", "ambiguous_addressing", "background_speech", "NON_OWNER_PROBABLE", True),
    ("case_14", "车来了", "registered_user", "ambiguous_addressing", "unknown_speech_context", "OWNER_UNCERTAIN", True),
    ("case_15", "暂停导航，先读这个", "registered_user", "directly_addressed_to_luna", "direct_command_to_luna", "OWNER_CONFIRMED", False),
    ("case_16", "继续刚才的导航", "registered_user", "implicit_followup_to_luna", "direct_command_to_luna", "OWNER_CONFIRMED", False),
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _has_safety_keyword(text: str) -> bool:
    return any(kw in text for kw in SAFETY_KEYWORDS)


def _resolve_allowed_blocked(
    ownership: str,
    speaker: str,
    addressing: str,
    context: str,
    safety_kw: bool,
) -> Tuple[List[str], List[str], bool, bool]:
    blocked = list(RUNTIME_BLOCKED)
    allowed: List[str] = []
    requires_confirmation = False
    safety_only = False

    if context in ("media_playback_voice", "public_announcement"):
        if safety_kw:
            return ["safety_observation_candidate"], blocked, True, True
        return [], blocked, False, False

    if ownership == "NON_OWNER_CONFIRMED":
        if safety_kw:
            allowed = ["safety_observation_candidate"]
            safety_only = True
        return allowed, blocked, True, safety_only

    if context in ("phone_call_speech", "human_conversation") and addressing not in (
        "directly_addressed_to_luna",
        "wake_context_active",
        "implicit_followup_to_luna",
    ):
        if safety_kw:
            allowed = ["safety_observation_candidate"]
            safety_only = True
        return allowed, blocked, True, safety_only

    if ownership == "OWNER_CONFIRMED":
        allowed = [
            "interruption_classifier",
            "safety_observation_candidate",
            "clarification_candidate",
            "task_control_candidate",
            "repeat_request_candidate",
            "correction_candidate",
            "human_assistance_candidate",
        ]
        return allowed, blocked, False, safety_kw and False

    if ownership == "OWNER_PROBABLE":
        allowed = [
            "interruption_classifier",
            "safety_observation_candidate",
            "clarification_candidate",
            "repeat_request_candidate",
        ]
        if speaker == "authorized_helper":
            requires_confirmation = True
        else:
            allowed.append("task_control_candidate")
            requires_confirmation = True
        return allowed, blocked, True, safety_kw

    if ownership == "OWNER_UNCERTAIN":
        if safety_kw:
            allowed = ["safety_observation_candidate", "clarification_candidate"]
            safety_only = True
        else:
            allowed = ["clarification_candidate"]
            requires_confirmation = True
        return allowed, blocked, True, safety_only

    if ownership == "NON_OWNER_PROBABLE":
        if safety_kw:
            allowed = ["safety_observation_candidate"]
            safety_only = True
        return allowed, blocked, True, safety_only

    return allowed, blocked, True, safety_only


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
                "intake_status": "loaded" if found else "optional_missing",
                "missing_impact": "optional_doc_reference_only",
                **_not_fact(),
            }
        )
    return rows


def run_voice_command_ownership_gate_policy_v1(
    *,
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
    for iid, art, optional in INTAKE_SPECS:
        root = roots[iid]
        loaded = root.is_dir()
        if art:
            loaded = loaded and (root / art).is_file()
        intake_rows.append(
            {
                "intake_id": iid,
                "input_source": iid,
                "source_root_or_path": str(root),
                "artifact": art or "(directory)",
                "loaded": loaded,
                "optional": optional,
                "intake_status": "loaded" if loaded else ("optional_missing" if optional else "missing"),
                "missing_impact": "none" if loaded else ("optional_reference_only" if optional else "check_partial"),
                **_not_fact(),
            }
        )
    intake_rows.extend(_find_optional_docs(ws))

    voice_inputs: List[Dict[str, Any]] = []
    decisions: List[Dict[str, Any]] = []

    for case_id, utterance, speaker, addressing, context, ownership, safety_kw in CASES:
        sk = safety_kw or _has_safety_keyword(utterance)
        vid = f"voice_input_{case_id}"
        allowed, blocked, req_conf, safety_only = _resolve_allowed_blocked(
            ownership, speaker, addressing, context, sk
        )
        voice_inputs.append(
            {
                "voice_input_candidate_id": vid,
                "case_id": case_id,
                "utterance_text_candidate_zh": utterance,
                "speaker_type": speaker,
                "addressing_status": addressing,
                "conversation_context": context,
                "simulated_only": True,
                "runtime_asr_invoked": False,
                "runtime_audio_recorded": False,
                **_not_fact(),
            }
        )
        handoff = "Voice-Interruption-Governance-DryRun-v1"
        if safety_only:
            handoff = "Safety-Task-Arbitration-Policy"
        decisions.append(
            {
                "ownership_gate_decision_candidate_id": f"ogd_{case_id}",
                "voice_input_candidate_id": vid,
                "ownership_state": ownership,
                "speaker_type": speaker,
                "addressing_status": addressing,
                "conversation_context": context,
                "allowed_entrypoints": allowed,
                "blocked_entrypoints": blocked,
                "requires_confirmation": req_conf,
                "safety_only_allowed": safety_only,
                "safety_keyword_detected": sk,
                "handoff_target": handoff,
                "runtime_action_committed": False,
                "source_chain": "voice_command_ownership_gate_policy_v1",
                **_not_fact(),
            }
        )

    speaker_matrix_rows = []
    for st in SPEAKER_TYPES:
        for ctx in ("direct_command_to_luna", "phone_call_speech", "human_conversation"):
            own = "OWNER_CONFIRMED" if st == "registered_user" and ctx == "direct_command_to_luna" else "OWNER_UNCERTAIN"
            if st in ("unknown_person", "background_voice", "media_playback_voice", "phone_call_remote_voice"):
                own = "NON_OWNER_PROBABLE"
            if st == "synthetic_or_replayed_voice_candidate":
                own = "NON_OWNER_CONFIRMED"
            a, b, _, _ = _resolve_allowed_blocked(own, st, "directly_addressed_to_luna", ctx, False)
            speaker_matrix_rows.append(
                {
                    "speaker_type": st,
                    "conversation_context": ctx,
                    "default_ownership_state": own,
                    "interruption_classifier_allowed": "interruption_classifier" in a,
                    "task_control_allowed": "task_control_candidate" in a,
                    "task_commit_allowed": False,
                    **_not_fact(),
                }
            )

    addressing_rows = []
    for addr in ADDRESSING_STATUSES:
        addressing_rows.append(
            {
                "addressing_status": addr,
                "direct_command_likely": addr in (
                    "directly_addressed_to_luna",
                    "wake_context_active",
                    "implicit_followup_to_luna",
                ),
                "interruption_precheck_pass": addr
                in ("directly_addressed_to_luna", "wake_context_active", "implicit_followup_to_luna"),
                "requires_wake_or_name": addr == "ambiguous_addressing",
                **_not_fact(),
            }
        )

    context_rows = []
    for ctx in CONVERSATION_CONTEXTS:
        block_interruption = ctx in (
            "phone_call_speech",
            "human_conversation",
            "media_playback_voice",
            "public_announcement",
            "background_speech",
        )
        context_rows.append(
            {
                "conversation_context": ctx,
                "default_block_interruption": block_interruption,
                "default_block_task_control": block_interruption or ctx == "unknown_speech_context",
                "default_block_task_commit": True,
                "safety_keyword_exception_allowed": True,
                **_not_fact(),
            }
        )

    entrypoint_rows = []
    for own in OWNERSHIP_STATES:
        for ep in ENTRYPOINTS:
            if ep in RUNTIME_BLOCKED:
                allow = False
            elif own == "OWNER_CONFIRMED":
                allow = ep not in RUNTIME_BLOCKED
            elif own in ("OWNER_PROBABLE", "OWNER_UNCERTAIN"):
                allow = ep in (
                    "interruption_classifier",
                    "safety_observation_candidate",
                    "clarification_candidate",
                    "repeat_request_candidate",
                )
            else:
                allow = ep == "safety_observation_candidate" and own == "NON_OWNER_PROBABLE"
            entrypoint_rows.append(
                {
                    "ownership_state": own,
                    "entrypoint": ep,
                    "allowed_as_candidate": allow,
                    "runtime_invoked_in_policy_phase": False,
                    **_not_fact(),
                }
            )

    safety_kw_rows = []
    for own in ("OWNER_UNCERTAIN", "NON_OWNER_PROBABLE"):
        safety_kw_rows.append(
            {
                "ownership_state": own,
                "safety_keyword_present": True,
                "allowed_entrypoint": "safety_observation_candidate",
                "blocked_entrypoints": list(RUNTIME_BLOCKED) + ["task_control_candidate", "interruption_classifier"]
                if own == "NON_OWNER_PROBABLE"
                else ["task_commit", "navigation_action", "task_control_candidate"],
                "must_route_to_safety_arbitration": True,
                "tts_stop_allowed": False,
                **_not_fact(),
            }
        )

    return {
        "summary": {
            "schema_version": "voice_command_ownership_gate_policy_v1_summary_v0",
            "phase": PHASE_ID,
            "policy_scope": "voice_command_ownership_gate_policy_only",
            "capability_layer": "capabilities/voice",
            "future_relocation_note": "evaluation runners under tools/evaluation/voice/",
            "based_on_safety_task_arbitration": roots["safety_task_arbitration"].is_dir(),
            "based_on_basic_navigation_loop": roots["basic_navigation_loop"].is_dir(),
            "ownership_states_defined": len(OWNERSHIP_STATES),
            "speaker_types_defined": len(SPEAKER_TYPES),
            "simulated_case_count": len(CASES),
            "voiceprint_schema_defined": True,
            "voice_emotion_schema_defined": True,
            "handoff_contracts_defined": True,
            "runtime_asr_invoked": False,
            "runtime_voiceprint_invoked": False,
            "runtime_diarization_invoked": False,
            "runtime_audio_recorded": False,
            "runtime_tts_stopped": False,
            "speech_gate_invoked": False,
            "vop_invoked": False,
            "task_state_committed_now": False,
            "navigation_action_triggered": False,
            "memory_written_now": False,
            "world_model_written": False,
            "scene_delta_generated": False,
            "runtime_routing_changed": False,
            **_not_fact(),
        },
        "policy_matrix": {
            "schema_version": "voice_command_ownership_gate_policy_matrix_v1",
            "ownership_states": OWNERSHIP_STATES,
            "speaker_types": SPEAKER_TYPES,
            "addressing_statuses": ADDRESSING_STATUSES,
            "conversation_contexts": CONVERSATION_CONTEXTS,
            "world_model_voiceprint_note": "voiceprint_is_high_privacy_world_model_evidence_candidate_requires_consent_enrollment_ttl_audit",
            "world_model_emotion_note": "voice_emotion_is_emotional_context_candidate_not_emotion_fact",
            "open_source_tool_reference_priority": ["SpeechBrain", "pyannote.audio", "3D-Speaker", "Resemblyzer"],
            **_not_fact(),
        },
        "intake": {
            "schema_version": "voice_command_ownership_gate_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "simulated_cases": {
            "schema_version": "voice_command_ownership_simulated_voice_input_cases_v1",
            "case_count": len(voice_inputs),
            "cases": voice_inputs,
            **_not_fact(),
        },
        "decisions": {
            "schema_version": "voice_command_ownership_gate_decision_candidates_v1",
            "decision_candidate_count": len(decisions),
            "candidates": decisions,
            **_not_fact(),
        },
        "speaker_matrix": {
            "schema_version": "voice_command_ownership_speaker_ownership_matrix_v1",
            "rows": speaker_matrix_rows,
            **_not_fact(),
        },
        "addressing_matrix": {
            "schema_version": "voice_command_ownership_addressing_matrix_v1",
            "rows": addressing_rows,
            **_not_fact(),
        },
        "context_matrix": {
            "schema_version": "voice_command_ownership_conversation_context_matrix_v1",
            "rows": context_rows,
            **_not_fact(),
        },
        "entrypoint_matrix": {
            "schema_version": "voice_command_ownership_entrypoint_decision_matrix_v1",
            "rows": entrypoint_rows,
            **_not_fact(),
        },
        "safety_keyword_matrix": {
            "schema_version": "voice_command_ownership_safety_keyword_exception_matrix_v1",
            "safety_keywords": SAFETY_KEYWORDS,
            "rows": safety_kw_rows,
            **_not_fact(),
        },
        "voiceprint_schema": {
            "schema_version": "voice_command_ownership_voiceprint_evidence_candidate_schema_v1",
            "voiceprint_model_invoked": False,
            "speaker_identity_fact": False,
            "speaker_identity_write_allowed": False,
            "field_definitions": {
                "voiceprint_candidate_id": {"required": True},
                "voice_input_id": {"required": True},
                "speaker_embedding_ref": {"type": "nullable_placeholder"},
                "match_status": {"type": "enum"},
                "match_confidence": {"type": "float_placeholder"},
                "speaker_identity_claim": {"type": "candidate_only"},
                "consent_status": {"required": True},
                "privacy_level": {"required": True},
                "retention_policy": {"required": True},
                "runtime_model_invoked": {"default": False},
            },
            "lifecycle_stages": [
                "VOICE_SEGMENT_CANDIDATE",
                "EMBEDDING_CANDIDATE",
                "MATCH_CANDIDATE",
                "OWNERSHIP_GATE_INPUT",
                "IDENTITY_ANCHOR_CANDIDATE_LATER",
            ],
            **_not_fact(),
        },
        "voiceprint_matrix": {
            "schema_version": "voice_command_ownership_voiceprint_candidate_matrix_v1",
            "candidate_only": True,
            "runtime_model_invoked": False,
            "no_enrollment_in_policy_phase": True,
            "no_raw_audio_retention": True,
            **_not_fact(),
        },
        "emotion_schema": {
            "schema_version": "voice_command_ownership_voice_emotion_evidence_candidate_schema_v1",
            "emotion_fact": False,
            "emotional_context_write_allowed": False,
            "runtime_model_invoked": False,
            "field_definitions": {
                "voice_emotion_candidate_id": {"required": True},
                "voice_input_id": {"required": True},
                "emotion_candidate": {"type": "enum_placeholder"},
                "stress_candidate": {"type": "boolean_placeholder"},
                "urgency_candidate": {"type": "boolean_placeholder"},
                "fatigue_candidate": {"type": "boolean_placeholder"},
                "affective_tone_candidate": {"type": "string_placeholder"},
                "text_emotion_link_ref": {"type": "nullable"},
                "runtime_model_invoked": {"default": False},
            },
            **_not_fact(),
        },
        "emotion_matrix": {
            "schema_version": "voice_command_ownership_voice_emotion_candidate_matrix_v1",
            "candidate_only": True,
            "must_not_replace_text_semantics": True,
            "must_not_write_long_term_profile_without_consent": True,
            **_not_fact(),
        },
        "handoffs": {
            "schema_version": "voice_command_ownership_handoff_contracts_v1",
            "to_voice_interruption_governance": {
                "target": "Voice-Interruption-Governance-DryRun-v1",
                "payload_fields": [
                    "voice_input_id",
                    "ownership_state",
                    "speaker_type",
                    "addressing_status",
                    "conversation_context",
                    "allowed_entrypoints",
                    "requires_confirmation",
                    "safety_only_allowed",
                    "interruption_allowed_precheck",
                ],
            },
            "to_safety_task_arbitration": {
                "target": "Safety-Task-Arbitration-Policy",
                "payload_fields": [
                    "ownership_state",
                    "safety_only_allowed",
                    "safety_keyword_detected",
                    "non_owner_risk",
                    "phone_call_or_human_conversation_risk",
                    "task_control_allowed_candidate",
                ],
            },
            "to_speech_gate": {
                "target": "Speech-Gate",
                "invoked_now": False,
                "future_payload_defined": True,
            },
            "to_world_model_emotional_context": {
                "target": "WorldModel-Emotional-Context",
                "invoked_now": False,
                "candidate_schemas_only": True,
            },
            "feedback_invoked_now": False,
            **_not_fact(),
        },
        "trace": {
            "schema_version": "voice_command_ownership_gate_decision_trace_v1",
            "steps": [
                {"step_id": s, "step_name": s, "runtime_action_committed": False}
                for s in [
                    "load_safety_task_arbitration",
                    "load_basic_navigation_loop",
                    "define_ownership_gate_schema",
                    "define_priority_matrices",
                    "define_voiceprint_emotion_schemas",
                    "generate_simulated_cases",
                    "define_handoff_contracts",
                    "generate_final_policy_decision",
                ]
            ],
            **_not_fact(),
        },
        "final": {
            "schema_version": "voice_command_ownership_gate_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "simulated_case_count": len(CASES),
            "decision_candidate_count": len(decisions),
            "recommended_next_phase": RECOMMENDED_NEXT,
            "mainline_order": [
                "Safety-Task-Arbitration-Policy-v1",
                "Voice-Command-Ownership-Gate-Policy-v1",
                "Voice-Interruption-Governance-DryRun-v1",
                "Basic-Navigation-Guidance-Loop-Stabilization-Test-v1",
            ],
            "runtime_action_committed": False,
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "voice_command_ownership_gate_boundary_report_v1",
            "policy_only": True,
            "boundary_ok": True,
            "violations": [],
            "runtime_asr_invoked": False,
            "runtime_voiceprint_invoked": False,
            "runtime_diarization_invoked": False,
            "runtime_audio_recorded": False,
            "runtime_tts_stopped": False,
            "speech_gate_invoked": False,
            "vop_invoked": False,
            "task_state_committed_now": False,
            "navigation_action_triggered": False,
            "memory_written_now": False,
            "world_model_written": False,
            "scene_delta_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
        },
        "metrics": {
            "schema_version": "voice_command_ownership_gate_metrics_candidate_report_v1",
            "simulated_case_count": len(CASES),
            "decision_candidate_count": len(decisions),
            "matrix_row_count": len(speaker_matrix_rows)
            + len(addressing_rows)
            + len(context_rows)
            + len(entrypoint_rows),
            "runtime_action_committed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "voice_command_ownership_gate_benchmark_link_report_v1",
            "benchmark_available": False,
            "benchmark_score_generated": False,
        },
        "health_report": {
            "schema_version": "voice_command_ownership_gate_system_health_report_v1",
            "system_health_governance_available": roots["system_health"].is_dir(),
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "voice_command_ownership_gate_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "policy_only": True,
            "runtime_asr_invoked": False,
            "runtime_voiceprint_invoked": False,
            "memory_written_now": False,
            "world_model_written": False,
        },
        "sim_report": {
            "schema_version": "voice_command_ownership_gate_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_only": True,
            "run_model": False,
        },
        "non_claims": {
            "schema_version": "voice_command_ownership_gate_non_claims_report_v1",
            "claims": [
                "policy_not_runtime",
                "simulated_cases_not_real_audio",
                "ownership_decision_not_speaker_verification",
                "voiceprint_schema_not_model_output",
                "emotion_schema_not_emotion_fact",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "voice_command_ownership_gate_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "voice_command_ownership_gate_audit_report_v1",
            "voice_command_ownership_gate_policy_v1_executed": True,
            "policy_only": True,
            "runtime_asr_invoked": False,
            "runtime_voiceprint_invoked": False,
            "runtime_diarization_invoked": False,
            "runtime_audio_recorded": False,
            "speaker_identity_fact": False,
            "emotion_fact": False,
            "final_decision_recorded": FINAL_DECISION,
            **_not_fact(),
        },
    }
