from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.protocol_manager.module.protocol_manager_module_types_v1 import (
    not_fact,
)


def resolve_protocol_manager_version_candidate_v1(
    input_candidate: Mapping[str, Any], registry_lookup: Mapping[str, Any]
) -> Dict[str, Any]:
    protocol_version = str(input_candidate.get("protocol_version") or "").strip()
    target_version = str(
        input_candidate.get("compatibility_target_version") or ""
    ).strip()
    record = dict(registry_lookup.get("protocol_record") or {})
    current_version = str(record.get("version") or protocol_version or "").strip()

    return {
        "schema_version": "protocol_manager_version_resolver_v1",
        "current_version": current_version,
        "requested_version": protocol_version,
        "compatibility_target_version": target_version,
        "version_snapshot_present": bool(input_candidate.get("version_snapshot")),
        "version_resolution_status": "resolved" if current_version else "unknown",
        **not_fact(),
    }
