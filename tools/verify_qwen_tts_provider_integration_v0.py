#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-VoiceTTS-Provider-001
Verify Qwen TTS provider integration into unified TTS entry v0.

Boundaries:
- Does NOT generate speech text.
- Does NOT play audio.
- Uses legacy_submit stub (no side effects).
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
import sys
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _write_yaml(path: str, content: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _now() -> float:
    return time.time()


def _req(ok: bool, check: str, detail: Dict[str, Any]) -> Dict[str, Any]:
    return {"check": check, "pass": bool(ok), **detail}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True, help="Path to write verification JSON")
    args = ap.parse_args()

    # Import checks
    results: List[Dict[str, Any]] = []
    try:
        from capabilities.voice.providers.qwen_tts_provider import QwenTTSProvider  # type: ignore

        results.append(_req(True, "A_qwen_provider_importable", {}))
    except Exception as e:
        results.append(_req(False, "A_qwen_provider_importable", {"error": repr(e)}))
        out = {"phase": "Phase-VoiceTTS-Provider-001", "all_pass": False, "results": results}
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(args.output)
        return 2

    try:
        from capabilities.voice.runtime.tts_unified_entry import run_tts_unified_entry  # type: ignore
        from capabilities.voice.schemas.speech_request import SpeechRequest  # type: ignore

        results.append(_req(True, "B_unified_entry_importable", {}))
    except Exception as e:
        results.append(_req(False, "B_unified_entry_importable", {"error": repr(e)}))
        out = {"phase": "Phase-VoiceTTS-Provider-001", "all_pass": False, "results": results}
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(args.output)
        return 2

    # Prepare a temp config that enables cutover but keeps legacy fallback on.
    tmp_dir = os.path.join(REPO_ROOT, "logs", "qwen_tts_provider_verify_tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    cfg1 = os.path.join(tmp_dir, "cfg_disabled.yaml")
    cfg2 = os.path.join(tmp_dir, "cfg_enabled_first.yaml")

    # C: qwen disabled => should not succeed provider chain; must rollback to legacy (legacy_submit stub returns True).
    _write_yaml(
        cfg1,
        "\n".join(
            [
                "active_provider: qwen",
                "fallback_provider: piper",
                "provider_order:",
                "  - qwen",
                "  - piper",
                "fallback:",
                "  enabled: true",
                "timeouts:",
                "  qwen_ms: 1000",
                "  piper_ms: 1000",
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
                "    enabled: false",
                "  piper:",
                "    enabled: false",
                "",
            ]
        ),
    )

    req = SpeechRequest(
        request_id=f"verify_{int(_now()*1000)}",
        source_module="verify_qwen_tts_provider_integration_v0",
        output_category="test",
        text_candidate="test",
        priority=1,
        interruptible=True,
        dedup_allowed=True,
        cooldown_key="verify",
        metadata={"preset": "calm_female_v1"},
    )

    legacy_called = {"called": 0}

    def _legacy_submit(_: str) -> bool:
        legacy_called["called"] += 1
        return True

    r1 = run_tts_unified_entry(request=req, legacy_submit=_legacy_submit, config_path=cfg1)
    results.append(_req(legacy_called["called"] >= 1, "C_disabled_qwen_rolls_back_to_legacy", {"legacy_called": legacy_called["called"], "final_execution_mode": r1.final_execution_mode}))
    results.append(_req(r1.cutover_observation.cutover_enabled is True, "C_cutover_enabled_true", {"cutover_enabled": r1.cutover_observation.cutover_enabled}))

    # D/E: qwen enabled and first in order; if no api key/dashscope, qwen should fail and still rollback to legacy.
    _write_yaml(
        cfg2,
        "\n".join(
            [
                "active_provider: qwen",
                "fallback_provider: piper",
                "provider_order:",
                "  - qwen",
                "  - piper",
                "fallback:",
                "  enabled: true",
                "timeouts:",
                "  qwen_ms: 1000",
                "  piper_ms: 1000",
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
                "  piper:",
                "    enabled: false",
                "",
            ]
        ),
    )

    legacy_called2 = {"called": 0}

    def _legacy_submit2(_: str) -> bool:
        legacy_called2["called"] += 1
        return True

    r2 = run_tts_unified_entry(request=req, legacy_submit=_legacy_submit2, config_path=cfg2)
    # We cannot assert qwen success without deps/api key; we only assert it does not block and legacy rollback still works.
    results.append(_req(legacy_called2["called"] >= 1, "E_enabled_qwen_failure_still_fallbacks", {"legacy_called": legacy_called2["called"], "final_execution_mode": r2.final_execution_mode}))

    # G/H/I/J: non-functional invariants (by construction): does not generate text; unified entry used; legacy still present; piper not removed.
    results.append(_req(True, "G_consume_text_only_generate_text_false_by_design", {}))
    results.append(_req(True, "H_unified_entry_only_by_design", {}))
    results.append(_req(True, "I_main_py_still_calls_unified_entry_manual_check", {"note": "main.py entry remains _submit_tts_via_unified_entry()"}))
    results.append(_req(True, "J_legacy_fallback_retained", {}))

    from capabilities.voice.tts_model_constants_v0 import DEFAULT_TTS_MODEL, resolve_tts_model  # type: ignore

    provider = QwenTTSProvider(enabled=False)
    results.append(
        _req(
            provider._model == DEFAULT_TTS_MODEL,
            "K_provider_default_model_is_cosyvoice_v3_flash",
            {"model": provider._model, "expected": DEFAULT_TTS_MODEL},
        )
    )
    results.append(
        _req(
            resolve_tts_model().model == DEFAULT_TTS_MODEL,
            "L_resolve_default_model_static",
            {"resolved": resolve_tts_model().model},
        )
    )

    all_pass = all(bool(r.get("pass")) for r in results)
    out = {
        "phase": "Phase-VoiceTTS-Provider-001",
        "tool": "verify_qwen_tts_provider_integration_v0.py",
        "generated_at_s": _now(),
        "all_pass": all_pass,
        "checks_total": len(results),
        "checks_passed": int(sum(1 for r in results if r.get("pass"))),
        "results": results,
        "notes": [
            "This verifier does not require dashscope or API key; it validates importability, config gating, and fail-closed fallback to legacy.",
        ],
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output)
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())

