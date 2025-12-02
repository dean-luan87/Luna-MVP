"""
Edge Detector (v1.3.0)

边缘检测器

用于检测危险边缘：桌边、墙角、悬空边缘、台阶前沿等
"""

import cv2
import numpy as np
import logging

from .config import EDGE_MAG_THRESHOLD, SOBEL_KSIZE

logger = logging.getLogger(__name__)


class EdgeDetector:
    """
    边缘检测器

    使用 Sobel 和 Canny 检测边缘，计算边缘密度
    """

    def detect(self, gray_tile: np.ndarray):
        """
        检测边缘并计算边缘密度

        Args:
            gray_tile: 灰度图像 tile

        Returns:
            tuple: (edge_density, edge_map)
                - edge_density: float, 边缘密度（0-1）
                - edge_map: np.ndarray, 边缘二值图
        """
        if gray_tile is None or gray_tile.size == 0:
            return 0.0, np.zeros((10, 10), dtype=np.uint8)

        try:
            # Sobel 边缘检测
            sobelx = cv2.Sobel(gray_tile, cv2.CV_64F, 1, 0, ksize=SOBEL_KSIZE)
            sobely = cv2.Sobel(gray_tile, cv2.CV_64F, 0, 1, ksize=SOBEL_KSIZE)

            # 计算边缘幅值
            mag = np.sqrt(sobelx**2 + sobely**2)

            # 二值化边缘图
            edge_map = (mag > EDGE_MAG_THRESHOLD).astype(np.uint8)

            # 计算边缘密度
            density = float(np.sum(edge_map)) / edge_map.size if edge_map.size > 0 else 0.0

            # 也可使用 Canny 作为补充
            canny = cv2.Canny(gray_tile, 50, 150)
            canny_density = float(np.sum(canny > 0)) / canny.size if canny.size > 0 else 0.0

            # 合并两种边缘检测结果
            combined_density = max(density, canny_density * 0.5)

            return combined_density, edge_map

        except Exception as e:
            logger.warning(f"边缘检测失败: {e}")
            return 0.0, np.zeros_like(gray_tile, dtype=np.uint8)









