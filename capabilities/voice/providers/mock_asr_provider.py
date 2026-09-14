# -*- coding: utf-8 -*-
"""
最小 ASR 占位实现：音频 bytes 按 UTF-8 解码为文本（测试/模拟），或空串。

真实 ASR 应实现 interfaces.asr_provider.ASRProvider，禁止业务侧散点直调。
"""

from __future__ import annotations

import uuid

from capabilities.voice.schemas.voice_input_event import VoiceInputEvent


class MockASRProvider:
    """骨架 provider：name/model 固定；transcribe 产出最小 VoiceInputEvent。"""

    name: str = "mock_asr"
    model_name: str = "mock_v1"

    def transcribe(self, *, audio_bytes: bytes, is_final: bool = True) -> VoiceInputEvent:
        try:
            text = audio_bytes.decode("utf-8").strip()
        except (UnicodeDecodeError, AttributeError):
            text = ""
        eid = str(uuid.uuid4())
        return VoiceInputEvent(
            event_id=eid,
            request_id=eid,
            timestamp=0.0,
            session_id="",
            turn_id="",
            source="mock_asr",
            text=text or None,
            raw_text=text or None,
            normalized_text=text or None,
            is_final=is_final,
            provider_name=self.name,
            model_name=self.model_name,
            source_type="asr",
            router_decision="pending_pipeline",
        )
