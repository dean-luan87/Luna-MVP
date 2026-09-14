# -*- coding: utf-8 -*-
"""
白名单短指令注册表（v1）：集中维护，不散落在业务分支。

后续「长语音 → LLM 拆解 → 关键词/任务动作」为扩展层，不在本模块实现。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class VoiceShortcutEntry:
    shortcut_id: str
    shortcut_type: str  # device_control | task_control | task_query | session_control
    phrases: Tuple[str, ...]  # 命中任一即视为该指令
    allowed_in_task_mode: bool = True
    allowed_in_normal_mode: bool = False
    requires_confirmation: bool = False
    mapped_route_type: str = ""  # 与 Bridge 路由语义对齐的占位名


def _default_whitelist() -> List[VoiceShortcutEntry]:
    """v1 最小白名单；高风险项标记 requires_confirmation，路由层可接确认。"""
    return [
        # A 设备控制
        VoiceShortcutEntry(
            "dev_pause",
            "device_control",
            # 显式设备短语；裸「暂停」在任务态归 task_pause，避免与任务抢优先级
            ("暂停播报", "先暂停"),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="device_control",
        ),
        VoiceShortcutEntry(
            "dev_stop",
            "device_control",
            ("停止",),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="device_control",
        ),
        VoiceShortcutEntry(
            "dev_resume",
            "device_control",
            ("继续播报",),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="device_control",
        ),
        VoiceShortcutEntry(
            "dev_cancel",
            "device_control",
            ("取消",),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="device_control",
        ),
        VoiceShortcutEntry(
            "dev_shutdown",
            "device_control",
            ("关机",),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            requires_confirmation=True,
            mapped_route_type="device_control",
        ),
        VoiceShortcutEntry(
            "dev_vol_up",
            "device_control",
            ("音量大一点", "大声点"),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="device_control",
        ),
        VoiceShortcutEntry(
            "dev_vol_down",
            "device_control",
            ("音量小一点",),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="device_control",
        ),
        # A2 TTS 语速控制（Qwen runtime control v0）
        VoiceShortcutEntry(
            "dev_tts_speed_down",
            "device_control",
            ("语速慢一点", "说慢点", "慢一点"),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="device_control",
        ),
        VoiceShortcutEntry(
            "dev_tts_speed_up",
            "device_control",
            ("语速快一点", "说快点", "快一点"),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="device_control",
        ),
        VoiceShortcutEntry(
            "dev_tts_speed_set_0_25",
            "device_control",
            ("语速0.25", "语速 0.25", "语速设置0.25", "语速设置为0.25", "语速调到0.25", "语速调为0.25"),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="device_control",
        ),
        VoiceShortcutEntry(
            "dev_tts_speed_set_0_5",
            "device_control",
            ("语速0.5", "语速 0.5", "语速设置0.5", "语速设置为0.5", "语速调到0.5", "语速调为0.5"),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="device_control",
        ),
        VoiceShortcutEntry(
            "dev_tts_speed_set_0_75",
            "device_control",
            ("语速0.75", "语速 0.75", "语速设置0.75", "语速设置为0.75", "语速调到0.75", "语速调为0.75"),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="device_control",
        ),
        VoiceShortcutEntry(
            "dev_tts_speed_set_1_0",
            "device_control",
            ("语速1", "语速 1", "语速1.0", "语速 1.0", "语速设置1", "语速设置为1", "语速调到1", "语速调为1"),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="device_control",
        ),
        # B 任务控制
        VoiceShortcutEntry(
            "task_start_nav",
            "task_control",
            ("开始导航",),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="task_lifecycle",
        ),
        VoiceShortcutEntry(
            "task_end",
            "task_control",
            ("结束任务",),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=False,
            mapped_route_type="task_lifecycle",
        ),
        VoiceShortcutEntry(
            "task_switch",
            "task_control",
            ("切换任务",),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=False,
            mapped_route_type="task_lifecycle",
        ),
        VoiceShortcutEntry(
            "task_pause",
            "task_control",
            ("暂停任务", "暂停"),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=False,
            mapped_route_type="task_lifecycle",
        ),
        VoiceShortcutEntry(
            "task_resume",
            "task_control",
            ("继续任务", "继续"),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=False,
            mapped_route_type="task_lifecycle",
        ),
        # C 任务问询
        VoiceShortcutEntry(
            "q_where",
            "task_query",
            ("现在到哪了", "到哪了"),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=False,
            mapped_route_type="task_context_query",
        ),
        VoiceShortcutEntry(
            "q_nearby",
            "task_query",
            ("附近有什么",),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=False,
            mapped_route_type="task_context_query",
        ),
        VoiceShortcutEntry(
            "q_status",
            "task_query",
            ("当前状态",),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=False,
            mapped_route_type="task_context_query",
        ),
        VoiceShortcutEntry(
            "q_ahead",
            "task_query",
            ("前面是什么",),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=False,
            mapped_route_type="task_context_query",
        ),
        VoiceShortcutEntry(
            "q_distance",
            "task_query",
            ("还有多远",),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=False,
            mapped_route_type="task_context_query",
        ),
        # 会话结束（白名单内显式结束窗口）
        VoiceShortcutEntry(
            "session_end",
            "session_control",
            ("结束对话", "不用了", "退出"),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="session_end",
        ),
        # D 确认/反馈证据（非直接命令；Bridge 走 CONFIRMATION / FEEDBACK）
        VoiceShortcutEntry(
            "cf_yes",
            "confirmation_feedback",
            ("是", "对"),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="confirmation",
        ),
        VoiceShortcutEntry(
            "cf_no",
            "confirmation_feedback",
            ("不是", "不对"),
            allowed_in_task_mode=True,
            allowed_in_normal_mode=True,
            mapped_route_type="confirmation",
        ),
    ]


def _phrase_matches_full_text(t: str, ph: str) -> bool:
    """单字短语必须整句匹配，避免「是」命中「这是一段…」等子串误伤。"""
    if not ph:
        return False
    if len(ph) <= 1:
        return t == ph
    return ph in t


class VoiceShortcutRegistry:
    """白名单命中：最长短语优先（避免子串误伤）。"""

    def __init__(self, entries: Optional[List[VoiceShortcutEntry]] = None) -> None:
        self._entries: List[VoiceShortcutEntry] = list(entries) if entries is not None else _default_whitelist()

    def all_entries(self) -> List[VoiceShortcutEntry]:
        return list(self._entries)

    def get_by_id(self, shortcut_id: str) -> Optional[VoiceShortcutEntry]:
        for e in self._entries:
            if e.shortcut_id == shortcut_id:
                return e
        return None

    def match(self, normalized_text: str, *, is_task_mode: bool) -> Optional[VoiceShortcutEntry]:
        """若命中则返回条目；否则 None。normalized_text 建议已 strip、无首尾空白。"""
        t = (normalized_text or "").strip()
        if not t:
            return None
        candidates: List[VoiceShortcutEntry] = []
        for e in self._entries:
            ok = (is_task_mode and e.allowed_in_task_mode) or ((not is_task_mode) and e.allowed_in_normal_mode)
            if not ok:
                continue
            for ph in sorted(e.phrases, key=len, reverse=True):
                if ph and _phrase_matches_full_text(t, ph):
                    candidates.append(e)
                    break
        if not candidates:
            return None
        # 选短语最长的一条（再按 id 稳定排序）
        best: Optional[VoiceShortcutEntry] = None
        best_len = -1
        for e in candidates:
            for ph in e.phrases:
                if _phrase_matches_full_text(t, ph) and len(ph) > best_len:
                    best_len = len(ph)
                    best = e
        return best
