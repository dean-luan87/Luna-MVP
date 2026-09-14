from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    not_fact,
)


def build_permission_risk_check_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    risk_context = dict(input_candidate.get("risk_context") or {})
    risk_level = str(risk_context.get("risk_level") or "low")
    risk_blocked = bool(risk_context.get("risk_blocked", False))
    review_required = bool(risk_context.get("review_required", False))
    return {
        "schema_version": "permission_risk_checker_v1",
        "risk_level": risk_level,
        "risk_blocked": risk_blocked,
        "review_required": review_required,
        **not_fact(),
    }
