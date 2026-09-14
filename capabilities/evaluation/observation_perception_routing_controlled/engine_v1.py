"""Controlled evaluation engine for perception routing candidate formation."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

from capabilities.midplatform.core.observation_gateway.perception_routing_candidate_v1 import (
    form_perception_routing_candidates,
)

from .fixtures_v1 import build_perception_routing_cases_v1


PHASE = "Phase-Observation-Capability-Perception-Routing-Controlled-Implementation-v1-001"


def _snapshot(value: object) -> object:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, tuple):
        return tuple(_snapshot(item) for item in value)
    if isinstance(value, list):
        return [_snapshot(item) for item in value]
    if isinstance(value, dict):
        return {key: _snapshot(item) for key, item in value.items()}
    return value


class PerceptionRoutingEvaluationEngineV1:
    """Run deterministic fixtures without Gateway/FPO/runtime calls."""

    def run(self) -> dict[str, Any]:
        cases = []
        for case in build_perception_routing_cases_v1():
            request = case.request
            demand_before = _snapshot(request.observation_demands)
            requirement_before = _snapshot(request.capability_requirements)
            resolution_before = _snapshot(request.resolution_result)
            result = form_perception_routing_candidates(request)
            demand_after = _snapshot(request.observation_demands)
            requirement_after = _snapshot(request.capability_requirements)
            resolution_after = _snapshot(request.resolution_result)
            replay = form_perception_routing_candidates(request)
            cases.append(
                {
                    "case_id": case.case_id,
                    "evaluation_marker": case.evaluation_marker,
                    "expected_status": case.expected_status,
                    "expected_route_count": case.expected_route_count,
                    "request": asdict(request),
                    "observation_demand_snapshot_before": demand_before,
                    "observation_demand_snapshot_after": demand_after,
                    "capability_requirement_snapshot_before": requirement_before,
                    "capability_requirement_snapshot_after": requirement_after,
                    "resolution_candidate_snapshot_before": resolution_before,
                    "resolution_candidate_snapshot_after": resolution_after,
                    "deterministic_replay_route_refs": list(replay.routing_candidate_refs),
                    "result": asdict(result),
                }
            )
        return {
            "phase": PHASE,
            "source_mode": "CONTROLLED_PERCEPTION_ROUTING_TEST",
            "routing_algorithm": (
                "one candidate-only perception routing projection per valid active "
                "Capability Resolution Candidate"
            ),
            "cases": cases,
            "candidate_only": True,
            "read_only": True,
            "routing_executed": False,
            "routing_admitted": False,
            "route_priority_assigned": False,
            "route_ranking_executed": False,
            "route_winner_selected": False,
            "gateway_submission": False,
            "fpo_runtime_request": False,
            "provider_binding": False,
            "provider_invocation": False,
            "model_binding": False,
            "model_invocation": False,
            "capability_activation": False,
            "capability_reservation": False,
            "capability_scheduling": False,
            "observation_execution": False,
            "resource_scheduling": False,
            "resource_acquisition": False,
            "attention_formed": False,
            "evidence_ingress": False,
            "decision_formed": False,
            "task_formed": False,
            "action_formed": False,
            "truth_declared": False,
            "world_truth_declared": False,
            "current_world_mutation": False,
            "field_mutation": False,
            "memory_pcn_mutation": False,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = ["PHASE", "PerceptionRoutingEvaluationEngineV1"]
