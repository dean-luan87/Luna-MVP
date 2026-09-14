from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_types_v1 import (
    not_fact,
)


def build_system_maintenance_capability_locator_v1(
    input_candidate: Mapping[str, Any],
    signal_classification: Mapping[str, Any],
) -> Dict[str, Any]:
    source_cap = str(input_candidate.get("source_capability_id") or "")
    domain_hint = str(signal_classification.get("fault_domain_hint") or "unknown")
    primary = source_cap
    secondary: tuple[str, ...] = tuple()
    if not primary:
        default_by_domain = {
            "protocol_contract": "luna.protocol_manager",
            "model_asset": "luna.model_manager",
            "resource": "luna.model_manager",
            "dependency": "luna.task_manager",
            "baseline_drift": "luna.system_maintenance_manager",
            "registry_drift": "luna.system_maintenance_manager",
            "trace_replay": "luna.system_maintenance_manager",
            "permission_boundary": "luna.permission_and_admission_manager",
            "module_logic": "luna.task_manager",
            "status_reduction": "luna.task_manager",
            "unknown": "luna.system_maintenance_manager",
        }
        primary = default_by_domain.get(domain_hint, "luna.system_maintenance_manager")

    if primary != "luna.protocol_manager":
        secondary = secondary + ("luna.protocol_manager",)
    if primary != "luna.model_manager":
        secondary = secondary + ("luna.model_manager",)

    return {
        "schema_version": "system_maintenance_capability_locator_v1",
        "primary_capability_candidate": primary,
        "secondary_capability_candidates": secondary,
        "suspected_internal_component": "module_api_chain",
        "fault_domain": domain_hint,
        "confidence": 0.82 if bool(source_cap) else 0.67,
        **not_fact(),
    }
