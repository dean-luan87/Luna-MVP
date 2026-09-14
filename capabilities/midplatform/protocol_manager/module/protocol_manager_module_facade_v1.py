from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.protocol_manager.module.protocol_manager_admission_v1 import (
    build_protocol_manager_admission_candidate_v1,
)
from capabilities.midplatform.protocol_manager.module.protocol_manager_boundary_checker_v1 import (
    build_protocol_manager_boundary_report_v1,
)
from capabilities.midplatform.protocol_manager.module.protocol_manager_change_control_v1 import (
    build_protocol_manager_change_control_candidate_v1,
)
from capabilities.midplatform.protocol_manager.module.protocol_manager_compatibility_checker_v1 import (
    build_protocol_manager_compatibility_candidate_v1,
)
from capabilities.midplatform.protocol_manager.module.protocol_manager_diagnostics_v1 import (
    build_protocol_manager_diagnostics_v1,
)
from capabilities.midplatform.protocol_manager.module.protocol_manager_error_namespace_governance_v1 import (
    build_protocol_manager_error_namespace_report_v1,
)
from capabilities.midplatform.protocol_manager.module.protocol_manager_impact_analysis_v1 import (
    build_protocol_manager_impact_analysis_candidate_v1,
)
from capabilities.midplatform.protocol_manager.module.protocol_manager_lifecycle_v1 import (
    build_protocol_manager_lifecycle_candidate_v1,
)
from capabilities.midplatform.protocol_manager.module.protocol_manager_module_input_adapter_v1 import (
    adapt_protocol_manager_input_v1,
)
from capabilities.midplatform.protocol_manager.module.protocol_manager_module_output_builder_v1 import (
    build_protocol_manager_result_summary_v1,
    resolve_protocol_manager_module_status_v1,
)
from capabilities.midplatform.protocol_manager.module.protocol_manager_registry_adapter_v1 import (
    run_protocol_manager_registry_lookup_v1,
)
from capabilities.midplatform.protocol_manager.module.protocol_manager_trace_replay_v1 import (
    build_protocol_manager_trace_replay_v1,
)
from capabilities.midplatform.protocol_manager.module.protocol_manager_version_resolver_v1 import (
    resolve_protocol_manager_version_candidate_v1,
)


def run_protocol_manager_module_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    input_candidate = adapt_protocol_manager_input_v1(payload)
    registry_lookup = run_protocol_manager_registry_lookup_v1(input_candidate)
    lifecycle_candidate = build_protocol_manager_lifecycle_candidate_v1(
        input_candidate, registry_lookup
    )
    version_candidate = resolve_protocol_manager_version_candidate_v1(
        input_candidate, registry_lookup
    )
    compatibility_candidate = build_protocol_manager_compatibility_candidate_v1(
        input_candidate, version_candidate
    )
    admission_candidate = build_protocol_manager_admission_candidate_v1(
        input_candidate, compatibility_candidate
    )
    change_control = build_protocol_manager_change_control_candidate_v1(
        input_candidate, compatibility_candidate
    )
    boundary_report = build_protocol_manager_boundary_report_v1(input_candidate)
    error_namespace_report = build_protocol_manager_error_namespace_report_v1(
        input_candidate, registry_lookup
    )
    impact_analysis = build_protocol_manager_impact_analysis_candidate_v1(
        input_candidate, compatibility_candidate
    )
    module_status = resolve_protocol_manager_module_status_v1(
        input_candidate,
        registry_lookup,
        lifecycle_candidate,
        compatibility_candidate,
        admission_candidate,
        change_control,
        boundary_report,
        error_namespace_report,
    )
    diagnostics = build_protocol_manager_diagnostics_v1(
        input_candidate,
        registry_lookup,
        compatibility_candidate,
        admission_candidate,
        change_control,
        boundary_report,
        error_namespace_report,
        impact_analysis,
    )
    trace_replay = build_protocol_manager_trace_replay_v1(
        input_candidate, module_status, compatibility_candidate
    )
    result_summary = build_protocol_manager_result_summary_v1(
        input_candidate=input_candidate,
        module_status=module_status,
        compatibility_candidate=compatibility_candidate,
        admission_candidate=admission_candidate,
        change_control=change_control,
        impact_analysis=impact_analysis,
    )

    return {
        "module_status": module_status,
        "input_candidate": input_candidate,
        "registry_lookup": registry_lookup,
        "lifecycle_candidate": lifecycle_candidate,
        "version_candidate": version_candidate,
        "compatibility_candidate": compatibility_candidate,
        "admission_candidate": admission_candidate,
        "change_control": change_control,
        "boundary_report": boundary_report,
        "error_namespace_report": error_namespace_report,
        "impact_analysis": impact_analysis,
        "diagnostics": diagnostics,
        "trace_ref": trace_replay["trace_ref"],
        "replay_key": trace_replay["replay_key"],
        "trace_replay": trace_replay,
        "result_summary": result_summary,
        "candidate_only": True,
        "protocol_asset_modified": False,
        "runtime_protocol_loaded": False,
        "dynamic_binding_executed": False,
        "database_write_executed": False,
        "state_mutation_executed": False,
        "fact_admission_executed": False,
        "action_execution_executed": False,
        "model_call_executed": False,
        "external_lookup_executed": False,
        "production_runtime_executed": False,
    }
