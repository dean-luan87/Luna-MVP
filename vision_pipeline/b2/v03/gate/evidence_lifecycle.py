# vision_pipeline/b2/v03/gate/evidence_lifecycle.py
"""
B2 Gate v0.5 - Evidence Lifecycle
证据生命周期管理：OBSERVING → CONFIRMED → DEGRADED → DROPPED
"""

from enum import Enum
from typing import Dict, Any, Optional
import time


class EvidenceState(Enum):
    """证据状态"""
    OBSERVING = "OBSERVING"     # 观察中
    CONFIRMED = "CONFIRMED"     # 已确认
    DEGRADED = "DEGRADED"       # 已降级
    DROPPED = "DROPPED"         # 已丢弃


class EvidenceLifecycle:
    """
    证据生命周期管理器
    
    状态机：
    OBSERVING
      ├─ 连续 ≥ N 帧 + 稳定 → CONFIRMED
      ├─ 稳定性下降 → DEGRADED
      └─ 长时间未再出现 → DROPPED
    """
    
    # 参数（v0.5 固定）
    N_CONFIRM = 8        # frames
    T_DROP = 1.5         # seconds
    
    def __init__(self):
        self._evidence_tracker: Dict[str, Dict[str, Any]] = {}
    
    def update(
        self,
        factor_key: str,
        current_ts: float,
        stability_score: float,
        seen: bool = True
    ) -> EvidenceState:
        """
        更新证据状态
        
        :param factor_key: 因子键（如 "path", "event"）
        :param current_ts: 当前时间戳
        :param stability_score: 当前稳定性分数
        :param seen: 是否在当前帧看到
        :return: 新的证据状态
        """
        
        if factor_key not in self._evidence_tracker:
            if seen:
                # 首次看到
                self._evidence_tracker[factor_key] = {
                    "state": EvidenceState.OBSERVING,
                    "first_seen_ts": current_ts,
                    "last_seen_ts": current_ts,
                    "seen_frames": 1,
                    "temporal_consistency": 1.0
                }
            return EvidenceState.OBSERVING
        
        tracker = self._evidence_tracker[factor_key]
        current_state = tracker["state"]
        
        if seen:
            # 更新看到的信息
            tracker["last_seen_ts"] = current_ts
            tracker["seen_frames"] += 1
            
            # 计算时间一致性（简化版：基于连续看到的帧数）
            duration = current_ts - tracker["first_seen_ts"]
            if duration > 0:
                tracker["temporal_consistency"] = min(
                    tracker["seen_frames"] / (duration * 30.0),  # 假设 30 fps
                    1.0
                )
            
            # 状态转移
            if current_state == EvidenceState.OBSERVING:
                if stability_score >= 0.60 and tracker["seen_frames"] >= self.N_CONFIRM:
                    tracker["state"] = EvidenceState.CONFIRMED
            elif current_state == EvidenceState.DEGRADED:
                # 从降级恢复
                if stability_score >= 0.60:
                    tracker["state"] = EvidenceState.OBSERVING
                    tracker["first_seen_ts"] = current_ts  # 重置
                    tracker["seen_frames"] = 1
        else:
            # 未看到
            if current_state != EvidenceState.DROPPED:
                time_since_last_seen = current_ts - tracker["last_seen_ts"]
                if time_since_last_seen > self.T_DROP:
                    tracker["state"] = EvidenceState.DROPPED
                elif stability_score < 0.45:
                    tracker["state"] = EvidenceState.DEGRADED
        
        return tracker["state"]
    
    def get_evidence_state_dict(
        self,
        factor_key: str,
        current_ts: float
    ) -> Optional[Dict[str, Any]]:
        """
        获取证据状态字典（用于 trace）
        """
        if factor_key not in self._evidence_tracker:
            return None
        
        tracker = self._evidence_tracker[factor_key]
        
        return {
            "state": tracker["state"].value,
            "first_seen_ts": tracker["first_seen_ts"],
            "last_seen_ts": tracker["last_seen_ts"],
            "seen_frames": tracker["seen_frames"],
            "temporal_consistency": round(tracker["temporal_consistency"], 2)
        }
    
    def is_confirmed(self) -> bool:
        """
        检查是否有已确认的证据
        
        :return: 如果有任何证据处于 CONFIRMED 状态，返回 True
        """
        for tracker in self._evidence_tracker.values():
            if tracker["state"] == EvidenceState.CONFIRMED:
                return True
        return False
    
    def get_confirm_frames(self) -> int:
        """
        获取已确认证据的帧数
        
        :return: 已确认证据的总帧数
        """
        total_frames = 0
        for tracker in self._evidence_tracker.values():
            if tracker["state"] == EvidenceState.CONFIRMED:
                total_frames += tracker.get("seen_frames", 0)
        return total_frames
    
    def clear(self, factor_key: Optional[str] = None):
        """
        清除证据跟踪
        
        :param factor_key: 如果为 None，清除所有
        """
        if factor_key is None:
            self._evidence_tracker.clear()
        elif factor_key in self._evidence_tracker:
            del self._evidence_tracker[factor_key]
