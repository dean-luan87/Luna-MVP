"""
Scene Complexity Estimator (v1.3.0)

环境复杂度评估模块（C 模块）

功能：
- 对每一帧图像评估其"复杂程度"，输出 0~1 的浮点数
  - 0 表示非常简单（空旷、静止）
  - 1 表示非常复杂（结构多、运动多）

评估依据：
- 边缘密度（结构复杂度）
- 帧间差异（动态复杂度）
- 灰度方差（整体纹理/对比度）

设计特点：
- 不依赖 YOLO 结果，只看画面本身（轻量级）
- 可在 YOLO 之前先判断是否需要提高处理频率
- 使用下采样和灰度处理，计算开销小
"""

from typing import Optional

import cv2
import numpy as np


class SceneComplexityEstimator:
    """
    环境复杂度评估模块（C 模块）

    功能：
    - 对每一帧图像评估其"复杂程度"，输出 0~1 的浮点数
      - 0 表示非常简单（空旷、静止）
      - 1 表示非常复杂（结构多、运动多）

    评估依据：
    - 边缘密度（结构复杂度）
    - 帧间差异（动态复杂度）
    - 灰度方差（整体纹理/对比度）
    """

    def __init__(
        self,
        resize_width: int = 80,
        resize_height: int = 60,
        canny_threshold1: int = 50,
        canny_threshold2: int = 150,
        weight_edges: float = 0.4,
        weight_motion: float = 0.4,
        weight_contrast: float = 0.2,
        smoothing_alpha: float = 0.5,
    ):
        """
        初始化环境复杂度评估器

        Args:
            resize_width: 下采样宽度（默认 80）
            resize_height: 下采样高度（默认 60）
            canny_threshold1: Canny 边缘检测低阈值（默认 50）
            canny_threshold2: Canny 边缘检测高阈值（默认 150）
            weight_edges: 边缘密度权重（默认 0.4）
            weight_motion: 运动复杂度权重（默认 0.4）
            weight_contrast: 对比度权重（默认 0.2）
            smoothing_alpha: 时间平滑系数（默认 0.5，越大越敏感）
        """
        self.resize_width = resize_width
        self.resize_height = resize_height
        self.canny_threshold1 = canny_threshold1
        self.canny_threshold2 = canny_threshold2

        # 各项权重
        self.weight_edges = weight_edges
        self.weight_motion = weight_motion
        self.weight_contrast = weight_contrast

        # 平滑系数
        self.smoothing_alpha = smoothing_alpha

        # 内部状态
        self._prev_gray_small: Optional[np.ndarray] = None
        self._last_complexity: float = 0.0

    # ------------------------------------------------------------------ #
    # 对外主接口
    # ------------------------------------------------------------------ #

    def evaluate(self, frame) -> float:
        """
        输入一帧 BGR 图像，返回复杂度分数 [0,1]

        Args:
            frame: 输入图像帧（BGR 格式，numpy array）

        Returns:
            float: 复杂度分数，范围 [0, 1]
                - ~0.1 → 很简单（空路、没什么变化）
                - ~0.5 → 中等（有些人/车/纹理）
                - ~0.8 → 很复杂（人车密集 / 大量运动）
        """
        # 1. 转灰度 + 下采样
        gray_small = self._preprocess(frame)

        # 2. 边缘密度
        edge_density = self._compute_edge_density(gray_small)

        # 3. 帧间差异（运动量）
        motion_score = self._compute_motion_score(gray_small)

        # 4. 对比度/纹理强度
        contrast_score = self._compute_contrast_score(gray_small)

        # 5. 线性加权得到原始复杂度
        raw = (
            self.weight_edges * edge_density
            + self.weight_motion * motion_score
            + self.weight_contrast * contrast_score
        )

        # 6. 限制到 [0,1]
        raw = self._clamp(raw, 0.0, 1.0)

        # 7. 时间平滑
        complexity = (
            self.smoothing_alpha * raw
            + (1.0 - self.smoothing_alpha) * self._last_complexity
        )

        complexity = self._clamp(complexity, 0.0, 1.0)

        # 更新内部状态
        self._last_complexity = complexity
        self._prev_gray_small = gray_small

        return float(complexity)

    # ------------------------------------------------------------------ #
    # 子步骤：预处理
    # ------------------------------------------------------------------ #

    def _preprocess(self, frame) -> np.ndarray:
        """
        转灰度 + resize 到较小尺寸

        Args:
            frame: 输入 BGR 图像

        Returns:
            np.ndarray: 下采样后的灰度图像
        """
        # 防御性检查
        if frame is None or frame.size == 0:
            raise ValueError("输入帧为空")
        
        # 如果已经是灰度图，直接使用
        if len(frame.shape) == 2:
            gray = frame
        elif len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            raise ValueError(f"不支持的图像格式: shape={frame.shape}")
        
        small = cv2.resize(gray, (self.resize_width, self.resize_height))
        return small

    # ------------------------------------------------------------------ #
    # 子步骤：边缘密度
    # ------------------------------------------------------------------ #

    def _compute_edge_density(self, gray_small: np.ndarray) -> float:
        """
        计算边缘密度（结构复杂度）

        Args:
            gray_small: 下采样后的灰度图像

        Returns:
            float: 边缘密度分数 [0, 1]
        """
        edges = cv2.Canny(
            gray_small,
            self.canny_threshold1,
            self.canny_threshold2,
        )
        edge_pixels = np.count_nonzero(edges)
        total_pixels = edges.size

        if total_pixels == 0:
            return 0.0

        density = edge_pixels / float(total_pixels)

        # 一般密度不会超过 0.3 左右，这里简单乘一个系数再 clamp
        normalized = density * 2.0  # 放大一点，便于参与 0~1 组合
        return self._clamp(normalized, 0.0, 1.0)

    # ------------------------------------------------------------------ #
    # 子步骤：帧间差异（运动复杂度）
    # ------------------------------------------------------------------ #

    def _compute_motion_score(self, gray_small: np.ndarray) -> float:
        """
        计算帧间差异（动态复杂度）

        Args:
            gray_small: 当前帧下采样后的灰度图像

        Returns:
            float: 运动分数 [0, 1]，0 表示无变化，1 表示变化很大
        """
        if self._prev_gray_small is None:
            return 0.0

        # 计算绝对差
        diff = cv2.absdiff(gray_small, self._prev_gray_small)
        mean_diff = float(np.mean(diff))  # 0~255

        # 映射到 0~1
        score = mean_diff / 255.0
        return self._clamp(score, 0.0, 1.0)

    # ------------------------------------------------------------------ #
    # 子步骤：对比度 / 纹理强度
    # ------------------------------------------------------------------ #

    def _compute_contrast_score(self, gray_small: np.ndarray) -> float:
        """
        计算对比度/纹理强度

        Args:
            gray_small: 下采样后的灰度图像

        Returns:
            float: 对比度分数 [0, 1]
        """
        var = float(np.var(gray_small))  # 理论范围大约 0~(255^2)
        normalized = var / (255.0 * 255.0)
        return self._clamp(normalized, 0.0, 1.0)

    # ------------------------------------------------------------------ #
    # 工具函数
    # ------------------------------------------------------------------ #

    @staticmethod
    def _clamp(value: float, vmin: float, vmax: float) -> float:
        """
        将值限制在指定范围内

        Args:
            value: 输入值
            vmin: 最小值
            vmax: 最大值

        Returns:
            float: 限制后的值
        """
        return max(vmin, min(vmax, value))
