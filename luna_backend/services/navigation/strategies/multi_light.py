"""
多点光源干扰策略 (Multi Light Strategy) v1.2.0
检测画面中多个高亮小斑点 + 局部过曝区，提示"光源复杂、识别可能不稳定"
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


class MultiLightStrategy(NavigationStrategy):
    """
    多点光源 / 复杂照明策略：
    - 检测多处高亮小区域（车灯、招牌灯等）
    - 提醒可能存在识别不稳定，建议用户更谨慎
    """
    
    name = "multi_light"
    
    def __init__(
        self,
        bright_threshold: int = 220,
        min_contour_area: int = 20,
        multi_light_count_threshold: int = 5,
    ) -> None:
        self.bright_threshold = bright_threshold
        self.min_contour_area = min_contour_area
        self.multi_light_count_threshold = multi_light_count_threshold
    
    def analyze(self, ctx: FrameContext) -> Optional[StrategyResult]:
        image = ctx.image_np
        if image is None:
            return None
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception:
            return None
        
        _, mask = cv2.threshold(
            gray, self.bright_threshold, 255, cv2.THRESH_BINARY
        )
        
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        bright_spots = [
            c for c in contours if cv2.contourArea(c) >= self.min_contour_area
        ]
        count = len(bright_spots)
        
        if count < self.multi_light_count_threshold:
            return None
        
        msg = "前方光源较多，环境较复杂，可能存在车灯或招牌灯，请特别注意周围动态。"
        
        return StrategyResult(
            active=True,
            severity="info",
            message=msg,
            code="NAV_STRAT_MULTI_LIGHT",
            extra={
                "bright_spots": count,
                "bright_threshold": self.bright_threshold,
                "min_contour_area": self.min_contour_area,
                "multi_light_count_threshold": self.multi_light_count_threshold,
            },
        )



