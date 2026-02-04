"""
Ground Model (v1.3.0)

地面模型

从底部区域提取地面颜色和纹理特征，用于识别可走路径
"""

import cv2
import numpy as np
import logging

SKLEARN_AVAILABLE = False
try:
    from sklearn.cluster import MiniBatchKMeans
    SKLEARN_AVAILABLE = True
except (ImportError, ValueError, OSError):
    SKLEARN_AVAILABLE = False
    # 不在这里 warning，在需要时再 warning

from .config import (
    KMEANS_N_CLUSTERS,
    KMEANS_BATCH_SIZE,
    BOTTOM_RATIO,
    LBP_HIST_BINS,
)

logger = logging.getLogger(__name__)


def _simple_kmeans(data, n_clusters=2, max_iter=10):
    """
    简化版 KMeans（如果 sklearn 不可用）

    Args:
        data: 输入数据 (N, 3)
        n_clusters: 聚类数量
        max_iter: 最大迭代次数

    Returns:
        cluster_centers: 聚类中心 (n_clusters, 3)
    """
    # 随机初始化聚类中心
    n_samples, n_features = data.shape
    centers = data[np.random.choice(n_samples, n_clusters, replace=False)].copy()

    for _ in range(max_iter):
        # 计算每个点到聚类中心的距离
        distances = np.sqrt(((data[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2))
        labels = np.argmin(distances, axis=1)

        # 更新聚类中心
        new_centers = np.array([data[labels == k].mean(axis=0) for k in range(n_clusters)])
        
        # 检查收敛
        if np.allclose(centers, new_centers):
            break
        centers = new_centers

    return centers


class GroundModel:
    """
    地面模型

    从底部区域提取地面颜色和纹理特征，用于识别可走路径
    """

    def __init__(self):
        """
        初始化地面模型
        """
        self.color_centers = None      # 颜色聚类中心
        self.texture_lbphist = None    # 纹理 LBP 直方图

    def build_from_frame(self, frame: np.ndarray):
        """
        从画面底部建立地面模型

        Args:
            frame: 输入图像（BGR 格式）
        """
        if frame is None or frame.size == 0:
            logger.warning("输入图像为空，无法建立地面模型")
            return

        h, w = frame.shape[:2]
        
        # 提取底部区域（底部 25%）
        bottom_start = int(h * (1 - BOTTOM_RATIO))
        bottom = frame[bottom_start:, :]

        if bottom.size == 0:
            logger.warning("底部区域为空")
            return

        try:
            # Step 1: Color cluster
            data = bottom.reshape(-1, 3).astype(np.float32)
            
            if SKLEARN_AVAILABLE:
                try:
                    km = MiniBatchKMeans(
                        n_clusters=KMEANS_N_CLUSTERS,
                        batch_size=min(KMEANS_BATCH_SIZE, len(data)),
                        random_state=42,
                        n_init=3
                    )
                    km.fit(data)
                    self.color_centers = km.cluster_centers_
                except Exception as e:
                    logger.warning(f"sklearn KMeans 失败，使用简化版: {e}")
                    self.color_centers = _simple_kmeans(data, n_clusters=KMEANS_N_CLUSTERS)
            else:
                # 使用简化版 KMeans
                logger.debug("使用简化版 KMeans（sklearn 不可用）")
                self.color_centers = _simple_kmeans(data, n_clusters=KMEANS_N_CLUSTERS)

            # Step 2: Texture model (LBP histogram)
            gray = cv2.cvtColor(bottom, cv2.COLOR_BGR2GRAY)
            lbp = self._lbp(gray)
            
            # 计算 LBP 直方图
            hist, _ = np.histogram(
                lbp.flatten(),
                bins=LBP_HIST_BINS,
                range=(0, 256),
                density=True
            )
            self.texture_lbphist = hist

            logger.debug("地面模型建立成功")

        except Exception as e:
            logger.warning(f"建立地面模型失败: {e}")

    def _lbp(self, gray: np.ndarray) -> np.ndarray:
        """
        计算 Local Binary Pattern (LBP)

        Args:
            gray: 灰度图像

        Returns:
            np.ndarray: LBP 特征图
        """
        h, w = gray.shape
        lbp = np.zeros_like(gray)

        for y in range(1, h - 1):
            for x in range(1, w - 1):
                center = gray[y, x]
                code = 0
                # 8 邻域
                code |= (gray[y - 1, x - 1] > center) << 7
                code |= (gray[y - 1, x] > center) << 6
                code |= (gray[y - 1, x + 1] > center) << 5
                code |= (gray[y, x + 1] > center) << 4
                code |= (gray[y + 1, x + 1] > center) << 3
                code |= (gray[y + 1, x] > center) << 2
                code |= (gray[y + 1, x - 1] > center) << 1
                code |= (gray[y, x - 1] > center) << 0
                lbp[y, x] = code

        return lbp

    def color_similarity(self, tile: np.ndarray) -> float:
        """
        计算 tile 与地面颜色的相似度

        Args:
            tile: 图像 tile（BGR 格式）

        Returns:
            float: 颜色相似度（0-1），越大越相似
        """
        if self.color_centers is None:
            return 0.5  # 默认值

        try:
            # 计算 tile 的平均颜色
            avg_color = tile.reshape(-1, 3).mean(axis=0)

            # 计算与所有聚类中心的距离
            dists = np.linalg.norm(self.color_centers - avg_color, axis=1)

            # 转换为相似度（距离越小，相似度越大）
            min_dist = np.min(dists)
            sim = 1.0 / (1.0 + min_dist / 255.0)  # 归一化到 0-1

            return float(sim)

        except Exception as e:
            logger.warning(f"颜色相似度计算失败: {e}")
            return 0.5

    def texture_similarity(self, tile_gray: np.ndarray) -> float:
        """
        计算 tile 与地面纹理的相似度

        Args:
            tile_gray: 灰度图像 tile

        Returns:
            float: 纹理相似度（0-1），越大越相似
        """
        if self.texture_lbphist is None:
            return 0.5  # 默认值

        try:
            # 计算 tile 的 LBP
            lbp = self._lbp(tile_gray)

            # 计算 LBP 直方图
            hist, _ = np.histogram(
                lbp.flatten(),
                bins=LBP_HIST_BINS,
                range=(0, 256),
                density=True
            )

            # 计算直方图差异
            diff = np.sum(np.abs(hist - self.texture_lbphist))

            # 转换为相似度（差异越小，相似度越大）
            sim = 1.0 / (1.0 + diff * 10.0)  # 缩放因子可调

            return float(sim)

        except Exception as e:
            logger.warning(f"纹理相似度计算失败: {e}")
            return 0.5

