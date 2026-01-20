# -*- coding: utf-8 -*-
"""
决策调度器（Decision Scheduler）

v1.8.3: 唯一有权决定是否触发 TTS 的模块

职责：
1. 现在要不要说？
2. 如果要说，说哪一句？
3. 是不是该闭嘴？

策略：
- 场景稳定且已播报过 → 不播
- 高风险 → 可打断播报
- 用户正在说话 → 延迟播报
- 其他情况 → 播一次
"""

import time
import logging
from typing import Dict, Optional, Callable

from core.scene_state_builder import SceneState
from core.system_memory import SystemMemory

logger = logging.getLogger(__name__)


class DecisionScheduler:
    """决策调度器"""
    
    def __init__(
        self,
        system_memory: Optional[SystemMemory] = None,
        cooldown_seconds: float = 2.0
    ):
        """
        初始化决策调度器
        
        Args:
            system_memory: 系统记忆（如果为 None，则自动创建）
            cooldown_seconds: 播报冷却时间（秒），默认 2 秒
        """
        self.memory = system_memory or SystemMemory()
        self.cooldown_seconds = cooldown_seconds
        self.last_speech_time: float = 0.0
        self.user_speaking: bool = False
    
    def should_speak(
        self,
        text: str,
        scene_state: SceneState,
        tts_callback: Optional[Callable[[str], None]] = None
    ) -> bool:
        """
        判断是否应该播报（唯一决策入口）
        
        Args:
            text: 要播报的文本
            scene_state: 场景状态
            tts_callback: TTS 回调函数（如果提供，则直接调用）
        
        Returns:
            bool: True 表示应该播报，False 表示不应该播报
        """
        # 清理过期记忆
        self.memory.cleanup_expired()
        
        # 策略 1: 场景稳定且已播报过 → 不播
        if scene_state.stability == "stable":
            if self.memory.has_spoken_scene(scene_state.scene_hash):
                logger.debug(
                    f"[DecisionScheduler] 场景稳定且已播报过，抑制播报: {scene_state.scene_id}"
                )
                return False
        
        # 策略 2: 高风险 → 可打断播报（优先级穿透）
        if scene_state.risk_level == "high":
            # 高风险仍然需要去重检查
            if self.memory.has_spoken(text):
                logger.debug(
                    f"[DecisionScheduler] 高风险消息在记忆窗口内已播过，抑制播报: {text[:30]}..."
                )
                return False
            
            # 允许播报
            if tts_callback:
                self._execute_speech(text, scene_state, tts_callback)
            return True
        
        # 策略 3: 用户正在说话 → 延迟播报
        if self.user_speaking:
            logger.debug("[DecisionScheduler] 用户正在说话，延迟播报")
            return False
        
        # 策略 4: 播报冷却检查
        current_time = time.time()
        if current_time - self.last_speech_time < self.cooldown_seconds:
            logger.debug(
                f"[DecisionScheduler] 播报冷却中（{current_time - self.last_speech_time:.1f}s < {self.cooldown_seconds}s），抑制播报"
            )
            return False
        
        # 策略 5: 文本去重检查
        if self.memory.has_spoken(text):
            logger.debug(
                f"[DecisionScheduler] 文本在记忆窗口内已播过，抑制播报: {text[:30]}..."
            )
            return False
        
        # 允许播报
        if tts_callback:
            self._execute_speech(text, scene_state, tts_callback)
        return True
    
    def _execute_speech(
        self,
        text: str,
        scene_state: SceneState,
        tts_callback: Callable[[str], None]
    ):
        """
        执行播报
        
        Args:
            text: 要播报的文本
            scene_state: 场景状态
            tts_callback: TTS 回调函数
        """
        # 记录播报
        self.memory.record_speech(text, scene_state.scene_hash)
        self.last_speech_time = time.time()
        
        # 调用 TTS
        logger.info(f"[DecisionScheduler] 执行播报: {text[:50]}...")
        tts_callback(text)
    
    def set_user_speaking(self, speaking: bool):
        """
        设置用户是否正在说话
        
        Args:
            speaking: True 表示用户正在说话，False 表示用户未说话
        """
        self.user_speaking = speaking
        if speaking:
            logger.debug("[DecisionScheduler] 用户开始说话，进入聆听态")
        else:
            logger.debug("[DecisionScheduler] 用户停止说话，退出聆听态")
    
    def reset(self):
        """重置调度器"""
        self.last_speech_time = 0.0
        self.user_speaking = False
        self.memory.reset()


