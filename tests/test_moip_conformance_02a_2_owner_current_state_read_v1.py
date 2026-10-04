from pathlib import Path

from capabilities.midplatform.core.cognitive_flow.integration.capability_model_provider_binding_controlled.current_state_read_v1 import (
    read_capability_model_binding_current_state,
    read_model_provider_binding_current_state,
)
from capabilities.midplatform.model_manager.lifecycle.model_current_state_read_v1 import (
    read_model_current_state,
)
from capabilities.midplatform.model_manager.registry.provider_current_state_read_v1 import (
    read_provider_current_state,
)


ROOT = Path(__file__).resolve().parents[1]


def test_known_model_is_bounded_static_read():
    result = read_model_current_state("yolo11n")
    assert result["read_status"] == "BOUNDED_STATIC_CURRENT_STATE"
    assert result["owner_ref"] == "Model Governance"


def test_unknown_model_fails_closed():
    assert read_model_current_state("missing-model")["read_status"] == "UNKNOWN"


def test_model_families_is_not_a_model_fallback():
    result = read_model_current_state("internvl2_5")
    assert result["lifecycle_state"] == "candidate"
    assert result["read_status"] == "BOUNDED_STATIC_CURRENT_STATE"


def test_known_provider_returns_provider_state_only():
    result = read_provider_current_state("provider:yolo:local:v1")
    assert result["owner_ref"] == "Provider Governance"
    assert result["lifecycle_state"] == "candidate"


def test_provider_state_does_not_change_model_read():
    model = read_model_current_state("yolo11n")
    provider = read_provider_current_state("provider:yolo:local:v1")
    assert model["lifecycle_state"] == "candidate"
    assert provider["lifecycle_state"] == "candidate"


def test_unknown_provider_fails_closed():
    assert read_provider_current_state("provider:missing:v1")["read_status"] == "UNKNOWN"


def test_known_capability_model_binding_returns_own_state():
    result = read_capability_model_binding_current_state("capability-model-binding:object-detection:yolo11n:v1", repo_root=ROOT)
    assert result["lifecycle_state"] == "candidate"
    assert result["compatibility_status"] == "declared"


def test_known_model_provider_binding_returns_own_state():
    result = read_model_provider_binding_current_state("model-provider-binding:yolo11n:yolo:v1", repo_root=ROOT)
    assert result["lifecycle_state"] == "candidate"
    assert result["compatibility_status"] == "declared"


def test_declared_compatibility_is_not_production_eligibility():
    result = read_capability_model_binding_current_state("capability-model-binding:object-detection:yolo11n:v1", repo_root=ROOT)
    assert result["compatibility_status"] == "declared"
    assert "production_eligible" not in result


def test_source_revision_mismatch_fails_closed():
    result = read_model_current_state("yolo11n", expected_source_revision="declaration:wrong:v9")
    assert result["read_status"] == "UNKNOWN"


def test_missing_currentness_basis_is_not_silently_filled():
    result = read_provider_current_state("provider:missing:v1")
    assert result["read_status"] == "UNKNOWN"
    assert result["currentness_basis"] is None


def test_read_result_has_no_aggregate_authority_fields():
    result = read_model_current_state("yolo11n")
    assert "production_ready" not in result
    assert "globally_eligible" not in result
