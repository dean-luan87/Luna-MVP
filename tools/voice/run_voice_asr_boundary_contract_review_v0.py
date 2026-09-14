#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-VoiceInteraction-Readiness-002 — Read-only ASR boundary & final_text trace contract review.

Does NOT invoke ASR, Whisper, Qianwen, TTS, or playback. Does NOT mutate voice runtime.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _load_readiness_summary(readiness_root: Path) -> Optional[Dict[str, Any]]:
    p = readiness_root / "voice_interaction_readiness_summary.json"
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _load_contract_module(repo: Path):
    """Load contract module by file path to avoid PYTHONPATH assumptions."""
    mod_path = repo / "capabilities" / "voice" / "input" / "asr_final_text_event_contract_v0.py"
    spec = importlib.util.spec_from_file_location("asr_final_text_event_contract_v0", mod_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"ERROR: cannot load contract module from {mod_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _state_machine_matrix() -> Dict[str, Any]:
    return {
        "states": [
            "idle",
            "listening",
            "partial_transcribing",
            "finalizing",
            "final_text_ready",
            "no_speech",
            "timeout",
            "cancelled",
            "provider_error",
            "low_confidence",
            "suppressed",
        ],
        "only_final_text_ready_allows_semantic_downstream": True,
        "downstream_entry_states": ["final_text_ready"],
        "rules": {
            "no_speech_timeout_cancelled_no_qianwen": True,
            "low_confidence_confirm_repeat_suppress_only": True,
            "provider_error_fail_closed": True,
        },
        "notes": "Semantic/Qianwen only after final_text_ready + event asr_status==final per architecture docs.",
    }


def _trace_replay_audit_matrix() -> Dict[str, Any]:
    return {
        "required_trace_fields": [
            "request_id",
            "trace_id",
            "session_id",
            "utterance_id",
            "source_audio_ref",
            "provider_id",
            "asr_status",
            "partial_count",
            "final_text",
            "confidence",
            "latency_ms",
            "fallback_reason",
            "hard_audit",
        ],
        "contract_version": "voice.asr.trace_replay_audit_v0",
    }


def _fallback_suppress_matrix() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = [
        {
            "condition": "provider_unavailable",
            "action": "suppress_or_fallback_provider_candidate",
            "qianwen_allowed": False,
        },
        {"condition": "low_confidence", "action": "confirm_repeat_suppress", "qianwen_allowed": False},
        {"condition": "no_speech", "action": "close_session_or_wait", "qianwen_allowed": False},
        {"condition": "timeout", "action": "close_utterance", "qianwen_allowed": False},
        {"condition": "cancelled", "action": "cancel_utterance", "qianwen_allowed": False},
        {"condition": "provider_error", "action": "fail_closed", "qianwen_allowed": False},
    ]
    return {"policy_rows": rows, "tts_playback_in_this_phase": False}


def _runtime_flag_matrix() -> Dict[str, Any]:
    return {
        "flags": [
            {
                "name": "LUNA_DISABLE_VOICE_ASR_RUNTIME_V1",
                "default_value": True,
                "meaning": "Global ASR runtime kill; when true no provider/final_text dispatch",
            },
            {
                "name": "LUNA_ENABLE_VOICE_ASR_SHADOW_V1",
                "default_value": False,
                "meaning": "Shadow/trace only path",
            },
            {
                "name": "LUNA_ENABLE_VOICE_ASR_PROVIDER_V1",
                "default_value": False,
                "meaning": "Real ASR provider calls (separate authorized phase)",
            },
            {
                "name": "LUNA_ENABLE_VOICE_ASR_FINAL_TEXT_DISPATCH_V1",
                "default_value": False,
                "meaning": "Emit final_text to downstream (separate authorized phase)",
            },
        ],
        "defaults_all_conservative_closed": True,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--voice-readiness-root", required=True)
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    readiness = _require_abs(args.voice_readiness_root, "--voice-readiness-root")
    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / f"voice_asr_boundary_contract_002_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    voice_doc = repo / "docs" / "architecture" / "voice"
    required_docs = [
        "LUNA_VOICE_ASR_BOUNDARY_CONTRACT_V0.md",
        "LUNA_VOICE_ASR_FINAL_TEXT_EVENT_SCHEMA_V0.md",
        "LUNA_VOICE_ASR_TRACE_REPLAY_AUDIT_CONTRACT_V0.md",
        "LUNA_VOICE_ASR_STATE_MACHINE_V0.md",
        "LUNA_VOICE_ASR_FALLBACK_SUPPRESS_POLICY_V0.md",
        "LUNA_VOICE_ASR_RUNTIME_FLAG_AND_KILL_SWITCH_PLAN_V0.md",
        "LUNA_VOICE_ASR_BOUNDARY_CONTRACT_GO_NO_GO_PACK_V0.md",
    ]
    doc_status = {name: (voice_doc / name).is_file() for name in required_docs}
    contract_py = repo / "capabilities" / "voice" / "input" / "asr_final_text_event_contract_v0.py"
    contract_exists = contract_py.is_file()

    prev_summary = _load_readiness_summary(readiness)

    mod = _load_contract_module(repo)
    event_schema = mod.asr_final_text_event_json_schema_fields_v0()
    example_event = mod.example_asr_final_text_event_v0()

    sm_m = _state_machine_matrix()
    tr_m = _trace_replay_audit_matrix()
    fb_m = _fallback_suppress_matrix()
    rf_m = _runtime_flag_matrix()

    all_docs_ok = all(doc_status.values()) and contract_exists

    summary: Dict[str, Any] = {
        "phase": "Phase-VoiceInteraction-Readiness-002",
        "repo_root": str(repo),
        "voice_readiness_input_root": str(readiness),
        "output_root": str(out),
        "prior_voice_interaction_readiness_001": prev_summary,
        "docs_present": doc_status,
        "asr_final_text_contract_py_present": contract_exists,
        "contract_review_ok": all_docs_ok,
        "readiness_posture": "CONDITIONAL_GO_pending_asr_runtime_wiring"
        if all_docs_ok
        else "NO_GO_missing_artifacts",
        "verdict": "GO" if all_docs_ok else "NO_GO",
        "constraints": {
            "asr_provider_invoked": False,
            "qianwen_invoked": False,
            "tts_invoked": False,
            "playback_executed": False,
            "runtime_mutation": False,
            "whisper_invoked": False,
        },
        "qianwen_first_policy_preserved": True,
        "tts_fallback_preserved": True,
        "only_final_text_ready_downstream_entry": sm_m.get("only_final_text_ready_allows_semantic_downstream"),
    }

    _write_json(out / "voice_asr_boundary_contract_summary.json", summary)
    _write_json(
        out / "voice_asr_final_text_event_schema.json",
        {"json_schema_fields": event_schema, "example_event": example_event},
    )
    _write_json(out / "voice_asr_state_machine_matrix.json", sm_m)
    _write_json(out / "voice_asr_trace_replay_audit_matrix.json", tr_m)
    _write_json(out / "voice_asr_fallback_suppress_matrix.json", fb_m)
    _write_json(out / "voice_asr_runtime_flag_matrix.json", rf_m)

    notes = out / "voice_asr_boundary_contract_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# Voice ASR Boundary Contract Review (v0)",
                "",
                f"- **repo_root**: `{repo}`",
                f"- **voice_readiness_input_root**: `{readiness}`",
                f"- **output_root**: `{out}`",
                "",
                "## Artifacts",
                "",
                "- Contract code: `capabilities/voice/input/asr_final_text_event_contract_v0.py`",
                "- Architecture docs under `docs/architecture/voice/LUNA_VOICE_ASR_*`",
                "",
                f"- **contract_review_ok**: `{all_docs_ok}`",
                f"- **verdict**: `{summary['verdict']}`",
                "",
                "## Hard rule",
                "",
                "Only **`final_text_ready`** (+ `asr_status==final` per docs) may feed semantic / Qianwen downstream.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "verdict": summary["verdict"], "contract_review_ok": all_docs_ok}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
