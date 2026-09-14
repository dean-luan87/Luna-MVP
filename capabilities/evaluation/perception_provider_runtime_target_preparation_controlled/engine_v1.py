"""Controlled evaluation wrapper for Provider Runtime Target Preparation."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

from capabilities.midplatform.provider_runtime_governance.provider_runtime_target_preparation_v1 import (
    form_provider_runtime_target_candidates,
)

from .fixtures_v1 import build_provider_runtime_target_preparation_cases_v1


PHASE = "Phase-Perception-Provider-Runtime-Target-Preparation-Controlled-Implementation-v1-001"


def _json_safe(value: Any) -> Any:
    if is_dataclass(value):
        return _json_safe(asdict(value))
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    return value


class ProviderRuntimeTargetPreparationEvaluationEngineV1:
    """Run pure projections over synthetic provider mappings only."""

    def run(self) -> dict[str, Any]:
        cases = []
        for case in build_provider_runtime_target_preparation_cases_v1():
            request = case.request
            before = _json_safe(request)
            result = form_provider_runtime_target_candidates(request)
            after = _json_safe(request)
            replay = form_provider_runtime_target_candidates(request)
            cases.append(
                {
                    "case_id": case.case_id,
                    "evaluation_marker": case.evaluation_marker,
                    "expected_status": case.expected_status,
                    "expected_target_count": case.expected_target_count,
                    "request": before,
                    "request_snapshot_before": before,
                    "request_snapshot_after": after,
                    "result": _json_safe(result),
                    "deterministic_replay": {
                        "formation_status": replay.formation_status,
                        "provider_target_candidate_refs": list(
                            replay.provider_target_candidate_refs
                        ),
                    },
                }
            )
        return {
            "phase": PHASE,
            "source_mode": "CONTROLLED_PROVIDER_RUNTIME_TARGET_PREPARATION",
            "canonical_owner": "Provider Governance",
            "provider_inventory_snapshot_controlled": True,
            "provider_registry_runtime_read": False,
            "provider_mapping_explicit_governed_input": True,
            "provider_runtime_governance_reused": True,
            "second_provider_owner_created": False,
            "provider_binding": False,
            "model_binding": False,
            "provider_selection": False,
            "provider_ranking": False,
            "provider_winner": False,
            "execution_instance_created": False,
            "provider_session_started": False,
            "runtime_admission_requested": False,
            "runtime_admission_executed": False,
            "gateway_submission": False,
            "capability_activation": False,
            "capability_reservation": False,
            "slot_reservation": False,
            "resource_scheduling": False,
            "provider_invocation": False,
            "model_invocation": False,
            "camera_execution": False,
            "ocr_execution": False,
            "slam_execution": False,
            "vlm_execution": False,
            "observation_execution": False,
            "evidence_ingress": False,
            "evidence_fusion": False,
            "attention_formed": False,
            "decision_formed": False,
            "task_formed": False,
            "action_formed": False,
            "current_world_mutation": False,
            "field_mutation": False,
            "memory_pcn_mutation": False,
            "candidate_only": True,
            "read_only": True,
            "truth_declared": False,
            "world_truth_declared": False,
            "cases": cases,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = ["PHASE", "ProviderRuntimeTargetPreparationEvaluationEngineV1"]
