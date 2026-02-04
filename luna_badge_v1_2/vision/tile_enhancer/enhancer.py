"""
Tile Enhancer (v1.3.0)

局部关键区增强器

对摄像头画面进行网格划分，对每个 tile 进行智能增强
- 低光 → Gamma 校正
- 低对比 → CLAHE
- 噪声 → Bilateral Filter

保持算法轻量级，支持未来扩展到任意 N×M 网格
"""

import cv2
import numpy as np
import logging

from .config import (
    TILE_ROWS,
    TILE_COLS,
    BRIGHTNESS_THRESHOLD,
    CONTRAST_THRESHOLD,
    NOISE_THRESHOLD,
    ENABLE_CLAHE,
    ENABLE_GAMMA,
    ENABLE_BILATERAL,
    GAMMA_VALUE,
    CLAHE_CLIP_LIMIT,
    CLAHE_TILE_GRID_SIZE,
    BILATERAL_D,
    BILATERAL_SIGMA_COLOR,
    BILATERAL_SIGMA_SPACE,
)

logger = logging.getLogger(__name__)


class TileEnhancer:
    """
    局部关键区增强器

    将画面切分为网格，对每个 tile 进行智能增强
    """

    def __init__(self, rows: int = None, cols: int = None):
        """
        初始化增强器

        Args:
            rows: 网格行数（如果为 None 则使用配置）
            cols: 网格列数（如果为 None 则使用配置）
        """
        self.tile_rows = rows if rows is not None else TILE_ROWS
        self.tile_cols = cols if cols is not None else TILE_COLS

        # 初始化 CLAHE（如果启用）
        if ENABLE_CLAHE:
            self.clahe = cv2.createCLAHE(
                clipLimit=CLAHE_CLIP_LIMIT,
                tileGridSize=CLAHE_TILE_GRID_SIZE
            )
        else:
            self.clahe = None

        logger.info(f"Tile Enhancer 初始化完成 ({self.tile_rows}×{self.tile_cols})")

    def split_tiles(self, frame: np.ndarray):
        """
        将画面切分为网格 tiles

        Args:
            frame: 输入图像（BGR 格式）

        Returns:
            tuple: (tiles 列表, coords 坐标列表)
                - tiles: List[np.ndarray]，每个 tile 的图像
                - coords: List[Tuple[int, int, int, int]]，每个 tile 的坐标 (y1, y2, x1, x2)
        """
        h, w = frame.shape[:2]
        tile_h = h // self.tile_rows
        tile_w = w // self.tile_cols

        tiles = []
        coords = []

        for i in range(self.tile_rows):
            for j in range(self.tile_cols):
                y1 = i * tile_h
                y2 = (i + 1) * tile_h if i < self.tile_rows - 1 else h
                x1 = j * tile_w
                x2 = (j + 1) * tile_w if j < self.tile_cols - 1 else w

                tile = frame[y1:y2, x1:x2]
                tiles.append(tile)
                coords.append((y1, y2, x1, x2))

        return tiles, coords

    def compute_stats(self, gray: np.ndarray):
        """
        计算 tile 的统计信息

        Args:
            gray: 灰度图像

        Returns:
            tuple: (brightness, contrast, noise)
                - brightness: 平均亮度
                - contrast: 对比度（标准差）
                - noise: 噪声水平
        """
        # 亮度：平均灰度值
        brightness = float(np.mean(gray))

        # 对比度：灰度标准差
        contrast = float(np.std(gray))

        # 噪声：与原图的差异（通过模糊后与原图对比）
        blurred = cv2.blur(gray, (3, 3))
        noise = float(np.mean(np.abs(gray.astype(np.float32) - blurred.astype(np.float32))))

        return brightness, contrast, noise

    def enhance_tile(self, tile: np.ndarray):
        """
        增强单个 tile

        Args:
            tile: 输入 tile 图像（BGR 格式）

        Returns:
            np.ndarray: 增强后的 tile 图像
        """
        # 转换为灰度用于统计
        gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
        brightness, contrast, noise = self.compute_stats(gray)

        # 复制原图
        enhanced = tile.copy()

        # 1. Gamma 校正（低光增强）
        if ENABLE_GAMMA and brightness < BRIGHTNESS_THRESHOLD:
            # Gamma 校正公式
            inv_gamma = 1.0 / GAMMA_VALUE
            table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
            enhanced = cv2.LUT(enhanced, table)

        # 2. CLAHE（低对比度增强）
        if ENABLE_CLAHE and contrast < CONTRAST_THRESHOLD and self.clahe is not None:
            # 转换为 LAB 颜色空间
            lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
            # 对 L 通道应用 CLAHE
            lab[:, :, 0] = self.clahe.apply(lab[:, :, 0])
            # 转换回 BGR
            enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        # 3. Bilateral Filter（去噪）
        if ENABLE_BILATERAL and noise > NOISE_THRESHOLD:
            enhanced = cv2.bilateralFilter(
                enhanced,
                d=BILATERAL_D,
                sigmaColor=BILATERAL_SIGMA_COLOR,
                sigmaSpace=BILATERAL_SIGMA_SPACE
            )

        return enhanced

    def process(self, frame: np.ndarray) -> np.ndarray:
        """
        处理整帧图像

        Args:
            frame: 输入图像（BGR 格式）

        Returns:
            np.ndarray: 增强后的图像
        """
        if frame is None or frame.size == 0:
            logger.warning("输入图像为空")
            return frame

        # 切分 tiles
        tiles, coords = self.split_tiles(frame)

        # 创建输出图像（复制原图）
        output = frame.copy()

        # 对每个 tile 进行增强
        for tile, (y1, y2, x1, x2) in zip(tiles, coords):
            try:
                enhanced_tile = self.enhance_tile(tile)
                # 将增强后的 tile 放回原位置
                output[y1:y2, x1:x2] = enhanced_tile
            except Exception as e:
                logger.warning(f"增强 tile ({y1},{y2},{x1},{x2}) 失败: {e}，使用原图")
                # 如果增强失败，保持原图

        return output

    def process_with_stats(self, frame: np.ndarray):
        """
        处理整帧图像并返回统计信息

        Args:
            frame: 输入图像

        Returns:
            tuple: (enhanced_frame, stats)
                - enhanced_frame: 增强后的图像
                - stats: 统计信息字典
        """
        tiles, coords = self.split_tiles(frame)
        output = frame.copy()

        stats = {
            "total_tiles": len(tiles),
            "enhanced_tiles": 0,
            "gamma_applied": 0,
            "clahe_applied": 0,
            "bilateral_applied": 0,
        }

        for tile, (y1, y2, x1, x2) in zip(tiles, coords):
            gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
            brightness, contrast, noise = self.compute_stats(gray)

            enhanced_tile = tile.copy()
            enhanced = False

            # 应用增强并统计
            if ENABLE_GAMMA and brightness < BRIGHTNESS_THRESHOLD:
                inv_gamma = 1.0 / GAMMA_VALUE
                table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
                enhanced_tile = cv2.LUT(enhanced_tile, table)
                stats["gamma_applied"] += 1
                enhanced = True

            if ENABLE_CLAHE and contrast < CONTRAST_THRESHOLD and self.clahe is not None:
                lab = cv2.cvtColor(enhanced_tile, cv2.COLOR_BGR2LAB)
                lab[:, :, 0] = self.clahe.apply(lab[:, :, 0])
                enhanced_tile = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
                stats["clahe_applied"] += 1
                enhanced = True

            if ENABLE_BILATERAL and noise > NOISE_THRESHOLD:
                enhanced_tile = cv2.bilateralFilter(
                    enhanced_tile,
                    d=BILATERAL_D,
                    sigmaColor=BILATERAL_SIGMA_COLOR,
                    sigmaSpace=BILATERAL_SIGMA_SPACE
                )
                stats["bilateral_applied"] += 1
                enhanced = True

            if enhanced:
                stats["enhanced_tiles"] += 1

            output[y1:y2, x1:x2] = enhanced_tile

        return output, stats
























