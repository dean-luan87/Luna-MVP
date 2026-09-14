# -*- coding: utf-8 -*-
"""
VoiceInput → Bridge → Core 的最小占位接口（输入接线 v1）。

不执行业务动作；仅证明「可进入主链边界」的调用形状，供后续 TaskChain/Core 替换实现。
"""

from __future__ import annotations

from typing import Any, Dict

from capabilities.voice.bridge.bridge_decision import BridgeDecision
from capabilities.voice.bridge.voice_input_to_bridge import bridge_decision_to_trace_dict


def dispatch_voice_bridge_to_core_placeholder(decision: BridgeDecision) -> Dict[str, Any]:
    """
    占位：将 BridgeDecision 交给 Core 的入口（当前无真实副作用）。

    返回可观测 trace，便于白盒断言「已进入主链边界」。
    """
    return {
        "received": True,
        "boundary": "core_placeholder_v1",
        "trace": bridge_decision_to_trace_dict(decision),
    }
