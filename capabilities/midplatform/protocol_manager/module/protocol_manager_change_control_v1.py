from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.protocol_manager.module.protocol_manager_module_types_v1 import (
    not_fact,
)


def build_protocol_manager_change_control_candidate_v1(
    input_candidate: Mapping[str, Any],
    compatibility_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    operation = str(input_candidate.get("operation") or "query")
    breaking = bool(compatibility_candidate.get("breaking_change_candidate"))
    migration_required = compatibility_candidate.get("compatibility_result") in {
        "migration_required",
        "incompatible",
    }

    change_review_required = operation == "change_review" and (
        breaking or migration_required
    )
    change_allowed_candidate = (
        operation == "change_review" and not change_review_required
    )

    return {
        "schema_version": "protocol_manager_change_control_candidate_v1",
        "change_review_required": change_review_required,
        "change_allowed_candidate": change_allowed_candidate,
        "breaking_change_candidate": breaking,
        "migration_required": migration_required,
        "change_applied": False,
        **not_fact(),
    }
