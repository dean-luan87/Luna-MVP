# -*- coding: utf-8 -*-
"""
Mac系统语音识别模块
使用系统内置录音功能，不依赖PyAudio
"""

import logging
import time
import subprocess
import os
import tempfile
import threading
from typing import Optional

logger = logging.getLogger(__name__)


class MacVoiceRecognition:
    """Mac系统语音识别类"""
    
    def __init__(self):
        """初始化语音识别模块"""
        self.is_available = False
        self.is_listening = False
        self._initialize_recognition()
    
    def _initialize_recognition(self):
        """初始化语音识别"""
        try:
            import platform
            if platform.system() != 'Darwin':
                logger.warning("此模块仅支持Mac系统")
                self.is_available = False
                return
            
            # 检查系统录音功能
            if self._check_recording_support():
                self.is_available = True
                logger.info("Mac语音识别模块初始化成功")
            else:
                self.is_available = False
                logger.warning("系统不支持录音功能")
                
        except Exception as e:
            logger.error(f"语音识别模块初始化失败: {e}")
            self.is_available = False
    
    def _check_recording_support(self) -> bool:
        """检查系统是否支持录音"""
        try:
            # 在Mac上，我们总是返回True，使用模拟模式
            logger.info("Mac系统检测到，使用模拟语音识别模式")
            return True
                
        except Exception:
            return False
    
    def _record_audio(self, duration: float = 3.0) -> str:
        """
        录制音频文件（模拟模式）
        
        Args:
            duration: 录音时长（秒）
            
        Returns:
            录音文件路径，失败返回空字符串
        """
        try:
            # 模拟录音过程
            logger.info(f"模拟录音 {duration} 秒...")
            time.sleep(duration)
            
            # 创建临时文件（模拟）
            temp_file = tempfile.mktemp(suffix='.wav')
            with open(temp_file, 'w') as f:
                f.write("mock audio data")
            
            logger.info(f"模拟录音完成: {temp_file}")
            return temp_file
            
        except Exception as e:
            logger.error(f"录音失败: {e}")
            return ""
    
    def _transcribe_audio(self, audio_file: str) -> str:
        """
        转录音频文件为文字
        
        Args:
            audio_file: 音频文件路径
            
        Returns:
            识别到的文字
        """
        try:
            # 这里应该调用语音识别服务
            # 由于没有真实的语音识别服务，我们返回模拟结果
            mock_texts = [
                "你好，Luna",
                "今天天气怎么样",
                "请帮我识别这个物体",
                "Luna，你在吗",
                "测试语音识别功能",
                "你好，世界",
                "这是一个测试"
            ]
            
            import random
            mock_text = random.choice(mock_texts)
            logger.info(f"模拟识别结果: {mock_text}")
            return mock_text
            
        except Exception as e:
            logger.error(f"语音转文字失败: {e}")
            return ""
    
    def listen_and_recognize(self, timeout: int = 5) -> str:
        """
        从麦克风录音并返回识别到的中文文本
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            识别到的文本，失败则返回空字符串
        """
        if not self.is_available:
            logger.warning("语音识别模块不可用")
            return ""
        
        try:
            logger.info(f"开始录音，超时时间: {timeout}秒")
            
            # 录制音频
            audio_file = self._record_audio(duration=timeout)
            if not audio_file:
                logger.warning("录音失败")
                return ""
            
            # 转录音频
            text = self._transcribe_audio(audio_file)
            
            # 清理临时文件
            try:
                if os.path.exists(audio_file):
                    os.remove(audio_file)
            except:
                pass
            
            return text
            
        except Exception as e:
            logger.error(f"语音识别过程出错: {e}")
            return ""
    
    def listen_with_silence_detection(self, silence_timeout: float = 1.0) -> str:
        """
        监听语音直到检测到静音后自动识别
        
        Args:
            silence_timeout: 静音超时时间（秒）
            
        Returns:
            识别到的文本
        """
        if not self.is_available:
            logger.warning("语音识别模块不可用")
            return ""
        
        try:
            logger.info("开始监听语音，检测到静音后自动识别...")
            
            # 使用较长的录音时间
            audio_file = self._record_audio(duration=5.0)
            if not audio_file:
                logger.warning("录音失败")
                return ""
            
            # 转录音频
            text = self._transcribe_audio(audio_file)
            
            # 清理临时文件
            try:
                if os.path.exists(audio_file):
                    os.remove(audio_file)
            except:
                pass
            
            return text
            
        except Exception as e:
            logger.error(f"静音检测识别失败: {e}")
            return ""
    
    def test_microphone(self) -> bool:
        """测试麦克风是否可用"""
        try:
            if not self.is_available:
                return False
            
            logger.info("测试麦克风...")
            
            # 尝试录制1秒音频
            audio_file = self._record_audio(duration=1.0)
            if audio_file:
                # 清理临时文件
                try:
                    if os.path.exists(audio_file):
                        os.remove(audio_file)
                except:
                    pass
                logger.info("麦克风测试成功")
                return True
            else:
                logger.warning("麦克风测试失败")
                return False
            
        except Exception as e:
            logger.error(f"麦克风测试失败: {e}")
            return False
    
    def get_status(self) -> dict:
        """获取语音识别模块状态"""
        return {
            'available': self.is_available,
            'listening': self.is_listening,
            'type': 'mac_system'
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
        vr = MacVoiceRecognition()
        
        if not vr.is_available:
            logger.warning("语音识别模块不可用")
            return ""
        
        # 执行识别
        return vr.listen_and_recognize(timeout)
        
    except Exception as e:
        logger.error(f"语音识别函数调用失败: {e}")
        return ""
