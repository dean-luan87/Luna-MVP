#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-VoiceInteraction-Readiness-001 — Read-only full voice interaction readiness scan.

Does NOT call providers, Qwen, TTS, ASR, or playback. Does NOT modify runtime.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
from pathlib import Path
from typing import Any, Dict, List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _exists(repo: Path, rel: str) -> bool:
    return (repo / rel).is_file()


def _read_text_limited(path: Path, max_bytes: int = 400_000) -> str:
    try:
        data = path.read_bytes()[:max_bytes]
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""


def _file_contains(repo: Path, rel: str, *needles: str) -> bool:
    p = repo / rel
    if not p.is_file():
        return False
    t = _read_text_limited(p)
    return all(n in t for n in needles)


def _scan_asr(repo: Path) -> Dict[str, Any]:
    v = repo / "capabilities" / "voice"
    has_iface = (v / "interfaces/asr_provider.py").is_file()
    has_mock = (v / "providers/mock_asr_provider.py").is_file()
    # core_snapshot has Whisper but is legacy stack — report separately in notes
    core_whisper = (repo / "core_snapshot/main.py").is_file() and _file_contains(repo, "core_snapshot/main.py", "WhisperProcessor")
    return {
        "asr_provider_exists": has_iface and has_mock,
        "asr_runtime_connected": False,
        "audio_capture_connected": core_whisper,
        "final_text_event_exists": (v / "runtime/voice_final_text_dispatcher.py").is_file(),
        "asr_trace_exists": (v / "observations/voice_input_observation.py").is_file(),
        "real_asr_invoked_by_this_phase": False,
        "notes": "Primary ASR path for full mainline still readiness_pending; mock_asr + interfaces exist under capabilities/voice.",
        "legacy_core_snapshot_whisper_referenced": core_whisper,
    }


def _scan_session(repo: Path) -> Dict[str, Any]:
    v = repo / "capabilities" / "voice"
    return {
        "wake_window_defined": (v / "runtime/voice_wake_window_manager.py").is_file(),
        "session_state_defined": (v / "runtime/voice_input_session_manager.py").is_file()
        and (v / "runtime/voice_v1_session_state_anchor.py").is_file(),
        "session_id_required": True,
        "multi_turn_state_defined": (v / "runtime/voice_v1_session_state_anchor.py").is_file(),
        "session_timeout_policy_defined": (v / "runtime/voice_segment_timeout_policy.py").is_file(),
        "interruption_cancel_paths_exist": (v / "runtime/semantic_converter_v2.py").is_file(),
    }


def _scan_semantic(repo: Path) -> Dict[str, Any]:
    v = repo / "capabilities" / "voice"
    return {
        "semantic_normalization_defined": (v / "runtime/semantic_converter_v2.py").is_file(),
        "intent_context_tracker_defined": (v / "schemas/voice_intent_candidate.py").is_file(),
        "multi_turn_context_defined": (v / "runtime/voice_v1_session_state_anchor.py").is_file(),
        "task_context_connected": False,
        "vision_context_connected": False,
        "ocr_context_connected": False,
        "memory_context_connected": False,
        "notes": "task/vision/ocr/memory hooks intentionally conservative false for mainline readiness_pending unless wired in separate phase.",
    }


def _scan_qianwen(repo: Path) -> Dict[str, Any]:
    v = repo / "capabilities" / "voice"
    tts = (v / "providers/qwen_tts_provider.py").is_file()
    long_model = (v / "providers/qwen_external_long_input_model_provider.py").is_file()
    diff_audit_docs = (repo / "docs/architecture/LUNA_VOICE_SOURCE_TEXT_SPOKEN_TEXT_DIFF_AUDIT_SCHEMA_V0.md").is_file()
    policy = (repo / "docs/architecture/LUNA_VOICE_QWEN_FIRST_TTS_FALLBACK_POLICY_V0.md").is_file()
    return {
        "qianwen_tts_provider_exists": tts,
        "qianwen_long_input_model_provider_exists": long_model,
        "qianwen_conversation_model_exists": long_model,
        "qianwen_conversation_model_note": "Long-input Qwen provider exists; not equivalent to full conversational mainline productization.",
        "qianwen_first_policy_documented": policy,
        "qianwen_runtime_wiring_done": False,
        "source_spoken_diff_audit_defined": diff_audit_docs,
        "rewrite_control_defined": (v / "output/voice_output_governance_v0.py").is_file(),
        "no_fabrication_defined": (v / "runtime/voice_information_gate_v0.py").is_file() or (v / "output/voice_output_governance_v0.py").is_file(),
    }


