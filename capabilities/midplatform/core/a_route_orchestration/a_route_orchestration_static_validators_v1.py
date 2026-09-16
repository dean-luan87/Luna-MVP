from __future__ import annotations

from typing import Iterable, Tuple

from .a_route_orchestration_core_types_v1 import (
    ARouteHandoffRecordV1,
    ARouteNegativeGuardsV1,
    ARouteStageResultV1,
    ARouteIngressRefsV1,
    ARouteOrchestrationRequestV1,
    HANDOFF_STATUSES,
    LIFECYCLE_STAGES,
)
from .a_route_orchestration_trace_types_v1 import ARouteTraceV1
from capabilities.midplatform.core.execution_mode_v1 import (
    CONTROLLED_REPLAY_RUNTIME,
    LIVE_RUNTIME,
    SYNTHETIC_CONTROLLED,
)


def validate_stage_result(stage: ARouteStageResultV1) -> bool:
    return bool(
        stage.stage_id
        and stage.producer_owner
        and stage.consumer_owner
        and stage.handoff_contract_ref
        and stage.trace_ref
        and stage.schema_version
        and stage.contract_version
        and stage.status
    )


def validate_handoff(handoff: ARouteHandoffRecordV1) -> bool:
    return (
        handoff.status in HANDOFF_STATUSES
        and bool(handoff.handoff_id)
        and bool(handoff.contract_ref)
        and bool(handoff.adapter_ref)
        and bool(handoff.trace_ref)
        and (not handoff.runtime_handoff_ready or handoff.status == "RUNTIME_HANDOFF_READY")
    )


def validate_trace(trace: ARouteTraceV1, stage_results: Iterable[ARouteStageResultV1]) -> bool:
    stages = tuple(stage_results)
    return bool(
        trace.root_cycle_trace_id
        and trace.cycle_id
        and trace.candidate_only
        and trace.authority_granted is False
        and len(trace.stage_trace_refs) == len(stages)
        and trace.reverse_lookup_path
        and all(item.trace_ref in trace.stage_trace_refs for item in stages)
    )


def validate_negative_guards(guards: ARouteNegativeGuardsV1) -> bool:
    return all(
        value is False
        for name, value in vars(guards).items()
        if name not in {"synthetic_only", "controlled_integration_only", "execution_mode"}
    ) and guards.controlled_integration_only and (
        (guards.execution_mode == SYNTHETIC_CONTROLLED and guards.synthetic_only)
        or (guards.execution_mode == CONTROLLED_REPLAY_RUNTIME and not guards.synthetic_only)
        or (guards.execution_mode == LIVE_RUNTIME and not guards.synthetic_only)
    )


def validate_lifecycle_state(state: str) -> bool:
    return state in LIFECYCLE_STAGES or state in {"STOPPED", "DEFERRED", "FAILED", "RECONSIDERING", "SUSPENDED"}


def validate_request_shape(request: ARouteOrchestrationRequestV1) -> Tuple[str, ...]:
    """Validate transport references before orchestration normalization."""
    if not isinstance(request, ARouteOrchestrationRequestV1):
        return ("request_type_invalid",)
    errors = []
    if not isinstance(request.ingress, ARouteIngressRefsV1):
        return ("ingress_shape_invalid",)
    for name in ("observation_refs", "perception_refs", "user_input_refs", "field_refs", "relation_refs"):
        value = getattr(request.ingress, name)
        if not isinstance(value, (list, tuple)) or any(not isinstance(item, str) or not item.strip() for item in value):
            errors.append(f"ingress.{name}_must_contain_strings")
    for name in ("role_refs", "task_refs", "goal_refs", "concern_refs", "information_need_refs"):
        value = getattr(request, name)
        if not isinstance(value, (list, tuple)) or any(not isinstance(item, str) or not item.strip() for item in value):
            errors.append(f"{name}_must_contain_strings")
    if not isinstance(request.relation_interpretation_candidates, (list, tuple)):
        errors.append("relation_interpretation_candidates_invalid_shape")
    if not isinstance(request.semantic_reference_values, (list, tuple)):
        errors.append("semantic_reference_values_invalid_shape")
    if not isinstance(request.scenario_id, str) or not request.scenario_id.strip():
        errors.append("scenario_id_invalid_field_type")
    return tuple(dict.fromkeys(errors))
