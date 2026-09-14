# -*- coding: utf-8 -*-
"""
VoiceDialogueBridge (Stage-1 placeholder).

Bridge 是受限路由层：把 VoiceIntentCandidate 路由成 Voice->Core 协议对象。
Stage-1 不实现逻辑，只固化接口/输入输出边界。
"""

from __future__ import annotations

from typing import Protocol

from capabilities.voice.schemas.voice_intent_candidate import VoiceIntentCandidate


class VoiceDialogueBridge(Protocol):
    def route(self, candidate: VoiceIntentCandidate) -> object:
        """
        返回 Voice->Core 协议对象（proposal/query/response）。
        Stage-1 使用 object 占位，后续阶段再收敛为 Union 类型。
        """

