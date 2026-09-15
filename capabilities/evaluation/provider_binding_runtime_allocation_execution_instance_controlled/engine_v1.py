"""Controlled engine for authoritative binding/allocation/identity records."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass, replace
from typing import Any

from capabilities.midplatform.core.runtime_executor.runtime_allocation_execution_instance_v1 import (
    ExecutionInstanceInputV1,
    RuntimeAllocationInputV1,
    create_execution_instances,
    form_runtime_allocation_records,
    release_runtime_allocation,
)
from capabilities.midplatform.core.runtime_executor.runtime_allocation_preparation_candidate_v1 import (
    ExecutionInstancePreparationInputV1,
    RuntimeAllocationPreparationInputV1,
    form_execution_instance_preparation_candidates,
    form_runtime_allocation_preparation_candidates,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    RuntimeExecutionGrantInputV1,
    form_runtime_execution_grants,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_candidate_v1 import (
    ProviderBindingCandidateInputV1,
    form_provider_binding_candidates,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_decision_v1 import (
    ProviderBindingDecisionInputV1,
    form_provider_binding_decisions,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_runtime_preparation_v1 import (
    ProviderBindingRuntimePreparationInputV1,
    form_provider_binding_runtime_preparation_candidates,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_target_preparation_v1 import (
    ProviderRuntimeTargetPreparationInputV1,
    form_provider_runtime_target_candidates,
)
from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    CORE_GOVERNANCE_RULE_REGISTRY_V1,
    resolve_applicable_governance_set,
    run_governance_postflight,
    run_governance_preflight,
    validate_failure_ownership,
    validate_requester_executor_boundary,
)

from .fixtures_v1 import (
    CONTEXT,
    EVALUATION_MARKER,
    PROBLEM,
    STATE,
    build_provider_binding_runtime_allocation_execution_cases_v1,
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


def _target_request(case: Any) -> ProviderRuntimeTargetPreparationInputV1:
    return ProviderRuntimeTargetPreparationInputV1(
        preparation_ref=f"execution-target:{case.case_id.lower()}",
        parent_cognitive_problem_ref=PROBLEM,
        source_state_ref=STATE,
        compatibility_candidates=case.compatibility_candidates,
        provider_mappings=case.provider_mappings,
        context_refs=CONTEXT,
        trace_ref=f"trace:execution-target:{case.case_id.lower()}",
        provenance_refs=(f"provenance:execution-target:{case.case_id.lower()}",),
    )


def _empty_pipeline(case: Any, target_request: Any, target: Any) -> dict[str, Any]:
    return {
        "target_request_snapshot_before": _json_safe(target_request),
        "target_request_snapshot_after": _json_safe(target_request),
        "target_preparation": _json_safe(target),
        "binding_preparation": None,
        "binding_candidate": None,
        "allocation_preparation": None,
        "execution_preparation": None,
        "grant": None,
        "binding_decision": None,
        "allocation": None,
        "execution_instance": None,
        "business_engine_executed": True,
        "pipeline_status": getattr(target, "formation_status", "INVALID_INPUT"),
    }


def _run_pipeline(case: Any, *, include_replay: bool = True) -> dict[str, Any]:
    target_request = _target_request(case)
    target_before = _json_safe(target_request)
    target = form_provider_runtime_target_candidates(target_request)
    target_after = _json_safe(target_request)
    if target.formation_status != "PROVIDER_TARGET_CANDIDATES_FORMED":
        result = _empty_pipeline(case, target_request, target)
        result["target_request_snapshot_before"] = target_before
        result["target_request_snapshot_after"] = target_after
        return result

    binding_prep_request = ProviderBindingRuntimePreparationInputV1(
        preparation_ref=f"binding-prep:{case.case_id.lower()}",
        parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
        source_state_ref=target.source_state_ref,
        provider_target_candidates=target.targets,
        context_refs=target.context_refs,
        trace_ref=f"trace:binding-prep:{case.case_id.lower()}",
        provenance_refs=(f"provenance:binding-prep:{case.case_id.lower()}",),
    )
    binding_prep = form_provider_binding_runtime_preparation_candidates(binding_prep_request)
    if not binding_prep.candidates:
        return {
            "target_request_snapshot_before": target_before, "target_request_snapshot_after": target_after,
            "target_preparation": _json_safe(target), "binding_preparation": _json_safe(binding_prep),
            "binding_candidate": None, "allocation_preparation": None, "execution_preparation": None,
            "grant": None, "binding_decision": None, "allocation": None, "execution_instance": None,
            "business_engine_executed": True, "pipeline_status": binding_prep.formation_status,
        }

    binding_candidate_request = ProviderBindingCandidateInputV1(
        preparation_ref=f"binding-candidate:{case.case_id.lower()}",
        parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
        source_state_ref=target.source_state_ref,
        preparation_candidates=binding_prep.candidates,
        context_refs=target.context_refs,
        trace_ref=f"trace:binding-candidate:{case.case_id.lower()}",
        provenance_refs=(f"provenance:binding-candidate:{case.case_id.lower()}",),
        runtime_requirement_refs=(f"runtime-requirement:{case.case_id.lower()}",),
        resource_class_refs=(f"resource-class:{case.case_id.lower()}",),
        execution_class_refs=(f"execution-class:{case.case_id.lower()}",),
    )
    binding_candidate = form_provider_binding_candidates(binding_candidate_request)
    if not binding_candidate.candidates:
        return {
            "target_request_snapshot_before": target_before, "target_request_snapshot_after": target_after,
            "target_preparation": _json_safe(target), "binding_preparation": _json_safe(binding_prep),
            "binding_candidate": _json_safe(binding_candidate), "allocation_preparation": None,
            "execution_preparation": None, "grant": None, "binding_decision": None,
            "allocation": None, "execution_instance": None, "business_engine_executed": True,
            "pipeline_status": binding_candidate.formation_status,
        }

    allocation_prep_request = RuntimeAllocationPreparationInputV1(
        preparation_ref=f"allocation-prep:{case.case_id.lower()}",
        parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
        source_state_ref=target.source_state_ref,
        provider_binding_candidates=binding_candidate.candidates,
        context_refs=target.context_refs,
        trace_ref=f"trace:allocation-prep:{case.case_id.lower()}",
        provenance_refs=(f"provenance:allocation-prep:{case.case_id.lower()}",),
    )
    allocation_prep = form_runtime_allocation_preparation_candidates(allocation_prep_request)
    execution_prep_request = ExecutionInstancePreparationInputV1(
        preparation_ref=f"instance-prep:{case.case_id.lower()}",
        parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
        source_state_ref=target.source_state_ref,
        runtime_allocation_candidates=allocation_prep.candidates,
        runtime_envelope_shape_refs=("runtime-envelope:observation",),
        context_refs=target.context_refs,
        trace_ref=f"trace:instance-prep:{case.case_id.lower()}",
        provenance_refs=(f"provenance:instance-prep:{case.case_id.lower()}",),
    )
    execution_prep = form_execution_instance_preparation_candidates(execution_prep_request)
    grant_request = RuntimeExecutionGrantInputV1(
        grant_request_ref=f"grant-request:{case.case_id.lower()}",
        parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
        source_state_ref=target.source_state_ref,
        provider_binding_candidates=binding_candidate.candidates,
        runtime_allocation_candidates=allocation_prep.candidates,
        execution_instance_preparation_candidates=execution_prep.candidates,
        permission_refs=(f"permission:{case.case_id.lower()}",),
        safety_refs=(f"safety:{case.case_id.lower()}",),
        protocol_refs=("protocol:runtime-execution-grant:v1",),
        governance_refs=(f"governance:{case.case_id.lower()}",),
        constraint_refs=(f"constraint:{case.case_id.lower()}",),
        validity_scope=(f"scope:{case.case_id.lower()}",),
        expiry_boundary_ref=f"expiry:{case.case_id.lower()}",
        provider_binding_status=case.provider_binding_status,
        capability_admission_status=case.capability_admission_status,
        permission_status=case.permission_status,
        safety_status=case.safety_status,
        constitution_status=case.constitution_status,
        resource_feasibility_status=case.grant_resource_feasibility_status or "SATISFIABLE",
        runtime_boundary_status=case.runtime_boundary_status,
        freshness_status=case.freshness_status,
        validity_status=case.validity_status,
        execution_ready=case.execution_ready,
        context_refs=target.context_refs,
        lineage_refs=tuple(dict.fromkeys(ref for item in binding_candidate.candidates for ref in item.lineage_refs)),
        provenance_refs=(f"provenance:grant:{case.case_id.lower()}",),
        trace_ref=f"trace:grant:{case.case_id.lower()}",
    )
    if case.malformed_grant:
        grant_request = replace(grant_request, execution_instance_preparation_candidates=execution_prep.candidates[0] if execution_prep.candidates else ())
    grant = form_runtime_execution_grants(grant_request)
    valid_grants = tuple(item for item in grant.decisions if item.decision == "GRANTED")
    if not valid_grants:
        return {
            "target_request_snapshot_before": target_before, "target_request_snapshot_after": target_after,
            "target_preparation": _json_safe(target), "binding_preparation": _json_safe(binding_prep),
            "binding_candidate": _json_safe(binding_candidate), "allocation_preparation": _json_safe(allocation_prep),
            "execution_preparation": _json_safe(execution_prep), "grant": _json_safe(grant),
            "binding_decision": None, "allocation": None, "execution_instance": None,
            "business_engine_executed": True, "pipeline_status": grant.formation_status,
        }

    binding_decision_request = ProviderBindingDecisionInputV1(
        decision_request_ref=f"binding-decision:{case.case_id.lower()}",
        binding_candidates=binding_candidate.candidates,
        runtime_grants=valid_grants,
        provider_eligibility_status=case.provider_eligibility_status,
        binding_status=case.binding_status,
        validity_status=case.binding_validity_status,
        constraint_refs=(f"constraint:binding:{case.case_id.lower()}",),
        trace_ref=f"trace:binding-decision:{case.case_id.lower()}",
        provenance_refs=(f"provenance:binding-decision:{case.case_id.lower()}",),
    )
    binding_decision = form_provider_binding_decisions(binding_decision_request)
    allocation_request = RuntimeAllocationInputV1(
        allocation_request_ref=f"allocation:{case.case_id.lower()}",
        binding_decisions=binding_decision.decisions,
        allocation_preparations=allocation_prep.candidates,
        runtime_grants=valid_grants,
        resource_feasibility_status=case.resource_feasibility_status,
        allocation_outcome=case.allocation_outcome,
        resource_identity_refs=(f"resource:controlled:{case.case_id.lower()}",),
        runtime_ref=f"runtime:controlled:{case.case_id.lower()}",
        trace_ref=f"trace:allocation:{case.case_id.lower()}",
        provenance_refs=(f"provenance:allocation:{case.case_id.lower()}",),
    )
    allocation = form_runtime_allocation_records(allocation_request)
    if case.release_allocation:
        allocation = replace(allocation, records=tuple(release_runtime_allocation(item) for item in allocation.records), allocation_refs=tuple(item.allocation_ref for item in allocation.records))
    if case.no_instance:
        execution_instance = None
    else:
        instance_grants = valid_grants
        instance_bindings = binding_decision.decisions
        if case.revoke_grant_before_instance:
            instance_grants = tuple(replace(item, decision="REVOKED", validity_status="REVOKED") for item in valid_grants)
        if case.revoke_binding_before_instance:
            instance_bindings = tuple(replace(item, decision="REVOKED", provider_bound=False) for item in binding_decision.decisions)
        execution_instance = create_execution_instances(ExecutionInstanceInputV1(
            instance_request_ref=f"instance:{case.case_id.lower()}",
            allocation_records=allocation.records,
            execution_preparations=execution_prep.candidates,
            binding_decisions=instance_bindings,
            runtime_grants=instance_grants,
            trace_ref=f"trace:instance:{case.case_id.lower()}",
            provenance_refs=(f"provenance:instance:{case.case_id.lower()}",),
        ))
    result = {
        "target_request_snapshot_before": target_before, "target_request_snapshot_after": target_after,
        "target_preparation": _json_safe(target), "binding_preparation": _json_safe(binding_prep),
        "binding_candidate": _json_safe(binding_candidate), "allocation_preparation": _json_safe(allocation_prep),
        "execution_preparation": _json_safe(execution_prep), "grant": _json_safe(grant),
        "binding_decision": _json_safe(binding_decision), "allocation": _json_safe(allocation),
        "execution_instance": _json_safe(execution_instance), "business_engine_executed": True,
        "pipeline_status": "EXECUTION_INSTANCE_PIPELINE_COMPLETE",
    }
    if case.case_id == "DETERMINISTIC_REPLAY" and include_replay:
        replay = _run_pipeline(case, include_replay=False)
        result["deterministic_replay"] = replay.get("execution_instance")
    return result


def _postflight_artifact(pipeline: dict[str, Any]) -> dict[str, Any]:
    binding = pipeline.get("binding_decision") or {}
    allocation = pipeline.get("allocation") or {}
    instance = pipeline.get("execution_instance") or {}
    bound = any(item.get("provider_bound") for item in binding.get("decisions", ()))
    allocated = any(item.get("allocation_status") == "ALLOCATED" for item in allocation.get("records", ()))
    created = bool(instance.get("instances"))
    return {
        "candidate_only": False, "read_only": True, "truth_declared": False,
        "world_truth_declared": False, "provider_binding_authoritative": bound,
        "runtime_allocation_authoritative": allocated,
        "execution_instance_created": False,
        "runtime_started": False, "resource_allocated": False, "provider_session_started": False,
        "mechanical_execution_identity_record_created": created,
        "mechanical_resource_allocation_record_created": allocated,
        "provider_invoked": False, "model_invoked": False, "gateway_submission": False,
        "observation_produced": False, "evidence_produced": False,
    }


class ProviderBindingRuntimeAllocationExecutionEvaluationEngineV1:
    def run(self) -> dict[str, Any]:
        results = []
        for case in build_provider_binding_runtime_allocation_execution_cases_v1():
            applicable = resolve_applicable_governance_set(case.profile, CORE_GOVERNANCE_RULE_REGISTRY_V1)
            preflight = run_governance_preflight(case.profile, CORE_GOVERNANCE_RULE_REGISTRY_V1, case.authority_records, tuple(case.profile.protocol_refs))
            if preflight.status == "PASS":
                pipeline = _run_pipeline(case)
                artifact = case.postflight_artifact or _postflight_artifact(pipeline)
                postflight = run_governance_postflight(case.profile, artifact)
                boundary_errors = validate_requester_executor_boundary(case.boundary_payload or {})
                failure_errors = validate_failure_ownership(case.failure_ownership_payload or {})
                if boundary_errors or failure_errors:
                    postflight = replace(postflight, status="GOVERNANCE_POSTFLIGHT_BLOCKED", blocker_refs=tuple(dict.fromkeys((*postflight.blocker_refs, *boundary_errors, *failure_errors))))
            else:
                pipeline = {"business_engine_executed": False, "binding_decision": None, "allocation": None, "execution_instance": None, "target_request_snapshot_before": _json_safe(_target_request(case)), "target_request_snapshot_after": _json_safe(_target_request(case))}
                postflight = None
            results.append({
                "case_id": case.case_id, "expected": {"binding_status": case.expected_binding_status, "binding_count": case.expected_binding_count, "bound_count": case.expected_bound_count, "allocation_status": case.expected_allocation_status, "allocation_count": case.expected_allocation_count, "allocated_count": case.expected_allocated_count, "instance_status": case.expected_instance_status, "instance_count": case.expected_instance_count},
                "applicable_rule_count": len(applicable.resolved_rule_refs),
                "resolved_rule_refs": list(applicable.resolved_rule_refs),
                "applicable_governance": _json_safe(applicable), "governance_preflight": _json_safe(preflight), "governance_postflight": _json_safe(postflight),
                "business_engine_executed": pipeline.get("business_engine_executed", True),
                "boundary_errors": list(validate_requester_executor_boundary(case.boundary_payload or {})),
                "failure_ownership_errors": list(validate_failure_ownership(case.failure_ownership_payload or {})),
                **pipeline,
            })
        return {
            "phase": "Phase-Provider-Binding-Runtime-Allocation-Execution-Instance-Controlled-Implementation-v1-001",
            "source_mode": EVALUATION_MARKER,
            "governance_backbone_reused": True,
            "governance_rule_registry_ref": CORE_GOVERNANCE_RULE_REGISTRY_V1.registry_ref,
            "preflight_before_business_engine": True,
            "canonical_provider_binding_owner": "Provider Governance",
            "canonical_runtime_allocation_owner": "Runtime Executor",
            "canonical_execution_instance_owner": "Runtime Executor",
            "provider_binding_authoritative": True,
            "runtime_allocation_authoritative": True,
            "execution_instance_authoritative": True,
            "candidate_only": False,
            "read_only": True,
            "runtime_started": False,
            "provider_session_started": False,
            "provider_invocation": False,
            "model_invocation": False,
            "gateway_submission": False,
            "observation_produced": False,
            "evidence_produced": False,
            "truth_declared": False,
            "world_truth_declared": False,
            "synthetic_controlled_no_real_resource_effect": True,
            "cases": results,
            "status": "READY_FOR_USER_VERIFICATION",
        }


__all__ = ["ProviderBindingRuntimeAllocationExecutionEvaluationEngineV1"]
