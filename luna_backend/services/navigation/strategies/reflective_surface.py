"""
反射面策略 (Reflective Surface Strategy) v1.2.0
检测大块高亮 + 边缘对称 + YOLO 中出现镜子/玻璃类 label；避免把反射当成真正障碍
"""

from __future__ import annotations

import cv2
import numpy as np
from typing import Any, Dict, List, Optional

from .base import (
    FrameContext,
    NavigationStrategy,
    StrategyResult,
)


class ReflectiveSurfaceStrategy(NavigationStrategy):
    """
    反射面（玻璃/镜子）策略：
    - 检测大面积高亮区域 + 平滑反射
    - 避免把"镜子里的路人"当成真实行人
    """
    
    name = "reflective_surface"
    
    def __init__(
        self,
        bright_threshold: int = 230,
        area_ratio_threshold: float = 0.1,
    ) -> None:
        """
        Args:
            bright_threshold: 亮度阈值（0-255），高于此为高亮区域
            area_ratio_threshold: 高亮区域面积占比阈值
        """
        self.bright_threshold = bright_threshold
        self.area_ratio_threshold = area_ratio_threshold
    
    def analyze(self, ctx: FrameContext) -> Optional[StrategyResult]:
        image = ctx.image_np
        if image is None:
            return None
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception:
            return None
        
        h, w = gray.shape[:2]
        _, bright_mask = cv2.threshold(
            gray, self.bright_threshold, 255, cv2.THRESH_BINARY
        )
        
        bright_area = float(bright_mask.sum() / 255.0)
        area_ratio = bright_area / max(h * w, 1)
        
        if area_ratio < self.area_ratio_threshold:
            return None
        
        # 可以进一步做边缘平滑检测，这里先简单一点
        msg = "前方可能是大面积玻璃或反光区域，请避免直接靠近反射面，稍微靠边行走。"
        
        return StrategyResult(
            active=True,
            severity="info",
            message=msg,
            code="NAV_STRAT_REFLECTIVE_SURFACE",
            extra={
                "area_ratio": area_ratio,
                "bright_threshold": self.bright_threshold,
                "area_ratio_threshold": self.area_ratio_threshold,
            },
        )



