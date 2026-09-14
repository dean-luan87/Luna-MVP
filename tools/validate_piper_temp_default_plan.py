#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务 A：通过统一入口验证 Piper 临时主链方案。
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capabilities.voice.runtime.tts_unified_entry import run_tts_unified_entry
from capabilities.voice.schemas.speech_request import SpeechRequest
from modules.voice import Voice


LOG_DIR = ROOT / "logs" / "piper_temp_plan"
LOG_DIR.mkdir(parents=True, exist_ok=True)

RESULT_JSON = ROOT / "logs" / "piper_temp_default_validation.json"
OBS_JSONL = ROOT / "logs" / "piper_temp_default_observations.jsonl"


def _save_yaml(path: Path, obj: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(obj, f, allow_unicode=True, sort_keys=False)


def _legacy_submit(text: str) -> bool:
    return Voice().speak(text)


def _append_obs(kind: str, data: Dict[str, Any], request_id: str) -> None:
    with OBS_JSONL.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {"request_id": request_id, "type": kind, "data": data},
                ensure_ascii=False,
            )
            + "\n"
        )


def _make_request(text: str, preset: str, scene: str) -> SpeechRequest:
    return SpeechRequest(
        request_id=f"piper_temp_{scene}_{int(time.time() * 1000)}",
        source_module="validate_piper_temp_default_plan",
        output_category="interaction_result",
        text_candidate=text,
        priority=1,
        interruptible=True,
        dedup_allowed=True,
        cooldown_key=f"piper_temp_{scene}",
        metadata={"preset": preset, "scene": scene},
    )


def _write_wav(path: Path, audio: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(audio)


def main() -> None:
    cfg_path = LOG_DIR / "voice_tts_config_piper_temp.yaml"
    presets_path = LOG_DIR / "voice_tts_presets_piper_temp.yaml"

    model = "speech/tts/piper/zh_CN-huayan-medium.onnx"
    base_exec = "/Users/luanlei/Library/Python/3.9/bin/piper"

    cfg = {
        "active_provider": "piper",
        "fallback_provider": "piper",
        "provider_order": ["piper"],
        "fallback": {"enabled": True},
        "timeouts": {"piper_ms": 6000},
        "cutover": {
            "enabled": True,
            "mode": "provider_chain_first",
            "rollback_to_legacy_on_failure": True,
            "rollback_on_selector_failure": True,
            "rollback_on_provider_chain_failure": True,
            "observe_rollbacks": True,
        },
        "legacy_fallback": {
            "enabled": True,
            "mode": "current_main_chain",
            "reason_tag": "legacy_voice_runtime",
        },
        "presets": {
            "default": "calm_female_v1",
            "available": [
                "calm_female_v1",
                "navigation_clear_v1",
                "warning_strong_v1",
                "gentle_companion_v1",
            ],
        },
        "local_runtime": {
            "piper": {
                "executable": base_exec,
                "voice_path": model,
                "enabled": True,
            },
        },
    }

    presets = {
        "calm_female_v1": {
            "provider": "piper",
            "model_params": {
                "model": model,
                "length_scale": 1.0,
                "sentence_silence": 0.15,
                "noise_scale": 0.667,
                "noise_w_scale": 0.8,
                "volume": 1.0,
            },
            "intended_use": "default",
        },
        "navigation_clear_v1": {
            "provider": "piper",
            "model_params": {
                "model": model,
                "length_scale": 0.92,
                "sentence_silence": 0.12,
                "noise_scale": 0.60,
                "noise_w_scale": 0.75,
                "volume": 1.05,
            },
            "intended_use": "navigation",
        },
        "warning_strong_v1": {
            "provider": "piper",
            "model_params": {
                "model": model,
                "length_scale": 0.86,
                "sentence_silence": 0.08,
                "noise_scale": 0.65,
                "noise_w_scale": 0.85,
                "volume": 1.12,
            },
            "intended_use": "safety",
        },
        "gentle_companion_v1": {
            "provider": "piper",
            "model_params": {
                "model": model,
                "length_scale": 1.05,
                "sentence_silence": 0.18,
                "noise_scale": 0.62,
                "noise_w_scale": 0.78,
                "volume": 0.98,
            },
            "intended_use": "feedback",
        },
    }

    _save_yaml(cfg_path, cfg)
    _save_yaml(presets_path, presets)

    cases: List[Tuple[str, str, str]] = [
        ("navigation", "navigation_clear_v1", "前方十米右转。"),
        ("navigation", "navigation_clear_v1", "请沿当前方向继续前进。"),
        ("warning", "warning_strong_v1", "前方靠近水边，请停一下。"),
        ("warning", "warning_strong_v1", "前面人多，请减速靠右。"),
        ("feedback", "calm_female_v1", "已开始导航。"),
        ("feedback", "gentle_companion_v1", "我没听清，请再说一次。"),
        ("feedback", "calm_female_v1", "已暂停当前任务。"),
    ]

    rows: List[Dict[str, Any]] = []
    for scene, preset, text in cases:
        req = _make_request(text=text, preset=preset, scene=scene)
        result = run_tts_unified_entry(
            request=req,
            legacy_submit=_legacy_submit,
            config_path=str(cfg_path),
            presets_path=str(presets_path),
        )
        row: Dict[str, Any] = {
            "request_id": req.request_id,
            "scene": scene,
            "preset": preset,
            "text": text,
            "ok": result.ok,
            "final_execution_mode": result.final_execution_mode,
            "provider_name": result.provider_result.provider_name if result.provider_result else None,
            "provider_latency_ms": result.provider_result.latency_ms if result.provider_result else None,
            "provider_failure_type": (
                result.provider_result.failure.failure_type
                if result.provider_result and result.provider_result.failure
                else None
            ),
            "selection_observation": result.selection_observation.__dict__ if result.selection_observation else None,
            "fallback_observation": result.fallback_observation.__dict__ if result.fallback_observation else None,
            "cutover_observation": result.cutover_observation.__dict__,
            "rollback_observation": result.rollback_observation.__dict__ if result.rollback_observation else None,
        }
        if result.provider_result and result.provider_result.ok and result.provider_result.audio_bytes:
            out = LOG_DIR / scene / f"{preset}_{req.request_id}.wav"
            _write_wav(out, result.provider_result.audio_bytes)
            row["audio_path"] = str(out)
            row["audio_bytes"] = len(result.provider_result.audio_bytes)
        rows.append(row)

        if result.selection_observation:
            _append_obs("selection", result.selection_observation.__dict__, req.request_id)
        if result.fallback_observation:
            _append_obs("fallback", result.fallback_observation.__dict__, req.request_id)
        _append_obs("cutover", result.cutover_observation.__dict__, req.request_id)
        if result.rollback_observation:
            _append_obs("rollback", result.rollback_observation.__dict__, req.request_id)

    summary = {
        "generated_at": int(time.time()),
        "config_path": str(cfg_path),
        "presets_path": str(presets_path),
        "total": len(rows),
        "success_count": sum(1 for r in rows if r["ok"]),
        "provider_chain_count": sum(1 for r in rows if r["final_execution_mode"] == "provider_chain"),
        "legacy_fallback_count": sum(1 for r in rows if r["final_execution_mode"] == "legacy_fallback"),
        "rows": rows,
    }
    RESULT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"saved result: {RESULT_JSON}")
    print(f"saved obs: {OBS_JSONL}")


if __name__ == "__main__":
    main()

