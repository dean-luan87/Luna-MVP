"""
水面反光/地面积水策略 (Water Reflection Strategy) v1.2.0
检测地面大片高反射 + 模糊边缘 → 可能是水；提醒打滑/积水
"""

from __future__ import annotations

import cv2
import numpy as np
from typing import Optional

from .base import (
    FrameContext,
    NavigationStrategy,
    StrategyResult,
)


class WaterReflectionStrategy(NavigationStrategy):
    """
    水面反光 / 地面积水策略：
    - 检测地面区域中的反光 + 模糊纹理
    - 提醒可能打滑或有积水
    """
    
    name = "water_reflection"
    
    def __init__(
        self,
        bottom_ratio: float = 0.5,
        reflection_bright_threshold: int = 200,
        area_ratio_threshold: float = 0.08,
    ) -> None:
        """
        Args:
            bottom_ratio: 只在画面下半部分检测水（默认0.5）
            reflection_bright_threshold: 亮度阈值
            area_ratio_threshold: 反光区域占比阈值
        """
        self.bottom_ratio = bottom_ratio
        self.reflection_bright_threshold = reflection_bright_threshold
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
        start_row = int(h * (1.0 - self.bottom_ratio))
        roi = gray[start_row:, :]
        
        _, mask = cv2.threshold(
            roi, self.reflection_bright_threshold, 255, cv2.THRESH_BINARY
        )
        
        area = float(mask.sum() / 255.0)
        area_ratio = area / max(roi.size, 1)
        
        if area_ratio < self.area_ratio_threshold:
            return None
        
        msg = "前方地面可能有积水或湿滑区域，请放慢速度，小心打滑。"
        
        return StrategyResult(
            active=True,
            severity="warning",
            message=msg,
            code="NAV_STRAT_WATER_REFLECTION",
            extra={
                "area_ratio": area_ratio,
                "reflection_bright_threshold": self.reflection_bright_threshold,
                "area_ratio_threshold": self.area_ratio_threshold,
            },
        )



