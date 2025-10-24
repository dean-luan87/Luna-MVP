#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge - 配置管理与加载模块
支持双运行环境（Mac / Embedded）的配置管理
"""

import json
import os
import platform
from typing import Dict, Any, Optional
from enum import Enum

class PlatformType(Enum):
    """平台类型枚举"""
    MAC = "mac"
    EMBEDDED = "embedded"

class SystemMode(Enum):
    """系统模式枚举"""
    ACTIVE = "ACTIVE"
    IDLE = "IDLE"
    SLEEP = "SLEEP"
    OFF = "OFF"

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.platform_type = self._detect_platform()
        
    def _detect_platform(self) -> PlatformType:
        """检测当前运行平台"""
        system = platform.system().lower()
        if system == "darwin":
            return PlatformType.MAC
        else:
            # 假设非macOS为嵌入式环境
            return PlatformType.EMBEDDED
    
    def load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置字典
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = self._create_default_config()
                self.save_config()
        except Exception as e:
            print(f"配置加载失败: {e}")
            self.config = self._create_default_config()
        
        return self.config
    
    def save_config(self) -> bool:
        """
        保存配置文件
        
        Returns:
            保存是否成功
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"配置保存失败: {e}")
            return False
    
    def _create_default_config(self) -> Dict[str, Any]:
        """创建默认配置"""
        return {
            "platform": self.platform_type.value,
            "system": {
                "mode": SystemMode.OFF.value,
                "auto_start": False,
                "debug_mode": True
            },
            "hardware": {
                "camera": {
                    "enabled": True,
                    "resolution": "640x480",
                    "fps": 30
                },
                "microphone": {
                    "enabled": True,
                    "sample_rate": 16000,
                    "channels": 1
                },
                "speaker": {
                    "enabled": True,
                    "volume": 0.8
                }
            },
            "ai_models": {
                "yolo": {
                    "model_path": "models/yolov8n.pt",
                    "confidence_threshold": 0.5
                },
                "whisper": {
                    "model_size": "base",
                    "language": "zh"
                }
            },
            "navigation": {
                "environment_detection": True,
                "weather_fail_safe": True,
                "signboard_navigation": True,
                "speech_route_understand": True
            },
            "voice": {
                "wake_word": "启动环境智能导航",
                "tts_engine": "edge-tts" if self.platform_type == PlatformType.MAC else "coqui-tts"
            }
        }
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set_config(self, key: str, value: Any) -> bool:
        """
        设置配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            value: 配置值
            
        Returns:
            设置是否成功
        """
        try:
            keys = key.split('.')
            config = self.config
            
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            config[keys[-1]] = value
            return True
        except Exception as e:
            print(f"配置设置失败: {e}")
            return False
    
    def get_platform_config(self) -> Dict[str, Any]:
        """获取当前平台的配置"""
        return self.config.get("platform", self.platform_type.value)
    
    def is_mac_platform(self) -> bool:
        """判断是否为Mac平台"""
        return self.platform_type == PlatformType.MAC
    
    def is_embedded_platform(self) -> bool:
        """判断是否为嵌入式平台"""
        return self.platform_type == PlatformType.EMBEDDED

# 全局配置实例
config_manager = ConfigManager()
