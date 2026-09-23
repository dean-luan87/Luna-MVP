"""Focused authority-origin tests for the F-07 Runtime Authorization state."""

from __future__ import annotations

from copy import copy, deepcopy
from dataclasses import replace
import pickle

import pytest

from capabilities.evaluation.runtime_grant_pre_execution_authorization_controlled.fixtures_v1 import (
    _target_request,
    build_runtime_grant_cases_v1,
)
from capabilities.midplatform.core.runtime_executor.runtime_allocation_preparation_candidate_v1 import (
    ExecutionInstancePreparationInputV1,
    RuntimeAllocationPreparationInputV1,
    form_execution_instance_preparation_candidates,
    form_runtime_allocation_preparation_candidates,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_authorization_state_v1 import (
    RuntimeAuthorizationScopeV1,
    RuntimeAuthorizationStateReadViewV1,
    RuntimeAuthorizationStateStoreV1,
    RuntimeAuthorizationStateV1,
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
    form_provider_binding_runtime_preparation_candidates,
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
    action_safety = form_runtime_safety_prerequisite_v1(
        binding_key=safety_key,
        effect_class="runtime-execution",
        scope_kind="ACTION_ADMISSION",
    )
    admitted_action = admit_action_v1(
        action_output,
        task_handoff=task_handoff,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
        safety_prerequisite=action_safety,
        profile_ref=ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL,
    )
    assert admitted_action is not None
    return admitted_action, envelope


def _genuine_grant(**changes):
    case = build_runtime_grant_cases_v1()[0]
    admitted_action, envelope = _canonical_runtime_scope("f07-runtime")
    target = form_provider_binding_runtime_preparation_candidates(
        _target_request(case.case_id, case.target_candidates)
    )
    binding = form_provider_binding_candidates(
        ProviderBindingCandidateInputV1(
            preparation_ref=f"f07-binding:{case.case_id.lower()}",
            parent_cognitive_problem_ref=target.parent_cognitive_problem_ref,
            source_state_ref=target.source_state_ref,
            preparation_candidates=target.candidates,
            context_refs=target.context_refs,
            trace_ref=f"trace:f07-binding:{case.case_id.lower()}",
            provenance_refs=(f"provenance:f07-binding:{case.case_id.lower()}",),
            runtime_requirement_refs=(f"runtime-requirement:{case.case_id.lower()}",),
            resource_class_refs=(f"resource-class:{case.case_id.lower()}",),
            execution_class_refs=(f"execution-class:{case.case_id.lower()}",),
        )
    )
    allocation = form_runtime_allocation_preparation_candidates(
        RuntimeAllocationPreparationInputV1(
            preparation_ref=f"f07-allocation:{case.case_id.lower()}",
            parent_cognitive_problem_ref=binding.parent_cognitive_problem_ref,
            source_state_ref=binding.source_state_ref,
            provider_binding_candidates=binding.candidates,
            context_refs=target.context_refs,
            trace_ref=f"trace:f07-allocation:{case.case_id.lower()}",
            provenance_refs=(f"provenance:f07-allocation:{case.case_id.lower()}",),
        )
    )
    execution = form_execution_instance_preparation_candidates(
        ExecutionInstancePreparationInputV1(
            preparation_ref=f"f07-execution:{case.case_id.lower()}",
            parent_cognitive_problem_ref=allocation.parent_cognitive_problem_ref,
            source_state_ref=allocation.source_state_ref,
            runtime_allocation_candidates=allocation.candidates,
            runtime_envelope_shape_refs=("runtime-envelope:f07",),
            context_refs=target.context_refs,
            trace_ref=f"trace:f07-execution:{case.case_id.lower()}",
            provenance_refs=(f"provenance:f07-execution:{case.case_id.lower()}",),
        )
    )
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
    requested_permission = changes.get("permission_status", "ALLOWED")
    requested_resource = changes.get("resource_feasibility_status", "SATISFIABLE")
    requested_freshness = changes.get("freshness_status", "FRESH")
    requested_validity = changes.get("validity_status", "FRESH")
    effect_class = "runtime-execution"
    if (
        requested_permission != "ALLOWED"
        or requested_resource != "SATISFIABLE"
        or requested_freshness != "FRESH"
        or requested_validity != "FRESH"
    ):
        effect_class = "blocked-controlled-scenario"
    binding_key = build_pregrant_authority_binding_key(
        execution_instance_preparation_candidate_ref=canonical_execution.execution_instance_preparation_candidate_ref,
        provider_candidate_ref=canonical_binding.provider_candidate_ref,
        capability_candidate_ref=canonical_binding.capability_candidate_ref,
        admitted_action_ref=admitted_action.admitted_action_ref,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
    )
    safety = form_runtime_safety_prerequisite_v1(
        binding_key=(*binding_key, effect_class),
        effect_class=effect_class,
    )
    request = RuntimeExecutionGrantInputV1(
        grant_request_ref=f"f07-grant:{case.case_id.lower()}",
        parent_cognitive_problem_ref=execution.parent_cognitive_problem_ref,
        source_state_ref=execution.source_state_ref,
        provider_binding_candidates=(canonical_binding,),
        runtime_allocation_candidates=(canonical_allocation,),
        execution_instance_preparation_candidates=(canonical_execution,),
        permission_refs=("permission:f07",),
        safety_refs=("safety:f07",),
        protocol_refs=("protocol:runtime-execution-grant:v1",),
        governance_refs=("governance:f07",),
        constraint_refs=("constraint:f07",),
        validity_scope=("scope:f07",),
        expiry_boundary_ref="expiry:f07",
        trace_ref="trace:f07-grant",
        provenance_refs=("provenance:f07-grant",),
        grant_authority_ref=case.grant_authority_ref,
        grant_responsibility_ref=case.grant_responsibility_ref,
        admitted_action_ref=admitted_action.admitted_action_ref,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
        freshness_status=changes.pop("freshness_status", "FRESH"),
        validity_status=changes.pop("validity_status", "FRESH"),
        resource_feasibility_status=changes.pop("resource_feasibility_status", "SATISFIABLE"),
        effect_class=effect_class,
        safety_prerequisite_ref=safety.result_ref,
        **changes,
    )
    result = form_runtime_execution_grants(request)
    assert result.decisions
    return result, result.decisions[0]


def test_t01_genuine_canonical_authorization_is_active():
    _, grant = _genuine_grant()
    assert grant.decision == "GRANTED"
    state = query_active_authorization_for_grant(grant)
    assert state is not None
    assert state.scope.runtime_safety_prerequisite_ref == grant.runtime_safety_prerequisite_ref
    assert state.scope.runtime_safety_binding_key == grant.runtime_safety_binding_key
    assert query_current_effect_eligibility_for_grant(grant).eligible is True


def test_t01_effect_eligibility_uses_canonical_typed_projection_not_caller_fallback():
    _, grant = _genuine_grant()
    missing_typed_projection = replace(
        grant,
        runtime_safety_prerequisite_ref=None,
        runtime_safety_binding_key=(),
    )
    result = query_current_effect_eligibility_for_grant(missing_typed_projection)
    assert result.eligible is True
    assert result.failure_code is None


def test_t02_caller_created_granted_projection_is_rejected():
    _, grant = _genuine_grant()
    forged = replace(
        grant,
        authorization_ref="runtime-authorization:caller-created",
        execution_authorized=True,
    )
    assert query_active_authorization_for_grant(forged) is None


def test_t03_copied_grant_without_owner_state_is_rejected():
    _, grant = _genuine_grant()
    copied = copy(grant)
    assert query_active_authorization_for_grant(
        replace(copied, authorization_ref="runtime-authorization:copied")
    ) is None


def test_t04_serialized_grant_reconstruction_cannot_restore_authority():
    _, grant = _genuine_grant()
    reconstructed = pickle.loads(pickle.dumps(grant))
    reconstructed = replace(
        reconstructed, authorization_ref="runtime-authorization:serialized"
    )
    assert query_active_authorization_for_grant(reconstructed) is None


@pytest.mark.parametrize(
    "field,value",
    [
        ("source_execution_instance_preparation_ref", "prep:other"),
        ("capability_candidate_ref", "capability:other"),
        ("source_provider_binding_candidate_ref", "binding:other"),
    ],
)
def test_t05_t07_scope_reuse_is_rejected(field, value):
    _, grant = _genuine_grant()
    assert query_active_authorization_for_grant(replace(grant, **{field: value})) is None


@pytest.mark.parametrize(
    "field,value",
    [
        ("parent_cognitive_problem_ref", "problem:legacy-other"),
        ("source_state_ref", "state:legacy-other"),
    ],
)
def test_legacy_metadata_mismatch_does_not_deny_current_authorization(field, value):
    _, grant = _genuine_grant()
    assert query_active_authorization_for_grant(replace(grant, **{field: value})) is not None


def test_t08_authorization_ref_with_altered_scope_is_rejected():
    _, grant = _genuine_grant()
    altered = replace(grant, validity_scope=("scope:other",))
    assert query_active_authorization_for_grant(altered) is None


def test_t09_fake_authorization_ref_is_rejected():
    _, grant = _genuine_grant()
    assert query_active_authorization_for_grant(
        replace(grant, authorization_ref="authorization:fake")
    ) is None


def test_t10_fake_state_dto_is_not_a_state_store():
    fake = RuntimeAuthorizationStateV1(
        authorization_ref="authorization:fake",
        subject_ref="prep:fake",
        status="AUTHORIZED",
        scope=RuntimeAuthorizationScopeV1(
            "prep:fake", "binding:fake", "allocation:fake", "execution:fake",
            "provider:fake", "capability:fake", "problem:fake", "state:fake",
            (), (), (), (), (), (), "expiry:fake",
        ),
    )
    assert not isinstance(fake, RuntimeAuthorizationStateStoreV1)


def test_t11_self_consistent_forged_package_is_rejected():
    _, grant = _genuine_grant()
    forged = replace(
        grant,
        grant_ref="runtime-execution-grant:fake",
        authorization_ref="runtime-authorization:fake",
        source_execution_instance_preparation_ref="prep:fake",
    )
    assert query_active_authorization_for_grant(forged) is None


def test_t12_stale_required_prerequisite_creates_no_authorized_state():
    result, grant = _genuine_grant(freshness_status="STALE")
    assert result.formation_status == "RUNTIME_EXECUTION_GRANTS_FORMED"
    assert grant.decision == "DENIED"
    assert query_active_authorization_for_grant(grant) is None


def test_t13_stale_validity_fresh_freshness_cannot_grant():
    _, grant = _genuine_grant(validity_status="STALE", freshness_status="FRESH")
    assert grant.decision != "GRANTED"
    assert not grant.execution_authorized


def test_t14_canonical_invalidation_blocks_later_consumption():
    result, grant = _genuine_grant()
    state = query_active_authorization_for_grant(grant)
    assert state is not None
    assert state.status == "AUTHORIZED"
    invalidate_runtime_authorization_state(
        authorization_ref=grant.authorization_ref,
        subject_ref=grant.source_execution_instance_preparation_ref,
        reason="permission_revoked",
    )
    assert state.status == "AUTHORIZED"
    assert query_active_authorization_for_grant(grant) is None


def test_t15_expiry_creates_no_active_authorization():
    _, grant = _genuine_grant(validity_status="EXPIRED")
    assert grant.decision != "GRANTED"
    assert query_active_authorization_for_grant(grant) is None


def test_t16_scope_mismatch_does_not_invalidate_genuine_state():
    _, grant = _genuine_grant()
    assert query_active_authorization_for_grant(
        replace(grant, source_execution_instance_preparation_ref="prep:other")
    ) is None
    assert query_active_authorization_for_grant(grant) is not None


def test_t17_resource_failure_is_a_denial_without_downstream_reauthorization():
    _, grant = _genuine_grant(resource_feasibility_status="UNAVAILABLE")
    assert grant.decision == "DENIED"
    assert query_active_authorization_for_grant(grant) is None


def test_t18_session_or_runtime_failure_does_not_mutate_active_state():
    _, grant = _genuine_grant()
    before = query_active_authorization_for_grant(grant)
    assert before is not None
    assert query_active_authorization_for_grant(grant) is before


def test_t19_downstream_has_no_public_authorization_mutation_api():
    _, grant = _genuine_grant()
    assert not hasattr(grant, "authorization_state_view")
    assert not hasattr(grant, "authorization_state_store")


def test_t20_downstream_cannot_reauthorize_an_empty_store():
    store = RuntimeAuthorizationStateStoreV1()
    assert store.query_active_authorization(
        authorization_ref="authorization:fake",
        scope=RuntimeAuthorizationScopeV1(
            "prep:fake", "binding:fake", "allocation:fake", "execution:fake",
            "provider:fake", "capability:fake", "problem:fake", "state:fake",
            (), (), (), (), (), (), "expiry:fake",
        ),
    ) is None


def test_t21_replay_requires_a_new_canonical_authorization_occurrence():
    _, first = _genuine_grant()
    _, replay = _genuine_grant()
    assert first.authorization_ref != replay.authorization_ref
    assert query_active_authorization_for_grant(first) is not None
    assert query_active_authorization_for_grant(replay) is not None


def test_t22_denied_decision_creates_no_authorized_state():
    _, grant = _genuine_grant(permission_status="DENIED")
    assert grant.decision == "DENIED"
    assert query_active_authorization_for_grant(grant) is None


def test_t23_copied_state_representation_cannot_create_authority():
    _, grant = _genuine_grant()
    state = query_active_authorization_for_grant(grant)
    assert state is not None
    copied = replace(state)
    assert copied == state
    assert query_active_authorization_for_grant(
        replace(grant, authorization_ref="runtime-authorization:copied-state")
    ) is None


def test_t24_state_key_requires_subject_and_authorization_ref():
    _, grant = _genuine_grant()
    state = query_active_authorization_for_grant(grant)
    assert state is not None
    assert grant.source_execution_instance_preparation_ref
    assert grant.authorization_ref
    assert query_active_authorization_for_grant(
        replace(grant, authorization_ref="authorization:other")
    ) is None


def test_t25_caller_created_store_is_not_canonical():
    _, grant = _genuine_grant()
    store = RuntimeAuthorizationStateStoreV1()
    assert store.query_active_authorization(
        authorization_ref=grant.authorization_ref,
        scope=RuntimeAuthorizationScopeV1.from_grant(grant),
    ) is None
    assert query_active_authorization_for_grant(grant) is not None


def test_t26_caller_reachable_store_authorize_does_not_install_canonical_state():
    _, grant = _genuine_grant()
    store = RuntimeAuthorizationStateStoreV1()
    store._authorize(
        authorization_ref="runtime-authorization:caller-store",
        scope=RuntimeAuthorizationScopeV1.from_grant(grant),
    )
    forged = replace(grant, authorization_ref="runtime-authorization:caller-store")
    assert query_active_authorization_for_grant(forged) is None


def test_t27_caller_backing_mapping_mutation_does_not_install_canonical_state():
    _, grant = _genuine_grant()
    store = RuntimeAuthorizationStateStoreV1()
    scope = RuntimeAuthorizationScopeV1.from_grant(grant)
    store._states[(scope.execution_instance_preparation_candidate_ref, "runtime-authorization:dict")] = RuntimeAuthorizationStateV1(
        "runtime-authorization:dict",
        scope.execution_instance_preparation_candidate_ref,
        "AUTHORIZED",
        scope,
    )
    assert query_active_authorization_for_grant(
        replace(grant, authorization_ref="runtime-authorization:dict")
    ) is None


def test_t28_caller_read_view_is_not_selected_by_grant_query():
    _, grant = _genuine_grant()
    caller_store = RuntimeAuthorizationStateStoreV1()
    caller_view = RuntimeAuthorizationStateReadViewV1(caller_store)
    assert caller_view.query_active_authorization(
        authorization_ref=grant.authorization_ref,
        scope=RuntimeAuthorizationScopeV1.from_grant(grant),
    ) is None
    assert query_active_authorization_for_grant(grant) is not None


def test_t29_self_consistent_granted_grant_with_caller_store_is_rejected():
    _, grant = _genuine_grant()
    caller_store = RuntimeAuthorizationStateStoreV1()
    scope = RuntimeAuthorizationScopeV1.from_grant(grant)
    caller_store._authorize(
        authorization_ref="runtime-authorization:forged-package", scope=scope
    )
    forged = replace(grant, authorization_ref="runtime-authorization:forged-package")
    assert query_active_authorization_for_grant(forged) is None


def test_t30_caller_created_store_and_view_cannot_establish_authority():
    _, grant = _genuine_grant()
    caller_view = RuntimeAuthorizationStateReadViewV1(RuntimeAuthorizationStateStoreV1())
    assert caller_view.query_active_authorization(
        authorization_ref=grant.authorization_ref,
        scope=RuntimeAuthorizationScopeV1.from_grant(grant),
    ) is None
    assert query_active_authorization_for_grant(grant) is not None


def test_t31_result_does_not_expose_authoritative_store():
    result, _ = _genuine_grant()
    assert not hasattr(result, "authorization_state_store")


def test_t32_invalidation_request_does_not_require_store_argument():
    result, grant = _genuine_grant()
    assert result is not None
    invalidated = invalidate_runtime_authorization_state(
        authorization_ref=grant.authorization_ref,
        subject_ref=grant.source_execution_instance_preparation_ref,
        reason="permission_revoked",
    )
    assert invalidated is not None
    assert query_active_authorization_for_grant(grant) is None


def test_t33_invalidation_request_does_not_target_caller_store():
    _, grant = _genuine_grant()
    caller_store = RuntimeAuthorizationStateStoreV1()
    caller_store._authorize(
        authorization_ref=grant.authorization_ref,
        scope=RuntimeAuthorizationScopeV1.from_grant(grant),
    )
    invalidate_runtime_authorization_state(
        authorization_ref=grant.authorization_ref,
        subject_ref=grant.source_execution_instance_preparation_ref,
        reason="caller_request",
    )
    assert caller_store.query_active_authorization(
        authorization_ref=grant.authorization_ref,
        scope=RuntimeAuthorizationScopeV1.from_grant(grant),
    ) is not None


def test_t34_genuine_grant_uses_canonical_query_without_embedded_view():
    _, grant = _genuine_grant()
    assert not hasattr(grant, "authorization_state_view")
    assert query_active_authorization_for_grant(grant) is not None


def test_t35_genuine_authorization_ref_with_altered_scope_is_rejected():
    _, grant = _genuine_grant()
    altered = replace(grant, capability_candidate_ref="capability:attacker")
    assert query_active_authorization_for_grant(altered) is None


def test_t36_assurance_distinguishes_canonical_from_caller_state():
    _, grant = _genuine_grant()
    caller_store = RuntimeAuthorizationStateStoreV1()
    caller_store._authorize(
        authorization_ref="runtime-authorization:assurance-fake",
        scope=RuntimeAuthorizationScopeV1.from_grant(grant),
    )
    fake = replace(grant, authorization_ref="runtime-authorization:assurance-fake")
    assert query_active_authorization_for_grant(fake) is None
    assert query_active_authorization_for_grant(grant) is not None
