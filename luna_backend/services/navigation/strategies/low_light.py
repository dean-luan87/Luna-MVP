"""
弱光导航策略 (Low Light Strategy) v1.2.0
根据灰度均值 + 直方图判断弱光，给出"减速 + 近距离提醒"类提示
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


class LowLightStrategy(NavigationStrategy):
    """
    弱光导航策略：
    - 判断当前画面是否整体偏暗
    - 可选：检测高噪声区域（ISO很高时噪点多）
    - 给出"减速、注意脚下"的提示
    """
    
    name = "low_light"
    
    def __init__(
        self,
        brightness_threshold: float = 60.0,
        dark_ratio_threshold: float = 0.6,
    ) -> None:
        """
        Args:
            brightness_threshold: 灰度均值阈值（0-255），低于此值认为整体偏暗
            dark_ratio_threshold: 直方图中偏暗像素占比阈值
        """
        self.brightness_threshold = brightness_threshold
        self.dark_ratio_threshold = dark_ratio_threshold
    
    def analyze(self, ctx: FrameContext) -> Optional[StrategyResult]:
        image = ctx.image_np
        if image is None:
            return None
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception:
            # 万一格式不对，直接跳过
            return None
        
        mean_brightness = float(gray.mean())
        
        # 统计暗像素比例（0~80 作为暗区）
        hist = cv2.calcHist([gray], [0], None, [64], [0, 256])
        total_pixels = gray.size
        dark_pixels = hist[:20].sum()  # 约 0~80
        dark_ratio = float(dark_pixels / max(total_pixels, 1))
        
        is_low_light = (
            mean_brightness < self.brightness_threshold
            and dark_ratio > self.dark_ratio_threshold
        )
        
        if not is_low_light:
            return None
        
        # 提示语不搞太花：核心是"弱光 + 慢行 + 注意脚下"
        msg = "当前环境光线较暗，请放慢速度，注意脚下。"
        
        return StrategyResult(
            active=True,
            severity="warning",
            message=msg,
            code="NAV_STRAT_LOW_LIGHT",
            extra={
                "mean_brightness": mean_brightness,
                "dark_ratio": dark_ratio,
                "brightness_threshold": self.brightness_threshold,
                "dark_ratio_threshold": self.dark_ratio_threshold,
            },
        )



