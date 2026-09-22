"""Focused Brain Concern/Grant owner-origin tests.

These tests cover Brain owner-origin and ref-only currentness contracts.
"""

from dataclasses import replace

import capabilities.midplatform.core.brain_governance.cognitive_grant_governance_v1 as cognitive_grant_governance
import capabilities.midplatform.core.brain_governance.concern_governance_v1 as concern_governance

from capabilities.midplatform.core.brain_governance.concern_governance_v1 import (
    BRAIN_CONTROLLED_PROFILE_REF,
    BRAIN_PRODUCTION_PROFILE_REF,
    CONCERN_CLOSED,
    CONCERN_CURRENT,
    CONCERN_SUPERSEDED,
    admit_concern,
    close_concern,
    query_current_concern,
    supersede_concern,
)
from capabilities.midplatform.core.brain_governance.cognitive_grant_governance_v1 import (
    COGNITIVE_GRANT_EXPIRED,
    COGNITIVE_GRANT_REVOKED,
    expire_cognitive_grant,
    issue_cognitive_grant,
    query_current_cognitive_grant,
    revoke_cognitive_grant,
)


def _admit(case: str, *, profile_ref: str = BRAIN_PRODUCTION_PROFILE_REF):
    return admit_concern(
        request_ref=f"request:{case}",
        goal_ref=f"goal:{case}",
        intent_ref=f"intent:{case}",
        scope_ref=f"scope:{case}",
        basis_refs=(f"evidence:{case}",),
        policy_refs=(f"policy:{case}",),
        profile_ref=profile_ref,
    )


def _grant(concern, case: str, *, profile_ref: str = BRAIN_PRODUCTION_PROFILE_REF):
    return issue_cognitive_grant(
        concern_ref=concern.concern_ref,
        receiver_ref=f"receiver:{case}",
        receiver_role="A_REASONING_ROLE",
        granted_authority_refs=("REALITY_REASONING",),
        work_ref=f"work:{case}",
        scope_ref=f"scope:{case}",
        expiry_ref=f"expiry:{case}",
        basis_refs=(f"basis:{case}",),
        policy_refs=(f"grant-policy:{case}",),
        profile_ref=profile_ref,
    )


def test_caller_candidate_cannot_self_admit_and_owner_issues_identity():
    candidate_ref = "caller-selected:concern"
    record = _admit("identity")

    assert record is not None
    assert record.state == CONCERN_CURRENT
    assert record.concern_ref != candidate_ref
    assert query_current_concern(candidate_ref) is None
    assert query_current_concern(record.concern_ref) == record


def test_concern_close_and_supersede_are_owner_transitions():
    closed = _admit("close")
    assert closed is not None
    closed_record = close_concern(closed.concern_ref, closure_ref="closure:close")
    assert closed_record is not None
    assert closed_record.state == CONCERN_CLOSED
    assert query_current_concern(closed.concern_ref) is None

    original = _admit("supersede")
    assert original is not None
    replacement = supersede_concern(
        original.concern_ref,
        request_ref="request:supersede:replacement",
        goal_ref="goal:supersede:replacement",
        intent_ref="intent:supersede:replacement",
        scope_ref="scope:supersede:replacement",
        basis_refs=("evidence:supersede:replacement",),
        policy_refs=("policy:supersede:replacement",),
    )
    assert replacement is not None
    assert replacement.supersedes_ref == original.concern_ref
    assert query_current_concern(original.concern_ref) is None
    assert query_current_concern(replacement.concern_ref) == replacement
    assert (
        query_current_concern(
            replacement.concern_ref,
            profile_ref=BRAIN_CONTROLLED_PROFILE_REF,
        )
        is None
    )


def test_grant_requires_current_concern_and_preserves_scope():
    concern = _admit("grant")
    assert concern is not None
    grant = _grant(concern, "grant")
    assert grant is not None
    assert query_current_cognitive_grant(grant.grant_ref, concern_ref=concern.concern_ref) == grant
    assert query_current_cognitive_grant(grant.grant_ref, scope_ref="scope:other") is None

    close_concern(concern.concern_ref, closure_ref="closure:grant")
    assert query_current_cognitive_grant(grant.grant_ref) is None


