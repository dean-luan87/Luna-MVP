"""Brain-owned Concern admission and currentness.

The existing Brain request integration remains candidate-only.  This module is
the owner boundary that issues immutable Concern records and keeps the
process-local current index private.  Callers can request admission and supply
evidence/policy references, but cannot select a canonical Concern identity or
declare its state.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import count
from threading import RLock
from typing import Dict, Iterable, Optional, Tuple


BRAIN_PRODUCTION_PROFILE_REF = "brain-profile:production"
BRAIN_CONTROLLED_PROFILE_REF = "brain-profile:controlled-evaluation"
_KNOWN_PROFILE_REFS = frozenset(
    {BRAIN_PRODUCTION_PROFILE_REF, BRAIN_CONTROLLED_PROFILE_REF}
)

CONCERN_CURRENT = "CURRENT"
CONCERN_CLOSED = "CLOSED"
CONCERN_SUPERSEDED = "SUPERSEDED"
_CONCERN_STATES = frozenset(
    {CONCERN_CURRENT, CONCERN_CLOSED, CONCERN_SUPERSEDED}
)


@dataclass(frozen=True)
class CanonicalConcernRecordV1:
    """Immutable Brain-issued Concern record.

    ``state`` is written only by Brain transition functions.  A historical
    record is not accepted as a current authority merely because it is typed
    or still held by a caller.
    """

    concern_ref: str
    profile_ref: str
    request_ref: str
    goal_ref: str
    intent_ref: str
    scope_ref: str
    version_ref: str
    state: str
    basis_refs: Tuple[str, ...]
    policy_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    supersedes_ref: Optional[str] = None
    closure_ref: Optional[str] = None
    owner_ref: str = "Brain Governance"
    authority_ref: str = "Brain.ADMIT_CONCERN"


_LOCK = RLock()
_ISSUANCE_COUNTER = count(1)
_CURRENT: Dict[str, Dict[str, CanonicalConcernRecordV1]] = {}
_HISTORY: Dict[str, Dict[str, Tuple[CanonicalConcernRecordV1, ...]]] = {}
_CONCERN_REF_TO_PROFILE: Dict[str, str] = {}


def resolve_brain_governance_profile_v1(profile_ref: Optional[str] = None) -> Optional[str]:
    """Resolve an owner-defined Brain profile; unknown values fail closed."""

    resolved = BRAIN_PRODUCTION_PROFILE_REF if profile_ref is None else profile_ref
    return resolved if resolved in _KNOWN_PROFILE_REFS else None


def _refs(values: Iterable[str]) -> Tuple[str, ...]:
    if isinstance(values, str):
        values = (values,)
    return tuple(dict.fromkeys(value for value in values if isinstance(value, str) and value))


def _valid_input(
    *,
    profile_ref: Optional[str],
    request_ref: str,
    goal_ref: str,
    intent_ref: str,
    scope_ref: str,
    basis_refs: Tuple[str, ...],
    policy_refs: Tuple[str, ...],
) -> Optional[str]:
    resolved = resolve_brain_governance_profile_v1(profile_ref)
    if resolved is None:
        return None
    if not all(isinstance(value, str) and value for value in (request_ref, goal_ref, intent_ref, scope_ref)):
        return None
    if not basis_refs or not policy_refs:
        return None
    return resolved


def _append_history(profile_ref: str, record: CanonicalConcernRecordV1) -> None:
    history = _HISTORY.setdefault(profile_ref, {})
    history[record.concern_ref] = history.get(record.concern_ref, ()) + (record,)


def _register_concern_namespace_v1(record: CanonicalConcernRecordV1) -> bool:
    """Register owner-issued identity location; never establishes currentness."""

    existing = _CONCERN_REF_TO_PROFILE.get(record.concern_ref)
    if existing is not None:
        return existing == record.profile_ref
    _CONCERN_REF_TO_PROFILE[record.concern_ref] = record.profile_ref
    return True


def _resolve_concern_profile_v1(
    concern_ref: str,
    explicit_profile_ref: Optional[str],
) -> Optional[str]:
    """Resolve namespace from the owner index, with optional consistency check."""

    resolved = _CONCERN_REF_TO_PROFILE.get(concern_ref)
    if resolved is None:
        return None
    if explicit_profile_ref is None:
        return resolved
    explicit = resolve_brain_governance_profile_v1(explicit_profile_ref)
    return resolved if explicit == resolved else None


def _new_concern(
    *,
    profile_ref: str,
    request_ref: str,
    goal_ref: str,
    intent_ref: str,
    scope_ref: str,
    basis_refs: Tuple[str, ...],
    policy_refs: Tuple[str, ...],
    supersedes_ref: Optional[str] = None,
) -> CanonicalConcernRecordV1:
    serial = next(_ISSUANCE_COUNTER)
    concern_ref = f"brain:concern:{serial}"
    version_ref = f"{concern_ref}:v1"
    return CanonicalConcernRecordV1(
        concern_ref=concern_ref,
        profile_ref=profile_ref,
        request_ref=request_ref,
        goal_ref=goal_ref,
        intent_ref=intent_ref,
        scope_ref=scope_ref,
        version_ref=version_ref,
        state=CONCERN_CURRENT,
        basis_refs=basis_refs,
        policy_refs=policy_refs,
        provenance_refs=(
            f"owner:{profile_ref}:Brain Governance",
            f"request:{request_ref}",
            *basis_refs,
        ),
        supersedes_ref=supersedes_ref,
    )


def admit_concern(
    *,
    request_ref: str,
    goal_ref: str,
    intent_ref: str,
    scope_ref: str,
    basis_refs: Iterable[str],
    policy_refs: Iterable[str],
    profile_ref: Optional[str] = None,
) -> Optional[CanonicalConcernRecordV1]:
    """Admit a new Concern through the Brain owner boundary.

    No ``concern_ref`` or positive state is accepted from the caller.  The
    returned identity is issued by this owner and registered in its private
    current index only after the basis is present.
    """

    normalized_basis = _refs(basis_refs)
    normalized_policy = _refs(policy_refs)
    resolved = _valid_input(
        profile_ref=profile_ref,
        request_ref=request_ref,
        goal_ref=goal_ref,
        intent_ref=intent_ref,
        scope_ref=scope_ref,
        basis_refs=normalized_basis,
        policy_refs=normalized_policy,
    )
    if resolved is None:
        return None
    with _LOCK:
        record = _new_concern(
            profile_ref=resolved,
            request_ref=request_ref,
            goal_ref=goal_ref,
            intent_ref=intent_ref,
            scope_ref=scope_ref,
            basis_refs=normalized_basis,
            policy_refs=normalized_policy,
        )
        if not _register_concern_namespace_v1(record):
            return None
        _CURRENT.setdefault(resolved, {})[record.concern_ref] = record
        _append_history(resolved, record)
        return record


def query_current_concern(
    concern_ref: str,
    *,
    profile_ref: Optional[str] = None,
) -> Optional[CanonicalConcernRecordV1]:
    """Return the current Brain-owned Concern or ``None`` fail-closed."""

    if not isinstance(concern_ref, str) or not concern_ref:
        return None
    resolved = _resolve_concern_profile_v1(concern_ref, profile_ref)
    if resolved is None:
        return None
    with _LOCK:
        record = _CURRENT.get(resolved, {}).get(concern_ref)
        return record if record is not None and record.state == CONCERN_CURRENT else None


def close_concern(
    concern_ref: str,
    *,
    closure_ref: str,
    profile_ref: Optional[str] = None,
) -> Optional[CanonicalConcernRecordV1]:
    """Close a current Concern; historical state remains queryable by owner only."""

    resolved = _resolve_concern_profile_v1(concern_ref, profile_ref)
    if resolved is None or not closure_ref:
        return None
    with _LOCK:
        current = query_current_concern(concern_ref, profile_ref=resolved)
        if current is None:
            return None
        closed = replace(
            current,
            state=CONCERN_CLOSED,
            version_ref=f"{concern_ref}:closed",
            closure_ref=closure_ref,
        )
        _CURRENT[resolved].pop(concern_ref, None)
        _append_history(resolved, closed)
        return closed


def supersede_concern(
    concern_ref: str,
    *,
    request_ref: str,
    goal_ref: str,
    intent_ref: str,
    scope_ref: str,
    basis_refs: Iterable[str],
    policy_refs: Iterable[str],
    profile_ref: Optional[str] = None,
) -> Optional[CanonicalConcernRecordV1]:
    """Supersede one current Concern and issue a new current Concern."""

    normalized_basis = _refs(basis_refs)
    normalized_policy = _refs(policy_refs)
    owner_profile = _resolve_concern_profile_v1(concern_ref, profile_ref)
    if owner_profile is None:
        return None
    resolved = _valid_input(
        profile_ref=owner_profile,
        request_ref=request_ref,
        goal_ref=goal_ref,
        intent_ref=intent_ref,
        scope_ref=scope_ref,
        basis_refs=normalized_basis,
        policy_refs=normalized_policy,
    )
    if resolved is None:
        return None
    with _LOCK:
        current = query_current_concern(concern_ref, profile_ref=resolved)
        if current is None:
            return None
        superseded = replace(
            current,
            state=CONCERN_SUPERSEDED,
            version_ref=f"{concern_ref}:superseded",
            closure_ref=f"supersession:{concern_ref}",
        )
        _CURRENT[resolved].pop(concern_ref, None)
        _append_history(resolved, superseded)
        replacement = _new_concern(
            profile_ref=resolved,
            request_ref=request_ref,
            goal_ref=goal_ref,
            intent_ref=intent_ref,
            scope_ref=scope_ref,
            basis_refs=normalized_basis,
            policy_refs=normalized_policy,
            supersedes_ref=concern_ref,
        )
        if not _register_concern_namespace_v1(replacement):
            return None
        _CURRENT[resolved][replacement.concern_ref] = replacement
        _append_history(resolved, replacement)
        return replacement


__all__ = [
    "BRAIN_CONTROLLED_PROFILE_REF",
    "BRAIN_PRODUCTION_PROFILE_REF",
    "CONCERN_CLOSED",
    "CONCERN_CURRENT",
    "CONCERN_SUPERSEDED",
    "CanonicalConcernRecordV1",
    "admit_concern",
    "close_concern",
    "query_current_concern",
    "resolve_brain_governance_profile_v1",
    "supersede_concern",
]
