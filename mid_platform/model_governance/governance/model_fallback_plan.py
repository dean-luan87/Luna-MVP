# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class ModelFallbackPlan:
    """失败情形下的降级去向（骨架；执行由调用方编排）。"""

    plan_id: str
    model_id: str
    on_timeout: str
    on_invalid_output: str
    on_schema_fail: str
    on_governance_blocked: str
    backup_model_id: Optional[str] = None

    def __post_init__(self) -> None:
        for name, v in [
            ("on_timeout", self.on_timeout),
            ("on_invalid_output", self.on_invalid_output),
            ("on_schema_fail", self.on_schema_fail),
            ("on_governance_blocked", self.on_governance_blocked),
        ]:
            if not v or not str(v).strip():
                raise ValueError(
                    f"{name} must be set (backup_model | rule_chain | clarification | reject)"
                )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ModelFallbackPlan:
        return cls(
            plan_id=str(d["plan_id"]),
            model_id=str(d["model_id"]),
            on_timeout=str(d["on_timeout"]),
            on_invalid_output=str(d["on_invalid_output"]),
            on_schema_fail=str(d["on_schema_fail"]),
            on_governance_blocked=str(d["on_governance_blocked"]),
            backup_model_id=(
                None if d.get("backup_model_id") in (None, "") else str(d["backup_model_id"])
            ),
        )


ERROR_TIMEOUT = "timeout"
ERROR_INVALID_OUTPUT = "invalid_output"
ERROR_SCHEMA_FAIL = "schema_fail"
ERROR_GOVERNANCE_BLOCKED = "governance_blocked"


def resolve_fallback_action(plan: ModelFallbackPlan, error_kind: str) -> str:
    """
    根据失败类型返回去向：backup_model | rule_chain | clarification | reject。
    backup_model 且无 backup_model_id 时抛出 ValueError。
    """
    m = {
        ERROR_TIMEOUT: plan.on_timeout,
        ERROR_INVALID_OUTPUT: plan.on_invalid_output,
        ERROR_SCHEMA_FAIL: plan.on_schema_fail,
        ERROR_GOVERNANCE_BLOCKED: plan.on_governance_blocked,
    }
    if error_kind not in m:
        raise ValueError(f"unknown error_kind: {error_kind}")
    action = m[error_kind]
    if action == "backup_model" and not plan.backup_model_id:
        raise ValueError("backup_model_id required when action is backup_model")
    return action


def resolve_backup_model_id_if_needed(plan: ModelFallbackPlan, error_kind: str) -> Optional[str]:
    action = resolve_fallback_action(plan, error_kind)
    if action == "backup_model":
        return plan.backup_model_id
    return None
