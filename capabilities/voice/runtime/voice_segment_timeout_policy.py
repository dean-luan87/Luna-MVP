# -*- coding: utf-8 -*-
"""
语音静默切段策略：静默超过固定秒数视为「当前一句/当前轮」结束。

仅定义输入切段规则，不实现会话窗口（30s）逻辑；会话窗口见 voice_wake_window_manager。
三套时间机制分离与四态状态机见 LUNA_VOICE_TIME_GOVERNANCE_V1.md。
"""

from __future__ import annotations

# v1 固定：语音停止超过该秒数，当前轮可送处理（与会话窗口无关）
DEFAULT_SEGMENT_END_SILENCE_SEC = 3.0


class VoiceSegmentTimeoutPolicy:
    """可配置切段阈值；默认 3 秒。"""

    def __init__(self, segment_end_silence_sec: float = DEFAULT_SEGMENT_END_SILENCE_SEC) -> None:
        self.segment_end_silence_sec = float(segment_end_silence_sec)

    def is_segment_end(self, silence_duration_sec: float) -> bool:
        """静默时长是否已达「当前句结束」。"""
        return silence_duration_sec >= self.segment_end_silence_sec
