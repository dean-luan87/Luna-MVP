"""Brain-owned cognitive Grant issuance and currentness."""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import count
from threading import RLock
from typing import Dict, Iterable, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_registry_v1 import (
    ROLE_A,
    ROLE_B,
    ROLE_LOOP,
    capability_boundary,
)

from .concern_governance_v1 import (
    BRAIN_CONTROLLED_PROFILE_REF,
    BRAIN_PRODUCTION_PROFILE_REF,
    CanonicalConcernRecordV1,
    query_current_concern,
    resolve_brain_governance_profile_v1,
)


COGNITIVE_GRANT_ISSUED = "ISSUED"
COGNITIVE_GRANT_REVOKED = "REVOKED"
COGNITIVE_GRANT_EXPIRED = "EXPIRED"
_ISSUABLE_RECEIVER_ROLES = frozenset({ROLE_A, ROLE_B, ROLE_LOOP})


@dataclass(frozen=True)
class CognitiveGrantRecordV1:
    """Immutable Brain-issued cognitive authority record."""

    grant_ref: str
    profile_ref: str
    concern_ref: str
    concern_version_ref: str
    receiver_ref: str
    receiver_role: str
    granted_authority_refs: Tuple[str, ...]
    work_ref: str
    scope_ref: str
    expiry_ref: str
    basis_refs: Tuple[str, ...]
    policy_refs: Tuple[str, ...]
    version_ref: str
    state: str
    provenance_refs: Tuple[str, ...]
    revocation_ref: Optional[str] = None


_LOCK = RLock()
_ISSUANCE_COUNTER = count(1)
_CURRENT: Dict[str, Dict[str, CognitiveGrantRecordV1]] = {}
_HISTORY: Dict[str, Dict[str, Tuple[CognitiveGrantRecordV1, ...]]] = {}
_GRANT_REF_TO_PROFILE: Dict[str, str] = {}


def _refs(values: Iterable[str]) -> Tuple[str, ...]:
    if isinstance(values, str):
        values = (values,)
    return tuple(dict.fromkeys(value for value in values if isinstance(value, str) and value))


def _append_history(profile_ref: str, record: CognitiveGrantRecordV1) -> None:
    history = _HISTORY.setdefault(profile_ref, {})
    history[record.grant_ref] = history.get(record.grant_ref, ()) + (record,)


def _register_grant_namespace_v1(record: CognitiveGrantRecordV1) -> bool:
    """Register owner-issued identity location; never establishes currentness."""

    existing = _GRANT_REF_TO_PROFILE.get(record.grant_ref)
    if existing is not None:
        return existing == record.profile_ref
    _GRANT_REF_TO_PROFILE[record.grant_ref] = record.profile_ref
    return True


def _resolve_grant_profile_v1(
    grant_ref: str,
    explicit_profile_ref: Optional[str],
) -> Optional[str]:
    """Resolve namespace from the owner index, with optional consistency check."""

    resolved = _GRANT_REF_TO_PROFILE.get(grant_ref)
    if resolved is None:
        return None
    if explicit_profile_ref is None:
        return resolved
    explicit = resolve_brain_governance_profile_v1(explicit_profile_ref)
    return resolved if explicit == resolved else None


def _valid_grant_input(
    *,
    profile_ref: Optional[str],
    receiver_ref: str,
    receiver_role: str,
    granted_authority_refs: Tuple[str, ...],
    work_ref: str,
    scope_ref: str,
    expiry_ref: str,
    basis_refs: Tuple[str, ...],
    policy_refs: Tuple[str, ...],
) -> Optional[str]:
    resolved = resolve_brain_governance_profile_v1(profile_ref)
    if resolved is None:
        return None
    if receiver_role not in _ISSUABLE_RECEIVER_ROLES:
        return None
    if not all(isinstance(value, str) and value for value in (receiver_ref, work_ref, scope_ref, expiry_ref)):
        return None
    if not granted_authority_refs or not set(granted_authority_refs).issubset(set(capability_boundary(receiver_role))):
        return None
    if not basis_refs or not policy_refs:
        return None
    return resolved


def _new_grant(
    *,
    profile_ref: str,
    concern: CanonicalConcernRecordV1,
    receiver_ref: str,
    receiver_role: str,
    granted_authority_refs: Tuple[str, ...],
    work_ref: str,
    scope_ref: str,
    expiry_ref: str,
    basis_refs: Tuple[str, ...],
    policy_refs: Tuple[str, ...],
) -> CognitiveGrantRecordV1:
    serial = next(_ISSUANCE_COUNTER)
    grant_ref = f"brain:grant:{serial}"
    return CognitiveGrantRecordV1(
        grant_ref=grant_ref,
        profile_ref=profile_ref,
        concern_ref=concern.concern_ref,
        concern_version_ref=concern.version_ref,
        receiver_ref=receiver_ref,
        receiver_role=receiver_role,
        granted_authority_refs=granted_authority_refs,
        work_ref=work_ref,
        scope_ref=scope_ref,
        expiry_ref=expiry_ref,
        basis_refs=basis_refs,
        policy_refs=policy_refs,
        version_ref=f"{grant_ref}:v1",
        state=COGNITIVE_GRANT_ISSUED,
        provenance_refs=(
            f"owner:{profile_ref}:Brain Governance",
            f"concern:{concern.concern_ref}:{concern.version_ref}",
            *basis_refs,
        ),
    )


