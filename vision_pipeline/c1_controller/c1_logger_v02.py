"""
C1 Logger v0.2（结构化日志）

v0.2 必须有结构化日志字段：
- c1_state
- state_transition（如 STABLE→SUSPENDED）
- motion_score
- frame_diff
- protection_active
- protection_reason（STATIC_OCCLUSION / FLICKER）
- protection_remaining_sec
- modeling_executed（True/False）

没有这些字段 = 不可回溯 = 不能上线。
"""

import time
import json
from typing import Optional, Dict, Any
from .c1_state_machine import C1State


class C1LoggerV02:
    """
    C1 Logger v0.2
    
    职责：
    - 记录结构化日志（逐帧）
    - 确保可回溯、可复盘
    """
    
    def __init__(self, log_file: Optional[str] = None):
        """
        初始化 C1 Logger v0.2
        
        Args:
            log_file: 日志文件路径（可选，如果为 None 则只记录到内存）
        """
        self.log_file = log_file
        self._logs: list[Dict[str, Any]] = []
        self._last_log_time = 0.0
        self._log_interval = 0.5  # 每 0.5 秒记录一次（避免日志爆炸）
    
    def log(
        self,
        c1_state: C1State,
        state_transition: Optional[str],
        motion_score: float,
        frame_diff: float,
        protection_active: bool,
        protection_reason: Optional[str],
        protection_remaining_sec: Optional[float],
        modeling_executed: bool,
        timestamp: Optional[float] = None,
    ):
        """
        记录结构化日志
        
        Args:
            c1_state: C1 状态
            state_transition: 状态转换（如 STABLE→SUSPENDED）
            motion_score: 运动评分
            frame_diff: 帧差异评分
            protection_active: Protection Mode 是否激活
            protection_reason: Protection 触发原因（STATIC_OCCLUSION / FLICKER）
            protection_remaining_sec: Protection 剩余时间（秒）
            modeling_executed: ModelingExecutor 是否执行
            timestamp: 时间戳（可选）
        """
        if timestamp is None:
            timestamp = time.time()
        
        # 日志节流（避免日志爆炸）
        if timestamp - self._last_log_time < self._log_interval:
            return
        
        self._last_log_time = timestamp
        
        # 构建结构化日志记录
        log_record = {
            "timestamp": timestamp,
            "c1_state": c1_state.value,
            "state_transition": state_transition,
            "motion_score": motion_score,
            "frame_diff": frame_diff,
            "protection_active": protection_active,
            "protection_reason": protection_reason,
            "protection_remaining_sec": protection_remaining_sec,
            "modeling_executed": modeling_executed,
        }
        
        # 记录到内存
        self._logs.append(log_record)
        
        # 如果指定了日志文件，写入文件（JSON Lines 格式）
        if self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(log_record) + "\n")
            except Exception as e:
                print(f"⚠️  写入日志文件失败: {e}")
        
        # 控制台输出（简化版）
        log_parts = [
            f"[C1-v0.2][{timestamp:.2f}]",
            f"state={c1_state.value}",
            f"motion={motion_score:.2f}",
            f"diff={frame_diff:.2f}",
            f"modeling={'YES' if modeling_executed else 'NO'}",
        ]
        
        if state_transition:
            log_parts.append(f"transition={state_transition}")
        if protection_active:
            log_parts.append(f"protection={protection_reason}")
            if protection_remaining_sec is not None:
                log_parts.append(f"remaining={protection_remaining_sec:.1f}s")
        
        print(" ".join(log_parts))
    
    def get_logs(self) -> list[Dict[str, Any]]:
        """获取所有日志记录"""
        return self._logs.copy()
    
    def clear_logs(self):
        """清空日志记录"""
        self._logs.clear()


