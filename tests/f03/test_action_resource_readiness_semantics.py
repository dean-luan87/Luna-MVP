"""F-03 resource/readiness boundary regressions."""

from dataclasses import replace

from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    ActionGovernanceEngineV1,
)
from capabilities.midplatform.core.action_governance.action_governance_fixture_v1 import (
    get_action_synthetic_fixtures_v1,
)
from capabilities.midplatform.core.action_governance.action_resource_types_v1 import (
    RESOURCE_AVAILABLE,
    RESOURCE_PENDING_REACTION,
    RESOURCE_UNKNOWN,
)
from capabilities.midplatform.core.cognitive_flow.integration.action_admission_safety_and_execution_boundary_closure.engine_v1 import (
    _positive_case,
    build_action_admission_safety_run_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.task_to_action_boundary_controlled_handoff.engine_v1 import (
    build_task_to_action_run_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    RuntimeExecutionGrantInputV1,
    form_runtime_execution_grants,
)


def _base_request():
    return get_action_synthetic_fixtures_v1()[0].request


def _action(state):
    return ActionGovernanceEngineV1().run_case(
        replace(_base_request(), scenario_id=f"F03_{state!r}", resource_state=state)
    )


def test_available_remains_candidate_ready_but_not_runtime_authority():
    output = _action(RESOURCE_AVAILABLE)

    assert output.resource_status.state == RESOURCE_AVAILABLE
    assert output.action_candidate.action_state == "READY_CANDIDATE"
    assert output.readiness.state == "candidate_ready"
    assert output.candidate_only is True
    assert output.action_candidate.runtime_authority is False
    assert output.runtime_handoff.candidate_only is True


def test_unavailable_preserves_suspended_behavior():
    output = _action("unavailable")

    assert output.action_candidate.action_state == "SUSPENDED"
    assert output.readiness.state == "suspended"
    assert output.resource_status.reaction == "become_suspended"
    assert output.action_candidate.runtime_authority is False


def test_unknown_remains_structural_candidate_but_is_unresolved():
    output = _action(RESOURCE_UNKNOWN)

    assert output.resource_status.state == RESOURCE_UNKNOWN
    assert output.resource_status.reaction == RESOURCE_PENDING_REACTION
    assert output.action_candidate.action_state == "READY_CANDIDATE"
    assert output.readiness.state == "candidate_ready"
    assert output.action_candidate.runtime_authority is False


def test_missing_and_malformed_resource_values_normalize_to_unknown():
    for value in (None, "", "partial", "conflict", "not_checked", "bogus"):
        output = _action(value)
        assert output.resource_status.state == RESOURCE_UNKNOWN
        assert output.resource_status.reaction == RESOURCE_PENDING_REACTION
        assert output.action_candidate.action_state == "READY_CANDIDATE"
        assert output.action_candidate.runtime_authority is False


def test_unknown_does_not_form_execution_eligibility_candidate():
    generic = build_task_to_action_run_v1()
    result = _positive_case(generic["cases"][0])

    assert result["action_boundary"]["request"]["resource_state"] == "unknown"
    assert result["execution_eligibility"]["status"] == "NOT_EXECUTION_ELIGIBLE"
    assert result["execution_eligibility"]["candidate_only"] is True
    assert result["runtime_executor_invoked"] is False


def test_controlled_safety_fixture_explicit_available_remains_eligible_candidate():
    run = build_action_admission_safety_run_v1()

    assert run["cases"]
    for case in run["cases"]:
        assert case["constraint_validation"]["resource_state"] == "available"
        assert case["execution_eligibility"]["status"] == "ELIGIBLE_CANDIDATE"
        assert case["execution_eligibility"]["candidate_only"] is True


def test_generic_task_to_action_path_does_not_fabricate_available():
    run = build_task_to_action_run_v1()

    assert run["cases"]
    for case in run["cases"]:
        assert case["action_boundary"]["request"]["resource_state"] == "unknown"


def test_explicit_task_to_action_resource_state_is_preserved():
    run = build_task_to_action_run_v1(resource_state="available")

    assert run["cases"]
    for case in run["cases"]:
        assert case["action_boundary"]["request"]["resource_state"] == "available"


def test_runtime_grant_rejects_unknown_resource_feasibility():
    result = form_runtime_execution_grants(
        RuntimeExecutionGrantInputV1(
            grant_request_ref="grant:f03:unknown",
            parent_cognitive_problem_ref="problem:f03",
            source_state_ref="state:f03",
            resource_feasibility_status="UNKNOWN",
        )
    )

    assert result.formation_status == "INVALID_INPUT"
    assert result.decisions == ()
    assert "resource_feasibility_status_invalid" in result.validation_errors


def test_action_candidate_ready_is_not_runtime_authority():
    output = _action(RESOURCE_AVAILABLE)

    assert output.readiness.state == "candidate_ready"
    assert output.action_candidate.runtime_authority is False
    assert output.runtime_handoff.candidate_only is True
    assert output.runtime_handoff.action_executed is False
    assert output.runtime_handoff.device_control_executed is False
