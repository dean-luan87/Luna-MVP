# -*- coding: utf-8 -*-
"""
Qwen / Qianwen TTS provider adapter (Stage-2).

Hard boundaries:
- Only text -> audio_bytes (TTS). Never generates text content.
- Never plays audio directly; returns audio_bytes for the unified chain.
- Fail-closed: on any error returns structured failure for fallback.
"""

from __future__ import annotations

import base64
import os
import time
from typing import Dict, Optional

from capabilities.voice.output.tts_provider_runtime import TTSFailure, TTSProviderResult
from capabilities.voice.tts_model_constants_v0 import (
    DEFAULT_TTS_MODEL,
    emit_tts_model_warnings,
    resolve_tts_model,
)


class QwenTTSProvider:
    name = "qwen"

    @staticmethod
    def _safe_getattr(obj, name: str, default=None):
        try:
            return getattr(obj, name, default)
        except Exception:
            return default

    def __init__(
        self,
        *,
        enabled: bool = True,
        api_key_env: str = "DASHSCOPE_API_KEY",
        model: str = DEFAULT_TTS_MODEL,
        voice: str = "Serena",
        sample_rate: int = 16000,
        audio_format: str = "wav",
        requires_network: bool = True,
        speed: Optional[float] = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._api_key_env = str(api_key_env or "DASHSCOPE_API_KEY")
        resolved = resolve_tts_model(explicit=model)
        emit_tts_model_warnings(resolved)
        self._model = str(resolved.model or DEFAULT_TTS_MODEL)
        self._voice = str(voice or "Serena")
        self._sample_rate = int(sample_rate or 16000)
        self._format = str(audio_format or "wav")
        self._requires_network = bool(requires_network)
        self._speed = float(speed) if speed is not None else None

    @staticmethod
    def _extract_audio_bytes(response) -> Optional[bytes]:
        """
        Extract bytes from dashscope response with multiple shapes.
        """
        if response is None:
            return None
        status_code = QwenTTSProvider._safe_getattr(response, "status_code", None)
        if status_code != 200:
            return None

        out = QwenTTSProvider._safe_getattr(response, "output", None)

        # response.output may be an object (attr) or a dict-like (keys).
        # IMPORTANT: some SDK objects raise KeyError on missing attributes; never let it escape.
        if out is not None:
            # object style: response.output.audio (guard against KeyError/TypeError)
            try:
                audio_data = getattr(out, "audio", None)
            except Exception:
                audio_data = None
            if audio_data is not None:
                audio = QwenTTSProvider._process_audio_data(audio_data)
                if audio:
                    return audio

            # dict style: response.output["audio"] / ["audios"]
            if isinstance(out, dict) or hasattr(out, "keys"):
                try:
                    out_dict = dict(out) if not isinstance(out, dict) else out
                except Exception:
                    out_dict = None
                if isinstance(out_dict, dict):
                    out = out_dict
                for k in ("audio", "audios", "data", "content", "binary"):
                    if k in out:
                        audio = QwenTTSProvider._process_audio_data(out.get(k))
                        if audio:
                            return audio

                # sometimes nested: output={"result": {...}}
                for k in ("result", "output"):
                    if k in out and isinstance(out.get(k), dict):
                        sub = out.get(k) or {}
                        for kk in ("audio", "audios", "data", "content", "binary"):
                            if kk in sub:
                                audio = QwenTTSProvider._process_audio_data(sub.get(kk))
                                if audio:
                                    return audio

        # response.audio
        audio_data2 = QwenTTSProvider._safe_getattr(response, "audio", None)
        if audio_data2 is not None:
            return QwenTTSProvider._process_audio_data(audio_data2)

        return None

    @staticmethod
    def _process_audio_data(audio_data) -> Optional[bytes]:
        if audio_data is None:
            return None
        if isinstance(audio_data, bytes):
            return audio_data
        if isinstance(audio_data, bytearray):
            return bytes(audio_data)
        if isinstance(audio_data, memoryview):
            try:
                return audio_data.tobytes()
            except Exception:
                return None
        if isinstance(audio_data, str):
            if audio_data.strip().lower().startswith(("http://", "https://")):
                return None
            try:
                return base64.b64decode(audio_data)
            except Exception:
                return None
        if isinstance(audio_data, list):
            if audio_data and all(isinstance(x, int) for x in audio_data[: min(16, len(audio_data))]):
                try:
                    return bytes(audio_data)
                except Exception:
                    return None
            for item in audio_data[:3]:
                audio = QwenTTSProvider._process_audio_data(item)
                if audio:
                    return audio
            return None
        if isinstance(audio_data, dict):
            for key in ["audio", "audios", "data", "content", "binary", "sound", "voice", "wav", "pcm"]:
                if key in audio_data:
                    v = audio_data[key]
                    if isinstance(v, bytes):
                        return v
                    if isinstance(v, str):
                        if v.strip().lower().startswith(("http://", "https://")):
                            return None
                        try:
                            return base64.b64decode(v)
                        except Exception:
                            continue
            # list-like audio container
            for key in ["audios", "items", "results"]:
                v = audio_data.get(key)
                if isinstance(v, list) and v:
                    for item in v[:3]:
                        audio = QwenTTSProvider._process_audio_data(item)
                        if audio:
                            return audio
            for key in ["url", "audio_url", "download_url"]:
                v = audio_data.get(key)
                if isinstance(v, str) and v.strip().lower().startswith(("http://", "https://")):
                    return None
            return None
        for key in ["audio", "data", "content", "binary", "wav", "pcm"]:
            v = QwenTTSProvider._safe_getattr(audio_data, key, None)
            if v is None:
                continue
            audio = QwenTTSProvider._process_audio_data(v)
            if audio:
                return audio
        return None

    @staticmethod
    def _response_shape_hint(resp) -> Dict:
        """
        Best-effort, privacy-safe hint for debugging response structure when audio is missing.
        Never includes full payload; only types/keys and truncated strings.
        """
        try:
            out = QwenTTSProvider._safe_getattr(resp, "output", None)
            hint = {
                "resp_type": type(resp).__name__,
                "status_code": QwenTTSProvider._safe_getattr(resp, "status_code", None),
                "message": (str(QwenTTSProvider._safe_getattr(resp, "message", ""))[:200] if QwenTTSProvider._safe_getattr(resp, "message", None) is not None else None),
                "has_audio_attr": QwenTTSProvider._safe_getattr(resp, "audio", None) is not None,
                "output_type": (type(out).__name__ if out is not None else None),
            }
            if isinstance(out, dict):
                hint["output_keys"] = sorted([str(k) for k in out.keys()])[:50]
                try:
                    av = out.get("audio")
                    hint["output_audio_type"] = type(av).__name__ if av is not None else None
                    if isinstance(av, (bytes, bytearray, memoryview)):
                        hint["output_audio_size"] = len(av)
                    elif isinstance(av, str):
                        hint["output_audio_str_prefix"] = av[:120]
                    elif isinstance(av, list):
                        hint["output_audio_list_len"] = len(av)
                    elif isinstance(av, dict):
                        hint["output_audio_keys"] = sorted([str(k) for k in av.keys()])[:50]
                        # include shallow types for top-level keys only
                        hint["output_audio_value_types"] = {
                            str(k): type(av.get(k)).__name__ for k in list(av.keys())[:20]
                        }
                except Exception as e:
                    hint["output_audio_inspect_error"] = repr(e)
            else:
                # object-ish: list some public attrs
                try:
                    attrs = [a for a in dir(out) if a and not a.startswith("_")] if out is not None else []
                    hint["output_attrs"] = sorted(attrs)[:50]
                except Exception:
                    hint["output_attrs"] = None
            return hint
        except Exception as e:
            return {"shape_hint_error": repr(e)}

    def synthesize(self, *, text: str, preset_name: str, preset: Dict, timeout_ms: int) -> TTSProviderResult:
        start = time.time()
        if not self._enabled:
            return TTSProviderResult(
                ok=False,
                provider_name=self.name,
                preset_name=preset_name,
                failure=TTSFailure(
                    failure_type="not_available",
                    reason="QWEN_PROVIDER_DISABLED",
                    detail={"requires_network": self._requires_network, "api_key_env": self._api_key_env},
                ),
                latency_ms=0,
            )
        if not text or not text.strip():
            return TTSProviderResult(
                ok=False,
                provider_name=self.name,
                preset_name=preset_name,
                failure=TTSFailure(failure_type="invalid_audio", reason="EMPTY_TEXT"),
                latency_ms=0,
            )

        api_key = os.getenv(self._api_key_env, "").strip()
        if not api_key:
            latency_ms = int((time.time() - start) * 1000)
            return TTSProviderResult(
                ok=False,
                provider_name=self.name,
                preset_name=preset_name,
                failure=TTSFailure(
                    failure_type="not_available",
                    reason="QWEN_API_KEY_MISSING",
                    detail={"api_key_env": self._api_key_env, "requires_network": self._requires_network},
                ),
                latency_ms=latency_ms,
            )

        # Lazy import dashscope so missing deps does not crash the mainline.
        try:
            import dashscope  # type: ignore
            from dashscope.audio.qwen_tts import SpeechSynthesizer  # type: ignore
        except Exception as e:
            latency_ms = int((time.time() - start) * 1000)
            return TTSProviderResult(
                ok=False,
                provider_name=self.name,
                preset_name=preset_name,
                failure=TTSFailure(
                    failure_type="not_available",
                    reason="QWEN_DASHSCOPE_IMPORT_FAILED",
                    detail={"error": repr(e), "requires_network": self._requires_network},
                ),
                latency_ms=latency_ms,
            )

        # Optional preset overrides (still TTS-only).
        mp = preset.get("model_params") or {}
        model = str(mp.get("qwen_model") or self._model)
        voice = str(mp.get("qwen_voice") or self._voice)
        sample_rate = int(mp.get("qwen_sample_rate") or self._sample_rate)
        audio_format = str(mp.get("qwen_audio_format") or self._format)
        speed = mp.get("qwen_speed")
        if speed is None:
            speed = self._speed
        try:
            speed = float(speed) if speed is not None else None
        except Exception:
            speed = None

        try:
            dashscope.api_key = api_key
            synth = SpeechSynthesizer()
            # dashscope SpeechSynthesizer.call() signature differs across versions:
            # some versions expect `text=...`, others expect `input=...`.
            try:
                call_kwargs = dict(
                    model=model,
                    text=text,
                    voice=voice,
                    format=audio_format,
                    sample_rate=sample_rate,
                    result_format="bytes",
                )
                # speed parameter name differs by SDK/version; try a few.
                if speed is not None:
                    for k in ("speed", "speech_rate", "rate"):
                        try:
                            resp = synth.call(**{**call_kwargs, k: speed})
                            break
                        except TypeError:
                            resp = None  # type: ignore[assignment]
                    if resp is None:
                        resp = synth.call(**call_kwargs)
                else:
                    resp = synth.call(**call_kwargs)
            except TypeError:
                call_kwargs = dict(
                    model=model,
                    input=text,
                    voice=voice,
                    format=audio_format,
                    sample_rate=sample_rate,
                    result_format="bytes",
                )
                if speed is not None:
                    for k in ("speed", "speech_rate", "rate"):
                        try:
                            resp = synth.call(**{**call_kwargs, k: speed})
                            break
                        except TypeError:
                            resp = None  # type: ignore[assignment]
                    if resp is None:
                        resp = synth.call(**call_kwargs)
                else:
                    resp = synth.call(**call_kwargs)
            audio = self._extract_audio_bytes(resp)
            latency_ms = int((time.time() - start) * 1000)
            # If SDK returns audio as {data,url,...} but extractor didn't catch it,
            # attempt to decode data or download from url (online experimental only).
            if (not audio) or (len(audio) < 64):
                try:
                    out = self._safe_getattr(resp, "output", None)
                    out_dict = None
                    if isinstance(out, dict) or hasattr(out, "keys"):
                        try:
                            out_dict = dict(out) if not isinstance(out, dict) else out
                        except Exception:
                            out_dict = None
                    audio_obj = None
                    if isinstance(out_dict, dict):
                        audio_obj = out_dict.get("audio")
                    # decode base64 in audio.data if present
                    if isinstance(audio_obj, dict):
                        data_s = audio_obj.get("data")
                        if isinstance(data_s, str) and data_s.strip():
                            try:
                                b = base64.b64decode(data_s)
                                if b and len(b) >= 64:
                                    audio = b
                            except Exception:
                                pass
                        # if still no audio, try download from url
                        if (not audio) or (len(audio) < 64):
                            url = audio_obj.get("url")
                            if isinstance(url, str) and url.strip().lower().startswith(("http://", "https://")):
                                # lazy import requests (already a transitive dep in most envs)
                                try:
                                    import requests  # type: ignore

                                    r = requests.get(url, timeout=max(1.0, float(timeout_ms) / 1000.0))
                                    if r.status_code == 200 and r.content and len(r.content) >= 64:
                                        audio = bytes(r.content)
                                except Exception:
                                    pass
                except Exception:
                    pass

            if not audio or len(audio) < 64:
                status_code = getattr(resp, "status_code", None)
                msg = getattr(resp, "message", None)
                return TTSProviderResult(
                    ok=False,
                    provider_name=self.name,
                    preset_name=preset_name,
                    failure=TTSFailure(
                        failure_type="invalid_audio",
                        reason="QWEN_EMPTY_OR_INVALID_AUDIO",
                        detail={
                            "status_code": status_code,
                            "message": str(msg)[:300] if msg is not None else None,
                            "model": model,
                            "voice": voice,
                            "format": audio_format,
                            "sample_rate": sample_rate,
                            "speed": speed,
                            "requires_network": self._requires_network,
                            "response_shape_hint": self._response_shape_hint(resp),
                        },
                    ),
                    latency_ms=latency_ms,
                )
            return TTSProviderResult(
                ok=True,
                provider_name=self.name,
                preset_name=preset_name,
                audio_bytes=audio,
                latency_ms=latency_ms,
            )
        except Exception as e:
            latency_ms = int((time.time() - start) * 1000)
            return TTSProviderResult(
                ok=False,
                provider_name=self.name,
                preset_name=preset_name,
                failure=TTSFailure(
                    failure_type="exception",
                    reason="QWEN_TTS_EXCEPTION",
                    detail={
                        "error": repr(e),
                        "speed": speed,
                        "requires_network": self._requires_network,
                        "response_shape_hint": self._response_shape_hint(resp) if "resp" in locals() and resp is not None else None,
                    },
                ),
                latency_ms=latency_ms,
            )

