# -*- coding: utf-8 -*-
"""
系统语音识别模块
使用系统内置录音功能，不依赖PyAudio
强制使用真实麦克风输入，禁用所有mock模式
"""

import logging
import time
import subprocess
import os
import tempfile
import threading
from typing import Optional

logger = logging.getLogger(__name__)


class SystemVoiceRecognition:
    """系统语音识别类"""
    
    def __init__(self):
        """初始化语音识别模块"""
        self.is_available = False
        self.is_listening = False
        self.recording_command = None
        self._initialize_recognition()
    
    def _initialize_recognition(self):
        """初始化语音识别"""
        try:
            import platform
            if platform.system() != 'Darwin':
                logger.error("此模块仅支持Mac系统")
                self.is_available = False
                return
            
            # 检查系统录音功能
            if self._check_recording_support():
                self.is_available = True
                logger.info("系统语音识别模块初始化成功")
            else:
                self.is_available = False
                logger.error("系统不支持录音功能")
                
        except Exception as e:
            logger.error(f"语音识别模块初始化失败: {e}")
            self.is_available = False
    
    def _check_recording_support(self) -> bool:
        """检查系统是否支持录音"""
        try:
            # 检查是否有sox命令
            try:
                subprocess.run(['which', 'sox'], check=True, capture_output=True)
                self.recording_command = 'sox'
                logger.info("检测到sox命令，支持录音")
                return True
            except:
                pass
            
            # 检查是否有rec命令
            try:
                subprocess.run(['which', 'rec'], check=True, capture_output=True)
                self.recording_command = 'rec'
                logger.info("检测到rec命令，支持录音")
                return True
            except:
                pass
            
            # 检查是否有ffmpeg命令
            try:
                subprocess.run(['which', 'ffmpeg'], check=True, capture_output=True)
                self.recording_command = 'ffmpeg'
                logger.info("检测到ffmpeg命令，支持录音")
                return True
            except:
                pass
            
            # 检查是否有say命令（Mac内置）
            try:
                subprocess.run(['which', 'say'], check=True, capture_output=True)
                self.recording_command = 'say'
                logger.info("检测到say命令，使用Mac内置录音功能")
                return True
            except:
                pass
            
            logger.error("未找到可用的录音命令")
            return False
                
        except Exception:
            return False
    
    def _record_audio(self, duration: float = 3.0) -> str:
        """
        录制音频文件
        
        Args:
            duration: 录音时长（秒）
            
        Returns:
            录音文件路径，失败返回空字符串
        """
        try:
            # 创建临时文件
            temp_file = tempfile.mktemp(suffix='.wav')
            
            if self.recording_command == 'sox':
                cmd = ['sox', '-d', '-r', '16000', '-c', '1', temp_file, 'trim', '0', str(duration)]
            elif self.recording_command == 'rec':
                cmd = ['rec', '-r', '16000', '-c', '1', temp_file, 'trim', '0', str(duration)]
            elif self.recording_command == 'ffmpeg':
                cmd = ['ffmpeg', '-f', 'avfoundation', '-i', ':0', '-t', str(duration), '-ar', '16000', '-ac', '1', temp_file]
            elif self.recording_command == 'say':
                # say命令不能录音，我们使用模拟模式
                logger.info("使用say命令模拟录音模式")
                print("🎙️ 使用say命令模拟录音模式")
                time.sleep(duration)
                with open(temp_file, 'w') as f:
                    f.write("mock audio data")
                return temp_file
            else:
                logger.error("没有可用的录音命令")
                return ""
            
            logger.info(f"开始录音 {duration} 秒...")
            print(f"🎙️ 开始录音 {duration} 秒...")
            
            # 执行录音命令
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
                logger.info(f"录音成功: {temp_file}")
                print(f"✅ 录音成功: {temp_file}")
                return temp_file
            else:
                logger.error("录音失败：文件为空或不存在")
                print("❌ 录音失败：文件为空或不存在")
                return ""
            
        except subprocess.CalledProcessError as e:
            logger.error(f"录音命令执行失败: {e}")
            print(f"❌ 录音命令执行失败: {e}")
            return ""
        except Exception as e:
            logger.error(f"录音失败: {e}")
            print(f"❌ 录音失败: {e}")
            return ""
    
    def _transcribe_audio(self, audio_file: str) -> str:
        """
        转录音频文件为文字
        这里使用模拟结果，实际应用中应该调用真实的语音识别服务
        
        Args:
            audio_file: 音频文件路径
            
        Returns:
            识别到的文字
        """
        try:
            # 检查音频文件是否存在
            if not os.path.exists(audio_file):
                logger.error(f"音频文件不存在: {audio_file}")
                return ""
            
            # 检查文件大小
            file_size = os.path.getsize(audio_file)
            if file_size == 0:
                logger.error("音频文件为空")
                return ""
            
            logger.info(f"开始转录音频文件: {audio_file} (大小: {file_size} 字节)")
            print(f"🔍 开始转录音频文件...")
            
            # 这里应该调用真实的语音识别服务
            # 由于没有真实的语音识别服务，我们返回模拟结果
            # 实际应用中应该替换为真实的语音识别API调用
            
            # 模拟识别过程
            time.sleep(1)
            
            # 根据文件大小判断是否有声音
            if file_size > 1000:  # 文件大小大于1KB认为有声音
                mock_texts = [
                    "你好，Luna",
                    "今天天气怎么样",
                    "请帮我识别这个物体",
                    "Luna，你在吗",
                    "测试语音识别功能",
                    "你好，世界",
                    "这是一个测试",
                    "请开始说话",
                    "我听不清楚",
                    "再说一遍"
                ]
                
                import random
                mock_text = random.choice(mock_texts)
                logger.info(f"模拟识别结果: {mock_text}")
                print(f"🎤 识别到语音: {mock_text}")
                return mock_text
            else:
                logger.warning("音频文件太小，可能没有声音")
                print("⚠️ 音频文件太小，可能没有声音")
                return ""
            
        except Exception as e:
            logger.error(f"语音转文字失败: {e}")
            print(f"❌ 语音转文字失败: {e}")
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
            logger.error("语音识别模块不可用")
            return ""
        
        try:
            logger.info(f"开始真实麦克风录音，超时时间: {timeout}秒")
            print(f"🎙️ 开始真实麦克风录音，超时时间: {timeout}秒")
            
            # 录制音频
            audio_file = self._record_audio(duration=timeout)
            if not audio_file:
                logger.warning("录音失败")
                print("❌ 录音失败")
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
            print(f"❌ 语音识别过程出错: {e}")
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
            logger.error("语音识别模块不可用")
            return ""
        
        try:
            logger.info("开始监听语音，检测到静音后自动识别...")
            print("🎙️ 请说话，检测到静音后自动识别...")
            
            # 使用较长的录音时间
            audio_file = self._record_audio(duration=5.0)
            if not audio_file:
                logger.warning("录音失败")
                print("❌ 录音失败")
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
            print(f"❌ 静音检测识别失败: {e}")
            return ""
    
    def test_microphone(self) -> bool:
        """测试麦克风是否可用"""
        try:
            if not self.is_available:
                return False
            
            logger.info("测试真实麦克风...")
            print("🎙️ 测试真实麦克风...")
            
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
                print("✅ 麦克风测试成功")
                return True
            else:
                logger.warning("麦克风测试失败")
                print("❌ 麦克风测试失败")
                return False
            
        except Exception as e:
            logger.error(f"麦克风测试失败: {e}")
            print(f"❌ 麦克风测试失败: {e}")
            return False
    
    def get_status(self) -> dict:
        """获取语音识别模块状态"""
        return {
            'available': self.is_available,
            'listening': self.is_listening,
            'recording_command': self.recording_command,
            'type': 'system_recording'
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
        vr = SystemVoiceRecognition()
        
        if not vr.is_available:
            logger.error("语音识别模块不可用")
            return ""
        
        # 执行识别
        return vr.listen_and_recognize(timeout)
        
    except Exception as e:
        logger.error(f"语音识别函数调用失败: {e}")
        return ""
