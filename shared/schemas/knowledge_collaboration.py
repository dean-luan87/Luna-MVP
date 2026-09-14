# -*- coding: utf-8 -*-
"""
知识协同（knowledge_collaboration）协议占位。

在 task_plan_v1 → task_plan_v2 路径上，汇总记忆/环境/经验等增强信号；
不裁决、不执行。详见：
docs/architecture/task/LUNA_TASK_PROTOCOL_AND_MODEL_GATE_V1.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class KnowledgeCollaborationContext:
    """进入协同层的输入引用（最小字段，可扩展）。"""

    base_plan_id: str
    session_id: Optional[str] = None
    task_chain_id: Optional[str] = None
    """显式用户字面约束（不可被协同层覆盖）。"""
    user_literal_constraints: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeCollaborationResult:
    """协同层输出，供生成/调整 task_plan_v2 与 plan_delta。"""

    result_id: str
    base_plan_id: str
    knowledge_sources: List[str] = field(default_factory=list)
    environment_hints: Dict[str, Any] = field(default_factory=dict)
    experience_hints: Dict[str, Any] = field(default_factory=dict)
    constraints_respected: bool = True
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "base_plan_id": self.base_plan_id,
            "knowledge_sources": list(self.knowledge_sources),
            "environment_hints": dict(self.environment_hints),
            "experience_hints": dict(self.experience_hints),
            "constraints_respected": self.constraints_respected,
            "notes": self.notes,
            "metadata": dict(self.metadata),
        }
