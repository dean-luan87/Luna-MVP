from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_types_v1 import (
    not_fact,
)


def build_system_maintenance_root_cause_candidates_v1(
    capability_locator: Mapping[str, Any],
    anomaly_correlation: Mapping[str, Any],
    baseline_calibration: Mapping[str, Any],
    protocol_result: Mapping[str, Any],
    model_result: Mapping[str, Any],
) -> Dict[str, Any]:
    root_causes = []
    domains = tuple(anomaly_correlation.get("fault_domains") or ())
    if "baseline_drift" in domains:
        root_causes.append({"cause": "baseline_drift", "confidence": 0.78})
    if "protocol_contract" in domains:
        root_causes.append({"cause": "protocol_contract_drift", "confidence": 0.76})
    if "model_asset" in domains:
        root_causes.append({"cause": "model_asset_health_issue", "confidence": 0.74})
    if "dependency" in domains:
        root_causes.append({"cause": "dependency_unavailable", "confidence": 0.8})
    if "trace_replay" in domains:
        root_causes.append(
            {"cause": "trace_replay_contract_missing", "confidence": 0.72}
        )
    if not root_causes:
        root_causes.append({"cause": "insufficient_signals", "confidence": 0.45})

    return {
        "schema_version": "system_maintenance_root_cause_candidate_v1",
        "primary_capability_candidate": capability_locator.get(
            "primary_capability_candidate"
        ),
        "secondary_capability_candidates": tuple(
            capability_locator.get("secondary_capability_candidates") or ()
        ),
        "suspected_internal_component": capability_locator.get(
            "suspected_internal_component"
        ),
        "fault_domain": capability_locator.get("fault_domain"),
        "confidence": capability_locator.get("confidence"),
        "root_cause_candidates": tuple(root_causes),
        **not_fact(),
    }
