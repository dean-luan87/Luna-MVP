# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ModelRouteDecision:
    """某次路由选择结果（可序列化、可解释）。"""

    task_domain: str
    selected_model_id: Optional[str]
    selection_reason: str
    fallback_applied: bool
    fallback_reason: Optional[str]
    governance_constraints: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ModelRouteDecision:
        return cls(
            task_domain=str(d["task_domain"]),
            selected_model_id=(
                None if d.get("selected_model_id") in (None, "") else str(d["selected_model_id"])
            ),
            selection_reason=str(d["selection_reason"]),
            fallback_applied=bool(d["fallback_applied"]),
            fallback_reason=(
                None if d.get("fallback_reason") is None else str(d["fallback_reason"])
            ),
            governance_constraints=dict(d.get("governance_constraints", {})),
        )
