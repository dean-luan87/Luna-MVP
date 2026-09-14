from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


READ_STATUS_REGISTRY_V1: Tuple[str, ...] = (
    "read_ready",
    "partial_projection",
    "insufficient_state",
    "stale_state",
    "state_unavailable",
    "query_rejected",
)


@dataclass(frozen=True)
class FieldStateReadQueryV1:
    query_id: str
    requester_ref: str
    query_scope: str
    field_state_ref: str | None
    snapshot_ref: str | None
    task_ref: str | None
    scene_ref: str | None
    object_ref: str | None
    temporal_scope: Dict[str, Any] | None
    required_fields: Tuple[str, ...]
    trace_ref: str
    replay_key: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FieldStateReadResultV1:
    query_id: str
    read_status: str
    projection: Dict[str, Any]
    state_version: str
    source_state_ref: str
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    replay_key: str
    stale_reason: str = ""
    insufficiency_reason: str = ""
    rejection_reason: str = ""
    boundary_flags: Dict[str, bool] = field(default_factory=dict)
    module_status: str = "completed_candidate"
    runtime_executed: bool = False


def get_default_boundary_flags_v1() -> Dict[str, bool]:
    return {
        "read_only": True,
        "candidate_only": True,
        "state_mutation_executed": False,
        "event_reduction_executed": False,
        "fact_admission_executed": False,
        "evidence_fabrication_executed": False,
        "model_execution_executed": False,
        "action_execution_executed": False,
        "runtime_loop_executed": False,
        "real_state_store_connected": False,
    }
