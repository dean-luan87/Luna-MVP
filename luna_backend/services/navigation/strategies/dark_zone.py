"""
夜间路灯/暗区跳变策略 (Dark Zone Strategy) v1.2.0
画面中存在亮区 + 暗区强对比，尤其是下半部分出现突暗区域 → 提醒"马上进入暗区"
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


class DarkZoneStrategy(NavigationStrategy):
    """
    夜间路灯 / 暗区跳变策略：
    - 检测亮区和暗区的强烈分界
    - 提醒用户准备从亮处进入暗区或反之
    """
    
    name = "dark_zone_jump"
    
    def __init__(
        self,
        bottom_ratio: float = 0.6,
        dark_threshold: int = 50,
        bright_threshold: int = 200,
        jump_ratio_threshold: float = 0.25,
    ) -> None:
        self.bottom_ratio = bottom_ratio
        self.dark_threshold = dark_threshold
        self.bright_threshold = bright_threshold
        self.jump_ratio_threshold = jump_ratio_threshold
    
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
        
        # 统计暗区和亮区像素比例
        dark_mask = (roi < self.dark_threshold).astype(np.uint8)
        bright_mask = (roi > self.bright_threshold).astype(np.uint8)
        
        dark_ratio = float(dark_mask.sum()) / max(roi.size, 1)
        bright_ratio = float(bright_mask.sum()) / max(roi.size, 1)
        
        # 亮暗都有，且某一方占比明显
        if dark_ratio < self.jump_ratio_threshold and bright_ratio < self.jump_ratio_threshold:
            return None
        
        if dark_ratio > bright_ratio:
            msg = "前方即将进入较暗的区域，光线会变暗，请放慢速度，注意脚下。"
            code = "NAV_STRAT_DARK_ZONE_AHEAD"
        else:
            msg = "前方光线会变亮，可能有车辆或路灯，请注意周围环境变化。"
            code = "NAV_STRAT_BRIGHT_ZONE_AHEAD"
        
        return StrategyResult(
            active=True,
            severity="info",
            message=msg,
            code=code,
            extra={
                "dark_ratio": dark_ratio,
                "bright_ratio": bright_ratio,
                "dark_threshold": self.dark_threshold,
                "bright_threshold": self.bright_threshold,
                "jump_ratio_threshold": self.jump_ratio_threshold,
            },
        )



