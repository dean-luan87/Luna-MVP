#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音合成引擎模块
支持多种 TTS 后端：edge-tts, pyttsx3
"""

import os
import sys
from typing import Optional, Dict, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTSEngine:
    """语音合成引擎类"""
    
    def __init__(self, engine_type: str = "auto", **kwargs):
        """
        初始化 TTS 引擎
        
        Args:
            engine_type: 引擎类型 ("edge-tts", "pyttsx3", "auto")
            **kwargs: 引擎特定参数
        """
        self.engine_type = engine_type
        self.engine = None
        self.config = kwargs
        
        # 可用引擎列表
        self.available_engines = []
        self._detect_available_engines()
        
        # 初始化引擎
        self._init_engine()
    
    def _detect_available_engines(self):
        """检测可用的 TTS 引擎"""
        # 检测 edge-tts
        try:
            import edge_tts
            self.available_engines.append("edge-tts")
            logger.info("✅ edge-tts 可用")
        except ImportError:
            logger.warning("⚠️ edge-tts 不可用，请安装: pip install edge-tts")
        
        # 检测 pyttsx3
        try:
            import pyttsx3
            self.available_engines.append("pyttsx3")
            logger.info("✅ pyttsx3 可用")
        except ImportError:
            logger.warning("⚠️ pyttsx3 不可用，请安装: pip install pyttsx3")
    
    def _init_engine(self):
        """初始化 TTS 引擎"""
        if self.engine_type == "auto":
            # 自动选择最佳引擎
            if "edge-tts" in self.available_engines:
                self.engine_type = "edge-tts"
            elif "pyttsx3" in self.available_engines:
                self.engine_type = "pyttsx3"
            else:
                raise RuntimeError("❌ 没有可用的 TTS 引擎")
        
        if self.engine_type == "edge-tts":
            self._init_edge_tts()
        elif self.engine_type == "pyttsx3":
            self._init_pyttsx3()
        else:
            raise ValueError(f"❌ 不支持的引擎类型: {self.engine_type}")
    
    def _init_edge_tts(self):
        """初始化 edge-tts 引擎"""
        try:
            import edge_tts
            self.engine = edge_tts
            logger.info("🎯 使用 edge-tts 引擎")
        except ImportError:
            raise ImportError("❌ edge-tts 未安装")
    
    def _init_pyttsx3(self):
        """初始化 pyttsx3 引擎"""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            
            # 配置语音参数
            voices = self.engine.getProperty('voices')
            if voices:
                # 尝试选择中文语音
                for voice in voices:
                    if 'chinese' in voice.name.lower() or 'zh' in voice.id.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
            
            # 设置语速和音量
            self.engine.setProperty('rate', self.config.get('rate', 150))
            self.engine.setProperty('volume', self.config.get('volume', 0.8))
            
            logger.info("🎯 使用 pyttsx3 引擎")
        except ImportError:
            raise ImportError("❌ pyttsx3 未安装")
    
    async def synthesize_edge_tts(self, text: str, voice: str = "zh-CN-XiaoxiaoNeural", 
                                output_file: Optional[str] = None) -> bytes:
        """
        使用 edge-tts 合成语音
        
        Args:
            text: 要合成的文本
            voice: 语音模型
            output_file: 输出文件路径
            
        Returns:
            音频数据 (bytes)
        """
        communicate = self.engine.Communicate(text, voice)
        
        if output_file:
            await communicate.save(output_file)
            logger.info(f"💾 语音文件已保存: {output_file}")
            return b""
        else:
            # 返回音频数据
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return audio_data
    
    def synthesize_pyttsx3(self, text: str, output_file: Optional[str] = None):
        """
        使用 pyttsx3 合成语音
        
        Args:
            text: 要合成的文本
            output_file: 输出文件路径
        """
        if output_file:
            # pyttsx3 不支持直接保存到文件，需要其他方法
            logger.warning("⚠️ pyttsx3 不支持直接保存到文件")
            return
        
        # 直接播放
        self.engine.say(text)
        self.engine.runAndWait()
        logger.info(f"🔊 已播放: {text}")
    
    async def synthesize(self, text: str, voice: str = "zh-CN-XiaoxiaoNeural", 
                        output_file: Optional[str] = None) -> Optional[bytes]:
        """
        通用语音合成接口
        
        Args:
            text: 要合成的文本
            voice: 语音模型 (edge-tts 有效)
            output_file: 输出文件路径
            
        Returns:
            音频数据 (edge-tts) 或 None (pyttsx3)
        """
        if not text.strip():
            logger.warning("⚠️ 文本为空，跳过合成")
            return None
        
        logger.info(f"🎤 开始合成语音: {text[:50]}...")
        
        try:
            if self.engine_type == "edge-tts":
                return await self.synthesize_edge_tts(text, voice, output_file)
            elif self.engine_type == "pyttsx3":
                self.synthesize_pyttsx3(text, output_file)
                return None
        except Exception as e:
            logger.error(f"❌ 语音合成失败: {e}")
            return None
    
    def get_available_voices(self) -> Dict[str, Any]:
        """获取可用的语音列表"""
        if self.engine_type == "edge-tts":
            # edge-tts 的语音列表
            return {
                "zh-CN-XiaoxiaoNeural": "中文(普通话，女声)",
                "zh-CN-YunxiNeural": "中文(普通话，男声)",
                "zh-CN-YunyangNeural": "中文(普通话，男声)",
                "en-US-AriaNeural": "英语(美式，女声)",
                "en-US-GuyNeural": "英语(美式，男声)"
            }
        elif self.engine_type == "pyttsx3":
            # pyttsx3 的语音列表
            voices = self.engine.getProperty('voices')
            voice_dict = {}
            for i, voice in enumerate(voices):
                voice_dict[voice.id] = voice.name
            return voice_dict
        return {}
    
    def set_voice(self, voice_id: str):
        """设置语音"""
        if self.engine_type == "pyttsx3":
            self.engine.setProperty('voice', voice_id)
            logger.info(f"🎵 语音已设置为: {voice_id}")
    
    def set_rate(self, rate: int):
        """设置语速"""
        if self.engine_type == "pyttsx3":
            self.engine.setProperty('rate', rate)
            logger.info(f"⚡ 语速已设置为: {rate}")
    
    def set_volume(self, volume: float):
        """设置音量"""
        if self.engine_type == "pyttsx3":
            self.engine.setProperty('volume', volume)
            logger.info(f"🔊 音量已设置为: {volume}")


# 便捷函数
async def create_tts_engine(engine_type: str = "auto", **kwargs) -> TTSEngine:
    """创建 TTS 引擎实例"""
    return TTSEngine(engine_type, **kwargs)


if __name__ == "__main__":
    # 测试代码
    import asyncio
    
    async def test_tts():
        try:
            tts = await create_tts_engine()
            await tts.synthesize("你好，我是 Luna 语音助手")
            print("✅ TTS 测试成功")
        except Exception as e:
            print(f"❌ TTS 测试失败: {e}")
    
    asyncio.run(test_tts())