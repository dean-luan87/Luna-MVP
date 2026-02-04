"""
NavigationVoiceAdapter v1.4.6d

统一处理：
- 危险播报
- 导航播报
- 状态播报
- 闲聊播报（低优先级）

核心能力：
- 优先级调度 priority_queue
- 播报节流（debounce + cooldown）
- 去重机制
- 播报锁（危险事件打断普通事件）
- 文本正规化处理（不同类型不同风格）
"""

import time
import threading
import heapq
import logging
from typing import Dict, Any, Optional

from task_engine.tts import tts_manager

LOGGER = logging.getLogger("NavigationVoiceAdapter")


class NavigationVoiceAdapter:
    """
    单例类，负责所有导航相关语音的调度。
    """

    _instance = None
    _instance_lock = threading.Lock()

    @staticmethod
    def get():
        """获取单例实例"""
        with NavigationVoiceAdapter._instance_lock:
            if NavigationVoiceAdapter._instance is None:
                NavigationVoiceAdapter._instance = NavigationVoiceAdapter()
        return NavigationVoiceAdapter._instance

    def __init__(self):
        self.tts = tts_manager
        self.queue = []  # priority queue
        self.last_speak_timestamp = {}
        self.cooldowns = {        # 单位：秒
            "danger": 1.2,
            "navigation": 1.5,
            "status": 1.0,
            "chat": 0.5,
        }

        self.debounce_window = 0.6
        self.last_text = None
        self.last_text_time = 0

        self.speaking_lock = threading.Lock()

        self.priority_map = {
            "danger": 90,
            "navigation": 60,
            "status": 30,
            "chat": 10,
        }

    # -------------------------------------------------------
    # 核心入口
    # -------------------------------------------------------
    def route_event(self, speech_event: Dict[str, Any]) -> None:
        """
        路由语音事件到对应的播报策略。

        Args:
            speech_event: 语音事件字典
                {
                    "type": "danger/navigation/status/chat",
                    "raw_text": "...",
                    "priority": 可选,
                    "meta": {...}
                }
        """
        if not speech_event:
            return

        ev_type = speech_event.get("type", "chat")
        text = speech_event.get("raw_text", "")
        priority = speech_event.get("priority") or self.priority_map.get(ev_type, 10)

        # 判定 cooldown（该类型短时间不可重复播报）
        if not self._check_cooldown(ev_type):
            LOGGER.debug(f"[cooldown] type={ev_type} 跳过")
            return

        # 去重（句子完全一致，不重复播报）
        if self._is_duplicate(text):
            LOGGER.debug("[debounce] 文本重复，跳过播报")
            return

        # 进入优先级队列
        self._enqueue(priority, text, ev_type)

        # 启动消费线程
        self._consume()

    # -------------------------------------------------------
    # 队列管理
    # -------------------------------------------------------
    def _enqueue(self, priority: int, text: str, ev_type: str) -> None:
        """将事件加入优先级队列"""
        timestamp = time.time()
        item = (-priority, timestamp, text, ev_type)
        heapq.heappush(self.queue, item)

    def _consume(self) -> None:
        """
        消费线程：严格按优先级出队执行。
        """
        # NOTE(1.5): implicit behavior drop
        # NOTE(1.5): decision handled here for backward compatibility
        # NOTE(>=1.6): should be routed through Action layer
        if not self.speaking_lock.acquire(blocking=False):
            # 正在播报中，稍后自动触发
            return

        try:
            while self.queue:
                priority_neg, ts, text, ev_type = heapq.heappop(self.queue)

                # 播报（使用 TTS 策略体系）
                LOGGER.info(f"[speak] [{ev_type}] {text}")
                
                # 根据类型选择对应的 TTS 策略
                if ev_type == "danger":
                    from task_engine.tts import speak_safety
                    speak_safety(text)
                elif ev_type == "navigation":
                    from task_engine.tts import speak_navigation
                    speak_navigation(text)
                elif ev_type == "status":
                    from task_engine.tts import speak_task
                    speak_task(text)
                else:  # chat
                    from task_engine.tts import speak_chat
                    speak_chat(text)

                # 记录 timestamp
                self._record_speak(ev_type)
                self.last_text = text
                self.last_text_time = time.time()

        finally:
            self.speaking_lock.release()

    # -------------------------------------------------------
    # 去重 / 冷却控制
    # -------------------------------------------------------
    def _check_cooldown(self, ev_type: str) -> bool:
        """检查是否在冷却期内"""
        now = time.time()
        last_time = self.last_speak_timestamp.get(ev_type, 0)
        cd = self.cooldowns.get(ev_type, 1.0)
        return (now - last_time) > cd

    def _record_speak(self, ev_type: str) -> None:
        """记录播报时间戳"""
        self.last_speak_timestamp[ev_type] = time.time()

    def _is_duplicate(self, text: str) -> bool:
        """检查是否为重复文本"""
        now = time.time()
        if self.last_text == text and (now - self.last_text_time) < self.debounce_window:
            return True
        return False

    # -------------------------------------------------------
    # 手动通道（外部可调用）
    # -------------------------------------------------------
    def speak_danger(self, text: str) -> None:
        """危险播报"""
        self.route_event({"type": "danger", "raw_text": text})

    def speak_nav(self, text: str) -> None:
        """导航播报"""
        self.route_event({"type": "navigation", "raw_text": text})

    def speak_status(self, text: str) -> None:
        """状态播报"""
        self.route_event({"type": "status", "raw_text": text})

    def speak_chat(self, text: str) -> None:
        """闲聊播报"""
        self.route_event({"type": "chat", "raw_text": text})

