from __future__ import annotations

from typing import Any, Dict, Mapping


def build_system_maintenance_diagnostics_v1(
    input_candidate: Mapping[str, Any],
    module_status: str,
    capability_locator: Mapping[str, Any],
    anomaly_correlation: Mapping[str, Any],
    baseline_calibration: Mapping[str, Any],
    protocol_result: Mapping[str, Any],
    model_result: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": "system_maintenance_diagnostics_v1",
        "maintenance_request_id": input_candidate.get("maintenance_request_id"),
        "anomaly_type": input_candidate.get("anomaly_type"),
        "module_status": module_status,
        "primary_capability_candidate": capability_locator.get(
            "primary_capability_candidate"
        ),
        "fault_domains": tuple(anomaly_correlation.get("fault_domains") or ()),
        "baseline_calibration_result": baseline_calibration.get(
            "baseline_calibration_result"
        ),
        "protocol_check_executed": bool(
            (protocol_result.get("protocol_drift_result") or {}).get(
                "protocol_check_executed", False
            )
        ),
        "model_check_executed": bool(
            (model_result.get("model_asset_result") or {}).get(
                "model_check_executed", False
            )
        ),
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }
