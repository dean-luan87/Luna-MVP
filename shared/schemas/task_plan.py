# -*- coding: utf-8 -*-
"""
任务计划三层对象（v1 / v2 / final）与计划差异。

统一骨架便于白盒 diff 与图书馆沉淀。详见：
docs/architecture/task/LUNA_TASK_PLAN_V1_V2_FINAL_V1.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

# plan_version 取值与文档一致
PlanVersionLiteral = Literal["v1", "v2", "final"]
TaskPriorityLiteral = Literal["primary", "secondary", "opportunistic"]
TaskChainImpactLiteral = Literal["low", "medium", "high"]


@dataclass
class TaskPlanItem:
    """单任务项（执行单元语义）。"""

    task_id: str
    task_domain: str
    task_action: str
    system_mapping_candidate: str
    target: Dict[str, Any] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    priority: TaskPriorityLiteral = "primary"
    dependency: Optional[str] = None  # 前置 task_id
    is_temporary: bool = False
    requires_confirmation: bool = False
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_domain": self.task_domain,
            "task_action": self.task_action,
            "system_mapping_candidate": self.system_mapping_candidate,
            "target": dict(self.target),
            "constraints": list(self.constraints),
            "priority": self.priority,
            "dependency": self.dependency,
            "is_temporary": self.is_temporary,
            "requires_confirmation": self.requires_confirmation,
            "confidence": self.confidence,
            "metadata": dict(self.metadata),
        }


@dataclass
class TaskPlan:
    """
    统一计划对象：task_plan_v1 / v2 / final 共用骨架。

    plan_version 区分 v1（原始）、v2（增强）、final（用户定稿执行版）。
    primary_domain / secondary_domains 取值见 task_domain_v1.PRIMARY_DOMAIN_V1。
    """

    plan_id: str
    plan_version: PlanVersionLiteral
    source: str
    primary_domain: str = ""
    secondary_domains: List[str] = field(default_factory=list)
    base_plan_id: Optional[str] = None
    tasks: List[TaskPlanItem] = field(default_factory=list)
    execution_order: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    clarification_needed: bool = False
    confirmation_needed: bool = False
    optimization_applied: bool = False
    optimization_reason: Optional[str] = None
    generated_at: str = ""
    # 长输入拆解 v1：预留 V2 协同位（不接模型、不生成 V2 时仍为 True / 固定 next_stage）
    knowledge_collaboration_pending: bool = True
    task_optimization_pending: bool = True
    next_stage: str = "knowledge_collaboration_and_optimization"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "plan_version": self.plan_version,
            "source": self.source,
            "primary_domain": self.primary_domain,
            "secondary_domains": list(self.secondary_domains),
            "base_plan_id": self.base_plan_id,
            "tasks": [t.to_dict() for t in self.tasks],
            "execution_order": list(self.execution_order),
            "constraints": list(self.constraints),
            "clarification_needed": self.clarification_needed,
            "confirmation_needed": self.confirmation_needed,
            "optimization_applied": self.optimization_applied,
            "optimization_reason": self.optimization_reason,
            "generated_at": self.generated_at,
            "knowledge_collaboration_pending": self.knowledge_collaboration_pending,
            "task_optimization_pending": self.task_optimization_pending,
            "next_stage": self.next_stage,
            "metadata": dict(self.metadata),
        }


@dataclass
class PlanChange:
    """单条变更说明（可带 task_id 便于白盒归因）。"""

    change_type: str
    details: str
    task_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlanDelta:
    """
    v1 → v2 或 v2 → final 等差异，用于白盒与经验归因。

    使用 from_plan_id / to_plan_id 与文档 JSON 一致。
    """

    delta_id: str
    from_plan_id: str
    to_plan_id: str
    changes: List[PlanChange] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "delta_id": self.delta_id,
            "from_plan_id": self.from_plan_id,
            "to_plan_id": self.to_plan_id,
            "changes": [
                {
                    "change_type": c.change_type,
                    "details": c.details,
                    **({"task_id": c.task_id} if c.task_id else {}),
                    **({"metadata": dict(c.metadata)} if c.metadata else {}),
                }
                for c in self.changes
            ],
            "metadata": dict(self.metadata),
        }


def wrap_plan_delta_nested(plan_delta: PlanDelta) -> Dict[str, Any]:
    """与文档 JSON 一致：plan_delta.from_plan_id / to_plan_id / changes。"""
    ch: List[Dict[str, Any]] = []
    for c in plan_delta.changes:
        row: Dict[str, Any] = {"change_type": c.change_type, "details": c.details}
        if c.task_id:
            row["task_id"] = c.task_id
        ch.append(row)
    return {
        "plan_delta": {
            "from_plan_id": plan_delta.from_plan_id,
            "to_plan_id": plan_delta.to_plan_id,
            "changes": ch,
        }
    }
