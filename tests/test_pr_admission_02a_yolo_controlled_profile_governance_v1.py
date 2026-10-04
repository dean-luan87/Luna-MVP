"""Focused governance tests for the real YOLO controlled-evaluation profiles."""

from capabilities.midplatform.model_manager.registries.universal_capability_slot.official_capability_catalog_governance_v1 import (
    CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_resolution_v1 import (
    evaluate_runtime_capability_admission_v1,
    resolve_capability_runtime_evaluation_profile_v1,
)
from capabilities.midplatform.model_manager.registry.provider_registry_loader_v1 import (
    get_provider_by_id,
    is_provider_routing_eligible,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_registry_v1 import (
    CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF,
    evaluate_provider_runtime_eligibility_v1,
    resolve_provider_runtime_evaluation_profile_v1,
)


YOLO_PROVIDER_REF = "provider:yolo:local:v1"
YOLO_MODEL_ID = "yolo11n"
OBJECT_DETECTION = "object_detection"
BOUNDING_KEY = (
    "runtime-scope:v2",
    "execution:profile-test",
    "provider:profile-test",
    OBJECT_DETECTION,
    "action:profile-test",
    "envelope:profile-test",
    "envelope-version:profile-test",
)


def test_yolo_provider_is_controlled_profile_eligible():
    profile = resolve_provider_runtime_evaluation_profile_v1(
        CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF
    )
    assert profile is not None
    assert YOLO_PROVIDER_REF in profile.provider_refs
    assert profile.production_canonical is False


def test_object_detection_is_controlled_profile_eligible():
    profile = resolve_capability_runtime_evaluation_profile_v1(
        CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF
    )
    assert profile is not None
    assert OBJECT_DETECTION in profile.capability_refs
    assert profile.production_canonical is False


def test_yolo_provider_is_not_added_to_production_profile():
    profile = resolve_provider_runtime_evaluation_profile_v1()
    assert profile is not None
    assert YOLO_PROVIDER_REF not in profile.provider_refs


def test_yolo_production_routing_remains_rejected():
    provider = get_provider_by_id(YOLO_MODEL_ID)
    assert provider is not None
    assert is_provider_routing_eligible(provider) is False


def test_synthetic_provider_does_not_substitute_for_yolo():
    profile = resolve_provider_runtime_evaluation_profile_v1(
        CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF
    )
    assert profile is not None
    assert "provider:controlled:1" in profile.provider_refs
    assert YOLO_PROVIDER_REF in profile.provider_refs
    assert "provider:controlled:1" != YOLO_PROVIDER_REF


def test_model_id_is_not_provider_identity():
    assert YOLO_MODEL_ID != YOLO_PROVIDER_REF


def test_unknown_provider_fails_closed():
    result = evaluate_provider_runtime_eligibility_v1(
        binding_key=BOUNDING_KEY,
        provider_candidate_ref="provider:unknown",
        capability_candidate_ref=OBJECT_DETECTION,
        execution_instance_preparation_candidate_ref="execution:profile-test",
        profile_ref=CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF,
    )
    assert result.status == "DENIED"


def test_unknown_capability_fails_closed():
    result = evaluate_runtime_capability_admission_v1(
        binding_key=BOUNDING_KEY,
        capability_candidate_ref="capability:unknown",
        provider_candidate_ref=YOLO_PROVIDER_REF,
        execution_instance_preparation_candidate_ref="execution:profile-test",
        profile_ref=CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF,
    )
    assert result.status == "DENIED"


def test_profile_eligibility_does_not_create_runtime_grant():
    provider_result = evaluate_provider_runtime_eligibility_v1(
        binding_key=BOUNDING_KEY,
        provider_candidate_ref=YOLO_PROVIDER_REF,
        capability_candidate_ref=OBJECT_DETECTION,
        execution_instance_preparation_candidate_ref="execution:profile-test",
        profile_ref=CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF,
    )
    capability_result = evaluate_runtime_capability_admission_v1(
        binding_key=BOUNDING_KEY,
        capability_candidate_ref=OBJECT_DETECTION,
        provider_candidate_ref=YOLO_PROVIDER_REF,
        execution_instance_preparation_candidate_ref="execution:profile-test",
        profile_ref=CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF,
    )
    assert provider_result.status == "ELIGIBLE"
    assert capability_result.status == "ADMITTED"
    assert not hasattr(provider_result, "grant_ref")
    assert not hasattr(capability_result, "grant_ref")


def test_profile_eligibility_does_not_change_provider_lifecycle():
    provider = get_provider_by_id(YOLO_MODEL_ID)
    assert provider is not None
    assert provider.get("lifecycle_state") == "candidate"


def test_profile_eligibility_does_not_change_model_lifecycle():
    provider = get_provider_by_id(YOLO_MODEL_ID)
    assert provider is not None
    assert provider.get("lifecycle_state") == "candidate"


def test_profile_eligibility_does_not_imply_production_admission():
    provider_profile = resolve_provider_runtime_evaluation_profile_v1(
        CONTROLLED_PROVIDER_EVALUATION_PROFILE_REF
    )
    capability_profile = resolve_capability_runtime_evaluation_profile_v1(
        CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF
    )
    assert provider_profile is not None and capability_profile is not None
    assert provider_profile.production_canonical is False
    assert capability_profile.production_canonical is False
