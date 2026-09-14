from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.protocols.protocol_registry_v1 import lookup_protocol

from capabilities.midplatform.protocol_manager.module.protocol_manager_module_types_v1 import (
    not_fact,
)


def run_protocol_manager_registry_lookup_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    protocol_id = str(input_candidate.get("protocol_id") or "")
    snapshot = dict(input_candidate.get("version_snapshot") or {})
    snapshot_registry = dict(snapshot.get("protocol_registry") or {})
    protocol_record = snapshot_registry.get(protocol_id)
    if protocol_record is None and protocol_id:
        protocol_record = lookup_protocol(protocol_id)

    exists = isinstance(protocol_record, dict)
    return {
        "schema_version": "protocol_manager_registry_lookup_v1",
        "protocol_id": protocol_id,
        "protocol_exists": exists,
        "protocol_record": protocol_record if exists else None,
        "registry_source": "version_snapshot"
        if exists and protocol_id in snapshot_registry
        else ("runtime_registry" if exists else "not_found"),
        "candidate_registration_requested": str(input_candidate.get("operation"))
        == "register_candidate",
        "registry_update_applied": False,
        **not_fact(),
    }
