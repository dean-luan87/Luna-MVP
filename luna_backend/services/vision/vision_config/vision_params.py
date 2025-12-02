"""
统一视觉参数：置信度 / IOU / ROI / 加速开关 (v1.2.0)
"""

from typing import Tuple, Dict, Any, Optional
from utils.logger import vision_log


class VisionParams:
    """视觉参数管理器"""
    
    def __init__(self):
        """初始化视觉参数"""
        # YOLO参数
        self.conf_threshold = 0.4
        self.iou_threshold = 0.5
        self.yolo_imgsz = 640
        
        # ROI参数
        self.roi_area = (0.15, 0.85)  # y-range fraction (top, bottom)
        self.roi_enabled = True
        
        # 缓存参数
        self.enable_signature_cache = True
        self.cache_ttl = 5.0  # 秒
        
        # 加速参数
        self.enable_half_precision = True  # FP16
        self.enable_tensorrt = False
        
        # 时序融合参数
        self.enable_temporal_fusion = True
        self.temporal_window_size = 3
        
        # OCR参数
        self.ocr_enabled = True
        self.ocr_confidence_threshold = 0.5
    
    def update(self, params: Dict[str, Any]):
        """
        更新参数
        
        Args:
            params: 参数字典
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
                vision_log("PARAM_UPDATED", {"key": key, "value": value})
    
    def get_all(self) -> Dict[str, Any]:
        """
        获取所有参数
        
        Returns:
            参数字典
        """
        return {
            "conf_threshold": self.conf_threshold,
            "iou_threshold": self.iou_threshold,
            "yolo_imgsz": self.yolo_imgsz,
            "roi_area": self.roi_area,
            "roi_enabled": self.roi_enabled,
            "enable_signature_cache": self.enable_signature_cache,
            "cache_ttl": self.cache_ttl,
            "enable_half_precision": self.enable_half_precision,
            "enable_tensorrt": self.enable_tensorrt,
            "enable_temporal_fusion": self.enable_temporal_fusion,
            "temporal_window_size": self.temporal_window_size,
            "ocr_enabled": self.ocr_enabled,
            "ocr_confidence_threshold": self.ocr_confidence_threshold
        }
    
    def reset_to_default(self):
        """重置为默认参数"""
        self.__init__()
        vision_log("PARAMS_RESET", {})

