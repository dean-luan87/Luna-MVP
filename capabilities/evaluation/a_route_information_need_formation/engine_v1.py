"""Controlled execution wrapper for A-Route Need formation."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)

from .fixtures_v1 import (
    SOURCE_MODE,
    build_information_need_formation_cases_v1,
    build_negative_need_formation_requests_v1,
)


class ARouteInformationNeedFormationEvaluationEngineV1:
    """Runs only deterministic, candidate-only formation; no observation path."""

    def run(self) -> dict[str, Any]:
        engine = ARouteOrchestrationEngineV1()
        cases = []
        for case in build_information_need_formation_cases_v1():
            result = engine.form_information_need(case.request)
            cases.append(
                {
                    "case_id": case.case_id,
                    "expected_status": case.expected_status,
                    "expected_unknown": list(case.expected_unknown),
                    "request": {
                        "goal_ref": case.request.goal_context.goal_ref,
                        "context_ref": case.request.context_ref,
                        "role_refs": list(case.request.role_refs),
                        "current_world_ref": case.request.current_world.current_world_id,
                        "current_cognitive_coverage_refs": list(case.request.current_cognitive_coverage_refs),
                    },
                    "result": asdict(result),
                }
            )
        negative = []
        for case_id, request in build_negative_need_formation_requests_v1():
            negative.append(
                {"case_id": case_id, "result": asdict(engine.form_information_need(request))}
            )
        return {
            "phase": "Phase-P1-Luna-A-Route-Information-Need-Formation-v1-001",
            "source_mode": SOURCE_MODE,
            "cases": cases,
            "negative_cases": negative,
            "formation_algorithm": "governed objective conditions minus Current World coverage",
            "provider_invoked": False,
            "model_invoked": False,
            "observation_execution": False,
            "observation_demand_formed": False,
            "capability_selection_executed": False,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }
