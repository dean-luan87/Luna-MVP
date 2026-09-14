"""Controlled evaluation engine for acquisition strategy candidate formation."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from capabilities.midplatform.core.cognitive_flow.information_acquisition_strategy_candidate_formation_v1 import (
    form_information_acquisition_strategy_candidates,
)

from .fixtures_v1 import (
    SOURCE_MODE,
    build_information_acquisition_strategy_cases_v1,
)


class InformationAcquisitionStrategyFormationEvaluationEngineV1:
    """Run only deterministic controlled inputs; never acquire or execute."""

    def run(self) -> Dict[str, Any]:
        cases = []
        for case in build_information_acquisition_strategy_cases_v1():
            request = case.request
            before = {
                "branches": tuple(asdict(item) for item in request.branch_candidates),
                "governance_decisions": tuple(
                    asdict(item) for item in request.governance_decisions
                ),
                "needs": tuple(asdict(item) for item in request.need_candidates),
                "bases": tuple(
                    asdict(item) for item in request.governed_acquisition_bases
                ),
            }
            result = form_information_acquisition_strategy_candidates(request)
            after = {
                "branches": tuple(asdict(item) for item in request.branch_candidates),
                "governance_decisions": tuple(
                    asdict(item) for item in request.governance_decisions
                ),
                "needs": tuple(asdict(item) for item in request.need_candidates),
                "bases": tuple(
                    asdict(item) for item in request.governed_acquisition_bases
                ),
            }
            cases.append(
                {
                    "case_id": case.case_id,
                    "evaluation_marker": case.evaluation_marker,
                    "expected_status": case.expected_status,
                    "expected_strategy_count": case.expected_strategy_count,
                    "request": asdict(request),
                    "input_snapshot_before": before,
                    "input_snapshot_after": after,
                    "result": asdict(result),
                }
            )

        return {
            "phase": "Phase-P1-Luna-Information-Acquisition-Strategy-Candidate-Formation-v1-001",
            "source_mode": SOURCE_MODE,
            "formation_algorithm": (
                "explicit governed acquisition basis projection for admitted branches; "
                "no goal/question/need string lookup and no coordination"
            ),
            "cases": cases,
            "candidate_only": True,
            "read_only": True,
            "strategy_coordination_executed": False,
            "strategy_priority_assigned": False,
            "resource_merge_executed": False,
            "resource_acquisition_executed": False,
            "attention_formed": False,
            "observation_demand_formed": False,
            "capability_requirement_formed": False,
            "capability_resolution_executed": False,
            "provider_invocation": False,
            "model_invocation": False,
            "decision_formed": False,
            "task_formed": False,
            "action_formed": False,
            "field_mutation": False,
            "current_world_mutation": False,
            "memory_pcn_mutation": False,
            "truth_declared": False,
            "world_truth_declared": False,
            "goal_string_lookup": False,
            "question_string_lookup": False,
            "need_string_strategy_lookup": False,
            "scenario_id_semantic_driver": False,
            "case_id_semantic_driver": False,
            "fixture_specific_mapping": False,
            "opaque_context_semantic_guess": False,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = ["InformationAcquisitionStrategyFormationEvaluationEngineV1"]
