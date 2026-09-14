"""Controlled evaluation engine for governed cognitive branch formation."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from capabilities.midplatform.core.cognitive_flow.governed_cognitive_branch_formation_v1 import (
    form_governed_cognitive_branches,
)

from .fixtures_v1 import (
    SOURCE_MODE,
    build_branch_formation_cases_v1,
    build_negative_branch_formation_requests_v1,
)


class GovernedCognitiveBranchFormationEvaluationEngineV1:
    """Build only deterministic, synthetic candidate outputs."""

    def run(self) -> Dict[str, Any]:
        cases = []
        for case in build_branch_formation_cases_v1():
            result = form_governed_cognitive_branches(case.request)
            cases.append(
                {
                    "case_id": case.case_id,
                    "expected_branch_count": case.expected_branch_count,
                    "expected_basis": list(case.expected_basis),
                    "request": asdict(case.request),
                    "result": asdict(result),
                }
            )

        negative_cases = []
        for case_id, request in build_negative_branch_formation_requests_v1():
            negative_cases.append(
                {
                    "case_id": case_id,
                    "request": asdict(request),
                    "result": asdict(form_governed_cognitive_branches(request)),
                }
            )

        return {
            "phase": "Phase-P1-Luna-Governed-Cognitive-Branch-Formation-v1-001",
            "source_mode": SOURCE_MODE,
            "formation_algorithm": "explicit governed cognitive basis grouping; no string or scenario lookup",
            "cases": cases,
            "negative_cases": negative_cases,
            "candidate_only": True,
            "read_only": True,
            "provider_invocation": False,
            "model_invocation": False,
            "resource_acquisition": False,
            "observation_demand_formed": False,
            "capability_requirement_formed": False,
            "governance_executed": False,
            "decision_formed": False,
            "task_formed": False,
            "action_formed": False,
            "current_world_mutation": False,
            "field_mutation": False,
            "world_truth_declared": False,
            "autonomous_child_runtime_spawn": False,
            "scenario_id_semantic_driver": False,
            "case_id_semantic_driver": False,
            "goal_string_branch_lookup": False,
            "question_string_branch_lookup": False,
            "fixture_specific_mapping": False,
            "opaque_context_semantic_guess": False,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = ["GovernedCognitiveBranchFormationEvaluationEngineV1"]
