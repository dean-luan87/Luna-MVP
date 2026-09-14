from __future__ import annotations

from typing import Dict, Tuple


FIELD_STATE_REDUCER_MODULE_API_CONTRACT_V1: Dict[str, object] = {
    "version": "1.0",
    "name": "Field State Reducer Module API Contract",
    "input": [
        "admitted_events",
        "existing_state_snapshot",
        "governed_snapshots",
        "version_snapshots",
    ],
    "output": [
        "field_state_candidate",
        "projection_candidate",
        "trace",
        "replay_key",
        "diagnostics",
    ],
    "owned_capabilities": [
        "event_to_candidate_reduction_orchestration",
        "candidate_build",
        "transition_legality_judgement",
        "conflict_overlay_boundary_handling",
    ],
    "not_owned_capabilities": [
        "fact_admission",
        "real_persistence",
        "action_execution",
        "provider_call",
        "model_call",
        "ui_publish",
        "read_model_store_write",
    ],
    "candidate_only": True,
    "fact_admitted": False,
    "state_store_write_executed": False,
    "action_trigger_executed": False,
    "runtime_execution": False,
}


def get_field_state_reducer_module_api_contract_v1() -> Dict[str, object]:
    return dict(FIELD_STATE_REDUCER_MODULE_API_CONTRACT_V1)
