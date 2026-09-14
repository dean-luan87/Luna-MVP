# -*- coding: utf-8 -*-
"""
系统记忆（System Memory）

v1.8.3: 轻量级系统记忆，记录最近说过什么和场景状态

职责：
- 最近说过什么
- 最近 10 秒的场景 hash
- 播报历史
"""

import time
from typing import Dict, List, Optional
from collections import deque


class SystemMemory:
    """系统记忆"""
    
    def __init__(self, memory_window: float = 10.0):
        """
        初始化系统记忆
        
        Args:
            memory_window: 记忆窗口（秒），默认 10 秒
        """
        self.memory_window = memory_window
        # 最近说过的文本（时间戳 -> 文本）
        self._spoken_texts: Dict[str, float] = {}
        # 最近说过的场景 hash（时间戳 -> hash）
        self._spoken_scenes: Dict[str, float] = {}
        # 播报历史（时间序列）
        self._speech_history: deque = deque(maxlen=50)
    
    def record_speech(self, text: str, scene_hash: Optional[str] = None):
        """
        记录播报
        
        Args:
            text: 播报的文本
            scene_hash: 场景哈希值（可选）
        """
        timestamp = time.time()
        
        # 记录文本
        self._spoken_texts[text] = timestamp
        
        # 记录场景
        if scene_hash:
            self._spoken_scenes[scene_hash] = timestamp
        
        # 记录历史
        self._speech_history.append({
            "timestamp": timestamp,
            "text": text,
            "scene_hash": scene_hash
        })
    
    def has_spoken(self, text: str) -> bool:
        """
        检查是否在记忆窗口内说过
        
        Args:
            text: 要检查的文本
        
        Returns:
            bool: True 表示在窗口内说过，False 表示未说过或已过期
        """
        if text not in self._spoken_texts:
            return False
        
        elapsed = time.time() - self._spoken_texts[text]
        return elapsed < self.memory_window
    
    def has_spoken_scene(self, scene_hash: str) -> bool:
        """
        检查是否在记忆窗口内说过该场景
        
        Args:
            scene_hash: 场景哈希值
        
        Returns:
            bool: True 表示在窗口内说过，False 表示未说过或已过期
        """
        if scene_hash not in self._spoken_scenes:
            return False
        
        elapsed = time.time() - self._spoken_scenes[scene_hash]
        return elapsed < self.memory_window
    
    def cleanup_expired(self):
        """清理过期的记忆"""
        current_time = time.time()
        
        # 清理过期的文本记忆
        expired_texts = [
            text for text, timestamp in self._spoken_texts.items()
            if current_time - timestamp >= self.memory_window
        ]
        for text in expired_texts:
            del self._spoken_texts[text]
        
        # 清理过期的场景记忆
        expired_scenes = [
            scene_hash for scene_hash, timestamp in self._spoken_scenes.items()
            if current_time - timestamp >= self.memory_window
        ]
        for scene_hash in expired_scenes:
            del self._spoken_scenes[scene_hash]
    
    def get_recent_speech(self, count: int = 5) -> List[Dict]:
        """
        获取最近的播报历史
        
        Args:
            count: 返回的数量
        
        Returns:
            List[Dict]: 最近的播报历史
        """
        return list(self._speech_history)[-count:]
    
    def reset(self):
        """重置记忆"""
        self._spoken_texts.clear()
        self._spoken_scenes.clear()
        self._speech_history.clear()


