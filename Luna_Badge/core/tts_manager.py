#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge TTS管理器模块
支持播报风格根据情绪/场景切换
"""

import logging
import asyncio
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import time

logger = logging.getLogger(__name__)

class TTSStyle(Enum):
    """TTS播报风格"""
    CHEERFUL = "cheerful"       # 欢快
    EMPATHETIC = "empathetic"   # 共情
    ANGRY = "angry"            # 愤怒
    CALM = "calm"              # 平静
    URGENT = "urgent"          # 紧急
    GENTLE = "gentle"          # 温和

class DangerLevel(Enum):
    """危险等级"""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class TTSConfig:
    """TTS配置"""
    style: TTSStyle
    voice: str
    rate: float                 # 语速
    pitch: float                # 音调
    volume: float               # 音量
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "style": self.style.value,
            "voice": self.voice,
            "rate": self.rate,
            "pitch": self.pitch,
            "volume": self.volume
        }

class TTSManager:
    """TTS管理器"""
    
    def __init__(self):
        """初始化TTS管理器"""
        self.logger = logging.getLogger(__name__)
        
        # 风格配置
        self.style_configs = {
            TTSStyle.CHEERFUL: {
                "voice": "zh-CN-XiaoxiaoNeural",
                "rate": 1.2,
                "pitch": 1.1
            },
            TTSStyle.EMPATHETIC: {
                "voice": "zh-CN-YunxiNeural",
                "rate": 0.9,
                "pitch": 0.95
            },
            TTSStyle.ANGRY: {
                "voice": "zh-CN-YunjianNeural",
                "rate": 1.3,
                "pitch": 1.2
            },
            TTSStyle.CALM: {
                "voice": "zh-CN-XiaoyiNeural",
                "rate": 0.95,
                "pitch": 1.0
            },
            TTSStyle.URGENT: {
                "voice": "zh-CN-XiaoxiaoNeural",
                "rate": 1.5,
                "pitch": 1.3
            },
            TTSStyle.GENTLE: {
                "voice": "zh-CN-YunxiNeural",
                "rate": 0.85,
                "pitch": 0.9
            }
        }
        
        # 默认配置
        self.default_config = TTSConfig(
            style=TTSStyle.CHEERFUL,
            voice="zh-CN-XiaoxiaoNeural",
            rate=1.0,
            pitch=1.0,
            volume=1.0
        )
        
        self.logger.info("🗣️ TTS管理器初始化完成")
    
    def select_style_for_danger(self, danger_level: DangerLevel) -> TTSStyle:
        """
        根据危险等级选择风格
        
        Args:
            danger_level: 危险等级
            
        Returns:
            TTSStyle: 播报风格
        """
        style_map = {
            DangerLevel.SAFE: TTSStyle.CHEERFUL,
            DangerLevel.LOW: TTSStyle.CALM,
            DangerLevel.MEDIUM: TTSStyle.GENTLE,
            DangerLevel.HIGH: TTSStyle.URGENT,
            DangerLevel.CRITICAL: TTSStyle.ANGRY
        }
        
        return style_map.get(danger_level, TTSStyle.CALM)
    
    def select_style_for_crowd_density(self, density: str) -> TTSStyle:
        """
        根据人群密度选择风格
        
        Args:
            density: 密度（sparse/normal/crowded/very_crowded）
            
        Returns:
            TTSStyle: 播报风格
        """
        if density == "very_crowded":
            return TTSStyle.URGENT
        elif density == "crowded":
            return TTSStyle.CALM
        else:
            return TTSStyle.CHEERFUL
    
    def get_config(self, style: TTSStyle) -> TTSConfig:
        """
        获取指定风格的配置
        
        Args:
            style: 播报风格
            
        Returns:
            TTSConfig: TTS配置
        """
        style_config = self.style_configs.get(style, self.style_configs[TTSStyle.CHEERFUL])
        
        return TTSConfig(
            style=style,
            voice=style_config["voice"],
            rate=style_config["rate"],
            pitch=style_config["pitch"],
            volume=1.0
        )
    
    async def speak(self, text: str, style: TTSStyle = TTSStyle.CHEERFUL) -> bool:
        """
        语音播报
        
        Args:
            text: 要播报的文本
            style: 播报风格
            
        Returns:
            bool: 是否成功
        """
        try:
            # 获取配置
            config = self.get_config(style)
            
            # 使用edge-tts播报
            import edge_tts
            communicate = edge_tts.Communicate(
                text=text,
                voice=config.voice,
                rate=config.rate
            )
            
            # 保存为临时文件
            output_file = f"temp_output_{int(time.time())}.mp3"
            await communicate.save(output_file)
            
            # 播报（使用系统命令）
            os.system(f"afplay {output_file}")  # macOS
            
            # 删除临时文件
            os.remove(output_file)
            
            self.logger.info(f"🗣️ 播报: {text} (风格: {style.value})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 播报失败: {e}")
            return False
    
    def speak_sync(self, text: str, style: TTSStyle = TTSStyle.CHEERFUL):
        """同步播报（简化版）"""
        # 使用系统say命令
        style_text = style.value
        os.system(f'say -v Ting-Ting "{text}"')  # macOS中文语音
        self.logger.info(f"🗣️ 播报: {text} (风格: {style.value})")


# 全局TTS管理器实例
global_tts_manager = TTSManager()

def speak(text: str, style: TTSStyle = TTSStyle.CHEERFUL) -> None:
    """播报的便捷函数"""
    global_tts_manager.speak_sync(text, style)


if __name__ == "__main__":
    # 测试TTS管理器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    manager = TTSManager()
    
    print("=" * 60)
    print("🗣️ TTS管理器测试")
    print("=" * 60)
    
    # 测试不同风格
    print("\n1. 不同危险等级的风格选择")
    for danger in [DangerLevel.SAFE, DangerLevel.MEDIUM, DangerLevel.CRITICAL]:
        style = manager.select_style_for_danger(danger)
        print(f"  {danger.value} → {style.value}")
    
    # 测试不同人群密度
    print("\n2. 不同人群密度的风格选择")
    for density in ["sparse", "normal", "crowded", "very_crowded"]:
        style = manager.select_style_for_crowd_density(density)
        print(f"  {density} → {style.value}")
    
    # 测试播报配置
    print("\n3. 获取播报配置")
    config = manager.get_config(TTSStyle.URGENT)
    print(f"  风格: {config.style.value}")
    print(f"  语音: {config.voice}")
    print(f"  语速: {config.rate}")
    print(f"  音调: {config.pitch}")
    
    print("\n" + "=" * 60)
