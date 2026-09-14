"""Decision-to-Action/Task candidate handoff types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class DecisionToActionTaskHandoffCandidateV1:
    handoff_id: str
    producer_owner: str
    consumer_owners: Tuple[str, ...]
    handoff_kind: str
    decision_candidate_refs: Tuple[str, ...]
    selected_candidate_ref: Optional[str]
    option_refs: Tuple[str, ...]
    constraint_refs: Tuple[str, ...]
    permission_status_refs: Tuple[str, ...]
    safety_status_refs: Tuple[str, ...]
    uncertainty: Tuple[str, ...]
    provenance: Tuple[str, ...]
    confirmation_requirement: str
    execution_eligibility_candidate: bool
    candidate_only: bool = True
    decision_executed: bool = False
    action_triggered: bool = False
    task_created: bool = False
