"""
Texture Analyzer (v1.3.0)

纹理分析器

用于检测危险纹理：台阶、水坑、光滑地面、复杂区域等
"""

import cv2
import numpy as np
import logging

try:
    from skimage.feature import local_binary_pattern
    SKIMAGE_AVAILABLE = True
except ImportError:
    SKIMAGE_AVAILABLE = False
    logging.warning("skimage 未安装，将使用简化版 LBP 实现")

from .config import LBP_POINTS, LBP_RADIUS

logger = logging.getLogger(__name__)


def _simple_lbp(gray: np.ndarray, points: int = 8, radius: int = 1) -> np.ndarray:
    """
    简化版 LBP（如果 skimage 不可用）

    Args:
        gray: 灰度图像
        points: 采样点数
        radius: 采样半径

    Returns:
        np.ndarray: LBP 特征图
    """
    h, w = gray.shape
    lbp = np.zeros_like(gray)

    for i in range(radius, h - radius):
        for j in range(radius, w - radius):
            center = gray[i, j]
            pattern = 0
            for k in range(points):
                angle = 2 * np.pi * k / points
                y = int(i + radius * np.sin(angle))
                x = int(j + radius * np.cos(angle))
                if gray[y, x] >= center:
                    pattern |= (1 << k)
            lbp[i, j] = pattern

    return lbp


class TextureAnalyzer:
    """
    纹理分析器

    使用 LBP（Local Binary Pattern）分析纹理特征
    """

    def analyze(self, gray_tile: np.ndarray):
        """
        分析纹理并计算纹理跳跃值

        Args:
            gray_tile: 灰度图像 tile

        Returns:
            float: 纹理跳跃值（标准差），值越大表示纹理越复杂
        """
        if gray_tile is None or gray_tile.size == 0:
            return 0.0

        try:
            # 计算 LBP
            if SKIMAGE_AVAILABLE:
                lbp = local_binary_pattern(
                    gray_tile,
                    P=LBP_POINTS,
                    R=LBP_RADIUS,
                    method='uniform'
                )
            else:
                lbp = _simple_lbp(gray_tile, points=LBP_POINTS, radius=LBP_RADIUS)

            # 计算纹理跳跃（标准差）
            texture_jump = float(np.std(lbp))

            # 也可以计算纹理对比度（相邻像素差异）
            grad_x = cv2.Sobel(gray_tile, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray_tile, cv2.CV_64F, 0, 1, ksize=3)
            texture_contrast = float(np.mean(np.sqrt(grad_x**2 + grad_y**2)))

            # 综合纹理复杂度
            texture_complexity = texture_jump + texture_contrast * 0.1

            return texture_complexity

        except Exception as e:
            logger.warning(f"纹理分析失败: {e}")
            return 0.0













