"""
C1 日志系统

C1 日志的目标不是 debug，而是解释系统"为什么这样看"。

设计原则：
- 不记录原始图像
- 不记录模型中间特征
- 只记录：状态、决策、原因、后果
"""

import time
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from .c1_types import C1Input, C1Decision
from .c1_state import C1State


@dataclass
class C1LogRecord:
    """
    C1 日志记录
    
    这是可解释 AI 的基础设施，后期价值极大。
    
    注意：格式兼容 C1ReplayRecord，便于回放工具使用。
    """
    timestamp: float

    # 状态
    prev_state: str
    current_state: str

    # 输入摘要（压缩）
    motion_score: float
    frame_diff_score: float

    # 决策结果
    allow_frame: bool
    target_fps: int
    observation_mode: str
    priority: str

    # 解释
    reason: str

    # 输入信号（可选字段，放在最后，兼容 C1ReplayRecord）
    privacy_hit: bool = False
    user_override: bool = False
    next_scene_hint: Optional[str] = None
    risk_hint: Optional[str] = None
    privacy_zone: Optional[str] = None

    # 执行后果（可选）
    modeling_executed: bool = False
    navigation_executed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于 JSON 序列化）"""
        return asdict(self)


class C1Logger:
    """
    C1 日志记录器
    
    职责：
    - 记录 C1 的关键决策
    - 只在状态切换、关键决策变化、安全兜底触发时记录
    - 不每帧都打日志（避免日志爆炸）
    """
    
    def __init__(self, log_file: Optional[str] = None):
        """
        初始化 C1 日志记录器
        
        Args:
            log_file: 日志文件路径（可选，如果为 None 则只记录到内存）
        """
        self.log_file = log_file
        self._logs: list[C1LogRecord] = []
        self._prev_state: Optional[C1State] = None
        self._prev_target_fps: Optional[int] = None
        self._prev_priority: Optional[str] = None
        self._prev_observation_mode: Optional[str] = None
    
    def should_log(
        self,
        current_state: C1State,
        decision: C1Decision,
    ) -> bool:
        """
        判断是否应该记录日志
        
        只在以下情况打日志：
        1. 状态切换
        2. 关键决策变化（target_fps 变化 ≥ 2 倍、priority 变化、observation_mode 变化）
        3. 安全兜底触发（晃动暂停、隐私关闭、频闪防护）
        
        Args:
            current_state: 当前 C1 状态
            decision: C1 决策
        
        Returns:
            如果应该记录日志，返回 True
        """
        # 1. 状态切换
        if self._prev_state != current_state:
            return True
        
        # 2. 关键决策变化
        if self._prev_target_fps is not None:
            if decision.target_fps == 0 and self._prev_target_fps > 0:
                # 从有 fps 变为 0（暂停）
                return True
            if decision.target_fps > 0 and self._prev_target_fps == 0:
                # 从 0 变为有 fps（恢复）
                return True
            if self._prev_target_fps > 0 and decision.target_fps > 0:
                # fps 变化 ≥ 2 倍
                if (decision.target_fps >= self._prev_target_fps * 2 or
                    decision.target_fps <= self._prev_target_fps / 2):
                    return True
        
        if self._prev_priority != decision.priority:
            return True
        
        if self._prev_observation_mode != decision.observation_mode:
            return True
        
        # 3. 安全兜底触发
        if not decision.allow_frame:
            # 晃动暂停、隐私关闭等
            return True
        
        return False
    
    def log(
        self,
        c1_input: C1Input,
        c1_decision: C1Decision,
        current_state: C1State,
        modeling_executed: bool = False,
        navigation_executed: bool = False,
    ) -> Optional[C1LogRecord]:
        """
        记录 C1 日志
        
        Args:
            c1_input: C1 输入信号
            c1_decision: C1 决策
            current_state: 当前 C1 状态
            modeling_executed: ModelingExecutor 是否执行
            navigation_executed: NavigationExecutor 是否执行
        
        Returns:
            如果记录了日志，返回 C1LogRecord；否则返回 None
        """
        # 判断是否应该记录
        if not self.should_log(current_state, c1_decision):
            # 更新 prev 状态（即使不记录也要更新，用于下次判断）
            self._prev_state = current_state
            self._prev_target_fps = c1_decision.target_fps
            self._prev_priority = c1_decision.priority
            self._prev_observation_mode = c1_decision.observation_mode
            return None
        
        # 创建日志记录（兼容 C1ReplayRecord 格式）
        record = C1LogRecord(
            timestamp=time.time(),
            prev_state=self._prev_state.value if self._prev_state else "unknown",
            current_state=current_state.value,
            motion_score=c1_input.motion_score,
            frame_diff_score=c1_input.frame_diff_score,
            privacy_hit=(c1_input.privacy_zone in ("B", "C")),
            user_override=c1_input.user_camera_override,
            next_scene_hint=c1_input.next_scene_hint,
            risk_hint=c1_input.risk_hint,
            privacy_zone=c1_input.privacy_zone,
            allow_frame=c1_decision.allow_frame,
            target_fps=c1_decision.target_fps,
            observation_mode=c1_decision.observation_mode,
            priority=c1_decision.priority,
            reason=c1_decision.reason,
            modeling_executed=modeling_executed,
            navigation_executed=navigation_executed,
        )
        
        # 保存到内存
        self._logs.append(record)
        
        # 如果指定了日志文件，写入文件
        if self.log_file:
            self._write_to_file(record)
        
        # 更新 prev 状态
        self._prev_state = current_state
        self._prev_target_fps = c1_decision.target_fps
        self._prev_priority = c1_decision.priority
        self._prev_observation_mode = c1_decision.observation_mode
        
        return record
    
    def _write_to_file(self, record: C1LogRecord) -> None:
        """
        写入日志文件
        
        Args:
            record: C1 日志记录
        """
        import json
        import os
        
        # 确保目录存在
        if self.log_file:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            
            # 追加模式写入 JSON（每行一个记录）
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
    
    def get_logs(self) -> list[C1LogRecord]:
        """
        获取所有日志记录
        
        Returns:
            日志记录列表
        """
        return self._logs.copy()
    
    def clear_logs(self) -> None:
        """清空日志记录"""
        self._logs.clear()
        self._prev_state = None
        self._prev_target_fps = None
        self._prev_priority = None
        self._prev_observation_mode = None