def issue_cognitive_grant(
    *,
    concern_ref: str,
    receiver_ref: str,
    receiver_role: str,
    granted_authority_refs: Iterable[str],
    work_ref: str,
    scope_ref: str,
    expiry_ref: str,
    basis_refs: Iterable[str],
    policy_refs: Iterable[str],
    profile_ref: Optional[str] = None,
) -> Optional[CognitiveGrantRecordV1]:
    """Issue a Brain-owned Grant only for a current Brain Concern."""

    authorities = _refs(granted_authority_refs)
    basis = _refs(basis_refs)
    policy = _refs(policy_refs)
    resolved = _valid_grant_input(
        profile_ref=profile_ref,
        receiver_ref=receiver_ref,
        receiver_role=receiver_role,
        granted_authority_refs=authorities,
        work_ref=work_ref,
        scope_ref=scope_ref,
        expiry_ref=expiry_ref,
        basis_refs=basis,
        policy_refs=policy,
    )
    if resolved is None or not isinstance(concern_ref, str) or not concern_ref:
        return None
    with _LOCK:
        concern = query_current_concern(concern_ref, profile_ref=resolved)
        if concern is None:
            return None
        record = _new_grant(
            profile_ref=resolved,
            concern=concern,
            receiver_ref=receiver_ref,
            receiver_role=receiver_role,
            granted_authority_refs=authorities,
            work_ref=work_ref,
            scope_ref=scope_ref,
            expiry_ref=expiry_ref,
            basis_refs=basis,
            policy_refs=policy,
        )
        if not _register_grant_namespace_v1(record):
            return None
        _CURRENT.setdefault(resolved, {})[record.grant_ref] = record
        _append_history(resolved, record)
        return record


def query_current_cognitive_grant(
    grant_ref: str,
    *,
    profile_ref: Optional[str] = None,
    concern_ref: Optional[str] = None,
    receiver_ref: Optional[str] = None,
    receiver_role: Optional[str] = None,
    work_ref: Optional[str] = None,
    scope_ref: Optional[str] = None,
    authority_ref: Optional[str] = None,
) -> Optional[CognitiveGrantRecordV1]:
    """Return a current, scope-matching Grant or ``None`` fail-closed."""

    if not isinstance(grant_ref, str) or not grant_ref:
        return None
    resolved = _resolve_grant_profile_v1(grant_ref, profile_ref)
    if resolved is None:
        return None
    with _LOCK:
        record = _CURRENT.get(resolved, {}).get(grant_ref)
        if record is None or record.state != COGNITIVE_GRANT_ISSUED:
            return None
        if query_current_concern(record.concern_ref, profile_ref=resolved) is None:
            return None
        if concern_ref is not None and record.concern_ref != concern_ref:
            return None
        if receiver_ref is not None and record.receiver_ref != receiver_ref:
            return None
        if receiver_role is not None and record.receiver_role != receiver_role:
            return None
        if work_ref is not None and record.work_ref != work_ref:
            return None
        if scope_ref is not None and record.scope_ref != scope_ref:
            return None
        if authority_ref is not None and authority_ref not in record.granted_authority_refs:
            return None
        return record


def _transition_grant(
    grant_ref: str,
    *,
    state: str,
    reason_ref: str,
    profile_ref: Optional[str],
) -> Optional[CognitiveGrantRecordV1]:
    resolved = _resolve_grant_profile_v1(grant_ref, profile_ref)
    if resolved is None or not reason_ref:
        return None
    with _LOCK:
        current = query_current_cognitive_grant(grant_ref, profile_ref=resolved)
        if current is None:
            return None
        transitioned = replace(
            current,
            state=state,
            version_ref=f"{grant_ref}:{state.lower()}",
            revocation_ref=reason_ref,
        )
        _CURRENT[resolved].pop(grant_ref, None)
        _append_history(resolved, transitioned)
        return transitioned


def revoke_cognitive_grant(
    grant_ref: str,
    *,
    revocation_ref: str,
    profile_ref: Optional[str] = None,
) -> Optional[CognitiveGrantRecordV1]:
    return _transition_grant(
        grant_ref,
        state=COGNITIVE_GRANT_REVOKED,
        reason_ref=revocation_ref,
        profile_ref=profile_ref,
    )


def expire_cognitive_grant(
    grant_ref: str,
    *,
    expiry_ref: str,
    profile_ref: Optional[str] = None,
) -> Optional[CognitiveGrantRecordV1]:
    return _transition_grant(
        grant_ref,
        state=COGNITIVE_GRANT_EXPIRED,
        reason_ref=expiry_ref,
        profile_ref=profile_ref,
    )


__all__ = [
    "BRAIN_CONTROLLED_PROFILE_REF",
    "BRAIN_PRODUCTION_PROFILE_REF",
    "COGNITIVE_GRANT_EXPIRED",
    "COGNITIVE_GRANT_ISSUED",
    "COGNITIVE_GRANT_REVOKED",
    "CognitiveGrantRecordV1",
    "expire_cognitive_grant",
    "issue_cognitive_grant",
    "query_current_cognitive_grant",
    "revoke_cognitive_grant",
]
