from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_anomaly_correlator_v1 import (
    build_system_maintenance_anomaly_correlation_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_baseline_calibrator_v1 import (
    build_system_maintenance_baseline_calibration_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_capability_locator_v1 import (
    build_system_maintenance_capability_locator_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_dependency_impact_v1 import (
    build_system_maintenance_dependency_impact_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_diagnostic_aggregator_v1 import (
    build_system_maintenance_diagnostic_aggregation_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_diagnostics_v1 import (
    build_system_maintenance_diagnostics_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_input_adapter_v1 import (
    adapt_system_maintenance_input_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_model_asset_adapter_v1 import (
    build_system_maintenance_model_asset_result_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_module_output_builder_v1 import (
    build_system_maintenance_module_output_v1,
    resolve_system_maintenance_module_status_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_protocol_drift_adapter_v1 import (
    build_system_maintenance_protocol_drift_result_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_remediation_candidate_v1 import (
    build_system_maintenance_remediation_candidates_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_root_cause_candidate_v1 import (
    build_system_maintenance_root_cause_candidates_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_signal_classifier_v1 import (
    build_system_maintenance_signal_classification_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_task_handoff_v1 import (
    build_system_maintenance_task_handoff_candidate_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_trace_replay_v1 import (
    build_system_maintenance_trace_replay_v1,
)


def run_system_maintenance_manager_module_v1(
    payload: Mapping[str, Any],
) -> Dict[str, Any]:
    try:
        input_candidate = adapt_system_maintenance_input_v1(payload)
        signal_classification = build_system_maintenance_signal_classification_v1(
            input_candidate
        )
        capability_locator = build_system_maintenance_capability_locator_v1(
            input_candidate,
            signal_classification,
        )
        diagnostic_aggregate = build_system_maintenance_diagnostic_aggregation_v1(
            input_candidate
        )
        baseline_calibration = build_system_maintenance_baseline_calibration_v1(
            input_candidate,
            signal_classification,
        )
        protocol_result = build_system_maintenance_protocol_drift_result_v1(
            input_candidate
        )
        model_result = build_system_maintenance_model_asset_result_v1(input_candidate)
        dependency_impact = build_system_maintenance_dependency_impact_v1(
            input_candidate
        )
        anomaly_correlation = build_system_maintenance_anomaly_correlation_v1(
            signal_classification,
            baseline_calibration,
            protocol_result,
            model_result,
            dependency_impact,
            diagnostic_aggregate,
        )
        root_cause = build_system_maintenance_root_cause_candidates_v1(
            capability_locator,
            anomaly_correlation,
            baseline_calibration,
            protocol_result,
            model_result,
        )
        remediation = build_system_maintenance_remediation_candidates_v1(
            input_candidate,
            anomaly_correlation,
            root_cause,
        )
        task_handoff = build_system_maintenance_task_handoff_candidate_v1(
            input_candidate,
            root_cause,
            remediation,
        )
        module_status = resolve_system_maintenance_module_status_v1(
            input_candidate,
            signal_classification,
            anomaly_correlation,
            baseline_calibration,
            protocol_result,
            model_result,
            dependency_impact,
        )
        trace_replay = build_system_maintenance_trace_replay_v1(
            input_candidate,
            module_status,
            str(root_cause.get("primary_capability_candidate") or ""),
        )
        diagnostics = build_system_maintenance_diagnostics_v1(
            input_candidate,
            module_status,
            capability_locator,
            anomaly_correlation,
            baseline_calibration,
            protocol_result,
            model_result,
        )
        output = build_system_maintenance_module_output_v1(
            input_candidate,
            module_status,
            root_cause,
            protocol_result,
            model_result,
            baseline_calibration,
            dependency_impact,
            remediation,
            task_handoff,
            diagnostics,
            str(trace_replay.get("trace_ref") or ""),
            str(trace_replay.get("replay_key") or ""),
        )
        output.update(
            {
                "signal_classification": signal_classification,
                "capability_locator": capability_locator,
                "diagnostic_aggregate": diagnostic_aggregate,
                "anomaly_correlation": anomaly_correlation,
                "trace_replay": trace_replay,
                "unhandled_exception": False,
            }
        )
        return output
    except Exception:  # noqa: BLE001
        return {
            "capability_id": "luna.system_maintenance_manager",
            "maintenance_request_id": "",
            "maintenance_status": "internal_error",
            "primary_capability_candidate": "",
            "secondary_capability_candidates": (),
            "fault_domain": "unknown",
            "root_cause_candidates": (),
            "protocol_drift_result": {},
            "model_asset_result": {},
            "baseline_calibration_result": "baseline_match",
            "dependency_impact": {},
            "remediation_candidates": (),
            "task_handoff_candidate": None,
            "diagnostics": {
                "schema_version": "system_maintenance_diagnostics_v1",
                "module_status": "internal_error",
            },
            "trace_ref": "",
            "replay_key": "",
            "boundary_flags": {},
            "unhandled_exception": True,
        }
