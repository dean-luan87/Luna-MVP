from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_types_v1 import (
    not_fact,
)


def build_system_maintenance_anomaly_correlation_v1(
    signal_classification: Mapping[str, Any],
    baseline_calibration: Mapping[str, Any],
    protocol_result: Mapping[str, Any],
    model_result: Mapping[str, Any],
    dependency_impact: Mapping[str, Any],
    diagnostic_aggregate: Mapping[str, Any],
) -> Dict[str, Any]:
    domains = {str(signal_classification.get("fault_domain_hint") or "unknown")}
    baseline_result = str(
        baseline_calibration.get("baseline_calibration_result") or "baseline_match"
    )
    if baseline_result in {
        "baseline_drift_candidate",
        "baseline_version_mismatch",
        "baseline_missing",
        "rebaseline_candidate",
    }:
        domains.add("baseline_drift")
    proto = dict(protocol_result.get("protocol_drift_result") or {})
    if (
        bool(proto.get("migration_required"))
        or bool(proto.get("deprecation_conflict"))
        or not bool(proto.get("schema_compatible", True))
    ):
        domains.add("protocol_contract")
    model = dict(model_result.get("model_asset_result") or {})
    if str(model.get("result_status") or "") in {
        "model_asset_degraded",
        "model_asset_unavailable",
        "model_asset_mismatch",
        "model_asset_ownership_conflict",
        "model_fallback_candidate",
    }:
        domains.add("model_asset")
    dep = dict(dependency_impact.get("dependency_impact") or {})
    if bool(dep.get("dependency_unavailable", False)):
        domains.add("dependency")
    if not bool(diagnostic_aggregate.get("trace_present", True)) or not bool(
        diagnostic_aggregate.get("replay_present", True)
    ):
        domains.add("trace_replay")

    domains_sorted = tuple(sorted(domains))
    return {
        "schema_version": "system_maintenance_anomaly_correlator_v1",
        "fault_domains": domains_sorted,
        "multiple_fault_domains": len(domains_sorted) > 1,
        "supporting_signals": tuple(
            diagnostic_aggregate.get("supporting_signals") or ()
        ),
        "contradicting_signals": tuple(
            diagnostic_aggregate.get("contradicting_signals") or ()
        ),
        **not_fact(),
    }
