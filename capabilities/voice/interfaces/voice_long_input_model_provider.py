# -*- coding: utf-8 -*-
"""
长语音模型 Provider 协议（v1）。

唯一合法桥梁：输出必须符合 VoiceLongInputStructuredParseResult（voice_task_parse_v1_1）。
具体实现（Qwen / 其他）不暴露给 classifier/mapper 以外层。
"""

from __future__ import annotations

from typing import Optional, Protocol, runtime_checkable

from capabilities.voice.schemas.voice_long_input_structured_parse_v1_1 import VoiceLongInputStructuredParseResult


@runtime_checkable
class VoiceLongInputModelProvider(Protocol):
    def parse_long_input(
        self,
        text: str,
        *,
        session_hint: str = "",
        request_id: str = "",
    ) -> Optional[VoiceLongInputStructuredParseResult]:
        """返回结构化理解；None 表示本 Provider 不参与，由路由回退规则链。"""


class MockVoiceLongInputModelProvider:
    """
    Mock：内部调用规则链 + structured builder，模拟「模型输出与规则一致」。

    用于双通道测试；不接真实权重。
    """

    def parse_long_input(
        self,
        text: str,
        *,
        session_hint: str = "",
        request_id: str = "",
    ) -> Optional[VoiceLongInputStructuredParseResult]:
        from capabilities.voice.bridge.voice_long_input_structured_parse_builder import (
            build_voice_long_input_structured_parse_v1_1,
        )
        from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1_rule_chain

        pr = run_long_input_task_planning_v1_rule_chain(
            text,
            request_id=request_id,
            session_hint=session_hint,
        )
        return build_voice_long_input_structured_parse_v1_1(
            pr,
            raw_text=text or "",
            context_resume_hint=session_hint,
        )


class PlaceholderVoiceLongInputModelProvider:
    """占位：始终返回 None → 路由走规则链。"""

    def parse_long_input(
        self,
        text: str,
        *,
        session_hint: str = "",
        request_id: str = "",
    ) -> Optional[VoiceLongInputStructuredParseResult]:
        return None
