from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.speech_manager.module.speech_manager_module_types_v1 import (
    MODULE_SCHEMA_VERSION,
    not_fact,
)


def adapt_speech_manager_input_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    candidate = dict(payload)
    speech_text = str(
        candidate.get("speech_text")
        or candidate.get("text_candidate")
        or candidate.get("prompt_text")
        or candidate.get("message")
        or ""
    ).strip()
    request_id_value = candidate.get("request_id")
    if request_id_value is None:
        request_id_value = candidate.get("speech_request_id")
    if request_id_value is None:
        request_id_value = "speech_mgr_req_unknown"
    request_id = str(request_id_value)

    source_module_value = candidate.get("source_module")
    if source_module_value is None:
        source_module_value = candidate.get("capability")
    if source_module_value is None:
        source_module_value = "luna.speech_manager"
    source_module = str(source_module_value)

    source_ref_value = candidate.get("source_ref")
    if source_ref_value is None:
        source_ref_value = candidate.get("input_ref")
    if source_ref_value is None:
        source_ref_value = request_id
    source_ref = str(source_ref_value)
    priority_label = str(
        candidate.get("priority_level") or candidate.get("priority") or "P4"
    )
    interruption_intent = str(
        candidate.get("interruption_intent_type")
        or candidate.get("interruption_intent")
        or "UNKNOWN_OR_AMBIGUOUS"
    )

    return {
        "schema_version": MODULE_SCHEMA_VERSION,
        "request_id": request_id,
        "source_module": source_module,
        "source_ref": source_ref,
        "speech_text": speech_text,
        "priority_level": priority_label,
        "priority_numeric_hint": candidate.get("priority_numeric_hint"),
        "audio_input_kind": str(
            candidate.get("audio_input_kind")
            or candidate.get("input_kind")
            or "text_candidate"
        ),
        "speaker_type": str(
            candidate.get("speaker_type")
            or candidate.get("speaker_role")
            or "registered_user"
        ),
        "speaker_identity_candidate": candidate.get("speaker_identity_candidate"),
        "speech_gate_required": bool(candidate.get("speech_gate_required", True)),
        "speech_gate_reason_hint": candidate.get("speech_gate_reason_hint"),
        "asr_requested": bool(
            candidate.get(
                "asr_requested", candidate.get("asr_candidate_requested", True)
            )
        ),
        "tts_requested": bool(
            candidate.get(
                "tts_requested", candidate.get("tts_candidate_requested", True)
            )
        ),
        "vop_requested": bool(
            candidate.get(
                "vop_requested", candidate.get("voice_output_plane_requested", True)
            )
        ),
        "interruption_intent_type": interruption_intent,
        "resume_requested": bool(
            candidate.get("resume_requested", interruption_intent == "RESUME")
        ),
        "repeat_requested": bool(
            candidate.get("repeat_requested", interruption_intent == "REPEAT")
        ),
        "cancel_requested": bool(
            candidate.get("cancel_requested", interruption_intent == "CANCEL_TASK")
        ),
        "content_policy_ref": str(
            candidate.get("content_policy_ref") or "speech_content_governance_v1"
        ),
        "trace_hint": str(candidate.get("trace_hint") or request_id),
        "replay_hint": str(candidate.get("replay_hint") or source_ref),
        "context": candidate.get("context") or {},
        "candidate_only": True,
        "requested_real_runtime": bool(candidate.get("requested_real_runtime", False)),
        "requested_real_tts": bool(candidate.get("requested_real_tts", False)),
        "requested_real_vop": bool(candidate.get("requested_real_vop", False)),
        **not_fact(),
    }
