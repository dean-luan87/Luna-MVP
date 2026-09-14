# -*- coding: utf-8 -*-
"""
切段文本长短模式判定（规则版 v1）。

不接模型：白名单短指令与待确认上下文下的 confirmation 优先于长输入拆解。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from capabilities.voice.runtime.voice_shortcut_registry import VoiceShortcutRegistry
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent

# 明显噪声/占位（无任务语义）
_NOISE_PATTERN = re.compile(r"^[嗯啊哦哈唉呀呃\d\s，。！？,.\!\?\-_]+$")


@dataclass(frozen=True)
class VoiceInputLengthModeResult:
    """分流语义：short / long / reject。"""

    mode: str  # short_controlled_input | long_task_planning_input | rejected_input
    reason_code: str
    notes: str


def classify_voice_input_length_mode(
    event: VoiceInputEvent,
    *,
    pending_confirmation_context: bool = False,
    registry: Optional[VoiceShortcutRegistry] = None,
) -> VoiceInputLengthModeResult:
    """
    判定顺序（写死）：
    1) 路由 reject → rejected_input
    2) 仅唤醒词、无正文 → short（SESSION_WAKE）
    3) 白名单 shortcut 命中 → short
    4) 有待确认上下文时：仅命中 confirmation_feedback 白名单 → short（先于长输入）
    5) 纯噪声短占位 → rejected_input
    6) 其余已 accept 且无短指令 → long_task_planning_input
    """
    reg = registry or VoiceShortcutRegistry()

    if event.router_decision == "reject":
        return VoiceInputLengthModeResult(
            "rejected_input",
            "router_rejected",
            "router 已拒绝该句",
        )

    stripped = (event.wake_word_stripped or event.normalized_text or "").strip()

    if event.wake_word_detected and not stripped:
        return VoiceInputLengthModeResult(
            "short_controlled_input",
            "wake_word_only_session_wake",
            "仅唤醒词，激活会话，不进入长输入拆解",
        )

    if event.shortcut_id is not None:
        return VoiceInputLengthModeResult(
            "short_controlled_input",
            "whitelist_shortcut",
            f"白名单短指令命中 shortcut_id={event.shortcut_id}",
        )

    if pending_confirmation_context:
        sc = reg.match(stripped, is_task_mode=event.is_task_mode)
        if sc is not None and sc.shortcut_type == "confirmation_feedback":
            return VoiceInputLengthModeResult(
                "short_controlled_input",
                "pending_confirmation_confirmation_feedback",
                "有待确认上下文，confirmation/feedback 优先于长输入理解",
            )

    if _is_noise_placeholder(stripped):
        return VoiceInputLengthModeResult(
            "rejected_input",
            "noise_or_placeholder",
            "空语义噪声或占位，不进入短链与长链",
        )

    return VoiceInputLengthModeResult(
        "long_task_planning_input",
        "natural_language_to_task_planning_v1",
        "非白名单受控短句，进入 run_long_input_task_planning_v1（止于 task_plan_v1）",
    )


def _is_noise_placeholder(t: str) -> bool:
    s = (t or "").strip()
    if not s:
        return True
    if len(s) <= 2 and _NOISE_PATTERN.match(s):
        return True
    return False
