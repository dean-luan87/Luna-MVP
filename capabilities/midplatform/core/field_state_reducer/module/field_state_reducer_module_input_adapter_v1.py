from __future__ import annotations

from collections.abc import Mapping
from typing import Dict, List, Tuple

from .field_state_reducer_module_types_v1 import (
    AdaptedModuleInputV1,
    FieldStateReducerModuleRequestV1,
)


_REQUIRED_VERSION_KEYS = {
    "policy_registry_version",
    "eligibility_matrix_version",
    "precedence_matrix_version",
    "composition_contract_version",
    "replay_contract_version",
    "evaluation_contract_version",
    "reduction_contract_version",
}


def adapt_module_input_v1(
    request: FieldStateReducerModuleRequestV1,
) -> Tuple[AdaptedModuleInputV1 | None, Tuple[str, ...], Tuple[str, ...]]:
    missing_inputs: List[str] = []
    rejection_reasons: List[str] = []

    if not isinstance(request, FieldStateReducerModuleRequestV1):
        return None, ("request_type_invalid",), ()

    if not isinstance(request.admitted_events, tuple):
        rejection_reasons.append("admitted_events_must_be_tuple")
    elif any(not isinstance(event, Mapping) for event in request.admitted_events):
        rejection_reasons.append("admitted_events_members_must_be_mapping")
    for name in (
        "existing_state_snapshot", "temporal_snapshot", "policy_registry_snapshot",
        "evaluation_contract_snapshot", "selection_contract_snapshot",
        "reduction_contract_snapshot", "conflict_snapshot", "overlay_snapshot",
        "owner_correction_snapshot", "provenance_snapshot", "version_snapshots",
    ):
        if not isinstance(getattr(request, name), Mapping):
            rejection_reasons.append(f"{name}_must_be_mapping")
    if isinstance(request.version_snapshots, Mapping) and any(
        not isinstance(key, str) or not key.strip() or not isinstance(value, str) or not value.strip()
        for key, value in request.version_snapshots.items()
    ):
        rejection_reasons.append("version_snapshots_members_invalid")

    if not request.reducer_request_id:
        missing_inputs.append("reducer_request_id")
    if not request.reducer_run_id:
        missing_inputs.append("reducer_run_id")
    if not request.field_id:
        missing_inputs.append("field_id")
    if not request.requested_state_type:
        missing_inputs.append("requested_state_type")

    if request.direct_mutation_requested:
        rejection_reasons.append("direct_mutation_request_forbidden")
    if request.runtime_request:
        rejection_reasons.append("runtime_request_forbidden")
    if request.provider_request:
        rejection_reasons.append("provider_request_forbidden")
    if request.model_request:
        rejection_reasons.append("model_request_forbidden")
    if request.external_lookup_request:
        rejection_reasons.append("external_lookup_request_forbidden")

    # Snapshot completeness check.
    if not request.policy_registry_snapshot:
        missing_inputs.append("policy_registry_snapshot")
    if not request.evaluation_contract_snapshot:
        missing_inputs.append("evaluation_contract_snapshot")
    if not request.selection_contract_snapshot:
        missing_inputs.append("selection_contract_snapshot")
    if not request.reduction_contract_snapshot:
        missing_inputs.append("reduction_contract_snapshot")

    # Admitted event and stable event id checks.
    admitted_event_refs: List[str] = []
    for idx, event in enumerate(request.admitted_events if isinstance(request.admitted_events, tuple) else ()):
        if not isinstance(event, Mapping):
            continue
        event_id = event.get("event_id", "")
        if not isinstance(event_id, str):
            rejection_reasons.append(f"admitted_events[{idx}].event_id_invalid_type")
            continue
        if not event_id:
            missing_inputs.append(f"admitted_events[{idx}].event_id")
            continue
        admitted_event_refs.append(event_id)
    if len(set(admitted_event_refs)) != len(admitted_event_refs):
        rejection_reasons.append("stable_event_id_duplicate")

    # Version completeness check.
    for key in _REQUIRED_VERSION_KEYS:
        if not isinstance(request.version_snapshots, Mapping) or not isinstance(request.version_snapshots.get(key, ""), str) or not request.version_snapshots.get(key, "").strip():
            missing_inputs.append(f"version_snapshots.{key}")

    if missing_inputs or rejection_reasons:
        return (
            None,
            tuple(dict.fromkeys(missing_inputs)),
            tuple(dict.fromkeys(rejection_reasons)),
        )

    adapted = AdaptedModuleInputV1(
        reducer_request_id=request.reducer_request_id,
        reducer_run_id=request.reducer_run_id,
        field_id=request.field_id,
        state_type=request.requested_state_type,
        admitted_events=tuple(request.admitted_events),
        admitted_event_refs=tuple(admitted_event_refs),
        existing_state_snapshot=dict(request.existing_state_snapshot),
        temporal_snapshot=dict(request.temporal_snapshot),
        conflict_snapshot=dict(request.conflict_snapshot),
        overlay_snapshot=dict(request.overlay_snapshot),
        owner_correction_snapshot=dict(request.owner_correction_snapshot),
        provenance_snapshot=dict(request.provenance_snapshot),
        version_snapshots=dict(request.version_snapshots),
    )
    return adapted, tuple(), tuple()
