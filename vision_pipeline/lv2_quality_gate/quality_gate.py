# -*- coding: utf-8 -*-
"""
LV2: Quality Gate（质量过滤层）

职责：
- 用最小算力，筛掉不值得浪费后端资源的帧
- 纯物理质量评估，不涉及任何语义

本模块禁止做什么：
- ❌ 禁止做任何语义理解
- ❌ 禁止调用下游模块
- ❌ 禁止修改输入帧
- ❌ 禁止触发重拍请求
"""

import time
import numpy as np
from dataclasses import dataclass
from typing import Optional
import cv2


@dataclass
class QualityResult:
    """
    质量评估结果
    
    字段说明：
    - frame_id: 帧 ID（可选）
    - quality_score: 质量分数 [0.0 ~ 1.0]
    - passed: 是否通过质量检查
    - reason: 未通过的原因（可选）
    """
    frame_id: Optional[str] = None
    quality_score: float = 0.0
    passed: bool = False  # 注意：pass 是关键字，改用 passed
    reason: Optional[str] = None


class QualityGate:
    """
    质量过滤层
    
    核心运算逻辑（纯物理质量评估，不涉及任何语义）：
    1. 清晰度评估（模糊度、高频信息比例）
    2. 稳定性评估（连续帧特征点位移）
    3. 曝光评估（亮度直方图）
    4. 冗余评估（帧间相似度）
    
    调度规则：
    - 同步执行
    - 极低延迟（毫秒级）
    - 可并行
    - 不得触发重拍
    """
    
    def __init__(
        self,
        min_quality_score: float = 0.3,  # 最低质量分数阈值
        enable_blur_check: bool = True,
        enable_exposure_check: bool = True,
        enable_redundancy_check: bool = False,  # 初期关闭，避免复杂度
    ):
        """
        初始化质量过滤层
        
        Args:
            min_quality_score: 最低质量分数阈值（默认 0.3）
            enable_blur_check: 是否启用模糊度检查（默认 True）
            enable_exposure_check: 是否启用曝光检查（默认 True）
            enable_redundancy_check: 是否启用冗余检查（默认 False，初期关闭）
        """
        self.min_quality_score = min_quality_score
        self.enable_blur_check = enable_blur_check
        self.enable_exposure_check = enable_exposure_check
        self.enable_redundancy_check = enable_redundancy_check
        
        # 用于冗余检查的上一帧（可选）
        self._last_frame: Optional[np.ndarray] = None
        self._last_frame_hash: Optional[int] = None
    
    def evaluate(
        self,
        frame: np.ndarray,
        frame_id: Optional[str] = None,
        timestamp: Optional[float] = None,
    ) -> QualityResult:
        """
        评估帧质量
        
        Args:
            frame: 输入图像帧（numpy array）
            frame_id: 帧 ID（可选）
            timestamp: 时间戳（可选）
        
        Returns:
            QualityResult: 质量评估结果
        """
        if frame is None or frame.size == 0:
            return QualityResult(
                frame_id=frame_id,
                quality_score=0.0,
                passed=False,
                reason="empty_frame",
            )
        
        # 初始化质量分数
        quality_score = 1.0
        reasons = []
        
        # 1. 清晰度评估（模糊度）
        if self.enable_blur_check:
            blur_score = self._evaluate_blur(frame)
            if blur_score < 0.5:
                quality_score *= blur_score
                reasons.append(f"blur_score={blur_score:.2f}")
        
        # 2. 曝光评估（亮度直方图）
        if self.enable_exposure_check:
            exposure_score = self._evaluate_exposure(frame)
            if exposure_score < 0.5:
                quality_score *= exposure_score
                reasons.append(f"exposure_score={exposure_score:.2f}")
        
        # 3. 冗余评估（帧间相似度，初期关闭）
        if self.enable_redundancy_check:
            redundancy_score = self._evaluate_redundancy(frame)
            if redundancy_score < 0.3:  # 高度相似
                quality_score *= 0.5  # 降权
                reasons.append(f"redundancy_score={redundancy_score:.2f}")
        
        # 判断是否通过
        passed = quality_score >= self.min_quality_score
        
        return QualityResult(
            frame_id=frame_id,
            quality_score=quality_score,
            passed=passed,
            reason="; ".join(reasons) if reasons and not passed else None,
        )
    
    def _evaluate_blur(self, frame: np.ndarray) -> float:
        """
        评估模糊度（Laplacian variance）
        
        Args:
            frame: 输入图像帧
        
        Returns:
            float: 清晰度分数 [0.0 ~ 1.0]
        """
        try:
            # 转换为灰度图
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                gray = frame
            
            # 计算 Laplacian 方差
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # 归一化到 [0, 1]（经验值：> 100 为清晰，< 50 为模糊）
            # 使用 sigmoid 函数平滑映射
            normalized = 1.0 / (1.0 + np.exp(-(laplacian_var - 100) / 20))
            
            return min(1.0, max(0.0, normalized))
        except Exception:
            # 评估失败，返回中等分数（不阻塞）
            return 0.5
    
    def _evaluate_exposure(self, frame: np.ndarray) -> float:
        """
        评估曝光（亮度直方图）
        
        Args:
            frame: 输入图像帧
        
        Returns:
            float: 曝光分数 [0.0 ~ 1.0]
        """
        try:
            # 转换为灰度图
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                gray = frame
            
            # 计算平均亮度
            mean_brightness = np.mean(gray)
            
            # 理想亮度范围：100 ~ 200（0-255 范围）
            # 使用高斯函数评估
            ideal = 150
            std = 50
            score = np.exp(-((mean_brightness - ideal) ** 2) / (2 * std ** 2))
            
            return min(1.0, max(0.0, score))
        except Exception:
            # 评估失败，返回中等分数（不阻塞）
            return 0.5
    
    def _evaluate_redundancy(self, frame: np.ndarray) -> float:
        """
        评估冗余度（帧间相似度）
        
        Args:
            frame: 输入图像帧
        
        Returns:
            float: 相似度分数 [0.0 ~ 1.0]（1.0 表示完全相同）
        """
        if self._last_frame is None:
            self._last_frame = frame.copy()
            return 0.0  # 第一帧，无冗余
        
        try:
            # 计算帧哈希（简化版：使用平均像素值）
            current_hash = int(np.mean(frame))
            last_hash = self._last_frame_hash or int(np.mean(self._last_frame))
            
            # 计算相似度（基于哈希差异）
            diff = abs(current_hash - last_hash)
            similarity = 1.0 - min(1.0, diff / 255.0)
            
            # 更新缓存
            self._last_frame = frame.copy()
            self._last_frame_hash = current_hash
            
            return similarity
        except Exception:
            # 评估失败，返回低相似度（不阻塞）
            return 0.0

