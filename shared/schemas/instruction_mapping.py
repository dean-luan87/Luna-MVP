# -*- coding: utf-8 -*-
"""
内部任务指令映射记录（候选审查用）。

模型/解析层产出 InstructionMappingRecord 或等价 dict，由 Core/TaskChain 裁决。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple


@dataclass(frozen=True)
class InstructionMappingRecord:
    """单条映射候选：人话域 → 系统指令 id + 参数约束 + 治理属性。"""

    human_intent_domain: str
    human_intent_action: str
    system_mapping_candidate: str
    required_params: Tuple[str, ...] = ()
    optional_params: Tuple[str, ...] = ()
    requires_confirmation_default: bool = False
    task_chain_impact_level: str = "medium"  # low | medium | high
    supports_temporary_insertion: bool = False
    allowed_in_no_task_mode: bool = True
    allowed_in_task_mode: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "human_intent_domain": self.human_intent_domain,
            "human_intent_action": self.human_intent_action,
            "system_mapping_candidate": self.system_mapping_candidate,
            "required_params": list(self.required_params),
            "optional_params": list(self.optional_params),
            "requires_confirmation_default": self.requires_confirmation_default,
            "task_chain_impact_level": self.task_chain_impact_level,
            "supports_temporary_insertion": self.supports_temporary_insertion,
            "allowed_in_no_task_mode": self.allowed_in_no_task_mode,
            "allowed_in_task_mode": self.allowed_in_task_mode,
            "metadata": dict(self.metadata),
        }


def mapping_records_to_jsonable(rows: List[InstructionMappingRecord]) -> List[Dict[str, Any]]:
    return [r.to_dict() for r in rows]
