from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


QUERY_SCOPE_REGISTRY_V1: Tuple[str, ...] = (
    "field_state",
    "task_scope",
    "scene_scope",
    "object_scope",
    "temporal_scope",
)

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
class FieldStateReadProjectionCandidateV1:
    source_state_ref: str
    state_version: str
    projection: Dict[str, Any]
    available_fields: Tuple[str, ...]
    missing_fields: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    temporal_status: str
    trace_ref: str
    replay_key: str


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
        "state_mutation": False,
        "event_reduction": False,
        "fact_admission": False,
        "evidence_fabrication": False,
        "real_model_execution": False,
        "action_execution": False,
        "runtime_loop": False,
        "real_state_store_connected": False,
        "candidate_only": True,
    }
