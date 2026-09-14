# -*- coding: utf-8 -*-
"""
语音总闸（Speech Gate）

v1.8.3a: 系统级"注意力与发言权中枢"

职责（非常窄）：
1. 我现在能不能说？
2. 如果不能说，是谁在占用？
3. 这句话是不是刚刚说过？
4. 说完之后，我要不要冷却？

不做推理，不做记忆，不做策略。
只拥有"是否允许说话"的最终裁决权。
"""

import time
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class SpeechGate:
    """语音总闸"""
    
    def __init__(self, cooldown_seconds: float = 3.0):
        """
        初始化语音总闸
        
        Args:
            cooldown_seconds: 播报冷却时间（秒），默认 3 秒
        """
        self.locked = False  # TTS 是否正在占用
        self.last_scene_hash: Optional[str] = None  # 上次播报的场景 hash
        self.cooldown_until: float = 0.0  # 冷却截止时间
        self.cooldown_seconds = cooldown_seconds
        self.lock_owner: Optional[str] = None  # 当前占用者（用于调试）
    
    def can_speak(
        self,
        scene_hash: Optional[str] = None,
        user_speaking: bool = False
    ) -> Tuple[bool, str]:
        """
        判断是否可以说话（最终裁决）
        
        Args:
            scene_hash: 场景哈希值（用于去重）
            user_speaking: 用户是否正在说话
        
        Returns:
            Tuple[bool, str]: (是否可以说话, 原因)
                - (False, "user_speaking"): 用户正在说话，系统必须闭嘴
                - (False, "tts_busy"): TTS 正在占用
                - (False, "cooldown"): 播报冷却中
                - (False, "duplicate_scene"): 重复场景
                - (True, "ok"): 可以说话
        """
        now = time.time()
        
        # 规则 1: 用户说话时，系统必须闭嘴（绝对规则）
        if user_speaking:
            logger.debug("[SpeechGate] 用户正在说话，系统必须闭嘴")
            return False, "user_speaking"
        
        # 规则 2: TTS 正在占用
        if self.locked:
            logger.debug(f"[SpeechGate] TTS 正在占用（占用者: {self.lock_owner}）")
            return False, "tts_busy"
        
        # 规则 3: 播报冷却中
        if now < self.cooldown_until:
            remaining = self.cooldown_until - now
            logger.debug(f"[SpeechGate] 播报冷却中（剩余 {remaining:.1f}s）")
            return False, "cooldown"
        
        # 规则 4: 重复场景（如果提供了 scene_hash）
        if scene_hash is not None and scene_hash == self.last_scene_hash:
            logger.debug("[SpeechGate] 重复场景，抑制播报")
            return False, "duplicate_scene"
        
        # 可以说话
        return True, "ok"
    
    def acquire(self, owner: Optional[str] = None):
        """
        获取说话权（锁定）
        
        Args:
            owner: 占用者标识（用于调试）
        """
        if self.locked:
            logger.warning(f"[SpeechGate] 尝试获取已被占用的锁（当前占用者: {self.lock_owner}）")
            return False
        
        self.locked = True
        self.lock_owner = owner or "unknown"
        logger.debug(f"[SpeechGate] 获取说话权（占用者: {self.lock_owner}）")
        return True
    
    def force_acquire(self, owner: Optional[str] = None, source: str = "RISK"):
        """
        强制获取说话权（用于 LV1 风险警报）
        
        LV1 行为特性：
        - ✅ 可以打断自动播报
        - ❌ 不打断用户正在说的话（由 can_speak 检查）
        - ✅ 不可被去重
        - ✅ 不可被冷却抑制
        
        Args:
            owner: 占用者标识（用于调试）
            source: 强制获取的来源（如 "RISK"）
        
        Returns:
            bool: 是否成功获取（如果用户正在说话，返回 False）
        """
        # 注意：force_acquire 不检查用户说话状态
        # 用户说话状态的检查应该在调用 force_acquire 之前完成
        
        # 强制获取：即使 TTS 正在占用，也要打断
        if self.locked:
            logger.warning(
                f"[SpeechGate] 强制获取说话权，打断当前占用者: {self.lock_owner} "
                f"（来源: {source}）"
            )
        
        self.locked = True
        self.lock_owner = f"{source}_{owner or 'unknown'}"
        # 强制获取时，清除冷却和去重状态
        self.cooldown_until = 0.0
        self.last_scene_hash = None
        logger.info(f"[SpeechGate] 强制获取说话权（占用者: {self.lock_owner}, 来源: {source}）")
        return True
    
    def release(
        self,
        scene_hash: Optional[str] = None,
        cooldown: Optional[float] = None
    ):
        """
        释放说话权（解锁）
        
        Args:
            scene_hash: 场景哈希值（用于去重）
            cooldown: 冷却时间（秒），如果为 None 则使用默认值
        """
        if not self.locked:
            logger.warning("[SpeechGate] 尝试释放未被占用的锁")
            return
        
        now = time.time()
        cooldown_duration = cooldown if cooldown is not None else self.cooldown_seconds
        
        self.locked = False
        if scene_hash:
            self.last_scene_hash = scene_hash
        self.cooldown_until = now + cooldown_duration
        owner = self.lock_owner
        self.lock_owner = None
        
        logger.debug(
            f"[SpeechGate] 释放说话权（占用者: {owner}, 场景: {scene_hash}, 冷却: {cooldown_duration}s）"
        )
    
    def reset(self):
        """重置总闸"""
        self.locked = False
        self.last_scene_hash = None
        self.cooldown_until = 0.0
        self.lock_owner = None
        logger.debug("[SpeechGate] 已重置")

