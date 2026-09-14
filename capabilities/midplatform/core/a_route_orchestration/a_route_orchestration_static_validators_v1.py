from __future__ import annotations

from typing import Iterable

from .a_route_orchestration_core_types_v1 import (
    ARouteHandoffRecordV1,
    ARouteNegativeGuardsV1,
    ARouteStageResultV1,
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
