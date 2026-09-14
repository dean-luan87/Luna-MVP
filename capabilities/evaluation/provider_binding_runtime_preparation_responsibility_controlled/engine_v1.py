"""Controlled evaluation wrapper for Provider Binding responsibility seams."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

from capabilities.midplatform.provider_runtime_governance.provider_binding_runtime_preparation_v1 import (
    form_provider_binding_runtime_preparation_candidates,
)

from .fixtures_v1 import (
    build_provider_binding_runtime_preparation_cases_v1,
    build_responsibility_audit_cases_v1,
)


PHASE = "Phase-Provider-Binding-And-Runtime-Preparation-Responsibility-Controlled-Implementation-v1-001"


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


RESPONSIBILITY_MATRIX = (
    {
        "module": "Cognitive Requirement",
        "requester": "Problem / cognitive context",
        "requirement_complexity_owned_by": "Cognitive Requirement owner",
        "module_decision": "which semantic requirement is necessary",
        "forbidden_complexity": "provider/model/runtime details",
    },
    {
        "module": "Observation Demand",
        "requester": "Cognitive Requirement / Need",
        "requirement_complexity_owned_by": "Observation Demand owner",
        "module_decision": "what information to observe",
        "forbidden_complexity": "provider selection, runtime allocation",
    },
    {
        "module": "Capability Resolution",
        "requester": "Observation Demand",
        "requirement_complexity_owned_by": "Capability Governance",
        "module_decision": "which capability candidates match",
        "forbidden_complexity": "cognitive goal reinterpretation",
    },
    {
        "module": "Perception Routing",
        "requester": "Capability Resolution",
        "requirement_complexity_owned_by": "Perception control boundary",
        "module_decision": "which demand×capability handoffs are possible",
        "forbidden_complexity": "provider/model choice",
    },
    {
        "module": "FPO Compatibility",
        "requester": "Perception Routing",
        "requirement_complexity_owned_by": "FPO compatibility boundary",
        "module_decision": "whether the handoff shape is FPO-compatible",
        "forbidden_complexity": "provider binding and runtime execution",
    },
    {
        "module": "Provider Target Preparation",
        "requester": "FPO Compatibility",
        "requirement_complexity_owned_by": "Provider Governance",
        "module_decision": "which explicit provider targets can be prepared",
        "forbidden_complexity": "new demand, model inference, binding, allocation",
    },
    {
        "module": "Provider Binding",
        "requester": "Provider Target Preparation",
        "requirement_complexity_owned_by": "Provider Governance",
        "module_decision": "whether a provider binding can be formed",
        "forbidden_complexity": "new Need, target rewrite, execution",
    },
    {
        "module": "Runtime Allocation",
        "requester": "Provider Binding",
        "requirement_complexity_owned_by": "Runtime / Resource owner",
        "module_decision": "whether runtime resources can be prepared",
        "forbidden_complexity": "cognitive requirement reinterpretation",
    },
    {
        "module": "Execution Instance",
        "requester": "Runtime Allocation",
        "requirement_complexity_owned_by": "Runtime owner",
        "module_decision": "create concrete execution identity",
        "forbidden_complexity": "provider choice and observation meaning",
    },
    {
        "module": "Observation Gateway Runtime Admission",
        "requester": "Runtime Observation Envelope",
        "requirement_complexity_owned_by": "Observation Gateway",
        "module_decision": "admit runtime ingress/proof",
        "forbidden_complexity": "strategy, provider selection, cognition rewrite",
    },
)


FAILURE_OWNERSHIP_MATRIX = (
    {"failure": "requirement_missing", "owner": "Requester / upstream requirement owner", "class": "semantic"},
    {"failure": "capability_mismatch", "owner": "Capability Resolution", "class": "semantic boundary"},
    {"failure": "provider_unavailable", "owner": "Provider Governance", "class": "operational"},
    {"failure": "binding_not_allowed", "owner": "Provider Binding owner", "class": "binding"},
    {"failure": "resource_unavailable", "owner": "Resource / Runtime Allocation", "class": "operational"},
    {"failure": "execution_failure", "owner": "Runtime owner", "class": "operational"},
    {"failure": "gateway_rejected", "owner": "Observation Gateway", "class": "ingress"},
    {"failure": "evidence_insufficient", "owner": "FPO / cognitive semantic control", "class": "semantic"},
)


class ProviderBindingRuntimePreparationEvaluationEngineV1:
    def run(self) -> dict[str, Any]:
        cases = []
        for case in build_provider_binding_runtime_preparation_cases_v1():
            request = case.request
            before = _json_safe(request)
            result = form_provider_binding_runtime_preparation_candidates(request)
            after = _json_safe(request)
            replay = form_provider_binding_runtime_preparation_candidates(request)
            cases.append(
                {
                    "case_id": case.case_id,
                    "evaluation_marker": case.evaluation_marker,
                    "expected_status": case.expected_status,
                    "expected_candidate_count": case.expected_candidate_count,
                    "request": before,
                    "request_snapshot_before": before,
                    "request_snapshot_after": after,
                    "result": _json_safe(result),
                    "deterministic_replay": {
                        "formation_status": replay.formation_status,
                        "candidate_refs": list(replay.provider_binding_preparation_candidate_refs),
                    },
                }
            )
        return {
            "phase": PHASE,
            "source_mode": "CONTROLLED_PROVIDER_BINDING_RUNTIME_PREPARATION",
            "canonical_owner": "Provider Governance",
            "requester_owns_requirement_complexity": True,
            "executor_owns_execution_complexity": True,
            "provider_governance_reused": True,
            "second_provider_owner_created": False,
            "new_cognitive_owner_created": False,
            "provider_binding_formed": False,
            "runtime_allocation_formed": False,
            "execution_instance_created": False,
            "provider_session_started": False,
            "gateway_submission": False,
            "runtime_admission_executed": False,
            "provider_invocation": False,
            "model_invocation": False,
            "capability_activation": False,
            "slot_reservation": False,
            "resource_scheduling": False,
            "runtime_observation_created": False,
            "observation_execution": False,
            "attention_formed": False,
            "decision_formed": False,
            "task_formed": False,
            "action_formed": False,
            "current_world_mutation": False,
            "field_mutation": False,
            "memory_pcn_mutation": False,
            "truth_declared": False,
            "world_truth_declared": False,
            "candidate_only": True,
            "read_only": True,
            "responsibility_matrix": RESPONSIBILITY_MATRIX,
            "failure_ownership_matrix": FAILURE_OWNERSHIP_MATRIX,
            "responsibility_audit_cases": [
                _json_safe(item) for item in build_responsibility_audit_cases_v1()
            ],
            "cases": cases,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = ["PHASE", "ProviderBindingRuntimePreparationEvaluationEngineV1"]
