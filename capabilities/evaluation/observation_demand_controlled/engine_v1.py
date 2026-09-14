"""Controlled evaluation engine for Cognitive Observation Demand formation."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from capabilities.midplatform.core.cognitive_flow.observation_demand_formation_v1 import (
    form_observation_demands,
)

from .fixtures_v1 import SOURCE_MODE, build_observation_demand_cases_v1


PHASE = "Phase-Observation-Demand-Controlled-Implementation-v1-001"


class ObservationDemandEvaluationEngineV1:
    """Run deterministic synthetic cases without invoking a downstream runtime."""

    def run(self) -> dict[str, Any]:
        cases = []
        for case in build_observation_demand_cases_v1():
            request = case.request
            strategy_before = tuple(asdict(item) for item in request.strategy_candidates)
            coordination_before = asdict(request.coordination_result)
            result = form_observation_demands(request)
            strategy_after = tuple(asdict(item) for item in request.strategy_candidates)
            coordination_after = asdict(request.coordination_result)
            replay = form_observation_demands(request)
            cases.append(
                {
                    "case_id": case.case_id,
                    "evaluation_marker": case.evaluation_marker,
                    "expected_status": case.expected_status,
                    "expected_demand_count": case.expected_demand_count,
                    "request": asdict(request),
                    "strategy_snapshot_before": strategy_before,
                    "strategy_snapshot_after": strategy_after,
                    "coordination_snapshot_before": coordination_before,
                    "coordination_snapshot_after": coordination_after,
                    "deterministic_replay_demand_refs": list(replay.demand_refs),
                    "result": asdict(result),
                }
            )
        return {
            "phase": PHASE,
            "source_mode": SOURCE_MODE,
            "formation_algorithm": (
                "explicit admitted Strategy Coordination decisions plus explicit "
                "governed strategy-to-observation mapping; one demand per admitted strategy"
            ),
            "cases": cases,
            "candidate_only": True,
            "read_only": True,
            "attention_formed": False,
            "observation_demand_formed": True,
            "capability_requirement_formed": False,
            "capability_resolution_executed": False,
            "capability_execution": False,
            "provider_invocation": False,
            "model_invocation": False,
            "ocr_execution": False,
            "camera_execution": False,
            "slam_execution": False,
            "runtime_observation_executed": False,
            "resource_acquisition_executed": False,
            "resource_scheduling_executed": False,
            "strategy_priority_assigned": False,
            "winner_selected": False,
            "decision_formed": False,
            "task_formed": False,
            "action_formed": False,
            "evidence_fusion_executed": False,
            "conflict_resolution_executed": False,
            "current_world_mutation": False,
            "field_mutation": False,
            "memory_pcn_mutation": False,
            "truth_declared": False,
            "world_truth_declared": False,
            "sandbox_integration": "DEFERRED",
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = ["ObservationDemandEvaluationEngineV1"]
