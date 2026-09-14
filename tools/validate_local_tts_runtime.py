#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stage-2.2 本机真实执行验证脚本

模式：
1) piper
2) rollback (Piper 失败 -> legacy rollback)
3) cutover_off (cutover 关闭 -> legacy 直通)
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
OBS_PATH = LOG_DIR / "voice_stage22_observations.jsonl"

from capabilities.voice.providers.piper_tts_provider import PiperTTSProvider
from capabilities.voice.runtime.tts_unified_entry import run_tts_unified_entry
from capabilities.voice.schemas.speech_request import SpeechRequest
from modules.voice import Voice


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data if isinstance(data, dict) else {}


def _save_yaml(path: Path, data: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def _record_obs(obj: Dict[str, Any]) -> None:
    with OBS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def _legacy_submit(text: str) -> bool:
    v = Voice()
    return v.speak(text)


def _speech_request(text: str, preset: str = "calm_female_v1") -> SpeechRequest:
    return SpeechRequest(
        request_id=f"stage22_{int(time.time()*1000)}",
        source_module="validate_local_tts_runtime",
        output_category="interaction_result",
        text_candidate=text,
        priority=1,
        interruptible=True,
        dedup_allowed=True,
        cooldown_key="stage22_validation",
        metadata={"preset": preset},
    )


def mode_piper(config_path: Path, presets_path: Path, text: str) -> Dict[str, Any]:
    cfg = _load_yaml(config_path)
    presets = _load_yaml(presets_path)
    preset_name = (cfg.get("presets", {}) or {}).get("default", "calm_female_v1")
    preset = presets.get(preset_name) or {}
    rt = ((cfg.get("local_runtime") or {}).get("piper") or {})
    provider = PiperTTSProvider(
        command=str(rt.get("executable") or "piper"),
        enabled=bool(rt.get("enabled", True)),
        model_path=(str(rt.get("voice_path")) if rt.get("voice_path") else None),
    )
    r = provider.synthesize(text=text, preset_name=preset_name, preset=preset, timeout_ms=int((cfg.get("timeouts") or {}).get("piper_ms", 5000)))
    out = {
        "test_item": "piper_direct",
        "provider": "piper",
        "success": r.ok,
        "latency_ms": r.latency_ms,
        "audio_bytes_size": len(r.audio_bytes) if r.audio_bytes else 0,
        "failure_type": r.failure.failure_type if r.failure else None,
        "failure_reason": r.failure.reason if r.failure else None,
    }
    if r.ok and r.audio_bytes:
        wav_path = LOG_DIR / "stage22_piper.wav"
        wav_path.write_bytes(r.audio_bytes)
        out["output_path"] = str(wav_path)
    return out


def _run_unified(config_path: Path, presets_path: Path, text: str) -> Dict[str, Any]:
    req = _speech_request(text=text)
    res = run_tts_unified_entry(
        request=req,
        legacy_submit=_legacy_submit,
        config_path=str(config_path),
        presets_path=str(presets_path),
    )
    row = {
        "request_id": req.request_id,
        "success": res.ok,
        "final_execution_mode": res.final_execution_mode,
        "provider_ok": bool(res.provider_result.ok) if res.provider_result else False,
        "provider_name": res.provider_result.provider_name if res.provider_result else None,
        "provider_failure_type": (res.provider_result.failure.failure_type if (res.provider_result and res.provider_result.failure) else None),
        "selection_observation": (res.selection_observation.__dict__ if res.selection_observation else None),
        "fallback_observation": (res.fallback_observation.__dict__ if res.fallback_observation else None),
        "cutover_observation": res.cutover_observation.__dict__,
        "rollback_observation": (res.rollback_observation.__dict__ if res.rollback_observation else None),
    }
    if res.selection_observation:
        _record_obs({"request_id": req.request_id, "type": "selection", "data": res.selection_observation.__dict__})
    if res.fallback_observation:
        _record_obs({"request_id": req.request_id, "type": "fallback", "data": res.fallback_observation.__dict__})
    _record_obs({"request_id": req.request_id, "type": "cutover", "data": res.cutover_observation.__dict__})
    if res.rollback_observation:
        _record_obs({"request_id": req.request_id, "type": "rollback", "data": res.rollback_observation.__dict__})
    return row


def _tmp_cfg(base_cfg: Dict[str, Any], *, piper_exec: str | None = None, cutover_enabled: bool | None = None) -> Dict[str, Any]:
    cfg = json.loads(json.dumps(base_cfg))
    cfg.setdefault("local_runtime", {}).setdefault("piper", {})
    if piper_exec is not None:
        cfg["local_runtime"]["piper"]["executable"] = piper_exec
    if cutover_enabled is not None:
        cfg.setdefault("cutover", {})["enabled"] = cutover_enabled
    return cfg


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["piper", "rollback", "cutover_off", "all"])
    parser.add_argument("--text", default="前方十米右转。")
    args = parser.parse_args()

    config_path = ROOT / "capabilities/voice/config/voice_tts_config.yaml"
    presets_path = ROOT / "capabilities/voice/config/voice_presets.yaml"
    base_cfg = _load_yaml(config_path)

    results = []
    if args.mode in ("piper", "all"):
        results.append(mode_piper(config_path, presets_path, "前方靠近水边，请停一下。"))

    if args.mode in ("rollback", "all"):
        cfg = _tmp_cfg(base_cfg, piper_exec="/nonexistent/piper", cutover_enabled=True)
        tmp = LOG_DIR / "stage22_tmp_rollback.yaml"
        _save_yaml(tmp, cfg)
        row = _run_unified(tmp, presets_path, "我没听清，请再说一次。")
        row["test_item"] = "provider_chain_to_legacy_rollback"
        results.append(row)

    if args.mode in ("cutover_off", "all"):
        cfg = _tmp_cfg(base_cfg, piper_exec="/nonexistent/piper", cutover_enabled=False)
        tmp = LOG_DIR / "stage22_tmp_cutover_off.yaml"
        _save_yaml(tmp, cfg)
        row = _run_unified(tmp, presets_path, "当前电量低于百分之二十。")
        row["test_item"] = "cutover_disabled_legacy_direct"
        results.append(row)

    output = {"mode": args.mode, "results": results}
    out_path = LOG_DIR / "voice_stage22_validation_results.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"saved: {out_path}")
    print(f"obs: {OBS_PATH}")


if __name__ == "__main__":
    main()
