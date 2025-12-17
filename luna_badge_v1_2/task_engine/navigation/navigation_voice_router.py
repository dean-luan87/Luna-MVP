"""
NavigationVoiceRouter: 导航语音路由器

核心能力：
- 安全播报 vs 导航播报的优先级冲突处理
- 安全播报之后的"静音期"，压制不必要的导航啰嗦
- CHAT/TASK 类别的可配置穿透策略
"""

# ======================================================================
# [v1.4.9 P0-1 FREEZE] Safety silence window & category suppression
#
# Frozen default behaviors (user-visible):
# - safety_silence_window = 3.0s:
#   within this window after a SAFETY output, NAVIGATION utterances are
#   suppressed (dropped) by default routing.
# - enable_chat_during_safety_window = True by default.
#
# Together with TimeWindowGate (0.8s safety / 2.0s navigation), these
# values define the stable "talking frequency" behavior for 1.4.x.
# ======================================================================

import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from task_engine.tts import Utterance, tts_manager
from task_engine.tts.routers.time_window_gate import TimeWindowGate


@dataclass
class NavigationVoiceRouterConfig:
    """
    导航语音路由配置：

    - 安全事件后静默导航播报的时间窗口
    - 是否允许闲聊在安全期内播放
    """
    safety_silence_window: float = 3.0   # 安全播报后 N 秒内抑制导航播报
    enable_chat_during_safety_window: bool = True


@dataclass
class NavigationVoiceRouterState:
    """
    导航语音路由运行时状态：

    - 上一次安全播报时间
    """
    last_safety_ts: float = 0.0


class NavigationVoiceRouter:
    """
    负责在 SAFETY / NAVIGATION / CHAT / TASK 等 Utterance 之间做路由与抑制：

    - SAFETY > NAVIGATION
    - 安全播报之后的一段时间内，抑制导航播报
    - CHAT/TASK 根据配置决定是否穿透
    """

    def __init__(
        self,
        config: Optional[NavigationVoiceRouterConfig] = None,
        state: Optional[NavigationVoiceRouterState] = None,
        time_window_gate: Optional[TimeWindowGate] = None,
    ) -> None:
        self.config = config or NavigationVoiceRouterConfig()
        self.state = state or NavigationVoiceRouterState()
        # Patch-H: 时间窗口节流控制器
        self.time_window_gate = time_window_gate or TimeWindowGate()

    # ------------- 分类工具 -------------

    @staticmethod
    def _get_category(u: Utterance) -> str:
        """
        从 Utterance 的 meta 中读取 category，
        默认值为 "TASK"（保守策略）。
        """
        meta = u.meta or {}
        cat = meta.get("category") or meta.get("ttscategory") or meta.get("tts_category")
        if not cat:
            # 回落到 level 或 priority 的弱推断
            if u.level == "warning":
                return "SAFETY"
            if u.level == "system":
                return "SYSTEM"
            if (u.priority or 0) >= 80:
                return "SAFETY"
            if (u.priority or 0) >= 70:
                return "NAVIGATION"
            return "TASK"
        return str(cat).upper()

    def _mark_safety(self, u: Utterance) -> None:
        """标记一次安全播报发生。"""
        self.state.last_safety_ts = time.time()

    def _within_safety_window(self) -> bool:
        """检查是否在安全静默窗口内"""
        if self.state.last_safety_ts <= 0:
            return False
        return (time.time() - self.state.last_safety_ts) < self.config.safety_silence_window

    # ------------- 核心路由逻辑 -------------

    def route_batch(self, utterances: List[Utterance]) -> List[Utterance]:
        """
        对一批待播报 Utterance 做路由：

        1. 如果存在 SAFETY 类，则只保留最高优先级的那条 SAFETY
        2. 否则：
           - 若处于安全静默窗口内：
             - 丢弃 NAVIGATION
             - CHAT 是否保留由配置决定
           - 不在安全窗口：全部通过
        3. Patch-H: 应用时间窗口节流（Time Window Gate）
        """
        if not utterances:
            return []

        # 标记类别
        categorized: List[Dict[str, Any]] = []
        for u in utterances:
            cat = self._get_category(u)
            categorized.append({"u": u, "category": cat})

        # Step 1: 有安全播报 → 仅保留最高优先级的一条
        safety_list = [x for x in categorized if x["category"] == "SAFETY"]
        if safety_list:
            # 选择优先级最高、若相同则时间最早的一条
            safety_list.sort(
                key=lambda x: (
                    -(x["u"].priority or 0),
                    x["u"].created_at,
                )
            )
            best = safety_list[0]["u"]

            # Patch-H: 时间窗口节流检查
            if not self.time_window_gate.allow("SAFETY"):
                # 安全播报被节流，但仍记录安全时间（用于静默窗口）
                self._mark_safety(best)
                return []

            # 安全播报强制打断：确保 interrupt、priority
            if best.priority is None or best.priority < 80:
                best.priority = 90
            best.interrupt = True

            # 记录安全时间
            self._mark_safety(best)
            return [best]

        # Step 2: 没有 SAFETY，考虑安全窗口对 NAVIGATION 的抑制
        if self._within_safety_window():
            filtered: List[Utterance] = []
            for x in categorized:
                cat = x["category"]
                u = x["u"]

                if cat == "NAVIGATION":
                    # 安全静默期内抑制导航播报
                    continue
                if cat == "CHAT" and not self.config.enable_chat_during_safety_window:
                    continue
                filtered.append(u)
            return filtered

        # Step 3: 正常情况，应用时间窗口节流
        filtered: List[Utterance] = []
        for x in categorized:
            cat = x["category"]
            u = x["u"]

            # Patch-H: 对 NAVIGATION 类别应用时间窗口节流
            if cat == "NAVIGATION":
                if not self.time_window_gate.allow("NAVIGATION"):
                    continue  # 被节流，跳过

            filtered.append(u)

        return filtered

    # ------------- 一站式入口（直接 speak） -------------

    def route_and_speak(self, utterances: List[Utterance]) -> None:
        """
        集成入口：
        - 对 Utterance 做路由/抑制
        - 将结果推入 tts_manager 队列
        - 触发 TTS Runtime Driver 处理一次
        """
        routed = self.route_batch(utterances)
        if not routed:
            return
        
        # 统一进入 TTS 管线
        for u in routed:
            tts_manager.enqueue(u)
        
        # 触发 TTS Runtime Driver 处理一次（如果已启动）
        try:
            from task_engine.tts.runtime_driver import TTSRuntimeDriver
            # 如果 driver 已启动，调用 process_once
            # 这里我们只负责入队，实际的驱动由外部管理
            pass
        except ImportError:
            pass

    def reset(self) -> None:
        """重置状态（用于测试）"""
        self.state.last_safety_ts = 0.0
        if hasattr(self, 'time_window_gate'):
            self.time_window_gate.reset()


# 模块级单例（导航任务内优先使用）
navigation_voice_router = NavigationVoiceRouter()

