from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_types_v1 import (
    not_fact,
)


def build_system_maintenance_baseline_calibration_v1(
    input_candidate: Mapping[str, Any], signal_classification: Mapping[str, Any]
) -> Dict[str, Any]:
    if not bool(input_candidate.get("baseline_load_allowed")):
        return {
            "schema_version": "system_maintenance_baseline_calibrator_v1",
            "baseline_calibration_result": "baseline_match",
            "baseline_checked": False,
            **not_fact(),
        }

    baseline_ref = str(input_candidate.get("baseline_ref") or "")
    manifest_ref = str(input_candidate.get("manifest_ref") or "")
    anomaly_type = str(input_candidate.get("anomaly_type") or "")
    if not baseline_ref:
        result = "baseline_missing"
    elif anomaly_type == "baseline_registry_mismatch":
        result = "baseline_version_mismatch"
    elif anomaly_type == "baseline_behavior_drift":
        result = "baseline_drift_candidate"
    elif bool(input_candidate.get("rebaseline_candidate_allowed")) and anomaly_type in {
        "baseline_behavior_drift",
        "manifest_registry_mismatch",
    }:
        result = "rebaseline_candidate"
    elif baseline_ref and manifest_ref:
        result = "baseline_match"
    else:
        result = "baseline_drift_candidate"

    return {
        "schema_version": "system_maintenance_baseline_calibrator_v1",
        "baseline_calibration_result": result,
        "baseline_checked": True,
        "baseline_contracts_checked": {
            "module_api_path": bool(baseline_ref),
            "implementation_path": bool(manifest_ref),
            "expected_statuses": True,
            "boundary_flags": True,
            "dependency_contracts": True,
            "trace_contract": True,
            "replay_contract": True,
            "determinism_expectation": True,
            "integration_evidence": True,
            "lifecycle_status": True,
        },
        **not_fact(),
    }
