# core/navigation/scene_context.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Tuple
import time
import math
import logging

logger = logging.getLogger(__name__)


@dataclass
class CameraPose:
    """相机姿态（简化版），以设备坐标系为基础."""
    heading_deg: float = 0.0   # 朝向（平面角度 0-360）
    pitch_deg: float = 0.0     # 俯仰
    roll_deg: float = 0.0      # 翻滚

    def as_tuple(self) -> Tuple[float, float, float]:
        return self.heading_deg, self.pitch_deg, self.roll_deg


@dataclass
class MotionState:
    """设备运动状态（可以从 IMU/光流推导）."""
    speed_mps: float = 0.0                # 平移速度
    turn_rate_deg_s: float = 0.0          # 转向角速度（+ 左转 / - 右转）
    last_step_interval_s: Optional[float] = None  # 上一步间隔，用于步行节奏判断


@dataclass
class FrameContext:
    """
    单帧视觉上下文信息，供方向判断 / 环境理解使用。

    这个类是 D（DirectionEvaluator）和 E（EnvironmentScanner）的统一输入。
    """
    frame_id: int
    timestamp: float
    camera_pose: CameraPose = field(default_factory=CameraPose)
    motion: MotionState = field(default_factory=MotionState)

    # 历史方向（上一帧的"主方向"）用于稳定方向判断
    previous_direction: Optional[str] = None  # 'forward' / 'left' / 'right' / 'backward' / 'stop'
    previous_direction_confidence: float = 0.0

    # 设备对当前姿态/运动的自信程度（0-1）
    pose_confidence: float = 0.8
    motion_confidence: float = 0.8

    # 额外可扩展信息（例如：楼层、导航阶段、子场景等）
    extras: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_raw(
        frame_id: int,
        camera_heading_deg: float,
        camera_pitch_deg: float,
        camera_roll_deg: float,
        speed_mps: float,
        turn_rate_deg_s: float,
        previous_direction: Optional[str] = None,
        previous_direction_confidence: float = 0.0,
        pose_confidence: float = 0.8,
        motion_confidence: float = 0.8,
        extras: Optional[Dict[str, Any]] = None,
    ) -> "FrameContext":
        """后端可以用这个工厂方法快速构造 FrameContext。"""
        ctx = FrameContext(
            frame_id=frame_id,
            timestamp=time.time(),
            camera_pose=CameraPose(
                heading_deg=camera_heading_deg,
                pitch_deg=camera_pitch_deg,
                roll_deg=camera_roll_deg,
            ),
            motion=MotionState(
                speed_mps=speed_mps,
                turn_rate_deg_s=turn_rate_deg_s,
            ),
            previous_direction=previous_direction,
            previous_direction_confidence=previous_direction_confidence,
            pose_confidence=pose_confidence,
            motion_confidence=motion_confidence,
            extras=extras or {},
        )
        logger.debug(
            "[FrameContext] created frame_id=%s heading=%.1f speed=%.2f turn_rate=%.1f",
            frame_id,
            camera_heading_deg,
            speed_mps,
            turn_rate_deg_s,
        )
        return ctx

    # 一些便捷方法，给 DirectionEvaluator 用
    def is_moving_forward(self, speed_threshold: float = 0.1) -> bool:
        return self.motion.speed_mps > speed_threshold

    def is_turning(self, turn_threshold_deg_s: float = 5.0) -> bool:
        return abs(self.motion.turn_rate_deg_s) > turn_threshold_deg_s

    def turning_direction(self, turn_threshold_deg_s: float = 5.0) -> Optional[str]:
        if not self.is_turning(turn_threshold_deg_s):
            return None
        return "left" if self.motion.turn_rate_deg_s > 0 else "right"

    def heading_delta(self, other: "FrameContext") -> float:
        """计算与另一帧 heading 的差值（-180 ~ 180）."""
        delta = self.camera_pose.heading_deg - other.camera_pose.heading_deg
        while delta > 180:
            delta -= 360
        while delta < -180:
            delta += 360
        return delta

    def to_dict(self) -> Dict[str, Any]:
        return {
            "frame_id": self.frame_id,
            "timestamp": self.timestamp,
            "camera_pose": {
                "heading_deg": self.camera_pose.heading_deg,
                "pitch_deg": self.camera_pose.pitch_deg,
                "roll_deg": self.camera_pose.roll_deg,
            },
            "motion": {
                "speed_mps": self.motion.speed_mps,
                "turn_rate_deg_s": self.motion.turn_rate_deg_s,
                "last_step_interval_s": self.motion.last_step_interval_s,
            },
            "previous_direction": self.previous_direction,
            "previous_direction_confidence": self.previous_direction_confidence,
            "pose_confidence": self.pose_confidence,
            "motion_confidence": self.motion_confidence,
            "extras": self.extras,
        }

