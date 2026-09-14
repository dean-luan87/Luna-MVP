"""Controlled evaluation wrapper for Required Cognitive Condition formation."""

from __future__ import annotations

from dataclasses import asdict, replace
from typing import Any

from capabilities.midplatform.core.a_route_orchestration.a_route_information_need_formation_types_v1 import (
    ARouteInformationNeedFormationRequestV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_minimum_relevant_cognitive_view_types_v1 import (
    ARouteMinimumRelevantCognitiveViewRequestV1,
    AvailableCognitiveInformationItemV1,
    EXTERNAL_INFORMATION,
    SELF_INFORMATION,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_types_v1 import (
    ARouteRequiredCognitiveConditionFormationRequestV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)

from .fixtures_v1 import (
    SOURCE_MODE,
    build_negative_required_condition_requests_v1,
    build_required_condition_formation_cases_v1,
)


def _available_information() -> tuple[AvailableCognitiveInformationItemV1, ...]:
    return (
        AvailableCognitiveInformationItemV1(
            information_ref="self:governed:mobility:ready:v1",
            object_type=SELF_INFORMATION,
            information_kind="SITUATED_SELF_SIGNAL",
            support_condition_refs=("condition:seat:operator-access-required:v1",),
            source_refs=("source:self:controlled:v1",),
            provenance_refs=("provenance:self:controlled:v1",),
        ),
        AvailableCognitiveInformationItemV1(
            information_ref="external:seat:location:v1",
            object_type=EXTERNAL_INFORMATION,
            information_kind="FIELD_ENTITY_CANDIDATE_VIEW",
            support_condition_refs=("condition:seat:location-required:v1",),
            source_refs=("source:external:controlled:v1",),
            provenance_refs=("provenance:external:controlled:v1",),
        ),
        AvailableCognitiveInformationItemV1(
            information_ref="external:irrelevant:weather:v1",
            object_type=EXTERNAL_INFORMATION,
            information_kind="UNRELATED_EXTERNAL_SIGNAL",
            support_condition_refs=("condition:unrelated:v1",),
            source_refs=("source:external:irrelevant:v1",),
            provenance_refs=("provenance:external:irrelevant:v1",),
        ),
    )


def _world(case_id: str) -> CurrentWorldCandidateV1:
    return CurrentWorldCandidateV1(
        current_world_id=f"world:formed:{case_id}:v1",
        attention_refs=(),
        active_hypothesis_refs=(),
        alternative_hypothesis_refs=(),
        context_refs=("context:opaque:controlled:v1",),
        field_state_refs=("field:controlled:v1",),
        pcn_refs=(),
        intent_refs=("intent:governed:situated-navigation:v1",),
        observation_refs=(),
        uncertainty_refs=(),
        conflict_refs=(),
        temporal_refs=(),
        source_versions={"current_world": "current-world-candidate-v1"},
        world_state_kind_candidate="PARTIAL",
        world_stability_candidate="LOW",
        trace_ref=f"trace:world:formed:{case_id}",
        provenance_refs=(f"provenance:world:formed:{case_id}",),
    )


def _downstream(
    request: ARouteRequiredCognitiveConditionFormationRequestV1,
    active_refs: tuple[str, ...],
    case_id: str,
) -> dict[str, Any]:
    route = ARouteOrchestrationEngineV1()
    goal_context = replace(request.goal_context, success_condition_refs=())
    view = route.form_minimum_relevant_cognitive_view(
        ARouteMinimumRelevantCognitiveViewRequestV1(
            goal_context=goal_context,
            available_information=_available_information(),
            governed_objective_condition_refs=active_refs,
            intent_ref=request.intent_ref,
            concern_ref=request.concern_ref,
            context_ref=request.context_ref,
            field_ref=request.field_ref,
            role_refs=request.role_refs,
            current_world_ref=f"world:formed:{case_id}:v1",
            current_cognitive_state_ref="cognitive-state:controlled:v1",
        )
    )
    world = _world(case_id)
    need = route.form_information_need(
        ARouteInformationNeedFormationRequestV1(
            goal_context=goal_context,
            current_world=world,
            current_cognitive_coverage_refs=request.current_situation.current_cognitive_coverage_refs,
            intent_ref=request.intent_ref,
            concern_ref=request.concern_ref,
            context_ref=request.context_ref,
            field_ref=request.field_ref,
            role_refs=request.role_refs,
            governed_objective_condition_refs=active_refs,
            formation_trace_ref=f"trace:need:from-formed-conditions:{case_id}",
        )
    )
    return {
        "minimum_relevant_view": asdict(view),
        "information_need": asdict(need),
    }


class ARouteRequiredCognitiveConditionFormationEvaluationEngineV1:
    """Runs only controlled formation and downstream contract compatibility."""

    def run(self) -> dict[str, Any]:
        route = ARouteOrchestrationEngineV1()
        cases = []
        for case in build_required_condition_formation_cases_v1():
            result = route.form_required_cognitive_conditions(case.request)
            cases.append(
                {
                    "case_id": case.case_id,
                    "expected_active": list(case.expected_active),
                    "expected_satisfied": list(case.expected_satisfied),
                    "expected_status": case.expected_status,
                    "request": {
                        "goal_ref": case.request.goal_context.goal_ref,
                        "context_ref": case.request.context_ref,
                        "role_refs": list(case.request.role_refs),
                        "current_situation_refs": list(case.request.current_situation.governed_refs()),
                    },
                    "result": asdict(result),
                    "downstream": _downstream(case.request, result.active_required_condition_refs, case.case_id),
                }
            )
        negative = []
        for case_id, request in build_negative_required_condition_requests_v1():
            negative_request = replace(request, candidate_only=False)
            negative.append(
                {
                    "case_id": case_id,
                    "result": asdict(route.form_required_cognitive_conditions(negative_request)),
                }
            )
        return {
            "phase": "Phase-P1-Luna-Required-Cognitive-Condition-Formation-v1-001",
            "source_mode": SOURCE_MODE,
            "formation_algorithm": "governed objective applicability + situation activation/suppression + coverage satisfaction + minimum-set selection",
            "cases": cases,
            "negative_cases": negative,
            "provider_invoked": False,
            "model_invoked": False,
            "observation_execution": False,
            "observation_demand_formed": False,
            "capability_selection_executed": False,
            "information_need_formation_reentered": False,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }
