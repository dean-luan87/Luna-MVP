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
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    RuntimeExecutionGrantInputV1,
    form_runtime_execution_grants,
    invalidate_runtime_authorization_state,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_candidate_v1 import (
    ProviderBindingCandidateInputV1,
    form_provider_binding_candidates,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_runtime_preparation_v1 import (
    form_provider_binding_runtime_preparation_candidates,
)


def _genuine_grant(**changes):
    case = build_runtime_grant_cases_v1()[0]
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
    request = RuntimeExecutionGrantInputV1(
        grant_request_ref=f"f07-grant:{case.case_id.lower()}",
        parent_cognitive_problem_ref=execution.parent_cognitive_problem_ref,
        source_state_ref=execution.source_state_ref,
        provider_binding_candidates=binding.candidates,
        runtime_allocation_candidates=allocation.candidates,
        execution_instance_preparation_candidates=execution.candidates,
        permission_refs=("permission:f07",),
        safety_refs=("safety:f07",),
        protocol_refs=("protocol:f07",),
        governance_refs=("governance:f07",),
        constraint_refs=("constraint:f07",),
        validity_scope=("scope:f07",),
        expiry_boundary_ref="expiry:f07",
        trace_ref="trace:f07-grant",
        provenance_refs=("provenance:f07-grant",),
        grant_authority_ref=case.grant_authority_ref,
        grant_responsibility_ref=case.grant_responsibility_ref,
        freshness_status=changes.pop("freshness_status", "FRESH"),
        validity_status=changes.pop("validity_status", "FRESH"),
        resource_feasibility_status=changes.pop(
            "resource_feasibility_status", "SATISFIABLE"
        ),
        **changes,
    )
    result = form_runtime_execution_grants(request)
    assert result.decisions
    return result, result.decisions[0]


def test_t01_genuine_canonical_authorization_is_active():
    _, grant = _genuine_grant()
    assert grant.decision == "GRANTED"
    assert query_active_authorization_for_grant(grant) is not None


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
    invalidate_runtime_authorization_state(
        authorization_ref=grant.authorization_ref,
        subject_ref=grant.source_execution_instance_preparation_ref,
        reason="permission_revoked",
    )
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
