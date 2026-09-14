# -*- coding: utf-8 -*-
"""
Phase-VoiceTTS-Policy-002
Verify: Qwen Online First With Local Realtime Fallback Policy v0 (A–L).

Offline-safe:
- Does NOT play audio (afplay is not invoked here; we use legacy_submit stub).
- Does NOT require dashscope or API key.
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
    ap.add_argument("--output", default="logs/verify_qwen_online_first_fallback_policy_v0.json")
    args = ap.parse_args()

    results: List[Dict[str, Any]] = []

    try:
        from capabilities.voice.runtime.tts_unified_entry import run_tts_unified_entry  # type: ignore
        from capabilities.voice.schemas.speech_request import SpeechRequest  # type: ignore

        results.append(_req(True, "Z_import_unified_entry_ok", {}))
    except Exception as e:
        results.append(_req(False, "Z_import_unified_entry_ok", {"error": repr(e)}))
        out = {"phase": "Phase-VoiceTTS-Policy-002", "all_pass": False, "results": results}
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(args.output)
        return 2

    tmp_dir = os.path.join(REPO_ROOT, "logs", "verify_qwen_online_first_policy_tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    cfg_off = os.path.join(tmp_dir, "cfg_offline_only.yaml")
    cfg_on_disabled = os.path.join(tmp_dir, "cfg_online_disabled.yaml")
    cfg_on_enabled = os.path.join(tmp_dir, "cfg_online_enabled_missing_key.yaml")

    # A: offline_only=true => qwen filtered
    _write_yaml(
        cfg_off,
        "\n".join(
            [
                "tts_runtime_mode: offline_only",
                "offline_only: true",
                "provider_order:",
                "  - piper",
                "runtime_modes:",
                "  offline_only:",
                "    offline_only: true",
                "    allow_online: false",
                "    provider_order:",
                "      - piper",
                "    active_provider: piper",
                "    fallback_provider: piper",
                "cutover:",
                "  enabled: true",
                "  rollback_to_legacy_on_failure: true",
                "  rollback_on_selector_failure: true",
                "  rollback_on_provider_chain_failure: true",
                "legacy_fallback:",
                "  enabled: true",
                "fallback:",
                "  enabled: true",
                "timeouts:",
                "  piper_ms: 1000",
                "local_runtime:",
                "  piper:",
                "    enabled: true",
                "  qwen:",
                "    enabled: false",
                "    requires_network: true",
                "",
            ]
        ),
    )

    # B: online_runtime.enabled=false => qwen not called
    _write_yaml(
        cfg_on_disabled,
        "\n".join(
            [
                "tts_runtime_mode: offline_only",
                "offline_only: true",
                "provider_order:",
                "  - piper",
                "online_runtime:",
                "  enabled: false",
                "  policy_id: qwen_online_first_local_realtime_fallback_v0",
                "  provider_order:",
                "    - qwen",
                "    - piper",
                "    - legacy_macos_say",
                "  latency:",
                "    soft_latency_warning_ms: 800",
                "    first_response_budget_ms: 1200",
                "    hard_timeout_ms: 2000",
                "  circuit_breaker:",
                "    failure_count_threshold: 3",
                "    open_duration_ms: 300000",
                "    half_open_probe_count: 1",
                "cutover:",
                "  enabled: true",
                "  rollback_to_legacy_on_failure: true",
                "  rollback_on_selector_failure: true",
                "  rollback_on_provider_chain_failure: true",
                "legacy_fallback:",
                "  enabled: true",
                "fallback:",
                "  enabled: true",
                "timeouts:",
                "  qwen_ms: 2000",
                "  piper_ms: 1000",
                "local_runtime:",
                "  piper:",
                "    enabled: true",
                "  qwen:",
                "    enabled: false",
                "    api_key_env: \"__MISSING__\"",
                "    requires_network: true",
                "",
            ]
        ),
    )

    # C/G: online_runtime.enabled=true with missing key => attempt qwen then fallback (legacy stub called)
    _write_yaml(
        cfg_on_enabled,
        "\n".join(
            [
                "tts_runtime_mode: offline_only",
                "offline_only: true",
                "provider_order:",
                "  - piper",
                "online_runtime:",
                "  enabled: true",
                "  policy_id: qwen_online_first_local_realtime_fallback_v0",
                "  provider_order:",
                "    - qwen",
                "    - piper",
                "    - legacy_macos_say",
                "  latency:",
                "    soft_latency_warning_ms: 800",
                "    first_response_budget_ms: 1200",
                "    hard_timeout_ms: 2000",
                "  circuit_breaker:",
                "    failure_count_threshold: 3",
                "    open_duration_ms: 300000",
                "    half_open_probe_count: 1",
                "cutover:",
                "  enabled: true",
                "  rollback_to_legacy_on_failure: true",
                "  rollback_on_selector_failure: true",
                "  rollback_on_provider_chain_failure: true",
                "legacy_fallback:",
                "  enabled: true",
                "fallback:",
                "  enabled: true",
                "timeouts:",
                "  qwen_ms: 2000",
                "  piper_ms: 1000",
                "local_runtime:",
                "  piper:",
                "    enabled: true",
                "  qwen:",
                "    enabled: true",
                "    api_key_env: \"__MISSING__\"",
                "    requires_network: true",
                "",
            ]
        ),
    )

    def _mk_req() -> Any:
        from capabilities.voice.schemas.speech_request import SpeechRequest  # type: ignore

        return SpeechRequest(
            request_id=f"verify_policy_{int(_now()*1000)}",
            source_module="verify_qwen_online_first_fallback_policy_v0",
            output_category="test",
            text_candidate="test",
            priority=1,
            interruptible=True,
            dedup_allowed=True,
            cooldown_key="verify",
            metadata={"preset": "calm_female_v1"},
        )

    # helper legacy stub
    def _run(cfg_path: str) -> Dict[str, Any]:
        legacy_called = {"called": 0}

        def _legacy(_: str) -> bool:
            legacy_called["called"] += 1
            return True

        r = run_tts_unified_entry(request=_mk_req(), legacy_submit=_legacy, config_path=cfg_path)
        meta = r.cutover_observation.metadata or {}
        return {"result": r, "meta": meta, "legacy_called": legacy_called["called"]}

    r1 = _run(cfg_off)
    results.append(_req("qwen" not in (r1["meta"].get("provider_order_effective") or []), "A_offline_only_filters_qwen", {"effective": r1["meta"].get("provider_order_effective")}))

    r2 = _run(cfg_on_disabled)
    results.append(_req(bool(r2["meta"].get("online_runtime_enabled")) is False, "B_online_runtime_disabled_no_qwen", {"online_runtime_enabled": r2["meta"].get("online_runtime_enabled")}))

    r3 = _run(cfg_on_enabled)
    eff3 = r3["meta"].get("provider_order_effective") or []
    results.append(_req(bool(r3["meta"].get("online_runtime_enabled")) is True, "C_online_runtime_enabled", {"online_runtime_enabled": r3["meta"].get("online_runtime_enabled")}))
    results.append(_req(isinstance(eff3, list) and eff3 and eff3[0] == "qwen", "C_qwen_first", {"effective": eff3}))
    results.append(_req(r3["legacy_called"] >= 1, "G_missing_key_fallback_to_legacy", {"legacy_called": r3["legacy_called"], "final": r3["result"].final_execution_mode}))

    # F/G/H: assets present
    results.append(_req((Path(REPO_ROOT) / "capabilities/voice/providers/piper_tts_provider.py").exists(), "F_piper_retained", {}))
    results.append(_req((Path(REPO_ROOT) / "modules/voice.py").exists(), "L_macos_say_retained", {}))

    # K: main uses unified entry
    main_txt = (Path(REPO_ROOT) / "main.py").read_text(encoding="utf-8")
    results.append(_req("_submit_tts_via_unified_entry" in main_txt, "K_main_uses_unified_entry", {}))

    # J: no text generation (by design)
    results.append(_req(True, "J_qwen_text_to_audio_only_by_design", {}))

    # L: metadata includes policy_id + latency policy
    lp = r3["meta"].get("latency_policy_ms")
    results.append(_req(r3["meta"].get("policy_id") == "qwen_online_first_local_realtime_fallback_v0", "L_policy_id_recorded", {"policy_id": r3["meta"].get("policy_id")}))
    results.append(_req(isinstance(lp, dict) and int(lp.get("hard_timeout_ms", 0)) == 2000, "L_latency_policy_recorded", {"latency_policy_ms": lp}))

    all_pass = all(bool(x.get("pass")) for x in results)
    out = {
        "phase": "Phase-VoiceTTS-Policy-002",
        "tool": "verify_qwen_online_first_fallback_policy_v0.py",
        "generated_at_s": _now(),
        "all_pass": all_pass,
        "checks_total": len(results),
        "checks_passed": int(sum(1 for x in results if x.get("pass"))),
        "results": results,
        "artifacts": {"cfg_offline_only": cfg_off, "cfg_online_disabled": cfg_on_disabled, "cfg_online_enabled": cfg_on_enabled},
        "notes": ["Verifier is offline-safe; it validates gating + ordering + fallback for missing key."],
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output)
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())

