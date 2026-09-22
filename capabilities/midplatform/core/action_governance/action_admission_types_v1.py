"""Canonical Action Admission records owned by Action Governance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from capabilities.midplatform.core.action_governance.action_core_types_v1 import (
    ActionCandidateV1,
)


ACTION_ADMISSION_CURRENT = "CURRENT"
ACTION_ADMISSION_SUPERSEDED = "SUPERSEDED"
ACTION_ADMISSION_REVOKED = "REVOKED"
ACTION_ADMISSION_CANCELLED = "CANCELLED"
ACTION_ADMISSION_STATES = frozenset(
    {
        ACTION_ADMISSION_CURRENT,
        ACTION_ADMISSION_SUPERSEDED,
        ACTION_ADMISSION_REVOKED,
        ACTION_ADMISSION_CANCELLED,
    }
)

ACTION_ADMISSION_OWNER = "Action Governance"
ACTION_ADMISSION_AUTHORITY = "ActionGovernance.ADMIT_ACTION"


@dataclass(frozen=True)
class CanonicalAdmittedActionRecordV1:
    """Immutable Action Governance admission fact.

    The complete Action candidate is retained as an immutable semantic
    snapshot.  It remains a candidate projection; this record's authority is
    only the Action Governance admission and lifecycle decision.
    """

    admitted_action_ref: str
    action_candidate_ref: str
    action_candidate: ActionCandidateV1
    working_envelope_ref: str
    working_envelope_version_ref: str
    selected_decision_ref: str
    selected_task_ref: str
    safety_prerequisite_ref: str
    safety_effect_class: str
    admission_basis_refs: Tuple[str, ...]
    applicable_policy_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    profile_ref: str
    lifecycle_status: str
    superseded_by_admitted_action_ref: Optional[str] = None
    supersession_reason_ref: Optional[str] = None
    revocation_ref: Optional[str] = None
    cancellation_ref: Optional[str] = None
    owner_ref: str = ACTION_ADMISSION_OWNER
    authority_ref: str = ACTION_ADMISSION_AUTHORITY
    candidate_only: bool = False
    canonical: bool = True

    def __post_init__(self) -> None:
        scalar_fields = (
            self.admitted_action_ref,
            self.action_candidate_ref,
            self.working_envelope_ref,
            self.working_envelope_version_ref,
            self.selected_decision_ref,
            self.selected_task_ref,
            self.safety_prerequisite_ref,
            self.safety_effect_class,
            self.profile_ref,
            self.lifecycle_status,
            self.owner_ref,
            self.authority_ref,
        )
        if any(not isinstance(value, str) or not value.strip() for value in scalar_fields):
            raise ValueError("admitted_action_record_scalar_invalid")
        if not isinstance(self.action_candidate, ActionCandidateV1):
            raise TypeError("admitted_action_record_candidate_invalid")
        if self.action_candidate.action_candidate_id != self.action_candidate_ref:
            raise ValueError("admitted_action_candidate_ref_mismatch")
        if self.lifecycle_status not in ACTION_ADMISSION_STATES:
            raise ValueError("admitted_action_record_lifecycle_invalid")
        if self.candidate_only is not False or self.canonical is not True:
            raise ValueError("admitted_action_record_authority_flags_invalid")
        for name in (
            "admission_basis_refs",
            "applicable_policy_refs",
            "provenance_refs",
        ):
            value = getattr(self, name)
            if not isinstance(value, tuple) or any(
                not isinstance(item, str) or not item.strip() for item in value
            ):
                raise ValueError(f"admitted_action_record_{name}_invalid")
        for name in (
            "superseded_by_admitted_action_ref",
            "supersession_reason_ref",
            "revocation_ref",
            "cancellation_ref",
        ):
            value = getattr(self, name)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"admitted_action_record_{name}_invalid")


__all__ = [
    "ACTION_ADMISSION_AUTHORITY",
    "ACTION_ADMISSION_CANCELLED",
    "ACTION_ADMISSION_CURRENT",
    "ACTION_ADMISSION_OWNER",
    "ACTION_ADMISSION_REVOKED",
    "ACTION_ADMISSION_STATES",
    "ACTION_ADMISSION_SUPERSEDED",
    "CanonicalAdmittedActionRecordV1",
]
