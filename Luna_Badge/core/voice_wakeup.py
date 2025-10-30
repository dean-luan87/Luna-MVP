#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 语音唤醒模块
借鉴小智ESP32的语音唤醒流程，实现离线唤醒词检测
"""

import logging
import asyncio
import time
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
from enum import Enum
import threading

logger = logging.getLogger(__name__)

class WakeWordStatus(Enum):
    """唤醒词状态枚举"""
    IDLE = "idle"               # 空闲
    LISTENING = "listening"     # 监听中
    DETECTING = "detecting"     # 检测中
    DETECTED = "detected"       # 已检测
    PROCESSING = "processing"   # 处理中
    SLEEP = "sleep"             # 睡眠

class VoiceWakeupEngine:
    """语音唤醒引擎"""
    
    def __init__(self, wake_words: List[str] = None):
        """
        初始化语音唤醒引擎
        
        Args:
            wake_words: 唤醒词列表，默认["你好Luna", "Luna你好"]
        """
        if wake_words is None:
            wake_words = ["你好Luna", "Luna你好", "小智小智"]
        
        self.wake_words = wake_words
        self.current_wake_word = None
        self.detection_threshold = 0.7  # 检测阈值
        self.enabled = True
        self.status = WakeWordStatus.IDLE
        
        # 唤醒回调函数
        self.wake_callbacks: List[Callable[[str], None]] = []
        
        # 检测统计
        self.detection_count = 0
        self.last_detection_time = 0.0
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"🎤 语音唤醒引擎初始化完成，唤醒词: {wake_words}")
    
    def add_wake_callback(self, callback: Callable[[str], None]):
        """
        添加唤醒回调函数
        
        Args:
            callback: 唤醒回调函数
        """
        self.wake_callbacks.append(callback)
        self.logger.info(f"✅ 添加唤醒回调函数: {callback.__name__}")
    
    async def detect_wake_word(self, audio_data: bytes) -> Optional[str]:
        """
        检测唤醒词（模拟实现）
        
        在实际实现中，这里应该调用PicoVoice或Porcupine
        
        Args:
            audio_data: 音频数据
            
        Returns:
            str: 检测到的唤醒词，如果没有则返回None
        """
        if not self.enabled or self.status == WakeWordStatus.SLEEP:
            return None
        
        # 模拟唤醒词检测
        # 实际实现应该调用唤醒词检测引擎
        # 这里简化处理，随机返回检测结果
        
        import random
        if random.random() > 0.95:  # 5%概率检测到唤醒词
            wake_word = random.choice(self.wake_words)
            return wake_word
        
        return None
    
    async def start_listening(self):
        """开始监听"""
        if self.status != WakeWordStatus.IDLE:
            return
        
        self.status = WakeWordStatus.LISTENING
        self.logger.info("🎧 开始监听唤醒词")
    
    async def stop_listening(self):
        """停止监听"""
        self.status = WakeWordStatus.IDLE
        self.logger.info("🛑 停止监听唤醒词")
    
    async def enter_sleep(self):
        """进入睡眠模式"""
        self.status = WakeWordStatus.SLEEP
        self.logger.info("😴 进入睡眠模式")
    
    async def wake_up(self):
        """唤醒"""
        if self.status == WakeWordStatus.SLEEP:
            self.status = WakeWordStatus.IDLE
            self.logger.info("🌅 唤醒系统")
    
    def set_detection_threshold(self, threshold: float):
        """设置检测阈值"""
        if 0.0 <= threshold <= 1.0:
            self.detection_threshold = threshold
            self.logger.info(f"✅ 设置检测阈值: {threshold}")
    
    async def process_audio(self, audio_data: bytes):
        """
        处理音频数据，检测唤醒词
        
        Args:
            audio_data: 音频数据
        """
        if self.status != WakeWordStatus.LISTENING:
            return
        
        self.status = WakeWordStatus.DETECTING
        
        # 检测唤醒词
        detected_word = await self.detect_wake_word(audio_data)
        
        if detected_word:
            self.status = WakeWordStatus.DETECTED
            self.detection_count += 1
            self.last_detection_time = time.time()
            self.current_wake_word = detected_word
            
            self.logger.info(f"🔔 检测到唤醒词: {detected_word}")
            
            # 调用唤醒回调
            for callback in self.wake_callbacks:
                try:
                    callback(detected_word)
                except Exception as e:
                    self.logger.error(f"❌ 唤醒回调执行失败: {e}")
            
            # 短暂延迟后恢复监听
            await asyncio.sleep(0.5)
            self.status = WakeWordStatus.LISTENING
        else:
            self.status = WakeWordStatus.LISTENING


class VoiceWakeupManager:
    """语音唤醒管理器"""
    
    def __init__(self, wake_words: List[str] = None):
        """
        初始化语音唤醒管理器
        
        Args:
            wake_words: 唤醒词列表
        """
        self.engine = VoiceWakeupEngine(wake_words)
        self.is_running = False
        self.logger = logging.getLogger(__name__)
        self.logger.info("🎙️ 语音唤醒管理器初始化完成")
    
    def add_wake_callback(self, callback: Callable[[str], None]):
        """添加唤醒回调函数"""
        self.engine.add_wake_callback(callback)
    
    async def start(self):
        """启动语音唤醒"""
        if self.is_running:
            return
        
        self.is_running = True
        await self.engine.start_listening()
        self.logger.info("🚀 语音唤醒已启动")
    
    async def stop(self):
        """停止语音唤醒"""
        if not self.is_running:
            return
        
        self.is_running = False
        await self.engine.stop_listening()
        self.logger.info("⏹️ 语音唤醒已停止")
    
    async def sleep(self):
        """睡眠"""
        await self.engine.enter_sleep()
        self.logger.info("😴 语音唤醒进入睡眠")
    
    async def wake_up(self):
        """唤醒"""
        await self.engine.wake_up()
        self.logger.info("🌅 语音唤醒已唤醒")
    
    async def process_audio(self, audio_data: bytes):
        """处理音频数据"""
        if self.is_running:
            await self.engine.process_audio(audio_data)
    
    def set_detection_threshold(self, threshold: float):
        """设置检测阈值"""
        self.engine.set_detection_threshold(threshold)
    
    def get_status(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            "enabled": self.engine.enabled,
            "status": self.engine.status.value,
            "wake_words": self.engine.wake_words,
            "detection_count": self.engine.detection_count,
            "last_detection_time": self.engine.last_detection_time
        }


# 全局语音唤醒管理器实例
global_voice_wakeup = VoiceWakeupManager()

def add_wake_callback(callback: Callable[[str], None]):
    """添加唤醒回调的便捷函数"""
    global_voice_wakeup.add_wake_callback(callback)

async def start_voice_wakeup():
    """启动语音唤醒的便捷函数"""
    await global_voice_wakeup.start()

async def stop_voice_wakeup():
    """停止语音唤醒的便捷函数"""
    await global_voice_wakeup.stop()


if __name__ == "__main__":
    # 测试语音唤醒
    import asyncio
    
    logging.basicConfig(level=logging.INFO)
    
    async def test_voice_wakeup():
        """测试语音唤醒"""
        manager = VoiceWakeupManager()
        
        # 添加唤醒回调
        def on_wakeup(wake_word: str):
            print(f"🔔 检测到唤醒词: {wake_word}")
        
        manager.add_wake_callback(on_wakeup)
        
        # 启动语音唤醒
        await manager.start()
        
        # 模拟处理音频数据
        for i in range(100):
            audio_data = b'fake audio data'
            await manager.process_audio(audio_data)
            await asyncio.sleep(0.1)
        
        # 停止语音唤醒
        await manager.stop()
    
    # 运行测试
    asyncio.run(test_voice_wakeup())
