# -*- coding: utf-8 -*-
"""
音频播放互斥锁（Audio Gate）

目标：确保任意时刻最多只有 1 个 TTS 在播
测试期策略：新播报不能打断旧播报，如果正在播就放弃
"""

import threading
import logging

logger = logging.getLogger(__name__)

# 全局音频锁（播放级总闸）
AUDIO_LOCK = threading.Lock()


def acquire_audio_lock(blocking: bool = False) -> bool:
    """
    尝试获取音频锁
    
    Args:
        blocking: 是否阻塞等待
            - False: 非阻塞，获取不到立即返回 False（测试期策略）
            - True: 阻塞等待直到获取到锁
    
    Returns:
        bool: 是否成功获取锁
    """
    if blocking:
        AUDIO_LOCK.acquire()
        return True
    else:
        # 非阻塞：测试期宁可少播，不可乱播
        acquired = AUDIO_LOCK.acquire(blocking=False)
        if not acquired:
            logger.debug("[AudioGate] 音频设备被占用，放弃本次播报")
        return acquired


def release_audio_lock():
    """释放音频锁"""
    try:
        AUDIO_LOCK.release()
    except Exception as e:
        logger.warning(f"[AudioGate] 释放锁失败: {e}")


def is_audio_available() -> bool:
    """
    检查音频设备是否可用（非阻塞）
    
    Returns:
        bool: True 表示可以立即播报，False 表示正在播报中
    """
    acquired = AUDIO_LOCK.acquire(blocking=False)
    if acquired:
        AUDIO_LOCK.release()
        return True
    return False


