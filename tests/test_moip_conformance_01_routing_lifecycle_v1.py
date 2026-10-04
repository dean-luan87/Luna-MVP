"""MOIP-CONFORMANCE-01: activation precedes production routing eligibility."""

import pytest

from capabilities.midplatform.core.provider_runtime_to_observation_ingress import (
    engine_v1 as ingress_engine,
)
from capabilities.midplatform.model_manager.engines import (
    model_provider_routing_lifecycle_closure_v1 as closure,
)
from capabilities.midplatform.model_manager.lifecycle.model_admission_processor_v1 import (
    complete_admission,
)
from capabilities.midplatform.model_manager.lifecycle.model_registry_state_machine_v1 import (
    ROUTING_ELIGIBLE_STATES,
    is_routing_eligible,
    transition_model_state,
)
from capabilities.midplatform.model_manager.registry.provider_registry_loader_v1 import (
    filter_routing_eligible,
    get_provider_by_id,
    is_provider_routing_eligible,
    list_capability_providers,
)


@pytest.mark.parametrize(
    ("state", "admission_status", "expected"),
    (
        ("candidate", "pending", False),
        ("evaluating", "pending", False),
        ("admitted", "admitted", False),
        ("active", "admitted", True),
        ("active", "pending", False),
        ("active", "rejected", False),
        ("active", "", False),
        ("blocked", "admitted", False),
    ),
)
def test_shared_routing_prerequisite(state, admission_status, expected):
    assert ROUTING_ELIGIBLE_STATES == frozenset({"active"})
    assert is_routing_eligible(state, admission_status=admission_status) is expected


def test_admission_then_separate_activation():
    evaluating = {
        "model_id": "model:controlled",
        "lifecycle_state": "evaluating",
        "admission_status": "pending",
    }
    admission = complete_admission(
        model_record=evaluating,
        benchmark_record={"evaluation_status": "passed", "record_id": "benchmark:1"},
    )
    assert admission["admitted"] is True
    assert admission["model_record"]["lifecycle_state"] == "admitted"
    assert admission["routing_eligible"] is False

    activation = transition_model_state(
        model_record=admission["model_record"],
        to_state="active",
        reason="activation_approved",
    )
    assert activation["success"] is True
    assert activation["model_record"]["admission_status"] == "admitted"
    assert activation["routing_eligible"] is True


def test_provider_loader_rejects_admitted_and_invalid_active():
    assert not is_provider_routing_eligible(
        {"provider_id": "provider:fixture:admitted", "lifecycle_state": "admitted", "admission_status": "admitted"}
    )
    assert not is_provider_routing_eligible(
        {"provider_id": "provider:fixture:active-pending", "lifecycle_state": "active", "admission_status": "pending"}
    )
    assert is_provider_routing_eligible(
        {"provider_id": "provider:fixture:active", "lifecycle_state": "active", "admission_status": "admitted"}
    )


def test_production_style_selector_excludes_admitted_provider(monkeypatch):
    providers = [
        {"provider_id": "provider:fixture:admitted", "model_id": "model:fixture:active", "lifecycle_state": "admitted", "admission_status": "admitted"},
        {"provider_id": "provider:fixture:active", "model_id": "model:fixture:active", "lifecycle_state": "active", "admission_status": "admitted"},
    ]
    def bounded_state(*, lifecycle_state, admission_status):
        return {
            "read_status": "BOUNDED_STATIC_CURRENT_STATE",
            "source_revision": "declaration:test:v1",
            "currentness_basis": "locked_test_declaration",
            "lifecycle_state": lifecycle_state,
            "admission_status": admission_status,
        }

    provider_states = {
        "provider:fixture:admitted": bounded_state(
            lifecycle_state="admitted", admission_status="admitted"
        ),
        "provider:fixture:active": bounded_state(
            lifecycle_state="active", admission_status="admitted"
        ),
    }
    model_states = {
        "model:fixture:active": bounded_state(
            lifecycle_state="active", admission_status="admitted"
        )
    }
    monkeypatch.setattr(
        closure,
        "read_provider_current_state",
        lambda identity_ref: provider_states[identity_ref],
    )
    monkeypatch.setattr(
        closure,
        "read_model_current_state",
        lambda identity_ref: model_states[identity_ref],
    )
    monkeypatch.setattr(ingress_engine, "list_capability_providers", lambda _: providers)
    admitted_result = closure.evaluate_model_provider_routing_lifecycle_closure(providers[0])
    assert admitted_result["reasons"] == ("provider_lifecycle_not_active",)
    assert ingress_engine.ProviderRuntimeObservationIngressEngineV1._select_provider(
        "object_detection"
    )["model_id"] == "model:fixture:active"

    monkeypatch.setattr(ingress_engine, "list_capability_providers", lambda _: providers[:1])
    assert ingress_engine.ProviderRuntimeObservationIngressEngineV1._select_provider(
        "object_detection"
    ) is None


def test_existing_ocr_is_active_and_yolo_candidate_is_not_routable():
    ocr = get_provider_by_id("ocr_v1")
    yolo = get_provider_by_id("yolo11n")
    assert ocr is not None and ocr["lifecycle_state"] == "active"
    assert ocr["admission_status"] == "admitted"
    assert is_provider_routing_eligible(ocr)
    assert "ocr_v1" in {
        provider["model_id"]
        for provider in filter_routing_eligible(list_capability_providers("text_recognition"))
    }
    assert yolo is not None and yolo["lifecycle_state"] == "candidate"
    assert not is_provider_routing_eligible(yolo)