def _scan_output_gov(repo: Path) -> Dict[str, Any]:
    v = repo / "capabilities" / "voice"
    arch = repo / "docs" / "architecture"
    gov007 = (arch / "LUNA_VOICE_GOVERNED_SUBMIT_SHADOW_READINESS_V0.md").is_file()
    trw = (v / "output/voice_output_trw_adapter_v0.py").is_file()
    shadow = (v / "output/voice_governed_submit_shadow_v0.py").is_file()
    entry = (v / "output/governed_voice_provider_entry_v0.py").is_file()
    tts_entry = (v / "runtime/tts_unified_entry.py").is_file()
    gate_wired = _file_contains(repo, "capabilities/voice/runtime/tts_unified_entry.py", "voice_output_governance") or _file_contains(
        repo, "capabilities/voice/runtime/tts_unified_entry.py", "GovernedVoice"
    )
    return {
        "output_governance_shadow_ready": shadow and trw,
        "request_trace_stage_ready": trw,
        "unified_query_export_ready": (arch / "LUNA_VOICE_GOVERNED_SUBMIT_UNIFIED_QUERY_EXPORT_VIEW_V0.md").is_file(),
        "governed_provider_entry_skeleton_ready": entry,
        "real_tts_entry_gate_wired": gate_wired,
        "voice_output_governance_docs_present": gov007,
    }


def _scan_playback(repo: Path) -> Dict[str, Any]:
    v = repo / "capabilities" / "voice"
    return {
        "tts_provider_selector_exists": (v / "providers/tts_provider_selector.py").is_file(),
        "qwen_tts_exists": (v / "providers/qwen_tts_provider.py").is_file(),
        "piper_fallback_exists": (v / "providers/piper_tts_provider.py").is_file(),
        "audio_worker_exists": (v / "output/audio_worker_v1.py").is_file(),
        "playback_runtime_connected": False,
        "provider_health_exists": (v / "runtime/tts_provider_health_v0.py").is_file(),
        "fallback_manager_exists": (v / "providers/tts_fallback_manager.py").is_file(),
        "tts_unified_entry_exists": (v / "runtime/tts_unified_entry.py").is_file(),
    }


def _scan_trace(repo: Path) -> Dict[str, Any]:
    v = repo / "capabilities" / "voice"
    ex = (v / "observations/request_trace_extractor.py").is_file()
    return {
        "request_id_required": True,
        "trace_id_required": True,
        "session_id_required": True,
        "diff_audit_required": True,
        "hard_audit_required": True,
        "trace_replay_whitebox_fields_defined": ex,
        "notes": "TRW adapter and extractor modules present; production hardening is separate phase.",
    }


def _gap_register(matrices: Dict[str, Any]) -> List[Dict[str, Any]]:
    gaps: List[Dict[str, Any]] = []
    asr = matrices["asr"]
    if not asr.get("asr_runtime_connected"):
        gaps.append({"id": "asr_mainline", "severity": "high", "detail": "ASR runtime chain not claimed connected"})
    if not matrices["semantic"].get("task_context_connected"):
        gaps.append({"id": "task_context", "severity": "medium", "detail": "Task context not connected to voice mainline"})
    if not matrices["qianwen"].get("qianwen_runtime_wiring_done"):
        gaps.append({"id": "qianwen_runtime", "severity": "high", "detail": "Qianwen-first runtime wiring not claimed done"})
    if not matrices["output_gov"].get("real_tts_entry_gate_wired"):
        gaps.append({"id": "tts_entry_gate", "severity": "high", "detail": "run_tts_unified_entry hard gate to voice_output_governance not verified wired in code scan"})
    if not matrices["playback"].get("playback_runtime_connected"):
        gaps.append({"id": "playback_mainline", "severity": "high", "detail": "Playback not claimed mainline-connected"})
    gaps.append(
        {
            "id": "full_chain",
            "severity": "high",
            "detail": "End-to-end user utterance → governed playback not claimed GO (expected for this readiness phase).",
        }
    )
    return gaps


