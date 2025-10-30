#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 离线语音识别模块
接入本地语音识别模型，实现基础命令识别
"""

import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time

logger = logging.getLogger(__name__)

class VoiceIntent(Enum):
    """语音意图"""
    FORWARD = "forward"              # 向前
    BACKWARD = "backward"            # 向后
    STOP = "stop"                   # 停止
    DANGER = "danger"               # 危险
    EDGE_SIDE = "edge_side"         # 靠边
    SLOW_DOWN = "slow_down"         # 减速
    HELP = "help"                   # 求助
    UNKNOWN = "unknown"             # 未知

@dataclass
class VoiceCommand:
    """语音命令"""
    intent: VoiceIntent              # 意图
    keywords: List[str]              # 识别到的关键词
    confidence: float                # 置信度
    raw_text: str                   # 原始文本
    timestamp: float                # 时间戳
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "intent": self.intent.value,
            "keywords": self.keywords,
            "confidence": self.confidence,
            "raw_text": self.raw_text,
            "timestamp": self.timestamp
        }

class VoiceRecognitionEngine:
    """离线语音识别引擎"""
    
    def __init__(self):
        """初始化语音识别引擎"""
        self.logger = logging.getLogger(__name__)
        
        # 关键词映射
        self.keyword_mapping = {
            VoiceIntent.FORWARD: [
                "向前", "前进", "继续", "直走",
                "forward", "go ahead", "continue"
            ],
            VoiceIntent.BACKWARD: [
                "向后", "后退", "往回走",
                "backward", "go back"
            ],
            VoiceIntent.STOP: [
                "停止", "停下", "暂停",
                "stop", "halt"
            ],
            VoiceIntent.DANGER: [
                "危险", "注意", "小心",
                "danger", "caution", "warning"
            ],
            VoiceIntent.EDGE_SIDE: [
                "靠边", "靠右边", "靠左边",
                "edge", "side"
            ],
            VoiceIntent.SLOW_DOWN: [
                "减速", "慢点", "慢下来",
                "slow down", "slow"
            ],
            VoiceIntent.HELP: [
                "帮助", "求助", "救命",
                "help", "assist", "rescue"
            ]
        }
        
        # 预留的真实引擎接口
        self.recognition_engine = None  # Vosk或PicoVoice引擎
        
        self.logger.info("🎤 离线语音识别引擎初始化完成")
    
    def recognize(self, audio_data: bytes = None, text: str = None) -> VoiceCommand:
        """
        识别语音命令
        
        Args:
            audio_data: 音频数据
            text: 文本（用于模拟）
            
        Returns:
            VoiceCommand: 语音命令
        """
        # 如果有真实引擎，使用真实引擎
        if self.recognition_engine and audio_data:
            recognized_text = self._recognize_with_engine(audio_data)
        else:
            # 模拟识别
            recognized_text = text or self._simulate_recognition()
        
        # 解析意图
        intent, keywords, confidence = self._parse_intent(recognized_text)
        
        command = VoiceCommand(
            intent=intent,
            keywords=keywords,
            confidence=confidence,
            raw_text=recognized_text,
            timestamp=time.time()
        )
        
        self.logger.info(f"🎤 识别结果: {intent.value}, "
                        f"关键词={keywords}, 置信度={confidence:.2f}")
        
        return command
    
    def _recognize_with_engine(self, audio_data: bytes) -> str:
        """
        使用真实引擎识别（预留接口）
        
        Args:
            audio_data: 音频数据
            
        Returns:
            str: 识别到的文本
        """
        # TODO: 集成Vosk或PicoVoice
        # if self.recognition_engine is None:
        #     self.recognition_engine = init_vosk_engine()
        # 
        # result = self.recognition_engine.recognize(audio_data)
        # return result.get('text', '')
        
        return ""
    
    def _simulate_recognition(self) -> str:
        """模拟识别（用于测试）"""
        # 返回空字符串，由外部传入text
        return ""
    
    def _parse_intent(self, text: str) -> Tuple[VoiceIntent, List[str], float]:
        """
        解析语音意图
        
        Args:
            text: 识别的文本
            
        Returns:
            Tuple[VoiceIntent, List[str], float]: (意图, 关键词列表, 置信度)
        """
        text_lower = text.lower()
        
        # 搜索匹配的关键词
        matched_intents = []
        matched_keywords = []
        
        for intent, keywords in self.keyword_mapping.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    matched_intents.append(intent)
                    matched_keywords.append(keyword)
                    break
        
        if not matched_intents:
            return VoiceIntent.UNKNOWN, [], 0.0
        
        # 选择最匹配的意图（如果多个匹配，选择第一个）
        intent = matched_intents[0]
        keywords = [k for k in matched_keywords if k]
        confidence = 0.9 if len(matched_keywords) > 0 else 0.5
        
        return intent, keywords, confidence


# 全局识别引擎实例
global_voice_recognition = VoiceRecognitionEngine()

def recognize_voice(audio_data: bytes = None, text: str = None) -> VoiceCommand:
    """识别语音的便捷函数"""
    return global_voice_recognition.recognize(audio_data, text)


if __name__ == "__main__":
    # 测试语音识别
    import logging
    logging.basicConfig(level=logging.INFO)
    
    engine = VoiceRecognitionEngine()
    
    print("=" * 60)
    print("🎤 离线语音识别测试")
    print("=" * 60)
    
    # 测试不同的命令
    test_cases = [
        ("向前走", VoiceIntent.FORWARD),
        ("停止", VoiceIntent.STOP),
        ("危险", VoiceIntent.DANGER),
        ("靠边", VoiceIntent.EDGE_SIDE),
        ("减速", VoiceIntent.SLOW_DOWN),
        ("帮助", VoiceIntent.HELP),
    ]
    
    for text, expected_intent in test_cases:
        result = engine.recognize(text=text)
        status = "✅" if result.intent == expected_intent else "❌"
        print(f"{status} '{text}' → {result.intent.value} "
              f"(置信度: {result.confidence:.2f})")
    
    print("\n" + "=" * 60)
