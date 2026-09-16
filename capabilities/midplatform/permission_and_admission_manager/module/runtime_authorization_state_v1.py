"""Execution-preparation-scoped Runtime Authorization state.

This state is owned by the Permission / Admission Manager authorization
boundary.  Records and projections may describe an authorization, but only
the canonical authorization path can populate this in-process state.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Dict, Optional, Tuple


AUTHORIZATION_STATE_STATUSES = ("AUTHORIZED", "INVALIDATED")
AUTHORIZATION_STATE_KEY = Tuple[str, str]

@dataclass(frozen=True)
class RuntimeAuthorizationScopeV1:
    """Exact scope bound to one pre-execution authorization subject."""

    execution_instance_preparation_candidate_ref: str
    source_provider_binding_candidate_ref: str
    source_runtime_allocation_preparation_ref: str
    source_execution_instance_preparation_ref: str
    provider_candidate_ref: str
    capability_candidate_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    permission_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    protocol_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    constraint_refs: Tuple[str, ...]
    validity_scope: Tuple[str, ...]
    expiry_boundary_ref: str

    @classmethod
    def from_grant(cls, grant: object) -> "RuntimeAuthorizationScopeV1":
        return cls(
            execution_instance_preparation_candidate_ref=getattr(
                grant, "source_execution_instance_preparation_ref", ""
            ),
            source_provider_binding_candidate_ref=getattr(
                grant, "source_provider_binding_candidate_ref", ""
            ),
            source_runtime_allocation_preparation_ref=getattr(
                grant, "source_runtime_allocation_preparation_ref", ""
            ),
            source_execution_instance_preparation_ref=getattr(
                grant, "source_execution_instance_preparation_ref", ""
            ),
            provider_candidate_ref=getattr(grant, "provider_candidate_ref", ""),
            capability_candidate_ref=getattr(grant, "capability_candidate_ref", ""),
            parent_cognitive_problem_ref=getattr(
                grant, "parent_cognitive_problem_ref", ""
            ),
            source_state_ref=getattr(grant, "source_state_ref", ""),
            permission_refs=tuple(getattr(grant, "permission_refs", ())),
            safety_refs=tuple(getattr(grant, "safety_refs", ())),
            protocol_refs=tuple(getattr(grant, "protocol_refs", ())),
            governance_refs=tuple(getattr(grant, "governance_refs", ())),
            constraint_refs=tuple(getattr(grant, "constraint_refs", ())),
            validity_scope=tuple(getattr(grant, "validity_scope", ())),
            expiry_boundary_ref=getattr(grant, "expiry_boundary_ref", ""),
        )


@dataclass(frozen=True)
class RuntimeAuthorizationStateV1:
    """Descriptive state returned by a read-only state query."""

    authorization_ref: str
    subject_ref: str
    status: str
    scope: RuntimeAuthorizationScopeV1
    invalidation_reason: Optional[str] = None


class RuntimeAuthorizationStateStoreV1:
    """Owner-controlled in-process state; no public mutation API is exposed."""

    def __init__(self) -> None:
        self._states: Dict[AUTHORIZATION_STATE_KEY, RuntimeAuthorizationStateV1] = {}

    def __copy__(self) -> "RuntimeAuthorizationStateStoreV1":
        """Copying the state container never copies authority."""

        return type(self)()

    def __deepcopy__(self, memo: dict) -> "RuntimeAuthorizationStateStoreV1":
        """Deep-copying a runtime state container starts with no state."""

        copied = type(self)()
        memo[id(self)] = copied
        return copied

    def __getstate__(self) -> dict:
        """Serialization carries only a descriptive marker, never state."""

        return {"state_surface": "descriptive_only"}

    def __setstate__(self, _state: object) -> None:
        """Deserialization cannot restore owner-controlled authorization."""

        self._states = {}

    def _authorize(
        self,
        *,
        authorization_ref: str,
        scope: RuntimeAuthorizationScopeV1,
    ) -> Optional[RuntimeAuthorizationStateV1]:
        if not authorization_ref or not scope.execution_instance_preparation_candidate_ref:
            return None
        key = (scope.execution_instance_preparation_candidate_ref, authorization_ref)
        existing = self._states.get(key)
        if existing is not None:
            if existing.scope != scope or existing.status != "AUTHORIZED":
                return None
            return existing
        state = RuntimeAuthorizationStateV1(
            authorization_ref=authorization_ref,
            subject_ref=scope.execution_instance_preparation_candidate_ref,
            status="AUTHORIZED",
            scope=scope,
        )
        self._states[key] = state
        return state

    def _invalidate(
        self,
        *,
        authorization_ref: str,
        subject_ref: str,
        reason: str,
    ) -> Optional[RuntimeAuthorizationStateV1]:
        key = (subject_ref, authorization_ref)
        state = self._states.get(key)
        if state is None or state.status != "AUTHORIZED":
            return state
        invalidated = replace(
            state,
            status="INVALIDATED",
            invalidation_reason=reason,
        )
        self._states[key] = invalidated
        return invalidated

    def read_view(self) -> "RuntimeAuthorizationStateReadViewV1":
        return RuntimeAuthorizationStateReadViewV1(self)

    def query_active_authorization(
        self,
        *,
        authorization_ref: str,
        scope: RuntimeAuthorizationScopeV1,
    ) -> Optional[RuntimeAuthorizationStateV1]:
        key = (scope.execution_instance_preparation_candidate_ref, authorization_ref)
        state = self._states.get(key)
        if state is None or state.status != "AUTHORIZED":
            return None
        if state.scope != scope:
            return None
        return state


class RuntimeAuthorizationStateReadViewV1:
    """Read-only consumer surface over owner-controlled authorization state."""

    def __init__(self, store: RuntimeAuthorizationStateStoreV1) -> None:
        self._store = store

    def __copy__(self) -> "RuntimeAuthorizationStateReadViewV1":
        return type(self)(RuntimeAuthorizationStateStoreV1())

    def __deepcopy__(self, memo: dict) -> "RuntimeAuthorizationStateReadViewV1":
        copied = type(self)(RuntimeAuthorizationStateStoreV1())
        memo[id(self)] = copied
        return copied

    def __getstate__(self) -> dict:
        return {"state_surface": "descriptive_only"}

    def __setstate__(self, _state: object) -> None:
        self._store = RuntimeAuthorizationStateStoreV1()

    def query_active_authorization(
        self,
        *,
        authorization_ref: str,
        scope: RuntimeAuthorizationScopeV1,
    ) -> Optional[RuntimeAuthorizationStateV1]:
        return self._store.query_active_authorization(
            authorization_ref=authorization_ref,
            scope=scope,
        )


# This is the Permission / Admission Manager's owner-controlled state root.
# It is deliberately not part of any result or projection contract.  Callers
# may construct descriptive stores/views for tests or records, but the
# canonical query below never selects a caller-provided store.
_CANONICAL_RUNTIME_AUTHORIZATION_STATE_STORE = RuntimeAuthorizationStateStoreV1()


def _authorize_canonical_runtime_authorization(
    *,
    authorization_ref: str,
    scope: RuntimeAuthorizationScopeV1,
) -> Optional[RuntimeAuthorizationStateV1]:
    return _CANONICAL_RUNTIME_AUTHORIZATION_STATE_STORE._authorize(
        authorization_ref=authorization_ref,
        scope=scope,
    )


def _invalidate_canonical_runtime_authorization(
    *,
    authorization_ref: str,
    subject_ref: str,
    reason: str,
) -> Optional[RuntimeAuthorizationStateV1]:
    return _CANONICAL_RUNTIME_AUTHORIZATION_STATE_STORE._invalidate(
        authorization_ref=authorization_ref,
        subject_ref=subject_ref,
        reason=reason,
    )


def query_active_authorization_for_grant(
    grant: object,
) -> Optional[RuntimeAuthorizationStateV1]:
    """Resolve a Grant projection through the owner-controlled state root."""

    authorization_ref = getattr(grant, "authorization_ref", "")
    if not authorization_ref:
        return None
    return _CANONICAL_RUNTIME_AUTHORIZATION_STATE_STORE.query_active_authorization(
        authorization_ref=authorization_ref,
        scope=RuntimeAuthorizationScopeV1.from_grant(grant),
    )


__all__ = [
    "AUTHORIZATION_STATE_STATUSES",
    "AUTHORIZATION_STATE_KEY",
    "RuntimeAuthorizationScopeV1",
    "RuntimeAuthorizationStateV1",
    "RuntimeAuthorizationStateStoreV1",
    "RuntimeAuthorizationStateReadViewV1",
    "query_active_authorization_for_grant",
]
