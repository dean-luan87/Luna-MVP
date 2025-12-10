"""
Image Corrector (v1.3.0)

图像补正模块

提供轻量级图像增强能力：
- Retinex-Lite 暗部提亮
- 高光压缩（Highlight Compression）
- 轻量去噪（Fast Denoise）
- 轻量锐化（Anti-Blur Sharpen）
- AI 修复接口预留（1.4 版本）
"""

import cv2
import numpy as np
import logging

from .correct_config import (
    ENABLE_RETINEX,
    ENABLE_HIGHLIGHT_COMPRESSION,
    ENABLE_DENOISE,
    ENABLE_SHARPEN,
    ENABLE_AI_RESTORER,
    RETINEX_SIGMA,
    RETINEX_WEIGHT,
    HIGHLIGHT_THRESHOLD,
    HIGHLIGHT_COMPRESSION_STRENGTH,
    DENOISE_H,
    DENOISE_TEMPLATE_SIZE,
    DENOISE_SEARCH_SIZE,
    SHARPEN_STRENGTH,
    AI_MODEL_PATH,
    AI_MAX_RESOLUTION,
    DEBUG_CORRECTOR,
)

logger = logging.getLogger(__name__)


class AIImageRestorer:
    """
    AI 图像修复器（1.3.0 占坑实现，未来 1.4 可接入真实 AI 修复模型）

    当前版本：如果 enabled=False 或 model_path 为空，直接返回原图
    1.4 版本：可加载 onnx / tflite 等模型进行真实修复增强
    """

    def __init__(self, enabled: bool = False, model_path: str = ""):
        """
        初始化 AI 修复器

        Args:
            enabled: 是否启用 AI 修复
            model_path: 模型路径（1.4 版本使用）
        """
        self.enabled = enabled and bool(model_path)
        self.model_path = model_path
        self._model = None

        if self.enabled:
            logger.info(f"AI 修复器已启用，模型路径: {model_path}")
            # 1.4 版本在这里加载模型（onnx / tflite 等）
            # 当前版本不加载，避免影响性能
        else:
            logger.debug("AI 修复器未启用（1.3.0 占位模式）")

    def enhance(self, frame: np.ndarray) -> np.ndarray:
        """
        使用 AI 模型增强图像

        Args:
            frame: 输入图像（BGR 格式）

        Returns:
            np.ndarray: 增强后的图像

        1.4 版本实现示例：
        1. resize 到 AI_MAX_RESOLUTION 范围
        2. 转 tensor / onnx 输入
        3. 推理
        4. resize 回原尺寸
        """
        if not self.enabled:
            return frame

        # TODO: 1.4 版本实现真实调用
        # 方案示例：
        # 1. resize 到 AI_MAX_RESOLUTION 范围
        # 2. 转 tensor / onnx 输入
        # 3. 推理
        # 4. resize 回原尺寸

        # 当前版本直接返回原图
        return frame


