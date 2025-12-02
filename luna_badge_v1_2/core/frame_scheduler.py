"""
Frame Scheduler (高级抽帧调度器，1.3.0 MVP)

职责：
- 综合亮度、密度、速度、旋转、环境记忆
- 计算最终 FPS，交给 FrameManager 使用

依赖（MVP阶段均可简单/占位）：
- MemoryMatcher        → 匹配程度 0~1
- DensityEstimator     → 返回检测对象数量
- MovementEstimator    → 返回速度等级
- RotationDetector     → 判断是否在转头
"""

from __future__ import annotations
from typing import Optional, Any


class FrameScheduler:
    def __init__(
        self,
        memory_matcher: Optional[Any] = None,
        density_estimator: Optional[Any] = None,
        movement_estimator: Optional[Any] = None,
        rotation_detector: Optional[Any] = None
    ):
        self.memory = memory_matcher
        self.density = density_estimator
        self.movement = movement_estimator
        self.rotation = rotation_detector

    # ---------------------- 计算总 FPS ---------------------- #

    def compute_final_fps(self, base_fps: int, frame) -> int:
        """
        输入：
        - base_fps：来自 FrameManager 的亮度基础 FPS
        - frame：当前图像帧

        输出：
        - final_fps：综合后的最终 FPS
        """

        memory_factor = self._calc_memory_factor(frame)
        density_factor = self._calc_density_factor(frame)
        speed_factor = self._calc_speed_factor(frame)
        rotation_factor = self._calc_rotation_factor(frame)

        final_fps = (
            base_fps
            + memory_factor
            + density_factor
            + speed_factor
            + rotation_factor
        )

        # 限制在 3~15 FPS 范围
        final_fps = max(3, min(15, final_fps))
        return final_fps

    # ---------------------- 四大因子逻辑 ---------------------- #

    def _calc_memory_factor(self, frame) -> int:
        """
        静态环境匹配因素
        匹配度：0~1
        """
        if not self.memory:
            return 0

        match = self.memory.match(frame)

        if match > 0.7:
            return -2
        elif match < 0.4:
            return +3
        return 0

    def _calc_density_factor(self, frame) -> int:
        """
        动态路况：检测对象数量决定 FPS
        """
        if not self.density:
            return 0

        count = self.density.count_objects(frame)

        if count >= 8:
            return +4
        if 4 <= count <= 7:
            return +2
        if 1 <= count <= 3:
            return +1
        return 0

    def _calc_speed_factor(self, frame) -> int:
        """
        移动速度（光流法）
        """
        if not self.movement:
            return 0

        speed = self.movement.get_speed(frame)

        if speed == "fast":
            return +3
        elif speed == "slow":
            return -1
        elif speed == "still":
            return -2
        return 0  # normal

    def _calc_rotation_factor(self, frame) -> int:
        """
        视角旋转检测：正在转头时暂停抽帧
        """
        if not self.rotation:
            return 0

        rotating = self.rotation.is_rotating(frame)
        if rotating:
            return -99  # 大幅降低 → 会被 clamp 到 3 FPS
        return 0
