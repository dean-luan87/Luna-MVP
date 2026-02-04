# vision_pipeline/b2/v03/runtime_state_machine.py
"""
B2 Runtime State Machine v0.5
行为触发前置状态机

目标：B2 只有在"有资格发言"时才允许进入判断链路，其余时间必须可解释地沉默。
"""

from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import time


class B2RuntimeState(Enum):
    """
    B2 Runtime State Machine v0.5 状态定义
    """
    INIT = auto()           # 启动态
    WARMING_UP = auto()     # 预热态
    SUSPENDED = auto()       # 挂起态
    ACTIVE = auto()          # 唯一允许判断的状态
    READ_ONLY = auto()       # 只读态
    ERROR = auto()           # 异常态


@dataclass
class StateGate:
    """
    状态门控信息
    """
    can_trigger: bool           # 是否允许触发判断
    blocked_by: Optional[str]   # 如果被阻止，原因是什么
    state: B2RuntimeState       # 当前状态
    since: float                 # 进入当前状态的时间戳
    reason: str                 # 进入当前状态的原因


class B2RuntimeStateMachine:
    """
    B2 Runtime State Machine v0.5
    
    职责：控制 B2 何时可以进入判断链路
    不关心识别"对不对"，只关心"现在是否适合做判断"
    """
    
    def __init__(
        self,
        n_frames_min: int = 90,          # 最小帧数（约 3 秒）
        window_min_seconds: float = 5.0,  # 最小窗口时间
        stable_time_seconds: float = 1.5, # 稳定时间要求
    ):
        self.n_frames_min = n_frames_min
        self.window_min_seconds = window_min_seconds
        self.stable_time_seconds = stable_time_seconds
        
        # 当前状态
        self.current_state = B2RuntimeState.INIT
        self.state_since = time.time()
        self.state_reason = "system_start"
        
        # 统计信息
        self.frame_count = 0
        self.stable_start_time: Optional[float] = None
        
        # 外部条件（可以从外部设置）
        self.imu_stable = True
        self.camera_stable = True
        self.distance_valid = True
        self.scene_valid = True
        self.system_load_ok = True
        
    def tick(
        self,
        frame_ts: float,
        window_size: float,
        has_evidences: bool = False
    ) -> StateGate:
        """
        每帧调用，更新状态并返回门控信息
        
        :param frame_ts: 当前帧时间戳
        :param window_size: 当前窗口大小（秒）
        :param has_evidences: 是否有 evidences
        :return: StateGate 对象
        """
        self.frame_count += 1
        
        # 状态转移
        new_state = self._transition(frame_ts, window_size)
        
        if new_state != self.current_state:
            # 状态变化
            self.current_state = new_state
            self.state_since = frame_ts
            self.state_reason = self._get_state_reason(new_state)
        
        # 计算门控信息
        can_trigger, blocked_by = self._compute_gate()
        
        return StateGate(
            can_trigger=can_trigger,
            blocked_by=blocked_by,
            state=self.current_state,
            since=self.state_since,
            reason=self.state_reason
        )
    
    def _transition(
        self,
        frame_ts: float,
        window_size: float
    ) -> B2RuntimeState:
        """
        状态转移逻辑
        """
        current = self.current_state
        
        # INIT → WARMING_UP
        if current == B2RuntimeState.INIT:
            if self.frame_count >= 10:  # 至少收到 10 帧
                return B2RuntimeState.WARMING_UP
        
        # WARMING_UP → ACTIVE / SUSPENDED
        elif current == B2RuntimeState.WARMING_UP:
            # 检查是否满足稳定条件
            if self._check_stability_conditions():
                if window_size >= self.window_min_seconds and self.frame_count >= self.n_frames_min:
                    # 检查稳定时间
                    if self.stable_start_time is None:
                        self.stable_start_time = frame_ts
                    elif frame_ts - self.stable_start_time >= self.stable_time_seconds:
                        return B2RuntimeState.ACTIVE
                # 窗口未完成，继续 WARMING_UP
            else:
                # 条件不满足，挂起
                self.stable_start_time = None
                return B2RuntimeState.SUSPENDED
        
        # SUSPENDED → ACTIVE
        elif current == B2RuntimeState.SUSPENDED:
            if self._check_stability_conditions():
                if self.stable_start_time is None:
                    self.stable_start_time = frame_ts
                elif frame_ts - self.stable_start_time >= self.stable_time_seconds:
                    return B2RuntimeState.ACTIVE
            else:
                # 条件仍不满足，重置稳定时间
                self.stable_start_time = None
        
        # ACTIVE → SUSPENDED
        elif current == B2RuntimeState.ACTIVE:
            if not self._check_stability_conditions():
                self.stable_start_time = None
                return B2RuntimeState.SUSPENDED
        
        # READ_ONLY 和 ERROR 需要外部显式设置
        # 这里不做自动转移
        
        return current
    
    def _check_stability_conditions(self) -> bool:
        """
        检查稳定性条件
        """
        return (
            self.imu_stable and
            self.camera_stable and
            self.distance_valid and
            self.scene_valid and
            self.system_load_ok
        )
    
    def _get_state_reason(self, state: B2RuntimeState) -> str:
        """
        获取状态原因
        """
        if state == B2RuntimeState.INIT:
            return "system_start"
        elif state == B2RuntimeState.WARMING_UP:
            if self.frame_count < self.n_frames_min:
                return "insufficient_frames"
            return "window_not_ready"
        elif state == B2RuntimeState.SUSPENDED:
            # 根据具体条件返回原因
            if not self.imu_stable:
                return "imu_unstable"
            elif not self.camera_stable:
                return "camera_shake"
            elif not self.distance_valid:
                return "distance_invalid"
            elif not self.scene_valid:
                return "scene_invalid"
            elif not self.system_load_ok:
                return "system_load_high"
            return "suspended"
        elif state == B2RuntimeState.ACTIVE:
            return "stable_camera_and_pose"
        elif state == B2RuntimeState.READ_ONLY:
            return "explicit_readonly"
        elif state == B2RuntimeState.ERROR:
            return "system_error"
        return "unknown"
    
    def _compute_gate(self):
        """
        计算门控信息
        """
        if self.current_state == B2RuntimeState.ACTIVE:
            return True, None
        elif self.current_state == B2RuntimeState.INIT:
            return False, "state: INIT"
        elif self.current_state == B2RuntimeState.WARMING_UP:
            return False, "state: WARMING_UP"
        elif self.current_state == B2RuntimeState.SUSPENDED:
            return False, f"state: SUSPENDED ({self.state_reason})"
        elif self.current_state == B2RuntimeState.READ_ONLY:
            return False, "state: READ_ONLY"
        elif self.current_state == B2RuntimeState.ERROR:
            return False, "state: ERROR"
        return False, "unknown_state"
    
    def set_suspended_reason(self, reason: str):
        """
        设置挂起原因（外部调用）
        """
        if reason == "imu_unstable":
            self.imu_stable = False
        elif reason == "camera_shake":
            self.camera_stable = False
        elif reason == "distance_invalid":
            self.distance_valid = False
        elif reason == "scene_invalid":
            self.scene_valid = False
        elif reason == "system_load_high":
            self.system_load_ok = False
    
    def set_readonly(self, readonly: bool):
        """
        设置 READ_ONLY 状态（外部调用）
        """
        if readonly and self.current_state != B2RuntimeState.ERROR:
            self.current_state = B2RuntimeState.READ_ONLY
            self.state_since = time.time()
            self.state_reason = "explicit_readonly"
        elif not readonly and self.current_state == B2RuntimeState.READ_ONLY:
            # 从 READ_ONLY 恢复
            self.current_state = B2RuntimeState.WARMING_UP
            self.state_since = time.time()
            self.state_reason = "readonly_released"
    
    def set_error(self, error: bool, reason: str = "system_error"):
        """
        设置 ERROR 状态（外部调用）
        """
        if error:
            self.current_state = B2RuntimeState.ERROR
            self.state_since = time.time()
            self.state_reason = reason
        elif self.current_state == B2RuntimeState.ERROR:
            # 从 ERROR 恢复
            self.current_state = B2RuntimeState.INIT
            self.state_since = time.time()
            self.state_reason = "error_recovered"
    
    def get_runtime_state_dict(self, frame_ts: float) -> Dict[str, Any]:
        """
        获取 runtime_state 字典（用于 trace）
        """
        state_duration = frame_ts - self.state_since
        
        # 格式化持续时间
        if state_duration < 60:
            since_str = f"{state_duration:.1f}s"
        else:
            m = int(state_duration // 60)
            s = int(state_duration % 60)
            since_str = f"{m:02d}:{s:02d}"
        
        return {
            "state": self.current_state.name,
            "since": since_str,
            "reason": self.state_reason
        }
    
    def get_state_gate_dict(self, gate: StateGate) -> Dict[str, Any]:
        """
        获取 state_gate 字典（用于 trace）
        """
        return {
            "can_trigger": gate.can_trigger,
            "blocked_by": gate.blocked_by
        }
