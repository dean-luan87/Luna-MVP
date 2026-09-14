# -*- coding: utf-8 -*-
"""
Voice providers interfaces (Stage-0 placeholder).

目标：固化 Voice 能力板块的 provider 边界（ASR/TTS/VoiceInput）。
禁止：在此处实现具体厂商逻辑。
"""

from __future__ import annotations

from typing import Optional, Protocol

from capabilities.voice.schemas.voice_event import VoiceEvent


class VoiceInputProvider(Protocol):
    """提供语音输入流（如麦克风/文件/网络流）。"""

    def read_chunk(self) -> bytes:
        """读取一段原始音频数据（格式由 adapter/provider 自己定义）。"""


class ASRProvider(Protocol):
    """ASR：音频 -> 文本事件。"""

    name: str
    model_name: str

    def transcribe(self, audio_bytes: bytes, *, is_final: bool = True) -> VoiceEvent:
        """将音频转为 VoiceEvent（文本/置信度等）。"""


class TTSProvider(Protocol):
    """TTS：文本 -> 播放/音频输出。"""

    name: str
    model_name: str

    def synthesize(self, text: str) -> bytes:
        """合成音频 bytes（编码/采样率由 provider 定义）。"""

    def play(self, audio_bytes: bytes) -> None:
        """播放音频（可选能力）。"""

    def say(self, text: str) -> None:
        """便捷播报（可直接走 synthesize+play，或 provider 内部实现）。"""


class VoiceDialogueBridge(Protocol):
    """
    Voice <-> Core 对话桥接（Stage-0 占位）。

    约束：桥接只负责把 VoiceEvent 适配成 Core 可消费的输入形态；
    不得把语音能力逻辑写进 Core。
    """

    def on_voice_event(self, event: VoiceEvent) -> None:
        """将 VoiceEvent 交给上层（Core/controller/session）处理。"""

    def current_session_id(self) -> Optional[str]:
        """返回当前会话 id（若有）。"""

