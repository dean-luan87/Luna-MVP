"""
TTS 和 OCR 模拟模块
用于测试中模拟 TTS 和 OCR 行为
"""
from typing import List, Optional


class MockTTSManager:
    """模拟 TTS 管理器"""
    
    _instance: Optional["MockTTSManager"] = None
    _speak_calls: List[str] = []
    
    def __init__(self):
        self.speak_count = 0
    
    @classmethod
    def get_instance(cls) -> "MockTTSManager":
        """获取单例"""
        if cls._instance is None:
            cls._instance = MockTTSManager()
        return cls._instance
    
    @classmethod
    def speak(cls, message: str) -> None:
        """播报消息（模拟）"""
        cls._speak_calls.append(message)
        if cls._instance:
            cls._instance.speak_count += 1
    
    @classmethod
    def clear_calls(cls) -> None:
        """清空调用记录"""
        cls._speak_calls.clear()
        if cls._instance:
            cls._instance.speak_count = 0
    
    @classmethod
    def get_calls(cls) -> List[str]:
        """获取所有调用记录"""
        return cls._speak_calls.copy()


class MockOCRManager:
    """模拟 OCR 管理器"""
    
    _instance: Optional["MockOCRManager"] = None
    _paused = False
    
    def __init__(self):
        self.pause_count = 0
        self.resume_count = 0
    
    @classmethod
    def get_instance(cls) -> "MockOCRManager":
        """获取单例"""
        if cls._instance is None:
            cls._instance = MockOCRManager()
        return cls._instance
    
    @classmethod
    def pause(cls) -> None:
        """暂停 OCR（模拟）"""
        cls._paused = True
        if cls._instance:
            cls._instance.pause_count += 1
    
    @classmethod
    def resume(cls) -> None:
        """恢复 OCR（模拟）"""
        cls._paused = False
        if cls._instance:
            cls._instance.resume_count += 1
    
    @classmethod
    def is_paused(cls) -> bool:
        """检查是否暂停"""
        return cls._paused
















