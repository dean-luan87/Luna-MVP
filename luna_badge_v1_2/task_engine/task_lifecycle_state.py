# task_engine/task_lifecycle_state.py

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal, Optional, Dict, Any
import time


class TaskLifecyclePhase(str, Enum):
    """粗粒度阶段：和现有 phase 对齐（ask / task / idle）"""

    IDLE = "idle"
    ASK = "ask"
    TASK = "task"


class TaskLifecycleStatus(str, Enum):
    """
    任务生命周期的细粒度状态（不等同于 phase）：

    - ACTIVE: 正在运行（Ask 或 Task）

    - PAUSED: 暂停状态（用户或系统暂停，具体来源通过 source 字段区分）

    - SUSPENDED_TEMP: 暂时挂起，用于插入子任务

    - FINISHED: 正常完成

    - ABORTED: 异常中止或策略终止
    """

    ACTIVE = "active"
    PAUSED = "paused"  # Ultra: 统一暂停状态，不再区分 PAUSED_USER/PAUSED_SYSTEM
    SUSPENDED_TEMP = "suspended_temp"
    FINISHED = "finished"
    ABORTED = "aborted"


@dataclass
class TaskLifecycleState:
    """
    统一的任务生命周期状态对象。

    后续会挂在 TaskChainManager / 缓存系统上，用于：

    - 当前状态查询

    - 暂停/恢复决策

    - 故障恢复（通过持久化）
    """

    phase: TaskLifecyclePhase = TaskLifecyclePhase.IDLE
    status: TaskLifecycleStatus = TaskLifecycleStatus.ACTIVE

    reason: Optional[str] = None            # 最近一次状态变更原因
    source: Optional[Literal["user", "system", "child_task"]] = None
    updated_at: float = field(default_factory=lambda: time.time())
    created_at: float = field(default_factory=lambda: time.time())

    # --- Ultra: 暂停统计字段 ---
    pause_count: int = 0
    total_pause_duration: float = 0.0
    last_paused_at: Optional[float] = None
    last_resumed_at: Optional[float] = None

    # 预留扩展字段（例如：子任务 ID、父任务 ID 等）
    meta: Dict[str, Any] = field(default_factory=dict)

    def mark(
        self,
        *,
        phase: Optional[TaskLifecyclePhase] = None,
        status: Optional[TaskLifecycleStatus] = None,
        reason: Optional[str] = None,
        source: Optional[Literal["user", "system", "child_task"]] = None,
        extra_meta: Optional[Dict[str, Any]] = None,
        now: Optional[float] = None,
    ) -> None:
        """
        状态更新的统一入口。
        
        Ultra: 同时维护暂停/恢复统计。
        """
        ts = now or time.time()
        
        # --- Ultra: 进入暂停状态时，记录暂停起点 ---
        if status is not None:
            if (
                self.status != TaskLifecycleStatus.PAUSED
                and status == TaskLifecycleStatus.PAUSED
            ):
                # 从非暂停 → 暂停
                self.pause_count += 1
                self.last_paused_at = ts
            
            # --- Ultra: 从暂停状态恢复时，累积暂停时长 ---
            if (
                self.status == TaskLifecycleStatus.PAUSED
                and status != TaskLifecycleStatus.PAUSED
            ):
                if self.last_paused_at is not None:
                    self.total_pause_duration += ts - self.last_paused_at
                self.last_resumed_at = ts
            
            self.status = status
        
        if phase is not None:
            self.phase = phase
        if reason is not None:
            self.reason = reason
        if source is not None:
            self.source = source
        if extra_meta:
            self.meta.update(extra_meta)

        self.updated_at = ts

    @property
    def is_active(self) -> bool:
        return self.status == TaskLifecycleStatus.ACTIVE

    @property
    def is_paused(self) -> bool:
        return self.status in (
            TaskLifecycleStatus.PAUSED,
            TaskLifecycleStatus.SUSPENDED_TEMP,
        )

    @property
    def is_finished(self) -> bool:
        return self.status == TaskLifecycleStatus.FINISHED

    @property
    def is_aborted(self) -> bool:
        return self.status == TaskLifecycleStatus.ABORTED

    def to_dict(self) -> Dict[str, Any]:
        """用于持久化 / 日志的序列化形式。"""
        return {
            "phase": self.phase.value,
            "status": self.status.value,
            "reason": self.reason,
            "source": self.source,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "pause_count": self.pause_count,
            "total_pause_duration": self.total_pause_duration,
            "last_paused_at": self.last_paused_at,
            "last_resumed_at": self.last_resumed_at,
            "meta": dict(self.meta) if self.meta else {},
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskLifecycleState":
        """从持久化数据恢复。"""
        # 兼容旧数据：将 PAUSED_USER/PAUSED_SYSTEM 转换为 PAUSED
        status_value = data.get("status", TaskLifecycleStatus.ACTIVE.value)
        if status_value in ("paused_user", "paused_system"):
            status_value = "paused"
        
        return cls(
            phase=TaskLifecyclePhase(data.get("phase", TaskLifecyclePhase.IDLE.value)),
            status=TaskLifecycleStatus(status_value),
            reason=data.get("reason"),
            source=data.get("source"),
            created_at=data.get("created_at", time.time()),
            updated_at=data.get("updated_at", time.time()),
            pause_count=data.get("pause_count", 0),
            total_pause_duration=data.get("total_pause_duration", 0.0),
            last_paused_at=data.get("last_paused_at"),
            last_resumed_at=data.get("last_resumed_at"),
            meta=data.get("meta") or {},
        )

