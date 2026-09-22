"""Focused proof that canonical Working Envelope lineage is transported only."""

from __future__ import annotations

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
from capabilities.midplatform.core.cognitive_flow.integration.cognitive_result_to_decision_governance_controlled_handoff.engine_v1 import (
    build_decision_handoff_run_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.decision_to_task_manager_controlled_handoff.engine_v1 import (
    build_decision_task_run_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.task_to_action_boundary_controlled_handoff.engine_v1 import (
    build_task_to_action_run_v1,
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


def _ref(owner: str, value: str) -> SourceRefV1:
    return SourceRefV1(owner, value, "v1", f"trace:{value}", f"provenance:{value}")


def _owner_issued_working_envelope():
    case = "g01-envelope-lineage"
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

    candidate = build_working_envelope(
        work_ref=f"work:{case}",
        concern_ref=concern.concern_ref,
        authority_grant_ref=grant.grant_ref,
        source_state_version_ref=state_version.version_ref,
        goal_refs=(f"goal:{case}",),
        context_refs=(f"context:{case}",),
        current_world_refs=(f"world:{case}:v1",),
        field_refs=(f"field:{case}",),
    )
    record = admit_working_envelope_v1(
        candidate,
        profile_ref=WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL,
    )
    assert record is not None
    return record


def _case(summary):
    return next(item for item in summary["cases"] if item["case_id"] == "CASE_A_SUFFICIENT_STOP")


def test_owner_issued_working_envelope_reaches_action_without_authority_upgrade():
    envelope = _owner_issued_working_envelope()

    decision_case = _case(
        build_decision_handoff_run_v1(
            "g01-envelope-lineage-decision",
            working_envelope=envelope,
        )
    )
    assert decision_case["decision_handoff"]["working_envelope_ref"] == envelope.envelope_ref
    assert (
        decision_case["decision_handoff"]["working_envelope_version_ref"]
        == envelope.envelope_version_ref
    )
    assert decision_case["decision"]["request"]["working_envelope_ref"] == envelope.envelope_ref
    assert (
        decision_case["decision"]["request"]["working_envelope_version_ref"]
        == envelope.envelope_version_ref
    )
    assert (
        decision_case["decision"]["output"]["handoff_candidate"]["working_envelope_ref"]
        == envelope.envelope_ref
    )
    assert (
        decision_case["decision"]["output"]["handoff_candidate"]["working_envelope_version_ref"]
        == envelope.envelope_version_ref
    )
    # DecisionGovernanceInputV1 intentionally exposes Envelope lineage without
    # duplicating concern_ref.  The downstream handoff DTOs that carry both
    # fields assert their semantic independence below.

    task_case = _case(
        build_decision_task_run_v1(
            "g01-envelope-lineage-task",
            working_envelope=envelope,
        )
    )
    assert task_case["working_envelope_ref"] == envelope.envelope_ref
    assert task_case["working_envelope_version_ref"] == envelope.envelope_version_ref
    assert task_case["task_handoff"]["working_envelope_ref"] == envelope.envelope_ref
    assert (
        task_case["task_handoff"]["working_envelope_version_ref"]
        == envelope.envelope_version_ref
    )
    assert task_case["task_handoff"]["concern_ref"] != envelope.envelope_ref
    assert task_case["task_manager"]["request"]["working_envelope_ref"] == envelope.envelope_ref
    assert (
        task_case["task_manager"]["request"]["working_envelope_version_ref"]
        == envelope.envelope_version_ref
    )

    action_case = _case(
        build_task_to_action_run_v1(
            resource_state="available",
            working_envelope=envelope,
        )
    )
    assert action_case["working_envelope_ref"] == envelope.envelope_ref
    assert action_case["working_envelope_version_ref"] == envelope.envelope_version_ref
    assert action_case["task_to_action_handoff"]["working_envelope_ref"] == envelope.envelope_ref
    assert (
        action_case["task_to_action_handoff"]["working_envelope_version_ref"]
        == envelope.envelope_version_ref
    )
    assert action_case["task_to_action_handoff"]["concern_ref"] != envelope.envelope_ref
    action_request = action_case["action_boundary"]["request"]
    assert action_request["working_envelope_ref"] == envelope.envelope_ref
    assert action_request["working_envelope_version_ref"] == envelope.envelope_version_ref
    assert action_case["action_boundary"]["runtime_dispatch"] is False
    assert "runtime_authorization_grant" not in action_request

    all_refs = {
        decision_case["decision_handoff"]["working_envelope_ref"],
        task_case["task_handoff"]["working_envelope_ref"],
        action_case["task_to_action_handoff"]["working_envelope_ref"],
    }
    all_version_refs = {
        decision_case["decision_handoff"]["working_envelope_version_ref"],
        task_case["task_handoff"]["working_envelope_version_ref"],
        action_case["task_to_action_handoff"]["working_envelope_version_ref"],
    }
    assert all_refs == {envelope.envelope_ref}
    assert all_version_refs == {envelope.envelope_version_ref}

    arbitrary = _case(
        build_decision_handoff_run_v1(
            "g01-envelope-lineage-arbitrary",
            working_envelope="working-envelope:arbitrary:v1",  # type: ignore[arg-type]
        )
    )
    assert arbitrary["decision_handoff"] is None
    assert "decision_handoff_requires_canonical_working_envelope_record" in arbitrary[
        "validation_errors"
    ]
