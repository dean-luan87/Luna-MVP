"""
Luna Badge v1.3.0
ISP Enhancer - 图像增强模块

职责：
- 对输入图像做轻量级 ISP 处理：
  - 降噪
  - 暗光增强
  - 对比度提升
  - 轻微锐化

说明：
- 该模块不依赖具体硬件，仅对 numpy 图像做处理
- 默认假设输入为 OpenCV 风格的 BGR 图像
- 若后续硬件有更强 ISP，可在此处做开关，直接返回原图
"""

from typing import Any, Dict, Optional

import cv2
import numpy as np


class ISPEnhancer:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        config 可选字段示例：
        {
            "enable_denoise": True,
            "enable_contrast": True,
            "enable_sharpen": True,
            "dark_luma_threshold": 60,   # 判断暗光的阈值（0~255）
            "gamma_dark": 1.4,           # 暗光增强的 gamma
            "gamma_normal": 1.0
        }
        """
        default_config: Dict[str, Any] = {
            "enable_denoise": True,
            "enable_contrast": True,
            "enable_sharpen": True,
            "dark_luma_threshold": 60,
            "gamma_dark": 1.4,
            "gamma_normal": 1.0,
        }
        self.config = {**default_config, **(config or {})}

    def enhance(self, frame: Any) -> Any:
        """
        输入：frame - BGR 图像（numpy.ndarray）
        输出：增强后的图像（同尺寸、同通道数）

        注意：
        - 若输入不是合法图像，直接原样返回
        - 所有增强都尽量保持轻量，避免破坏后续检测
        """
        if frame is None or not isinstance(frame, np.ndarray):
            return frame

        enhanced = frame.copy()

        # 1. 计算亮度，决定是否做暗光增强
        avg_luma = self._compute_luma(enhanced)
        is_dark = avg_luma < self.config["dark_luma_threshold"]

        # 2. 降噪（轻度高斯模糊）
        if self.config["enable_denoise"]:
            enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)

        # 3. 亮度/对比度处理（使用 LAB + CLAHE）
        if self.config["enable_contrast"]:
            enhanced = self._apply_clahe(enhanced, is_dark)

        # 4. 轻微锐化（unsharp mask）
        if self.config["enable_sharpen"]:
            enhanced = self._sharpen(enhanced)

        return enhanced

    # ---------------- 内部工具函数 ---------------- #

    def _compute_luma(self, frame: np.ndarray) -> float:
        """
        计算图像平均亮度（0~255）
        """
        if frame.ndim == 2:
            gray = frame
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return float(gray.mean())

    def _apply_clahe(self, frame: np.ndarray, is_dark: bool) -> np.ndarray:
        """
        使用 LAB 颜色空间 + CLAHE 做局部对比度增强，
        暗光场景下效果更明显。
        """
        try:
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        except Exception:
            # 如果转换失败，则不做处理
            return frame

        l, a, b = cv2.split(lab)

        # 根据是否暗光调整 CLAHE 参数
        clip_limit = 3.0 if is_dark else 2.0
        tile_grid_size = (8, 8)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        l_clahe = clahe.apply(l)

        lab_clahe = cv2.merge((l_clahe, a, b))
        enhanced = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)

        # 额外的 gamma 校正（暗光时稍微提亮）
        gamma = self.config["gamma_dark"] if is_dark else self.config["gamma_normal"]
        if abs(gamma - 1.0) > 1e-3:
            enhanced = self._apply_gamma(enhanced, gamma)

        return enhanced

    def _apply_gamma(self, frame: np.ndarray, gamma: float) -> np.ndarray:
        """
        Gamma 校正：用于暗光提亮或微调对比度。
        """
        inv_gamma = 1.0 / max(gamma, 1e-6)
        table = np.array(
            [(i / 255.0) ** inv_gamma * 255 for i in range(256)]
        ).astype("uint8")
        return cv2.LUT(frame, table)

    def _sharpen(self, frame: np.ndarray) -> np.ndarray:
        """
        轻量锐化：提高边缘清晰度，辅助模型识别轮廓。
        使用 unsharp masking：
        sharpened = frame + alpha * (frame - blur(frame))
        """
        alpha = 0.6  # 锐化强度，不宜太大
        blurred = cv2.GaussianBlur(frame, (3, 3), 0)
        sharpened = cv2.addWeighted(frame, 1 + alpha, blurred, -alpha, 0)
        return sharpened
