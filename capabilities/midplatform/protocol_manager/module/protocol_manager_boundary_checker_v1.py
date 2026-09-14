from __future__ import annotations

from typing import Any, Dict, Mapping


def build_protocol_manager_boundary_report_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    boundary_request_flags = {
        "requested_protocol_asset_modify": bool(
            input_candidate.get("change_set", {}).get(
                "modify_protocol_asset_now", False
            )
        ),
        "requested_runtime_protocol_load": bool(
            input_candidate.get("change_set", {}).get(
                "runtime_protocol_load_now", False
            )
        ),
        "requested_dynamic_binding": bool(
            input_candidate.get("change_set", {}).get("dynamic_binding_now", False)
        ),
    }
    boundary_violation = any(boundary_request_flags.values())

    return {
        "schema_version": "protocol_manager_boundary_checker_v1",
        "boundary_violation": boundary_violation,
        "violation_reasons": [k for k, v in boundary_request_flags.items() if v],
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
        "fact_status": "not_fact",
        "write_allowed": False,
    }
