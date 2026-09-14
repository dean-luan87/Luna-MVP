from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    MODULE_SCHEMA_VERSION,
    SUPPORTED_REQUEST_TYPES,
    not_fact,
)


def adapt_permission_and_admission_input_v1(
    payload: Mapping[str, Any],
) -> Dict[str, Any]:
    candidate = dict(payload)
    request_type = str(candidate.get("request_type") or "").strip()
    return {
        "schema_version": MODULE_SCHEMA_VERSION,
        "request_id": str(candidate.get("request_id") or "").strip(),
        "request_type": request_type,
        "request_type_supported": request_type in SUPPORTED_REQUEST_TYPES,
        "subject_ref": candidate.get("subject_ref"),
        "resource_ref": candidate.get("resource_ref"),
        "source_ref": candidate.get("source_ref"),
        "owner_ref": candidate.get("owner_ref"),
        "consent_ref": candidate.get("consent_ref"),
        "evidence_refs": tuple(candidate.get("evidence_refs") or ()),
        "provenance_refs": tuple(candidate.get("provenance_refs") or ()),
        "requested_authority": str(candidate.get("requested_authority") or "").strip(),
        "requested_operation": str(candidate.get("requested_operation") or "").strip(),
        "policy_snapshot": dict(candidate.get("policy_snapshot") or {}),
        "version_snapshot": dict(candidate.get("version_snapshot") or {}),
        "temporal_snapshot": dict(candidate.get("temporal_snapshot") or {}),
        "risk_context": dict(candidate.get("risk_context") or {}),
        "trace_ref": str(candidate.get("trace_ref") or "").strip(),
        "candidate_only": True,
        **not_fact(),
    }
