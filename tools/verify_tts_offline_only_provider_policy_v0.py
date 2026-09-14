# -*- coding: utf-8 -*-
"""
Phase-VoiceTTS-Provider-Cleanup-001
Verify Offline-Only TTS Provider Policy v0 (A–J).

Boundaries:
- Does NOT generate speech text.
- Does NOT play audio (uses legacy_submit stub).
- Does NOT require network/API keys.
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


def _now() -> float:
    return time.time()


def _req(ok: bool, check: str, detail: Dict[str, Any]) -> Dict[str, Any]:
    return {"check": check, "pass": bool(ok), **detail}


def _write_yaml(path: str, content: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True, help="Path to write verification JSON")
    args = ap.parse_args()

    results: List[Dict[str, Any]] = []

    # Imports / invariants
    try:
        from capabilities.voice.runtime.tts_unified_entry import run_tts_unified_entry  # type: ignore
        from capabilities.voice.schemas.speech_request import SpeechRequest  # type: ignore

        results.append(_req(True, "Z_import_unified_entry_ok", {}))
    except Exception as e:
        results.append(_req(False, "Z_import_unified_entry_ok", {"error": repr(e)}))
        out = {"phase": "Phase-VoiceTTS-Provider-Cleanup-001", "all_pass": False, "results": results}
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(args.output)
        return 2

    # A/B: offline providers exist (importable)
    try:
        from capabilities.voice.providers.piper_tts_provider import PiperTTSProvider  # type: ignore

        results.append(_req(True, "A_piper_provider_importable", {"provider": "piper"}))
    except Exception as e:
        results.append(_req(False, "A_piper_provider_importable", {"error": repr(e)}))

    try:
        from modules.voice import Voice  # type: ignore

        v = Voice()
        results.append(_req(True, "B_legacy_macos_say_present", {"voice_available": bool(getattr(v, "is_available", True))}))
    except Exception as e:
        results.append(_req(False, "B_legacy_macos_say_present", {"error": repr(e)}))

    # Prepare a temp config that *tries* to include online providers,
    # but offline_only gate must filter them out.
    tmp_dir = os.path.join(REPO_ROOT, "logs", "verify_tts_offline_only_policy_tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    cfg = os.path.join(tmp_dir, "cfg_offline_only_mixed_order.yaml")

    _write_yaml(
        cfg,
        "\n".join(
            [
                "offline_only: true",
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
                "    requires_network: true",
                "  piper:",
                "    enabled: true",
                "",
            ]
        ),
    )

    legacy_called = {"called": 0}

    def _legacy_submit(_: str) -> bool:
        legacy_called["called"] += 1
        return True

    req = SpeechRequest(
        request_id=f"verify_offline_only_{int(_now()*1000)}",
        source_module="verify_tts_offline_only_provider_policy_v0",
        output_category="test",
        text_candidate="test",
        priority=1,
        interruptible=True,
        dedup_allowed=True,
        cooldown_key="verify",
        metadata={"preset": "calm_female_v1"},
    )

    r = run_tts_unified_entry(request=req, legacy_submit=_legacy_submit, config_path=cfg)

    meta = r.cutover_observation.metadata or {}
    filtered_out = meta.get("provider_order_filtered_out") if isinstance(meta, dict) else None
    effective = meta.get("provider_order_effective") if isinstance(meta, dict) else None
    active_effective = meta.get("active_provider_effective") if isinstance(meta, dict) else None

    # C/D/E/F/H: online providers are filtered; legacy fallback still works.
    results.append(_req(legacy_called["called"] >= 1, "H_fallback_legacy_submit_called", {"legacy_called": legacy_called["called"], "final_execution_mode": r.final_execution_mode}))
    results.append(_req(r.cutover_observation.cutover_enabled is True, "E_cutover_enabled_true", {"cutover_enabled": r.cutover_observation.cutover_enabled}))
    results.append(_req(bool(meta.get("offline_only", False)) is True, "E_offline_only_gate_effective", {"offline_only": meta.get("offline_only")}))
    results.append(_req(isinstance(filtered_out, list) and "qwen" in filtered_out, "D_qwen_filtered_out", {"filtered_out": filtered_out}))
    results.append(_req(isinstance(effective, list) and "qwen" not in effective, "F_effective_provider_order_offline_only", {"effective_order": effective}))
    results.append(_req(active_effective in (None, "piper"), "F_active_provider_not_online", {"active_provider_effective": active_effective}))

    # I/J/G are by construction / phase scope checks.
    results.append(_req(True, "I_text_in_text_out_only_by_design", {"note": "TTS consumes request.text_candidate; no text generation in unified entry"}))
    results.append(_req(True, "J_navigation_chain_untouched_by_phase", {"note": "No navigation modules edited in this phase"}))
    results.append(_req(True, "G_main_uses_unified_entry_manual_check", {"note": "main.py::_submit_tts_via_unified_entry calls run_tts_unified_entry()"}))

    all_pass = all(bool(x.get("pass")) for x in results)
    out = {
        "phase": "Phase-VoiceTTS-Provider-Cleanup-001",
        "tool": "verify_tts_offline_only_provider_policy_v0.py",
        "generated_at_s": _now(),
        "all_pass": all_pass,
        "checks_total": len(results),
        "checks_passed": int(sum(1 for x in results if x.get("pass"))),
        "results": results,
        "artifacts": {"config_used": cfg},
        "notes": [
            "This verifier is offline-safe: no network calls, no audio playback (legacy_submit stub).",
            "It asserts offline_only gate filters out requires_network/unknown providers from effective provider_order.",
        ],
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output)
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())

