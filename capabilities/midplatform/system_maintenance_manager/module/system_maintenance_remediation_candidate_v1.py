from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_types_v1 import (
    not_fact,
)


def build_system_maintenance_remediation_candidates_v1(
    input_candidate: Mapping[str, Any],
    anomaly_correlation: Mapping[str, Any],
    root_cause: Mapping[str, Any],
) -> Dict[str, Any]:
    anomaly = str(input_candidate.get("anomaly_type") or "unknown_anomaly")
    domains = tuple(anomaly_correlation.get("fault_domains") or ())
    candidates = []
    if "protocol_contract" in domains:
        candidates.append("inspect_protocol")
        candidates.append("update_protocol_candidate")
    if "model_asset" in domains or anomaly.startswith("model_"):
        candidates.append("inspect_model_asset")
        candidates.append("replace_model_candidate")
    if "baseline_drift" in domains:
        candidates.append("rebaseline_candidate")
    if "dependency" in domains:
        candidates.append("dependency_recovery_candidate")
    if "module_logic" in domains or "status_reduction" in domains:
        candidates.append("inspect_module")
        candidates.append("repair_module_candidate")
    if "trace_replay" in domains or "permission_boundary" in domains:
        candidates.append("manual_review_required")
    if not candidates:
        candidates.append("manual_review_required")

    unique = tuple(dict.fromkeys(candidates))
    return {
        "schema_version": "system_maintenance_remediation_candidate_v1",
        "remediation_candidates": tuple(
            {
                "candidate_id": f"rem_{idx}_{input_candidate.get('maintenance_request_id')}",
                "maintenance_task_type": task_type,
                "candidate_only": True,
                **not_fact(),
            }
            for idx, task_type in enumerate(unique)
        ),
        **not_fact(),
    }
