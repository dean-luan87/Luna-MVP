from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple


MODULE_STATUS_REGISTRY_V1: Tuple[str, ...] = (
    "completed_candidate",
    "no_state_change",
    "unresolved",
    "conflicted",
    "temporally_invalid",
    "insufficient_evidence",
    "governance_review_required",
    "rejected_input",
    "internal_error",
)


@dataclass(frozen=True)
class FieldStateReducerModuleRequestV1:
    reducer_request_id: str
    reducer_run_id: str
    field_id: str
    requested_state_type: str
    admitted_events: Tuple[Dict[str, Any], ...]
    existing_state_snapshot: Dict[str, Any]
    temporal_snapshot: Dict[str, Any]
    policy_registry_snapshot: Dict[str, Any]
    evaluation_contract_snapshot: Dict[str, Any]
    selection_contract_snapshot: Dict[str, Any]
    reduction_contract_snapshot: Dict[str, Any]
    conflict_snapshot: Dict[str, Any]
    overlay_snapshot: Dict[str, Any]
    owner_correction_snapshot: Dict[str, Any]
    provenance_snapshot: Dict[str, Any]
    version_snapshots: Dict[str, str]
    direct_mutation_requested: bool = False
    runtime_request: bool = False
    provider_request: bool = False
    model_request: bool = False
    external_lookup_request: bool = False


@dataclass(frozen=True)
class AdaptedModuleInputV1:
    reducer_request_id: str
    reducer_run_id: str
    field_id: str
    state_type: str
    admitted_events: Tuple[Dict[str, Any], ...]
    admitted_event_refs: Tuple[str, ...]
    existing_state_snapshot: Dict[str, Any]
    temporal_snapshot: Dict[str, Any]
    conflict_snapshot: Dict[str, Any]
    overlay_snapshot: Dict[str, Any]
    owner_correction_snapshot: Dict[str, Any]
    provenance_snapshot: Dict[str, Any]
    version_snapshots: Dict[str, str]


@dataclass(frozen=True)
class FieldStateReducerModuleResultV1:
    reducer_request_id: str
    reducer_run_id: str
    field_id: str
    state_type: str
    module_status: str
    evaluation_summary: Dict[str, Any]
    selection_summary: Dict[str, Any]
    reduction_summary: Dict[str, Any]
    transition_summary: Dict[str, Any]
    field_state_candidate: Dict[str, Any] | None
    read_model_projection_candidate: Dict[str, Any] | None
    unresolved_items: Tuple[str, ...]
    rejection_reasons: Tuple[str, ...]
    diagnostics: Dict[str, Any]
    trace_ref: str
    replay_key: str
    contract_versions: Dict[str, str]
    candidate_only: bool = True
    fact_admitted: bool = False
    state_store_write_executed: bool = False
    action_trigger_executed: bool = False
    runtime_execution: bool = False
