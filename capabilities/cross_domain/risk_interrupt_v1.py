#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Risk Interrupt V1 (旁路最小实现，默认关闭)。

目标（V1）：
- 接收统一风险事件
- 最小裁决：是否达到抢占阈值
- 打 paused_by_risk 标记 + 生成白盒观测
- 支持 whitebox-only 降级（只记录不抢占）

重要边界：
- 本模块不被任何主链默认 import；只有显式在上层接入时才会生效
- 不实现自动恢复 / 多风险合并 / 重算 / 多模型融合
"""

from __future__ import annotations

import os
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def _env_truthy(name: str, *, default: bool = False) -> bool:
    raw = os.getenv(name, "")
    if raw == "":
        return bool(default)
    return raw.strip().lower() in ("1", "true", "yes")


def risk_interrupt_enabled() -> bool:
    return _env_truthy("LUNA_ENABLE_RISK_INTERRUPT_V1", default=False)


def risk_interrupt_whitebox_only() -> bool:
    # 默认 true：即使开启了总开关，也建议先只入白盒验证
    return _env_truthy("LUNA_RISK_INTERRUPT_WHITEBOX_ONLY", default=True)


@dataclass(frozen=True)
class RiskInterruptEventV1:
    risk_type: str
    risk_level: str  # low | medium | high | critical
    direction_hint: str  # left/right/front/back/unknown
    distance_band: str  # near/medium/far/unknown
    confidence: float
    timestamp_ms: int
    event_id: str = ""

    @staticmethod
    def new(
        *,
        risk_type: str,
        risk_level: str,
        direction_hint: str = "unknown",
        distance_band: str = "unknown",
        confidence: float = 0.0,
        timestamp_ms: Optional[int] = None,
    ) -> "RiskInterruptEventV1":
        ts = int(timestamp_ms if isinstance(timestamp_ms, int) else (time.time() * 1000.0))
        eid = f"risk_{ts}_{uuid.uuid4().hex[:8]}"
        return RiskInterruptEventV1(
            risk_type=str(risk_type),
            risk_level=str(risk_level),
            direction_hint=str(direction_hint),
            distance_band=str(distance_band),
            confidence=float(confidence),
            timestamp_ms=ts,
            event_id=eid,
        )


@dataclass
class OutputStateSnapshot:
    """当前输出状态（最小字段）。"""

    speaking: bool
    output_category: str  # task_tip | safety | explanation | other
    output_digest: str = ""


@dataclass
class TaskChainStateSnapshot:
    """当前任务链状态（最小字段；V1 仅打标）。"""

    task_chain_id: str
    task_status: str  # running | paused | waiting_user | completed
    paused_by_risk: bool = False


@dataclass(frozen=True)
class RiskInterruptDecision:
    interrupt_applied: bool
    task_paused: bool
    final_spoken_output: str
    interrupt_reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RiskInterruptWhitebox:
    event_timestamp_ms: int
    risk_event_summary: Dict[str, Any]
    original_output: Dict[str, Any]
    interrupt_applied: bool
    task_paused: bool
    final_spoken_output: str
    interrupt_reason: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_timestamp": self.event_timestamp_ms,
            "risk_event_summary": dict(self.risk_event_summary),
            "original_output": dict(self.original_output),
            "interrupt_applied": bool(self.interrupt_applied),
            "task_paused": bool(self.task_paused),
            "final_spoken_output": self.final_spoken_output,
            "interrupt_reason": self.interrupt_reason,
        }


def _should_preempt(event: RiskInterruptEventV1) -> bool:
    lv = (event.risk_level or "").strip().lower()
    return lv in ("high", "critical")


def handle_risk_interrupt_v1(
    *,
    event: RiskInterruptEventV1,
    current_output: OutputStateSnapshot,
    task_state: TaskChainStateSnapshot,
) -> RiskInterruptDecision:
    """
    旁路处理：不依赖任何主链对象。

    行为：
    - 若未开启总开关：不做任何抢占，返回 interrupt_applied=False，但仍可被上层选择是否记录白盒
    - 若 whitebox-only：不抢占、不打 paused_by_risk，仅返回白盒可用信息
    - 若 high/critical 且当前输出为 task_tip 且 speaking：允许最小抢占，打 paused_by_risk 并产出一条风险提示
    """
    enabled = risk_interrupt_enabled()
    whitebox_only = risk_interrupt_whitebox_only()
    preempt = _should_preempt(event)

    original_output = {
        "speaking": bool(current_output.speaking),
        "output_category": str(current_output.output_category),
        "output_digest": str(current_output.output_digest or ""),
    }
    risk_summary = {
        "event_id": event.event_id,
        "risk_type": event.risk_type,
        "risk_level": event.risk_level,
        "direction_hint": event.direction_hint,
        "distance_band": event.distance_band,
        "confidence": event.confidence,
    }

    interrupt_applied = False
    task_paused = False
    final_spoken = ""
    interrupt_reason = ""

    if not enabled:
        interrupt_reason = "disabled"
    elif whitebox_only:
        interrupt_reason = "whitebox_only"
    elif not preempt:
        interrupt_reason = "below_preempt_threshold"
    else:
        # preempt path: only interrupt "normal task tip" speaking
        if current_output.speaking and current_output.output_category == "task_tip":
            interrupt_applied = True
            # V1: task pause mark only
            task_state.paused_by_risk = True
            task_paused = True
            interrupt_reason = "preempt_high_or_critical"
            # V1: simple, single-sentence safety output (no fancy NLG)
            if event.direction_hint and event.direction_hint != "unknown":
                final_spoken = f"注意安全，{event.direction_hint}侧有风险，请先停一下。"
            else:
                final_spoken = "注意安全，前方有风险，请先停一下。"
        else:
            interrupt_reason = "not_interruptible_output_state"

    wb = RiskInterruptWhitebox(
        event_timestamp_ms=int(event.timestamp_ms),
        risk_event_summary=risk_summary,
        original_output=original_output,
        interrupt_applied=interrupt_applied,
        task_paused=task_paused,
        final_spoken_output=final_spoken,
        interrupt_reason=interrupt_reason,
    )

    return RiskInterruptDecision(
        interrupt_applied=interrupt_applied,
        task_paused=task_paused,
        final_spoken_output=final_spoken,
        interrupt_reason=interrupt_reason,
        metadata={
            "risk_interrupt_v1": wb.to_dict(),
        },
    )

