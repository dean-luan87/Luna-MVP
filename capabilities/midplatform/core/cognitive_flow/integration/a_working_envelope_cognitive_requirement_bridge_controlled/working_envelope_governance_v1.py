"""Owner-bound Working Envelope admission and currentness.

The neighbouring bridge modules form candidate-only working-context data.  This
module is the owner boundary that resolves the three independent prerequisite
owners and issues immutable Envelope records without copying their authority.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from threading import RLock
from typing import Dict, Iterable, Optional, Tuple

from capabilities.midplatform.core.brain_governance.concern_governance_v1 import (
    BRAIN_CONTROLLED_PROFILE_REF,
    BRAIN_PRODUCTION_PROFILE_REF,
    CanonicalConcernRecordV1,
    query_current_concern,
)
from capabilities.midplatform.core.brain_governance.cognitive_grant_governance_v1 import (
    CognitiveGrantRecordV1,
    query_current_cognitive_grant,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    CognitiveStateVersionRecordV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_engine_v1 import (
    query_valid_cognitive_state_version_v1,
)

from .a_working_envelope_cognitive_requirement_types_v1 import (
    AWorkingEnvelopeCandidateV1,
)


WORKING_ENVELOPE_OWNER = "Working Envelope Governance"
WORKING_ENVELOPE_AUTHORITY = "WorkingEnvelope.ADMIT_ENVELOPE"
WORKING_ENVELOPE_CURRENT = "CURRENT"
WORKING_ENVELOPE_SUPERSEDED = "SUPERSEDED"
WORKING_ENVELOPE_INVALIDATED = "INVALIDATED"
WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL = BRAIN_PRODUCTION_PROFILE_REF
WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1 = BRAIN_CONTROLLED_PROFILE_REF
WORKING_ENVELOPE_CONSTRAINT_PROFILE = "working-envelope-constraints:v1"

_PROFILE_TO_CSTATE_PROFILE = {
    WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL:
        "cognitive-state-profile:production-canonical",
    WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1:
        "cognitive-state-profile:controlled-evaluation-v1",
}
_KNOWN_PROFILES = frozenset(_PROFILE_TO_CSTATE_PROFILE)
_VALID_STATES = frozenset(
    {
        WORKING_ENVELOPE_CURRENT,
        WORKING_ENVELOPE_SUPERSEDED,
        WORKING_ENVELOPE_INVALIDATED,
    }
)


@dataclass(frozen=True)
class WorkingEnvelopeRecordV1:
    """Immutable owner-issued working-context binding record."""

    envelope_ref: str
    envelope_version_ref: str
    concern_ref: str
    cognitive_grant_ref: str
    cognitive_state_version_ref: str
    admission_basis_refs: Tuple[str, ...]
    applicable_constraint_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    profile_ref: str
    state: str
    owner_ref: str = WORKING_ENVELOPE_OWNER
    authority_ref: str = WORKING_ENVELOPE_AUTHORITY
    parent_version_ref: Optional[str] = None
    superseded_by_version_ref: Optional[str] = None
    invalidation_reason_ref: Optional[str] = None
    canonical: bool = True

    def __post_init__(self) -> None:
        scalar_fields = (
            self.envelope_ref,
            self.envelope_version_ref,
            self.concern_ref,
            self.cognitive_grant_ref,
            self.cognitive_state_version_ref,
            self.profile_ref,
            self.state,
            self.owner_ref,
            self.authority_ref,
        )
        if any(not isinstance(value, str) or not value.strip() for value in scalar_fields):
            raise ValueError("working_envelope_record_scalar_invalid")
        if self.state not in _VALID_STATES:
            raise ValueError("working_envelope_record_state_invalid")
        if not self.canonical:
            raise ValueError("working_envelope_record_must_be_canonical")
        for name in (
            "admission_basis_refs",
            "applicable_constraint_refs",
            "provenance_refs",
        ):
            value = getattr(self, name)
            if not isinstance(value, tuple) or any(
                not isinstance(item, str) or not item.strip() for item in value
            ):
                raise ValueError(f"working_envelope_record_{name}_invalid")
        for name in ("parent_version_ref", "superseded_by_version_ref", "invalidation_reason_ref"):
            value = getattr(self, name)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"working_envelope_record_{name}_invalid")


_LOCK = RLock()
_CURRENT: Dict[str, Dict[str, WorkingEnvelopeRecordV1]] = {}
_HISTORY: Dict[str, Dict[str, WorkingEnvelopeRecordV1]] = {}
_ENVELOPE_REF_TO_PROFILE: Dict[str, str] = {}
_ENVELOPE_VERSION_REF_TO_PROFILE: Dict[str, str] = {}
_NEXT_ENVELOPE_NUMBER: Dict[str, int] = {profile: 0 for profile in _KNOWN_PROFILES}
_NEXT_VERSION_NUMBER: Dict[Tuple[str, str], int] = {}


def resolve_working_envelope_profile_v1(profile_ref: Optional[str] = None) -> Optional[str]:
    """Resolve an owner-defined profile; omitted means production."""

    resolved = (
        WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL
        if profile_ref is None
        else profile_ref
    )
    if not isinstance(resolved, str) or not resolved.strip() or resolved not in _KNOWN_PROFILES:
        return None
    return resolved


def _register_working_envelope_namespace_v1(record: WorkingEnvelopeRecordV1) -> bool:
    """Register owner-issued identity locations; never establishes currentness."""

    existing_envelope = _ENVELOPE_REF_TO_PROFILE.get(record.envelope_ref)
    existing_version = _ENVELOPE_VERSION_REF_TO_PROFILE.get(record.envelope_version_ref)
    if existing_envelope is not None and existing_envelope != record.profile_ref:
        return False
    if existing_version is not None and existing_version != record.profile_ref:
        return False
    _ENVELOPE_REF_TO_PROFILE[record.envelope_ref] = record.profile_ref
    _ENVELOPE_VERSION_REF_TO_PROFILE[record.envelope_version_ref] = record.profile_ref
    return True


def _resolve_working_envelope_profile_for_ref_v1(
    canonical_ref: str,
    explicit_profile_ref: Optional[str],
    *,
    version_ref: bool = False,
) -> Optional[str]:
    """Resolve namespace from the owner index, with optional consistency check."""

    index = _ENVELOPE_VERSION_REF_TO_PROFILE if version_ref else _ENVELOPE_REF_TO_PROFILE
    resolved = index.get(canonical_ref)
    if resolved is None:
        return None
    if explicit_profile_ref is None:
        return resolved
    explicit = resolve_working_envelope_profile_v1(explicit_profile_ref)
    return resolved if explicit == resolved else None


def _unique_refs(*groups: Iterable[str]) -> Tuple[str, ...]:
    return tuple(
        dict.fromkeys(
            item
            for group in groups
            for item in group
            if isinstance(item, str) and item.strip()
        )
    )


def _resolve_prerequisites(
    *,
    concern_ref: str,
    cognitive_grant_ref: str,
    cognitive_state_version_ref: str,
    profile_ref: str,
) -> Optional[Tuple[CanonicalConcernRecordV1, CognitiveGrantRecordV1, CognitiveStateVersionRecordV1]]:
    concern = query_current_concern(concern_ref)
    if concern is None or concern.profile_ref != profile_ref:
        return None
    grant = query_current_cognitive_grant(
        cognitive_grant_ref,
        concern_ref=concern.concern_ref,
    )
    if (
        grant is None
        or grant.profile_ref != profile_ref
        or grant.concern_ref != concern.concern_ref
    ):
        return None
    cstate = query_valid_cognitive_state_version_v1(
        cognitive_state_version_ref,
    )
    if (
        cstate is None
        or cstate.profile_ref != _PROFILE_TO_CSTATE_PROFILE[profile_ref]
    ):
        return None
    return concern, grant, cstate


def _candidate_refs(
    candidate: AWorkingEnvelopeCandidateV1,
) -> Optional[Tuple[str, str, str]]:
    if not isinstance(candidate, AWorkingEnvelopeCandidateV1):
        return None
    if candidate.candidate_only is not True:
        return None
    values = (
        candidate.concern_ref,
        candidate.authority_grant_ref,
        candidate.source_cognitive_state_version_ref,
    )
    if any(not isinstance(value, str) or not value.strip() for value in values):
        return None
    return values


def _issue_record(
    *,
    candidate: AWorkingEnvelopeCandidateV1,
    profile_ref: str,
    prerequisites: Tuple[CanonicalConcernRecordV1, CognitiveGrantRecordV1, CognitiveStateVersionRecordV1],
    envelope_ref: Optional[str] = None,
    parent_version_ref: Optional[str] = None,
) -> WorkingEnvelopeRecordV1:
    concern, grant, cstate = prerequisites
    if envelope_ref is None:
        _NEXT_ENVELOPE_NUMBER[profile_ref] += 1
        profile_token = profile_ref.rsplit(":", 1)[-1]
        envelope_ref = f"working-envelope:{profile_token}:{_NEXT_ENVELOPE_NUMBER[profile_ref]}"
    version_key = (profile_ref, envelope_ref)
    version_number = _NEXT_VERSION_NUMBER.get(version_key, 0) + 1
    _NEXT_VERSION_NUMBER[version_key] = version_number
    version_ref = f"{envelope_ref}:v{version_number}"
    return WorkingEnvelopeRecordV1(
        envelope_ref=envelope_ref,
        envelope_version_ref=version_ref,
        concern_ref=concern.concern_ref,
        cognitive_grant_ref=grant.grant_ref,
        cognitive_state_version_ref=cstate.version_ref,
        admission_basis_refs=(
            f"current-concern:{concern.concern_ref}:{concern.version_ref}",
            f"current-grant:{grant.grant_ref}:{grant.version_ref}",
            f"valid-cognitive-state:{cstate.version_ref}",
            "grant-concern-compatibility",
        ),
        applicable_constraint_refs=(WORKING_ENVELOPE_CONSTRAINT_PROFILE,),
        provenance_refs=_unique_refs(
            (f"owner:{WORKING_ENVELOPE_OWNER}", f"profile:{profile_ref}"),
            (f"candidate-work:{candidate.work_ref}",),
            candidate.provenance_refs,
            concern.provenance_refs,
            grant.provenance_refs,
            cstate.provenance_refs,
        ),
        profile_ref=profile_ref,
        state=WORKING_ENVELOPE_CURRENT,
        parent_version_ref=parent_version_ref,
    )


def _store_current(record: WorkingEnvelopeRecordV1) -> None:
    _CURRENT.setdefault(record.profile_ref, {})[record.envelope_ref] = record
    _HISTORY.setdefault(record.profile_ref, {})[record.envelope_version_ref] = record


def admit_working_envelope_v1(
    candidate: AWorkingEnvelopeCandidateV1,
    *,
    profile_ref: Optional[str] = None,
) -> Optional[WorkingEnvelopeRecordV1]:
    """Admit a candidate only after all three prerequisite owner queries pass."""

    resolved = resolve_working_envelope_profile_v1(profile_ref)
    refs = _candidate_refs(candidate)
    if resolved is None or refs is None:
        return None
    prerequisites = _resolve_prerequisites(
        concern_ref=refs[0],
        cognitive_grant_ref=refs[1],
        cognitive_state_version_ref=refs[2],
        profile_ref=resolved,
    )
    if prerequisites is None:
        return None
    with _LOCK:
        record = _issue_record(
            candidate=candidate,
            profile_ref=resolved,
            prerequisites=prerequisites,
        )
        if not _register_working_envelope_namespace_v1(record):
            return None
        _store_current(record)
        return record


def query_current_working_envelope_v1(
    envelope_ref: str,
    *,
    profile_ref: Optional[str] = None,
) -> Optional[WorkingEnvelopeRecordV1]:
    """Return a current Envelope only while its owner prerequisites remain valid."""

    if not isinstance(envelope_ref, str) or not envelope_ref.strip():
        return None
    resolved = _resolve_working_envelope_profile_for_ref_v1(envelope_ref, profile_ref)
    if resolved is None:
        return None
    with _LOCK:
        record = _CURRENT.get(resolved, {}).get(envelope_ref)
        if record is None or record.state != WORKING_ENVELOPE_CURRENT:
            return None
    prerequisites = _resolve_prerequisites(
        concern_ref=record.concern_ref,
        cognitive_grant_ref=record.cognitive_grant_ref,
        cognitive_state_version_ref=record.cognitive_state_version_ref,
        profile_ref=resolved,
    )
    return record if prerequisites is not None else None


def query_working_envelope_version_v1(
    envelope_version_ref: str,
    *,
    profile_ref: Optional[str] = None,
) -> Optional[WorkingEnvelopeRecordV1]:
    """Return an immutable historical Envelope version, regardless of state."""

    if not isinstance(envelope_version_ref, str) or not envelope_version_ref.strip():
        return None
    resolved = _resolve_working_envelope_profile_for_ref_v1(
        envelope_version_ref,
        profile_ref,
        version_ref=True,
    )
    if resolved is None:
        return None
    with _LOCK:
        return _HISTORY.get(resolved, {}).get(envelope_version_ref)


def refresh_working_envelope_v1(
    envelope_ref: str,
    candidate: AWorkingEnvelopeCandidateV1,
    *,
    profile_ref: Optional[str] = None,
) -> Optional[WorkingEnvelopeRecordV1]:
    """Issue a new current version after resolving a new binding set."""

    resolved = _resolve_working_envelope_profile_for_ref_v1(envelope_ref, profile_ref)
    refs = _candidate_refs(candidate)
    if resolved is None or refs is None:
        return None
    current = query_current_working_envelope_v1(envelope_ref, profile_ref=resolved)
    if current is None:
        return None
    prerequisites = _resolve_prerequisites(
        concern_ref=refs[0],
        cognitive_grant_ref=refs[1],
        cognitive_state_version_ref=refs[2],
        profile_ref=resolved,
    )
    if prerequisites is None:
        return None
    with _LOCK:
        refreshed = _issue_record(
            candidate=candidate,
            profile_ref=resolved,
            prerequisites=prerequisites,
            envelope_ref=current.envelope_ref,
            parent_version_ref=current.envelope_version_ref,
        )
        if not _register_working_envelope_namespace_v1(refreshed):
            return None
        superseded = replace(
            current,
            state=WORKING_ENVELOPE_SUPERSEDED,
            superseded_by_version_ref=refreshed.envelope_version_ref,
        )
        _HISTORY[resolved][superseded.envelope_version_ref] = superseded
        _CURRENT[resolved][current.envelope_ref] = refreshed
        _HISTORY[resolved][refreshed.envelope_version_ref] = refreshed
        return refreshed


def invalidate_working_envelope_v1(
    envelope_ref: str,
    *,
    reason_ref: str,
    profile_ref: Optional[str] = None,
) -> Optional[WorkingEnvelopeRecordV1]:
    """Invalidate the current Envelope version; historical records remain."""

    resolved = _resolve_working_envelope_profile_for_ref_v1(envelope_ref, profile_ref)
    if resolved is None or not isinstance(reason_ref, str) or not reason_ref.strip():
        return None
    current = query_current_working_envelope_v1(envelope_ref, profile_ref=resolved)
    if current is None:
        return None
    invalidated = replace(
        current,
        state=WORKING_ENVELOPE_INVALIDATED,
        invalidation_reason_ref=reason_ref,
    )
    with _LOCK:
        _CURRENT[resolved].pop(envelope_ref, None)
        _HISTORY[resolved][invalidated.envelope_version_ref] = invalidated
    return invalidated


__all__ = [
    "WORKING_ENVELOPE_AUTHORITY",
    "WORKING_ENVELOPE_CONSTRAINT_PROFILE",
    "WORKING_ENVELOPE_CURRENT",
    "WORKING_ENVELOPE_INVALIDATED",
    "WORKING_ENVELOPE_OWNER",
    "WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1",
    "WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL",
    "WORKING_ENVELOPE_SUPERSEDED",
    "WorkingEnvelopeRecordV1",
    "admit_working_envelope_v1",
    "invalidate_working_envelope_v1",
    "query_current_working_envelope_v1",
    "query_working_envelope_version_v1",
    "refresh_working_envelope_v1",
    "resolve_working_envelope_profile_v1",
]
