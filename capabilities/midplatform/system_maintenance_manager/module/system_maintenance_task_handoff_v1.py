from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_types_v1 import (
    not_fact,
)


def build_system_maintenance_task_handoff_candidate_v1(
    input_candidate: Mapping[str, Any],
    root_cause: Mapping[str, Any],
    remediation: Mapping[str, Any],
) -> Dict[str, Any]:
    remediations = tuple(remediation.get("remediation_candidates") or ())
    task_type = "manual_review_required"
    if remediations:
        task_type = str(
            (remediations[0] or {}).get("maintenance_task_type") or task_type
        )
    return {
        "schema_version": "system_maintenance_task_handoff_v1",
        "task_handoff_candidate": {
            "candidate_id": f"maint_task_{input_candidate.get('maintenance_request_id')}",
            "task_type": task_type,
            "source_capability": root_cause.get("primary_capability_candidate"),
            "fault_domain": root_cause.get("fault_domain"),
            "remediation_candidates": remediations,
            "candidate_only": True,
            **not_fact(),
        },
        **not_fact(),
    }
