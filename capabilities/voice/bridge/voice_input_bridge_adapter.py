# -*- coding: utf-8 -*-
"""
VoiceInputEvent → Bridge 的薄适配层：补齐元数据、统一供决策器消费。

不裁决，不调用 Core。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from capabilities.voice.runtime.voice_shortcut_registry import VoiceShortcutEntry, VoiceShortcutRegistry
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent


@dataclass(frozen=True)
class AdaptedVoiceInputForBridge:
    """标准化后的 Bridge 输入视图。"""

    event: VoiceInputEvent
    shortcut_entry: Optional[VoiceShortcutEntry]
    route_reason_code: str


def adapt_voice_input_for_bridge(
    event: VoiceInputEvent,
    *,
    registry: VoiceShortcutRegistry,
) -> AdaptedVoiceInputForBridge:
    """根据 shortcut_id 反查 registry；附带 reason_code。"""
    sid = event.shortcut_id
    entry = registry.get_by_id(sid) if sid else None
    meta = event.metadata or {}
    reason = str(meta.get("route_reason_code", "") or "")
    return AdaptedVoiceInputForBridge(event=event, shortcut_entry=entry, route_reason_code=reason)
