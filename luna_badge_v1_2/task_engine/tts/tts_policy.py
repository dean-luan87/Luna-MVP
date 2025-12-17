"""
TTS Policy: 语音播报策略映射模块

负责定义 Category → priority / interrupt 的规则，并提供工具函数。
"""

# ======================================================================
# [v1.4.9 P0-1 FREEZE] Policy table semantics (behavior contract)
#
# The policy table below defines user-visible precedence and interruption
# behavior. Any change is a behavior change and requires a version bump.
#
# Frozen concepts:
# - Category set: SAFETY / NAVIGATION / SYSTEM / TASK / CHAT
# - Category -> (priority, interrupt, default_level) mapping semantics
# - PriorityBand mapping is frozen in `priority_bands.py`
#
# Allowed within 1.4.x without version bump:
# - Documentation/logging improvements ONLY (no semantic change)
# ======================================================================

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

from .utterance import Utterance


class TTSCategory(str, Enum):
    """语音播报的业务类别，用于映射优先级和打断策略。"""

    SAFETY = "safety"          # 安全相关（障碍物、危险环境等）
    NAVIGATION = "navigation"  # 路线/方向播报
    SYSTEM = "system"          # 系统状态、错误提示
    TASK = "task"              # 任务执行反馈（已完成、下一步等）
    CHAT = "chat"              # 闲聊、陪伴、非刚需内容


@dataclass(frozen=True)
class TTSPolicy:
    """单一类别的 TTS 策略定义。"""

    priority: int
    interrupt: bool
    default_level: str = "info"
    default_channel: str = "tts"
    meta_overrides: Dict[str, Any] = field(default_factory=dict)

    def band(self) -> "PriorityBand":
        """
        Step 12: 返回该策略对应的优先级段.

        Returns:
            PriorityBand: 对应的优先级段
        """
        from .priority_bands import PriorityBand
        return PriorityBand.from_priority(self.priority)


# 全局策略表：可以根据需要微调数值
TTS_POLICY_TABLE: Dict[TTSCategory, TTSPolicy] = {
    TTSCategory.SAFETY: TTSPolicy(
        priority=90,
        interrupt=True,
        default_level="warning",
        meta_overrides={"safety": True, "hazard_level": "high"},
    ),
    TTSCategory.NAVIGATION: TTSPolicy(
        priority=75,
        interrupt=False,
        default_level="info",
        meta_overrides={"navigation": True},
    ),
    TTSCategory.SYSTEM: TTSPolicy(
        priority=65,
        interrupt=False,
        default_level="system",
        meta_overrides={"system": True},
    ),
    TTSCategory.TASK: TTSPolicy(
        priority=50,
        interrupt=False,
        default_level="info",
        meta_overrides={"task": True},
    ),
    TTSCategory.CHAT: TTSPolicy(
        priority=25,
        interrupt=False,
        default_level="info",
        meta_overrides={"chat": True},
    ),
}


def get_policy(category: TTSCategory) -> TTSPolicy:
    """获取某个类别的策略；如未配置则回退到 TASK 策略。"""
    return TTS_POLICY_TABLE.get(category, TTS_POLICY_TABLE[TTSCategory.TASK])


def make_utterance(
    text: str,
    category: TTSCategory,
    *,
    level: Optional[str] = None,
    channel: Optional[str] = None,
    meta: Optional[Dict[str, Any]] = None,
    priority: Optional[int] = None,
    interrupt: Optional[bool] = None,
) -> Utterance:
    """
    根据类别创建一个带好 priority / interrupt 的 Utterance。

    调用方只需要关心 text + category，其他信息由策略自动填充，
    如有特殊需求可以通过显式参数覆盖。
    """
    policy = get_policy(category)

    final_priority = priority if priority is not None else policy.priority
    final_interrupt = interrupt if interrupt is not None else policy.interrupt
    final_level = level if level is not None else policy.default_level
    final_channel = channel if channel is not None else policy.default_channel

    merged_meta: Dict[str, Any] = {}
    if policy.meta_overrides:
        merged_meta.update(policy.meta_overrides)
    if meta:
        merged_meta.update(meta)

    # 在 meta 中写入 category，便于下游调试 / 统计
    merged_meta.setdefault("ttscategory", category.value)

    return Utterance(
        text=text,
        level=final_level,
        channel=final_channel,
        priority=final_priority,
        interrupt=final_interrupt,
        meta=merged_meta,
    )


def apply_policy_to_utterance(
    utterance: Utterance,
    category: TTSCategory,
    *,
    override_priority: bool = True,
    override_interrupt: bool = True,
) -> Utterance:
    """
    在已有 Utterance 上应用策略（不会就地修改，返回新对象）。

    用于 TaskExecutionResult 已经构造了 utterance，但没有设置优先级的场景。
    """
    policy = get_policy(category)

    new_priority = utterance.priority
    new_interrupt = utterance.interrupt

    if override_priority or utterance.priority == 0:
        new_priority = policy.priority
    if override_interrupt:
        new_interrupt = policy.interrupt

    new_meta: Dict[str, Any] = {}
    if utterance.meta:
        new_meta.update(utterance.meta)
    if policy.meta_overrides:
        # 策略覆盖可写入一些标记字段，如 safety/navigation 等
        new_meta.update(policy.meta_overrides)
    new_meta.setdefault("ttscategory", category.value)

    # 如果原始 utterance 没有 level 或 channel，使用策略的默认值
    new_level = utterance.level if utterance.level else policy.default_level
    new_channel = utterance.channel if utterance.channel else policy.default_channel

    return Utterance(
        text=utterance.text,
        level=new_level,
        channel=new_channel,
        priority=new_priority,
        interrupt=new_interrupt,
        created_at=utterance.created_at,
        meta=new_meta,
        play_id=getattr(utterance, "play_id", ""),
    )

