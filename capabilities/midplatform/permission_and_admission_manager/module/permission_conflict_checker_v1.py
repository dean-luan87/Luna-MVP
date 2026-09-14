from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    not_fact,
)


def build_permission_conflict_check_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    risk_context = dict(input_candidate.get("risk_context") or {})
    conflict_unresolved = bool(risk_context.get("conflict_unresolved", False))
    return {
        "schema_version": "permission_conflict_checker_v1",
        "conflict_unresolved": conflict_unresolved,
        "conflict_count": int(
            risk_context.get("conflict_count") or (1 if conflict_unresolved else 0)
        ),
        **not_fact(),
    }
