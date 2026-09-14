from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .gate_runtime_profile import GateRuntimeProfile, GateMode, ComputeLevel


@dataclass
class _State:
    last_tick_ts: Optional[float] = None


class B2SchedulerV05:
    """
    v0.5 scheduling enforcer:
    - Enforces tick rate from GateRuntimeProfile
    - Ensures B cannot "self-override" runtime cadence
    """

    def __init__(self) -> None:
        self._st = _State()

    def allow_tick(self, profile: GateRuntimeProfile, frame_ts: float) -> bool:
        # GateRuntimeProfile must exist (DCS can enforce this via trace)
        interval_s = max(profile.tick_interval_ms, 1) / 1000.0

        # SUSPENDED: still allow writing trace elsewhere, but B execution must be blocked
        # We return True here only to let tick() continue to the SUSPENDED early-exit path
        # so the behavior is uniform.
        if profile.gate_mode == GateMode.SUSPENDED:
            self._st.last_tick_ts = frame_ts
            return True

        # Rate-limit execution
        if self._st.last_tick_ts is None:
            self._st.last_tick_ts = frame_ts
            return True

        if (frame_ts - self._st.last_tick_ts) < interval_s:
            return False

        self._st.last_tick_ts = frame_ts
        return True

    def get_compute_budget(self, profile: GateRuntimeProfile) -> dict:
        """
        根据 GateRuntimeProfile 的 compute_level 返回计算预算
        
        :param profile: GateRuntimeProfile 对象
        :return: 计算预算字典，包含允许的操作
        """
        compute_level = profile.compute_level
        
        if compute_level == ComputeLevel.NONE:
            return {
                "allow_perception": False,
                "allow_evidence": False,
                "allow_impact": False,
                "allow_output": False
            }
        elif compute_level == ComputeLevel.LIGHT:
            return {
                "allow_perception": True,
                "allow_evidence": False,  # LIGHT 模式：不产生新证据
                "allow_impact": False,
                "allow_output": False
            }
        elif compute_level == ComputeLevel.FULL:
            return {
                "allow_perception": True,
                "allow_evidence": True,
                "allow_impact": True,
                "allow_output": True
            }
        else:
            # 默认：保守策略
            return {
                "allow_perception": False,
                "allow_evidence": False,
                "allow_impact": False,
                "allow_output": False
            }
