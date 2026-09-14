from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.protocol_manager.module.protocol_manager_module_types_v1 import (
    not_fact,
)


def build_protocol_manager_admission_candidate_v1(
    input_candidate: Mapping[str, Any],
    compatibility_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    operation = str(input_candidate.get("operation") or "query")
    admission_contract_ref = str(input_candidate.get("admission_contract_ref") or "")

    if operation == "admission_check" and not admission_contract_ref:
        admitted = False
        reason = "missing_admission_contract_ref"
    elif compatibility_candidate.get("compatibility_result") == "incompatible":
        admitted = False
        reason = "compatibility_incompatible"
    else:
        admitted = True
        reason = "admission_candidate_allowed"

    return {
        "schema_version": "protocol_manager_admission_candidate_v1",
        "admitted": admitted,
        "admission_reason": reason,
        "admission_contract_ref": admission_contract_ref,
        "admission_applied": False,
        **not_fact(),
    }
