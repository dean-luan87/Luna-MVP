from dataclasses import replace

import pytest

from capabilities.evaluation.provider_binding_runtime_allocation_execution_instance_controlled.engine_v1 import (
    ProviderBindingRuntimeAllocationExecutionEvaluationEngineV1,
)
from capabilities.evaluation.provider_binding_runtime_allocation_execution_instance_controlled.fixtures_v1 import (
    valid_profile as binding_profile,
)
from capabilities.evaluation.provider_session_controlled_invocation_multiscenario_sandbox.engine_v1 import (
    ProviderSessionControlledInvocationEvaluationEngineV1,
)
from capabilities.evaluation.provider_session_controlled_invocation_multiscenario_sandbox.fixtures_v1 import (
    valid_profile as session_profile,
)
from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    compute_unified_final_decision,
    run_governance_postflight,
)


def _artifact(**values: object) -> dict[str, object]:
    return {"candidate_only": False, "read_only": True, **values}


@pytest.mark.parametrize("profile_factory", (binding_profile, session_profile))
@pytest.mark.parametrize(
    "runtime_field",
    (
        "runtime_started",
        "provider_session_started",
        "gateway_submission",
        "execution_instance_created",
        "resource_allocated",
    ),
)
def test_mechanical_authority_cannot_suppress_positive_runtime_signal(
    profile_factory, runtime_field: str
) -> None:
    result = run_governance_postflight(
        profile_factory(), _artifact(**{runtime_field: True})
    )
    assert result.status == "GOVERNANCE_POSTFLIGHT_BLOCKED"
    assert f"runtime_effect_without_authority:{runtime_field}" in result.blocker_refs


@pytest.mark.parametrize("profile_factory", (binding_profile, session_profile))
def test_mechanical_only_record_scope_remains_valid(profile_factory) -> None:
    profile = profile_factory()
    result = run_governance_postflight(
        profile,
        _artifact(
            mechanical_provider_session_record_created=True,
            mechanical_execution_identity_record_created=True,
            mechanical_resource_allocation_record_created=True,
        ),
    )
    assert result.status == "PASS"
    assert result.blocker_refs == ()


def test_controlled_provider_session_uses_mechanical_record_scope() -> None:
    result = ProviderSessionControlledInvocationEvaluationEngineV1().run()
    executed = [item for item in result["cases"] if item["business_engine_executed"]]
    assert executed
    assert all(item["governance_postflight"]["status"] == "PASS" for item in executed)
    assert all(
        item["lifecycle_artifact"]["provider_session_started"] is False
        for item in executed
    )
    assert any(
        item["lifecycle_artifact"]["mechanical_provider_session_record_created"]
        for item in executed
    )


def test_controlled_binding_allocation_uses_mechanical_record_scope() -> None:
    result = ProviderBindingRuntimeAllocationExecutionEvaluationEngineV1().run()
    executed = [item for item in result["cases"] if item["business_engine_executed"]]
    assert executed
    assert all(item["governance_postflight"]["status"] == "PASS" for item in executed)
    assert result["runtime_started"] is False
    assert result["provider_session_started"] is False
    assert result["gateway_submission"] is False


@pytest.mark.parametrize("profile_factory", (binding_profile, session_profile))
def test_mechanical_authority_with_prohibited_runtime_signals_false_may_pass(
    profile_factory,
) -> None:
    result = run_governance_postflight(
        profile_factory(),
        _artifact(
            runtime_started=False,
            provider_session_started=False,
            gateway_submission=False,
            execution_instance_created=False,
            resource_allocated=False,
        ),
    )
    assert result.status == "PASS"


@pytest.mark.parametrize("profile_factory", (binding_profile, session_profile))
def test_missing_or_malformed_runtime_fields_do_not_create_positive_signal(
    profile_factory,
) -> None:
    for value in (None, "UNKNOWN", {"value": True}):
        result = run_governance_postflight(
            profile_factory(), _artifact(runtime_started=value)
        )
        assert result.status == "PASS"
        assert "runtime_effect_without_authority:runtime_started" not in result.blocker_refs


def test_runtime_authority_positive_path_remains_valid() -> None:
    profile = replace(
        binding_profile(), runtime_authority=True, mechanical_authority=False
    )
    result = run_governance_postflight(
        profile,
        _artifact(
            runtime_started=True,
            provider_session_started=True,
            gateway_submission=True,
            execution_instance_created=True,
            resource_allocated=True,
        ),
    )
    assert result.status == "PASS"


def test_mechanical_authority_does_not_create_runtime_grant_or_final_authority() -> None:
    postflight = run_governance_postflight(
        binding_profile(), _artifact(runtime_grant_ref="missing")
    )
    assert postflight.status == "PASS"
    assert compute_unified_final_decision(
        functional_checks_passed=True,
        contract_failures=("runtime_grant_not_verified",),
        governance_preflight="PASS",
        governance_postflight=postflight.status,
        cognitive_logic_result="PASS",
        operational_result="PASS",
    ) == "NO_GO"


def test_legacy_overloaded_record_fields_cannot_bypass_runtime_guard() -> None:
    result = run_governance_postflight(
        binding_profile(), _artifact(execution_instance_created=True)
    )
    assert result.status == "GOVERNANCE_POSTFLIGHT_BLOCKED"
