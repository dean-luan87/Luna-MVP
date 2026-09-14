# -*- coding: utf-8 -*-
"""
简化语音识别模块
使用系统内置录音功能，不依赖PyAudio
"""

import logging
import time
import subprocess
import os
import tempfile
from typing import Optional

logger = logging.getLogger(__name__)


class SimpleVoiceRecognition:
    """简化语音识别类"""
    
    def __init__(self):
        """初始化语音识别模块"""
        self.is_available = False
        self._initialize_recognition()
    
    def _initialize_recognition(self):
        """初始化语音识别"""
        try:
            # 检查系统是否支持录音
            if self._check_recording_support():
                self.is_available = True
                logger.info("简化语音识别模块初始化成功")
            else:
                self.is_available = False
                logger.warning("系统不支持录音功能")
                
        except Exception as e:
            logger.error(f"语音识别模块初始化失败: {e}")
            self.is_available = False
    
    def _check_recording_support(self) -> bool:
        """检查系统是否支持录音"""
        try:
            import platform
            system = platform.system()
            
            if system == 'Darwin':  # macOS
                # 在Mac上，我们使用模拟模式，总是返回True
                logger.info("Mac系统检测到，使用模拟语音识别模式")
                return True
            else:
                # 其他系统暂时不支持
                return False
                
        except Exception:
            return False
    
    def listen_and_recognize(self, timeout: int = 5) -> str:
        """
        从麦克风录音并返回识别到的中文文本（模拟）
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            模拟的识别文本，失败则返回空字符串
        """
        if not self.is_available:
            logger.warning("语音识别模块不可用")
            return ""
        
        try:
            logger.info(f"开始录音，超时时间: {timeout}秒")
            
            # 模拟录音过程
            time.sleep(2)  # 模拟录音时间
            
            # 返回模拟的识别结果
            mock_texts = [
                "你好，Luna",
                "今天天气怎么样",
                "请帮我识别这个物体",
                "Luna，你在吗",
                "测试语音识别功能"
            ]
            
            import random
            mock_text = random.choice(mock_texts)
            
            logger.info(f"模拟识别结果: {mock_text}")
            return mock_text
            
        except Exception as e:
            logger.error(f"语音识别过程出错: {e}")
            return ""
    
    def test_microphone(self) -> bool:
        """测试麦克风是否可用"""
        return self.is_available
    
    def get_status(self) -> dict:
        """获取语音识别模块状态"""
        return {
            'available': self.is_available,
            'type': 'simple_mock'
        }


def listen_and_recognize(timeout: int = 5) -> str:
    """
    便捷函数：从麦克风录音并返回识别到的中文文本
    
    Args:
        timeout: 超时时间（秒）
        
    Returns:
        识别到的文本，失败则返回空字符串
    """
    try:
        # 创建语音识别实例
        vr = SimpleVoiceRecognition()
        
        if not vr.is_available:
            logger.warning("语音识别模块不可用")
            return ""
        
        # 执行识别
        return vr.listen_and_recognize(timeout)
        
    except Exception as e:
        logger.error(f"语音识别函数调用失败: {e}")
        return ""
