"""Focused adjudication for GPT6-G06 Runtime Grant authority origin."""

from dataclasses import replace

import pytest

import capabilities.midplatform.core.action_governance.action_governance_engine_v1 as safety_owner

from capabilities.evaluation.runtime_grant_pre_execution_authorization_controlled.fixtures_v1 import (
    build_runtime_grant_cases_v1,
)
from capabilities.evaluation.perception_provider_runtime_target_preparation_controlled.fixtures_v1 import (
    build_provider_runtime_target_preparation_cases_v1,
)
from capabilities.midplatform.core.runtime_executor.runtime_allocation_preparation_candidate_v1 import (
    ExecutionInstancePreparationInputV1,
    RuntimeAllocationPreparationInputV1,
    form_execution_instance_preparation_candidates,
    form_runtime_allocation_preparation_candidates,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_authorization_state_v1 import (
    query_active_authorization_for_grant,
    query_current_effect_eligibility_for_grant,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    RuntimeExecutionGrantInputV1,
    build_pregrant_authority_binding_key,
    form_runtime_execution_grants,
    invalidate_runtime_authorization_state,
)
from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    ActionGovernanceEngineV1,
    form_runtime_safety_prerequisite_v1,
    invalidate_runtime_safety_prerequisite_v1,
    query_current_runtime_safety_prerequisite_v1,
)
from capabilities.midplatform.core.action_governance.action_admission_governance_v1 import (
    ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL,
    admit_action_v1,
)
from capabilities.midplatform.core.action_governance.action_io_types_v1 import (
    ActionGovernanceInputV1,
)
from capabilities.midplatform.core.brain_governance.concern_governance_v1 import (
    BRAIN_PRODUCTION_PROFILE_REF,
    admit_concern,
)
from capabilities.midplatform.core.brain_governance.cognitive_grant_governance_v1 import (
    issue_cognitive_grant,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.a_working_envelope_cognitive_requirement_engine_v1 import (
    build_working_envelope,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.working_envelope_governance_v1 import (
    WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL,
    admit_working_envelope_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.decision_to_task_manager_controlled_handoff.engine_v1 import (
    build_decision_task_run_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.task_to_action_boundary_controlled_handoff.engine_v1 import (
    _action_request,
    _build_task_to_action_handoff,
)
from capabilities.midplatform.core.cognitive_state_formation import (
    issue_cognitive_state_version_v1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_engine_v1 import (
    CognitiveStateFormationEngineV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_registry_v1 import (
    COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_candidate_v1 import (
    ProviderBindingCandidateInputV1,
    form_provider_binding_candidates,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_runtime_preparation_v1 import (
    ProviderBindingRuntimePreparationInputV1,
    form_provider_binding_runtime_preparation_candidates,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_target_preparation_v1 import (
    form_provider_runtime_target_candidates,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_registry_v1 import (
    evaluate_provider_runtime_eligibility_v1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_resolution_v1 import (
    evaluate_runtime_capability_admission_v1,
)
from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    evaluate_runtime_protocol_compliance_v1,
)


def _canonical_runtime_scope(case: str):
    concern = admit_concern(
        request_ref=f"request:{case}",
        goal_ref=f"goal:{case}",
        intent_ref=f"intent:{case}",
        scope_ref=f"scope:{case}",
        basis_refs=(f"basis:{case}",),
        policy_refs=(f"policy:{case}",),
        profile_ref=BRAIN_PRODUCTION_PROFILE_REF,
    )
    assert concern is not None
    grant = issue_cognitive_grant(
        concern_ref=concern.concern_ref,
        receiver_ref=f"receiver:{case}",
        receiver_role="A_REASONING_ROLE",
        granted_authority_refs=("REALITY_REASONING",),
        work_ref=f"work:{case}",
        scope_ref=f"scope:{case}",
        expiry_ref=f"expiry:{case}",
        basis_refs=(f"grant-basis:{case}",),
        policy_refs=(f"grant-policy:{case}",),
        profile_ref=BRAIN_PRODUCTION_PROFILE_REF,
    )
    assert grant is not None

    def _ref(owner: str, value: str) -> SourceRefV1:
        return SourceRefV1(owner, value, "v1", f"trace:{value}", f"provenance:{value}")

    state = CognitiveStateFormationEngineV1().run_case(
        CognitiveStateFormationInputV1(
            scenario_id="F09",
            context_refs=(_ref("Context", f"context:{case}"),),
            pcn_refs=(_ref("PCN", f"pcn:{case}"),),
            intent_refs=(_ref("Intent", f"intent:{case}"),),
            field_refs=(_ref("Field", f"field:{case}"),),
            observation_refs=(_ref("Observation", f"observation:{case}"),),
            evidence_refs=(_ref("Evidence", f"evidence:{case}"),),
            goal_refs=(_ref("Goal", f"goal:{case}"),),
            concern_refs=(_ref("Concern", f"concern:{case}"),),
            information_need_refs=(_ref("Need", f"need:{case}"),),
            task_refs=(_ref("Task", f"task:{case}"),),
            role_refs=(_ref("Role", f"role:{case}"),),
            relation_refs=(_ref("Field", f"relation:{case}"),),
            candidate_only=True,
            synthetic_only=True,
        )
    )
    state_version = issue_cognitive_state_version_v1(
        state,
        profile_ref=COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL,
    )
    assert state_version is not None
    envelope = admit_working_envelope_v1(
        build_working_envelope(
            work_ref=f"work:{case}",
            concern_ref=concern.concern_ref,
            authority_grant_ref=grant.grant_ref,
            source_state_version_ref=state_version.version_ref,
            goal_refs=(f"goal:{case}",),
            context_refs=(f"context:{case}",),
            current_world_refs=(f"world:{case}:v1",),
            field_refs=(f"field:{case}",),
        ),
        profile_ref=WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL,
    )
    assert envelope is not None
    task_summary = build_decision_task_run_v1(
        f"action-runtime:{case}",
        working_envelope=envelope,
    )
    task_case = next(
        item for item in task_summary["cases"] if item["case_id"] == "CASE_A_SUFFICIENT_STOP"
    )
    task_handoff, errors = _build_task_to_action_handoff(
        {**task_case, "resource_state": "available"}
    )
    assert not errors and task_handoff is not None
    action_request = _action_request(task_handoff)
    action_request["scenario_id"] = f"action-runtime:{case}"
    action_output = ActionGovernanceEngineV1().run_case(
        ActionGovernanceInputV1(**action_request)
    )
    safety_key = (
        action_output.action_candidate.action_candidate_id,
        task_handoff.task_state_ref,
        task_handoff.decision_candidate_ref,
        envelope.envelope_ref,
        envelope.envelope_version_ref,
        "runtime-execution",
    )
    safety = form_runtime_safety_prerequisite_v1(
        binding_key=safety_key,
        effect_class="runtime-execution",
        scope_kind="ACTION_ADMISSION",
    )
    admitted_action = admit_action_v1(
        action_output,
        task_handoff=task_handoff,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
        safety_prerequisite=safety,
        profile_ref=ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL,
    )
    assert admitted_action is not None
    return admitted_action, envelope, state


def _public_candidate_chain():
    case = build_runtime_grant_cases_v1()[0]
    admitted_action, envelope, state = _canonical_runtime_scope("gpt6-g06")
    target = form_provider_binding_runtime_preparation_candidates(
        ProviderBindingRuntimePreparationInputV1(
            preparation_ref="gpt6-g06-target",
            parent_cognitive_problem_ref=case.target_candidates[0].parent_cognitive_problem_ref,
            source_state_ref=case.target_candidates[0].source_state_ref,
            provider_target_candidates=tuple(case.target_candidates),
            context_refs=case.target_candidates[0].context_refs,
            trace_ref="trace:gpt6-g06-target",
            provenance_refs=("provenance:gpt6-g06-target",),
        )
    )
    binding = form_provider_binding_candidates(
        ProviderBindingCandidateInputV1(
            preparation_ref="gpt6-g06-binding",
            parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
            source_state_ref=target.source_state_ref,
            preparation_candidates=target.candidates,
            context_refs=target.context_refs,
            trace_ref="trace:gpt6-g06-binding",
            provenance_refs=("provenance:gpt6-g06-binding",),
            runtime_requirement_refs=("runtime-requirement:gpt6-g06",),
            resource_class_refs=("resource-class:gpt6-g06",),
            execution_class_refs=("execution-class:gpt6-g06",),
        )
    )
    allocation = form_runtime_allocation_preparation_candidates(
        RuntimeAllocationPreparationInputV1(
            preparation_ref="gpt6-g06-allocation",
            parent_cognitive_problem_ref=binding.parent_cognitive_problem_ref,
            source_state_ref=binding.source_state_ref,
            provider_binding_candidates=binding.candidates,
            context_refs=target.context_refs,
            trace_ref="trace:gpt6-g06-allocation",
            provenance_refs=("provenance:gpt6-g06-allocation",),
        )
    )
    execution = form_execution_instance_preparation_candidates(
        ExecutionInstancePreparationInputV1(
            preparation_ref="gpt6-g06-execution",
            parent_cognitive_problem_ref=allocation.parent_cognitive_problem_ref,
            source_state_ref=allocation.source_state_ref,
            runtime_allocation_candidates=allocation.candidates,
            runtime_envelope_shape_refs=("runtime-envelope:gpt6-g06",),
            context_refs=target.context_refs,
            trace_ref="trace:gpt6-g06-execution",
            provenance_refs=("provenance:gpt6-g06-execution",),
        )
    )
    return case, binding, allocation, execution, admitted_action, envelope, state


def test_v2_scope_accepts_empty_legacy_metadata_through_all_preparation_sites():
    source_case = build_provider_runtime_target_preparation_cases_v1()[0]
    admitted_action, envelope, _ = _canonical_runtime_scope("g06-legacy-extinction")
    scope = {
        "admitted_action_ref": admitted_action.admitted_action_ref,
        "working_envelope_ref": envelope.envelope_ref,
        "working_envelope_version_ref": envelope.envelope_version_ref,
    }
    target_request = replace(
        source_case.request,
        parent_cognitive_problem_ref="",
        source_state_ref="",
        compatibility_candidates=tuple(
            replace(candidate, parent_cognitive_problem_ref="", source_state_ref="")
            for candidate in source_case.request.compatibility_candidates
        ),
        **scope,
    )
    target = form_provider_runtime_target_candidates(target_request)
    assert target.targets
    target_candidate = replace(
        target.targets[0],
        parent_cognitive_problem_ref="",
        source_state_ref="",
    )

    binding_preparation = form_provider_binding_runtime_preparation_candidates(
        ProviderBindingRuntimePreparationInputV1(
            preparation_ref="g06-legacy-extinction-binding-preparation",
            parent_cognitive_problem_ref="",
            source_state_ref="",
            provider_target_candidates=(target_candidate,),
            context_refs=target_request.context_refs,
            trace_ref="trace:g06-legacy-extinction-binding-preparation",
            provenance_refs=("provenance:g06-legacy-extinction-binding-preparation",),
            **scope,
        )
    )
    assert binding_preparation.candidates
    binding_candidates = tuple(
        replace(candidate, parent_cognitive_problem_ref="", source_state_ref="")
        for candidate in binding_preparation.candidates
    )

    binding = form_provider_binding_candidates(
        ProviderBindingCandidateInputV1(
            preparation_ref="g06-legacy-extinction-binding",
            parent_cognitive_problem_ref="",
            source_state_ref="",
            preparation_candidates=binding_candidates,
            context_refs=target_request.context_refs,
            trace_ref="trace:g06-legacy-extinction-binding",
            provenance_refs=("provenance:g06-legacy-extinction-binding",),
            runtime_requirement_refs=("runtime-requirement:g06-legacy-extinction",),
            resource_class_refs=("resource-class:g06-legacy-extinction",),
            execution_class_refs=("execution-class:g06-legacy-extinction",),
            **scope,
        )
    )
    assert binding.candidates
    allocation = form_runtime_allocation_preparation_candidates(
        RuntimeAllocationPreparationInputV1(
            preparation_ref="g06-legacy-extinction-allocation",
            parent_cognitive_problem_ref="",
            source_state_ref="",
            provider_binding_candidates=tuple(
                replace(candidate, parent_cognitive_problem_ref="", source_state_ref="")
                for candidate in binding.candidates
            ),
            context_refs=target_request.context_refs,
            trace_ref="trace:g06-legacy-extinction-allocation",
            provenance_refs=("provenance:g06-legacy-extinction-allocation",),
            **scope,
        )
    )
    assert allocation.candidates, allocation.validation_errors
    execution = form_execution_instance_preparation_candidates(
        ExecutionInstancePreparationInputV1(
            preparation_ref="g06-legacy-extinction-execution",
            parent_cognitive_problem_ref="",
            source_state_ref="",
            runtime_allocation_candidates=tuple(
                replace(candidate, parent_cognitive_problem_ref="", source_state_ref="")
                for candidate in allocation.candidates
            ),
            runtime_envelope_shape_refs=("runtime-envelope:g06-legacy-extinction",),
            context_refs=target_request.context_refs,
            trace_ref="trace:g06-legacy-extinction-execution",
            provenance_refs=("provenance:g06-legacy-extinction-execution",),
            **scope,
        )
    )
    assert execution.candidates

    for candidate in (
        target.targets[0],
        binding_preparation.candidates[0],
        binding.candidates[0],
        allocation.candidates[0],
        execution.candidates[0],
    ):
        assert (
            candidate.admitted_action_ref,
            candidate.working_envelope_ref,
            candidate.working_envelope_version_ref,
        ) == (
            scope["admitted_action_ref"],
            scope["working_envelope_ref"],
            scope["working_envelope_version_ref"],
        )


def test_public_grant_path_requires_current_owner_prerequisites():
    case, binding, allocation, execution, admitted_action, envelope, state = _public_candidate_chain()
    canonical_binding = replace(
        binding.candidates[0],
        provider_candidate_ref="provider_openvins",
        capability_candidate_ref="spatial_mapping",
        capability_class_ref="capability-class:spatial-mapping",
        admitted_action_ref=admitted_action.admitted_action_ref,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
    )
    canonical_allocation = replace(
        allocation.candidates[0],
        provider_candidate_ref=canonical_binding.provider_candidate_ref,
        capability_candidate_ref=canonical_binding.capability_candidate_ref,
        capability_class_ref=canonical_binding.capability_class_ref,
        admitted_action_ref=admitted_action.admitted_action_ref,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
    )
    canonical_execution = replace(
        execution.candidates[0],
        provider_candidate_ref=canonical_binding.provider_candidate_ref,
        capability_candidate_ref=canonical_binding.capability_candidate_ref,
        capability_class_ref=canonical_binding.capability_class_ref,
        admitted_action_ref=admitted_action.admitted_action_ref,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
    )
    request = RuntimeExecutionGrantInputV1(
        grant_request_ref="gpt6-g06-grant",
        parent_cognitive_problem_ref=execution.parent_cognitive_problem_ref,
        source_state_ref=execution.source_state_ref,
        provider_binding_candidates=(canonical_binding,),
        runtime_allocation_candidates=(canonical_allocation,),
        execution_instance_preparation_candidates=(canonical_execution,),
        permission_refs=("permission:gpt6-g06",),
        safety_refs=("safety:gpt6-g06",),
        protocol_refs=("protocol:runtime-execution-grant:v1",),
        governance_refs=("governance:gpt6-g06",),
        constraint_refs=("constraint:gpt6-g06",),
        validity_scope=("scope:gpt6-g06",),
        expiry_boundary_ref="expiry:gpt6-g06",
        trace_ref="trace:gpt6-g06-grant",
        provenance_refs=("provenance:gpt6-g06-grant",),
        grant_authority_ref=case.grant_authority_ref,
        grant_responsibility_ref=case.grant_responsibility_ref,
        admitted_action_ref=admitted_action.admitted_action_ref,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
    )

    result = form_runtime_execution_grants(request)
    assert result.formation_status == "INVALID_INPUT"
    assert not result.decisions
    assert "safety_prerequisite_missing" in result.validation_errors

    binding_key = build_pregrant_authority_binding_key(
        execution_instance_preparation_candidate_ref=canonical_execution.execution_instance_preparation_candidate_ref,
        provider_candidate_ref=canonical_binding.provider_candidate_ref,
        capability_candidate_ref=canonical_binding.capability_candidate_ref,
        admitted_action_ref=request.admitted_action_ref,
        working_envelope_ref=request.working_envelope_ref,
        working_envelope_version_ref=request.working_envelope_version_ref,
    )
    safety = form_runtime_safety_prerequisite_v1(
        binding_key=(*binding_key, request.effect_class),
        effect_class=request.effect_class,
    )
    authorized_request = replace(
        request,
        safety_prerequisite_ref=safety.result_ref,
    )
    authorized = form_runtime_execution_grants(authorized_request)
    assert authorized.decisions
    grant = authorized.decisions[0]
    assert grant.decision == "GRANTED"
    runtime_authorization_state = query_active_authorization_for_grant(grant)
    assert runtime_authorization_state is not None
    assert runtime_authorization_state.scope.runtime_safety_prerequisite_ref == safety.result_ref
    assert runtime_authorization_state.scope.runtime_safety_binding_key == safety.binding_key
    eligibility = query_current_effect_eligibility_for_grant(grant)
    assert eligibility.eligible is True
    assert eligibility.failure_code is None

    # Diagnostic presence, contents and shape cannot gate canonical issuance.
    for diagnostic_refs in (
        (), ("diagnostic:a", "diagnostic:b"), ("diagnostic:b", "diagnostic:a"),
        ("diagnostic:replacement",), None, False, ("diagnostic:valid", None, []),
    ):
        diagnostic_result = form_runtime_execution_grants(
            replace(authorized_request, safety_refs=diagnostic_refs)
        )
        assert diagnostic_result.formation_status == "RUNTIME_EXECUTION_GRANTS_FORMED"
        diagnostic_grant = diagnostic_result.decisions[0]
        assert diagnostic_grant.decision == "GRANTED"
        assert diagnostic_grant.runtime_safety_prerequisite_ref == safety.result_ref
        assert query_current_effect_eligibility_for_grant(diagnostic_grant).eligible is True
    assert "diagnostic:valid" in diagnostic_grant.safety_refs
    assert safety.result_ref in diagnostic_grant.safety_refs

    legacy_only = form_runtime_execution_grants(
        replace(authorized_request, safety_prerequisite_ref=None, safety_refs=(safety.result_ref,))
    )
    assert legacy_only.formation_status == "INVALID_INPUT"
    assert "safety_prerequisite_missing" in legacy_only.validation_errors
    assert not legacy_only.decisions

    new_state_version = issue_cognitive_state_version_v1(
        state,
        profile_ref=COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL,
    )
    assert new_state_version is not None
    assert new_state_version.version_ref != envelope.cognitive_state_version_ref
    assert query_current_effect_eligibility_for_grant(grant).eligible is True

    mismatched_binding_key = (*binding_key[:-1], "capability:gpt6-g06-mismatch")
    mismatched_safety = form_runtime_safety_prerequisite_v1(
        binding_key=(*mismatched_binding_key, request.effect_class),
        effect_class=request.effect_class,
    )
    mismatched = form_runtime_execution_grants(
        replace(
            authorized_request,
            safety_prerequisite_ref=mismatched_safety.result_ref,
        )
    )
    assert mismatched.decisions
    assert mismatched.decisions[0].decision == "DENIED"
    assert mismatched.decisions[0].denial_reason == "safety_prerequisite_not_current"

    invalidate_runtime_safety_prerequisite_v1(
        binding_key=(*binding_key, request.effect_class),
        reason="gpt6-g06-focused-safety-invalidation",
    )
    denied = form_runtime_execution_grants(authorized_request)
    assert denied.decisions
    assert denied.decisions[0].decision == "DENIED"

    eligibility_after_safety_invalidation = query_current_effect_eligibility_for_grant(
        grant
    )
    assert eligibility_after_safety_invalidation.eligible is False
    assert eligibility_after_safety_invalidation.failure_code == "RUNTIME_SAFETY_PREREQUISITE_NOT_CURRENT"

    replacement_safety = form_runtime_safety_prerequisite_v1(
        binding_key=safety.binding_key,
        effect_class=request.effect_class,
    )
    assert replacement_safety.result_ref != safety.result_ref
    assert replacement_safety.binding_key == safety.binding_key
    assert replacement_safety.policy_version_ref == safety.policy_version_ref
    assert query_current_runtime_safety_prerequisite_v1(
        binding_key=safety.binding_key, result_ref=safety.result_ref,
    ) is None
    assert query_current_runtime_safety_prerequisite_v1(
        binding_key=safety.binding_key, result_ref=replacement_safety.result_ref,
    ) is replacement_safety
    assert query_active_authorization_for_grant(grant) is runtime_authorization_state
    assert runtime_authorization_state.scope.runtime_safety_prerequisite_ref == safety.result_ref
    assert query_current_effect_eligibility_for_grant(grant).failure_code == "RUNTIME_SAFETY_PREREQUISITE_NOT_CURRENT"
    # A new owner evaluation cannot repair an old explicit prerequisite ref.
    old_request_result = form_runtime_execution_grants(authorized_request)
    assert old_request_result.decisions[0].decision == "DENIED"
    assert old_request_result.decisions[0].denial_reason == "safety_prerequisite_not_current"

    replacement_grant = form_runtime_execution_grants(
        replace(authorized_request, safety_prerequisite_ref=replacement_safety.result_ref, safety_refs=())
    ).decisions[0]
    assert replacement_grant.decision == "GRANTED"
    assert replacement_grant.authorization_ref != grant.authorization_ref
    assert replacement_grant.runtime_safety_prerequisite_ref == replacement_safety.result_ref
    replacement_state = query_active_authorization_for_grant(replacement_grant)
    assert replacement_state is not None
    assert replacement_state.scope.runtime_safety_prerequisite_ref == replacement_safety.result_ref
    assert query_current_effect_eligibility_for_grant(replacement_grant).eligible is True
    assert query_current_effect_eligibility_for_grant(grant).eligible is False

    invalidated = invalidate_runtime_authorization_state(
        authorization_ref=grant.authorization_ref,
        subject_ref=grant.source_execution_instance_preparation_ref,
        reason="gpt6-g06-focused-cleanup",
    )
    assert invalidated is not None
    third_safety = form_runtime_safety_prerequisite_v1(
        binding_key=safety.binding_key,
        effect_class=request.effect_class,
    )
    assert third_safety.result_ref not in {safety.result_ref, replacement_safety.result_ref}
    assert query_active_authorization_for_grant(grant) is None
    assert query_current_effect_eligibility_for_grant(grant).failure_code == "RUNTIME_AUTHORIZATION_NOT_CURRENT"
    assert query_current_effect_eligibility_for_grant(replacement_grant).failure_code == "RUNTIME_SAFETY_PREREQUISITE_NOT_CURRENT"


def _safety_test_binding(case, scope_kind="RUNTIME_EXECUTION"):
    if scope_kind == "ACTION_ADMISSION":
        return (f"action:{case}", "task:test", "decision:test", "envelope:test", "version:test", "runtime-execution")
    return (*build_pregrant_authority_binding_key(
        admitted_action_ref=f"admitted-action:{case}",
        working_envelope_ref="envelope:test",
        working_envelope_version_ref="version:test",
        execution_instance_preparation_candidate_ref="execution:test",
        provider_candidate_ref="provider:test",
        capability_candidate_ref="capability:test",
    ), "runtime-execution")


@pytest.mark.parametrize("scope_kind", ["RUNTIME_EXECUTION", "ACTION_ADMISSION"])
def test_safety_occurrences_never_revive_and_query_never_issues(scope_kind, monkeypatch):
    key = _safety_test_binding("occurrence-cycles", scope_kind)
    current = form_runtime_safety_prerequisite_v1(
        binding_key=key, effect_class="runtime-execution", scope_kind=scope_kind,
    )
    assert current.status == "ALLOWED"
    old_refs = set()

    def issuance_forbidden():
        raise AssertionError("query must not issue an evaluation")

    for _ in range(3):
        with monkeypatch.context() as query_guard:
            query_guard.setattr(safety_owner, "_safety_result_ref", issuance_forbidden)
            for _ in range(2):
                assert query_current_runtime_safety_prerequisite_v1(
                    binding_key=key, result_ref=current.result_ref,
                ) is current
        revoked = invalidate_runtime_safety_prerequisite_v1(binding_key=key, reason="test-revoke")
        assert revoked is not None
        assert revoked.result_ref == current.result_ref
        assert revoked.revoked is True
        assert query_current_runtime_safety_prerequisite_v1(binding_key=key, result_ref=current.result_ref) is None
        old_refs.add(current.result_ref)
        previous = current
        current = form_runtime_safety_prerequisite_v1(
            binding_key=key, effect_class="runtime-execution", scope_kind=scope_kind,
        )
        assert current.result_ref not in old_refs
        assert current.binding_key == previous.binding_key == key
        assert current.policy_version_ref == previous.policy_version_ref
        assert query_current_runtime_safety_prerequisite_v1(binding_key=key, result_ref=current.result_ref) is current
        for ref in old_refs:
            assert query_current_runtime_safety_prerequisite_v1(binding_key=key, result_ref=ref) is None

    # A new evaluation is distinct even without an intervening revocation.
    latest = form_runtime_safety_prerequisite_v1(
        binding_key=key, effect_class="runtime-execution", scope_kind=scope_kind,
    )
    assert latest.result_ref != current.result_ref
    assert query_current_runtime_safety_prerequisite_v1(binding_key=key, result_ref=current.result_ref) is None


@pytest.mark.parametrize("scope_kind", ["RUNTIME_EXECUTION", "ACTION_ADMISSION"])
def test_completed_blocked_evaluation_replaces_allowed_outcome(scope_kind, monkeypatch):
    key = _safety_test_binding("blocked-outcome", scope_kind)
    first = form_runtime_safety_prerequisite_v1(
        binding_key=key, effect_class="runtime-execution", scope_kind=scope_kind,
    )
    assert query_current_runtime_safety_prerequisite_v1(binding_key=key, result_ref=first.result_ref) is first
    # Exercise a negative owner policy outcome, not caller-supplied truth.
    with monkeypatch.context() as owner_policy:
        owner_policy.setattr(safety_owner, "RUNTIME_SAFETY_ALLOWED_EFFECT_CLASSES", ())
        blocked = form_runtime_safety_prerequisite_v1(
            binding_key=key, effect_class="runtime-execution", scope_kind=scope_kind,
        )
    assert blocked.status == "BLOCKED"
    assert blocked.authoritative is True and blocked.candidate_only is False
    assert blocked.result_ref and blocked.result_ref != first.result_ref
    assert blocked.binding_key == first.binding_key
    assert query_current_runtime_safety_prerequisite_v1(binding_key=key, result_ref=first.result_ref) is None
    assert query_current_runtime_safety_prerequisite_v1(binding_key=key, result_ref=blocked.result_ref) is None
    # The binding's latest owner outcome really is BLOCKED, not retained E1.
    revoked = invalidate_runtime_safety_prerequisite_v1(binding_key=key, reason="blocked-outcome-check")
    assert revoked is not None and revoked.result_ref == blocked.result_ref
    recovery = form_runtime_safety_prerequisite_v1(
        binding_key=key, effect_class="runtime-execution", scope_kind=scope_kind,
    )
    assert recovery.result_ref not in {first.result_ref, blocked.result_ref}
    assert query_current_runtime_safety_prerequisite_v1(binding_key=key, result_ref=recovery.result_ref) is recovery
    assert query_current_runtime_safety_prerequisite_v1(binding_key=key, result_ref=first.result_ref) is None
    assert query_current_runtime_safety_prerequisite_v1(binding_key=key, result_ref=blocked.result_ref) is None


@pytest.mark.parametrize("invalid_fields", [
    {"binding_key": None}, {"binding_key": []}, {"binding_key": ()},
    {"binding_key": ("runtime-scope:v2",) * 7},
    {"binding_key": ("runtime-scope:v2", "a", "e", "v", "x", "p", True, "runtime-execution")},
    {"binding_key": ("runtime-scope:v2", "a", "e", "v", "x", "p", " ", "runtime-execution")},
    {"binding_key": ("runtime-scope:v2", "a", "e", "v", "x", "p", [], "runtime-execution")},
    {"effect_class": None}, {"effect_class": False}, {"effect_class": " "},
    {"scope_kind": "UNKNOWN"},
])
def test_malformed_safety_input_never_publishes_an_occurrence(invalid_fields, monkeypatch):
    key = _safety_test_binding("invalid-input")
    request = dict(binding_key=key, effect_class="runtime-execution", scope_kind="RUNTIME_EXECUTION")
    current = form_runtime_safety_prerequisite_v1(**request)

    def issuance_forbidden():
        raise AssertionError("invalid input must not issue an evaluation")

    with monkeypatch.context() as issuance_guard:
        issuance_guard.setattr(safety_owner, "_safety_result_ref", issuance_forbidden)
        invalid = form_runtime_safety_prerequisite_v1(**{**request, **invalid_fields})
    assert invalid.status == "BLOCKED"
    assert invalid.result_ref == invalid.expiry_boundary_ref == ""
    assert invalid.reason == "safety_prerequisite_input_invalid"
    assert invalid.authoritative is False and invalid.candidate_only is True
    assert query_current_runtime_safety_prerequisite_v1(binding_key=key, result_ref=current.result_ref) is current


def test_legacy_runtime_scope_cannot_form_any_positive_prerequisite():
    legacy_key = (
        "problem:gpt6-g06-legacy",
        "state:gpt6-g06-legacy",
        "execution:gpt6-g06-legacy",
        "provider_openvins",
        "spatial_mapping",
    )
    provider = evaluate_provider_runtime_eligibility_v1(
        binding_key=legacy_key,
        provider_candidate_ref="provider_openvins",
        capability_candidate_ref="spatial_mapping",
        execution_instance_preparation_candidate_ref=legacy_key[2],
    )
    capability = evaluate_runtime_capability_admission_v1(
        binding_key=legacy_key,
        capability_candidate_ref="spatial_mapping",
        provider_candidate_ref="provider_openvins",
        execution_instance_preparation_candidate_ref=legacy_key[2],
    )
    protocol = evaluate_runtime_protocol_compliance_v1(
        binding_key=legacy_key,
        protocol_refs=("protocol:runtime-execution-grant:v1",),
    )
    safety = form_runtime_safety_prerequisite_v1(
        binding_key=(*legacy_key, "runtime-execution"),
        effect_class="runtime-execution",
    )

    assert provider.status == "DENIED"
    assert capability.status == "DENIED"
    assert protocol.status == "BLOCKED"
    assert safety.status == "BLOCKED"
