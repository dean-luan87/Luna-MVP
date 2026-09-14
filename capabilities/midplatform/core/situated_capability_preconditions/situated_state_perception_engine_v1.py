"""Derive situated condition candidates from existing observation-state inputs."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Mapping, Tuple

from .situated_capability_precondition_types_v1 import (
    SituatedCapabilityStateV1,
    SituatedConditionStateCandidateV1,
)
from .situated_state_perception_types_v1 import (
    SituatedStatePerceptionRequestV1,
    SituatedStatePerceptionResultV1,
)


EXECUTION_MODE = "CONTROLLED_SITUATED_STATE_PERCEPTION"
OWNER = "Capability Admission / Capability Governance"


def _ref(prefix: str, request: SituatedStatePerceptionRequestV1) -> str:
    return f"{prefix}:{request.case_id}:{request.state_id}"


def _status(value: str, satisfied: Tuple[str, ...], unsatisfied: Tuple[str, ...]) -> str:
    if value in satisfied:
        return "SATISFIED"
    if value in unsatisfied:
        return "UNSATISFIED"
    return "UNKNOWN"


def _condition_statuses(request: SituatedStatePerceptionRequestV1) -> Tuple[Tuple[str, str, str], ...]:
    relative = request.relative_state
    stable_value = relative.stability_candidate
    if stable_value == "UNKNOWN" and relative.relative_motion_candidate == "LOW":
        stable_value = "STABLE"
    elif stable_value == "UNKNOWN" and relative.relative_motion_candidate == "HIGH":
        stable_value = "UNSTABLE"
    return (
        (
            "condition:target-visible:v1",
            _status(relative.target_visibility_candidate, ("VISIBLE",), ("NOT_VISIBLE", "PARTIAL")),
            f"target visibility candidate={relative.target_visibility_candidate}",
        ),
        (
            "condition:target-complete:v1",
            _status(relative.target_completeness_candidate, ("COMPLETE",), ("INCOMPLETE", "PARTIAL", "INSUFFICIENT")),
            f"target completeness candidate={relative.target_completeness_candidate}",
        ),
        (
            "condition:target-scale-adequate:v1",
            _status(relative.target_scale_candidate, ("ADEQUATE",), ("SMALL", "INADEQUATE")),
            f"target scale candidate={relative.target_scale_candidate}",
        ),
        (
            "condition:stable-relation:v1",
            _status(stable_value, ("STABLE",), ("UNSTABLE",)),
            f"relative stability candidate={relative.stability_candidate}; motion candidate={relative.relative_motion_candidate}",
        ),
    )


def derive(request: SituatedStatePerceptionRequestV1) -> SituatedStatePerceptionResultV1:
    """Materialize condition candidates without invoking any provider."""

    common_sources = tuple(dict.fromkeys(
        (
            *request.source_refs,
            *request.self_state.source_refs,
            *request.relative_state.source_refs,
            *request.field_state_refs,
            *request.target_refs,
            *request.evidence_refs,
        )
    ))
    common_provenance = tuple(dict.fromkeys(
        (*request.provenance_refs, *request.self_state.provenance_refs, *request.relative_state.provenance_refs)
    ))
    candidates = tuple(
        SituatedConditionStateCandidateV1(
            condition_ref=condition_ref,
            status=status,
            self_state_refs=(request.self_state.state_ref,),
            field_state_refs=request.field_state_refs,
            target_refs=request.target_refs or (request.relative_state.target_ref,),
            relation_refs=(request.relative_state.relative_state_ref,),
            evidence_refs=request.evidence_refs,
            temporal_ref=request.temporal_ref,
            reason=reason,
            source_refs=tuple(dict.fromkeys((*common_sources, request.relative_state.relative_state_ref))),
            provenance_refs=tuple(dict.fromkeys((*common_provenance, f"provenance:condition:{condition_ref}"))),
        )
        for condition_ref, status, reason in _condition_statuses(request)
    )
    satisfied = tuple(item.condition_ref for item in candidates if item.status == "SATISFIED")
    state = SituatedCapabilityStateV1(
        situated_state_ref=request.situated_state_ref,
        capability_requirement_ref=request.capability_requirement_ref,
        self_state_refs=(request.self_state.state_ref,),
        field_state_refs=request.field_state_refs,
        target_refs=request.target_refs or (request.relative_state.target_ref,),
        relation_refs=(request.relative_state.relative_state_ref,),
        temporal_ref=request.temporal_ref,
        satisfied_condition_refs=satisfied,
        condition_state_refs=tuple(f"condition-state:{request.case_id}:{request.state_id}:{item.condition_ref}" for item in candidates),
        relation_stability_candidate=request.relative_state.stability_candidate,
        source_refs=common_sources,
        provenance_refs=common_provenance,
        condition_state_candidates=candidates,
    )
    trace = tuple(dict.fromkeys((*common_provenance, _ref("trace:situated-state-perception", request))))
    return SituatedStatePerceptionResultV1(
        case_id=request.case_id,
        state_id=request.state_id,
        cycle_index=request.cycle_index,
        request=request,
        condition_candidates=candidates,
        situated_state=state,
        trace_refs=trace,
        provenance_refs=trace,
        behavior={
            "provider_invocation": False,
            "model_invocation": False,
            "decision_execution": False,
            "task_execution": False,
            "device_control": False,
            "action_execution": False,
            "field_mutation": False,
            "world_truth_declared": False,
            "scenario_id_semantic_driver": False,
            "cycle_index_semantic_driver": False,
        },
    )


def jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


__all__ = ["EXECUTION_MODE", "OWNER", "derive", "jsonable"]
