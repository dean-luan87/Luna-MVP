from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence

from capabilities.midplatform.speech_manager.module.speech_manager_module_types_v1 import (
    SPEECH_PRIORITY_ORDER,
    not_fact,
)


def run_speech_manager_request_governance_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    rejection_reasons: list[str] = []
    request_id = str(input_candidate.get("request_id") or "")
    speech_text = str(input_candidate.get("speech_text") or "").strip()
    priority_label = str(input_candidate.get("priority_level") or "P4")

    if not request_id:
        rejection_reasons.append("missing_request_id")
    if not speech_text:
        rejection_reasons.append("missing_speech_text")
    if priority_label not in SPEECH_PRIORITY_ORDER:
        rejection_reasons.append("invalid_priority_label")
    if bool(input_candidate.get("requested_real_runtime")):
        rejection_reasons.append("real_runtime_forbidden_in_module_validation")
    if bool(input_candidate.get("requested_real_tts")):
        rejection_reasons.append("real_tts_forbidden_in_module_validation")
    if bool(input_candidate.get("requested_real_vop")):
        rejection_reasons.append("real_vop_forbidden_in_module_validation")

    return {
        "schema_version": "speech_manager_request_governance_v1",
        "request_id": request_id,
        "admitted": len(rejection_reasons) == 0,
        "rejection_reasons": rejection_reasons,
        "candidate_only": True,
        "input_valid": len(rejection_reasons) == 0,
        "explicit_authority_boundary_preserved": True,
        "no_real_asr": True,
        "no_real_tts": True,
        "no_real_speech_gate": True,
        "no_real_vop": True,
        "speech_gate_required": bool(input_candidate.get("speech_gate_required", True)),
        "fact_status": "not_fact",
        "write_allowed": False,
    }
