"""Focused grant issue/carry/effect-time checks for controlled YOLO execution."""

from dataclasses import replace

from capabilities.midplatform.core.provider_runtime_to_observation_ingress.engine_v1 import (
    ProviderRuntimeObservationIngressEngineV1,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.fixtures_v1 import (
    build_provider_observation_cases_v1,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.real_provider_execution_runner_v1 import (
    _controlled_runtime_grant,
    build_runner_summary_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_active_observation_control_engine_v1 import (
    FieldPerceptionActiveObservationControlEngineV1,
)
from capabilities.midplatform.model_manager.registry.provider_registry_loader_v1 import (
    get_provider_by_id,
    is_provider_routing_eligible,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_authorization_state_v1 import (
    query_current_effect_eligibility_for_grant,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    invalidate_runtime_authorization_state,
)


def _owner_grant():
    case = replace(
        build_provider_observation_cases_v1()[0],
        case_id="PR_ADMISSION_02_GRANT_PROPAGATION",
        execution_instance_ref="provider-runtime:pr-admission-02-focused",
    )
    ingress = ProviderRuntimeObservationIngressEngineV1()
    fpo = FieldPerceptionActiveObservationControlEngineV1().run_case(
        ingress._fpo_payload(case)
    )
    requirement, _assessment, resolution, errors = ingress._resolve(case, fpo)
    assert not errors
    grant, grant_errors = _controlled_runtime_grant(case, fpo, requirement, resolution)
    assert not grant_errors
    assert grant is not None
    return grant


def test_missing_grant_fails_closed():
    result = query_current_effect_eligibility_for_grant(None)
    assert result.eligible is False
    assert result.failure_code == "RUNTIME_AUTHORIZATION_NOT_CURRENT"


def test_unknown_grant_fails_closed():
    grant = _owner_grant()
    result = query_current_effect_eligibility_for_grant(
        replace(grant, authorization_ref="runtime-authorization:unknown")
    )
    assert result.eligible is False
    assert result.failure_code == "RUNTIME_AUTHORIZATION_NOT_CURRENT"


def test_current_owner_grant_is_effect_time_eligible():
    grant = _owner_grant()
    result = query_current_effect_eligibility_for_grant(grant)
    assert result.eligible is True
    assert result.failure_code is None


def test_expired_grant_fails_closed():
    grant = _owner_grant()
    result = query_current_effect_eligibility_for_grant(
        replace(grant, validity_status="EXPIRED")
    )
    assert result.eligible is False
    assert result.failure_code == "RUNTIME_AUTHORIZATION_NOT_CURRENT"


def test_revoked_grant_fails_closed():
    grant = _owner_grant()
    invalidated = invalidate_runtime_authorization_state(
        authorization_ref=grant.authorization_ref,
        subject_ref="provider:yolo:local:v1",
        reason="focused-test-revocation",
    )
    assert invalidated is not None
    result = query_current_effect_eligibility_for_grant(grant)
    assert result.eligible is False


def test_identity_scope_mismatch_fails_closed():
    grant = _owner_grant()
    result = query_current_effect_eligibility_for_grant(
        replace(grant, provider_candidate_ref="provider:other")
    )
    assert result.eligible is False


def test_controlled_grant_does_not_enable_production_routing():
    _owner_grant()
    provider = get_provider_by_id("yolo11n")
    assert provider is not None
    assert is_provider_routing_eligible(provider) is False


def test_runner_carries_owner_grant_to_executor(monkeypatch):
    captured = {}

    def fake_run(self, case, *, source_ref, model_path, runtime_authorization_grant=None):
        captured["grant"] = runtime_authorization_grant
        return {
            "provider_real_execution_attempted": True,
            "provider_real_execution_verified": False,
            "provider_invoked": False,
            "model_invoked": False,
            "errors": ["focused-test-no-provider-call"],
        }

    monkeypatch.setattr(
        "capabilities.midplatform.core.provider_runtime_to_observation_ingress.real_provider_execution_runner_v1.RealProviderExecutionEngineV1.run",
        fake_run,
    )
    build_runner_summary_v1(
        source_ref="source:focused-test",
        model_path="model:focused-test",
    )
    assert captured["grant"] is not None
    assert captured["grant"].decision == "GRANTED"


def test_profile_eligibility_without_grant_does_not_authorize_effect():
    result = query_current_effect_eligibility_for_grant(None)
    assert result.eligible is False
