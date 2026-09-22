"""Controlled synthetic Provider session/invocation evaluation engine."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass, replace
from typing import Any

from capabilities.evaluation.provider_binding_runtime_allocation_execution_instance_controlled.fixtures_v1 import (
    CONTEXT as SOURCE_CONTEXT,
    PROBLEM as SOURCE_PROBLEM,
    STATE as SOURCE_STATE,
    build_provider_binding_runtime_allocation_execution_cases_v1,
)
from capabilities.evaluation.runtime_grant_pre_execution_authorization_controlled.fixtures_v1 import (
    build_controlled_canonical_runtime_scope_v1,
)
from capabilities.midplatform.core.runtime_executor.runtime_allocation_execution_instance_v1 import (
    ExecutionInstanceInputV1,
    RuntimeAllocationInputV1,
    create_execution_instances,
    form_runtime_allocation_records,
)
from capabilities.midplatform.core.runtime_executor.runtime_allocation_preparation_candidate_v1 import (
    ExecutionInstancePreparationInputV1,
    RuntimeAllocationPreparationInputV1,
    form_execution_instance_preparation_candidates,
    form_runtime_allocation_preparation_candidates,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    build_pregrant_authority_binding_key,
    RuntimeExecutionGrantInputV1,
    form_runtime_execution_grants,
)
from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    form_runtime_safety_prerequisite_v1,
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
from capabilities.midplatform.provider_runtime_governance.provider_runtime_session_invocation_v1 import (
    ProviderInvocationInputV1,
    ProviderRuntimeSessionInputV1,
    create_provider_runtime_session,
    start_controlled_provider_invocation,
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
)

from .fixtures_v1 import (
    CONTEXT,
    EVALUATION_MARKER,
    OWNER,
    PHASE,
    PROBLEM,
    STATE,
    SessionCaseV1,
    build_provider_session_cases_v1,
    valid_authority_records,
    valid_profile,
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


def _source_chain(case: SessionCaseV1, source_case: Any) -> dict[str, Any]:
    suffix = case.case_id.lower()
    canonical_scope = build_controlled_canonical_runtime_scope_v1(
        f"provider-session:{suffix}"
    )
    if canonical_scope is None:
        return {
            "grant": type("Unavailable", (), {"decisions": ()})(),
            "binding_decisions": type("Unavailable", (), {"decisions": ()})(),
            "allocation": type("Unavailable", (), {"records": ()})(),
            "instances": type("Unavailable", (), {"instances": ()})(),
        }
    admitted_action_ref, working_envelope_ref, working_envelope_version_ref = canonical_scope
    target_request = ProviderRuntimeTargetPreparationInputV1(
        preparation_ref=f"session-source-target:{suffix}",
        parent_cognitive_problem_ref=SOURCE_PROBLEM,
        source_state_ref=SOURCE_STATE,
        compatibility_candidates=source_case.compatibility_candidates,
        provider_mappings=source_case.provider_mappings,
        context_refs=SOURCE_CONTEXT,
        trace_ref=f"trace:session-source-target:{suffix}",
        provenance_refs=(f"provenance:session-source-target:{suffix}",),
        admitted_action_ref=admitted_action_ref,
        working_envelope_ref=working_envelope_ref,
        working_envelope_version_ref=working_envelope_version_ref,
    )
    target_before = _json_safe(target_request)
    target = form_provider_runtime_target_candidates(target_request)
    target = replace(
        target,
        targets=tuple(
            replace(
                item,
                provider_candidate_ref="provider_openvins",
                capability_candidate_ref="spatial_mapping",
                capability_class_ref="capability-class:spatial-mapping",
            )
            for item in target.targets
        ),
    )
    target_after = _json_safe(target_request)
    binding_prep = form_provider_binding_runtime_preparation_candidates(
        ProviderBindingRuntimePreparationInputV1(
            preparation_ref=f"session-source-binding-prep:{suffix}",
            parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
            source_state_ref=target.source_state_ref,
            provider_target_candidates=target.targets,
            context_refs=target.context_refs,
            trace_ref=f"trace:session-source-binding-prep:{suffix}",
            provenance_refs=(f"provenance:session-source-binding-prep:{suffix}",),
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=working_envelope_ref,
            working_envelope_version_ref=working_envelope_version_ref,
        )
    )
    binding_candidates = form_provider_binding_candidates(
        ProviderBindingCandidateInputV1(
            preparation_ref=f"session-source-binding-candidate:{suffix}",
            parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
            source_state_ref=target.source_state_ref,
            preparation_candidates=binding_prep.candidates,
            context_refs=target.context_refs,
            trace_ref=f"trace:session-source-binding-candidate:{suffix}",
            provenance_refs=(f"provenance:session-source-binding-candidate:{suffix}",),
            runtime_requirement_refs=(f"runtime-requirement:{suffix}",),
            resource_class_refs=(f"resource-class:{suffix}",),
            execution_class_refs=(f"execution-class:{suffix}",),
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=working_envelope_ref,
            working_envelope_version_ref=working_envelope_version_ref,
        )
    )
    allocation_prep = form_runtime_allocation_preparation_candidates(
        RuntimeAllocationPreparationInputV1(
            preparation_ref=f"session-source-allocation-prep:{suffix}",
            parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
            source_state_ref=target.source_state_ref,
            provider_binding_candidates=binding_candidates.candidates,
            context_refs=target.context_refs,
            trace_ref=f"trace:session-source-allocation-prep:{suffix}",
            provenance_refs=(f"provenance:session-source-allocation-prep:{suffix}",),
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=working_envelope_ref,
            working_envelope_version_ref=working_envelope_version_ref,
        )
    )
    execution_prep = form_execution_instance_preparation_candidates(
        ExecutionInstancePreparationInputV1(
            preparation_ref=f"session-source-instance-prep:{suffix}",
            parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
            source_state_ref=target.source_state_ref,
            runtime_allocation_candidates=allocation_prep.candidates,
            runtime_envelope_shape_refs=("runtime-envelope:controlled-provider",),
            context_refs=target.context_refs,
            trace_ref=f"trace:session-source-instance-prep:{suffix}",
            provenance_refs=(f"provenance:session-source-instance-prep:{suffix}",),
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=working_envelope_ref,
            working_envelope_version_ref=working_envelope_version_ref,
        )
    )
    safety_refs = []
    effect_class = "controlled-observation"
    if case.grant_status == "DENIED" or case.grant_validity_status in {"STALE", "EXPIRED", "REVOKED"}:
        effect_class = "blocked-controlled-scenario"
    for execution_candidate in execution_prep.candidates:
        binding_candidate = next(
            item
            for item in binding_candidates.candidates
            if item.provider_binding_candidate_ref == execution_candidate.source_provider_binding_candidate_ref
        )
        binding_key = build_pregrant_authority_binding_key(
            execution_instance_preparation_candidate_ref=execution_candidate.execution_instance_preparation_candidate_ref,
            provider_candidate_ref=binding_candidate.provider_candidate_ref,
            capability_candidate_ref=binding_candidate.capability_candidate_ref,
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=working_envelope_ref,
            working_envelope_version_ref=working_envelope_version_ref,
        )
        safety = form_runtime_safety_prerequisite_v1(
            binding_key=(*binding_key, effect_class),
            effect_class=effect_class,
        )
        safety_refs.append(safety.result_ref)
    grant = form_runtime_execution_grants(
        RuntimeExecutionGrantInputV1(
            grant_request_ref=f"session-source-grant:{suffix}",
            parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
            source_state_ref=target.source_state_ref,
            provider_binding_candidates=binding_candidates.candidates,
            runtime_allocation_candidates=allocation_prep.candidates,
            execution_instance_preparation_candidates=execution_prep.candidates,
            permission_refs=(f"permission:{suffix}",),
            safety_refs=(f"safety:{suffix}",),
            protocol_refs=("protocol:runtime-execution-grant:v1",),
            governance_refs=(f"governance:{suffix}",),
            constraint_refs=(f"constraint:{suffix}",),
            validity_scope=(f"scope:{suffix}",),
            expiry_boundary_ref=f"expiry:{suffix}",
            effect_class=effect_class,
            safety_prerequisite_refs=tuple(safety_refs),
            context_refs=target.context_refs,
            lineage_refs=tuple(
                dict.fromkeys(ref for item in binding_candidates.candidates for ref in item.lineage_refs)
            ),
            provenance_refs=(f"provenance:session-source-grant:{suffix}",),
            trace_ref=f"trace:session-source-grant:{suffix}",
            admitted_action_ref=admitted_action_ref,
            working_envelope_ref=working_envelope_ref,
            working_envelope_version_ref=working_envelope_version_ref,
        )
    )
    valid_grants = tuple(item for item in grant.decisions if item.decision == "GRANTED")
    binding_decisions = form_provider_binding_decisions(
        ProviderBindingDecisionInputV1(
            decision_request_ref=f"session-source-binding-decision:{suffix}",
            binding_candidates=binding_candidates.candidates,
            runtime_grants=valid_grants,
            trace_ref=f"trace:session-source-binding-decision:{suffix}",
            provenance_refs=(f"provenance:session-source-binding-decision:{suffix}",),
        )
    )
    allocation = form_runtime_allocation_records(
        RuntimeAllocationInputV1(
            allocation_request_ref=f"session-source-allocation:{suffix}",
            binding_decisions=binding_decisions.decisions,
            allocation_preparations=allocation_prep.candidates,
            runtime_grants=valid_grants,
            resource_identity_refs=(f"resource:controlled:{suffix}",),
            runtime_ref=f"runtime:controlled:{suffix}",
            trace_ref=f"trace:session-source-allocation:{suffix}",
            provenance_refs=(f"provenance:session-source-allocation:{suffix}",),
        )
    )
    instances = create_execution_instances(
        ExecutionInstanceInputV1(
            instance_request_ref=f"session-source-instance:{suffix}",
            allocation_records=allocation.records,
            execution_preparations=execution_prep.candidates,
            binding_decisions=binding_decisions.decisions,
            runtime_grants=valid_grants,
            trace_ref=f"trace:session-source-instance:{suffix}",
            provenance_refs=(f"provenance:session-source-instance:{suffix}",),
        )
    )
    return {
        "target_request": target_request,
        "target_request_snapshot_before": target_before,
        "target_request_snapshot_after": target_after,
        "target": target,
        "binding_prep": binding_prep,
        "binding_candidates": binding_candidates,
        "allocation_prep": allocation_prep,
        "execution_prep": execution_prep,
        "grant": grant,
        "binding_decisions": binding_decisions,
        "allocation": allocation,
        "instances": instances,
    }


def _mutate_sources(case: SessionCaseV1, chain: dict[str, Any]) -> tuple[Any, Any, Any, Any]:
    grants = chain["grant"].decisions
    bindings = chain["binding_decisions"].decisions
    allocations = chain["allocation"].records
    instances = chain["instances"].instances
    if case.grant_status:
        grants = tuple(
            replace(item, decision=case.grant_status, execution_authorized=case.grant_status == "GRANTED")
            for item in grants
        )
    if case.grant_validity_status:
        grants = tuple(replace(item, validity_status=case.grant_validity_status) for item in grants)
    if case.binding_status:
        bindings = tuple(
            replace(item, decision=case.binding_status, provider_bound=case.binding_status == "BOUND")
            for item in bindings
        )
    if case.binding_validity_status:
        bindings = tuple(replace(item, validity_status=case.binding_validity_status) for item in bindings)
    if case.allocation_status:
        allocations = tuple(
            replace(item, allocation_status=case.allocation_status, runtime_allocated=case.allocation_status == "ALLOCATED")
            for item in allocations
        )
    if case.instance_state:
        instances = tuple(replace(item, state=case.instance_state) for item in instances)
    if case.lineage_mismatch and instances:
        instances = (replace(instances[0], source_provider_binding_ref="provider-binding:other"), *instances[1:])
    return grants, bindings, allocations, instances


def _lifecycle_artifact(sessions: list[Any], invocations: list[Any]) -> dict[str, Any]:
    return {
        "candidate_only": False,
        "read_only": True,
        "truth_declared": False,
        "world_truth_declared": False,
        "runtime_started": False,
        "execution_instance_created": False,
        "provider_session_started": False,
        "resource_allocated": False,
        "mechanical_provider_session_record_created": bool(sessions),
        "provider_invoked": False,
        "model_invoked": False,
        "gateway_submission": False,
        "controlled_invocation_started": bool(invocations),
        "controlled_invocation_completed": any(getattr(item, "status", "") == "COMPLETED" for item in invocations),
        "real_provider_invoked": False,
        "real_model_invoked": False,
        "network_called": False,
        "subprocess_started": False,
        "thread_started": False,
        "socket_used": False,
        "runtime_observation_created": False,
        "evidence_created": False,
    }


class ProviderSessionControlledInvocationEvaluationEngineV1:
    def run(self) -> dict[str, Any]:
        source_cases = {item.case_id: item for item in build_provider_binding_runtime_allocation_execution_cases_v1()}
        profile = valid_profile()
        results = []
        for case in build_provider_session_cases_v1():
            authority_records = case.authority_records or valid_authority_records()
            applicable = resolve_applicable_governance_set(profile, CORE_GOVERNANCE_RULE_REGISTRY_V1)
            preflight = run_governance_preflight(
                profile, CORE_GOVERNANCE_RULE_REGISTRY_V1, authority_records, tuple(profile.protocol_refs)
            )
            sessions: list[Any] = []
            invocations: list[Any] = []
            invocation_results: list[Any] = []
            session_result = None
            if preflight.status == "PASS":
                source = _source_chain(case, source_cases[case.source_case_id])
                grants, bindings, allocations, instances = _mutate_sources(case, source)
                if case.malformed_session:
                    session_result = create_provider_runtime_session(
                        ProviderRuntimeSessionInputV1(
                            session_request_ref=f"session:{case.case_id.lower()}",
                            execution_instance=object(),
                            provider_binding=bindings[0],
                            runtime_grant=grants[0],
                            runtime_allocation=allocations[0],
                            trace_ref=f"trace:session:{case.case_id.lower()}",
                        )
                    )
                else:
                    for index, (binding, grant, allocation, instance) in enumerate(zip(bindings, grants, allocations, instances), start=1):
                        session_result = create_provider_runtime_session(
                            ProviderRuntimeSessionInputV1(
                                session_request_ref=f"session:{case.case_id.lower()}:{index}",
                                execution_instance=instance,
                                provider_binding=binding,
                                runtime_grant=grant,
                                runtime_allocation=allocation,
                                trace_ref=f"trace:session:{case.case_id.lower()}:{index}",
                                provenance_refs=(f"provenance:session:{case.case_id.lower()}:{index}",),
                            )
                        )
                        if session_result.session is not None:
                            sessions.append(session_result.session)
                        if case.invoke and session_result.session is not None:
                            invocation_session = session_result.session
                            if case.duplicate_start:
                                invocation_session = replace(invocation_session, status="STARTED", execution_started=True)
                            invocation_binding = binding
                            invocation_grant = grant
                            invocation_allocation = allocation
                            invocation_instance = instance
                            if case.invocation_grant_status:
                                invocation_grant = replace(invocation_grant, decision=case.invocation_grant_status, execution_authorized=False)
                            if case.invocation_binding_status:
                                invocation_binding = replace(invocation_binding, decision=case.invocation_binding_status, provider_bound=False)
                            if case.invocation_allocation_status:
                                invocation_allocation = replace(invocation_allocation, allocation_status=case.invocation_allocation_status, runtime_allocated=False)
                            if case.invocation_instance_state:
                                invocation_instance = replace(invocation_instance, state=case.invocation_instance_state)
                            invocation_request = ProviderInvocationInputV1(
                                invocation_request_ref=f"invocation:{case.case_id.lower()}:{index}",
                                session=invocation_session,
                                execution_instance=object() if case.malformed_invocation else invocation_instance,
                                provider_binding=invocation_binding,
                                runtime_grant=invocation_grant,
                                runtime_allocation=invocation_allocation,
                                outcome=case.outcome,
                                duplicate_start=case.duplicate_start,
                                trace_ref=f"trace:invocation:{case.case_id.lower()}:{index}",
                                provenance_refs=(f"provenance:invocation:{case.case_id.lower()}:{index}",),
                            )
                            invocation_result = start_controlled_provider_invocation(invocation_request)
                            invocation_results.append(invocation_result)
                            if invocation_result.session is not None:
                                sessions[-1] = invocation_result.session
                            if invocation_result.invocation is not None:
                                invocations.append(invocation_result.invocation)
            else:
                source = {}
                session_result = None
            artifact = _lifecycle_artifact(sessions, invocations)
            postflight = run_governance_postflight(profile, artifact) if preflight.status == "PASS" else None
            results.append({
                "case_id": case.case_id,
                "expected": _json_safe(case),
                "applicable_governance": _json_safe(applicable),
                "governance_preflight": _json_safe(preflight),
                "governance_postflight": _json_safe(postflight),
                "business_engine_executed": preflight.status == "PASS",
                "source_chain": _json_safe(source),
                "session": _json_safe(session_result),
                "sessions": _json_safe(sessions),
                "invocation": _json_safe(invocations[0] if invocations else None),
                "invocations": _json_safe(invocations),
                "invocation_results": _json_safe(invocation_results),
                "lifecycle_artifact": artifact,
            })
        return {
            "phase": PHASE,
            "source_mode": EVALUATION_MARKER,
            "governance_backbone_reused": True,
            "canonical_session_owner": OWNER,
            "canonical_invocation_owner": OWNER,
            "bounded_provider_session_is_candidate": True,
            "synthetic_only": True,
            "controlled": True,
            "no_real_runtime_effect": True,
            "no_real_provider_effect": True,
            "no_real_model_effect": True,
            "execution_started": any(item.get("lifecycle_artifact", {}).get("provider_session_started") for item in results),
            "real_provider_invoked": False,
            "real_model_invoked": False,
            "network_called": False,
            "subprocess_started": False,
            "thread_started": False,
            "socket_used": False,
            "runtime_observation_created": False,
            "gateway_submission": False,
            "evidence_created": False,
            "truth_declared": False,
            "world_truth_declared": False,
            "retry_engine": False,
            "provider_fallback": False,
            "provider_autonomous_continuation": False,
            "cases": results,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = ["PHASE", "ProviderSessionControlledInvocationEvaluationEngineV1"]
