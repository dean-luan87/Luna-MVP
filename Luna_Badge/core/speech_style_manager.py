#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 播报策略控制器模块
根据路径评估结果和环境场景，控制TTS播报的风格（语气/情绪）
"""

import logging
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)

class SpeechStyle(Enum):
    """播报风格"""
    CHEERFUL = "cheerful"       # 轻松提示
    DEFAULT = "default"         # 默认
    EMPATHETIC = "empathetic"   # 关切建议
    SERIOUS = "serious"         # 紧急指令
    GENTLE = "gentle"           # 温和引导
    URGENT = "urgent"           # 紧急警告

class PathStatus(Enum):
    """路径状态"""
    NORMAL = "normal"
    CAUTION = "caution"
    REROUTE = "reroute"
    STOP = "stop"

@dataclass
class TTSConfig:
    """TTS配置"""
    voice: str
    style: str
    rate: float
    pitch: float
    volume: float
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "voice": self.voice,
            "style": self.style,
            "rate": self.rate,
            "pitch": self.pitch,
            "volume": self.volume
        }

@dataclass
class SpeechStyleOutput:
    """播报风格输出"""
    speech_style: SpeechStyle
    tts_config: TTSConfig
    urgency: str                   # 紧急程度
    message_template: str          # 消息模板
    timestamp: float               # 时间戳
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        output = {
            "speech_style": self.speech_style.value,
            "tts_config": self.tts_config.to_dict(),
            "urgency": self.urgency,
            "message_template": self.message_template,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.timestamp))
        }
        return json.dumps(output, ensure_ascii=False, indent=2)

class SpeechStyleManager:
    """播报策略控制器"""
    
    def __init__(self):
        """初始化播报策略控制器"""
        self.logger = logging.getLogger(__name__)
        
        # 路径状态到播报风格的映射
        self.style_mapping = {
            PathStatus.NORMAL: {
                "style": SpeechStyle.CHEERFUL,
                "voice": "zh-CN-XiaoxiaoNeural",
                "rate": 1.0,
                "pitch": 1.0,
                "urgency": "low",
                "template": "✅ {message}"
            },
            PathStatus.CAUTION: {
                "style": SpeechStyle.GENTLE,
                "voice": "zh-CN-YunxiNeural",
                "rate": 0.95,
                "pitch": 0.95,
                "urgency": "medium",
                "template": "⚠️ {message}"
            },
            PathStatus.REROUTE: {
                "style": SpeechStyle.EMPATHETIC,
                "voice": "zh-CN-XiaoxiaoNeural",
                "rate": 0.9,
                "pitch": 0.9,
                "urgency": "high",
                "template": "🔴 {message}"
            },
            PathStatus.STOP: {
                "style": SpeechStyle.SERIOUS,
                "voice": "zh-CN-YunjianNeural",
                "rate": 1.3,
                "pitch": 1.2,
                "urgency": "critical",
                "template": "🚨 {message}"
            }
        }
        
        self.logger.info("🎙️ 播报策略控制器初始化完成")
    
    def get_speech_style(self, 
                        path_status: str,
                        danger_level: Optional[str] = None,
                        object_type: Optional[str] = None,
                        emotion_tag: Optional[str] = None,
                        user_hesitation: bool = False) -> SpeechStyleOutput:
        """
        根据路径状态获取播报风格（支持情绪联动）
        
        Args:
            path_status: 路径状态 (normal/caution/reroute/stop)
            danger_level: 危险等级（可选）
            object_type: 对象类型（如"排队人群"）（可选）
            emotion_tag: 情绪标签（anxious/stressed/calm/confident等）（可选）
            user_hesitation: 用户是否存在迟疑/停顿（可选）
            
        Returns:
            SpeechStyleOutput: 播报风格输出
        """
        # 确定路径状态
        status = self._parse_status(path_status)
        
        # 获取基础配置
        base_config = self.style_mapping.get(status, self.style_mapping[PathStatus.NORMAL])
        
        # 根据危险等级和对象类型调整
        if danger_level == "critical":
            # 提升紧急程度
            base_config["style"] = SpeechStyle.URGENT
            base_config["rate"] = 1.5
            base_config["pitch"] = 1.3
        
        # 情绪联动调整
        if emotion_tag:
            base_config = self._adjust_for_emotion(base_config, emotion_tag)
        
        # 用户迟疑检测 - 如果检测到迟疑，放慢语速，更柔和
        if user_hesitation:
            base_config["rate"] = max(0.5, base_config["rate"] * 0.8)  # 降低20%语速
            base_config["pitch"] = max(0.8, base_config["pitch"] * 0.9)  # 降低音调
            if base_config["style"] != SpeechStyle.GENTLE:
                base_config["style"] = SpeechStyle.GENTLE  # 切换到温和风格
            self.logger.info("🎙️ 检测到用户迟疑，切换为温和播报")
        
        # 构建消息模板
        message_template = self._build_template(base_config["template"], object_type)
        
        # 创建输出
        output = SpeechStyleOutput(
            speech_style=base_config["style"],
            tts_config=TTSConfig(
                voice=base_config["voice"],
                style=base_config["style"].value,
                rate=base_config["rate"],
                pitch=base_config["pitch"],
                volume=1.0
            ),
            urgency=base_config["urgency"],
            message_template=message_template,
            timestamp=time.time()
        )
        
        self.logger.info(f"🎙️ 播报风格: {output.speech_style.value}, "
                        f"紧急程度: {output.urgency}")
        
        return output
    
    def _adjust_for_emotion(self, base_config: Dict[str, Any], emotion_tag: str) -> Dict[str, Any]:
        """
        根据情绪标签调整播报风格
        
        Args:
            base_config: 基础配置
            emotion_tag: 情绪标签
        
        Returns:
            Dict[str, Any]: 调整后的配置
        """
        # 创建配置副本
        config = base_config.copy()
        
        # 情绪到风格的映射
        emotion_adjustments = {
            "anxious": {
                "style": SpeechStyle.GENTLE,
                "rate_multiplier": 0.85,
                "pitch_multiplier": 0.9
            },
            "stressed": {
                "style": SpeechStyle.EMPATHETIC,
                "rate_multiplier": 0.9,
                "pitch_multiplier": 0.95
            },
            "calm": {
                "style": SpeechStyle.CHEERFUL,
                "rate_multiplier": 1.0,
                "pitch_multiplier": 1.0
            },
            "confident": {
                "style": SpeechStyle.CHEERFUL,
                "rate_multiplier": 1.1,
                "pitch_multiplier": 1.05
            },
            "frustrated": {
                "style": SpeechStyle.EMPATHETIC,
                "rate_multiplier": 0.9,
                "pitch_multiplier": 0.9
            }
        }
        
        if emotion_tag.lower() in emotion_adjustments:
            adjustment = emotion_adjustments[emotion_tag.lower()]
            config["style"] = adjustment["style"]
            config["rate"] = config.get("rate", 1.0) * adjustment["rate_multiplier"]
            config["pitch"] = config.get("pitch", 1.0) * adjustment["pitch_multiplier"]
            self.logger.info(f"🎙️ 根据情绪 '{emotion_tag}' 调整播报风格")
        
        return config
    
    def _parse_status(self, status_str: str) -> PathStatus:
        """解析路径状态字符串"""
        try:
            return PathStatus(status_str.lower())
        except ValueError:
            return PathStatus.NORMAL
    
    def _build_template(self, base_template: str, object_type: Optional[str] = None) -> str:
        """构建消息模板"""
        if object_type:
            # 根据对象类型调整模板
            templates = {
                "排队人群": "前方有{object_type}，建议{action}",
                "逆向人流": "当前存在大量逆向人流，建议靠边行走",
                "危险环境": "检测到{object_type}，请注意安全",
                "门牌反序": "门牌号反序，可能走错方向，请重新确认路线"
            }
            
            if object_type in templates:
                return templates[object_type]
        
        return base_template.replace("{message}", "{content}")
    
    def format_message(self, content: str, style_output: SpeechStyleOutput) -> str:
        """
        格式化消息
        
        Args:
            content: 消息内容
            style_output: 风格输出
            
        Returns:
            str: 格式化后的消息
        """
        template = style_output.message_template
        
        # 根据紧急程度添加前缀
        if style_output.urgency == "critical":
            return f"🚨紧急：{content}"
        elif style_output.urgency == "high":
            return f"🔴{content}"
        elif style_output.urgency == "medium":
            return f"⚠️{content}"
        else:
            return f"✅{content}"


# 全局管理器实例
global_speech_style_manager = SpeechStyleManager()

def get_speech_style(path_status: str, **kwargs) -> SpeechStyleOutput:
    """获取播报风格的便捷函数"""
    return global_speech_style_manager.get_speech_style(path_status, **kwargs)


if __name__ == "__main__":
    # 测试播报策略控制器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    manager = SpeechStyleManager()
    
    print("=" * 70)
    print("🎙️ 播报策略控制器测试")
    print("=" * 70)
    
    # 测试不同路径状态
    test_cases = [
        ("normal", None, None),
        ("caution", "low", "人群密集"),
        ("reroute", "high", "逆向人流"),
        ("stop", "critical", "严重危险")
    ]
    
    for status, danger, obj_type in test_cases:
        print(f"\n测试: path_status={status}, danger={danger}, object={obj_type}")
        result = manager.get_speech_style(status, danger, obj_type)
        print(result.to_json())
    
    print("\n" + "=" * 70)

