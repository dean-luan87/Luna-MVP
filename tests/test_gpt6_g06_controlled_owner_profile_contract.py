"""Focused contract checks for owner-defined controlled evaluation profiles."""

import inspect

from capabilities.evaluation.provider_binding_runtime_allocation_execution_instance_controlled.engine_v1 import (
    ProviderBindingRuntimeAllocationExecutionEvaluationEngineV1,
)
from capabilities.evaluation.runtime_grant_pre_execution_authorization_controlled.fixtures_v1 import (
    build_controlled_canonical_runtime_scope_v1,
)
from capabilities.midplatform.core.action_governance.action_admission_governance_v1 import (
    ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1,
    query_current_admitted_action_v1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_resolution_v1 import (
    CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF,
    PRODUCTION_CAPABILITY_EVALUATION_PROFILE_REF,
    evaluate_runtime_capability_admission_v1,
    resolve_capability_runtime_evaluation_profile_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    RuntimeExecutionGrantInputV1,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_registry_v1 import (
    CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF,
    PRODUCTION_PROVIDER_EVALUATION_PROFILE_REF,
    evaluate_provider_runtime_eligibility_v1,
    resolve_provider_runtime_evaluation_profile_v1,
)


def _binding_key(provider_ref: str, capability_ref: str) -> tuple[str, ...]:
    return (
        "runtime-scope:v2",
        "admitted-action:gpt6-g06-profile",
        "working-envelope:gpt6-g06-profile",
        "working-envelope-version:gpt6-g06-profile:v1",
        "execution:gpt6-g06-profile",
        provider_ref,
        capability_ref,
    )


def test_owner_profiles_isolate_production_and_controlled_identities() -> None:
    production_provider = evaluate_provider_runtime_eligibility_v1(
        binding_key=_binding_key("provider:controlled:1", "capability:controlled:a"),
        provider_candidate_ref="provider:controlled:1",
        capability_candidate_ref="capability:controlled:a",
        execution_instance_preparation_candidate_ref="execution:gpt6-g06-profile",
    )
    controlled_provider_one = evaluate_provider_runtime_eligibility_v1(
        binding_key=_binding_key("provider:controlled:1", "capability:controlled:a"),
        provider_candidate_ref="provider:controlled:1",
        capability_candidate_ref="capability:controlled:a",
        execution_instance_preparation_candidate_ref="execution:gpt6-g06-profile",
        profile_ref=CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF,
    )
    controlled_provider_two = evaluate_provider_runtime_eligibility_v1(
        binding_key=_binding_key("provider:controlled:2", "capability:controlled:b"),
        provider_candidate_ref="provider:controlled:2",
        capability_candidate_ref="capability:controlled:b",
        execution_instance_preparation_candidate_ref="execution:gpt6-g06-profile-2",
        profile_ref=CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF,
    )

    assert production_provider.status == "DENIED"
    assert controlled_provider_one.status == "ELIGIBLE"
    assert controlled_provider_two.status == "ELIGIBLE"
    assert controlled_provider_one.evaluation_profile_ref == CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF
    assert controlled_provider_two.evaluation_profile_ref == CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF
    assert controlled_provider_one.result_ref != controlled_provider_two.result_ref


def test_owner_profiles_isolate_capability_identities() -> None:
    production_capability = evaluate_runtime_capability_admission_v1(
        binding_key=_binding_key("provider:controlled:1", "capability:controlled:a"),
        capability_candidate_ref="capability:controlled:a",
        provider_candidate_ref="provider:controlled:1",
        execution_instance_preparation_candidate_ref="execution:gpt6-g06-profile",
    )
    controlled_capability_a = evaluate_runtime_capability_admission_v1(
        binding_key=_binding_key("provider:controlled:1", "capability:controlled:a"),
        capability_candidate_ref="capability:controlled:a",
        provider_candidate_ref="provider:controlled:1",
        execution_instance_preparation_candidate_ref="execution:gpt6-g06-profile",
        profile_ref=CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF,
    )
    controlled_capability_b = evaluate_runtime_capability_admission_v1(
        binding_key=_binding_key("provider:controlled:2", "capability:controlled:b"),
        capability_candidate_ref="capability:controlled:b",
        provider_candidate_ref="provider:controlled:2",
        execution_instance_preparation_candidate_ref="execution:gpt6-g06-profile-2",
        profile_ref=CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF,
    )

    assert production_capability.status == "DENIED"
    assert controlled_capability_a.status == "ADMITTED"
    assert controlled_capability_b.status == "ADMITTED"
    assert controlled_capability_a.evaluation_profile_ref == CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF
    assert controlled_capability_b.evaluation_profile_ref == CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF
    assert controlled_capability_a.result_ref != controlled_capability_b.result_ref


def test_unknown_or_empty_profiles_fail_closed_without_fallback() -> None:
    provider_args = {
        "binding_key": _binding_key("provider:controlled:1", "capability:controlled:a"),
        "provider_candidate_ref": "provider:controlled:1",
        "capability_candidate_ref": "capability:controlled:a",
        "execution_instance_preparation_candidate_ref": "execution:gpt6-g06-profile",
    }
    capability_args = {
        "binding_key": _binding_key("provider:controlled:1", "capability:controlled:a"),
        "capability_candidate_ref": "capability:controlled:a",
        "provider_candidate_ref": "provider:controlled:1",
        "execution_instance_preparation_candidate_ref": "execution:gpt6-g06-profile",
    }

    for invalid_profile in ("", "unknown:profile", None):
        assert evaluate_provider_runtime_eligibility_v1(
            **provider_args, profile_ref=invalid_profile
        ).status == "DENIED"
        assert evaluate_runtime_capability_admission_v1(
            **capability_args, profile_ref=invalid_profile
        ).status == "DENIED"


def test_profiles_are_owner_resolved_and_production_catalogs_remain_isolated() -> None:
    production_provider_profile = resolve_provider_runtime_evaluation_profile_v1(
        PRODUCTION_PROVIDER_EVALUATION_PROFILE_REF
    )
    controlled_provider_profile = resolve_provider_runtime_evaluation_profile_v1(
        CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF
    )
    production_capability_profile = resolve_capability_runtime_evaluation_profile_v1(
        PRODUCTION_CAPABILITY_EVALUATION_PROFILE_REF
    )
    controlled_capability_profile = resolve_capability_runtime_evaluation_profile_v1(
        CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF
    )

    assert production_provider_profile is not None
    assert controlled_provider_profile is not None
    assert production_capability_profile is not None
    assert controlled_capability_profile is not None
    assert "provider:controlled:1" not in production_provider_profile.provider_refs
    assert "provider:controlled:2" not in production_provider_profile.provider_refs
    assert "capability:controlled:a" not in production_capability_profile.capability_refs
    assert "capability:controlled:b" not in production_capability_profile.capability_refs
    assert "provider:controlled:1" in controlled_provider_profile.provider_refs
    assert "provider:controlled:2" in controlled_provider_profile.provider_refs
    assert "capability:controlled:a" in controlled_capability_profile.capability_refs
    assert "capability:controlled:b" in controlled_capability_profile.capability_refs


def test_profile_selection_does_not_expose_catalog_or_legacy_authority() -> None:
    provider_parameters = inspect.signature(evaluate_provider_runtime_eligibility_v1).parameters
    capability_parameters = inspect.signature(evaluate_runtime_capability_admission_v1).parameters
    assert "catalog" not in provider_parameters
    assert "catalog" not in capability_parameters
    assert "eligible" not in provider_parameters
    assert "admitted" not in capability_parameters

    fields = RuntimeExecutionGrantInputV1.__dataclass_fields__
    assert fields["provider_evaluation_profile_ref"].default == PRODUCTION_PROVIDER_EVALUATION_PROFILE_REF
    assert fields["capability_evaluation_profile_ref"].default == PRODUCTION_CAPABILITY_EVALUATION_PROFILE_REF
    assert "action_admission_profile_ref" not in fields


def test_controlled_action_ref_only_requery_uses_owner_namespace() -> None:
    scope = build_controlled_canonical_runtime_scope_v1("g06-ref-only-action")

    assert scope is not None
    action = query_current_admitted_action_v1(scope[0])
    assert action is not None
    assert action.profile_ref == ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1


def test_controlled_engine_retains_distinct_provider_identity() -> None:
    summary = ProviderBindingRuntimeAllocationExecutionEvaluationEngineV1().run()
    case = next(
        item
        for item in summary["cases"]
        if item["case_id"] == "MULTIPLE_PROVIDER_DISTINCT_BINDINGS"
    )
    decisions = case["binding_decision"]["decisions"]
    provider_refs = tuple(item["provider_ref"] for item in decisions)

    assert set(provider_refs) == {"provider:controlled:1", "provider:controlled:2"}
    assert len(set(provider_refs)) == 2
