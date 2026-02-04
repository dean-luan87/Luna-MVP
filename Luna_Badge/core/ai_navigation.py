#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge - AI识别模块统一调度
环境检测、天气故障保护、指示牌导航、语音路径理解
"""

import time
import threading
import cv2
import numpy as np
import os
from typing import Dict, List, Any, Optional
from enum import Enum

from .config import config_manager

# 尝试导入AI模型依赖
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️ YOLO模块加载失败：ultralytics")

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️ Whisper模块加载失败：openai-whisper")

class NavigationModule(Enum):
    """导航模块枚举"""
    ENVIRONMENT_DETECT = "environment_detect"
    WEATHER_FAIL_SAFE = "weather_fail_safe"
    SIGNBOARD_NAVIGATION = "signboard_navigation"
    SPEECH_ROUTE_UNDERSTAND = "speech_route_understand"

class ModuleStatus(Enum):
    """模块状态枚举"""
    IDLE = "idle"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"

class AINavigation:
    """AI导航统一调度器"""
    
    def __init__(self):
        """初始化AI导航调度器"""
        self.modules = {}
        self.module_status = {}
        self.is_running = False
        self.hal_interface = None
        
        # 配置
        self.config = config_manager.load_config()
        
        # 初始化模块状态
        for module in NavigationModule:
            self.module_status[module] = ModuleStatus.IDLE
        
        # 初始化AI模型
        self.yolo_model = None
        self.whisper_model = None
        self.camera = None
        self.is_yolo_initialized = False
        self.is_whisper_initialized = False
        
        # 初始化AI模型
        self._initialize_ai_models()
    
    def set_hal_interface(self, hal_interface):
        """设置硬件抽象层接口"""
        self.hal_interface = hal_interface
    
    def _initialize_ai_models(self):
        """初始化AI模型"""
        try:
            # 初始化YOLO模型
            if YOLO_AVAILABLE:
                print("🚀 正在加载YOLOv8n模型...")
                self.yolo_model = YOLO('yolov8n.pt')
                self.is_yolo_initialized = True
                print("✅ YOLOv8n模型加载成功")
            else:
                print("⚠️ YOLO模块加载失败：ultralytics")
                
            # 初始化Whisper模型
            if WHISPER_AVAILABLE:
                print("🎧 正在加载Whisper模型...")
                self.whisper_model = whisper.load_model("base")
                self.is_whisper_initialized = True
                print("✅ Whisper模型加载成功")
            else:
                print("⚠️ Whisper模块加载失败：openai-whisper")
                
        except Exception as e:
            print(f"❌ AI模型初始化失败: {e}")
    
    def start_yolo_detection(self, duration=10):
        """
        启动YOLO实时检测
        
        Args:
            duration: 检测持续时间（秒）
        """
        if not self.is_yolo_initialized:
            print("⚠️ YOLO模型未初始化，无法启动检测")
            return False
        
        try:
            print("🚀 YOLO 推理启动")
            
            # 初始化摄像头
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                print("❌ 摄像头初始化失败")
                return False
            
            # 注册摄像头到资源管理器
            if self.camera_manager:
                self.camera_manager.register_camera(self.camera)
            
            start_time = time.time()
            frame_count = 0
            
            while time.time() - start_time < duration:
                ret, frame = self.camera.read()
                if not ret:
                    print("❌ 无法读取摄像头帧")
                    break
                
                frame_count += 1
                
                # 每5帧进行一次检测（降低计算负载）
                if frame_count % 5 == 0:
                    # YOLO检测
                    results = self.yolo_model(frame, verbose=False)
                    
                    # 处理检测结果
                    for result in results:
                        boxes = result.boxes
                        if boxes is not None:
                            for box in boxes:
                                # 获取检测信息
                                conf = box.conf.item()
                                cls = int(box.cls.item())
                                class_name = self.yolo_model.names[cls]
                                
                                # 打印检测结果
                                print(f"🔍 检测到: {class_name} (置信度: {conf:.2f})")
                                
                                # 安全提示检测
                                if class_name in ['person', 'car', 'truck', 'bus', 'motorcycle']:
                                    safety_msg = self._get_safety_message(class_name)
                                    print(f"⚠️ 安全提示: {safety_msg}")
                                    
                                    # 语音播报安全提示
                                    if self.hal_interface and hasattr(self.hal_interface, 'speak'):
                                        try:
                                            self.hal_interface.speak(safety_msg)
                                            print("🗣️ 播报完成")
                                        except Exception as e:
                                            print(f"❌ 语音播报失败: {e}")
                
                # 显示帧（可选）
                cv2.imshow('Luna YOLO Detection', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # 清理资源
            self._cleanup_camera()
            print("✅ YOLO检测完成")
            return True
            
        except KeyboardInterrupt:
            print("\n⚠️ 用户中断检测")
            self._cleanup_camera()
            return False
        except Exception as e:
            print(f"❌ YOLO检测失败: {e}")
            self._cleanup_camera()
            return False
        finally:
            # 确保摄像头关闭
            self._cleanup_camera()
    
    def _cleanup_camera(self):
        """清理摄像头资源"""
        try:
            if self.camera:
                # 从资源管理器注销
                if self.camera_manager:
                    self.camera_manager.unregister_camera(self.camera)
                
                self.camera.release()
                self.camera = None
            cv2.destroyAllWindows()
            
            # 尝试使用摄像头管理器关闭
            try:
                from core.camera_manager import get_camera_manager
                camera_manager = get_camera_manager()
                if camera_manager.state.is_open:
                    camera_manager.close_camera()
            except Exception:
                pass
                
            # 强制清理所有摄像头资源
            if self.camera_manager:
                self.camera_manager.force_cleanup_all()
                
        except Exception as e:
            print(f"⚠️ 摄像头清理警告: {e}")
    
    def _get_safety_message(self, class_name):
        """根据检测到的对象类型生成安全提示"""
        safety_messages = {
            'person': '检测到行人，请注意避让',
            'car': '检测到车辆，请注意安全',
            'truck': '检测到卡车，请保持距离',
            'bus': '检测到公交车，请注意安全',
            'motorcycle': '检测到摩托车，请小心避让'
        }
        return safety_messages.get(class_name, '检测到移动物体，请注意安全')
    
    def start_whisper_listening(self, audio_file=None):
        """
        启动Whisper语音识别
        
        Args:
            audio_file: 音频文件路径，如果为None则使用麦克风
        """
        if not self.is_whisper_initialized:
            print("⚠️ Whisper模型未初始化，无法启动语音识别")
            return None
        
        try:
            print("🎧 Whisper 听取中")
            
            if audio_file:
                # 从音频文件识别
                if not os.path.exists(audio_file):
                    print(f"❌ 音频文件不存在: {audio_file}")
                    return None
                
                # 支持多种音频格式
                supported_formats = ['.wav', '.mp3', '.aiff', '.m4a', '.flac']
                file_ext = os.path.splitext(audio_file)[1].lower()
                
                if file_ext not in supported_formats:
                    print(f"⚠️ 不支持的音频格式: {file_ext}")
                    return None
                
                result = self.whisper_model.transcribe(audio_file, language='zh')
                text = result['text'].strip()
                
            else:
                # 从麦克风识别（简化版本，实际应该使用音频录制）
                print("⚠️ 麦克风输入功能需要音频录制实现")
                # 这里可以使用pyaudio录制音频，然后传递给whisper
                return None
            
            if text:
                print(f"用户说：{text}")
                return text
            else:
                print("⚠️ 未识别到语音内容")
                return None
                
        except Exception as e:
            print(f"❌ Whisper语音识别失败: {e}")
            return None
    
    def initialize_modules(self) -> bool:
        """
        初始化所有AI模块（统一使用嵌入式平台）
        
        Returns:
            初始化是否成功
        """
        try:
            # 统一使用嵌入式平台模块
            self._initialize_embedded_modules()
            
            return True
            
        except Exception as e:
            print(f"AI模块初始化失败: {e}")
            return False
    
    def _initialize_embedded_modules(self):
        """初始化嵌入式平台的AI模块"""
        # 环境检测模块
        self.modules[NavigationModule.ENVIRONMENT_DETECT] = EmbeddedEnvironmentDetector()
        
        # 天气故障保护模块
        self.modules[NavigationModule.WEATHER_FAIL_SAFE] = EmbeddedWeatherFailSafe()
        
        # 指示牌导航模块
        self.modules[NavigationModule.SIGNBOARD_NAVIGATION] = EmbeddedSignboardNavigation()
        
        # 语音路径理解模块
        self.modules[NavigationModule.SPEECH_ROUTE_UNDERSTAND] = EmbeddedSpeechRouteUnderstand()
    
    def start_auto_navigation(self) -> bool:
        """
        启动自动导航
        
        Returns:
            启动是否成功
        """
        try:
            if self.hal_interface:
                self.hal_interface.speak("启动环境智能导航系统")
            
            self.is_running = True
            
            # 依次启动各个模块
            self._run_environment_detect()
            self._run_weather_fail_safe()
            self._run_signboard_navigation()
            self._run_speech_route_understand()
            
            if self.hal_interface:
                self.hal_interface.speak("导航模式已启动")
            
            return True
            
        except Exception as e:
            print(f"自动导航启动失败: {e}")
            return False
    
    def stop_auto_navigation(self) -> bool:
        """
        停止自动导航
        
        Returns:
            停止是否成功
        """
        try:
            self.is_running = False
            
            # 停止所有模块
            for module in self.modules.values():
                if hasattr(module, 'stop'):
                    module.stop()
            
            return True
            
        except Exception as e:
            print(f"自动导航停止失败: {e}")
            return False
    
    def _run_environment_detect(self):
        """运行环境检测模块"""
        try:
            if self.hal_interface:
                self.hal_interface.speak("正在识别环境类型")
            
            module = self.modules.get(NavigationModule.ENVIRONMENT_DETECT)
            if module:
                self.module_status[NavigationModule.ENVIRONMENT_DETECT] = ModuleStatus.RUNNING
                result = module.detect_environment()
                self.module_status[NavigationModule.ENVIRONMENT_DETECT] = ModuleStatus.IDLE
                
                # 处理检测结果
                self._handle_environment_result(result)
            
        except Exception as e:
            print(f"环境检测模块运行失败: {e}")
            self.module_status[NavigationModule.ENVIRONMENT_DETECT] = ModuleStatus.ERROR
    
    def _run_weather_fail_safe(self):
        """运行天气故障保护模块"""
        try:
            if self.hal_interface:
                self.hal_interface.speak("检测天气与能见度中")
            
            module = self.modules.get(NavigationModule.WEATHER_FAIL_SAFE)
            if module:
                self.module_status[NavigationModule.WEATHER_FAIL_SAFE] = ModuleStatus.RUNNING
                result = module.check_weather()
                self.module_status[NavigationModule.WEATHER_FAIL_SAFE] = ModuleStatus.IDLE
                
                # 处理检测结果
                self._handle_weather_result(result)
            
        except Exception as e:
            print(f"天气故障保护模块运行失败: {e}")
            self.module_status[NavigationModule.WEATHER_FAIL_SAFE] = ModuleStatus.ERROR
    
    def _run_signboard_navigation(self):
        """运行指示牌导航模块"""
        try:
            if self.hal_interface:
                self.hal_interface.speak("扫描指示牌")
            
            module = self.modules.get(NavigationModule.SIGNBOARD_NAVIGATION)
            if module:
                self.module_status[NavigationModule.SIGNBOARD_NAVIGATION] = ModuleStatus.RUNNING
                result = module.detect_signboards()
                self.module_status[NavigationModule.SIGNBOARD_NAVIGATION] = ModuleStatus.IDLE
                
                # 处理检测结果
                self._handle_signboard_result(result)
            
        except Exception as e:
            print(f"指示牌导航模块运行失败: {e}")
            self.module_status[NavigationModule.SIGNBOARD_NAVIGATION] = ModuleStatus.ERROR
    
    def _run_speech_route_understand(self):
        """运行语音路径理解模块"""
        try:
            if self.hal_interface:
                self.hal_interface.speak("等待语音导航指令")
            
            module = self.modules.get(NavigationModule.SPEECH_ROUTE_UNDERSTAND)
            if module:
                self.module_status[NavigationModule.SPEECH_ROUTE_UNDERSTAND] = ModuleStatus.RUNNING
                result = module.understand_route()
                self.module_status[NavigationModule.SPEECH_ROUTE_UNDERSTAND] = ModuleStatus.IDLE
                
                # 处理检测结果
                self._handle_speech_result(result)
            
        except Exception as e:
            print(f"语音路径理解模块运行失败: {e}")
            self.module_status[NavigationModule.SPEECH_ROUTE_UNDERSTAND] = ModuleStatus.ERROR
    
    def _handle_environment_result(self, result: Dict[str, Any]):
        """处理环境检测结果"""
        if result and result.get("success"):
            environment_type = result.get("environment_type", "未知")
            safety_level = result.get("safety_level", "未知")
            
            print(f"环境检测结果: {environment_type} - {safety_level}")
            
            # 根据检测结果进行语音播报
            if self.hal_interface:
                if safety_level == "安全":
                    self.hal_interface.speak(f"检测到{environment_type}，安全模式")
                else:
                    self.hal_interface.speak(f"检测到{environment_type}，请注意安全")
    
    def _handle_weather_result(self, result: Dict[str, Any]):
        """处理天气检测结果"""
        if result and result.get("success"):
            weather_status = result.get("status", "正常")
            print(f"天气检测结果: {weather_status}")
            
            if self.hal_interface:
                if weather_status == "正常":
                    self.hal_interface.speak("天气正常")
                else:
                    self.hal_interface.speak(f"天气异常: {weather_status}")
    
    def _handle_signboard_result(self, result: Dict[str, Any]):
        """处理指示牌检测结果"""
        if result and result.get("success"):
            signboards = result.get("signboards", [])
            
            if signboards:
                for signboard in signboards:
                    direction = signboard.get("direction", "未知")
                    distance = signboard.get("distance", "未知")
                    print(f"检测到指示牌: {direction} {distance}米")
                    
                    if self.hal_interface:
                        self.hal_interface.speak(f"检测到{direction}标志，请向{direction}方向{distance}米移动")
            else:
                print("未检测到指示牌")
    
    def _handle_speech_result(self, result: Dict[str, Any]):
        """处理语音路径理解结果"""
        if result and result.get("success"):
            route_summary = result.get("summary", "未知路线")
            print(f"语音路径理解结果: {route_summary}")
            
            if self.hal_interface:
                self.hal_interface.speak(f"好的，我记住路线了: {route_summary}")
    
    def get_module_status(self) -> Dict[str, str]:
        """获取所有模块状态"""
        return {module.value: status.value for module, status in self.module_status.items()}
    
    def get_status(self) -> Dict[str, Any]:
        """获取AI导航状态"""
        return {
            "is_running": self.is_running,
            "module_status": self.get_module_status(),
            "modules_count": len(self.modules)
        }

# 嵌入式平台AI模块基类（唯一平台支持）
class EmbeddedEnvironmentDetector:
    """嵌入式平台环境检测器"""
    
    def detect_environment(self) -> Dict[str, Any]:
        """检测环境"""
        # TODO: 实现嵌入式平台的环境检测逻辑
        return {"success": True, "environment_type": "人行道", "safety_level": "安全"}

class EmbeddedWeatherFailSafe:
    """嵌入式平台天气故障保护器"""
    
    def check_weather(self) -> Dict[str, Any]:
        """检查天气"""
        # TODO: 实现嵌入式平台的天气检查逻辑
        return {"success": True, "status": "正常"}

class EmbeddedSignboardNavigation:
    """嵌入式平台指示牌导航器"""
    
    def detect_signboards(self) -> Dict[str, Any]:
        """检测指示牌"""
        # TODO: 实现嵌入式平台的指示牌检测逻辑
        return {"success": True, "signboards": []}

class EmbeddedSpeechRouteUnderstand:
    """嵌入式平台语音路径理解器"""
    
    def understand_route(self) -> Dict[str, Any]:
        """理解路径"""
        # TODO: 实现嵌入式平台的语音路径理解逻辑
        return {"success": True, "summary": "前方两个红绿灯后右转"}
