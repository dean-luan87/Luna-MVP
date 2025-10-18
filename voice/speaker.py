#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音播报模块
统一的语音播报接口，支持多种后端
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from .tts_engine import TTSEngine

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Speaker:
    """语音播报器类"""
    
    def __init__(self, engine_type: str = "auto", **kwargs):
        """
        初始化语音播报器
        
        Args:
            engine_type: TTS 引擎类型
            **kwargs: TTS 引擎参数
        """
        self.tts_engine = None
        self.engine_type = engine_type
        self.config = kwargs
        self.is_initialized = False
        
        # 初始化 TTS 引擎
        self._init_tts_engine()
    
    def _init_tts_engine(self):
        """初始化 TTS 引擎"""
        try:
            self.tts_engine = TTSEngine(self.engine_type, **self.config)
            self.is_initialized = True
            logger.info("✅ 语音播报器初始化成功")
        except Exception as e:
            logger.error(f"❌ 语音播报器初始化失败: {e}")
            self.is_initialized = False
    
    async def speak(self, text: str, voice: str = "zh-CN-XiaoxiaoNeural", 
                   output_file: Optional[str] = None, block: bool = True) -> bool:
        """
        语音播报主接口
        
        Args:
            text: 要播报的文本
            voice: 语音模型 (edge-tts 有效)
            output_file: 输出文件路径
            block: 是否阻塞等待播报完成
            
        Returns:
            播报是否成功
        """
        if not self.is_initialized:
            logger.error("❌ 语音播报器未初始化")
            return False
        
        if not text or not text.strip():
            logger.warning("⚠️ 播报文本为空")
            return False
        
        logger.info(f"🔊 开始播报: {text[:50]}...")
        
        try:
            if block:
                # 阻塞模式：等待播报完成
                result = await self.tts_engine.synthesize(text, voice, output_file)
                logger.info("✅ 播报完成")
                return result is not None
            else:
                # 非阻塞模式：异步播报
                asyncio.create_task(self.tts_engine.synthesize(text, voice, output_file))
                logger.info("🚀 播报已启动（异步）")
                return True
                
        except Exception as e:
            logger.error(f"❌ 播报失败: {e}")
            return False
    
    def speak_sync(self, text: str, voice: str = "zh-CN-XiaoxiaoNeural", 
                   output_file: Optional[str] = None) -> bool:
        """
        同步语音播报接口
        
        Args:
            text: 要播报的文本
            voice: 语音模型
            output_file: 输出文件路径
            
        Returns:
            播报是否成功
        """
        if not self.is_initialized:
            logger.error("❌ 语音播报器未初始化")
            return False
        
        if not text or not text.strip():
            logger.warning("⚠️ 播报文本为空")
            return False
        
        try:
            # 运行异步函数
            return asyncio.run(self.speak(text, voice, output_file, block=True))
        except Exception as e:
            logger.error(f"❌ 同步播报失败: {e}")
            return False
    
    async def speak_multiple(self, texts: list, voice: str = "zh-CN-XiaoxiaoNeural", 
                           delay: float = 0.5) -> bool:
        """
        批量语音播报
        
        Args:
            texts: 要播报的文本列表
            voice: 语音模型
            delay: 播报间隔（秒）
            
        Returns:
            播报是否成功
        """
        if not texts:
            logger.warning("⚠️ 播报文本列表为空")
            return False
        
        logger.info(f"🔊 开始批量播报 {len(texts)} 条消息")
        
        try:
            for i, text in enumerate(texts):
                logger.info(f"📢 播报第 {i+1}/{len(texts)} 条")
                success = await self.speak(text, voice, block=True)
                if not success:
                    logger.error(f"❌ 第 {i+1} 条播报失败")
                    return False
                
                # 添加延迟（除了最后一条）
                if i < len(texts) - 1:
                    await asyncio.sleep(delay)
            
            logger.info("✅ 批量播报完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 批量播报失败: {e}")
            return False
    
    def set_voice(self, voice_id: str):
        """设置语音"""
        if self.tts_engine:
            self.tts_engine.set_voice(voice_id)
    
    def set_rate(self, rate: int):
        """设置语速"""
        if self.tts_engine:
            self.tts_engine.set_rate(rate)
    
    def set_volume(self, volume: float):
        """设置音量"""
        if self.tts_engine:
            self.tts_engine.set_volume(volume)
    
    def get_available_voices(self) -> Dict[str, Any]:
        """获取可用的语音列表"""
        if self.tts_engine:
            return self.tts_engine.get_available_voices()
        return {}
    
    def get_status(self) -> Dict[str, Any]:
        """获取播报器状态"""
        return {
            "initialized": self.is_initialized,
            "engine_type": self.engine_type,
            "available_voices": len(self.get_available_voices()) if self.tts_engine else 0
        }
    
    async def test(self) -> bool:
        """测试语音播报功能"""
        test_text = "你好，我是 Luna 语音助手，语音播报功能测试成功"
        return await self.speak(test_text)


# 全局播报器实例
_global_speaker: Optional[Speaker] = None

async def get_speaker(engine_type: str = "auto", **kwargs) -> Speaker:
    """获取全局语音播报器实例"""
    global _global_speaker
    if _global_speaker is None:
        _global_speaker = Speaker(engine_type, **kwargs)
    return _global_speaker

def speak(text: str, voice: str = "zh-CN-XiaoxiaoNeural", 
          output_file: Optional[str] = None, block: bool = True) -> bool:
    """
    便捷的语音播报函数
    
    Args:
        text: 要播报的文本
        voice: 语音模型
        output_file: 输出文件路径
        block: 是否阻塞等待播报完成
        
    Returns:
        播报是否成功
    """
    try:
        speaker = asyncio.run(get_speaker())
        return asyncio.run(speaker.speak(text, voice, output_file, block))
    except Exception as e:
        logger.error(f"❌ 便捷播报失败: {e}")
        return False

def speak_sync(text: str, voice: str = "zh-CN-XiaoxiaoNeural", 
               output_file: Optional[str] = None) -> bool:
    """
    同步语音播报便捷函数
    
    Args:
        text: 要播报的文本
        voice: 语音模型
        output_file: 输出文件路径
        
    Returns:
        播报是否成功
    """
    try:
        speaker = asyncio.run(get_speaker())
        return speaker.speak_sync(text, voice, output_file)
    except Exception as e:
        logger.error(f"❌ 同步播报失败: {e}")
        return False


if __name__ == "__main__":
    # 测试代码
    async def test_speaker():
        try:
            speaker = await get_speaker()
            success = await speaker.test()
            if success:
                print("✅ 语音播报测试成功")
            else:
                print("❌ 语音播报测试失败")
        except Exception as e:
            print(f"❌ 语音播报测试异常: {e}")
    
    # 运行测试
    asyncio.run(test_speaker())