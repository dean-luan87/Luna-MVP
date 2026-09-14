"""Controlled evaluation engine for Strategy Coordination."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from capabilities.midplatform.core.cognitive_flow.strategy_coordination_v1 import (
    coordinate_acquisition_strategies,
)

from .fixtures_v1 import SOURCE_MODE, build_strategy_coordination_cases_v1


PHASE = "Phase-Strategy-Coordination-Controlled-Implementation-v1-001"


class StrategyCoordinationEvaluationEngineV1:
    """Build deterministic synthetic coordination summaries."""

    def run(self) -> dict[str, Any]:
        cases = []
        for case in build_strategy_coordination_cases_v1():
            before = tuple(asdict(item) for item in case.request.strategy_candidates)
            result = coordinate_acquisition_strategies(case.request)
            after = tuple(asdict(item) for item in case.request.strategy_candidates)
            cases.append(
                {
                    "case_id": case.case_id,
                    "evaluation_marker": case.evaluation_marker,
                    "expected_result_status": case.expected_result_status,
                    "expected_statuses": list(case.expected_statuses),
                    "request": asdict(case.request),
                    "strategy_snapshot_before": before,
                    "strategy_snapshot_after": after,
                    "result": asdict(result),
                }
            )
        return {
            "phase": PHASE,
            "source_mode": SOURCE_MODE,
            "coordination_algorithm": (
                "explicit branch admission, dependency coverage, governed defer, "
                "explicit redundancy and explicit incompatibility; no ranking or execution"
            ),
            "cases": cases,
            "candidate_only": True,
            "read_only": True,
            "strategy_execution": False,
            "observation_demand_formed": False,
            "capability_resolution_executed": False,
            "provider_invocation": False,
            "model_invocation": False,
            "decision_formed": False,
            "task_formed": False,
            "action_formed": False,
            "truth_declared": False,
            "world_truth_declared": False,
            "current_world_mutation": False,
            "field_mutation": False,
            "memory_pcn_mutation": False,
            "attention_formed": False,
            "resource_governance_executed": False,
            "resource_acquisition_executed": False,
            "priority_assigned": False,
            "ranking_executed": False,
            "winner_selected": False,
            "evidence_fusion_executed": False,
            "branch_mutation": False,
            "information_need_mutation": False,
            "requirement_satisfaction_mutation": False,
            "strategy_coordination_only": True,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = ["StrategyCoordinationEvaluationEngineV1"]
