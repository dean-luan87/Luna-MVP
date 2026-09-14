"""Immutable result types for fixture-only CWR integration DryRun v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Mapping, Tuple


INTEGRATION_SCHEMA_VERSION_V1 = "luna.current_world_representation_integration.v1"


@dataclass(frozen=True)
class CurrentWorldRepresentationIntegrationDryRunResultV1:
    schema_version: str
    dryrun_id: str
    case_id: str
    case_name: str
    execution_scope: str
    runtime_executed: bool
    simulation_only: bool
    input_refs: Tuple[str, ...]
    admitted_event_ref: str
    reducer_output_ref: str
    field_state_ref: str
    state_version_refs: Tuple[str, ...]
    transition_record_refs: Tuple[str, ...]
    history_projection_ref: str
    snapshot_ref: str
    read_model_result_ref: str
    context_refs: Tuple[str, ...]
    active_context_ref: str | None
    envelope_ref: str
    reference_chain_valid: bool
    version_chain_valid: bool
    mutation_authority_valid: bool
    readonly_boundary_valid: bool
    unknown_preservation_valid: bool
    context_isolation_valid: bool
    cognitive_writeback_absent: bool
    analysis_boundary_admission: bool
    failure_codes: Tuple[str, ...]
    warning_codes: Tuple[str, ...]
    provenance: Mapping[str, Any]
    trace: str


def to_jsonable_v1(value: Any) -> Any:
    """Convert fixed DryRun values to JSON without changing their contents."""

    if is_dataclass(value):
        return to_jsonable_v1(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): to_jsonable_v1(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [to_jsonable_v1(item) for item in value]
    if isinstance(value, list):
        return [to_jsonable_v1(item) for item in value]
    return value
