"""Controlled runner engine for common Self/External minimum-view formation."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)

from .fixtures_v1 import (
    SOURCE_MODE,
    build_minimum_view_cases_v1,
    build_negative_minimum_view_requests_v1,
)


def _request_summary(request: Any) -> Dict[str, Any]:
    return {
        "goal_ref": request.goal_context.goal_ref,
        "goal_conditions": list(request.goal_context.success_condition_refs),
        "role_conditions": list(request.governed_role_condition_refs),
        "context_ref": request.context_ref,
        "available_information_refs": [
            item.information_ref for item in request.available_information
        ],
        "available_object_types": {
            item.information_ref: item.object_type
            for item in request.available_information
        },
    }


class ARouteMinimumRelevantCognitiveViewEvaluationEngineV1:
    def run(self) -> Dict[str, Any]:
        route = ARouteOrchestrationEngineV1()
        cases = []
        for case in build_minimum_view_cases_v1():
            result = route.form_minimum_relevant_cognitive_view(case.request)
            cases.append(
                {
                    "case_id": case.case_id,
                    "category": case.category,
                    "request": _request_summary(case.request),
                    "result": asdict(result),
                }
            )

        negative_cases = []
        for case_id, request in build_negative_minimum_view_requests_v1():
            result = route.form_minimum_relevant_cognitive_view(request)
            negative_cases.append(
                {
                    "case_id": case_id,
                    "request": _request_summary(request),
                    "result": asdict(result),
                }
            )

        return {
            "phase": "Phase-P1-Luna-Minimum-Relevant-Cognitive-View-Formation-v1-001",
            "source_mode": SOURCE_MODE,
            "selection_algorithm": "declared governed condition intersection; object type does not select",
            "cases": cases,
            "negative_cases": negative_cases,
            "provider_invoked": False,
            "model_invoked": False,
            "observation_execution": False,
            "observation_demand_formed": False,
            "capability_selection_executed": False,
            "goal_mutation": False,
            "self_mutation": False,
            "field_mutation": False,
            "world_truth_declared": False,
            "memory_mutation": False,
            "pcn_mutation": False,
            "decision_execution": False,
            "task_execution": False,
            "action_execution": False,
            "scenario_id_semantic_driver": False,
            "opaque_context_semantic_guess": False,
            "static_goal_need_lookup": False,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = ["ARouteMinimumRelevantCognitiveViewEvaluationEngineV1"]
