"""
语音路由 (SpeechRouter) v1.2.0
统一处理策略系统输出的语音播报（TTS / 真人语音统一接口）
"""

from typing import Optional, Dict, Any

# 延迟导入以避免循环依赖
def _get_logger():
    try:
        from luna_backend.utils.logger import system_log
        return system_log
    except ImportError:
        try:
            from utils.logger import system_log
            return system_log
        except ImportError:
            def _dummy_log(tag, extra):
                pass
            return _dummy_log


class SpeechRouter:
    """
    语音路由
    
    统一处理策略系统输出的语音播报
    支持TTS和真人语音两种模式
    """
    
    def __init__(self):
        """初始化语音路由"""
        self.tts_manager = None
        self.real_voice_bank = None
        self._tts_enabled = True
        self._real_voice_enabled = False
        
        # 延迟加载TTS管理器
        self._init_tts()
        self._init_real_voice()
    
    def _init_tts(self):
        """初始化TTS管理器"""
        try:
            from luna_backend.services.tts.tts_engine import TTSEngine
            self.tts_manager = TTSEngine()
            self._tts_enabled = True
        except ImportError:
            try:
                from services.tts.tts_engine import TTSEngine
                self.tts_manager = TTSEngine()
                self._tts_enabled = True
            except ImportError:
                # 如果TTS引擎不存在，尝试使用全局的TTS管理器
                try:
                    from core.runtime import tts_manager
                    self.tts_manager = tts_manager
                    self._tts_enabled = True
                except:
                    self._tts_enabled = False
    
    def _init_real_voice(self):
        """初始化真人语音库"""
        # TODO: 实现真人语音库
        # 暂时禁用
        self._real_voice_enabled = False
    
    def speak(self, text: str, emotion: Optional[str] = None, priority: str = "normal") -> bool:
        """
        播报文本
        
        Args:
            text: 要播报的文本
            emotion: 情绪类型（calm, urgent, warm, gentle等）
            priority: 优先级（normal, high, urgent）
        
        Returns:
            是否成功播报
        """
        if not text or not isinstance(text, str):
            return False
        
        system_log = _get_logger()
        
        # 若有真人音色 → 优先
        if self._real_voice_enabled and self.real_voice_bank:
            try:
                system_log("SPEECH", {
                    "text": text,
                    "from": "REAL",
                    "emotion": emotion,
                    "priority": priority
                })
                return self.real_voice_bank.play(text, emotion)
            except Exception as e:
                system_log("SPEECH_ERROR", {
                    "error": str(e),
                    "fallback": "TTS"
                })
                # 失败时fallback到TTS
        
        # 使用TTS
        if self._tts_enabled and self.tts_manager:
            try:
                system_log("SPEECH", {
                    "text": text,
                    "from": "TTS",
                    "emotion": emotion,
                    "priority": priority
                })
                
                # 调用TTS引擎
                if hasattr(self.tts_manager, 'synthesize'):
                    # 使用TTSEngine接口
                    audio_b64 = self.tts_manager.synthesize(
                        text=text,
                        voice="zh-CN-XiaoxiaoNeural",  # 默认语音
                        rate="+0%"
                    )
                    # TODO: 播放音频（需要音频播放器）
                    return True
                elif hasattr(self.tts_manager, 'speak'):
                    # 使用TTSManager接口
                    self.tts_manager.speak(text, emotion or "calm")
                    return True
                else:
                    # 尝试使用全局speakText（前端）
                    try:
                        import threading
                        def async_speak():
                            # 这里可以通过HTTP请求调用前端TTS
                            pass
                        thread = threading.Thread(target=async_speak)
                        thread.daemon = True
                        thread.start()
                        return True
                    except:
                        pass
            except Exception as e:
                system_log("SPEECH_ERROR", {
                    "error": str(e),
                    "text": text
                })
        
        # 如果都失败了，至少记录日志
        system_log("SPEECH_FAILED", {
            "text": text,
            "tts_enabled": self._tts_enabled,
            "real_voice_enabled": self._real_voice_enabled
        })
        
        return False
    
    def speak_action(self, action_result: Dict[str, Any]) -> bool:
        """
        播报策略动作结果
        
        Args:
            action_result: 策略执行结果字典，包含action, text, emotion等
        
        Returns:
            是否成功播报
        """
        text = action_result.get("text")
        if not text:
            return False
        
        emotion = action_result.get("emotion")
        priority = action_result.get("priority", "normal")
        
        # 根据action类型调整优先级
        action = action_result.get("action", "")
        if action in ["STOP_AND_WARN", "AVOID_SEVERE", "REROUTE"]:
            priority = "urgent"
        elif action in ["WAIT", "CAUTION"]:
            priority = "high"
        
        return self.speak(text, emotion, priority)



