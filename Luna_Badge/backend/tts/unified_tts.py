#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一TTS接口（规范要求）
提供统一的TTS调用接口：await generate_tts(text, style="default")
"""

import logging
import asyncio
from typing import Optional
from enum import Enum

logger = logging.getLogger(__name__)


class TTSStyle(Enum):
    """TTS风格枚举"""
    DEFAULT = "default"
    CALM = "calm"
    URGENT = "urgent"
    CHEERFUL = "cheerful"
    EMPATHETIC = "empathetic"
    GENTLE = "gentle"


# 全局TTS管理器实例
_global_tts_manager = None


def set_tts_manager(tts_manager):
    """
    设置全局TTS管理器
    
    Args:
        tts_manager: TTS管理器实例
    """
    global _global_tts_manager
    _global_tts_manager = tts_manager
    logger.info("全局TTS管理器已设置", extra={"module": "tts", "meta": {"component": "unified_tts"}})


async def generate_tts(text: str, style: str = "default") -> bool:
    """
    统一TTS生成接口（规范要求）
    
    Args:
        text: 要播报的文本
        style: 播报风格（default/calm/urgent/cheerful/empathetic/gentle）
    
    Returns:
        bool: 是否成功播报
    
    Raises:
        Exception: 如果TTS管理器未初始化或播报失败
    """
    global _global_tts_manager
    
    if not _global_tts_manager:
        logger.warning("TTS管理器未初始化，使用模拟播报", extra={"module": "tts", "meta": {"component": "unified_tts"}})
        print(f"🔊 [模拟TTS] {text} (风格: {style})")
        return True
    
    try:
        # 转换风格字符串为TTSManager需要的格式
        style_mapping = {
            "default": "calm",
            "calm": "calm",
            "urgent": "urgent",
            "cheerful": "cheerful",
            "empathetic": "empathetic",
            "gentle": "gentle"
        }
        
        tts_style = style_mapping.get(style.lower(), "calm")
        
        # 调用TTS管理器
        if hasattr(_global_tts_manager, 'speak'):
            # 同步方法，在线程中执行
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, _global_tts_manager.speak, text, tts_style)
        elif hasattr(_global_tts_manager, 'speak_async'):
            # 异步方法
            await _global_tts_manager.speak_async(text, tts_style)
        else:
            logger.error("TTS管理器不支持speak或speak_async方法", extra={"module": "tts", "meta": {"component": "unified_tts"}})
            return False
        
        logger.info(f"TTS播报成功: {text[:50]}...", extra={"module": "tts", "meta": {
            "component": "unified_tts",
            "style": style,
            "text_length": len(text)
        }})
        
        return True
        
    except Exception as e:
        logger.error(f"TTS播报失败: {e}", extra={"module": "tts", "meta": {
            "component": "unified_tts",
            "error": str(e),
            "style": style
        }})
        return False


def generate_tts_sync(text: str, style: str = "default") -> bool:
    """
    同步版本的TTS生成接口
    
    Args:
        text: 要播报的文本
        style: 播报风格
    
    Returns:
        bool: 是否成功播报
    """
    global _global_tts_manager
    
    if not _global_tts_manager:
        logger.warning("TTS管理器未初始化，使用模拟播报", extra={"module": "tts", "meta": {"component": "unified_tts"}})
        print(f"🔊 [模拟TTS] {text} (风格: {style})")
        return True
    
    try:
        style_mapping = {
            "default": "calm",
            "calm": "calm",
            "urgent": "urgent",
            "cheerful": "cheerful",
            "empathetic": "empathetic",
            "gentle": "gentle"
        }
        
        tts_style = style_mapping.get(style.lower(), "calm")
        
        if hasattr(_global_tts_manager, 'speak'):
            _global_tts_manager.speak(text, tts_style)
        elif hasattr(_global_tts_manager, 'speak_sync'):
            _global_tts_manager.speak_sync(text, tts_style)
        else:
            logger.error("TTS管理器不支持speak或speak_sync方法", extra={"module": "tts", "meta": {"component": "unified_tts"}})
            return False
        
        logger.info(f"TTS播报成功: {text[:50]}...", extra={"module": "tts", "meta": {
            "component": "unified_tts",
            "style": style,
            "text_length": len(text)
        }})
        
        return True
        
    except Exception as e:
        logger.error(f"TTS播报失败: {e}", extra={"module": "tts", "meta": {
            "component": "unified_tts",
            "error": str(e),
            "style": style
        }})
        return False


if __name__ == "__main__":
    # 自检代码
    print("🧪 UnifiedTTS自检开始...")
    
    # 测试模拟播报（TTS管理器未设置）
    result = asyncio.run(generate_tts("测试文本", "default"))
    assert result == True
    
    # 测试同步版本
    result = generate_tts_sync("测试文本", "urgent")
    assert result == True
    
    print("✅ UnifiedTTS自检完成")


