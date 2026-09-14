# -*- coding: utf-8 -*-
"""
Voice Whitebox Pipeline V1 — 流程阶段枚举（仅说明性，无业务逻辑）。

用途：
- 文档与后续日志抽链时统一阶段命名
- 禁止在此文件写执行逻辑或接线代码
"""

from __future__ import annotations

from enum import Enum


class WhiteboxPipelineStageV1(str, Enum):
    REQUEST_INGRESS = "request_ingress"
    MESSAGE_PREPARATION = "message_preparation"
    BRIDGE_OR_ROUTING_DECISION = "bridge_or_routing_decision"
    CORE_OR_POLICY_HANDLING = "core_or_policy_handling"
    PROVIDER_SELECTION = "provider_selection"
    PROVIDER_EXECUTION = "provider_execution"
    FALLBACK_OR_ROLLBACK = "fallback_or_rollback"
    PLAYBACK_RESULT = "playback_result"
