"""Controlled evaluation wrapper for the FPO compatibility projection."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

from capabilities.midplatform.field_perception_orchestrator.integration.perception_routing_admission_compatibility_v1 import (
    form_fpo_admission_compatibility_candidates,
)

from .fixtures_v1 import build_perception_routing_admission_compatibility_cases_v1


PHASE = "Phase-Perception-Routing-Admission-Ownership-And-Compatibility-Controlled-Implementation-v1-001"


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


class PerceptionRoutingAdmissionCompatibilityEvaluationEngineV1:
    """Run pure candidate projections; never call FPO/Gateway runtime code."""

    def run(self) -> dict[str, Any]:
        cases = []
        for case in build_perception_routing_admission_compatibility_cases_v1():
            request = case.request
            before = _snapshot(request)
            result = form_fpo_admission_compatibility_candidates(request)
            after = _snapshot(request)
            replay = form_fpo_admission_compatibility_candidates(request)
            cases.append(
                {
                    "case_id": case.case_id,
                    "evaluation_marker": case.evaluation_marker,
                    "expected_status": case.expected_status,
                    "expected_candidate_count": case.expected_candidate_count,
                    "request": _snapshot(request),
                    "request_snapshot_before": before,
                    "request_snapshot_after": after,
                    "deterministic_replay_candidate_refs": list(
                        replay.admission_compatibility_candidate_refs
                    ),
                    "result": asdict(result),
                }
            )
        return {
            "phase": PHASE,
            "source_mode": "CONTROLLED_PERCEPTION_ROUTING_ADMISSION_COMPATIBILITY",
            "canonical_owner": "Field Perception Orchestrator / Active Observation Control",
            "gateway_runtime_called": False,
            "fpo_runtime_called": False,
            "runtime_admission_executed": False,
            "provider_binding": False,
            "model_binding": False,
            "capability_activation": False,
            "slot_reservation": False,
            "resource_scheduling": False,
            "routing_admission_owner_created": False,
            "gateway_submission": False,
            "provider_invocation": False,
            "model_invocation": False,
            "observation_execution": False,
            "attention_formed": False,
            "decision_formed": False,
            "task_formed": False,
            "action_formed": False,
            "truth_declared": False,
            "world_truth_declared": False,
            "current_world_mutation": False,
            "field_mutation": False,
            "memory_pcn_mutation": False,
            "candidate_only": True,
            "read_only": True,
            "cases": cases,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = ["PHASE", "PerceptionRoutingAdmissionCompatibilityEvaluationEngineV1"]
