# vision_pipeline/b2/v03/gate/gate_evaluator.py
"""
B2 Gate v0.5 - Gate Evaluator
Gate 判定：什么时候不工作 / 只读 / 延迟承认
"""

from enum import Enum
from typing import Dict, Any, Optional, Tuple


class B2GateMode(Enum):
    """B2 Gate 模式"""
    ACTIVE = "ACTIVE"           # 允许进入 OBSERVING / CONFIRMED
    READ_ONLY = "READ_ONLY"     # 只观测，不产出
    SUSPENDED = "SUSPENDED"     # 完全不工作


class GateEvaluator:
    """
    B2 Gate 评估器
    
    Gate 判定顺序（顺序很重要）：
    1. 资源 Gate（C 是否抢占）
    2. 稳定性 Gate（stability_score）
    3. 距离 Gate（3m 规则）
    4. 可见性 Gate（遮挡/模糊）
    5. 场景 Gate（室内/狭窄，由 C 提供 context）
    """
    
    # Gate 阈值（固定）
    STABILITY_HARD_BLOCK = 0.45
    STABILITY_SOFT_BLOCK = 0.60
    
    # 距离 Gate 参数（带滞回）
    DISTANCE_ENTER = 3.2  # m
    DISTANCE_EXIT = 2.8   # m
    
    # 可见性 Gate 参数
    OCCLUSION_THRESHOLD = 0.35
    
    def __init__(self):
        self._last_distance = None
        self._last_mode = None
    
    def evaluate(
        self,
        stability_score: float,
        range_m: Optional[float] = None,
        c_runtime_state: Optional[Dict[str, Any]] = None,
        system_fps: Optional[float] = None,
        occlusion_ratio: Optional[float] = None,
        blur_score: Optional[float] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[B2GateMode, Optional[str]]:
        """
        评估 Gate 状态
        
        :return: (mode, blocked_reason)
        """
        
        # 1. 资源 Gate（最高优先级）
        if c_runtime_state and c_runtime_state.get("high_priority", False):
            return B2GateMode.SUSPENDED, "yield_to_C"
        
        if system_fps is not None and system_fps < 15:
            return B2GateMode.SUSPENDED, "system_fps_low"
        
        # 2. 稳定性 Gate（核心）
        if stability_score < self.STABILITY_HARD_BLOCK:
            return B2GateMode.SUSPENDED, f"stability_too_low_{stability_score:.2f}"
        
        if stability_score < self.STABILITY_SOFT_BLOCK:
            # 继续后续 Gate，但最终可能是 READ_ONLY
            pass
        # else: stability_score >= 0.60，继续后续 Gate
        
        # 3. 距离 Gate（3m 边界，带滞回）
        if range_m is not None:
            if self._last_mode == B2GateMode.ACTIVE:
                # 退出条件（滞回）
                if range_m <= self.DISTANCE_EXIT:
                    return B2GateMode.READ_ONLY, f"distance_too_close_{range_m:.2f}m"
            else:
                # 进入条件
                if range_m < self.DISTANCE_ENTER:
                    return B2GateMode.READ_ONLY, f"distance_too_close_{range_m:.2f}m"
        
        # 4. 可见性 Gate（最小可行版）
        if occlusion_ratio is not None and occlusion_ratio > self.OCCLUSION_THRESHOLD:
            return B2GateMode.SUSPENDED, f"occlusion_too_high_{occlusion_ratio:.2f}"
        
        # blur_score 检查（v0.5 可选）
        # if blur_score is not None:
        #     if blur_score < BLUR_MIN or blur_score > BLUR_MAX:
        #         return B2GateMode.READ_ONLY, "blur_out_of_range"
        
        # 5. 场景 Gate（由 C 提供）
        if context:
            if context.get("indoor", False) or context.get("narrow", False) or context.get("elevator", False):
                return B2GateMode.READ_ONLY, "context_owned_by_C"
        
        # 所有 Gate 通过
        if stability_score >= self.STABILITY_SOFT_BLOCK:
            mode = B2GateMode.ACTIVE
            reason = None
        else:
            # stability_score 在 0.45 ~ 0.60 之间
            mode = B2GateMode.READ_ONLY
            reason = f"stability_marginal_{stability_score:.2f}"
        
        # 更新状态
        self._last_distance = range_m
        self._last_mode = mode
        
        return mode, reason
    
    def get_gate_eval_dict(
        self,
        mode: B2GateMode,
        blocked_reason: Optional[str],
        stability_score: float
    ) -> Dict[str, Any]:
        """
        获取 Gate 评估结果字典（用于 trace）
        """
        return {
            "gate_mode": mode.value,
            "stability_score": stability_score,
            "blocked": blocked_reason is not None,
            "blocked_reason": blocked_reason
        }
