"""
Emergency Voice Layer
1.4.1-failsafe.3: 应急播报层
在进入应急模式时提供语音提示（带节流机制）
"""
import time
from typing import Optional

from core.logging.log_manager import LogManager

# 预留的播报通道
try:
    from core.tts.tts_manager import TTSManager
    TTS_AVAILABLE = True
except (ImportError, AttributeError):
    TTSManager = None
    TTS_AVAILABLE = False


class EmergencyVoiceLayer:
    """
    v1: 应急播报层
    
    功能：
    - 仅播报一次，防抖 10 秒
    - 不依赖具体 TTS（若无法加载 TTSManager，则仅打印日志）
    - 保证稳定，不对 FailSafeManager 造成阻塞
    
    设计原则：
    - 非阻塞
    - 防御性编程（TTS 不存在时不影响）
    - 节流机制防止频繁播报
    """
    
    _instance: Optional["EmergencyVoiceLayer"] = None
    
    def __init__(self, min_interval: float = 10.0):
        """
        初始化应急语音层
        
        Args:
            min_interval: 最小播报间隔（秒），默认 10 秒
        """
        self.logger = LogManager.get_logger("EmergencyVoiceLayer")
        self.last_play_ts = 0.0
        self.min_interval = min_interval
        self.play_count = 0

    @classmethod
    def get_instance(cls, min_interval: float = 10.0) -> "EmergencyVoiceLayer":
        """
        获取单例实例
        
        Args:
            min_interval: 最小播报间隔（秒）
        
        Returns:
            EmergencyVoiceLayer 实例
        """
        if cls._instance is None:
            cls._instance = EmergencyVoiceLayer(min_interval=min_interval)
        return cls._instance

    def play(self, message: str) -> bool:
        """
        播报应急消息
        
        Args:
            message: 要播报的消息
        
        Returns:
            True 如果成功播报，False 如果被节流或失败
        """
        now = time.time()
        
        # 节流检查
        if now - self.last_play_ts < self.min_interval:
            self.logger.debug(f"[EmergencyVoice] Throttled (last_play: {self.last_play_ts:.1f}s ago)")
            return False

        self.last_play_ts = now
        self.play_count += 1
        self.logger.warning(f"[EmergencyVoice] {message}")

        # 尝试使用 TTS 播报
        if TTS_AVAILABLE and TTSManager is not None:
            try:
                # 假设 TTSManager 有 speak 方法
                if hasattr(TTSManager, 'speak'):
                    TTSManager.speak(message)
                    self.logger.info("[EmergencyVoice] TTS playback successful")
                    return True
                else:
                    self.logger.warning("[EmergencyVoice] TTSManager.speak() not available")
            except Exception as e:
                self.logger.error(f"[EmergencyVoice] TTS failed: {e}")
        else:
            self.logger.info("[EmergencyVoice] TTSManager not available, using log only")

        return True

    def get_stats(self) -> dict:
        """
        获取统计信息
        
        Returns:
            包含播报次数等统计信息的字典
        """
        return {
            "play_count": self.play_count,
            "last_play_ts": self.last_play_ts,
            "tts_available": TTS_AVAILABLE,
        }

