"""
Risk Fusion (v1.3.0)

风险融合器

整合边缘检测、纹理分析、形状分析的结果，生成风险热力图
"""

import cv2
import numpy as np
import logging
from typing import Dict, Any, Tuple, List

from .config import (
    TILE_ROWS,
    TILE_COLS,
    W_EDGE,
    W_TEXTURE,
    W_SHAPE,
)
from .edge_detector import EdgeDetector
from .texture_analyzer import TextureAnalyzer
from .shape_analyzer import ShapeAnalyzer

logger = logging.getLogger(__name__)


class HazardDetector:
    """
    危险检测器

    综合边缘、纹理、形状分析，生成风险热力图
    """

    def __init__(self, rows: int = None, cols: int = None):
        """
        初始化危险检测器

        Args:
            rows: 网格行数（如果为 None 则使用配置）
            cols: 网格列数（如果为 None 则使用配置）
        """
        self.tile_rows = rows if rows is not None else TILE_ROWS
        self.tile_cols = cols if cols is not None else TILE_COLS

        self.ed = EdgeDetector()
        self.ta = TextureAnalyzer()
        self.sa = ShapeAnalyzer()

        logger.info(f"危险检测器初始化完成 ({self.tile_rows}×{self.tile_cols})")

    def compute_risk(self, frame: np.ndarray) -> np.ndarray:
        """
        计算风险热力图

        Args:
            frame: 输入图像（BGR 格式）

        Returns:
            np.ndarray: 风险矩阵（TILE_ROWS × TILE_COLS），值范围 [0, 1]
        """
        if frame is None or frame.size == 0:
            logger.warning("输入图像为空")
            return np.zeros((self.tile_rows, self.tile_cols), dtype=np.float32)

        h, w = frame.shape[:2]
        tile_h = h // self.tile_rows
        tile_w = w // self.tile_cols

        risk_map = np.zeros((self.tile_rows, self.tile_cols), dtype=np.float32)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 遍历每个 tile
        for i in range(self.tile_rows):
            for j in range(self.tile_cols):
                y1 = i * tile_h
                y2 = (i + 1) * tile_h if i < self.tile_rows - 1 else h
                x1 = j * tile_w
                x2 = (j + 1) * tile_w if j < self.tile_cols - 1 else w

                tile = gray[y1:y2, x1:x2]

                if tile.size == 0:
                    continue

                try:
                    # 1. 边缘检测
                    edge_density, edge_map = self.ed.detect(tile)

                    # 2. 纹理分析
                    texture_jump = self.ta.analyze(tile)
                    # 归一化到 [0, 1]（假设最大值为 100）
                    texture_normalized = min(texture_jump / 100.0, 1.0)

                    # 3. 形状分析
                    shape_abnormal = self.sa.analyze(edge_map)

                    # 4. 融合风险分数
                    risk = (
                        W_EDGE * edge_density +
                        W_TEXTURE * texture_normalized +
                        W_SHAPE * shape_abnormal
                    )

                    # 限制在 [0, 1] 范围内
                    risk_map[i, j] = max(0.0, min(1.0, risk))

                except Exception as e:
                    logger.warning(f"处理 tile ({i},{j}) 失败: {e}")
                    risk_map[i, j] = 0.0

        return risk_map

    def compute_risk_with_details(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        计算风险热力图并返回详细信息

        Args:
            frame: 输入图像

        Returns:
            Dict[str, Any]: 包含风险矩阵和详细信息的字典
        """
        if frame is None or frame.size == 0:
            return {
                "risk_map": np.zeros((self.tile_rows, self.tile_cols)),
                "details": {},
            }

        h, w = frame.shape[:2]
        tile_h = h // self.tile_rows
        tile_w = w // self.tile_cols

        risk_map = np.zeros((self.tile_rows, self.tile_cols), dtype=np.float32)
        details_map = {}

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        for i in range(self.tile_rows):
            for j in range(self.tile_cols):
                y1 = i * tile_h
                y2 = (i + 1) * tile_h if i < self.tile_rows - 1 else h
                x1 = j * tile_w
                x2 = (j + 1) * tile_w if j < self.tile_cols - 1 else w

                tile = gray[y1:y2, x1:x2]

                if tile.size == 0:
                    continue

                try:
                    # 各维度分析
                    edge_density, edge_map = self.ed.detect(tile)
                    texture_jump = self.ta.analyze(tile)
                    texture_normalized = min(texture_jump / 100.0, 1.0)
                    shape_abnormal = self.sa.analyze(edge_map)

                    # 融合风险
                    risk = (
                        W_EDGE * edge_density +
                        W_TEXTURE * texture_normalized +
                        W_SHAPE * shape_abnormal
                    )

                    risk_map[i, j] = max(0.0, min(1.0, risk))

                    # 保存详细信息
                    details_map[(i, j)] = {
                        "edge_density": float(edge_density),
                        "texture_jump": float(texture_jump),
                        "texture_normalized": float(texture_normalized),
                        "shape_abnormal": float(shape_abnormal),
                        "risk": float(risk_map[i, j]),
                    }

                except Exception as e:
                    logger.warning(f"处理 tile ({i},{j}) 失败: {e}")
                    risk_map[i, j] = 0.0

        return {
            "risk_map": risk_map,
            "details": details_map,
        }

    def get_risk_level(self, risk_score: float) -> str:
        """
        将风险分数转换为风险等级

        Args:
            risk_score: 风险分数（0-1）

        Returns:
            str: 风险等级（"low" / "medium" / "high"）
        """
        if risk_score < 0.3:
            return "low"
        elif risk_score < 0.6:
            return "medium"
        else:
            return "high"

    def get_safe_path_candidates(self, risk_map: np.ndarray, top_k: int = 3) -> List[int]:
        """
        根据风险热力图找出安全路径候选（列索引）

        Args:
            risk_map: 风险矩阵
            top_k: 返回前 k 个最安全的列

        Returns:
            List[int]: 安全路径候选列索引列表（按风险从低到高排序）
        """
        if risk_map.shape[0] == 0 or risk_map.shape[1] == 0:
            return []

        # 计算每列的平均风险
        column_risks = []
        for col in range(risk_map.shape[1]):
            col_risk = float(np.mean(risk_map[:, col]))
            column_risks.append((col, col_risk))

        # 按风险排序
        column_risks.sort(key=lambda x: x[1])

        # 返回前 k 个最安全的列
        return [col for col, _ in column_risks[:top_k]]

