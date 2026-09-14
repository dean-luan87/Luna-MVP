"""
C1 Shadow Controller (Phase C1)

Phase C1 Shadow Controller
- Observe only
- No control
- No feedback to pipeline

⚠️ 禁止：
- 改 fps
- 改 executor
- 改 pipeline routing
"""

import time
from typing import Dict, Any, Optional
from .c1_config import (
    MOTION_SCORE_THRESHOLD,
    RECOVERY_MOTION_THRESHOLD,
    CLASS_C_PRIVATE,
    MIN_FPS,
    MAX_FPS,
    LOG_INTERVAL_SEC,
)


class C1ShadowController:
    """
    Phase C1 Shadow Controller
    
    职责：
    - 只观察，不控制
    - 不影响 pipeline
    - 记录决策建议（但不执行）
    """
    
    def __init__(self):
        """
        初始化 Shadow Controller
        
        注意：这是 Shadow Mode，不会影响系统行为。
        """
        self.last_log_time = 0.0
        self.last_fps_decision: Optional[int] = None
        self.current_state = "STABLE"
        self.state_start_time = time.time()
    
    def observe(
        self,
        motion_score: float,
        frame_diff: float,
        scene_class: str = "allow_camera",
        timestamp: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        观察当前状态并生成决策建议（但不执行）
        
        Args:
            motion_score: 运动评分（0-1）
            frame_diff: 帧差异评分（0-1）
            scene_class: 场景隐私等级（CLASS_A_PUBLIC / CLASS_B_SEMI_PRIVATE / CLASS_C_PRIVATE）
            timestamp: 时间戳（可选，默认使用当前时间）
        
        Returns:
            决策建议字典（但不执行）
        """
        if timestamp is None:
            timestamp = time.time()
        
        decisions: Dict[str, Any] = {}
        
        # --- Stability 判断 ---
        if motion_score >= MOTION_SCORE_THRESHOLD:
            decisions["state"] = "SUSPEND"
        else:
            decisions["state"] = "STABLE"
        
        # 更新状态持续时间
        if decisions["state"] != self.current_state:
            self.current_state = decisions["state"]
            self.state_start_time = timestamp
        
        # --- 隐私判断 ---
        if scene_class == CLASS_C_PRIVATE:
            decisions["camera_policy"] = "FORCE_OFF"
        else:
            decisions["camera_policy"] = "ALLOW"
        
        # --- 抽帧建议（不执行） ---
        suggested_fps = MIN_FPS
        if decisions["state"] == "STABLE" and decisions["camera_policy"] == "ALLOW":
            suggested_fps = min(MAX_FPS, 3)
        elif decisions["state"] == "SUSPEND":
            suggested_fps = 0
        
        decisions["suggested_fps"] = suggested_fps
        
        # --- 优先级建议（不执行） ---
        if decisions["state"] == "SUSPEND":
            decisions["suggested_priority"] = "safety"
        elif motion_score > 0.5:
            decisions["suggested_priority"] = "navigation"
        else:
            decisions["suggested_priority"] = "environment"
        
        # --- 日志节流 ---
        if timestamp - self.last_log_time >= LOG_INTERVAL_SEC:
            self._log(decisions, timestamp, motion_score, frame_diff)
            self.last_log_time = timestamp
        
        self.last_fps_decision = suggested_fps
        
        return decisions  # ⚠️ 只返回，不执行
    
    def _log(
        self,
        decisions: Dict[str, Any],
        timestamp: float,
        motion_score: float,
        frame_diff: float,
    ):
        """
        记录决策建议（但不执行）
        
        Args:
            decisions: 决策建议字典
            timestamp: 时间戳
            motion_score: 运动评分
            frame_diff: 帧差异评分
        """
        state_duration = timestamp - self.state_start_time
        
        print(
            f"[C1-SHADOW][{timestamp:.2f}] "
            f"state={decisions['state']} "
            f"fps={decisions['suggested_fps']} "
            f"priority={decisions['suggested_priority']} "
            f"camera={decisions['camera_policy']} "
            f"motion={motion_score:.2f} "
            f"diff={frame_diff:.2f} "
            f"duration={state_duration:.1f}s"
        )


