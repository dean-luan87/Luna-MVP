"""
危险检测器服务层 (v1.2.0)
"""

import sys
import os
import numpy as np
from typing import List, Dict, Any

# 添加Luna_Badge路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "Luna_Badge"))

from core.logger import logger

try:
    from core.hazard_detector import HazardDetector as CoreHazardDetector
except ImportError:
    CoreHazardDetector = None


class HazardDetector:
    """危险检测器服务类"""
    
    def __init__(self):
        """初始化危险检测器"""
        self.detector: CoreHazardDetector = None
        self._init_detector()
    
    def _init_detector(self):
        """初始化核心危险检测器"""
        try:
            if CoreHazardDetector:
                self.detector = CoreHazardDetector()
                logger.info("✅ 危险检测器初始化成功", module="Vision")
            else:
                logger.warn("危险检测器模块未找到", module="Vision")
        except Exception as e:
            logger.error("危险检测器初始化失败", details={"error": str(e)}, module="Vision")
    
    def detect(self, image_np: np.ndarray, detected_objects: Optional[List] = None) -> List[Dict[str, Any]]:
        """
        检测危险
        
        Args:
            image_np: 输入图像（numpy数组）
            detected_objects: 已检测到的物体列表（可选）
        
        Returns:
            危险列表
        """
        if not self.detector:
            return []
        
        try:
            hazards = self.detector.detect_hazards(image_np, detected_objects=detected_objects)
            if hazards:
                return [h.to_dict() if hasattr(h, 'to_dict') else str(h) for h in hazards]
            return []
        except Exception as e:
            logger.error("危险检测失败", details={"error": str(e)}, module="Vision")
            return []


# 全局实例
_hazard_detector: Optional[HazardDetector] = None

def get_hazard_detector() -> HazardDetector:
    """获取全局危险检测器实例"""
    global _hazard_detector
    if _hazard_detector is None:
        _hazard_detector = HazardDetector()
    return _hazard_detector



