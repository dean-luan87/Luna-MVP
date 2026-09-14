"""Controlled engine for the Provider Binding → Runtime Preparation seam."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass, replace
from typing import Any, Mapping

from capabilities.midplatform.core.runtime_executor.runtime_allocation_preparation_candidate_v1 import (
    ExecutionInstancePreparationInputV1,
    form_execution_instance_preparation_candidates,
    form_runtime_allocation_preparation_candidates,
    RuntimeAllocationPreparationInputV1,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_candidate_v1 import (
    form_provider_binding_candidates,
)
from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    CORE_GOVERNANCE_RULE_REGISTRY_V1,
    compute_unified_final_decision,
    resolve_applicable_governance_set,
    run_governance_postflight,
    run_governance_preflight,
    validate_failure_ownership,
    validate_requester_executor_boundary,
)

from .fixtures_v1 import build_provider_binding_to_runtime_allocation_cases_v1


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


def _valid_postflight_artifact(result: Any) -> dict[str, Any]:
    return {
        "candidate_only": getattr(result, "candidate_only", True),
        "read_only": getattr(result, "read_only", True),
        "truth_declared": getattr(result, "truth_declared", False),
        "world_truth_declared": getattr(result, "world_truth_declared", False),
        "provider_bound": getattr(result, "provider_bound", False),
        "runtime_allocated": getattr(result, "runtime_allocated", False),
        "execution_instance_created": getattr(result, "execution_instance_created", False),
        "provider_session_started": getattr(result, "provider_session_started", False),
        "gateway_submission": getattr(result, "gateway_submission", False),
        "resource_allocated": getattr(result, "resource_allocation", False),
    }


def _run_pipeline(case: Any) -> dict[str, Any]:
    request = case.request
    request_before = _json_safe(request)
    binding = form_provider_binding_candidates(request)
    binding_replay = form_provider_binding_candidates(request)
    allocation = None
    execution = None
    business_executed = True
    if case.run_allocation and binding.candidates:
        allocation_request = RuntimeAllocationPreparationInputV1(
            preparation_ref=f"runtime:{case.case_id}",
            parent_cognitive_problem_ref=binding.parent_cognitive_problem_ref,
            source_state_ref=binding.source_state_ref,
            provider_binding_candidates=binding.candidates,
            context_refs=case.request.context_refs if hasattr(case.request, "context_refs") else (),
            trace_ref=f"trace:runtime:{case.case_id}",
            provenance_refs=(f"provenance:runtime:{case.case_id}",),
        )
        allocation = form_runtime_allocation_preparation_candidates(allocation_request)
        if case.run_execution_preparation and allocation.candidates:
            execution_request = ExecutionInstancePreparationInputV1(
                preparation_ref=f"execution:{case.case_id}",
                parent_cognitive_problem_ref=allocation.parent_cognitive_problem_ref,
                source_state_ref=allocation.source_state_ref,
                runtime_allocation_candidates=allocation.candidates,
                runtime_envelope_shape_refs=("runtime-envelope:observation",),
                context_refs=allocation_request.context_refs,
                trace_ref=f"trace:execution:{case.case_id}",
                provenance_refs=(f"provenance:execution:{case.case_id}",),
            )
            execution = form_execution_instance_preparation_candidates(execution_request)
    request_after = _json_safe(request)
    artifact = case.postflight_artifact or _valid_postflight_artifact(execution or allocation or binding)
    return {
        "request_snapshot_before": request_before,
        "request_snapshot_after": request_after,
        "binding": _json_safe(binding),
        "deterministic_replay": {
            "formation_status": binding_replay.formation_status,
            "provider_binding_candidate_refs": list(
                binding_replay.provider_binding_candidate_refs
            ),
        },
        "allocation": _json_safe(allocation),
        "execution_instance_preparation": _json_safe(execution),
        "business_engine_executed": business_executed,
        "postflight_artifact": _json_safe(artifact),
    }


class ProviderBindingToRuntimeAllocationEvaluationEngineV1:
    def run(self) -> dict[str, Any]:
        case_results = []
        for case in build_provider_binding_to_runtime_allocation_cases_v1():
            applicable = resolve_applicable_governance_set(case.profile, CORE_GOVERNANCE_RULE_REGISTRY_V1)
            preflight = run_governance_preflight(
                case.profile,
                CORE_GOVERNANCE_RULE_REGISTRY_V1,
                case.authority_records,
                tuple(case.profile.protocol_refs) if hasattr(case.profile, "protocol_refs") else (),
            )
            if preflight.status == "PASS":
                pipeline = _run_pipeline(case)
                business_executed = pipeline["business_engine_executed"]
                postflight = run_governance_postflight(case.profile, pipeline["postflight_artifact"])
                boundary_errors = validate_requester_executor_boundary(case.boundary_payload or {})
                failure_errors = validate_failure_ownership(case.failure_ownership_payload or {})
                if boundary_errors or failure_errors:
                    postflight = replace(
                        postflight,
                        status="GOVERNANCE_POSTFLIGHT_BLOCKED",
                        blocker_refs=tuple(
                            dict.fromkeys(
                                (*postflight.blocker_refs, *boundary_errors, *failure_errors)
                            )
                        ),
                    )
            else:
                pipeline = {
                    "request_snapshot_before": _json_safe(case.request),
                    "request_snapshot_after": _json_safe(case.request),
                    "binding": None,
                    "allocation": None,
                    "execution_instance_preparation": None,
                    "business_engine_executed": False,
                    "postflight_artifact": {},
                }
                business_executed = False
                postflight = None
            case_results.append(
                {
                    "case_id": case.case_id,
                    "evaluation_marker": case.evaluation_marker,
                    "expected": {
                        "binding_status": case.expected_binding_status,
                        "binding_count": case.expected_binding_count,
                        "allocation_status": case.expected_allocation_status,
                        "allocation_count": case.expected_allocation_count,
                        "execution_status": case.expected_execution_status,
                        "execution_count": case.expected_execution_count,
                    },
                    "applicable_governance": _json_safe(applicable),
                    "governance_preflight": _json_safe(preflight),
                    "governance_postflight": _json_safe(postflight),
                    "boundary_errors": list(validate_requester_executor_boundary(case.boundary_payload or {})),
                    "boundary_payload": _json_safe(case.boundary_payload),
                    "failure_ownership_payload": _json_safe(case.failure_ownership_payload),
                    "failure_ownership_errors": list(validate_failure_ownership(case.failure_ownership_payload or {})),
                    "business_engine_executed": business_executed,
                    **pipeline,
                }
            )
        return {
            "phase": "Phase-Provider-Binding-To-Runtime-Allocation-Controlled-Implementation-v1-001",
            "source_mode": "CONTROLLED_PROVIDER_BINDING_TO_RUNTIME_ALLOCATION",
            "canonical_provider_binding_owner": "Provider Governance",
            "canonical_runtime_owner": "Runtime Executor",
            "governance_backbone_reused": True,
            "governance_rule_registry_ref": CORE_GOVERNANCE_RULE_REGISTRY_V1.registry_ref,
            "preflight_before_business_engine": True,
            "provider_binding_decision_formed": False,
            "provider_bound": False,
            "runtime_allocated": False,
            "resource_allocated": False,
            "execution_instance_created": False,
            "provider_session_started": False,
            "gateway_submission": False,
            "provider_invocation": False,
            "model_invocation": False,
            "capability_activation": False,
            "slot_reservation": False,
            "truth_declared": False,
            "world_truth_declared": False,
            "candidate_only": True,
            "read_only": True,
            "requester_owns_requirement_complexity": True,
            "executor_owns_execution_complexity": True,
            "provider_only_model_optional": True,
            "cases": case_results,
            "status": "READY_FOR_USER_VERIFICATION",
        }


__all__ = ["ProviderBindingToRuntimeAllocationEvaluationEngineV1"]
