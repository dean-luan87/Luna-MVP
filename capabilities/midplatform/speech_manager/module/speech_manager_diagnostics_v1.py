from __future__ import annotations

from typing import Any, Dict, Mapping


def build_speech_manager_diagnostics_v1(
    input_candidate: Mapping[str, Any],
    governance: Mapping[str, Any],
    content_candidate: Mapping[str, Any],
    interruption_plan: Mapping[str, Any],
    provider_candidates: Mapping[str, Any],
    trace_replay: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": "speech_manager_diagnostics_v1",
        "admitted": bool(governance.get("admitted")),
        "candidate_only": True,
        "no_real_asr": True,
        "no_real_tts": True,
        "no_real_speech_gate": True,
        "no_real_vop": True,
        "speaker_identity_auto_confirmed": bool(
            content_candidate.get("speaker_identity_auto_confirmed")
        ),
        "asr_candidate_auto_fact": bool(
            provider_candidates.get("asr_candidate", {}).get("asr_candidate_auto_fact")
        ),
        "trace_present": bool(trace_replay.get("trace_present")),
        "replay_present": bool(trace_replay.get("replay_present")),
        "boundary_preserved": True,
        "rejection_reason_count": len(governance.get("rejection_reasons") or []),
        "selected_action_candidate": interruption_plan.get("selected_action_candidate"),
        "priority_level": input_candidate.get("priority_level"),
        "fact_status": "not_fact",
        "write_allowed": False,
    }
