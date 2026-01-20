"""
Shape Analyzer (v1.3.0)

形状分析器

用于检测异常占位物体：杂物、箱子、低矮障碍等
"""

import cv2
import numpy as np
import logging

from .config import MIN_CONTOUR_AREA

logger = logging.getLogger(__name__)


class ShapeAnalyzer:
    """
    形状分析器

    分析边缘轮廓的形状特征，识别异常物体
    """

    def analyze(self, edge_map: np.ndarray):
        """
        分析形状异常度

        Args:
            edge_map: 边缘二值图

        Returns:
            float: 形状异常度（0-1），值越大表示形状越异常
        """
        if edge_map is None or edge_map.size == 0:
            return 0.0

        try:
            # 查找轮廓
            contours, _ = cv2.findContours(
                edge_map,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            if not contours:
                return 0.0

            # 找到最大轮廓
            max_cnt = max(contours, key=cv2.contourArea)

            # 计算面积和周长
            area = cv2.contourArea(max_cnt)
            perimeter = cv2.arcLength(max_cnt, True)

            if perimeter == 0 or area < MIN_CONTOUR_AREA:
                return 0.0

            # 计算圆度（circularity）
            # 圆度 = 4π*面积 / 周长²
            # 完美圆 = 1.0，越不规则越接近 0
            circularity = (4 * np.pi * area) / (perimeter ** 2)

            # 形状异常度 = 1 - 圆度
            abnormality = 1.0 - circularity

            # 限制在 [0, 1] 范围内
            abnormality = max(0.0, min(1.0, abnormality))

            # 也可以考虑长宽比
            rect = cv2.minAreaRect(max_cnt)
            width, height = rect[1]
            if width > 0 and height > 0:
                aspect_ratio = max(width, height) / min(width, height)
                # 长宽比过大或过小都表示异常
                aspect_abnormality = min(abs(aspect_ratio - 1.0) / 5.0, 1.0)
                abnormality = max(abnormality, aspect_abnormality * 0.5)

            return abnormality

        except Exception as e:
            logger.warning(f"形状分析失败: {e}")
            return 0.0

    def analyze_all_contours(self, edge_map: np.ndarray):
        """
        分析所有轮廓的综合异常度

        Args:
            edge_map: 边缘二值图

        Returns:
            float: 综合形状异常度
        """
        if edge_map is None or edge_map.size == 0:
            return 0.0

        try:
            contours, _ = cv2.findContours(
                edge_map,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            if not contours:
                return 0.0

            # 过滤小轮廓
            large_contours = [c for c in contours if cv2.contourArea(c) >= MIN_CONTOUR_AREA]

            if not large_contours:
                return 0.0

            # 计算所有轮廓的平均异常度
            abnormalities = []
            for cnt in large_contours:
                area = cv2.contourArea(cnt)
                perimeter = cv2.arcLength(cnt, True)
                if perimeter > 0:
                    circularity = (4 * np.pi * area) / (perimeter ** 2)
                    abnormality = 1.0 - circularity
                    abnormalities.append(max(0.0, min(1.0, abnormality)))

            if abnormalities:
                return float(np.mean(abnormalities))

            return 0.0

        except Exception as e:
            logger.warning(f"形状分析失败: {e}")
            return 0.0
























