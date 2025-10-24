#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge - Mac版本硬件驱动层
摄像头、麦克风、TTS播报
"""

import cv2
import numpy as np
import pyttsx3
import edge_tts
import whisper
import threading
import time
import os
import subprocess
from typing import Dict, Any, Optional, List
from ultralytics import YOLO

try:
    from ..core.hal_interface import (
        HALInterface, CameraInterface, MicrophoneInterface, 
        SpeakerInterface, NetworkInterface, YOLOInterface, 
        WhisperInterface, TTSInterface, HardwareType
    )
except ImportError:
    # 当作为独立模块运行时，使用绝对导入
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.hal_interface import (
        HALInterface, CameraInterface, MicrophoneInterface, 
        SpeakerInterface, NetworkInterface, YOLOInterface, 
        WhisperInterface, TTSInterface, HardwareType
    )

class MacHAL(HALInterface):
    """Mac平台硬件抽象层"""
    
    def __init__(self):
        """初始化Mac硬件抽象层"""
        self.camera = MacCamera()
        self.microphone = MacMicrophone()
        self.speaker = MacSpeaker()
        self.network = MacNetwork()
        self.yolo = MacYOLO()
        self.whisper = MacWhisper()
        self.tts = MacTTS()
        
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """初始化硬件"""
        try:
            print("初始化Mac硬件抽象层...")
            
            # 初始化各个硬件组件
            if not self.camera.initialize():
                print("摄像头初始化失败")
                return False
            
            if not self.microphone.initialize():
                print("麦克风初始化失败")
                return False
            
            if not self.speaker.initialize():
                print("扬声器初始化失败")
                return False
            
            if not self.network.initialize():
                print("网络初始化失败")
                return False
            
            if not self.yolo.initialize():
                print("YOLO模型初始化失败")
                return False
            
            if not self.whisper.initialize():
                print("Whisper模型初始化失败")
                return False
            
            if not self.tts.initialize():
                print("TTS引擎初始化失败")
                return False
            
            self.is_initialized = True
            print("Mac硬件抽象层初始化成功")
            return True
            
        except Exception as e:
            print(f"Mac硬件抽象层初始化失败: {e}")
            return False
    
    def cleanup(self) -> bool:
        """清理硬件资源"""
        try:
            self.camera.cleanup()
            self.microphone.cleanup()
            self.speaker.cleanup()
            self.network.cleanup()
            self.yolo.cleanup()
            self.whisper.cleanup()
            self.tts.cleanup()
            
            self.is_initialized = False
            return True
            
        except Exception as e:
            print(f"硬件清理失败: {e}")
            return False
    
    def speak(self, text: str) -> bool:
        """语音播报"""
        try:
            return self.tts.synthesize_speech(text)
        except Exception as e:
            print(f"语音播报失败: {e}")
            return False
    
    async def speak_async(self, text: str, voice: str = "zh-CN-XiaoxiaoNeural") -> bool:
        """
        异步语音播报（使用Edge-TTS或系统say命令）
        
        Args:
            text: 要播报的文本
            voice: 语音类型，默认为中文女声
            
        Returns:
            播报是否成功
        """
        try:
            print(f"🗣️ 正在播报: {text}")
            
            # 首先尝试使用Edge-TTS
            try:
                import edge_tts
                import tempfile
                import os
                
                # 创建临时音频文件
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    temp_path = tmp_file.name
                
                # 使用edge-tts生成音频
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(temp_path)
                
                # 播放音频文件
                if os.path.exists(temp_path):
                    # 使用系统命令播放音频
                    subprocess.run(['afplay', temp_path], check=True)
                    os.unlink(temp_path)  # 删除临时文件
                    print("🗣️ 播报完成")
                    return True
                else:
                    raise Exception("Edge-TTS音频文件生成失败")
                    
            except Exception as edge_error:
                print(f"⚠️ Edge-TTS失败，使用系统say命令: {edge_error}")
                
                # 备选方案：使用系统say命令
                try:
                    subprocess.run(['say', '-v', 'Ting-Ting', text], check=True)
                    print("🗣️ 播报完成")
                    return True
                except Exception as say_error:
                    print(f"❌ 系统say命令失败: {say_error}")
                    return False
                
        except Exception as e:
            print(f"❌ 异步语音播报失败: {e}")
            return False
    
    def check_camera(self) -> bool:
        """检查摄像头状态"""
        return self.camera.is_available()
    
    def check_microphone(self) -> bool:
        """检查麦克风状态"""
        return self.microphone.is_available()
    
    def check_network(self) -> bool:
        """检查网络连接"""
        return self.network.check_connection()
    
    def check_voice_engine(self) -> bool:
        """检查语音引擎状态"""
        return self.tts.is_available()
    
    def detect_wake_word(self) -> bool:
        """检测语音唤醒词"""
        try:
            # 获取音频数据
            audio_data = self.microphone.get_audio_data()
            if audio_data:
                # 使用Whisper进行语音识别
                text = self.whisper.transcribe_audio(audio_data)
                # 检查是否包含唤醒词
                wake_word = "启动环境智能导航"
                return wake_word in text
            return False
        except Exception as e:
            print(f"唤醒词检测失败: {e}")
            return False
    
    def get_hardware_info(self) -> Dict[str, Any]:
        """获取硬件信息"""
        return {
            "platform": "mac",
            "camera": self.camera.get_info(),
            "microphone": self.microphone.get_info(),
            "speaker": self.speaker.get_info(),
            "network": self.network.get_info(),
            "yolo": self.yolo.get_info(),
            "whisper": self.whisper.get_info(),
            "tts": self.tts.get_info()
        }

class MacCamera(CameraInterface):
    """Mac摄像头接口"""
    
    def __init__(self):
        """初始化Mac摄像头"""
        self.cap = None
        self.is_running = False
        self.resolution = (640, 480)
        self.fps = 30
    
    def initialize(self) -> bool:
        """初始化摄像头"""
        try:
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
                self.cap.set(cv2.CAP_PROP_FPS, self.fps)
                return True
            return False
        except Exception as e:
            print(f"摄像头初始化失败: {e}")
            return False
    
    def cleanup(self) -> bool:
        """清理摄像头资源"""
        try:
            if self.cap:
                self.cap.release()
                self.cap = None
            return True
        except Exception as e:
            print(f"摄像头清理失败: {e}")
            return False
    
    def start_camera(self) -> bool:
        """启动摄像头"""
        try:
            if self.cap and self.cap.isOpened():
                self.is_running = True
                return True
            return False
        except Exception as e:
            print(f"摄像头启动失败: {e}")
            return False
    
    def stop_camera(self) -> bool:
        """停止摄像头"""
        try:
            self.is_running = False
            return True
        except Exception as e:
            print(f"摄像头停止失败: {e}")
            return False
    
    def capture_frame(self) -> Optional[np.ndarray]:
        """捕获帧"""
        try:
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    return frame
            return None
        except Exception as e:
            print(f"帧捕获失败: {e}")
            return None
    
    def set_resolution(self, width: int, height: int) -> bool:
        """设置分辨率"""
        try:
            self.resolution = (width, height)
            if self.cap:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            return True
        except Exception as e:
            print(f"分辨率设置失败: {e}")
            return False
    
    def set_fps(self, fps: int) -> bool:
        """设置帧率"""
        try:
            self.fps = fps
            if self.cap:
                self.cap.set(cv2.CAP_PROP_FPS, fps)
            return True
        except Exception as e:
            print(f"帧率设置失败: {e}")
            return False
    
    def is_available(self) -> bool:
        """检查摄像头是否可用"""
        return self.cap is not None and self.cap.isOpened()
    
    def get_info(self) -> Dict[str, Any]:
        """获取摄像头信息"""
        return {
            "available": self.is_available(),
            "resolution": self.resolution,
            "fps": self.fps,
            "running": self.is_running
        }

class MacMicrophone(MicrophoneInterface):
    """Mac麦克风接口"""
    
    def __init__(self):
        """初始化Mac麦克风"""
        self.is_recording = False
        self.sample_rate = 16000
        self.audio_data = None
    
    def initialize(self) -> bool:
        """初始化麦克风"""
        try:
            # TODO: 实现麦克风初始化逻辑
            return True
        except Exception as e:
            print(f"麦克风初始化失败: {e}")
            return False
    
    def cleanup(self) -> bool:
        """清理麦克风资源"""
        try:
            self.stop_recording()
            return True
        except Exception as e:
            print(f"麦克风清理失败: {e}")
            return False
    
    def start_recording(self) -> bool:
        """开始录音"""
        try:
            self.is_recording = True
            return True
        except Exception as e:
            print(f"录音开始失败: {e}")
            return False
    
    def stop_recording(self) -> bool:
        """停止录音"""
        try:
            self.is_recording = False
            return True
        except Exception as e:
            print(f"录音停止失败: {e}")
            return False
    
    def get_audio_data(self) -> Optional[bytes]:
        """获取音频数据"""
        try:
            # TODO: 实现音频数据获取逻辑
            return None
        except Exception as e:
            print(f"音频数据获取失败: {e}")
            return None
    
    def set_sample_rate(self, sample_rate: int) -> bool:
        """设置采样率"""
        try:
            self.sample_rate = sample_rate
            return True
        except Exception as e:
            print(f"采样率设置失败: {e}")
            return False
    
    def is_available(self) -> bool:
        """检查麦克风是否可用"""
        return True  # TODO: 实现实际的可用性检查
    
    def get_info(self) -> Dict[str, Any]:
        """获取麦克风信息"""
        return {
            "available": self.is_available(),
            "recording": self.is_recording,
            "sample_rate": self.sample_rate
        }

class MacSpeaker(SpeakerInterface):
    """Mac扬声器接口"""
    
    def __init__(self):
        """初始化Mac扬声器"""
        self.volume = 0.8
        self.is_playing = False
    
    def initialize(self) -> bool:
        """初始化扬声器"""
        try:
            return True
        except Exception as e:
            print(f"扬声器初始化失败: {e}")
            return False
    
    def cleanup(self) -> bool:
        """清理扬声器资源"""
        try:
            self.stop_playing()
            return True
        except Exception as e:
            print(f"扬声器清理失败: {e}")
            return False
    
    def play_audio(self, audio_data: bytes) -> bool:
        """播放音频"""
        try:
            # TODO: 实现音频播放逻辑
            return True
        except Exception as e:
            print(f"音频播放失败: {e}")
            return False
    
    def play_text(self, text: str) -> bool:
        """播放文本"""
        try:
            # 使用系统say命令播放文本
            subprocess.run(['say', text], check=True)
            return True
        except Exception as e:
            print(f"文本播放失败: {e}")
            return False
    
    def set_volume(self, volume: float) -> bool:
        """设置音量"""
        try:
            self.volume = max(0.0, min(1.0, volume))
            return True
        except Exception as e:
            print(f"音量设置失败: {e}")
            return False
    
    def stop_playing(self) -> bool:
        """停止播放"""
        try:
            self.is_playing = False
            return True
        except Exception as e:
            print(f"播放停止失败: {e}")
            return False
    
    def get_info(self) -> Dict[str, Any]:
        """获取扬声器信息"""
        return {
            "available": True,
            "volume": self.volume,
            "playing": self.is_playing
        }

class MacNetwork(NetworkInterface):
    """Mac网络接口"""
    
    def __init__(self):
        """初始化Mac网络"""
        self.ip_address = None
    
    def initialize(self) -> bool:
        """初始化网络"""
        try:
            self.ip_address = self.get_ip_address()
            return True
        except Exception as e:
            print(f"网络初始化失败: {e}")
            return False
    
    def cleanup(self) -> bool:
        """清理网络资源"""
        try:
            return True
        except Exception as e:
            print(f"网络清理失败: {e}")
            return False
    
    def check_connection(self) -> bool:
        """检查网络连接"""
        try:
            # 尝试ping Google DNS
            result = subprocess.run(['ping', '-c', '1', '8.8.8.8'], 
                                  capture_output=True, timeout=5)
            return result.returncode == 0
        except Exception as e:
            print(f"网络连接检查失败: {e}")
            return False
    
    def get_ip_address(self) -> Optional[str]:
        """获取IP地址"""
        try:
            result = subprocess.run(['ifconfig'], capture_output=True, text=True)
            # 解析IP地址
            # TODO: 实现IP地址解析逻辑
            return "127.0.0.1"
        except Exception as e:
            print(f"IP地址获取失败: {e}")
            return None
    
    def ping(self, host: str) -> bool:
        """Ping测试"""
        try:
            result = subprocess.run(['ping', '-c', '1', host], 
                                  capture_output=True, timeout=5)
            return result.returncode == 0
        except Exception as e:
            print(f"Ping测试失败: {e}")
            return False
    
    def get_info(self) -> Dict[str, Any]:
        """获取网络信息"""
        return {
            "available": self.check_connection(),
            "ip_address": self.ip_address
        }

class MacYOLO(YOLOInterface):
    """Mac YOLO接口"""
    
    def __init__(self):
        """初始化Mac YOLO"""
        self.model = None
        self.model_path = "yolov8n.pt"
        self.confidence_threshold = 0.5
    
    def initialize(self) -> bool:
        """初始化YOLO模型"""
        try:
            self.model = YOLO(self.model_path)
            return True
        except Exception as e:
            print(f"YOLO模型初始化失败: {e}")
            return False
    
    def cleanup(self) -> bool:
        """清理YOLO模型"""
        try:
            self.model = None
            return True
        except Exception as e:
            print(f"YOLO模型清理失败: {e}")
            return False
    
    def load_model(self, model_path: str) -> bool:
        """加载模型"""
        try:
            self.model_path = model_path
            self.model = YOLO(model_path)
            return True
        except Exception as e:
            print(f"模型加载失败: {e}")
            return False
    
    def predict(self, input_data: Any) -> Any:
        """预测"""
        try:
            if self.model:
                return self.model.predict(input_data)
            return None
        except Exception as e:
            print(f"预测失败: {e}")
            return None
    
    def detect_objects(self, image: Any) -> List[Dict[str, Any]]:
        """检测物体"""
        try:
            if self.model:
                results = self.model.predict(image)
                objects = []
                for result in results:
                    for box in result.boxes:
                        objects.append({
                            "class": box.cls.item(),
                            "confidence": box.conf.item(),
                            "bbox": box.xyxy.tolist()[0]
                        })
                return objects
            return []
        except Exception as e:
            print(f"物体检测失败: {e}")
            return []
    
    def set_confidence_threshold(self, threshold: float) -> bool:
        """设置置信度阈值"""
        try:
            self.confidence_threshold = threshold
            return True
        except Exception as e:
            print(f"置信度阈值设置失败: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            "available": self.model is not None,
            "model_path": self.model_path,
            "confidence_threshold": self.confidence_threshold
        }

class MacWhisper(WhisperInterface):
    """Mac Whisper接口"""
    
    def __init__(self):
        """初始化Mac Whisper"""
        self.model = None
        self.model_size = "base"
        self.language = "zh"
    
    def initialize(self) -> bool:
        """初始化Whisper模型"""
        try:
            self.model = whisper.load_model(self.model_size)
            return True
        except Exception as e:
            print(f"Whisper模型初始化失败: {e}")
            return False
    
    def cleanup(self) -> bool:
        """清理Whisper模型"""
        try:
            self.model = None
            return True
        except Exception as e:
            print(f"Whisper模型清理失败: {e}")
            return False
    
    def load_model(self, model_path: str) -> bool:
        """加载模型"""
        try:
            self.model = whisper.load_model(model_path)
            return True
        except Exception as e:
            print(f"模型加载失败: {e}")
            return False
    
    def predict(self, input_data: Any) -> Any:
        """预测"""
        try:
            if self.model:
                return self.model.transcribe(input_data)
            return None
        except Exception as e:
            print(f"预测失败: {e}")
            return None
    
    def transcribe_audio(self, audio_data: bytes) -> str:
        """转录音频"""
        try:
            if self.model:
                result = self.model.transcribe(audio_data, language=self.language)
                return result["text"]
            return ""
        except Exception as e:
            print(f"音频转录失败: {e}")
            return ""
    
    def set_language(self, language: str) -> bool:
        """设置语言"""
        try:
            self.language = language
            return True
        except Exception as e:
            print(f"语言设置失败: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            "available": self.model is not None,
            "model_size": self.model_size,
            "language": self.language
        }

class MacTTS(TTSInterface):
    """Mac TTS接口"""
    
    def __init__(self):
        """初始化Mac TTS"""
        self.engine = None
        self.voice = None
        self.speed = 1.0
        self.volume = 0.8
    
    def initialize(self) -> bool:
        """初始化TTS引擎"""
        try:
            # 尝试使用edge-tts
            try:
                import edge_tts
                self.engine = "edge-tts"
                return True
            except ImportError:
                pass
            
            # 回退到pyttsx3
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 150)
                self.engine.setProperty('volume', self.volume)
                return True
            except Exception as e:
                print(f"TTS引擎初始化失败: {e}")
                return False
                
        except Exception as e:
            print(f"TTS初始化失败: {e}")
            return False
    
    def cleanup(self) -> bool:
        """清理TTS引擎"""
        try:
            if self.engine and hasattr(self.engine, 'stop'):
                self.engine.stop()
            self.engine = None
            return True
        except Exception as e:
            print(f"TTS清理失败: {e}")
            return False
    
    def synthesize_speech(self, text: str) -> bytes:
        """合成语音"""
        try:
            if self.engine == "edge-tts":
                # 使用edge-tts合成语音
                import asyncio
                import edge_tts
                
                async def _synthesize():
                    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
                    return await communicate.async_synthesize()
                
                audio_data = asyncio.run(_synthesize())
                return audio_data
            else:
                # 使用pyttsx3合成语音
                self.engine.say(text)
                self.engine.runAndWait()
                return b""  # pyttsx3不返回音频数据
                
        except Exception as e:
            print(f"语音合成失败: {e}")
            return b""
    
    def set_voice(self, voice: str) -> bool:
        """设置语音"""
        try:
            self.voice = voice
            return True
        except Exception as e:
            print(f"语音设置失败: {e}")
            return False
    
    def set_speed(self, speed: float) -> bool:
        """设置语速"""
        try:
            self.speed = speed
            if self.engine and hasattr(self.engine, 'setProperty'):
                self.engine.setProperty('rate', int(150 * speed))
            return True
        except Exception as e:
            print(f"语速设置失败: {e}")
            return False
    
    def is_available(self) -> bool:
        """检查TTS是否可用"""
        return self.engine is not None
    
    def get_info(self) -> Dict[str, Any]:
        """获取TTS信息"""
        return {
            "available": self.is_available(),
            "engine": self.engine,
            "voice": self.voice,
            "speed": self.speed,
            "volume": self.volume
        }
