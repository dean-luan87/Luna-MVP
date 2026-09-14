from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    ADMISSION_STATUSES,
    BOUNDARY_FALSE_FIELDS,
)


def build_permission_and_admission_module_output_v1(
    input_candidate: Mapping[str, Any],
    eligibility: Mapping[str, Any],
    decision_candidate: Mapping[str, Any],
    diagnostics: Mapping[str, Any],
    trace_replay: Mapping[str, Any],
) -> Dict[str, Any]:
    status = str(eligibility.get("admission_status") or "invalid_input")
    if status not in ADMISSION_STATUSES:
        status = "invalid_input"

    output = {
        "module_status": status,
        "admission_decision_candidate": decision_candidate,
        "rejection_reasons": tuple(eligibility.get("rejection_reasons") or ()),
        "review_required": bool(eligibility.get("review_required")),
        "authority_boundary_result": {
            "requested_authority": input_candidate.get("requested_authority"),
            "requested_operation": input_candidate.get("requested_operation"),
            "boundary_preserved": True,
        },
        "diagnostics": diagnostics,
        "trace_ref": trace_replay.get("trace_ref"),
        "replay_key": trace_replay.get("replay_key"),
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }
    for field in BOUNDARY_FALSE_FIELDS:
        output[field] = False
    return output
