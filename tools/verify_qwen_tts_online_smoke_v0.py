# -*- coding: utf-8 -*-
"""
Phase-VoiceTTS-OnlineExp-001
Verify Qwen TTS Online Experimental Smoke v0 (A–J).

This verifier:
- checks offline-only default config is unchanged
- checks smoke result structure and invariants
- checks online attempts require allow_online=true
- checks graceful fallback behavior without API key/deps
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


DEFAULT_OFFLINE_CONFIG = Path(REPO_ROOT) / "capabilities/voice/config/voice_tts_config.yaml"


def _req(ok: bool, check: str, detail: Dict[str, Any]) -> Dict[str, Any]:
    return {"check": check, "pass": bool(ok), **detail}


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _offline_defaults_ok() -> Dict[str, Any]:
    txt = DEFAULT_OFFLINE_CONFIG.read_text(encoding="utf-8")
    return {
        "offline_only_true": "offline_only: true" in txt,
        "provider_order_piper_only": ("\nprovider_order:\n  - piper\n" in txt) or ("provider_order:\n  - piper\n" in txt),
    }


def _contains(s: str, sub: str) -> bool:
    return sub in (s or "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True, help="output_root produced by smoke tool")
    ap.add_argument("--output", default="", help="optional path to write verification JSON")
    args = ap.parse_args()

    smoke_root = Path(args.smoke_root)
    smoke_json = smoke_root / "qwen_tts_online_smoke_result.json"
    out_path = Path(args.output) if args.output else (smoke_root / "verify_qwen_tts_online_smoke_v0.json")

    results: List[Dict[str, Any]] = []

    # A. offline-only default config not modified
    off = _offline_defaults_ok()
    results.append(
        _req(
            bool(off["offline_only_true"] and off["provider_order_piper_only"]),
            "A_offline_default_config_preserved",
            {"offline_config": str(DEFAULT_OFFLINE_CONFIG), **off},
        )
    )

    # Load smoke result
    if not smoke_json.exists():
        results.append(_req(False, "Z_smoke_result_exists", {"path": str(smoke_json)}))
        out = {"phase": "Phase-VoiceTTS-OnlineExp-001", "all_pass": False, "results": results}
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(str(out_path))
        return 2

    smoke = _read_json(smoke_json)
    results.append(_req(True, "Z_smoke_result_exists", {"path": str(smoke_json)}))

    # Basic structure
    results.append(_req(smoke.get("online_experimental") is True, "Z_online_experimental_true", {"online_experimental": smoke.get("online_experimental")}))
    results.append(_req(smoke.get("unified_entry_used") in (True, False), "Z_unified_entry_field_present", {"unified_entry_used": smoke.get("unified_entry_used")}))

    # B. qwen only attempted when allow_online=true
    allow_online = smoke.get("allow_online")
    provider_invoked = bool(smoke.get("provider_invoked"))
    results.append(
        _req(
            (allow_online is True and smoke.get("unified_entry_used") is True) or (allow_online is False and provider_invoked is False),
            "B_qwen_only_attempted_when_allow_online_true",
            {"allow_online": allow_online, "provider_invoked": provider_invoked, "unified_entry_used": smoke.get("unified_entry_used")},
        )
    )

    # C. missing key => graceful fail or fallback; no crash
    key_present = bool(smoke.get("dashscope_api_key_present"))
    provider_success = bool(smoke.get("provider_success"))
    fallback_used = bool(smoke.get("fallback_used"))
    if not key_present:
        results.append(
            _req(
                (provider_success is False) and (fallback_used is True),
                "C_missing_api_key_graceful_fail_and_fallback",
                {"dashscope_api_key_present": key_present, "provider_success": provider_success, "fallback_used": fallback_used, "provider_failed_reason": smoke.get("provider_failed_reason")},
            )
        )
    else:
        results.append(_req(True, "C_missing_api_key_graceful_fail_and_fallback", {"skipped": True, "dashscope_api_key_present": True}))

    # D. key present => attempt synthesis (provider_invoked should be true)
    if key_present:
        results.append(
            _req(
                provider_invoked is True,
                "D_key_present_attempted_provider_invoke",
                {"dashscope_api_key_present": key_present, "provider_invoked": provider_invoked},
            )
        )
    else:
        results.append(_req(True, "D_key_present_attempted_provider_invoke", {"skipped": True, "dashscope_api_key_present": False}))

    # E. provider result schema present (even on failure)
    pr = smoke.get("provider_result")
    results.append(_req(pr is None or isinstance(pr, dict), "E_provider_result_schema_present_or_null", {"provider_result_type": type(pr).__name__}))

    # F. fallback usable
    results.append(_req(fallback_used is True, "F_fallback_used_or_available", {"fallback_used": fallback_used, "legacy_submit_called": smoke.get("legacy_submit_called")}))

    # G. Piper/macOS say not removed (smoke can't prove removal; we assert key files exist)
    piper_file = Path(REPO_ROOT) / "capabilities/voice/providers/piper_tts_provider.py"
    macos_voice_file = Path(REPO_ROOT) / "modules/voice.py"
    results.append(_req(piper_file.exists() and macos_voice_file.exists(), "G_offline_fallback_assets_present", {"piper_exists": piper_file.exists(), "macos_voice_exists": macos_voice_file.exists()}))

    # H. main.py not modified to call qwen directly (simple text scan)
    main_py = (Path(REPO_ROOT) / "main.py").read_text(encoding="utf-8")
    results.append(
        _req(
            ("qwen_tts_provider" not in main_py) and ("dashscope" not in main_py) and ("QwenTTSProvider" not in main_py),
            "H_main_py_not_calling_qwen_directly",
            {"main_contains_qwen_provider": _contains(main_py, "QwenTTSProvider"), "main_contains_dashscope": _contains(main_py, "dashscope")},
        )
    )

    # I. no text generation (fixed)
    results.append(_req(smoke.get("generate_text") is False, "I_no_text_generation", {"generate_text": smoke.get("generate_text")}))

    # J. online experimental result does not write back default config
    results.append(
        _req(
            smoke.get("mainline_config_mutated") is False and bool(smoke.get("offline_default_policy_preserved")) is True,
            "J_no_default_config_mutation",
            {"mainline_config_mutated": smoke.get("mainline_config_mutated"), "offline_default_policy_preserved": smoke.get("offline_default_policy_preserved")},
        )
    )

    all_pass = all(bool(r.get("pass")) for r in results)
    out = {
        "phase": "Phase-VoiceTTS-OnlineExp-001",
        "tool": "verify_qwen_tts_online_smoke_v0.py",
        "all_pass": all_pass,
        "checks_total": len(results),
        "checks_passed": int(sum(1 for r in results if r.get("pass"))),
        "results": results,
        "artifacts": {"smoke_root": str(smoke_root), "smoke_json": str(smoke_json)},
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(out_path))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())

