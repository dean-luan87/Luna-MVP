"""Focused canonical Action-to-Runtime scope migration tests.

The tests intentionally use the existing owner-bound Action admission helper
and the existing controlled preparation builders.  They do not execute a
provider effect.
"""

from __future__ import annotations

from dataclasses import replace

from capabilities.midplatform.core.action_governance.action_admission_governance_v1 import (
    ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL,
    admit_action_v1,
    cancel_admitted_action_v1,
    query_current_admitted_action_v1,
    revoke_admitted_action_v1,
    supersede_admitted_action_v1,
)
from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    ActionGovernanceEngineV1,
    form_runtime_safety_prerequisite_v1,
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
from capabilities.evaluation.runtime_grant_pre_execution_authorization_controlled.fixtures_v1 import (
    _target_request,
    build_runtime_grant_cases_v1,
)
from capabilities.midplatform.core.runtime_executor.runtime_admission_projection_v1 import (
    project_current_admitted_action_to_runtime_handoff_v1,
    project_runtime_handoff_to_provider_preparation_request_v1,
)
from capabilities.midplatform.core.runtime_executor.runtime_allocation_preparation_candidate_v1 import (
    ExecutionInstancePreparationInputV1,
    RuntimeAllocationPreparationInputV1,
    form_execution_instance_preparation_candidates,
    form_runtime_allocation_preparation_candidates,
)
from capabilities.midplatform.core.runtime_executor.runtime_allocation_execution_instance_v1 import (
    ExecutionInstanceInputV1,
    RuntimeAllocationInputV1,
    create_execution_instances,
    form_runtime_allocation_records,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_authorization_state_v1 import (
    query_active_authorization_for_grant,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    RuntimeExecutionGrantInputV1,
    build_pregrant_authority_binding_key,
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
    form_provider_binding_runtime_preparation_candidates,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_session_invocation_v1 import (
    ProviderInvocationInputV1,
    ProviderRuntimeSessionInputV1,
    create_provider_runtime_session,
    start_controlled_provider_invocation,
)


def _ref(owner: str, value: str) -> SourceRefV1:
    return SourceRefV1(owner, value, "v1", f"trace:{value}", f"provenance:{value}")


def _admit_current_action_for_runtime_scope_test(case: str):
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
    envelope_candidate = build_working_envelope(
        work_ref=f"work:{case}",
        concern_ref=concern.concern_ref,
        authority_grant_ref=grant.grant_ref,
        source_state_version_ref=state_version.version_ref,
        goal_refs=(f"goal:{case}",),
        context_refs=(f"context:{case}",),
        current_world_refs=(f"world:{case}:v1",),
        field_refs=(f"field:{case}",),
    )
    envelope = admit_working_envelope_v1(
        envelope_candidate,
        profile_ref=WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL,
    )
    assert envelope is not None
    task_summary = build_decision_task_run_v1(
        f"action-runtime-scope:{case}",
        working_envelope=envelope,
    )
    task_case = next(
        item
        for item in task_summary["cases"]
        if item["case_id"] == "CASE_A_SUFFICIENT_STOP"
    )
    task_handoff, errors = _build_task_to_action_handoff(
        {**task_case, "resource_state": "available"}
    )
    assert not errors and task_handoff is not None
    action_request = _action_request(task_handoff)
    action_request["scenario_id"] = f"action-runtime-scope:{case}"
    action_output = ActionGovernanceEngineV1().run_case(
        ActionGovernanceInputV1(**action_request)
    )
    safety_binding_key = (
        action_output.action_candidate.action_candidate_id,
        task_handoff.task_state_ref,
        task_handoff.decision_candidate_ref,
        envelope.envelope_ref,
        envelope.envelope_version_ref,
        "runtime-execution",
    )
    safety = form_runtime_safety_prerequisite_v1(
        binding_key=safety_binding_key,
        effect_class="runtime-execution",
        scope_kind="ACTION_ADMISSION",
    )
    record = admit_action_v1(
        action_output,
        task_handoff=task_handoff,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
        safety_prerequisite=safety,
        profile_ref=ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL,
    )
    assert record is not None
    return record, envelope, task_handoff, action_output, safety, safety_binding_key


def _canonical_runtime_bundle(case: str = "canonical-scope"):
    record, envelope, _task_handoff, _action_output, _safety, _ = (
        _admit_current_action_for_runtime_scope_test(case)
    )
    action_handoff = project_current_admitted_action_to_runtime_handoff_v1(
        record.admitted_action_ref
    )
    assert action_handoff is not None

    runtime_case = build_runtime_grant_cases_v1()[0]
    legacy_target_request = _target_request(
        runtime_case.case_id, runtime_case.target_candidates
    )
    canonical_provider_target_candidates = tuple(
        replace(
            candidate,
            provider_candidate_ref="provider_openvins",
            capability_candidate_ref="spatial_mapping",
            capability_class_ref="capability-class:spatial-mapping",
        )
        for candidate in legacy_target_request.provider_target_candidates
    )
    target_request = project_runtime_handoff_to_provider_preparation_request_v1(
        action_handoff,
        preparation_ref=legacy_target_request.preparation_ref,
        parent_cognitive_problem_ref=legacy_target_request.parent_cognitive_problem_ref,
        source_state_ref=legacy_target_request.source_state_ref,
        provider_target_candidates=canonical_provider_target_candidates,
        context_refs=legacy_target_request.context_refs,
        trace_ref=legacy_target_request.trace_ref,
        provenance_refs=legacy_target_request.provenance_refs,
    )
    assert target_request is not None
    target = form_provider_binding_runtime_preparation_candidates(target_request)
    assert target.candidates

    binding = form_provider_binding_candidates(
        ProviderBindingCandidateInputV1(
            preparation_ref="gpt6-g01-binding",
            parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
            source_state_ref=target.source_state_ref,
            preparation_candidates=target.candidates,
            context_refs=target.context_refs,
            trace_ref="trace:gpt6-g01-binding",
            provenance_refs=("provenance:gpt6-g01-binding",),
            runtime_requirement_refs=("runtime-requirement:gpt6-g01",),
            resource_class_refs=("resource-class:gpt6-g01",),
            execution_class_refs=("execution-class:gpt6-g01",),
            admitted_action_ref=record.admitted_action_ref,
            working_envelope_ref=record.working_envelope_ref,
            working_envelope_version_ref=record.working_envelope_version_ref,
        )
    )
    assert binding.candidates

    allocation = form_runtime_allocation_preparation_candidates(
        RuntimeAllocationPreparationInputV1(
            preparation_ref="gpt6-g01-allocation",
            parent_cognitive_problem_ref=binding.parent_cognitive_problem_ref,
            source_state_ref=binding.source_state_ref,
            provider_binding_candidates=binding.candidates,
            context_refs=target.context_refs,
            trace_ref="trace:gpt6-g01-allocation",
            provenance_refs=("provenance:gpt6-g01-allocation",),
            admitted_action_ref=record.admitted_action_ref,
            working_envelope_ref=record.working_envelope_ref,
            working_envelope_version_ref=record.working_envelope_version_ref,
        )
    )
    assert allocation.candidates

    execution = form_execution_instance_preparation_candidates(
        ExecutionInstancePreparationInputV1(
            preparation_ref="gpt6-g01-execution",
            parent_cognitive_problem_ref=allocation.parent_cognitive_problem_ref,
            source_state_ref=allocation.source_state_ref,
            runtime_allocation_candidates=allocation.candidates,
            runtime_envelope_shape_refs=("runtime-envelope:gpt6-g01",),
            context_refs=target.context_refs,
            trace_ref="trace:gpt6-g01-execution",
            provenance_refs=("provenance:gpt6-g01-execution",),
            admitted_action_ref=record.admitted_action_ref,
            working_envelope_ref=record.working_envelope_ref,
            working_envelope_version_ref=record.working_envelope_version_ref,
        )
    )
    assert execution.candidates

    execution_candidate = execution.candidates[0]
    binding_candidate = binding.candidates[0]
    allocation_candidate = allocation.candidates[0]
    binding_key = build_pregrant_authority_binding_key(
        admitted_action_ref=record.admitted_action_ref,
        working_envelope_ref=record.working_envelope_ref,
        working_envelope_version_ref=record.working_envelope_version_ref,
        execution_instance_preparation_candidate_ref=(
            execution_candidate.execution_instance_preparation_candidate_ref
        ),
        provider_candidate_ref=binding_candidate.provider_candidate_ref,
        capability_candidate_ref=binding_candidate.capability_candidate_ref,
    )
    safety = form_runtime_safety_prerequisite_v1(
        binding_key=(*binding_key, "runtime-execution"),
        effect_class="runtime-execution",
    )
    grant_request = RuntimeExecutionGrantInputV1(
        grant_request_ref="gpt6-g01-runtime-grant",
        parent_cognitive_problem_ref=execution.parent_cognitive_problem_ref,
        source_state_ref=execution.source_state_ref,
        provider_binding_candidates=(binding_candidate,),
        runtime_allocation_candidates=(allocation_candidate,),
        execution_instance_preparation_candidates=(execution_candidate,),
        permission_refs=("permission:gpt6-g01",),
        safety_refs=("safety:gpt6-g01",),
        protocol_refs=("protocol:runtime-execution-grant:v1",),
        governance_refs=("governance:gpt6-g01",),
        constraint_refs=("constraint:gpt6-g01",),
        validity_scope=("scope:gpt6-g01",),
        expiry_boundary_ref="expiry:gpt6-g01",
        safety_prerequisite_ref=safety.result_ref,
        trace_ref="trace:gpt6-g01-grant",
        provenance_refs=("provenance:gpt6-g01-grant",),
        grant_authority_ref="authority:runtime-execution-authorization",
        grant_responsibility_ref="responsibility:runtime-execution-authorization-decision",
        admitted_action_ref=record.admitted_action_ref,
        working_envelope_ref=record.working_envelope_ref,
        working_envelope_version_ref=record.working_envelope_version_ref,
    )
    return record, envelope, action_handoff, grant_request


def test_current_admitted_action_projects_and_preserves_canonical_scope():
    record, envelope, handoff, request = _canonical_runtime_bundle()
    assert handoff.admitted_action_ref == record.admitted_action_ref
    assert handoff.working_envelope_ref == envelope.envelope_ref
    assert handoff.working_envelope_version_ref == envelope.envelope_version_ref

    result = form_runtime_execution_grants(request)
    assert result.decisions
    grant = result.decisions[0]
    assert grant.decision == "GRANTED"
    assert grant.admitted_action_ref == record.admitted_action_ref
    assert grant.working_envelope_ref == envelope.envelope_ref
    assert grant.working_envelope_version_ref == envelope.envelope_version_ref
    state = query_active_authorization_for_grant(grant)
    assert state is not None
    assert state.scope.admitted_action_ref == record.admitted_action_ref
    assert state.scope.working_envelope_ref == envelope.envelope_ref
    assert state.scope.working_envelope_version_ref == envelope.envelope_version_ref
    for candidate in (
        request.provider_binding_candidates[0],
        request.runtime_allocation_candidates[0],
        request.execution_instance_preparation_candidates[0],
    ):
        assert candidate.admitted_action_ref == record.admitted_action_ref
        assert candidate.working_envelope_ref == envelope.envelope_ref
        assert candidate.working_envelope_version_ref == envelope.envelope_version_ref
    assert not hasattr(grant, "execution_intent_ref")
    assert not grant.provider_invoked
    assert not grant.provider_invocation

    binding_result = form_provider_binding_decisions(
        ProviderBindingDecisionInputV1(
            decision_request_ref="gpt6-g01-binding-decision",
            binding_candidates=(request.provider_binding_candidates[0],),
            runtime_grants=(grant,),
            trace_ref="trace:gpt6-g01-binding-decision",
        )
    )
    assert binding_result.decisions
    binding_decision = binding_result.decisions[0]

    allocation_result = form_runtime_allocation_records(
        RuntimeAllocationInputV1(
            allocation_request_ref="gpt6-g01-allocation-record",
            binding_decisions=(binding_decision,),
            allocation_preparations=(request.runtime_allocation_candidates[0],),
            runtime_grants=(grant,),
            resource_identity_refs=("resource:gpt6-g01",),
            runtime_ref="runtime:gpt6-g01",
            trace_ref="trace:gpt6-g01-allocation-record",
        )
    )
    assert allocation_result.records
    allocation_record = allocation_result.records[0]

    instance_result = create_execution_instances(
        ExecutionInstanceInputV1(
            instance_request_ref="gpt6-g01-execution-instance",
            allocation_records=(allocation_record,),
            execution_preparations=(request.execution_instance_preparation_candidates[0],),
            binding_decisions=(binding_decision,),
            runtime_grants=(grant,),
            trace_ref="trace:gpt6-g01-execution-instance",
        )
    )
    assert instance_result.instances
    execution_instance = instance_result.instances[0]

    session_result = create_provider_runtime_session(
        ProviderRuntimeSessionInputV1(
            session_request_ref="gpt6-g01-session",
            execution_instance=execution_instance,
            provider_binding=binding_decision,
            runtime_grant=grant,
            runtime_allocation=allocation_record,
            trace_ref="trace:gpt6-g01-session",
        )
    )
    assert session_result.session is not None
    invocation_result = start_controlled_provider_invocation(
        ProviderInvocationInputV1(
            invocation_request_ref="gpt6-g01-invocation",
            session=session_result.session,
            execution_instance=execution_instance,
            provider_binding=binding_decision,
            runtime_grant=grant,
            runtime_allocation=allocation_record,
            trace_ref="trace:gpt6-g01-invocation",
        )
    )
    assert invocation_result.invocation is not None

    expected_scope = (
        record.admitted_action_ref,
        envelope.envelope_ref,
        envelope.envelope_version_ref,
    )
    for lifecycle_record in (
        binding_decision,
        allocation_record,
        execution_instance,
        session_result.session,
        invocation_result.invocation,
    ):
        assert (
            lifecycle_record.admitted_action_ref,
            lifecycle_record.working_envelope_ref,
            lifecycle_record.working_envelope_version_ref,
        ) == expected_scope

    invalid_session_invocation = start_controlled_provider_invocation(
        ProviderInvocationInputV1(
            invocation_request_ref="gpt6-g01-session-scope-mismatch",
            session=replace(
                session_result.session,
                working_envelope_ref="working-envelope:other",
            ),
            execution_instance=execution_instance,
            provider_binding=binding_decision,
            runtime_grant=grant,
            runtime_allocation=allocation_record,
            trace_ref="trace:gpt6-g01-session-scope-mismatch",
        )
    )
    assert invalid_session_invocation.invocation is None
    assert "canonical_runtime_scope_mismatch" in invalid_session_invocation.validation_errors

    mismatched_allocation = form_runtime_allocation_records(
        replace(
            RuntimeAllocationInputV1(
                allocation_request_ref="gpt6-g01-allocation-mismatch",
                binding_decisions=(binding_decision,),
                allocation_preparations=(request.runtime_allocation_candidates[0],),
                runtime_grants=(grant,),
                resource_identity_refs=("resource:gpt6-g01",),
                runtime_ref="runtime:gpt6-g01",
                trace_ref="trace:gpt6-g01-allocation-mismatch",
            ),
            binding_decisions=(
                replace(
                    binding_decision,
                    working_envelope_version_ref="envelope-version:other",
                ),
            ),
        )
    )
    assert mismatched_allocation.formation_status == "INVALID_INPUT"
    assert any(
        error.startswith("canonical_runtime_scope_mismatch:")
        for error in mismatched_allocation.validation_errors
    )

    legacy_metadata_only = replace(
        binding_decision,
        parent_cognitive_problem_ref="problem:legacy-other",
        source_state_ref="state:legacy-other",
    )
    legacy_allocation = form_runtime_allocation_records(
        replace(
            RuntimeAllocationInputV1(
                allocation_request_ref="gpt6-g01-legacy-metadata",
                binding_decisions=(binding_decision,),
                allocation_preparations=(request.runtime_allocation_candidates[0],),
                runtime_grants=(grant,),
                resource_identity_refs=("resource:gpt6-g01",),
                runtime_ref="runtime:gpt6-g01",
                trace_ref="trace:gpt6-g01-legacy-metadata",
            ),
            binding_decisions=(legacy_metadata_only,),
        )
    )
    assert legacy_allocation.records
    legacy_instance = create_execution_instances(
        replace(
            ExecutionInstanceInputV1(
                instance_request_ref="gpt6-g01-legacy-instance",
                allocation_records=legacy_allocation.records,
                execution_preparations=(request.execution_instance_preparation_candidates[0],),
                binding_decisions=(legacy_metadata_only,),
                runtime_grants=(grant,),
                trace_ref="trace:gpt6-g01-legacy-instance",
            ),
        )
    )
    assert legacy_instance.instances
    legacy_session = create_provider_runtime_session(
        ProviderRuntimeSessionInputV1(
            session_request_ref="gpt6-g01-legacy-session",
            execution_instance=legacy_instance.instances[0],
            provider_binding=legacy_metadata_only,
            runtime_grant=grant,
            runtime_allocation=legacy_allocation.records[0],
            trace_ref="trace:gpt6-g01-legacy-session",
        )
    )
    assert legacy_session.session is not None


def test_revoked_action_cannot_enter_canonical_runtime_grant():
    record, _envelope, _handoff, request = _canonical_runtime_bundle("revoked")
    assert revoke_admitted_action_v1(
        record.admitted_action_ref,
        reason_ref="gpt6-g01:revoked",
    ) is not None
    assert query_current_admitted_action_v1(record.admitted_action_ref) is None
    result = form_runtime_execution_grants(request)
    assert result.formation_status == "INVALID_INPUT"
    assert "admitted_action_not_current" in result.validation_errors


def test_cancelled_and_superseded_actions_cannot_enter_runtime():
    cancelled, _envelope, _handoff, cancelled_request = _canonical_runtime_bundle(
        "cancelled"
    )
    assert cancel_admitted_action_v1(
        cancelled.admitted_action_ref,
        reason_ref="gpt6-g01:cancelled",
    ) is not None
    cancelled_result = form_runtime_execution_grants(cancelled_request)
    assert cancelled_result.formation_status == "INVALID_INPUT"
    assert "admitted_action_not_current" in cancelled_result.validation_errors

    old, _old_envelope, _old_handoff, old_request = _canonical_runtime_bundle(
        "superseded-old"
    )
    new, _new_envelope, _new_handoff, _new_request = _canonical_runtime_bundle(
        "superseded-new"
    )
    assert supersede_admitted_action_v1(
        old.admitted_action_ref,
        replacement_admitted_action_ref=new.admitted_action_ref,
        reason_ref="gpt6-g01:superseded",
    ) is not None
    old_result = form_runtime_execution_grants(old_request)
    assert old_result.formation_status == "INVALID_INPUT"
    assert "admitted_action_not_current" in old_result.validation_errors


def test_fake_action_or_envelope_scope_fails_closed():
    record, envelope, handoff, request = _canonical_runtime_bundle("fake-scope")
    assert project_current_admitted_action_to_runtime_handoff_v1(
        "admitted-action:caller-fake"
    ) is None
    assert handoff.admitted_action_ref == record.admitted_action_ref
    assert handoff.working_envelope_ref != envelope.concern_ref
    invalid = replace(
        request,
        admitted_action_ref="admitted-action:caller-fake",
    )
    result = form_runtime_execution_grants(invalid)
    assert result.formation_status == "INVALID_INPUT"
    assert "admitted_action_not_current" in result.validation_errors


def test_legacy_fields_do_not_define_canonical_scope():
    _record, _envelope, _handoff, request = _canonical_runtime_bundle("legacy")
    legacy_only = replace(
        request,
        admitted_action_ref=None,
        working_envelope_ref=None,
        working_envelope_version_ref=None,
    )
    result = form_runtime_execution_grants(legacy_only)
    assert result.formation_status == "INVALID_INPUT"
    assert result.decisions == ()
    assert "canonical_runtime_scope_incomplete" in result.validation_errors


def test_legacy_field_mismatch_does_not_deny_canonical_scope():
    record, _envelope, _handoff, request = _canonical_runtime_bundle("legacy-mismatch")
    mismatched = replace(
        request,
        parent_cognitive_problem_ref="problem:caller-substitute",
        source_state_ref="state:caller-substitute",
    )
    result = form_runtime_execution_grants(mismatched)
    assert result.decisions
    assert result.decisions[0].decision == "GRANTED"
    assert query_active_authorization_for_grant(result.decisions[0]) is not None
    assert record.admitted_action_ref == request.admitted_action_ref


def test_legacy_metadata_cannot_authorize_different_canonical_scope():
    record, envelope, _handoff, request = _canonical_runtime_bundle(
        "legacy-cannot-authorize"
    )
    result = form_runtime_execution_grants(request)
    assert result.decisions
    grant = result.decisions[0]
    assert query_active_authorization_for_grant(grant) is not None

    altered = replace(
        grant,
        admitted_action_ref=f"{record.admitted_action_ref}:other",
        working_envelope_ref=f"{envelope.envelope_ref}:other",
        working_envelope_version_ref=f"{envelope.envelope_version_ref}:other",
        parent_cognitive_problem_ref=grant.parent_cognitive_problem_ref,
        source_state_ref=grant.source_state_ref,
    )
    assert query_active_authorization_for_grant(altered) is None


def test_different_admitted_action_scope_keys_are_distinct():
    first, first_envelope, _first_handoff, first_request = _canonical_runtime_bundle(
        "scope-one"
    )
    second, second_envelope, _second_handoff, second_request = _canonical_runtime_bundle(
        "scope-two"
    )
    first_result = form_runtime_execution_grants(first_request)
    second_result = form_runtime_execution_grants(second_request)
    assert first_result.decisions and second_result.decisions
    first_grant = first_result.decisions[0]
    second_grant = second_result.decisions[0]
    assert first_grant.admitted_action_ref != second_grant.admitted_action_ref
    assert first_grant.working_envelope_ref != second_grant.working_envelope_ref
    assert first_envelope.envelope_version_ref != second_envelope.envelope_version_ref
    assert query_active_authorization_for_grant(first_grant) is not None
    assert query_active_authorization_for_grant(second_grant) is not None


def test_runtime_handoff_remains_candidate_only_and_owner_profiles_remain_intact():
    record, _envelope, handoff, request = _canonical_runtime_bundle("boundary")
    assert handoff.candidate_only is True
    assert handoff.action_executed is False
    assert handoff.scheduler_executed is False
    assert handoff.device_control_executed is False
    result = form_runtime_execution_grants(request)
    assert result.decisions
    grant = result.decisions[0]
    assert grant.provider_evaluation_profile_ref
    assert grant.capability_evaluation_profile_ref
    assert grant.failure_owner_ref in {None, "Provider Governance", "Capability Governance", "Safety Governance", "Protocol Manager", "Permission / Admission Manager", "Runtime Executor", "Resource Governance"}
    assert grant.admitted_action_ref == record.admitted_action_ref
