"""
户外强逆光策略 (Backlight Strategy) v1.2.0
画面中心高曝光 + 周边暗、对比强 → 逆光；提醒"有强光、帮你校正方向"
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


class BacklightStrategy(NavigationStrategy):
    """
    户外强逆光策略：
    - 检测画面中间高曝光区域
    - 提醒用户前方有强光，可能看不清细节
    """
    
    name = "backlight"
    
    def __init__(
        self,
        center_ratio: float = 0.4,
        center_bright_threshold: int = 220,
        contrast_threshold: float = 35.0,
    ) -> None:
        self.center_ratio = center_ratio
        self.center_bright_threshold = center_bright_threshold
        self.contrast_threshold = contrast_threshold
    
    def analyze(self, ctx: FrameContext) -> Optional[StrategyResult]:
        image = ctx.image_np
        if image is None:
            return None
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception:
            return None
        
        h, w = gray.shape[:2]
        
        # 中心区域
        ch = int(h * self.center_ratio)
        cw = int(w * self.center_ratio)
        y1 = (h - ch) // 2
        x1 = (w - cw) // 2
        center_roi = gray[y1 : y1 + ch, x1 : x1 + cw]
        
        center_mean = float(center_roi.mean())
        global_mean = float(gray.mean())
        contrast = center_mean - global_mean  # 中心比整体亮多少
        
        if center_mean < self.center_bright_threshold:
            return None
        
        if contrast < self.contrast_threshold:
            return None
        
        msg = "前方有强光区域，可能看不清细节，我会帮你注意前方情况，请稍微偏离强光方向行走。"
        
        return StrategyResult(
            active=True,
            severity="info",
            message=msg,
            code="NAV_STRAT_BACKLIGHT",
            extra={
                "center_mean": center_mean,
                "global_mean": global_mean,
                "contrast": contrast,
                "center_bright_threshold": self.center_bright_threshold,
                "contrast_threshold": self.contrast_threshold,
            },
        )



