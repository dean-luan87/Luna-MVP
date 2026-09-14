from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.protocol_manager.module.protocol_manager_module_types_v1 import (
    MODULE_SCHEMA_VERSION,
    SUPPORTED_OPERATIONS,
    not_fact,
)


def adapt_protocol_manager_input_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    candidate = dict(payload)
    operation = str(candidate.get("operation") or "query")

    return {
        "schema_version": MODULE_SCHEMA_VERSION,
        "protocol_request_id": str(
            candidate.get("protocol_request_id")
            or candidate.get("request_id")
            or "proto_req_unknown"
        ),
        "operation": operation,
        "operation_supported": operation in SUPPORTED_OPERATIONS,
        "protocol_id": str(candidate.get("protocol_id") or "").strip(),
        "protocol_type": str(candidate.get("protocol_type") or "interface_contract"),
        "protocol_version": str(candidate.get("protocol_version") or "").strip(),
        "consumer_capability_id": str(candidate.get("consumer_capability_id") or ""),
        "provider_capability_id": str(candidate.get("provider_capability_id") or ""),
        "input_contract_ref": str(candidate.get("input_contract_ref") or ""),
        "output_contract_ref": str(candidate.get("output_contract_ref") or ""),
        "schema_refs": tuple(candidate.get("schema_refs") or ()),
        "error_namespace_ref": str(candidate.get("error_namespace_ref") or ""),
        "runtime_boundary_ref": str(candidate.get("runtime_boundary_ref") or ""),
        "admission_contract_ref": str(candidate.get("admission_contract_ref") or ""),
        "compatibility_target_version": str(
            candidate.get("compatibility_target_version") or ""
        ).strip(),
        "change_set": dict(candidate.get("change_set") or {}),
        "requested_lifecycle_transition": dict(
            candidate.get("requested_lifecycle_transition") or {}
        ),
        "trace_context": dict(candidate.get("trace_context") or {}),
        "version_snapshot": dict(candidate.get("version_snapshot") or {}),
        "candidate_only": True,
        **not_fact(),
    }
