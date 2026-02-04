"""
Navigation Speech Manager (v1.3.0)

导航语音策略管理器

根据 F7 导航决策，决定是否播报，以及播报什么
"""

import time
import logging

from .nav_speech_config import (
    COOLDOWN,
    PRIORITY,
    STYLE,
    TEMPLATES,
    STOP_DANGER_MESSAGE,
    DEBUG_NAV_SPEECH,
)

logger = logging.getLogger(__name__)


class NavSpeechManager:
    """
    导航语音策略管理器

    负责将 F7 的导航决策转换为语音播报事件
    - 去"话痨"：同一指令不会频繁重复
    - 优先级：STOP > HARD_* > SLIGHT_* > FORWARD
    - 语气控制：calm / alert
    - 状态切换感知：只在决策变化时播报
    """

    def __init__(self):
        """
        初始化语音策略管理器
        """
        # 记录每个 decision 上次播报时间
        self.last_spoken_time = {}
        self.last_decision = None
        self.last_text = None

        logger.info("导航语音策略管理器初始化完成")

    def build_from_nav(self, nav_result: dict, danger: bool = False):
        """
        根据导航决策生成语音播报事件

        Args:
            nav_result: 来自 Navigator.decide 的输出，例如：
                {
                    "decision": "SLIGHT_RIGHT",
                    "offset": 0.8,
                    "column_score": [...],
                    "message": "右侧稍微更通畅，请向右一点",
                    "blockage_level": "partial",
                    "is_narrow": False,
                }
            danger: 是否为高危场景（可由上层根据 risk_map / 其他信息判断）

        Returns:
            dict | None: SpeechEvent 字典，或 None 表示这帧不需要说话
                {
                    "speak": True,
                    "decision": str,
                    "text": str,
                    "style": str,          # "calm" / "alert"
                    "priority": int,       # 0-3，数字越大优先级越高
                    "interruptible": bool, # 是否可以被更高优先级语音打断
                    "category": "navigation"
                }
        """
        if nav_result is None:
            return None

        decision = nav_result.get("decision", "FORWARD")
        now = time.time()

        # STOP 特殊处理
        if decision == "STOP":
            # 高危场景使用加重提示
            if danger:
                text = STOP_DANGER_MESSAGE
            else:
                # 优先使用 nav_result 中的 message
                text = nav_result.get("message") or TEMPLATES.get("STOP", "前方无法通行，请原地停下。")

            style = STYLE.get("STOP", "alert")

            # 简单防抖：0.5 秒内只说一次 STOP
            min_gap = COOLDOWN.get("STOP", 0.5)
            last_t = self.last_spoken_time.get("STOP", 0)

            if now - last_t < min_gap:
                if DEBUG_NAV_SPEECH:
                    logger.debug(f"[NavSpeech] STOP 在冷却期内，跳过播报（距离上次 {now - last_t:.2f} 秒）")
                return None

            self._mark_spoken("STOP", text, now)

            if DEBUG_NAV_SPEECH:
                logger.debug(f"[NavSpeech] STOP: {text}")

            return self._build_event(
                decision="STOP",
                text=text,
                style=style,
                priority=PRIORITY.get("STOP", 3)
            )

        # 其他决策
        # 如果与上一次播报的 decision 一样，需要检查冷却时间
        if decision == self.last_decision:
            min_gap = COOLDOWN.get(decision, COOLDOWN["DEFAULT"])
            last_t = self.last_spoken_time.get(decision, 0)

            if now - last_t < min_gap:
                if DEBUG_NAV_SPEECH:
                    logger.debug(f"[NavSpeech] {decision} 在冷却期内，跳过播报（距离上次 {now - last_t:.2f} 秒）")
                return None

        # 从 nav_result["message"] 或 TEMPLATES 中取文本
        text = nav_result.get("message") or TEMPLATES.get(decision, "")

        if not text:
            # 没有可用文案，放弃播报
            if DEBUG_NAV_SPEECH:
                logger.warning(f"[NavSpeech] 没有找到 {decision} 的文案模板")
            return None

        style = STYLE.get(decision, "calm")
        priority = PRIORITY.get(decision, 0)

        self._mark_spoken(decision, text, now)

        if DEBUG_NAV_SPEECH:
            logger.debug(f"[NavSpeech] decision={decision}, text={text}, style={style}, priority={priority}")

        return self._build_event(decision, text, style, priority)

    def _mark_spoken(self, decision: str, text: str, ts: float):
        """
        标记已播报

        Args:
            decision: 决策类型
            text: 播报文本
            ts: 时间戳
        """
        self.last_spoken_time[decision] = ts
        self.last_decision = decision
        self.last_text = text

    def _build_event(self, decision: str, text: str, style: str, priority: int):
        """
        构建语音播报事件

        Args:
            decision: 决策类型
            text: 播报文本
            style: 语气风格
            priority: 优先级

        Returns:
            dict: SpeechEvent 字典
        """
        return {
            "speak": True,
            "decision": decision,
            "text": text,
            "style": style,
            "priority": priority,
            "interruptible": (priority < 3),  # STOP（3）不可被打断，其它可以
            "category": "navigation",
        }

    def reset(self):
        """
        重置状态（清除历史记录）
        """
        self.last_spoken_time = {}
        self.last_decision = None
        self.last_text = None
        logger.debug("导航语音策略管理器状态已重置")

    def get_last_decision(self) -> str:
        """
        获取上一次播报的决策

        Returns:
            str: 上一次的决策类型，如果没有则返回 None
        """
        return self.last_decision

    def should_interrupt(self, new_priority: int) -> bool:
        """
        判断新事件是否应该打断当前播报

        Args:
            new_priority: 新事件的优先级

        Returns:
            bool: 是否应该打断
        """
        # 如果新优先级更高，且当前播报是可打断的
        # 这里简化处理，实际应该检查当前是否有正在播报的内容
        return new_priority >= 2  # HARD_* 及以上优先级可以打断









