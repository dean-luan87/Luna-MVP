"""
NavigationVoiceRouter: 导航语音路由器（TTS Routers 层）

负责在 TTS 播报前进行路由决策，包括：
- 时间窗口节流（Time Window Gate）
- 优先级控制
- 类别过滤

v1.4.6d-TW
"""

# ======================================================================
# [v1.4.9 P0-1 FREEZE] Navigation/Safety gating semantics (contract)
#
# Frozen behaviors:
# - NAVIGATION category is throttled by TimeWindowGate("NAVIGATION")
# - SAFETY category is throttled by TimeWindowGate("SAFETY") for
#   route_obstacle_warning(), but route_safety()/route_safety_warning()
#   bypasses the TimeWindowGate and uses TtsManager.push_safety() with
#   safety de-duplication (2s) in TtsManager.
#
# Any change here alters when the user hears navigation vs safety prompts.
# ======================================================================

from typing import Optional, Dict, Any

from task_engine.tts.routers.time_window_gate import TimeWindowGate
from task_engine.navigation.navigation_voice_adapter import NavigationVoiceAdapter
from task_engine.tts import tts_manager


class NavigationVoiceRouter:
    """
    导航语音路由器

    负责将导航/安全相关的语音事件路由到 TTS 系统，
    并在路由前应用时间窗口节流。
    """

    def __init__(self, tts_manager_instance=None):
        """
        初始化路由器

        Args:
            tts_manager_instance: TTS 管理器实例（可选，默认使用模块级单例）
        """
        self.tts = tts_manager_instance or tts_manager
        self.voice = NavigationVoiceAdapter()
        self.gate = TimeWindowGate()  # 新增：时间窗口控制器

    # ---------------------
    # 路由方法
    # ---------------------

    def route_turn(self, direction: str, distance: Optional[int] = None) -> None:
        """
        处理左右转播报

        Args:
            direction: 方向（"左转" / "右转" / "调头" 等）
            distance: 距离（米，可选）
        """
        category = "NAVIGATION"
        # 新增节流控制
        if not self.gate.allow(category):
            return

        utterances = self.voice.announce_turn(direction=direction, distance_m=distance)
        # 将 Utterance 列表推入 TTS 队列
        for u in utterances:
            self.tts.enqueue(u)

    def route_straight(self, distance: Optional[int] = None) -> None:
        """
        处理直行播报

        Args:
            distance: 距离（米，可选）
        """
        category = "NAVIGATION"
        # 节流控制
        if not self.gate.allow(category):
            return

        utterances = self.voice.announce_straight(distance_m=distance)
        # 将 Utterance 列表推入 TTS 队列
        for u in utterances:
            self.tts.enqueue(u)

    def route_obstacle_warning(
        self,
        text: Optional[str] = None,
        *,
        direction: Optional[str] = None,
        distance_m: Optional[int] = None,
    ) -> None:
        """
        安全播报：障碍物警告

        Args:
            text: 自定义文本（可选）
            direction: 方向（可选）
            distance_m: 距离（米，可选）
        """
        category = "SAFETY"
        # 节流控制（安全频率更快）
        if not self.gate.allow(category):
            return

        utterances = self.voice.announce_obstacle_warning(
            direction=direction, distance_m=distance_m
        )
        # 将 Utterance 列表推入 TTS 队列
        for u in utterances:
            self.tts.enqueue(u)

    def route_generic(self, category: str, text: str, **kwargs) -> None:
        """
        默认路由入口

        Args:
            category: 类别（"SAFETY" / "NAVIGATION" / "TASK" / "CHAT"）
            text: 播报文本
            **kwargs: 其他参数（传递给 announce_* 方法）
        """
        # Step 11: SAFETY 类别直接走安全队列，跳过时间窗口
        if category == "SAFETY":
            self.route_safety_warning(text=text, **kwargs)
            return

        # 添加节流判断
        if not self.gate.allow(category):
            return

        # 根据类别调用相应的 announce_* 方法
        if category == "NAVIGATION":
            # 如果有 text，使用 handle_speech_event；否则使用 announce_* 方法
            if text:
                utterances = self.voice.handle_speech_event({
                    "text": text,
                    "category": "navigation",
                    "decision": kwargs.get("decision"),
                })
            else:
                # 尝试从 kwargs 中提取 direction 和 distance
                direction = kwargs.get("direction")
                distance = kwargs.get("distance_m") or kwargs.get("distance")
                if direction:
                    utterances = self.voice.announce_turn(direction=direction, distance_m=distance)
                else:
                    utterances = self.voice.announce_straight(distance_m=distance)
        else:
            # 默认使用 handle_speech_event
            utterances = self.voice.handle_speech_event({"text": text, "category": category})

        # 将 Utterance 列表推入 TTS 队列
        for u in utterances:
            self.tts.enqueue(u)

    def route_safety_warning(self, text: str, **kwargs) -> bool:
        """
        Step 11: 导航安全播报（危险靠近、前方危险等），直接进入安全队列，跳过时间窗口限制。

        Args:
            text: 播报文本
            **kwargs: 其他参数

        Returns:
            bool: 是否成功加入安全队列（如果 2 秒内重复同一句，返回 False）
        """
        from task_engine.tts import Utterance
        
        # 创建安全播报 Utterance
        utter = Utterance(
            text=text,
            level=kwargs.get("level", "warning"),
            channel=kwargs.get("channel", "tts"),
            priority=kwargs.get("priority", 100),  # 安全播报默认最高优先级
            interrupt=True,  # 安全播报总是可打断
            meta=kwargs.get("meta", {}),
        )
        utter.meta["ttscategory"] = "SAFETY"
        utter.meta["safety"] = True
        
        # 直接推入安全队列（跳过时间窗口限制）
        return self.tts.push_safety(utter)

    def route_safety(self, text: str, meta: Optional[Dict[str, Any]] = None) -> bool:
        """
        Step 13.2: 用于一般安全事件（纯文本安全播报）。

        Args:
            text: 播报文本
            meta: 元数据（可选）

        Returns:
            bool: 是否成功加入安全队列（如果 2 秒内重复同一句，返回 False）
        """
        from task_engine.tts import Utterance
        
        utter = Utterance(
            text=text,
            meta=meta or {},
            level="warning",
            channel="tts",
            priority=95,  # 进入 P0 band
            interrupt=True,
        )
        utter.meta["ttscategory"] = "SAFETY"
        utter.meta["safety"] = True
        
        # 安全播报直接进入安全队列，跳过时间窗口限制
        return self.tts.push_safety(utter)

    def route_navigation(self, text: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """
        Step 13.2: 用于一般导航信息（纯文本导航，非转向、非障碍）。

        Args:
            text: 播报文本
            meta: 元数据（可选）
        """
        from task_engine.tts import Utterance
        
        utter = Utterance(
            text=text,
            meta=meta or {},
            level="info",
            channel="tts",
            priority=75,  # 进入 P1 band
            interrupt=False,
        )
        utter.meta["ttscategory"] = "NAVIGATION"
        
        # 时间窗口控制
        if self.gate.allow("NAVIGATION"):
            self.tts.enqueue(utter)

    def reset(self) -> None:
        """重置状态（用于测试）"""
        self.gate.reset()


# 模块级单例（可选）
navigation_voice_router = NavigationVoiceRouter()

