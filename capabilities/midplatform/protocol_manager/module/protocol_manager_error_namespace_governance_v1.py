from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.protocol_manager.module.protocol_manager_module_types_v1 import (
    not_fact,
)


def build_protocol_manager_error_namespace_report_v1(
    input_candidate: Mapping[str, Any],
    registry_lookup: Mapping[str, Any],
) -> Dict[str, Any]:
    requested_namespace = str(input_candidate.get("error_namespace_ref") or "")
    protocol_record = dict(registry_lookup.get("protocol_record") or {})
    registered_namespace = str(
        protocol_record.get("error_namespace")
        or protocol_record.get("error_code_namespace")
        or ""
    )

    conflict = bool(
        requested_namespace
        and registered_namespace
        and requested_namespace != registered_namespace
    )

    return {
        "schema_version": "protocol_manager_error_namespace_governance_v1",
        "requested_namespace": requested_namespace,
        "registered_namespace": registered_namespace,
        "error_namespace_conflict": conflict,
        "error_namespace_check_applied": True,
        **not_fact(),
    }
