# -*- coding: utf-8 -*-
"""
Piper TTS provider adapter (Stage-2).

定位：稳定兜底（fallback provider）。
注意：Stage-2 不做设备运维治理，仅做本地调用 + 结构化失败。
"""

from __future__ import annotations

import subprocess
import time
from typing import Dict, Optional

from capabilities.voice.output.tts_provider_runtime import TTSFailure, TTSProviderResult


class PiperTTSProvider:
    name = "piper"

    def __init__(self, *, command: str = "piper", enabled: bool = True, model_path: Optional[str] = None) -> None:
        self._command = command
        self._enabled = enabled
        self._model_path = model_path

    def synthesize(self, *, text: str, preset_name: str, preset: Dict, timeout_ms: int) -> TTSProviderResult:
        start = time.time()
        if not self._enabled:
            return TTSProviderResult(
                ok=False,
                provider_name=self.name,
                preset_name=preset_name,
                failure=TTSFailure(failure_type="not_available", reason="PIPER_PROVIDER_DISABLED"),
                latency_ms=0,
            )
        if not text.strip():
            return TTSProviderResult(
                ok=False,
                provider_name=self.name,
                preset_name=preset_name,
                failure=TTSFailure(failure_type="invalid_audio", reason="EMPTY_TEXT"),
                latency_ms=0,
            )

        # Piper 常见用法：echo "text" | piper --model <path> --output_file -
        model = None
        model_params = preset.get("model_params") or {}
        if isinstance(model_params, dict):
            model = model_params.get("model")
        if not model:
            model = self._model_path

        cmd = [self._command]
        if not model:
            return TTSProviderResult(
                ok=False,
                provider_name=self.name,
                preset_name=preset_name,
                failure=TTSFailure(failure_type="config_error", reason="PIPER_MODEL_NOT_CONFIGURED"),
                latency_ms=0,
            )
        cmd += ["--model", str(model)]
        # 最小参数映射：仅接收受控的 preset model_params 字段
        if isinstance(model_params, dict):
            if model_params.get("length_scale") is not None:
                cmd += ["--length-scale", str(model_params.get("length_scale"))]
            # sentence_silence>0 在 zh_CN Piper + stdin 路径下会在尾部产生持续杂音，仅传正值
            ss = model_params.get("sentence_silence")
            if ss is not None and float(ss) > 0:
                cmd += ["--sentence-silence", str(ss)]
            if model_params.get("noise_scale") is not None:
                cmd += ["--noise-scale", str(model_params.get("noise_scale"))]
            if model_params.get("noise_w_scale") is not None:
                cmd += ["--noise-w-scale", str(model_params.get("noise_w_scale"))]
            if model_params.get("volume") is not None:
                cmd += ["--volume", str(model_params.get("volume"))]
        cmd += ["--output_file", "-"]

        try:
            p = subprocess.run(
                cmd,
                input=text.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=max(0.001, timeout_ms / 1000.0),
                check=False,
            )
            latency_ms = int((time.time() - start) * 1000)
            if p.returncode != 0:
                return TTSProviderResult(
                    ok=False,
                    provider_name=self.name,
                    preset_name=preset_name,
                    failure=TTSFailure(
                        failure_type="exception",
                        reason="PIPER_NONZERO_EXIT",
                        detail={"returncode": p.returncode, "stderr": p.stderr.decode("utf-8", errors="ignore")[:200]},
                    ),
                    latency_ms=latency_ms,
                )
            audio = p.stdout
            if not audio:
                return TTSProviderResult(
                    ok=False,
                    provider_name=self.name,
                    preset_name=preset_name,
                    failure=TTSFailure(failure_type="invalid_audio", reason="EMPTY_AUDIO"),
                    latency_ms=latency_ms,
                )
            return TTSProviderResult(
                ok=True,
                provider_name=self.name,
                preset_name=preset_name,
                audio_bytes=audio,
                latency_ms=latency_ms,
            )
        except subprocess.TimeoutExpired:
            latency_ms = int((time.time() - start) * 1000)
            return TTSProviderResult(
                ok=False,
                provider_name=self.name,
                preset_name=preset_name,
                failure=TTSFailure(failure_type="timeout", reason="PIPER_TIMEOUT"),
                latency_ms=latency_ms,
            )
        except FileNotFoundError:
            latency_ms = int((time.time() - start) * 1000)
            return TTSProviderResult(
                ok=False,
                provider_name=self.name,
                preset_name=preset_name,
                failure=TTSFailure(failure_type="not_available", reason="PIPER_BINARY_NOT_FOUND"),
                latency_ms=latency_ms,
            )
        except Exception as e:
            latency_ms = int((time.time() - start) * 1000)
            return TTSProviderResult(
                ok=False,
                provider_name=self.name,
                preset_name=preset_name,
                failure=TTSFailure(failure_type="exception", reason="PIPER_EXCEPTION", detail={"error": str(e)}),
                latency_ms=latency_ms,
            )

