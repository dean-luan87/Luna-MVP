"""Controlled evaluation engine for alternative satisfaction basis semantics."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_engine_v1 import (
    ARouteRequiredCognitiveConditionFormationEngineV1,
)
from capabilities.midplatform.sandbox.cognitive_exploration.cognitive_exploration_sandbox_v1 import (
    run_controlled_cognitive_exploration_sandbox,
)

from .fixtures_v1 import SOURCE_MODE, build_alternative_satisfaction_cases_v1


class CognitiveRequirementAlternativeSatisfactionBasisEvaluationEngineV1:
    """Runs direct contract cases and the corrected Sandbox Scenario 12 seam."""

    def run(self) -> dict[str, Any]:
        condition_engine = ARouteRequiredCognitiveConditionFormationEngineV1()
        cases = []
        for case in build_alternative_satisfaction_cases_v1():
            result = condition_engine.form(case.request)
            cases.append(
                {
                    "case_id": case.case_id,
                    "expected_status": case.expected_status,
                    "expected_satisfaction_status": case.expected_satisfaction_status,
                    "expected_satisfaction_coverage_refs": list(
                        case.expected_satisfaction_coverage_refs
                    ),
                    "result": asdict(result),
                }
            )

        sandbox_trace = asdict(run_controlled_cognitive_exploration_sandbox())
        sandbox_cases = {
            item["scenario_id"]: item for item in sandbox_trace["scenarios"]
        }
        scenario_12 = sandbox_cases["SCENARIO_12_EVIDENCE_CHANGES_COGNITIVE_BASIS"]
        scenario_10 = sandbox_cases["SCENARIO_10_NO_ACQUISITION_STRATEGY_AVAILABLE"]
        scenario_11 = sandbox_cases["SCENARIO_11_IRRELEVANT_ENVIRONMENTAL_CHANGE"]

        return {
            "phase": "Phase-Cognitive-Requirement-Alternative-Satisfaction-Basis-Controlled-Implementation-v1-001",
            "source_mode": SOURCE_MODE,
            "formation_algorithm": (
                "alternative basis ANY coverage with legacy exact coverage fallback"
            ),
            "cases": cases,
            "sandbox_regressions": {
                "scenario_12": scenario_12,
                "scenario_10": scenario_10,
                "scenario_11": scenario_11,
            },
            "negative_guards": {
                "strategy_coordination": False,
                "observation_demand": False,
                "provider": False,
                "model": False,
                "ocr": False,
                "capability_execution": False,
                "decision": False,
                "task": False,
                "action": False,
                "truth_authority": False,
                "world_truth_authority": False,
                "current_world_mutation": False,
                "field_mutation": False,
                "memory_pcn_mutation": False,
                "evidence_fusion": False,
                "confidence_scoring": False,
                "boolean_dsl": False,
                "many_to_many_general_relation_engine": False,
                "need_lifecycle": False,
                "hidden_fallback_strategy": False,
            },
            "information_need_core_subtraction_changed": False,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = [
    "CognitiveRequirementAlternativeSatisfactionBasisEvaluationEngineV1"
]