class ImageCorrector:
    """
    图像补正器

    提供多种轻量级图像增强能力，提升视觉检测效果
    """

    def __init__(self):
        """
        初始化图像补正器
        """
        self.ai_restorer = AIImageRestorer(
            enabled=ENABLE_AI_RESTORER,
            model_path=AI_MODEL_PATH
        )
        logger.info("Image Corrector 初始化完成")

    # --------- 子步骤实现 ----------

    def _retinex_lite(self, frame: np.ndarray) -> np.ndarray:
        """
        Retinex-Lite 暗部提亮

        基于 SSR (Single Scale Retinex) 思路：log(I) - log(Gaussian(I))
        比简单 gamma 更自然，暗处提亮同时保留细节

        Args:
            frame: 输入图像（BGR 格式）

        Returns:
            np.ndarray: 增强后的图像
        """
        # 转换为浮点数并归一化
        img = frame.astype(np.float32) / 255.0

        # 转换为灰度用于计算 Retinex
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0

        # 高斯模糊（模拟光照）
        blur = cv2.GaussianBlur(gray, (0, 0), RETINEX_SIGMA)
        blur = np.clip(blur, 1e-4, 1.0)

        # Retinex 计算：log(I) - log(Gaussian(I))
        retinex = np.log(gray + 1e-4) - np.log(blur)

        # 归一化到 [0, 1]
        retinex -= retinex.min()
        if retinex.max() > 0:
            retinex /= retinex.max()

        # 扩展维度用于广播
        retinex = retinex[..., None]  # (H, W, 1)

        # 用 retinex 作为权重提升暗部
        # enhanced = img * (1 - weight) + img * retinex * weight
        enhanced = img * (1 - RETINEX_WEIGHT) + img * retinex * RETINEX_WEIGHT

        # 限制到 [0, 1] 并转回 uint8
        enhanced = np.clip(enhanced, 0, 1)
        return (enhanced * 255).astype(np.uint8)

    def _highlight_compress(self, frame: np.ndarray) -> np.ndarray:
        """
        高光压缩（Highlight Compression）

        对特别亮的区域做 tone mapping，避免地面、台阶被"白光糊掉"

        Args:
            frame: 输入图像（BGR 格式）

        Returns:
            np.ndarray: 压缩高光后的图像
        """
        # 转换到 HSV 颜色空间
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        v = hsv[:, :, 2].astype(np.float32)

        # 找到高光区域
        mask = v > HIGHLIGHT_THRESHOLD

        # 对高光部分做压缩：v_new = T + (v - T) * strength
        v[mask] = HIGHLIGHT_THRESHOLD + (v[mask] - HIGHLIGHT_THRESHOLD) * HIGHLIGHT_COMPRESSION_STRENGTH

        # 限制到 [0, 255] 并转换回 uint8
        v = np.clip(v, 0, 255).astype(np.uint8)
        hsv[:, :, 2] = v

        # 转换回 BGR
        out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return out

    def _fast_denoise(self, frame: np.ndarray) -> np.ndarray:
        """
        轻量去噪（Fast Denoise）

        使用 fastNlMeans 进行轻量去噪，避免过度模糊

        Args:
            frame: 输入图像（BGR 格式）

        Returns:
            np.ndarray: 去噪后的图像
        """
        # 使用 fastNlMeans 进行彩色图像去噪
        return cv2.fastNlMeansDenoisingColored(
            frame,
            None,
            h=DENOISE_H,
            hColor=DENOISE_H,
            templateWindowSize=DENOISE_TEMPLATE_SIZE,
            searchWindowSize=DENOISE_SEARCH_SIZE
        )

    def _sharpen(self, frame: np.ndarray) -> np.ndarray:
        """
        轻量锐化（Anti-Blur Sharpen）

        使用简单锐化核，让边缘更清晰，利于 F4 边缘检测 & YOLO

        Args:
            frame: 输入图像（BGR 格式）

        Returns:
            np.ndarray: 锐化后的图像
        """
        # 锐化核
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], dtype=np.float32)

        # 应用锐化核
        sharpened = cv2.filter2D(frame, -1, kernel)

        # 按强度混合原图和锐化结果
        out = cv2.addWeighted(
            frame,
            1 - SHARPEN_STRENGTH,
            sharpened,
            SHARPEN_STRENGTH,
            0
        )

        return out

    # --------- 总入口 ----------

    def process(self, frame: np.ndarray):
        """
        处理图像，应用所有启用的增强步骤

        Args:
            frame: 输入图像（BGR 格式）

        Returns:
            tuple: (enhanced_frame, meta_info)
                - enhanced_frame: 增强后的图像
                - meta_info: 元信息字典，记录哪些步骤被启用
        """
        meta = {
            "retinex_used": False,
            "highlight_compress_used": False,
            "denoise_used": False,
            "sharpen_used": False,
            "ai_restorer_used": False,
        }

        if frame is None or frame.size == 0:
            logger.warning("输入图像为空")
            return frame, meta

        out = frame.copy()

        # 1. Retinex-Lite 暗部提亮
        if ENABLE_RETINEX:
            try:
                out = self._retinex_lite(out)
                meta["retinex_used"] = True
            except Exception as e:
                logger.warning(f"Retinex-Lite 处理失败: {e}")

        # 2. 高光压缩
        if ENABLE_HIGHLIGHT_COMPRESSION:
            try:
                out = self._highlight_compress(out)
                meta["highlight_compress_used"] = True
            except Exception as e:
                logger.warning(f"高光压缩处理失败: {e}")

        # 3. 轻量去噪
        if ENABLE_DENOISE:
            try:
                out = self._fast_denoise(out)
                meta["denoise_used"] = True
            except Exception as e:
                logger.warning(f"去噪处理失败: {e}")

        # 4. 轻量锐化
        if ENABLE_SHARPEN:
            try:
                out = self._sharpen(out)
                meta["sharpen_used"] = True
            except Exception as e:
                logger.warning(f"锐化处理失败: {e}")

        # 5. 预留 AI 修复模型调用（1.4 使用）
        out_ai = self.ai_restorer.enhance(out)
        if out_ai is not out:
            meta["ai_restorer_used"] = True
            out = out_ai

        # 调试输出
        if DEBUG_CORRECTOR:
            enabled_steps = [k for k, v in meta.items() if v]
            logger.debug(f"[Corrector] 已启用步骤: {', '.join(enabled_steps)}")

        return out, meta













