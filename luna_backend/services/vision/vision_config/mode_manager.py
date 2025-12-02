"""
切换视觉模式（默认 / 快速 / 低功耗）(v1.2.0)
"""

from typing import Dict, Any
from enum import Enum
from utils.logger import vision_log


class VisionMode(Enum):
    """视觉模式枚举"""
    DEFAULT = "default"      # 默认模式
    FAST = "fast"            # 快速模式
    LOW_POWER = "low_power"  # 低功耗模式
    HIGH_QUALITY = "high_quality"  # 高质量模式


class VisionModeManager:
    """视觉模式管理器"""
    
    def __init__(self):
        """初始化视觉模式管理器"""
        self.mode = VisionMode.DEFAULT
        self.mode_configs = {
            VisionMode.DEFAULT: {
                "yolo_imgsz": 640,
                "conf_threshold": 0.4,
                "enable_cache": True,
                "enable_temporal_fusion": True
            },
            VisionMode.FAST: {
                "yolo_imgsz": 416,
                "conf_threshold": 0.5,
                "enable_cache": True,
                "enable_temporal_fusion": False
            },
            VisionMode.LOW_POWER: {
                "yolo_imgsz": 320,
                "conf_threshold": 0.6,
                "enable_cache": True,
                "enable_temporal_fusion": False
            },
            VisionMode.HIGH_QUALITY: {
                "yolo_imgsz": 1280,
                "conf_threshold": 0.3,
                "enable_cache": True,
                "enable_temporal_fusion": True
            }
        }
    
    def set_mode(self, mode: str):
        """
        设置视觉模式
        
        Args:
            mode: 模式名称（"default", "fast", "low_power", "high_quality"）
        """
        try:
            self.mode = VisionMode(mode)
            vision_log("MODE_CHANGED", {"mode": mode})
        except ValueError:
            vision_log("MODE_INVALID", {"mode": mode})
            self.mode = VisionMode.DEFAULT
    
    def get_mode(self) -> str:
        """
        获取当前模式
        
        Returns:
            当前模式名称
        """
        return self.mode.value
    
    def get_config(self) -> Dict[str, Any]:
        """
        获取当前模式的配置
        
        Returns:
            模式配置字典
        """
        return self.mode_configs.get(self.mode, self.mode_configs[VisionMode.DEFAULT])
    
    def update_config(self, mode: str, config: Dict[str, Any]):
        """
        更新指定模式的配置
        
        Args:
            mode: 模式名称
            config: 配置字典
        """
        try:
            mode_enum = VisionMode(mode)
            if mode_enum in self.mode_configs:
                self.mode_configs[mode_enum].update(config)
                vision_log("CONFIG_UPDATED", {"mode": mode, "config": config})
        except ValueError:
            vision_log("MODE_INVALID", {"mode": mode})



