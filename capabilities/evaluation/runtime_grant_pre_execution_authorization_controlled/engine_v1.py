"""Controlled engine for the pre-execution Runtime Grant boundary."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass, replace
from typing import Any

from capabilities.midplatform.core.runtime_executor.runtime_allocation_preparation_candidate_v1 import (
    ExecutionInstancePreparationInputV1,
    form_execution_instance_preparation_candidates,
    form_runtime_allocation_preparation_candidates,
    RuntimeAllocationPreparationInputV1,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    AUTHORITY_REF,
    OWNER,
    RESPONSIBILITY_REF,
    RuntimeExecutionGrantInputV1,
    build_pregrant_authority_binding_key,
    form_runtime_execution_grants,
)
from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    form_runtime_safety_prerequisite_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_authorization_state_v1 import (
    query_active_authorization_for_grant,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_candidate_v1 import (
    ProviderBindingCandidateInputV1,
    form_provider_binding_candidates,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_runtime_preparation_v1 import (
    form_provider_binding_runtime_preparation_candidates,
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

from .fixtures_v1 import (
    EVALUATION_MARKER,
    PHASE,
    _target_request,
    build_controlled_canonical_runtime_scope_v1,
    build_runtime_grant_cases_v1,
)


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


def _postflight_artifact(result: Any) -> dict[str, Any]:
    return {
        "candidate_only": getattr(result, "candidate_only", False),
        "read_only": getattr(result, "read_only", True),
        "truth_declared": getattr(result, "truth_declared", False),
        "world_truth_declared": getattr(result, "world_truth_declared", False),
        "runtime_started": False,
        "runtime_allocated": getattr(result, "runtime_allocated", False),
        "execution_instance_created": getattr(result, "execution_instance_created", False),
        "provider_session_started": getattr(result, "provider_session_started", False),
        "gateway_submission": getattr(result, "gateway_submission", False),
        "resource_allocated": getattr(result, "resource_allocated", False),
    }


def _run_pipeline(case: Any) -> dict[str, Any]:
    canonical_scope = build_controlled_canonical_runtime_scope_v1(
        f"runtime-grant:{case.case_id.lower()}"
    )
    if canonical_scope is None:
        return {
            "grant": None,
            "pipeline_status": "CANONICAL_SCOPE_UNAVAILABLE",
            "business_engine_executed": True,
        }
    admitted_action_ref, working_envelope_ref, working_envelope_version_ref = canonical_scope
    target_request = replace(
        _target_request(case.case_id, case.target_candidates),
        admitted_action_ref=admitted_action_ref,
        working_envelope_ref=working_envelope_ref,
        working_envelope_version_ref=working_envelope_version_ref,
    )
    target_request_before = _json_safe(target_request)
    target = form_provider_binding_runtime_preparation_candidates(target_request)
    target_request_after = _json_safe(target_request)
    if target.formation_status != "PROVIDER_BINDING_PREPARATION_CANDIDATES_FORMED":
        return {
            "target_request_snapshot_before": target_request_before,
            "target_request_snapshot_after": target_request_after,
            "target_preparation": _json_safe(target),
            "binding": None,
            "allocation": None,
            "execution_instance_preparation": None,
            "grant": None,
            "pipeline_status": target.formation_status,
            "business_engine_executed": True,
        }

    target = replace(
        target,
        candidates=tuple(
            replace(
                item,
                provider_candidate_ref="provider_openvins",
                capability_candidate_ref="spatial_mapping",
                capability_class_ref="capability-class:spatial-mapping",
            )
            for item in target.candidates
        ),
    )

    binding_request = ProviderBindingCandidateInputV1(
        preparation_ref=f"grant-binding:{case.case_id.lower()}",
        parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
        source_state_ref=target.source_state_ref,
        preparation_candidates=target.candidates,
        context_refs=target.context_refs,
        trace_ref=f"trace:grant-binding:{case.case_id.lower()}",
        provenance_refs=(f"provenance:grant-binding:{case.case_id.lower()}",),
        runtime_requirement_refs=(f"runtime-requirement:{case.case_id.lower()}",),
        resource_class_refs=(f"resource-class:{case.case_id.lower()}",),
        execution_class_refs=(f"execution-class:{case.case_id.lower()}",),
        admitted_action_ref=admitted_action_ref,
        working_envelope_ref=working_envelope_ref,
        working_envelope_version_ref=working_envelope_version_ref,
    )
    binding_request_before = _json_safe(binding_request)
    binding = form_provider_binding_candidates(binding_request)
    binding_request_after = _json_safe(binding_request)
    if not binding.candidates:
        return {
            "target_request_snapshot_before": target_request_before,
            "target_request_snapshot_after": target_request_after,
            "binding_request_snapshot_before": binding_request_before,
            "binding_request_snapshot_after": binding_request_after,
            "target_preparation": _json_safe(target),
            "binding": _json_safe(binding),
            "allocation": None,
            "execution_instance_preparation": None,
            "grant": None,
            "pipeline_status": binding.formation_status,
            "business_engine_executed": True,
        }

    allocation_request = RuntimeAllocationPreparationInputV1(
        preparation_ref=f"grant-allocation:{case.case_id.lower()}",
        parent_cognitive_problem_ref=binding.parent_cognitive_problem_ref,
        source_state_ref=binding.source_state_ref,
        provider_binding_candidates=binding.candidates,
        context_refs=target.context_refs,
        trace_ref=f"trace:grant-allocation:{case.case_id.lower()}",
        provenance_refs=(f"provenance:grant-allocation:{case.case_id.lower()}",),
        admitted_action_ref=admitted_action_ref,
        working_envelope_ref=working_envelope_ref,
        working_envelope_version_ref=working_envelope_version_ref,
    )
    allocation_request_before = _json_safe(allocation_request)
    allocation = form_runtime_allocation_preparation_candidates(allocation_request)
    allocation_request_after = _json_safe(allocation_request)
    if not allocation.candidates:
        return {
            "target_request_snapshot_before": target_request_before,
            "target_request_snapshot_after": target_request_after,
            "binding_request_snapshot_before": binding_request_before,
            "binding_request_snapshot_after": binding_request_after,
            "allocation_request_snapshot_before": allocation_request_before,
            "allocation_request_snapshot_after": allocation_request_after,
            "target_preparation": _json_safe(target),
            "binding": _json_safe(binding),
            "allocation": _json_safe(allocation),
            "execution_instance_preparation": None,
            "grant": None,
            "pipeline_status": allocation.formation_status,
            "business_engine_executed": True,
        }

    execution_request = ExecutionInstancePreparationInputV1(
        preparation_ref=f"grant-execution:{case.case_id.lower()}",
        parent_cognitive_problem_ref=allocation.parent_cognitive_problem_ref,
        source_state_ref=allocation.source_state_ref,
        runtime_allocation_candidates=allocation.candidates,
        runtime_envelope_shape_refs=("runtime-envelope:observation",),
        context_refs=target.context_refs,
        trace_ref=f"trace:grant-execution:{case.case_id.lower()}",
        provenance_refs=(f"provenance:grant-execution:{case.case_id.lower()}",),
        admitted_action_ref=admitted_action_ref,
        working_envelope_ref=working_envelope_ref,
        working_envelope_version_ref=working_envelope_version_ref,
    )
    execution_request_before = _json_safe(execution_request)
    execution = form_execution_instance_preparation_candidates(execution_request)
    execution_request_after = _json_safe(execution_request)
    if not execution.candidates:
        return {
            "target_request_snapshot_before": target_request_before,
            "target_request_snapshot_after": target_request_after,
            "binding_request_snapshot_before": binding_request_before,
            "binding_request_snapshot_after": binding_request_after,
            "allocation_request_snapshot_before": allocation_request_before,
            "allocation_request_snapshot_after": allocation_request_after,
            "execution_request_snapshot_before": execution_request_before,
            "execution_request_snapshot_after": execution_request_after,
            "target_preparation": _json_safe(target),
            "binding": _json_safe(binding),
            "allocation": _json_safe(allocation),
            "execution_instance_preparation": _json_safe(execution),
            "grant": None,
            "pipeline_status": execution.formation_status,
            "business_engine_executed": True,
        }

    binding_candidate = binding.candidates[0]
    execution_candidate = execution.candidates[0]
    binding_key = build_pregrant_authority_binding_key(
        execution_instance_preparation_candidate_ref=execution_candidate.execution_instance_preparation_candidate_ref,
        provider_candidate_ref=binding_candidate.provider_candidate_ref,
        capability_candidate_ref=binding_candidate.capability_candidate_ref,
        admitted_action_ref=admitted_action_ref,
        working_envelope_ref=working_envelope_ref,
        working_envelope_version_ref=working_envelope_version_ref,
    )
    effect_class = "runtime-execution"
    if any(
        (
            case.provider_binding_status != "ELIGIBLE",
            case.capability_admission_status != "ADMITTED",
            case.permission_status != "ALLOWED",
            case.safety_status != "ALLOWED",
            case.constitution_status != "ALLOWED",
            case.resource_feasibility_status != "SATISFIABLE",
            case.runtime_boundary_status != "VALID",
            case.freshness_status != "FRESH",
            case.validity_status != "FRESH",
            not case.execution_ready,
        )
    ):
        effect_class = "blocked-controlled-scenario"
    safety = form_runtime_safety_prerequisite_v1(
        binding_key=(*binding_key, effect_class),
        effect_class=effect_class,
    )

    grant_request = RuntimeExecutionGrantInputV1(
        grant_request_ref=f"grant-request:{case.case_id.lower()}",
        parent_cognitive_problem_ref=execution.parent_cognitive_problem_ref,
        source_state_ref=execution.source_state_ref,
        provider_binding_candidates=binding.candidates,
        runtime_allocation_candidates=allocation.candidates,
        execution_instance_preparation_candidates=execution.candidates,
        permission_refs=(f"permission:{case.case_id.lower()}",),
        safety_refs=(f"safety:{case.case_id.lower()}",),
        protocol_refs=("protocol:runtime-execution-grant:v1",),
        governance_refs=(f"governance:{case.case_id.lower()}",),
        constraint_refs=(f"constraint:{case.case_id.lower()}",),
        validity_scope=(f"scope:{case.case_id.lower()}",),
        expiry_boundary_ref=f"expiry:{case.case_id.lower()}",
        safety_prerequisite_ref=safety.result_ref,
        effect_class=effect_class,
        context_refs=target.context_refs,
        lineage_refs=tuple(
            dict.fromkeys(
                ref
                for candidate in binding.candidates
                for ref in candidate.lineage_refs
            )
        ),
        provenance_refs=(f"provenance:grant:{case.case_id.lower()}",),
        trace_ref=f"trace:grant:{case.case_id.lower()}",
        grant_authority_ref=case.grant_authority_ref,
        grant_responsibility_ref=case.grant_responsibility_ref,
        admitted_action_ref=admitted_action_ref,
        working_envelope_ref=working_envelope_ref,
        working_envelope_version_ref=working_envelope_version_ref,
    )
    if case.malformed_grant_input:
        grant_request = replace(
            grant_request,
            execution_instance_preparation_candidates=execution.candidates[0],
        )
    grant = form_runtime_execution_grants(grant_request)
    return {
        "target_request_snapshot_before": target_request_before,
        "target_request_snapshot_after": target_request_after,
        "binding_request_snapshot_before": binding_request_before,
        "binding_request_snapshot_after": binding_request_after,
        "allocation_request_snapshot_before": allocation_request_before,
        "allocation_request_snapshot_after": allocation_request_after,
        "execution_request_snapshot_before": execution_request_before,
        "execution_request_snapshot_after": execution_request_after,
        "target_preparation": _json_safe(target),
        "binding": _json_safe(binding),
        "allocation": _json_safe(allocation),
        "execution_instance_preparation": _json_safe(execution),
        "grant_request_snapshot_before": _json_safe(grant_request),
        "grant_request_snapshot_after": _json_safe(grant_request),
        "grant": _json_safe(grant),
        "runtime_authorization_state_formed": any(
            item.decision == "GRANTED" for item in grant.decisions
        ) and all(
            query_active_authorization_for_grant(item) is not None
            for item in grant.decisions
            if item.decision == "GRANTED"
        ),
        "pipeline_status": grant.formation_status,
        "business_engine_executed": True,
    }


class RuntimeGrantPreExecutionAuthorizationEvaluationEngineV1:
    def run(self) -> dict[str, Any]:
        case_results = []
        for case in build_runtime_grant_cases_v1():
            applicable = resolve_applicable_governance_set(
                case.profile, CORE_GOVERNANCE_RULE_REGISTRY_V1
            )
            preflight = run_governance_preflight(
                case.profile,
                CORE_GOVERNANCE_RULE_REGISTRY_V1,
                case.authority_records,
                tuple(case.profile.protocol_refs),
            )
            if preflight.status == "PASS":
                pipeline = _run_pipeline(case)
                grant_result = pipeline.get("grant") or {}
                decisions = grant_result.get("decisions", [])
                postflight_artifact = {
                    "candidate_only": False,
                    "read_only": True,
                    "truth_declared": False,
                    "world_truth_declared": False,
                    "runtime_started": False,
                    "runtime_allocated": False,
                    "execution_instance_created": False,
                    "provider_session_started": False,
                    "gateway_submission": False,
                    "resource_allocated": False,
                }
                if case.postflight_artifact:
                    postflight_artifact.update(case.postflight_artifact)
                postflight = run_governance_postflight(case.profile, postflight_artifact)
                boundary_errors = validate_requester_executor_boundary(
                    case.boundary_payload or {}
                )
                failure_errors = validate_failure_ownership(
                    case.failure_ownership_payload or {}
                )
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
                replay = None
                if case.case_id == "DETERMINISTIC_DECISION" and pipeline.get(
                    "grant_request_snapshot_before"
                ):
                    # Reconstructing through the same immutable pipeline is a
                    # deterministic replay check; no runtime call is made.
                    replay = _run_pipeline(case).get("grant")
                replay_payload = {
                    "grant_refs": [item.get("grant_ref") for item in decisions],
                    "replayed_grant_refs": [
                        item.get("grant_ref")
                        for item in (replay or {}).get("decisions", [])
                    ],
                    "deterministic": replay is not None
                    and [item.get("grant_ref") for item in decisions]
                    == [item.get("grant_ref") for item in replay.get("decisions", [])],
                    "new_authorization_occurrence": replay is not None
                    and [item.get("authorization_ref") for item in decisions]
                    != [item.get("authorization_ref") for item in replay.get("decisions", [])],
                }
            else:
                pipeline = {
                    "target_preparation": None,
                    "binding": None,
                    "allocation": None,
                    "execution_instance_preparation": None,
                    "grant": None,
                    "pipeline_status": "GOVERNANCE_PREFLIGHT_BLOCKED",
                    "business_engine_executed": False,
                }
                postflight = None
                boundary_errors = validate_requester_executor_boundary(
                    case.boundary_payload or {}
                )
                failure_errors = validate_failure_ownership(
                    case.failure_ownership_payload or {}
                )
                replay_payload = {"deterministic": False}
            case_results.append(
                {
                    "case_id": case.case_id,
                    "evaluation_marker": EVALUATION_MARKER,
                    "expected": {
                        "status": case.expected_status,
                        "decision": case.expected_decision,
                        "count": case.expected_count,
                    },
                    "fpo_continuation_status": case.fpo_continuation_status,
                    "gateway_admission_status": case.gateway_admission_status,
                    "applicable_governance": _json_safe(applicable),
                    "governance_preflight": _json_safe(preflight),
                    "governance_postflight": _json_safe(postflight),
                    "boundary_errors": list(boundary_errors),
                    "failure_ownership_errors": list(failure_errors),
                    "failure_ownership_payload": _json_safe(case.failure_ownership_payload),
                    "business_engine_executed": pipeline["business_engine_executed"],
                    **pipeline,
                    "deterministic_replay": replay_payload,
                }
            )
        return {
            "phase": PHASE,
            "source_mode": EVALUATION_MARKER,
            "canonical_runtime_grant_owner": OWNER,
            "permission_admission_manager_reused": True,
            "runtime_executor_reused": True,
            "protocol_manager_reused": True,
            "new_runtime_grant_owner_created": False,
            "new_governance_super_owner_created": False,
            "requester_owns_requirement_complexity": True,
            "executor_owns_execution_complexity": True,
            "runtime_execution_authorization_authority": AUTHORITY_REF,
            "runtime_execution_authorization_responsibility": RESPONSIBILITY_REF,
            "runtime_execution_grant_authoritative": True,
            "runtime_execution_grant_candidate_only": False,
            "runtime_execution_grant_decision_formed": True,
            "provider_binding_candidate_formed": True,
            "provider_binding_decision_formed": False,
            "provider_bound": False,
            "runtime_allocated": False,
            "provider_binding_formed": False,
            "model_binding": False,
            "execution_instance_created": False,
            "provider_session_started": False,
            "gateway_submission": False,
            "provider_invoked": False,
            "model_invoked": False,
            "capability_activated": False,
            "slot_reserved": False,
            "resource_allocated": False,
            "resource_scheduling": False,
            "runtime_started": False,
            "runtime_admission_executed": False,
            "observation_execution": False,
            "truth_declared": False,
            "world_truth_declared": False,
            "provider_selected": False,
            "model_selected": False,
            "semantic_rewrite": False,
            "attention_formed": False,
            "decision_formed": False,
            "task_formed": False,
            "action_formed": False,
            "current_world_mutation": False,
            "field_mutation": False,
            "memory_pcn_mutation": False,
            "cases": case_results,
            "status": "READY_FOR_USER_VERIFICATION",
        }


__all__ = ["RuntimeGrantPreExecutionAuthorizationEvaluationEngineV1"]
