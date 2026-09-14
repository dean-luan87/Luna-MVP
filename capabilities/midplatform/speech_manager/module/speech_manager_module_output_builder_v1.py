from __future__ import annotations

from typing import Any, Dict, Mapping


def build_speech_manager_module_status_v1(
    governance: Mapping[str, Any],
    provider_candidates: Mapping[str, Any],
    trace_replay: Mapping[str, Any],
) -> str:
    if not governance.get("admitted"):
        return "speech_manager_module_integration_remediation_required"
    if not trace_replay.get("trace_present") or not trace_replay.get("replay_present"):
        return "speech_manager_module_integration_remediation_required"
    if not provider_candidates.get("speech_gate_candidate", {}).get(
        "candidate_only", False
    ):
        return "speech_manager_module_integration_remediation_required"
    return "speech_manager_functional_module_ready"


def build_speech_manager_result_summary_v1(
    *,
    request_id: str,
    module_status: str,
    content_candidate: Mapping[str, Any],
    interruption_plan: Mapping[str, Any],
    provider_candidates: Mapping[str, Any],
    trace_replay: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": "speech_manager_result_summary_v1",
        "request_id": request_id,
        "module_status": module_status,
        "speech_text": content_candidate.get("normalized_text"),
        "selected_action_candidate": interruption_plan.get("selected_action_candidate"),
        "trace_ref": trace_replay.get("trace_ref"),
        "replay_key": trace_replay.get("replay_key"),
        "speaker_identity_auto_confirmed": False,
        "asr_candidate_auto_fact": False,
        "real_asr_invoked": False,
        "real_tts_invoked": False,
        "real_speech_gate_invoked": False,
        "real_vop_invoked": False,
        "candidate_only": True,
        "boundary_preserved": True,
    }
