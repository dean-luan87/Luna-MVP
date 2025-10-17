# -*- coding: utf-8 -*-
"""
语音播报模块
支持离线TTS（pyttsx3）和在线TTS（edge-tts）
"""

import platform
import logging
import threading
import time
from typing import Optional

logger = logging.getLogger(__name__)


class Voice:
    """语音播报类"""
    
    def __init__(self):
        """初始化语音播报模块"""
        self.engine = None
        self.engine_type = None
        self.is_available = False
        self.speaking = False
        self._lock = threading.Lock()
        
        # 检测系统环境并初始化TTS引擎
        self._initialize_tts()
    
    def _initialize_tts(self):
        """初始化TTS引擎"""
        try:
            # 优先尝试pyttsx3（离线TTS）
            if self._try_pyttsx3():
                self.engine_type = "pyttsx3"
                self.is_available = True
                logger.info("语音播报模块初始化成功: pyttsx3")
                return
            
            # 如果pyttsx3不可用，尝试edge-tts（在线TTS）
            if self._try_edge_tts():
                self.engine_type = "edge-tts"
                self.is_available = True
                logger.info("语音播报模块初始化成功: edge-tts")
                return
            
            # 如果都不可用
            logger.warning("所有TTS引擎都不可用，语音播报功能将被禁用")
            self.is_available = False
            
        except Exception as e:
            logger.error(f"语音播报模块初始化失败: {e}")
            self.is_available = False
    
    def _try_pyttsx3(self) -> bool:
        """尝试初始化pyttsx3引擎"""
        try:
            import pyttsx3
            
            # 在Mac上强制使用nsss驱动
            if platform.system() == 'Darwin':
                try:
                    self.engine = pyttsx3.init(driverName="nsss")
                    logger.info("使用nsss驱动初始化pyttsx3")
                except Exception as e:
                    logger.warning(f"nsss驱动初始化失败: {e}")
                    logger.info("尝试使用默认驱动...")
                    self.engine = pyttsx3.init()
            else:
                self.engine = pyttsx3.init()
            
            # 设置语音参数
            if self.engine:
                # 设置语速
                self.engine.setProperty('rate', 150)
                
                # 设置音量
                self.engine.setProperty('volume', 0.8)
                
                # 智能选择中文语音
                voices = self.engine.getProperty('voices')
                if voices:
                    selected_voice = self._select_best_voice(voices)
                    if selected_voice:
                        self.engine.setProperty('voice', selected_voice.id)
                        logger.info(f"设置语音: {selected_voice.name} (ID: {selected_voice.id})")
                    else:
                        # 使用默认语音
                        self.engine.setProperty('voice', voices[0].id)
                        logger.info(f"使用默认语音: {voices[0].name}")
                
                return True
            
        except ImportError:
            logger.warning("pyttsx3未安装，跳过离线TTS")
        except Exception as e:
            logger.warning(f"pyttsx3初始化失败: {e}")
        
        return False
    
    def _select_best_voice(self, voices):
        """选择最佳语音（优先中文）"""
        chinese_voices = []
        
        for voice in voices:
            voice_name = voice.name.lower()
            voice_languages = getattr(voice, 'languages', [])
            
            # 检查语言属性
            is_chinese = False
            if voice_languages:
                for lang in voice_languages:
                    if any(keyword in str(lang).lower() for keyword in ['zh', 'chinese', 'cn', 'mandarin']):
                        is_chinese = True
                        break
            
            # 检查名称中的中文关键词
            if not is_chinese:
                if any(keyword in voice_name for keyword in ['chinese', 'zh', 'cn', 'mandarin', 'ting-ting', 'xiaoyi']):
                    is_chinese = True
            
            if is_chinese:
                chinese_voices.append(voice)
        
        # 优先返回中文语音
        if chinese_voices:
            logger.info(f"发现 {len(chinese_voices)} 个中文语音")
            return chinese_voices[0]
        
        logger.info("未发现中文语音，将使用默认语音")
        return None
    
    def _try_edge_tts(self) -> bool:
        """尝试初始化edge-tts引擎"""
        try:
            import edge_tts
            
            # 检查网络连接
            import urllib.request
            try:
                urllib.request.urlopen('https://www.microsoft.com', timeout=3)
            except:
                logger.warning("网络连接不可用，跳过edge-tts")
                return False
            
            # 设置中文语音
            self.voice_name = "zh-CN-XiaoxiaoNeural"  # 默认中文语音
            self.engine = edge_tts
            
            return True
            
        except ImportError:
            logger.warning("edge-tts未安装，跳过在线TTS")
        except Exception as e:
            logger.warning(f"edge-tts初始化失败: {e}")
        
        return False
    
    def speak(self, text: str) -> bool:
        """
        语音播报文本
        
        Args:
            text: 要播报的文本
            
        Returns:
            是否播报成功
        """
        if not text or not text.strip():
            return True
        
        if not self.is_available:
            logger.warning("语音播报模块不可用，跳过播报")
            return False
        
        # 检查是否正在播报
        with self._lock:
            if self.speaking:
                logger.warning("正在播报中，跳过新的播报请求")
                return False
            self.speaking = True
        
        try:
            # 在新线程中播报，避免阻塞主线程
            thread = threading.Thread(target=self._speak_thread, args=(text,))
            thread.daemon = True
            thread.start()
            return True
            
        except Exception as e:
            logger.error(f"启动语音播报线程失败: {e}")
            with self._lock:
                self.speaking = False
            return False
    
    def _speak_thread(self, text: str):
        """语音播报线程"""
        try:
            if self.engine_type == "pyttsx3":
                self._speak_pyttsx3(text)
            elif self.engine_type == "edge-tts":
                self._speak_edge_tts(text)
            
        except Exception as e:
            logger.error(f"语音播报失败: {e}")
        finally:
            with self._lock:
                self.speaking = False
    
    def _speak_pyttsx3(self, text: str):
        """使用pyttsx3播报"""
        try:
            if self.engine:
                # 清空之前的队列
                self.engine.stop()
                
                # 设置超时保护
                import threading
                import time
                
                def timeout_handler():
                    time.sleep(10)  # 10秒超时
                    try:
                        self.engine.stop()
                    except:
                        pass
                
                # 启动超时保护
                timeout_thread = threading.Thread(target=timeout_handler)
                timeout_thread.daemon = True
                timeout_thread.start()
                
                # 开始播报
                self.engine.say(text)
                self.engine.runAndWait()
                
                logger.debug(f"pyttsx3播报完成: {text[:50]}...")
                
        except Exception as e:
            logger.warning(f"pyttsx3播报失败: {e}")
            # 尝试重新初始化引擎
            try:
                self._try_pyttsx3()
            except:
                pass
    
    def _speak_edge_tts(self, text: str):
        """使用edge-tts播报"""
        try:
            import asyncio
            import edge_tts
            
            async def _async_speak():
                communicate = edge_tts.Communicate(text, self.voice_name)
                await communicate.save("temp_voice.mp3")
                
                # 播放音频文件
                import subprocess
                import os
                try:
                    if platform.system() == 'Darwin':
                        subprocess.run(['afplay', 'temp_voice.mp3'], check=True)
                    else:
                        subprocess.run(['mpg123', 'temp_voice.mp3'], check=True)
                finally:
                    # 清理临时文件
                    if os.path.exists('temp_voice.mp3'):
                        os.remove('temp_voice.mp3')
            
            # 在新的事件循环中运行
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_async_speak())
            loop.close()
            
            logger.debug(f"edge-tts播报完成: {text[:50]}...")
            
        except Exception as e:
            logger.error(f"edge-tts播报失败: {e}")
    
    def is_speaking(self) -> bool:
        """检查是否正在播报"""
        with self._lock:
            return self.speaking
    
    def stop(self):
        """停止当前播报"""
        try:
            if self.engine_type == "pyttsx3" and self.engine:
                self.engine.stop()
            with self._lock:
                self.speaking = False
            logger.info("语音播报已停止")
        except Exception as e:
            logger.error(f"停止语音播报失败: {e}")
    
    def get_status(self) -> dict:
        """获取语音模块状态"""
        return {
            'available': self.is_available,
            'engine_type': self.engine_type,
            'speaking': self.speaking,
            'platform': platform.system()
        }
