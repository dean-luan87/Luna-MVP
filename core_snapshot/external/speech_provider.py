# -*- coding: utf-8 -*-
"""
Phase 2.2: SpeechProvider — 事件型，只产离散 event token 与 produced_ts。
不输出原始 ASR 文本；不触发 SPEAK/WAIT/YIELD，只产事件。
"""
from typing import Tuple

from .base_provider import ExternalProvider

SPEECH_EVENT_TOKENS = frozenset({
    "STOP_COMMAND", "HELP_REQUEST", "CONFIRM_YES", "CONFIRM_NO",
    "UNKNOWN",
})


class SpeechProvider(ExternalProvider):
    """
    内部维护最近一次事件；外部通过 push_event(event, produced_ts) 注入。
    poll(now) 返回并清空该事件（或返回上次缓存若未清空）；produced_ts 来自语音模块事件时间。
    """

    def __init__(self):
        self._event: str = ""
        self._produced_ts: float = 0.0

    def push_event(self, event: str, produced_ts: float) -> None:
        """语音模块/主流程注入一次事件；poll 取走后清空。"""
        event = (event or "").strip().upper()
        if event:
            self._event = event if event in SPEECH_EVENT_TOKENS else "UNKNOWN"
            self._produced_ts = produced_ts

    def poll(self, now: float) -> Tuple[str, float]:
        """返回当前事件 (event, produced_ts)，并清空事件（下次 poll 返回空）。"""
        out_event, out_ts = self._event, self._produced_ts
        self._event = ""
        self._produced_ts = 0.0
        return (out_event, out_ts)
