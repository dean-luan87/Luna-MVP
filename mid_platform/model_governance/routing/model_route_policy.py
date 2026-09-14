# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ModelRoutePolicy:
    """任务域到主模型 / 回退的静态路由策略（骨架，无运行时学习）。"""

    policy_id: str
    task_domain_to_primary: Dict[str, str]
    task_domain_to_fallback: Dict[str, str] = field(default_factory=dict)
    default_fallback_model_id: Optional[str] = None
    fallback_to_rule_chain: bool = False
    shadow_candidates: List[str] = field(default_factory=list)
    background_only_models: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id is required")

    @property
    def fallback_model_id(self) -> Optional[str]:
        """与文档一致的别名，等价于 default_fallback_model_id。"""
        return self.default_fallback_model_id

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ModelRoutePolicy:
        return cls(
            policy_id=str(d["policy_id"]),
            task_domain_to_primary=dict(d["task_domain_to_primary"]),
            task_domain_to_fallback=dict(d.get("task_domain_to_fallback", {})),
            default_fallback_model_id=(
                None
                if d.get("default_fallback_model_id") in (None, "")
                else str(d["default_fallback_model_id"])
            ),
            fallback_to_rule_chain=bool(d.get("fallback_to_rule_chain", False)),
            shadow_candidates=list(d.get("shadow_candidates", [])),
            background_only_models=list(d.get("background_only_models", [])),
        )
