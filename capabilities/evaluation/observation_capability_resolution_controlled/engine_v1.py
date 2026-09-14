"""Controlled evaluation engine for Observation Demand capability resolution."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from capabilities.midplatform.model_manager.registries.universal_capability_slot.observation_demand_capability_resolution_v1 import (
    resolve_observation_demand_capabilities,
)

from .fixtures_v1 import SOURCE_MODE, build_observation_capability_resolution_cases_v1


PHASE = "Phase-Observation-Demand-Capability-Resolution-Controlled-Implementation-v1-001"


class ObservationCapabilityResolutionEvaluationEngineV1:
    """Run deterministic synthetic resolution cases without runtime binding."""

    def run(self) -> dict[str, Any]:
        cases = []
        for case in build_observation_capability_resolution_cases_v1():
            request = case.request
            demand_before = tuple(asdict(item) for item in request.observation_demands)
            result = resolve_observation_demand_capabilities(request)
            demand_after = tuple(asdict(item) for item in request.observation_demands)
            replay = resolve_observation_demand_capabilities(request)
            cases.append(
                {
                    "case_id": case.case_id,
                    "evaluation_marker": case.evaluation_marker,
                    "expected_status": case.expected_status,
                    "expected_candidate_count": case.expected_candidate_count,
                    "request": asdict(request),
                    "observation_demand_snapshot_before": demand_before,
                    "observation_demand_snapshot_after": demand_after,
                    "deterministic_replay_candidate_refs": list(replay.resolved_candidate_refs),
                    "result": asdict(result),
                }
            )
        return {
            "phase": PHASE,
            "source_mode": SOURCE_MODE,
            "resolution_algorithm": (
                "explicit Demand-to-single-capability-class mapping plus exact class "
                "matching against controlled available/admitted inventory"
            ),
            "cases": cases,
            "candidate_only": True,
            "read_only": True,
            "provider_binding": False,
            "model_binding": False,
            "capability_activation": False,
            "capability_reservation": False,
            "capability_scheduling": False,
            "capability_execution": False,
            "provider_invocation": False,
            "model_invocation": False,
            "perception_routing": False,
            "observation_gateway_request": False,
            "fpo_runtime_request": False,
            "resource_acquisition": False,
            "ranking_executed": False,
            "winner_selected": False,
            "current_world_mutation": False,
            "field_mutation": False,
            "memory_pcn_mutation": False,
            "truth_declared": False,
            "world_truth_declared": False,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = ["ObservationCapabilityResolutionEvaluationEngineV1"]
