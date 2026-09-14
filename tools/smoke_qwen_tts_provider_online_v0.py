# -*- coding: utf-8 -*-
"""
Phase-VoiceTTS-OnlineExp-001
Qwen TTS Controlled Online Provider Smoke v0.

Hard boundaries:
- Online experimental only: requires explicit --allow-online true.
- Must NOT modify offline-only default config.
- Must NOT call main.py; must NOT touch navigation chain.
- Must use unified TTS entry.
- Must NOT generate speech text; only consume provided --text.
- Must NOT play audio directly (legacy_submit is a stub).
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
import sys

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


DEFAULT_OFFLINE_CONFIG = "capabilities/voice/config/voice_tts_config.yaml"


def _now() -> float:
    return time.time()


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_json(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _to_jsonable(x: Any) -> Any:
    """
    Best-effort conversion to JSON-serializable objects.
    We must never crash the smoke tool due to serialization issues.
    """
    if x is None:
        return None
    if isinstance(x, (str, int, float, bool)):
        return x
    if isinstance(x, bytes):
        return {"_type": "bytes", "size": len(x), "b64_prefix": _safe_b64_prefix(x, 128)}
    if isinstance(x, (list, tuple)):
        return [_to_jsonable(v) for v in x]
    if isinstance(x, dict):
        return {str(k): _to_jsonable(v) for k, v in x.items()}
    # dataclass-like
    d = getattr(x, "__dict__", None)
    if isinstance(d, dict):
        return {str(k): _to_jsonable(v) for k, v in d.items()}
    return {"_type": type(x).__name__, "repr": repr(x)}


def _detect_wav(audio: bytes) -> bool:
    return len(audio) >= 12 and audio[:4] == b"RIFF" and audio[8:12] == b"WAVE"


def _safe_b64_prefix(audio: bytes, max_bytes: int = 256) -> str:
    if not audio:
        return ""
    raw = audio[: max(0, int(max_bytes))]
    return base64.b64encode(raw).decode("ascii")


def _boolish(s: str) -> bool:
    return str(s).strip().lower() in ("1", "true", "yes", "on")


def _try_import_dashscope() -> Dict[str, Any]:
    try:
        import dashscope  # type: ignore  # noqa: F401

        return {"dashscope_import_ok": True, "dashscope_import_error": None}
    except Exception as e:
        return {"dashscope_import_ok": False, "dashscope_import_error": repr(e)}


def _read_offline_defaults_snapshot() -> Dict[str, Any]:
    """
    Minimal snapshot to assert offline-only default policy is preserved.
    We intentionally do not parse YAML here to avoid adding deps; we rely on
    a simple text check for the frozen facts.
    """
    p = Path(REPO_ROOT) / DEFAULT_OFFLINE_CONFIG
    txt = p.read_text(encoding="utf-8")
    return {
        "offline_config_path": str(p),
        "offline_config_contains_offline_only_true": "offline_only: true" in txt,
        "offline_config_contains_provider_order_piper": "\nprovider_order:\n  - piper\n" in txt or "provider_order:\n  - piper\n" in txt,
        "offline_config_sha256_hint": None,  # intentionally omitted (no hashlib requirement)
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True, help="Text to synthesize (fixed test text).")
    ap.add_argument("--allow-online", required=True, help="Must be true to run online experimental smoke.")
    ap.add_argument("--provider", default="qwen", choices=["qwen"], help="Provider to smoke test.")
    ap.add_argument("--output-root", required=True, help="Output directory under logs/ ...")
    args = ap.parse_args()

    allow_online = _boolish(args.allow_online)
    out_root = Path(args.output_root)
    out_root.mkdir(parents=True, exist_ok=True)

    experiment_id = f"qwen_tts_online_smoke_001_{int(_now()*1000)}"
    started_s = _now()

    # Always snapshot offline defaults BEFORE running.
    offline_defaults_before = _read_offline_defaults_snapshot()

    dashscope_info = _try_import_dashscope()
    api_key_present = bool(os.environ.get("DASHSCOPE_API_KEY", "").strip())

    # Hard gate: must explicitly allow online.
    if not allow_online:
        result = {
            "experiment_id": experiment_id,
            "phase": "Phase-VoiceTTS-OnlineExp-001",
            "online_experimental": True,
            "allow_online": False,
            "provider_requested": args.provider,
            "provider_invoked": False,
            "provider_success": False,
            "provider_failed_reason": "ALLOW_ONLINE_FALSE",
            "fallback_used": False,
            "fallback_provider": "legacy_macos_say_stub",
            "dashscope_import_ok": dashscope_info["dashscope_import_ok"],
            "dashscope_import_error": dashscope_info["dashscope_import_error"],
            "dashscope_api_key_present": api_key_present,
            "generated_audio_file": None,
            "generated_audio_bytes_size": 0,
            "audio_bytes_b64_prefix": "",
            "text_input": args.text,
            "generate_text": False,
            "unified_entry_used": False,
            "mainline_config_mutated": False,
            "offline_default_policy_preserved": bool(
                offline_defaults_before["offline_config_contains_offline_only_true"]
                and offline_defaults_before["offline_config_contains_provider_order_piper"]
            ),
            "offline_defaults_before": offline_defaults_before,
            "offline_defaults_after": _read_offline_defaults_snapshot(),
            "final_execution_mode": "blocked",
            "fallback_trace": [],
            "hard_blockers": [],
            "soft_followups": [],
            "elapsed_ms": int((_now() - started_s) * 1000),
        }
        _write_json(out_root / "qwen_tts_online_smoke_result.json", result)
        _write_text(out_root / "smoke_notes.md", "Blocked: --allow-online must be true.\n")
        print(str(out_root))
        return 2

    # Build an *ephemeral* online experimental config under output_root.
    # Do NOT modify default offline config file.
    exp_cfg_path = out_root / "online_experimental_voice_tts_config.yaml"
    exp_cfg = "\n".join(
        [
            "offline_only: false",
            "active_provider: qwen",
            "fallback_provider: piper",
            "provider_order:",
            "  - qwen",
            "  - piper",
            "fallback:",
            "  enabled: true",
            "timeouts:",
            "  qwen_ms: 15000",
            "  piper_ms: 1500",
            "cutover:",
            "  enabled: true",
            "  mode: provider_chain_first",
            "  rollback_to_legacy_on_failure: true",
            "  rollback_on_selector_failure: true",
            "  rollback_on_provider_chain_failure: true",
            "legacy_fallback:",
            "  enabled: true",
            "local_runtime:",
            "  qwen:",
            "    enabled: true",
            "    api_key_env: \"DASHSCOPE_API_KEY\"",
            "    requires_network: true",
            "    requires_api_key: true",
            "    model: \"cosyvoice-v3-flash\"",
            "    voice: \"Serena\"",
            "    format: \"wav\"",
            "    sample_rate: 16000",
            "  piper:",
            "    enabled: false",
            "",
        ]
    )
    _write_text(exp_cfg_path, exp_cfg)

    legacy_called = {"called": 0}

    def _legacy_submit(_: str) -> bool:
        # MUST NOT play audio; only record fallback/execution.
        legacy_called["called"] += 1
        return True

    try:
        from capabilities.voice.runtime.tts_unified_entry import run_tts_unified_entry  # type: ignore
        from capabilities.voice.schemas.speech_request import SpeechRequest  # type: ignore

        req = SpeechRequest(
            request_id=f"onlineexp_{int(_now()*1000)}",
            source_module="smoke_qwen_tts_provider_online_v0",
            output_category="test",
            text_candidate=str(args.text),
            priority=1,
            interruptible=True,
            dedup_allowed=True,
            cooldown_key="qwen_onlineexp_smoke",
            metadata={"preset": "calm_female_v1"},
        )

        unified_result = run_tts_unified_entry(
            request=req,
            legacy_submit=_legacy_submit,
            config_path=str(exp_cfg_path),
        )

        pr = unified_result.provider_result
        sel = unified_result.selection_observation
        attempts = getattr(unified_result, "chain_attempts", None)
        audio_bytes: Optional[bytes] = pr.audio_bytes if (pr and getattr(pr, "audio_bytes", None)) else None
        audio_size = int(len(audio_bytes)) if audio_bytes else 0

        audio_file = None
        if audio_bytes and audio_size >= 64:
            if _detect_wav(audio_bytes):
                audio_file = "audio_output.wav"
                (out_root / audio_file).write_bytes(audio_bytes)
            else:
                audio_file = "audio_output.bin"
                (out_root / audio_file).write_bytes(audio_bytes)

        selected_provider = getattr(sel, "chosen_provider", None) if sel is not None else None
        provider_invoked = bool(selected_provider == args.provider)
        provider_success = bool(getattr(pr, "ok", False)) and bool(audio_bytes)
        provider_failed_reason = None
        if pr is not None and not provider_success:
            failure = getattr(pr, "failure", None)
            provider_failed_reason = getattr(failure, "reason", None) if failure is not None else "unknown"
        # If available, prefer the primary(qwen) failure reason from attempts.
        if isinstance(attempts, list):
            for a in attempts:
                if isinstance(a, dict) and a.get("provider") == args.provider and not a.get("ok"):
                    r = a.get("failure_reason")
                    if r:
                        provider_failed_reason = r
                    break

        offline_defaults_after = _read_offline_defaults_snapshot()
        offline_policy_preserved = bool(
            offline_defaults_before["offline_config_contains_offline_only_true"]
            and offline_defaults_before["offline_config_contains_provider_order_piper"]
            and offline_defaults_after["offline_config_contains_offline_only_true"]
            and offline_defaults_after["offline_config_contains_provider_order_piper"]
        )

        result = {
            "experiment_id": experiment_id,
            "phase": "Phase-VoiceTTS-OnlineExp-001",
            "online_experimental": True,
            "allow_online": True,
            "provider_requested": args.provider,
            "provider_invoked": bool(provider_invoked),
            "provider_success": bool(provider_success),
            "provider_failed_reason": provider_failed_reason,
            "selected_provider": selected_provider,
            "fallback_used": bool(legacy_called["called"] >= 1),
            "fallback_provider": "legacy_macos_say_stub",
            "legacy_submit_called": legacy_called["called"],
            "dashscope_import_ok": dashscope_info["dashscope_import_ok"],
            "dashscope_import_error": dashscope_info["dashscope_import_error"],
            "dashscope_api_key_present": api_key_present,
            "generated_audio_file": audio_file,
            "generated_audio_bytes_size": audio_size,
            "audio_bytes_b64_prefix": _safe_b64_prefix(audio_bytes or b"", 256),
            "text_input": str(args.text),
            "generate_text": False,
            "unified_entry_used": True,
            "mainline_config_mutated": False,
            "offline_default_policy_preserved": bool(offline_policy_preserved),
            "offline_defaults_before": offline_defaults_before,
            "offline_defaults_after": offline_defaults_after,
            "online_experimental_config_path": str(exp_cfg_path),
            "final_execution_mode": unified_result.final_execution_mode,
            "cutover_observation": _to_jsonable(unified_result.cutover_observation) if unified_result.cutover_observation else None,
            "provider_result": _to_jsonable(pr) if pr is not None else None,
            "chain_attempts": _to_jsonable(attempts),
            "selection_observation": _to_jsonable(unified_result.selection_observation) if unified_result.selection_observation else None,
            "fallback_observation": _to_jsonable(unified_result.fallback_observation) if unified_result.fallback_observation else None,
            "rollback_observation": _to_jsonable(unified_result.rollback_observation) if unified_result.rollback_observation else None,
            "hard_blockers": [],
            "soft_followups": [],
            "elapsed_ms": int((_now() - started_s) * 1000),
        }

        _write_json(out_root / "qwen_tts_online_smoke_result.json", result)
        _write_text(
            out_root / "smoke_notes.md",
            "\n".join(
                [
                    f"experiment_id: {experiment_id}",
                    "online_experimental: true",
                    "allow_online: true",
                    f"dashscope_import_ok: {dashscope_info['dashscope_import_ok']}",
                    f"DASHSCOPE_API_KEY_SET: {api_key_present}",
                    f"provider_success: {provider_success}",
                    f"fallback_used(legacy_stub_called): {legacy_called['called']}",
                    f"audio_file: {audio_file}",
                    "",
                    "NOTE: legacy_submit is a stub and does NOT play audio.",
                ]
            )
            + "\n",
        )
        print(str(out_root))
        return 0
    except Exception as e:
        offline_defaults_after = _read_offline_defaults_snapshot()
        result = {
            "experiment_id": experiment_id,
            "phase": "Phase-VoiceTTS-OnlineExp-001",
            "online_experimental": True,
            "allow_online": True,
            "provider_requested": args.provider,
            "provider_invoked": False,
            "provider_success": False,
            "provider_failed_reason": "EXCEPTION",
            "exception": repr(e),
            "fallback_used": bool(legacy_called["called"] >= 1),
            "fallback_provider": "legacy_macos_say_stub",
            "legacy_submit_called": legacy_called["called"],
            "dashscope_import_ok": dashscope_info["dashscope_import_ok"],
            "dashscope_import_error": dashscope_info["dashscope_import_error"],
            "dashscope_api_key_present": api_key_present,
            "generated_audio_file": None,
            "generated_audio_bytes_size": 0,
            "audio_bytes_b64_prefix": "",
            "text_input": str(args.text),
            "generate_text": False,
            "unified_entry_used": True,
            "mainline_config_mutated": False,
            "offline_default_policy_preserved": bool(
                offline_defaults_before["offline_config_contains_offline_only_true"]
                and offline_defaults_before["offline_config_contains_provider_order_piper"]
                and offline_defaults_after["offline_config_contains_offline_only_true"]
                and offline_defaults_after["offline_config_contains_provider_order_piper"]
            ),
            "offline_defaults_before": offline_defaults_before,
            "offline_defaults_after": offline_defaults_after,
            "online_experimental_config_path": str(exp_cfg_path),
            "hard_blockers": ["smoke_exception"],
            "soft_followups": [],
            "elapsed_ms": int((_now() - started_s) * 1000),
        }
        _write_json(out_root / "qwen_tts_online_smoke_result.json", result)
        _write_text(out_root / "smoke_notes.md", f"Exception: {repr(e)}\n")
        print(str(out_root))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

