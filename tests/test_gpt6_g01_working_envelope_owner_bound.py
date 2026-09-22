"""Focused owner-origin tests for canonical Working Envelope admission."""

from __future__ import annotations

from dataclasses import replace

import capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.working_envelope_governance_v1 as working_envelope_governance

from capabilities.midplatform.core.brain_governance.concern_governance_v1 import (
    BRAIN_CONTROLLED_PROFILE_REF,
    BRAIN_PRODUCTION_PROFILE_REF,
    admit_concern,
    close_concern,
)
from capabilities.midplatform.core.brain_governance.cognitive_grant_governance_v1 import (
    issue_cognitive_grant,
    revoke_cognitive_grant,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.a_working_envelope_cognitive_requirement_engine_v1 import (
    build_working_envelope,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.working_envelope_governance_v1 import (
    WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1,
    WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL,
    WORKING_ENVELOPE_SUPERSEDED,
    admit_working_envelope_v1,
    invalidate_working_envelope_v1,
    query_current_working_envelope_v1,
    query_working_envelope_version_v1,
    refresh_working_envelope_v1,
)
from capabilities.midplatform.core.cognitive_state_formation import (
    invalidate_cognitive_state_version_v1,
    issue_cognitive_state_version_v1,
    query_valid_cognitive_state_version_v1,
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


def _ref(owner: str, value: str) -> SourceRefV1:
    return SourceRefV1(owner, value, "v1", f"trace:{value}", f"provenance:{value}")


def _cstate(profile_ref: str = COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL):
    output = CognitiveStateFormationEngineV1().run_case(
        CognitiveStateFormationInputV1(
            scenario_id="F09",
            context_refs=(_ref("Context", "context:envelope"),),
            pcn_refs=(_ref("PCN", "pcn:envelope"),),
            intent_refs=(_ref("Intent", "intent:envelope"),),
            field_refs=(_ref("Field", "field:envelope"),),
            observation_refs=(_ref("Observation", "observation:envelope"),),
            evidence_refs=(_ref("Evidence", "evidence:envelope"),),
            goal_refs=(_ref("Goal", "goal:envelope"),),
            concern_refs=(_ref("Concern", "concern:formation"),),
            information_need_refs=(_ref("Need", "need:envelope"),),
            task_refs=(_ref("Task", "task:envelope"),),
            role_refs=(_ref("Role", "role:envelope"),),
            relation_refs=(_ref("Field", "relation:envelope"),),
            candidate_only=True,
            synthetic_only=True,
        )
    )
    return issue_cognitive_state_version_v1(output, profile_ref=profile_ref)


def _brain_pair(case: str, profile_ref: str = BRAIN_PRODUCTION_PROFILE_REF):
    concern = admit_concern(
        request_ref=f"request:{case}",
        goal_ref=f"goal:{case}",
        intent_ref=f"intent:{case}",
        scope_ref=f"scope:{case}",
        basis_refs=(f"basis:{case}",),
        policy_refs=(f"policy:{case}",),
        profile_ref=profile_ref,
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
        profile_ref=profile_ref,
    )
    assert grant is not None
    return concern, grant


def _candidate(case: str, concern_ref: str, grant_ref: str, state_ref: str):
    return build_working_envelope(
        work_ref=f"work:{case}",
        concern_ref=concern_ref,
        authority_grant_ref=grant_ref,
        source_state_version_ref=state_ref,
        goal_refs=(f"goal:{case}",),
        context_refs=(f"context:{case}",),
        current_world_refs=(f"world:{case}:v1",),
        field_refs=(f"field:{case}",),
    )


def _admitted(case: str, profile_ref: str = WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL):
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
    concern, grant = _brain_pair(case, brain_profile)
    cstate = _cstate(cstate_profile)
    assert cstate is not None
    candidate = _candidate(case, concern.concern_ref, grant.grant_ref, cstate.version_ref)
    record = admit_working_envelope_v1(candidate, profile_ref=profile_ref)
    assert record is not None
    return concern, grant, cstate, candidate, record


def test_caller_cannot_self_admit_envelope() -> None:
    fake = _candidate("fake", "caller:concern", "caller:grant", "caller:cstate")
    assert admit_working_envelope_v1(fake) is None


def test_caller_cannot_choose_canonical_identity_or_version() -> None:
    _, _, _, candidate, record = _admitted("identity")
    assert record.envelope_ref != candidate.work_ref
    assert record.envelope_version_ref != "caller:selected:version"
    assert record.canonical is True


def test_admission_requires_current_concern() -> None:
    concern, grant, cstate, candidate, _ = _admitted("closed-concern")
    assert close_concern(concern.concern_ref, closure_ref="closure:envelope") is not None
    assert admit_working_envelope_v1(candidate) is None
    assert query_valid_cognitive_state_version_v1(cstate.version_ref) is cstate
    assert grant.concern_ref == concern.concern_ref


def test_admission_requires_current_grant() -> None:
    concern, grant, _, candidate, _ = _admitted("revoked-grant")
    assert revoke_cognitive_grant(grant.grant_ref, revocation_ref="revoke:envelope") is not None
    assert admit_working_envelope_v1(candidate) is None
    assert concern.concern_ref == grant.concern_ref


def test_grant_must_match_current_concern() -> None:
    first, _, cstate, _, _ = _admitted("mismatch-first")
    second, second_grant = _brain_pair("mismatch-second")
    candidate = _candidate("mismatch", first.concern_ref, second_grant.grant_ref, cstate.version_ref)
    assert admit_working_envelope_v1(candidate) is None
    assert second.concern_ref != first.concern_ref


def test_admission_requires_valid_cognitive_state_version() -> None:
    concern, grant = _brain_pair("invalid-cstate")
    candidate = _candidate("invalid-cstate", concern.concern_ref, grant.grant_ref, "unknown:cstate")
    assert admit_working_envelope_v1(candidate) is None


def test_cstate_does_not_need_concern_or_grant_binding() -> None:
    _, _, cstate, _, _ = _admitted("cstate-independent")
    assert not hasattr(cstate, "concern_ref")
    assert not hasattr(cstate, "grant_ref")


def test_same_valid_cstate_can_be_reused_across_concerns() -> None:
    cstate = _cstate()
    assert cstate is not None
    first, first_grant = _brain_pair("reuse-first")
    second, second_grant = _brain_pair("reuse-second")
    first_record = admit_working_envelope_v1(
        _candidate("reuse-first", first.concern_ref, first_grant.grant_ref, cstate.version_ref)
    )
    second_record = admit_working_envelope_v1(
        _candidate("reuse-second", second.concern_ref, second_grant.grant_ref, cstate.version_ref)
    )
    assert first_record is not None and second_record is not None
    assert first_record.cognitive_state_version_ref == second_record.cognitive_state_version_ref


def test_concern_closure_fails_closed_for_current_envelope_without_mutating_cstate() -> None:
    concern, _, cstate, _, record = _admitted("query-concern")
    assert close_concern(concern.concern_ref, closure_ref="closure:query") is not None
    assert query_current_working_envelope_v1(record.envelope_ref) is None
    assert query_valid_cognitive_state_version_v1(cstate.version_ref) is cstate


def test_grant_revocation_fails_closed_for_current_envelope_without_mutating_cstate() -> None:
    _, grant, cstate, _, record = _admitted("query-grant")
    assert revoke_cognitive_grant(grant.grant_ref, revocation_ref="revoke:query") is not None
    assert query_current_working_envelope_v1(record.envelope_ref) is None
    assert query_valid_cognitive_state_version_v1(cstate.version_ref) is cstate


def test_cstate_invalidation_fails_closed_for_current_envelope() -> None:
    _, _, cstate, _, record = _admitted("query-cstate")
    assert invalidate_cognitive_state_version_v1(
        cstate.version_ref,
        reason_ref="invalidate:query",
    ) is not None
    assert query_current_working_envelope_v1(record.envelope_ref) is None


def test_refresh_supersedes_old_envelope_version() -> None:
    concern, grant, _, candidate, first = _admitted("refresh")
    second_cstate = _cstate()
    assert second_cstate is not None
    refreshed = refresh_working_envelope_v1(
        first.envelope_ref,
        _candidate("refresh:v2", concern.concern_ref, grant.grant_ref, second_cstate.version_ref),
    )
    assert refreshed is not None
    assert refreshed.envelope_ref == first.envelope_ref
    assert refreshed.envelope_version_ref != first.envelope_version_ref
    assert query_current_working_envelope_v1(first.envelope_ref) is refreshed
    historical = query_working_envelope_version_v1(first.envelope_version_ref)
    assert historical is not None
    assert historical.state == WORKING_ENVELOPE_SUPERSEDED


def test_newer_cstate_version_alone_does_not_invalidate_old_envelope() -> None:
    _, _, _, _, first = _admitted("newer-cstate")
    newer = _cstate()
    assert newer is not None
    assert query_current_working_envelope_v1(first.envelope_ref) is first
    assert query_valid_cognitive_state_version_v1(newer.version_ref) is newer


def test_historical_valid_cstate_supports_envelope() -> None:
    cstate = _cstate()
    newer = _cstate()
    assert cstate is not None and newer is not None
    concern, grant = _brain_pair("historical-cstate")
    record = admit_working_envelope_v1(
        _candidate("historical-cstate", concern.concern_ref, grant.grant_ref, cstate.version_ref)
    )
    assert record is not None
    assert query_valid_cognitive_state_version_v1(cstate.version_ref) is cstate
    assert query_valid_cognitive_state_version_v1(newer.version_ref) is newer


def test_envelope_invalidation_is_owner_transition() -> None:
    _, _, cstate, _, record = _admitted("invalidate-envelope")
    invalidated = invalidate_working_envelope_v1(
        record.envelope_ref,
        reason_ref="constraint:invalidated",
    )
    assert invalidated is not None
    assert invalidated.state == "INVALIDATED"
    assert query_current_working_envelope_v1(record.envelope_ref) is None
    assert query_valid_cognitive_state_version_v1(cstate.version_ref) is cstate


def test_caller_cannot_declare_current_candidate() -> None:
    concern, grant, cstate, candidate, _ = _admitted("candidate-flag")
    forged = replace(candidate, candidate_only=False)
    assert admit_working_envelope_v1(forged) is None
    assert query_current_working_envelope_v1("caller:envelope") is None
    assert concern.concern_ref == grant.concern_ref
    assert query_valid_cognitive_state_version_v1(cstate.version_ref) is cstate


def test_controlled_and_production_envelope_state_are_isolated() -> None:
    _, _, _, _, production = _admitted("production", WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL)
    _, _, _, _, controlled = _admitted(
        "controlled",
        WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1,
    )
    assert query_current_working_envelope_v1(
        production.envelope_ref,
        profile_ref=WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1,
    ) is None
    assert query_current_working_envelope_v1(
        controlled.envelope_ref,
        profile_ref=WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL,
    ) is None


def test_controlled_envelope_supports_ref_only_owner_requery() -> None:
    concern, _, _, _, record = _admitted(
        "ref-only-controlled",
        WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1,
    )
    assert query_current_working_envelope_v1(record.envelope_ref) is record
    assert query_working_envelope_version_v1(record.envelope_version_ref) is record
    assert (
        query_current_working_envelope_v1(
            record.envelope_ref,
            profile_ref=WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL,
        )
        is None
    )

    assert close_concern(concern.concern_ref, closure_ref="closure:ref-only") is not None
    assert query_current_working_envelope_v1(record.envelope_ref) is None
    assert query_working_envelope_version_v1(record.envelope_version_ref) is record


def test_working_envelope_owner_namespace_collision_fails_closed() -> None:
    _, _, _, _, record = _admitted(
        "namespace-collision",
        WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1,
    )
    assert (
        working_envelope_governance._register_working_envelope_namespace_v1(
            replace(
                record,
                profile_ref=WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL,
            )
        )
        is False
    )
    assert query_current_working_envelope_v1(record.envelope_ref) is record


def test_unknown_profile_fails_closed() -> None:
    _, _, cstate, candidate, _ = _admitted("unknown-profile")
    assert admit_working_envelope_v1(candidate, profile_ref="working-envelope:unknown") is None
    assert query_current_working_envelope_v1(
        "working-envelope:unknown:1",
        profile_ref="working-envelope:unknown",
    ) is None
    assert query_valid_cognitive_state_version_v1(cstate.version_ref) is cstate


def test_canonical_envelope_has_no_direct_lower_source_bindings() -> None:
    _, _, _, _, record = _admitted("no-lower-bindings")
    assert not hasattr(record, "field_refs")
    assert not hasattr(record, "current_world_refs")
    assert not hasattr(record, "evidence_refs")
    assert record.cognitive_state_version_ref
