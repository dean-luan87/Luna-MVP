from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_types_v1 import (
    MODULE_SCHEMA_VERSION,
    SUPPORTED_ANOMALY_TYPES,
    SUPPORTED_RUNTIME_MODES,
    not_fact,
)


def adapt_system_maintenance_input_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    data = dict(payload)
    anomaly_type = str(data.get("anomaly_type") or "").strip()
    runtime_mode = str(data.get("runtime_mode") or "CALIBRATION").strip()
    if runtime_mode not in SUPPORTED_RUNTIME_MODES:
        runtime_mode = "CALIBRATION"
    return {
        "schema_version": MODULE_SCHEMA_VERSION,
        "maintenance_request_id": str(data.get("maintenance_request_id") or "").strip(),
        "source_capability_id": str(data.get("source_capability_id") or "").strip(),
        "source_module_version": str(data.get("source_module_version") or "").strip(),
        "anomaly_type": anomaly_type,
        "anomaly_type_supported": anomaly_type in SUPPORTED_ANOMALY_TYPES,
        "observed_status": str(data.get("observed_status") or "").strip(),
        "expected_status": str(data.get("expected_status") or "").strip(),
        "diagnostics": dict(data.get("diagnostics") or {}),
        "trace_ref": str(data.get("trace_ref") or "").strip(),
        "replay_key": str(data.get("replay_key") or "").strip(),
        "manifest_ref": str(data.get("manifest_ref") or "").strip(),
        "baseline_ref": str(data.get("baseline_ref") or "").strip(),
        "protocol_refs": tuple(data.get("protocol_refs") or ()),
        "model_asset_refs": tuple(data.get("model_asset_refs") or ()),
        "dependency_refs": tuple(data.get("dependency_refs") or ()),
        "timestamp": str(data.get("timestamp") or "").strip(),
        "runtime_mode": runtime_mode,
        "baseline_load_allowed": runtime_mode in {"CALIBRATION", "REBASELINE"},
        "full_calibration_allowed": runtime_mode == "CALIBRATION",
        "behavior_comparison_allowed": runtime_mode in {"CALIBRATION", "REBASELINE"},
        "protocol_drift_check_allowed": runtime_mode in {"CALIBRATION", "REBASELINE"},
        "model_asset_check_allowed": runtime_mode in {"CALIBRATION", "REBASELINE"},
        "rebaseline_candidate_allowed": runtime_mode == "REBASELINE",
        "rebaseline_allowed": False,
        "automatic_rebaseline_execution": False,
        "candidate_only": True,
        **not_fact(),
    }