def test_grant_revoke_and_expiry_remove_current_authority():
    revoked_concern = _admit("revoked")
    assert revoked_concern is not None
    revoked = _grant(revoked_concern, "revoked")
    assert revoked is not None
    revoked_record = revoke_cognitive_grant(revoked.grant_ref, revocation_ref="revoke:test")
    assert revoked_record is not None
    assert revoked_record.state == COGNITIVE_GRANT_REVOKED
    assert query_current_cognitive_grant(revoked.grant_ref) is None

    expired_concern = _admit("expired")
    assert expired_concern is not None
    expired = _grant(expired_concern, "expired")
    assert expired is not None
    expired_record = expire_cognitive_grant(expired.grant_ref, expiry_ref="expiry:test")
    assert expired_record is not None
    assert expired_record.state == COGNITIVE_GRANT_EXPIRED
    assert query_current_cognitive_grant(expired.grant_ref) is None


def test_brain_profiles_are_owner_defined_and_isolated():
    production = _admit("profile", profile_ref=BRAIN_PRODUCTION_PROFILE_REF)
    controlled = _admit("profile", profile_ref=BRAIN_CONTROLLED_PROFILE_REF)
    assert production is not None and controlled is not None
    assert production.concern_ref != controlled.concern_ref
    assert query_current_concern(production.concern_ref, profile_ref=BRAIN_CONTROLLED_PROFILE_REF) is None
    assert query_current_concern(controlled.concern_ref, profile_ref=BRAIN_PRODUCTION_PROFILE_REF) is None

    assert _grant(production, "profile", profile_ref=BRAIN_PRODUCTION_PROFILE_REF) is not None
    assert _grant(controlled, "profile", profile_ref=BRAIN_CONTROLLED_PROFILE_REF) is not None


def test_controlled_concern_and_grant_support_ref_only_owner_requery():
    concern = _admit("ref-only-controlled", profile_ref=BRAIN_CONTROLLED_PROFILE_REF)
    assert concern is not None
    grant = _grant(
        concern,
        "ref-only-controlled",
        profile_ref=BRAIN_CONTROLLED_PROFILE_REF,
    )
    assert grant is not None

    assert query_current_concern(concern.concern_ref) is concern
    assert query_current_cognitive_grant(grant.grant_ref) is grant
    assert (
        query_current_concern(
            concern.concern_ref,
            profile_ref=BRAIN_PRODUCTION_PROFILE_REF,
        )
        is None
    )
    assert (
        query_current_cognitive_grant(
            grant.grant_ref,
            profile_ref=BRAIN_PRODUCTION_PROFILE_REF,
        )
        is None
    )

    assert close_concern(concern.concern_ref, closure_ref="closure:ref-only") is not None
    assert query_current_concern(concern.concern_ref) is None
    assert query_current_cognitive_grant(grant.grant_ref) is None


def test_brain_owner_namespace_collision_fails_closed():
    concern = _admit("namespace-collision", profile_ref=BRAIN_CONTROLLED_PROFILE_REF)
    assert concern is not None
    assert (
        concern_governance._register_concern_namespace_v1(
            replace(concern, profile_ref=BRAIN_PRODUCTION_PROFILE_REF)
        )
        is False
    )

    grant = _grant(
        concern,
        "namespace-collision",
        profile_ref=BRAIN_CONTROLLED_PROFILE_REF,
    )
    assert grant is not None
    assert (
        cognitive_grant_governance._register_grant_namespace_v1(
            replace(grant, profile_ref=BRAIN_PRODUCTION_PROFILE_REF)
        )
        is False
    )
    assert query_current_concern(concern.concern_ref) is concern
    assert query_current_cognitive_grant(grant.grant_ref) is grant


def test_unknown_profile_fails_closed_for_admission_and_grant():
    assert _admit("unknown", profile_ref="brain-profile:caller-defined") is None

    concern = _admit("unknown-grant")
    assert concern is not None
    assert _grant(concern, "unknown-grant", profile_ref="brain-profile:caller-defined") is None
