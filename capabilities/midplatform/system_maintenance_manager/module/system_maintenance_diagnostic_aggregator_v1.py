from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_types_v1 import (
    not_fact,
)


def build_system_maintenance_diagnostic_aggregation_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    diagnostics = dict(input_candidate.get("diagnostics") or {})
    trace_present = bool(input_candidate.get("trace_ref"))
    replay_present = bool(input_candidate.get("replay_key"))
    return {
        "schema_version": "system_maintenance_diagnostic_aggregator_v1",
        "diagnostics_aggregate": diagnostics,
        "trace_present": trace_present,
        "replay_present": replay_present,
        "determinism_drift_hint": bool(diagnostics.get("determinism_drift", False)),
        "supporting_signals": tuple(diagnostics.get("supporting_signals") or ()),
        "contradicting_signals": tuple(diagnostics.get("contradicting_signals") or ()),
        **not_fact(),
    }
