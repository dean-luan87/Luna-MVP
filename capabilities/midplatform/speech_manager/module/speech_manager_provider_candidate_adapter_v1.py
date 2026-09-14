from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.speech_manager.module.speech_manager_module_types_v1 import (
    not_fact,
)


def build_speech_manager_provider_candidates_v1(
    input_candidate: Mapping[str, Any],
    content_candidate: Mapping[str, Any],
    interruption_plan: Mapping[str, Any],
) -> Dict[str, Any]:
    request_id = str(input_candidate.get("request_id") or "speech_mgr_req_unknown")
    normalized_text = str(content_candidate.get("normalized_text") or "")
    priority_level = str(input_candidate.get("priority_level") or "P4")

    asr_candidate = {
        "schema_version": "speech_manager_asr_candidate_v1",
        "asr_candidate_id": f"asr_{request_id}",
        "asr_requested": bool(input_candidate.get("asr_requested", True)),
        "asr_candidate_auto_fact": False,
        "asr_candidate_only": True,
        "recognized_text": None,
        "source_audio_kind": str(
            input_candidate.get("audio_input_kind") or "text_candidate"
        ),
        **not_fact(),
    }

    tts_candidate = {
        "schema_version": "speech_manager_tts_candidate_v1",
        "tts_candidate_id": f"tts_{request_id}",
        "tts_requested": bool(input_candidate.get("tts_requested", True)),
        "tts_text_candidate": normalized_text,
        "tts_provider_candidate": str(
            input_candidate.get("tts_provider_candidate")
            or "default_tts_provider_candidate"
        ),
        "real_tts_invoked": False,
        "candidate_only": True,
        **not_fact(),
    }

    speech_gate_candidate = {
        "schema_version": "speech_manager_speech_gate_candidate_v1",
        "speech_gate_candidate_id": f"gate_{request_id}",
        "gate_allowed": bool(content_candidate.get("speakable", True))
        and bool(input_candidate.get("speech_gate_required", True)),
        "gate_reason": content_candidate.get("guard_reason")
        or "candidate_text_allowed",
        "cooldown_key": str(input_candidate.get("trace_hint") or request_id),
        "interruptible": True,
        "priority_level": priority_level,
        "candidate_only": True,
        "real_speech_gate_invoked": False,
        **not_fact(),
    }

    vop_candidate = {
        "schema_version": "speech_manager_vop_candidate_v1",
        "vop_candidate_id": f"vop_{request_id}",
        "submitted_now": False,
        "voice_output_plane_required": bool(input_candidate.get("vop_requested", True)),
        "speech_gate_candidate_ref": speech_gate_candidate["speech_gate_candidate_id"],
        "tts_candidate_ref": tts_candidate["tts_candidate_id"],
        "candidate_only": True,
        "real_vop_invoked": False,
        **not_fact(),
    }

    return {
        "schema_version": "speech_manager_provider_candidate_bundle_v1",
        "asr_candidate": asr_candidate,
        "tts_candidate": tts_candidate,
        "speech_gate_candidate": speech_gate_candidate,
        "vop_candidate": vop_candidate,
        "candidate_only": True,
        **not_fact(),
    }
