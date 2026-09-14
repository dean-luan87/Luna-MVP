# -*- coding: utf-8 -*-
"""
任务域分类结果（长语音/长文本解析后分类层输出）。

与 docs/architecture/task/LUNA_TASK_DOMAIN_CLASSIFICATION_V1.md §1.4 一致。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DomainClassificationResult:
    """一级域分类 + 可否映射 + 拒绝/澄清候选（模型/parser 产出候选，Core 裁决）。"""

    primary_domain: str
    secondary_domains: List[str] = field(default_factory=list)
    intent_complexity: str = "single_step"
    can_map_to_system_tasks: bool = True
    needs_confirmation: bool = False
    needs_clarification: bool = False
    should_reject: bool = False
    rejection_reason_candidate: Optional[str] = None
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_domain": self.primary_domain,
            "secondary_domains": list(self.secondary_domains),
            "intent_complexity": self.intent_complexity,
            "can_map_to_system_tasks": self.can_map_to_system_tasks,
            "needs_confirmation": self.needs_confirmation,
            "needs_clarification": self.needs_clarification,
            "should_reject": self.should_reject,
            "rejection_reason_candidate": self.rejection_reason_candidate,
            "confidence": self.confidence,
            "metadata": dict(self.metadata),
        }
