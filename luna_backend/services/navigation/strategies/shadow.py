"""
影子/光差策略 (Shadow Strategy) v1.2.0
检测大块深色区域 + 明暗边界；提醒地面凹凸、坑洼可能性，建议减速
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


class ShadowStrategy(NavigationStrategy):
    """
    影子 / 光差策略：
    - 检测大面积阴影和强烈明暗边界
    - 提醒可能存在地面起伏/坑洼
    """
    
    name = "shadow"
    
    def __init__(
        self,
        dark_threshold: int = 50,
        shadow_area_ratio_threshold: float = 0.15,
        gradient_threshold: float = 25.0,
    ) -> None:
        self.dark_threshold = dark_threshold
        self.shadow_area_ratio_threshold = shadow_area_ratio_threshold
        self.gradient_threshold = gradient_threshold
    
    def analyze(self, ctx: FrameContext) -> Optional[StrategyResult]:
        image = ctx.image_np
        if image is None:
            return None
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception:
            return None
        
        h, w = gray.shape[:2]
        
        # 1) 阴影区域：低亮度占比
        _, dark_mask = cv2.threshold(
            gray, self.dark_threshold, 255, cv2.THRESH_BINARY_INV
        )
        dark_area = float(dark_mask.sum() / 255.0)
        dark_ratio = dark_area / max(h * w, 1)
        
        if dark_ratio < self.shadow_area_ratio_threshold:
            # 阴影不够多，不触发
            return None
        
        # 2) 明暗边界（梯度）
        grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        mag = cv2.magnitude(grad_x, grad_y)
        mean_grad = float(mag.mean())
        
        if mean_grad < self.gradient_threshold:
            # 阴影多但边界不强，可能只是整体偏暗
            return None
        
        msg = "前方地面明暗变化较大，可能有台阶、坑洼或斜坡，请放慢速度，注意脚下。"
        
        return StrategyResult(
            active=True,
            severity="warning",
            message=msg,
            code="NAV_STRAT_SHADOW_RISK",
            extra={
                "dark_ratio": dark_ratio,
                "mean_gradient": mean_grad,
                "dark_threshold": self.dark_threshold,
                "shadow_area_ratio_threshold": self.shadow_area_ratio_threshold,
            },
        )



