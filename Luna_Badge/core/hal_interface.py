#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge - 硬件抽象层接口定义
定义统一的硬件接口，支持Mac和嵌入式平台
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from enum import Enum

class HardwareType(Enum):
    """硬件类型枚举"""
    CAMERA = "camera"
    MICROPHONE = "microphone"
    SPEAKER = "speaker"
    NETWORK = "network"

class HardwareInterface(ABC):
    """硬件抽象层接口基类"""
    
    @abstractmethod
    def initialize(self) -> bool:
        """初始化硬件"""
        pass
    
    @abstractmethod
    def cleanup(self) -> bool:
        """清理硬件资源"""
        pass
    
    @abstractmethod
    def speak(self, text: str) -> bool:
        """语音播报"""
        pass
    
    @abstractmethod
    def check_camera(self) -> bool:
        """检查摄像头状态"""
        pass
    
    @abstractmethod
    def check_microphone(self) -> bool:
        """检查麦克风状态"""
        pass
    
    @abstractmethod
    def check_network(self) -> bool:
        """检查网络连接"""
        pass
    
    @abstractmethod
    def check_voice_engine(self) -> bool:
        """检查语音引擎状态"""
        pass
    
    @abstractmethod
    def detect_wake_word(self) -> bool:
        """检测语音唤醒词"""
        pass
    
    @abstractmethod
    def get_hardware_info(self) -> Dict[str, Any]:
        """获取硬件信息"""
        pass

class CameraInterface(ABC):
    """摄像头接口"""
    
    @abstractmethod
    def start_camera(self) -> bool:
        """启动摄像头"""
        pass
    
    @abstractmethod
    def stop_camera(self) -> bool:
        """停止摄像头"""
        pass
    
    @abstractmethod
    def capture_frame(self) -> Optional[Any]:
        """捕获帧"""
        pass
    
    @abstractmethod
    def set_resolution(self, width: int, height: int) -> bool:
        """设置分辨率"""
        pass
    
    @abstractmethod
    def set_fps(self, fps: int) -> bool:
        """设置帧率"""
        pass

class MicrophoneInterface(ABC):
    """麦克风接口"""
    
    @abstractmethod
    def start_recording(self) -> bool:
        """开始录音"""
        pass
    
    @abstractmethod
    def stop_recording(self) -> bool:
        """停止录音"""
        pass
    
    @abstractmethod
    def get_audio_data(self) -> Optional[bytes]:
        """获取音频数据"""
        pass
    
    @abstractmethod
    def set_sample_rate(self, sample_rate: int) -> bool:
        """设置采样率"""
        pass

class SpeakerInterface(ABC):
    """扬声器接口"""
    
    @abstractmethod
    def play_audio(self, audio_data: bytes) -> bool:
        """播放音频"""
        pass
    
    @abstractmethod
    def play_text(self, text: str) -> bool:
        """播放文本"""
        pass
    
    @abstractmethod
    def set_volume(self, volume: float) -> bool:
        """设置音量"""
        pass
    
    @abstractmethod
    def stop_playing(self) -> bool:
        """停止播放"""
        pass

class NetworkInterface(ABC):
    """网络接口"""
    
    @abstractmethod
    def check_connection(self) -> bool:
        """检查网络连接"""
        pass
    
    @abstractmethod
    def get_ip_address(self) -> Optional[str]:
        """获取IP地址"""
        pass
    
    @abstractmethod
    def ping(self, host: str) -> bool:
        """Ping测试"""
        pass

class AIModelInterface(ABC):
    """AI模型接口"""
    
    @abstractmethod
    def load_model(self, model_path: str) -> bool:
        """加载模型"""
        pass
    
    @abstractmethod
    def predict(self, input_data: Any) -> Any:
        """预测"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        pass

class YOLOInterface(AIModelInterface):
    """YOLO模型接口"""
    
    @abstractmethod
    def detect_objects(self, image: Any) -> List[Dict[str, Any]]:
        """检测物体"""
        pass
    
    @abstractmethod
    def set_confidence_threshold(self, threshold: float) -> bool:
        """设置置信度阈值"""
        pass

class WhisperInterface(AIModelInterface):
    """Whisper语音识别接口"""
    
    @abstractmethod
    def transcribe_audio(self, audio_data: bytes) -> str:
        """转录音频"""
        pass
    
    @abstractmethod
    def set_language(self, language: str) -> bool:
        """设置语言"""
        pass

class TTSInterface(ABC):
    """文本转语音接口"""
    
    @abstractmethod
    def synthesize_speech(self, text: str) -> bytes:
        """合成语音"""
        pass
    
    @abstractmethod
    def set_voice(self, voice: str) -> bool:
        """设置语音"""
        pass
    
    @abstractmethod
    def set_speed(self, speed: float) -> bool:
        """设置语速"""
        pass

class HardwareManager:
    """硬件管理器"""
    
    def __init__(self):
        """初始化硬件管理器"""
        self.interfaces = {}
        self.is_initialized = False
    
    def register_interface(self, hardware_type: HardwareType, interface: Any) -> bool:
        """
        注册硬件接口
        
        Args:
            hardware_type: 硬件类型
            interface: 硬件接口实例
            
        Returns:
            注册是否成功
        """
        try:
            self.interfaces[hardware_type] = interface
            return True
        except Exception as e:
            print(f"硬件接口注册失败: {e}")
            return False
    
    def get_interface(self, hardware_type: HardwareType) -> Optional[Any]:
        """
        获取硬件接口
        
        Args:
            hardware_type: 硬件类型
            
        Returns:
            硬件接口实例
        """
        return self.interfaces.get(hardware_type)
    
    def initialize_all(self) -> bool:
        """
        初始化所有硬件接口
        
        Returns:
            初始化是否成功
        """
        try:
            for interface in self.interfaces.values():
                if hasattr(interface, 'initialize'):
                    if not interface.initialize():
                        return False
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            print(f"硬件初始化失败: {e}")
            return False
    
    def cleanup_all(self) -> bool:
        """
        清理所有硬件接口
        
        Returns:
            清理是否成功
        """
        try:
            for interface in self.interfaces.values():
                if hasattr(interface, 'cleanup'):
                    interface.cleanup()
            
            self.is_initialized = False
            return True
            
        except Exception as e:
            print(f"硬件清理失败: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """获取硬件状态"""
        status = {
            "is_initialized": self.is_initialized,
            "interfaces": {}
        }
        
        for hardware_type, interface in self.interfaces.items():
            status["interfaces"][hardware_type.value] = {
                "available": interface is not None,
                "type": type(interface).__name__
            }
        
        return status
