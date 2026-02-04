"""
一些环境标志位，用于在嵌入式中关闭不必要功能 (v1.2.0)
"""

from typing import Optional, Dict, Any
from utils.logger import vision_log


class EnvFlags:
    """环境标志管理器"""
    
    def __init__(self):
        """初始化环境标志"""
        # 调试标志
        self.debug_mode = False
        self.verbose_logging = False
        
        # 性能标志
        self.low_power = False
        self.enable_gpu = True
        
        # 功能标志
        self.snapshot_allowed = True
        self.save_detection_images = False
        
        # 嵌入式标志
        self.is_embedded = False
        self.memory_limit_mb = None  # None表示无限制
        
        # 开发标志
        self.enable_profiling = False
        self.enable_metrics = True
    
    def set_embedded_mode(self, memory_limit_mb: Optional[int] = None):
        """
        设置嵌入式模式
        
        Args:
            memory_limit_mb: 内存限制（MB）
        """
        self.is_embedded = True
        self.low_power = True
        self.enable_gpu = False
        self.snapshot_allowed = False
        self.save_detection_images = False
        self.memory_limit_mb = memory_limit_mb
        
        vision_log("EMBEDDED_MODE_ENABLED", {"memory_limit_mb": memory_limit_mb})
    
    def set_debug_mode(self, enabled: bool = True):
        """
        设置调试模式
        
        Args:
            enabled: 是否启用
        """
        self.debug_mode = enabled
        self.verbose_logging = enabled
        self.enable_profiling = enabled
        
        vision_log("DEBUG_MODE_CHANGED", {"enabled": enabled})
    
    def get_all(self) -> Dict[str, Any]:
        """
        获取所有标志
        
        Returns:
            标志字典
        """
        return {
            "debug_mode": self.debug_mode,
            "verbose_logging": self.verbose_logging,
            "low_power": self.low_power,
            "enable_gpu": self.enable_gpu,
            "snapshot_allowed": self.snapshot_allowed,
            "save_detection_images": self.save_detection_images,
            "is_embedded": self.is_embedded,
            "memory_limit_mb": self.memory_limit_mb,
            "enable_profiling": self.enable_profiling,
            "enable_metrics": self.enable_metrics
        }

