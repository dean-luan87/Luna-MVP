"""
C1 State Machine (Phase C1 Active Mode v0.2)

状态机实现：
- STABLE: 正常状态
- SUSPENDED: 暂停状态（严重晃动）
- RECOVERING: 恢复中状态

Protection Mode:
- 静态遮挡检测（frame_diff 连续低于阈值）
- 频闪检测（frame_diff 高频跳变次数）
"""

import time
from enum import Enum
from typing import Optional, Dict, Any
from .c1_config import (
    MOTION_SCORE_THRESHOLD,
    RECOVERY_MOTION_THRESHOLD,
    RECOVERY_STABLE_TIME_SEC,
    STATIC_DIFF_THRESHOLD,
    STATIC_FRAMES_THRESHOLD,
    FLICKER_COUNT_THRESHOLD,
    PROTECTION_MODE_DURATION_SEC,
)
from .c1_decision_logger import C1DecisionLogger


class C1State(Enum):
    """C1 状态枚举"""
    STABLE = "STABLE"
    SUSPENDED = "SUSPENDED"
    RECOVERING = "RECOVERING"


class C1StateMachine:
    """
    C1 状态机
    
    职责：
    - 管理 C1 状态转换（STABLE / SUSPENDED / RECOVERING）
    - 检测 Protection Mode（静态遮挡、频闪）
    """
    
    def __init__(self, decision_logger: Optional[C1DecisionLogger] = None):
        """
        初始化状态机
        
        Args:
            decision_logger: C1 决策日志记录器（如果为 None，会创建新的）
        """
        self.current_state = C1State.STABLE
        self.state_start_time = time.time()
        self.last_state_transition_time = time.time()
        
        # C1 决策日志记录器（用于 log_frequency 验证）
        self.decision_logger = decision_logger or C1DecisionLogger()
        
        # Recovery 相关
        self.recovery_start_time: Optional[float] = None
        self.recovery_stable_start_time: Optional[float] = None
        
        # Protection Mode 相关
        self.protection_mode_active = False
        self.protection_mode_start_time: Optional[float] = None
        self.protection_trigger_reason: Optional[str] = None
        
        # 静态遮挡检测
        self.low_diff_count = 0
        self.last_frame_diff = 0.0
        
        # 频闪检测
        self.frame_diff_history: list[float] = []
        self.high_freq_jump_count = 0
    
    def update(
        self,
        motion_score: float,
        frame_diff: float,
        timestamp: float,
    ) -> Dict[str, Any]:
        """
        更新状态机
        
        Args:
            motion_score: 运动评分
            frame_diff: 帧差异评分
            timestamp: 时间戳
        
        Returns:
            状态机输出字典
        """
        prev_state = self.current_state
        
        # 更新 Protection Mode
        protection_result = self._update_protection_mode(frame_diff, timestamp)
        
        # 如果 Protection Mode 激活，强制 SKIP_MODELING
        if self.protection_mode_active:
            return {
                "state": C1State.SUSPENDED,
                "skip_modeling": True,
                "state_transition": None,  # Protection Mode 不触发状态转换
                "protection_trigger_reason": self.protection_trigger_reason,
                "protection_remaining_sec": max(0, PROTECTION_MODE_DURATION_SEC - (timestamp - self.protection_mode_start_time)),
            }
        
        # 状态转换逻辑
        if self.current_state == C1State.STABLE:
            # STABLE → SUSPENDED: motion_score >= MOTION_SCORE_THRESHOLD
            if motion_score >= MOTION_SCORE_THRESHOLD:
                self.current_state = C1State.SUSPENDED
                self.state_start_time = timestamp
                self.last_state_transition_time = timestamp
                
                # ⚠️ 只记录状态切换事件，决策日志由 C1ActiveController 统一管理
                self.decision_logger.record_state_transition(timestamp)
                
                return {
                    "state": C1State.SUSPENDED,
                    "skip_modeling": True,
                    "state_transition": "STABLE→SUSPENDED",
                    "protection_trigger_reason": None,
                    "protection_remaining_sec": None,
                }
            else:
                # 仍然 STABLE，不记录决策（由 C1ActiveController 的节律闸门控制）
                # 返回 STABLE 状态（在最后统一返回）
                pass
        
        elif self.current_state == C1State.SUSPENDED:
            # SUSPENDED → RECOVERING: motion_score < RECOVERY_MOTION_THRESHOLD
            if motion_score < RECOVERY_MOTION_THRESHOLD:
                self.current_state = C1State.RECOVERING
                self.recovery_start_time = timestamp
                self.recovery_stable_start_time = timestamp
                self.state_start_time = timestamp
                self.last_state_transition_time = timestamp
                
                # ⚠️ 只记录状态切换事件，决策日志由 C1ActiveController 统一管理
                self.decision_logger.record_state_transition(timestamp)
                
                return {
                    "state": C1State.RECOVERING,
                    "skip_modeling": True,  # RECOVERING 期间仍然跳过
                    "state_transition": "SUSPENDED→RECOVERING",
                    "protection_trigger_reason": None,
                    "protection_remaining_sec": None,
                }
            else:
                # 仍然 SUSPENDED，不记录决策（由 C1ActiveController 的节律闸门控制）
                return {
                    "state": C1State.SUSPENDED,
                    "skip_modeling": True,
                    "state_transition": None,
                    "protection_trigger_reason": None,
                    "protection_remaining_sec": None,
                }
        
        elif self.current_state == C1State.RECOVERING:
            # RECOVERING → STABLE: 持续 RECOVERY_STABLE_TIME_SEC 且 motion_score < RECOVERY_MOTION_THRESHOLD
            if motion_score >= RECOVERY_MOTION_THRESHOLD:
                # 恢复失败，回到 SUSPENDED
                self.current_state = C1State.SUSPENDED
                self.recovery_start_time = None
                self.recovery_stable_start_time = None
                self.state_start_time = timestamp
                self.last_state_transition_time = timestamp
                
                # ⚠️ 只记录状态切换事件，决策日志由 C1ActiveController 统一管理
                self.decision_logger.record_state_transition(timestamp)
                
                return {
                    "state": C1State.SUSPENDED,
                    "skip_modeling": True,
                    "state_transition": "RECOVERING→SUSPENDED",
                    "protection_trigger_reason": None,
                    "protection_remaining_sec": None,
                }
            else:
                # 检查是否持续稳定足够长时间
                if self.recovery_stable_start_time is None:
                    self.recovery_stable_start_time = timestamp
                
                stable_duration = timestamp - self.recovery_stable_start_time
                if stable_duration >= RECOVERY_STABLE_TIME_SEC:
                    # 恢复成功，回到 STABLE
                    self.current_state = C1State.STABLE
                    self.recovery_start_time = None
                    self.recovery_stable_start_time = None
                    self.state_start_time = timestamp
                    self.last_state_transition_time = timestamp
                    
                    # ⚠️ 只记录状态切换事件，决策日志由 C1ActiveController 统一管理
                    self.decision_logger.record_state_transition(timestamp)
                    
                    return {
                        "state": C1State.STABLE,
                        "skip_modeling": False,
                        "state_transition": "RECOVERING→STABLE",
                        "protection_trigger_reason": None,
                        "protection_remaining_sec": None,
                    }
                else:
                    # 仍然 RECOVERING，不记录决策（由 C1ActiveController 的节律闸门控制）
                    return {
                        "state": C1State.RECOVERING,
                        "skip_modeling": True,
                        "state_transition": None,
                        "protection_trigger_reason": None,
                        "protection_remaining_sec": None,
                    }
        
        # 默认返回 STABLE，不记录决策（由 C1ActiveController 的节律闸门控制）
        return {
            "state": C1State.STABLE,
            "skip_modeling": False,
            "state_transition": None,
            "protection_trigger_reason": None,
            "protection_remaining_sec": None,
        }
    
    def _update_protection_mode(
        self,
        frame_diff: float,
        timestamp: float,
    ) -> Dict[str, Any]:
        """
        更新 Protection Mode
        
        Args:
            frame_diff: 帧差异评分
            timestamp: 时间戳
        
        Returns:
            Protection Mode 结果
        """
        # 检查 Protection Mode 是否过期
        if self.protection_mode_active:
            if self.protection_mode_start_time is not None:
                elapsed = timestamp - self.protection_mode_start_time
                if elapsed >= PROTECTION_MODE_DURATION_SEC:
                    # Protection Mode 过期 → 进入 RECOVERING
                    self.protection_mode_active = False
                    self.protection_mode_start_time = None
                    self.protection_trigger_reason = None
                    # 记录 Protection 事件（退出）
                    self.decision_logger.record_protection_event(timestamp)
                    # 进入 RECOVERING 状态
                    if self.current_state == C1State.STABLE:
                        self.current_state = C1State.RECOVERING
                        self.recovery_start_time = timestamp
                        self.recovery_stable_start_time = timestamp
        
        # 静态遮挡检测：frame_diff 连续低于阈值
        if frame_diff < STATIC_DIFF_THRESHOLD:
            self.low_diff_count += 1
            if self.low_diff_count >= STATIC_FRAMES_THRESHOLD:
                if not self.protection_mode_active:
                    self.protection_mode_active = True
                    self.protection_mode_start_time = timestamp
                    self.protection_trigger_reason = "STATIC_OCCLUSION"
                    return {"triggered": True, "reason": "STATIC_OCCLUSION"}
        else:
            self.low_diff_count = 0
        
        # 频闪检测：frame_diff 高频跳变
        self.frame_diff_history.append(frame_diff)
        if len(self.frame_diff_history) > 10:
            self.frame_diff_history.pop(0)
        
        # 检测高频跳变（相邻帧 diff 变化大）
        if len(self.frame_diff_history) >= 2:
            if abs(self.frame_diff_history[-1] - self.frame_diff_history[-2]) > 0.5:
                self.high_freq_jump_count += 1
            else:
                self.high_freq_jump_count = max(0, self.high_freq_jump_count - 1)
            
            if self.high_freq_jump_count >= FLICKER_COUNT_THRESHOLD:
                if not self.protection_mode_active:
                    self.protection_mode_active = True
                    self.protection_mode_start_time = timestamp
                    self.protection_trigger_reason = "FLICKER"
                    return {"triggered": True, "reason": "FLICKER"}
        
        self.last_frame_diff = frame_diff
        
        return {"triggered": False, "reason": None}
    
    def get_current_state(self) -> C1State:
        """获取当前状态"""
        return self.current_state
    
    def should_run_modeling(self) -> bool:
        """
        最终决策函数（唯一出口）
        
        Returns:
            是否应该执行 ModelingExecutor
        """
        if self.protection_mode_active:
            return False
        if self.current_state in (C1State.SUSPENDED, C1State.RECOVERING):
            return False
        return True