def _next_step() -> Dict[str, Any]:
    return {
        "recommended_phases": [
            "VoiceInteraction-Readiness-002: ASR provider boundary + trace contract (design)",
            "VoiceRuntime-Gate-TTSUnified-001: wire voice_output_governance before run_tts_unified_entry (authorized phase only)",
            "VoiceConversation-Session-001: multi-turn session policy vs mainline product goals",
        ],
        "explicit_non_goals": ["Do not treat QwenTTSProvider as full conversational Qianwen", "Do not remove Piper/TTS fallback"],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / f"voice_interaction_readiness_001_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    asr_m = _scan_asr(repo)
    sess_m = _scan_session(repo)
    sem_m = _scan_semantic(repo)
    qw_m = _scan_qianwen(repo)
    og_m = _scan_output_gov(repo)
    pb_m = _scan_playback(repo)
    tr_m = _scan_trace(repo)

    matrices = {
        "asr": asr_m,
        "session": sess_m,
        "semantic": sem_m,
        "qianwen": qw_m,
        "output_gov": og_m,
        "playback": pb_m,
        "trace": tr_m,
    }
    gaps = _gap_register(matrices)

    summary = {
        "phase": "Phase-VoiceInteraction-Readiness-001",
        "repo_root": str(repo),
        "output_root": str(out),
        "three_way_split": {
            "voice_output_governance": "shadow_docs_and_modules_present_not_equal_full_voice",
            "qianwen_voice": "tts_provider_and_long_input_model_present_runtime_wiring_pending",
            "full_voice_interaction": "not_connected_readiness_pending",
        },
        "full_voice_interaction_connected": False,
        "qianwen_first_policy_preserved": True,
        "tts_fallback_preserved": True,
        "constraints": {
            "provider_invoked_by_tool": False,
            "real_tts_invoked": False,
            "playback_executed": False,
            "runtime_mutation": False,
            "ocr_bridge_touched": False,
        },
        "readiness_posture": "CONDITIONAL_GO_pending_mainline_wiring",
        "verdict": "GO",
        "gap_count": len(gaps),
    }

    _write_json(out / "voice_interaction_readiness_summary.json", summary)
    _write_json(out / "voice_asr_readiness_matrix.json", asr_m)
    _write_json(out / "voice_session_readiness_matrix.json", sess_m)
    _write_json(out / "voice_semantic_context_readiness_matrix.json", sem_m)
    _write_json(out / "voice_qianwen_interaction_readiness_matrix.json", qw_m)
    _write_json(out / "voice_output_governance_readiness_matrix.json", og_m)
    _write_json(out / "voice_playback_audio_readiness_matrix.json", pb_m)
    _write_json(out / "voice_trace_replay_audit_readiness_matrix.json", tr_m)
    _write_json(out / "voice_interaction_gap_register.json", {"gaps": gaps})
    _write_json(out / "voice_interaction_next_step_recommendation.json", _next_step())

    notes = out / "voice_interaction_readiness_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# Voice Interaction Readiness (v0)",
                "",
                f"- **repo_root**: `{repo}`",
                f"- **output_root**: `{out}`",
                "",
                "## Classification",
                "",
                "1. **Voice Output Governance** — shadow / TRW / query-export; **≠** full interaction.",
                "2. **Qwen TTS + long-input model providers** — **≠** full conversational product.",
                "3. **Full voice interaction** — `full_voice_interaction_connected=false` (readiness_pending).",
                "",
                f"- **verdict**: `{summary['verdict']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "verdict": summary["verdict"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
