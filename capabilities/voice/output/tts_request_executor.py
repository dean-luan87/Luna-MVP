# -*- coding: utf-8 -*-
"""
TTS request executor (Stage-2).

说明：
- 只负责读取配置/预设、调用 provider chain、返回结构化结果
- Stage-2 不做播放接线（不调用 speech_gate/audio_worker）
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from capabilities.model_paths_v1 import resolve_model_path, resolve_preset_model_params
from capabilities.voice.output.tts_provider_runtime import TTSProviderResult
from capabilities.voice.providers.piper_tts_provider import PiperTTSProvider
from capabilities.voice.providers.tts_fallback_manager import TTSChainResult
from capabilities.voice.providers.tts_provider_selector import execute_provider_chain
from capabilities.voice.schemas.speech_request import SpeechRequest


@dataclass(frozen=True)
class TTSExecutionOutcome:
    ok: bool
    chain: TTSChainResult


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        return {}
    return data


def execute_tts_request(
    *,
    request: SpeechRequest,
    config_path: str = "capabilities/voice/config/voice_tts_config.yaml",
    presets_path: str = "capabilities/voice/config/voice_presets.yaml",
) -> TTSExecutionOutcome:
    cfg = _load_yaml(Path(config_path))
    presets = _load_yaml(Path(presets_path))

    preset_name = (request.metadata.get("preset") if isinstance(request.metadata, dict) else None) or cfg.get("presets", {}).get("default", "calm_female_v1")
    preset = presets.get(preset_name) if isinstance(presets, dict) else None
    if not isinstance(preset, dict):
        preset = {}
    preset = resolve_preset_model_params(preset)

    provider_order = cfg.get("provider_order") or ["piper"]
    if not isinstance(provider_order, list):
        provider_order = ["piper"]

    active_provider = cfg.get("active_provider") or "piper"
    fallback_provider = cfg.get("fallback_provider") or "piper"
    fallback_enabled = bool((cfg.get("fallback") or {}).get("enabled", True))
    timeouts = cfg.get("timeouts") or {"piper_ms": 4000, "qwen_ms": 4000}

    local_runtime = cfg.get("local_runtime") if isinstance(cfg.get("local_runtime"), dict) else {}
    piper_rt = local_runtime.get("piper") if isinstance(local_runtime.get("piper"), dict) else {}

    def _resolved(ref: Optional[str]) -> Optional[str]:
        if not ref:
            return None
        path = resolve_model_path(str(ref))
        return str(path) if path is not None else str(ref)

    providers = {
        "piper": PiperTTSProvider(
            command=str(piper_rt.get("executable") or "piper"),
            enabled=bool(piper_rt.get("enabled", True)),
            model_path=_resolved(piper_rt.get("voice_path")),
        ),
    }

    chain = execute_provider_chain(
        request_id=request.request_id,
        text=request.text_candidate,
        preset_name=preset_name,
        preset=preset,
        provider_order=[str(x) for x in provider_order],
        active_provider=str(active_provider),
        fallback_provider=str(fallback_provider),
        providers=providers,
        timeouts_ms={str(k): int(v) for k, v in (timeouts.items() if isinstance(timeouts, dict) else [])},
        fallback_enabled=fallback_enabled,
    )
    return TTSExecutionOutcome(ok=chain.ok, chain=chain)
