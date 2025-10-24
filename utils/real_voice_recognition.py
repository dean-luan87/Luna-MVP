# -*- coding: utf-8 -*-
"""
真实语音识别模块
使用speech_recognition库实现真实麦克风录音和语音转文字
支持静音检测和自动识别
"""

import logging
import time
import threading
from typing import Optional

logger = logging.getLogger(__name__)

# 尝试导入speech_recognition
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    logger.warning("speech_recognition未安装，语音识别功能将被禁用")


class RealVoiceRecognition:
    """真实语音识别类"""
    
    def __init__(self):
        """初始化语音识别模块"""
        self.recognizer = None
        self.microphone = None
        self.is_available = False
        self.is_listening = False
        self._initialize_recognition()
    
    def _initialize_recognition(self):
        """初始化语音识别"""
        try:
            if not SPEECH_RECOGNITION_AVAILABLE:
                logger.warning("speech_recognition库不可用")
                self.is_available = False
                return
            
            # 创建识别器实例
            self.recognizer = sr.Recognizer()
            
            # 获取麦克风
            self.microphone = sr.Microphone()
            
            # 调整环境噪音
            logger.info("正在调整环境噪音，请保持安静...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # 设置识别参数
            self.recognizer.energy_threshold = 300  # 能量阈值
            self.recognizer.dynamic_energy_threshold = True  # 动态调整
            self.recognizer.pause_threshold = 0.8  # 停顿阈值
            self.recognizer.phrase_threshold = 0.3  # 短语阈值
            self.recognizer.non_speaking_duration = 0.8  # 非说话持续时间
            
            self.is_available = True
            logger.info("真实语音识别模块初始化成功")
            
        except Exception as e:
            logger.error(f"语音识别模块初始化失败: {e}")
            self.is_available = False
    
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
            
            # 使用麦克风录音
            with self.microphone as source:
                # 清空缓冲区
                self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                
                # 录音
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)
            
            logger.info("录音完成，开始识别...")
            
            # 语音识别
            try:
                # 优先使用Google中文识别
                text = self.recognizer.recognize_google(audio, language='zh-CN')
                logger.info(f"Google识别结果: {text}")
                return text
                
            except sr.UnknownValueError:
                logger.warning("Google无法识别语音内容")
                
                # 备用：尝试使用Sphinx离线识别
                try:
                    text = self.recognizer.recognize_sphinx(audio, language='zh-CN')
                    logger.info(f"Sphinx识别结果: {text}")
                    return text
                except sr.UnknownValueError:
                    logger.warning("Sphinx也无法识别语音内容")
                    return ""
                except Exception as e:
                    logger.warning(f"Sphinx识别失败: {e}")
                    return ""
                    
            except sr.RequestError as e:
                logger.warning(f"Google识别服务错误: {e}")
                
                # 备用：尝试使用Sphinx离线识别
                try:
                    text = self.recognizer.recognize_sphinx(audio, language='zh-CN')
                    logger.info(f"Sphinx识别结果: {text}")
                    return text
                except Exception as e:
                    logger.warning(f"Sphinx识别失败: {e}")
                    return ""
            
        except sr.WaitTimeoutError:
            logger.warning(f"录音超时（{timeout}秒内无声音）")
            return ""
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
            
            with self.microphone as source:
                # 调整环境噪音
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # 监听语音，检测到静音后停止
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=None)
            
            logger.info("检测到静音，开始识别...")
            
            # 语音识别
            try:
                text = self.recognizer.recognize_google(audio, language='zh-CN')
                logger.info(f"识别结果: {text}")
                return text
                
            except sr.UnknownValueError:
                logger.warning("无法识别语音内容")
                return ""
            except sr.RequestError as e:
                logger.warning(f"识别服务错误: {e}")
                return ""
            
        except Exception as e:
            logger.error(f"静音检测识别失败: {e}")
            return ""
    
    def test_microphone(self) -> bool:
        """测试麦克风是否可用"""
        try:
            if not self.is_available:
                return False
            
            logger.info("测试麦克风...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            logger.info("麦克风测试成功")
            return True
            
        except Exception as e:
            logger.error(f"麦克风测试失败: {e}")
            return False
    
    def get_status(self) -> dict:
        """获取语音识别模块状态"""
        return {
            'available': self.is_available,
            'recognizer': self.recognizer is not None,
            'microphone': self.microphone is not None,
            'listening': self.is_listening
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
        vr = RealVoiceRecognition()
        
        if not vr.is_available:
            logger.warning("语音识别模块不可用")
            return ""
        
        # 执行识别
        return vr.listen_and_recognize(timeout)
        
    except Exception as e:
        logger.error(f"语音识别函数调用失败: {e}")
        return ""

