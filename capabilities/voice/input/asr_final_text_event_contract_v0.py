# -*- coding: utf-8 -*-
"""
ASRFinalTextEventV0 — ASR → final_text 事件合同（Phase-VoiceInteraction-Readiness-002）。

边界：
- 仅定义 schema / 序列化形状；本文件不调用任何 ASR / Qianwen / TTS / playback。
- normalized_text 可为 null；语义改写不在本阶段执行；text 原文必须保留。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Literal, Optional

# --- Literals (contract vocabulary) ---

ASRFinalTextEventTypeV0 = Literal["voice.asr.final_text"]

LanguageCodeV0 = Literal["zh", "en", "mixed", "unknown"]

ASRStatusV0 = Literal[
    "final",
    "no_speech",
    "timeout",
    "cancelled",
    "provider_error",
    "low_confidence",
]


@dataclass
class ASRFinalTextHardAuditV0:
    """ASR 侧硬审计：证明本事件路径未触碰下游禁区。"""

    qianwen_invoked: bool = False
    tts_invoked: bool = False
    playback_invoked: bool = False
    navigation_action: Optional[str] = None
    midplatform_invoked: bool = False
    world_write_invoked: bool = False


@dataclass
class ASRFinalTextEventV0:
    """
    单次 utterance 的最终（或终结性）ASR 结果载体。

    is_final：协议层「本事件是否为终结帧」；与 asr_status 组合使用。
    asr_status == final 且进入 final_text_ready 状态机后，才允许进入语义 / Qianwen（见状态机文档）。
    """

    event_id: str
    event_type: ASRFinalTextEventTypeV0 = "voice.asr.final_text"
    request_id: str = ""
    trace_id: str = ""
    session_id: str = ""
    utterance_id: str = ""
    source_audio_ref: str = ""
    provider_id: str = ""
    language: LanguageCodeV0 = "unknown"
    text: str = ""
    normalized_text: Optional[str] = None
    confidence: float = 0.0
    is_final: bool = True
    asr_status: ASRStatusV0 = "final"
    latency_ms: int = 0
    hard_audit: ASRFinalTextHardAuditV0 = field(default_factory=ASRFinalTextHardAuditV0)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d


def asr_final_text_event_json_schema_fields_v0() -> Dict[str, Any]:
    """供只读 review 工具导出 voice_asr_final_text_event_schema.json。"""
    return {
        "schema_id": "voice.asr.final_text_event_v0",
        "event_type_const": "voice.asr.final_text",
        "fields": {
            "event_id": {"type": "string", "required": True},
            "event_type": {"type": "string", "const": "voice.asr.final_text", "required": True},
            "request_id": {"type": "string", "required": True},
            "trace_id": {"type": "string", "required": True},
            "session_id": {"type": "string", "required": True},
            "utterance_id": {"type": "string", "required": True},
            "source_audio_ref": {"type": "string", "required": True},
            "provider_id": {"type": "string", "required": True},
            "language": {"enum": ["zh", "en", "mixed", "unknown"], "required": True},
            "text": {"type": "string", "required": True, "note": "原文必须保留"},
            "normalized_text": {"type": ["string", "null"], "required": False},
            "confidence": {"type": "number", "required": True},
            "is_final": {"type": "boolean", "required": True},
            "asr_status": {
                "enum": ["final", "no_speech", "timeout", "cancelled", "provider_error", "low_confidence"],
                "required": True,
            },
            "latency_ms": {"type": "integer", "required": True},
            "hard_audit": {
                "type": "object",
                "required": True,
                "properties": {
                    "qianwen_invoked": {"type": "boolean"},
                    "tts_invoked": {"type": "boolean"},
                    "playback_invoked": {"type": "boolean"},
                    "navigation_action": {"type": ["string", "null"]},
                    "midplatform_invoked": {"type": "boolean"},
                    "world_write_invoked": {"type": "boolean"},
                },
            },
        },
    }


def example_asr_final_text_event_v0() -> Dict[str, Any]:
    """示例负载（占位符字符串）；不触发任何外部调用。"""
    ev = ASRFinalTextEventV0(
        event_id="evt_asr_example_001",
        request_id="req_example_001",
        trace_id="trace_example_001",
        session_id="sess_example_001",
        utterance_id="utt_example_001",
        source_audio_ref="audio_ref://session/utt/wav_placeholder",
        provider_id="mock_asr",
        language="zh",
        text="示例原文",
        normalized_text=None,
        confidence=0.92,
        is_final=True,
        asr_status="final",
        latency_ms=120,
    )
    return ev.to_dict()


__all__ = [
    "ASRFinalTextEventV0",
    "ASRFinalTextHardAuditV0",
    "ASRStatusV0",
    "LanguageCodeV0",
    "asr_final_text_event_json_schema_fields_v0",
    "example_asr_final_text_event_v0",
]
