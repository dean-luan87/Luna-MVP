# -*- coding: utf-8 -*-
"""Phase-Voice-TTS-Model-Deprecation-Minimal-Patch-v1-001."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Voice-TTS-Model-Deprecation-Minimal-Patch-v1-001"
FINAL_DECISION_GO = f"{PHASE_ID}_PATCH_APPLIED_STATIC_VERIFY_ONLY"

NON_CLAIMS: Tuple[str, ...] = (
    "Default model patched ≠ TTS runtime validated",
    "cosyvoice-v3-flash configured ≠ audio quality benchmarked",
    "qwen-tts deprecated ≠ removed from historical registry",
    "ASR unaffected by current patch ≠ ASR lifecycle permanently safe",
    "No real DashScope TTS synthesis performed in this patch verify",
)

PATCH_SCOPE_FILES: Tuple[str, ...] = (
    "modules/qwen_tts.py",
    "capabilities/voice/providers/qwen_tts_provider.py",
    "capabilities/voice/runtime/tts_unified_entry.py",
    "capabilities/voice/tts_model_constants_v0.py",
    "capabilities/governance/model_profile_registry_planning_v1.py",
)

TTS_CANDIDATE_GOVERNANCE: Dict[str, Dict[str, Any]] = {
    "qianwen_tts_candidate": {
        "status": "deprecated_pending",
        "retirement_date": "2026-09-07",
        "preferred": False,
        "runtime_default_allowed": False,
        "dashscope_model_name": "qwen-tts",
    },
    "cosyvoice_v3_flash_candidate": {
        "status": "replacement_candidate",
        "preferred": True,
        "runtime_default_allowed": True,
        "dashscope_model_name": "cosyvoice-v3-flash",
    },
    "qwen_tts_flash_candidate": {
        "status": "transitional_candidate",
        "preferred": False,
        "runtime_default_allowed": False,
        "dashscope_model_name": "qwen-tts-flash",
    },
}

ASR_PATCH_NOTE = {
    "impact": "no_current_impact",
    "reason": "ASR candidates (SenseVoice/Whisper/Qwen-ASR style) not in Aliyun Paraformer retirement list",
    "action": "registered_only_no_code_change_in_this_patch",
}


def run_voice_tts_model_deprecation_minimal_patch_v1(*, output_root: Optional[str] = None) -> Dict[str, Any]:
    from capabilities.governance.model_profile_registry_planning_v1 import _tts_governance_overlay, _seed_candidate
    from capabilities.voice.tts_model_constants_v0 import (
        DEFAULT_TTS_MODEL,
        LEGACY_QWEN_TTS_MODEL,
        LEGACY_QWEN_TTS_RETIREMENT_DATE,
        TRANSITIONAL_QWEN_TTS_FLASH_MODEL,
        resolve_tts_model,
        runtime_fallback_model,
    )

    out_root = Path(output_root or "_tmp_eval_out/voice_tts_model_deprecation_minimal_patch")
    out_root.mkdir(parents=True, exist_ok=True)

    runtime_defaults = {
        "default_tts_model": DEFAULT_TTS_MODEL,
        "legacy_qwen_tts_model": LEGACY_QWEN_TTS_MODEL,
        "transitional_qwen_tts_flash_model": TRANSITIONAL_QWEN_TTS_FLASH_MODEL,
        "legacy_retirement_date": LEGACY_QWEN_TTS_RETIREMENT_DATE,
        "resolved_default": resolve_tts_model().__dict__,
        "legacy_explicit": resolve_tts_model(explicit=LEGACY_QWEN_TTS_MODEL).__dict__,
        "transitional_explicit": resolve_tts_model(explicit=TRANSITIONAL_QWEN_TTS_FLASH_MODEL).__dict__,
        "fallback_from_default": runtime_fallback_model(DEFAULT_TTS_MODEL),
        "fallback_from_legacy": runtime_fallback_model(LEGACY_QWEN_TTS_MODEL),
    }

    registry_preview = [
        _tts_governance_overlay(
            _seed_candidate(
                profile_id,
                TTS_CANDIDATE_GOVERNANCE[profile_id]["dashscope_model_name"].replace("-", "_"),
                "tts_voice_output",
                "stage_3",
                "direct_open_source_or_external_provider",
                TTS_CANDIDATE_GOVERNANCE[profile_id]["status"],
                layer="layer_6_runtime_later",
            )
        )
        for profile_id in ("qianwen_tts_candidate", "cosyvoice_v3_flash_candidate", "qwen_tts_flash_candidate")
    ]

    patch_policy = {
        "phase_id": PHASE_ID,
        "scope_files": list(PATCH_SCOPE_FILES),
        "runtime_constants": runtime_defaults,
        "tts_candidate_governance": TTS_CANDIDATE_GOVERNANCE,
        "asr_note": ASR_PATCH_NOTE,
        "non_claims": list(NON_CLAIMS),
        "verify_mode": "static_model_name_and_fallback_only",
    }

    summary = {
        "phase_id": PHASE_ID,
        "final_decision": FINAL_DECISION_GO,
        "default_tts_model": DEFAULT_TTS_MODEL,
        "legacy_model": LEGACY_QWEN_TTS_MODEL,
        "transitional_model": TRANSITIONAL_QWEN_TTS_FLASH_MODEL,
        "registry_candidates_updated": list(TTS_CANDIDATE_GOVERNANCE.keys()),
        "non_claims": list(NON_CLAIMS),
        "asr_impact": ASR_PATCH_NOTE["impact"],
    }

    _write_json(out_root / "summary.json", summary)
    _write_json(out_root / "voice_tts_model_deprecation_minimal_patch_policy_v1.json", patch_policy)
    _write_json(out_root / "tts_candidate_governance_registry_preview_v1.json", {"candidates": registry_preview})
    _write_json(out_root / "asr_no_current_impact_note_v1.json", ASR_PATCH_NOTE)
    _write_json(out_root / "non_claims_v1.json", {"non_claims": list(NON_CLAIMS)})

    return {"output_root": str(out_root), "summary": summary, "patch_policy": patch_policy}


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
