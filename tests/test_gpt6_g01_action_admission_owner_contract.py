"""Focused Action Governance owner-bound admission contract tests."""

from __future__ import annotations

from dataclasses import replace

import capabilities.midplatform.core.action_governance.action_admission_governance_v1 as action_admission_governance

from capabilities.midplatform.core.action_governance.action_admission_governance_v1 import (
    ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1,
    ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL,
    admit_action_v1,
    cancel_admitted_action_v1,
    query_current_admitted_action_v1,
    query_historical_admitted_action_v1,
    revoke_admitted_action_v1,
    supersede_admitted_action_v1,
)
from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    ActionGovernanceEngineV1,
    form_runtime_safety_prerequisite_v1,
    invalidate_runtime_safety_prerequisite_v1,
)
from capabilities.midplatform.core.action_governance.action_io_types_v1 import (
    ActionGovernanceInputV1,
)
from capabilities.midplatform.core.brain_governance.concern_governance_v1 import (
    BRAIN_CONTROLLED_PROFILE_REF,
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
    WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1,
    WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL,
    admit_working_envelope_v1,
    invalidate_working_envelope_v1,
    refresh_working_envelope_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.decision_to_task_manager_controlled_handoff.engine_v1 import (
    build_decision_task_run_v1,
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
    COGNITIVE_STATE_PROFILE_CONTROLLED_EVALUATION_V1,
    COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL,
)
from capabilities.midplatform.core.cognitive_flow.integration.task_to_action_boundary_controlled_handoff.engine_v1 import (
    _action_request,
    _build_task_to_action_handoff,
)


def _ref(owner: str, value: str) -> SourceRefV1:
    return SourceRefV1(owner, value, "v1", f"trace:{value}", f"provenance:{value}")


def _working_envelope(case: str, profile_ref: str):
    brain_profile = (
        BRAIN_CONTROLLED_PROFILE_REF
        if profile_ref == WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1
        else BRAIN_PRODUCTION_PROFILE_REF
    )
    cstate_profile = (
        COGNITIVE_STATE_PROFILE_CONTROLLED_EVALUATION_V1
        if profile_ref == WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1
        else COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL
    )
    concern = admit_concern(
        request_ref=f"request:{case}",
        goal_ref=f"goal:{case}",
        intent_ref=f"intent:{case}",
        scope_ref=f"scope:{case}",
        basis_refs=(f"basis:{case}",),
        policy_refs=(f"policy:{case}",),
        profile_ref=brain_profile,
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
        profile_ref=brain_profile,
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
        profile_ref=cstate_profile,
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
    record = admit_working_envelope_v1(candidate, profile_ref=profile_ref)
    assert record is not None
    return record


def _action_bundle(case: str, profile_ref: str = ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL):
    envelope_profile = (
        WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1
        if profile_ref == ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1
        else WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL
    )
    envelope = _working_envelope(case, envelope_profile)
    task_summary = build_decision_task_run_v1(
        f"action-admission:{case}",
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
    action_request["scenario_id"] = f"action-admission:{case}"
    action_output = ActionGovernanceEngineV1().run_case(
        ActionGovernanceInputV1(**action_request)
    )
    safety_binding_key = (
        action_output.action_candidate.action_candidate_id,
        task_handoff.task_state_ref,
        task_handoff.decision_candidate_ref,
        envelope.envelope_ref,
        envelope.envelope_version_ref,
        "runtime-execution",
    )
    safety = form_runtime_safety_prerequisite_v1(
        binding_key=safety_binding_key,
        effect_class="runtime-execution",
        scope_kind="ACTION_ADMISSION",
    )
    return envelope, task_handoff, action_output, safety, safety_binding_key


def _admit(case: str, profile_ref: str = ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL):
    envelope, task_handoff, action_output, safety, safety_binding_key = _action_bundle(
        case, profile_ref
    )
    record = admit_action_v1(
        action_output,
        task_handoff=task_handoff,
        working_envelope_ref=envelope.envelope_ref,
        working_envelope_version_ref=envelope.envelope_version_ref,
        safety_prerequisite=safety,
        profile_ref=profile_ref,
    )
    assert record is not None
    return record, envelope, task_handoff, action_output, safety, safety_binding_key


def test_valid_action_candidate_is_owner_admitted_with_complete_lineage():
    record, envelope, task_handoff, action_output, safety, _ = _admit("valid")

    assert record.admitted_action_ref != record.action_candidate_ref
    assert record.admitted_action_ref.startswith("admitted-action:")
    assert record.lifecycle_status == "CURRENT"
    assert record.working_envelope_ref == envelope.envelope_ref
    assert record.working_envelope_version_ref == envelope.envelope_version_ref
    assert record.selected_decision_ref == task_handoff.decision_candidate_ref
    assert record.selected_task_ref == task_handoff.task_state_ref
    assert record.action_candidate == action_output.action_candidate
    assert record.safety_prerequisite_ref == safety.result_ref
    assert record.action_candidate.target_refs
    assert record.action_candidate.precondition_refs
    assert record.action_candidate.dependency_refs
    assert record.action_candidate.resource_refs
    assert not hasattr(record, "authorization_ref")
    assert not hasattr(record, "runtime_grant_ref")
    assert action_output.runtime_handoff.candidate_only is True
    assert action_output.runtime_handoff.action_executed is False
    assert action_output.runtime_handoff.device_control_executed is False
    assert query_current_admitted_action_v1(record.admitted_action_ref) is record


def test_caller_cannot_self_admit_choose_identity_or_use_fake_envelope():
    envelope, task_handoff, action_output, safety, _ = _action_bundle("caller-guards")
    forged_output = replace(action_output, candidate_only=False)
    assert (
        admit_action_v1(
            forged_output,
            task_handoff=task_handoff,
            working_envelope_ref=envelope.envelope_ref,
            working_envelope_version_ref=envelope.envelope_version_ref,
            safety_prerequisite=safety,
        )
        is None
    )
    assert (
        admit_action_v1(
            action_output,
            task_handoff=task_handoff,
            working_envelope_ref="working-envelope:caller-fake",
            working_envelope_version_ref="working-envelope:caller-fake:v1",
            safety_prerequisite=safety,
        )
        is None
    )
    forged_safety = replace(safety, revoked=True)
    assert (
        admit_action_v1(
            action_output,
            task_handoff=task_handoff,
            working_envelope_ref=envelope.envelope_ref,
            working_envelope_version_ref=envelope.envelope_version_ref,
            safety_prerequisite=forged_safety,
        )
        is None
    )


def test_admission_requeries_envelope_and_safety_currentness():
    record, envelope, task_handoff, action_output, safety, safety_binding_key = _admit(
        "currentness"
    )
    assert invalidate_working_envelope_v1(
        envelope.envelope_ref,
        reason_ref="action-admission:envelope-invalidated",
    ) is not None
    assert query_current_admitted_action_v1(record.admitted_action_ref) is None

    fresh = _action_bundle("safety-currentness")
    fresh_record = admit_action_v1(
        fresh[2],
        task_handoff=fresh[1],
        working_envelope_ref=fresh[0].envelope_ref,
        working_envelope_version_ref=fresh[0].envelope_version_ref,
        safety_prerequisite=fresh[3],
    )
    assert fresh_record is not None
    assert invalidate_runtime_safety_prerequisite_v1(
        binding_key=fresh[4],
        reason="action-admission:safety-invalidated",
    ) is not None
    assert query_current_admitted_action_v1(fresh_record.admitted_action_ref) is None
    assert safety.result_ref != fresh[3].result_ref
    assert task_handoff.task_state_ref
    assert action_output.action_candidate.action_candidate_id
    assert safety_binding_key


def test_refresh_supersedes_old_envelope_version_and_blocks_old_admission():
    envelope, task_handoff, action_output, safety, _ = _action_bundle("envelope-refresh")
    refreshed_candidate = build_working_envelope(
        work_ref="work:envelope-refresh:v2",
        concern_ref=envelope.concern_ref,
        authority_grant_ref=envelope.cognitive_grant_ref,
        source_state_version_ref=envelope.cognitive_state_version_ref,
        goal_refs=("goal:envelope-refresh",),
        context_refs=("context:envelope-refresh",),
        current_world_refs=("world:envelope-refresh:v2",),
        field_refs=("field:envelope-refresh:v2",),
    )
    refreshed = refresh_working_envelope_v1(
        envelope.envelope_ref,
        refreshed_candidate,
    )
    assert refreshed is not None
    assert refreshed.envelope_version_ref != envelope.envelope_version_ref
    assert (
        admit_action_v1(
            action_output,
            task_handoff=task_handoff,
            working_envelope_ref=envelope.envelope_ref,
            working_envelope_version_ref=envelope.envelope_version_ref,
            safety_prerequisite=safety,
        )
        is None
    )


def test_admission_lifecycle_preserves_history_and_fail_closed_queries():
    revoked, _, _, _, _, _ = _admit("revoke")
    assert revoke_admitted_action_v1(
        revoked.admitted_action_ref,
        reason_ref="action-admission:revoke",
    ) is not None
    assert query_current_admitted_action_v1(revoked.admitted_action_ref) is None
    assert query_historical_admitted_action_v1(revoked.admitted_action_ref).lifecycle_status == "REVOKED"

    cancelled, _, _, _, _, _ = _admit("cancel")
    assert cancel_admitted_action_v1(
        cancelled.admitted_action_ref,
        reason_ref="action-admission:cancel",
    ) is not None
    assert query_current_admitted_action_v1(cancelled.admitted_action_ref) is None
    assert query_historical_admitted_action_v1(cancelled.admitted_action_ref).lifecycle_status == "CANCELLED"

    old, _, _, _, _, _ = _admit("supersede-old")
    new, _, _, _, _, _ = _admit("supersede-new")
    transitioned = supersede_admitted_action_v1(
        old.admitted_action_ref,
        replacement_admitted_action_ref=new.admitted_action_ref,
        reason_ref="action-admission:supersede",
    )
    assert transitioned is not None
    assert transitioned.lifecycle_status == "SUPERSEDED"
    assert query_current_admitted_action_v1(old.admitted_action_ref) is None
    assert query_current_admitted_action_v1(new.admitted_action_ref) is new
    assert query_historical_admitted_action_v1(old.admitted_action_ref).lifecycle_status == "SUPERSEDED"


def test_profiles_are_isolated_and_unknown_profile_fails_closed():
    production = _action_bundle("production", ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL)
    controlled = _action_bundle(
        "controlled",
        ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1,
    )
    production_record = admit_action_v1(
        production[2],
        task_handoff=production[1],
        working_envelope_ref=production[0].envelope_ref,
        working_envelope_version_ref=production[0].envelope_version_ref,
        safety_prerequisite=production[3],
        profile_ref=ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL,
    )
    controlled_record = admit_action_v1(
        controlled[2],
        task_handoff=controlled[1],
        working_envelope_ref=controlled[0].envelope_ref,
        working_envelope_version_ref=controlled[0].envelope_version_ref,
        safety_prerequisite=controlled[3],
        profile_ref=ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1,
    )
    assert production_record is not None and controlled_record is not None
    assert query_current_admitted_action_v1(
        production_record.admitted_action_ref,
        profile_ref=ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1,
    ) is None
    assert query_current_admitted_action_v1(
        controlled_record.admitted_action_ref,
        profile_ref=ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL,
    ) is None
    assert (
        admit_action_v1(
            production[2],
            task_handoff=production[1],
            working_envelope_ref=production[0].envelope_ref,
            working_envelope_version_ref=production[0].envelope_version_ref,
            safety_prerequisite=production[3],
            profile_ref="action-admission:unknown",
        )
        is None
    )


def test_ref_only_query_resolves_owner_namespace_for_controlled_action():
    record, *_ = _admit(
        "ref-only-controlled",
        ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1,
    )

    assert query_current_admitted_action_v1(record.admitted_action_ref) is record
    assert (
        query_current_admitted_action_v1(
            record.admitted_action_ref,
            profile_ref=ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL,
        )
        is None
    )


def test_owner_namespace_collision_fails_closed():
    record, *_ = _admit("namespace-collision")
    colliding_record = replace(
        record,
        profile_ref=ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1,
    )

    assert (
        action_admission_governance._register_admitted_action_namespace_v1(
            colliding_record
        )
        is False
    )
    assert query_current_admitted_action_v1(record.admitted_action_ref) is record


def test_concern_ref_cannot_replace_envelope_and_runtime_handoff_stays_candidate():
    record, envelope, task_handoff, action_output, safety, _ = _admit("identity-separation")
    assert record.working_envelope_ref == envelope.envelope_ref
    assert record.working_envelope_ref != envelope.concern_ref
    assert record.working_envelope_version_ref == envelope.envelope_version_ref
    assert task_handoff.concern_ref != record.working_envelope_ref
    assert action_output.runtime_handoff.candidate_only is True
    assert action_output.runtime_handoff.execution_readiness == "candidate_ready"
    assert safety.authoritative is True
