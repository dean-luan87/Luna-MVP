"""Reference-only bridge types for the cognitive-result Decision handoff."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


COGNITION_OWNER = "Cognitive State Formation Governance"
DECISION_OWNER = "Decision Governance"


@dataclass(frozen=True)
class CognitiveDecisionHandoffCandidateV1:
    """Candidate handoff consumed by Decision Governance.

    This is an integration envelope, not a Decision candidate and not a
    commitment.  All cognition references are read-only inputs to the
    existing Decision Governance contract.
    """

    handoff_ref: str
    case_id: str
    producer_owner_ref: str
    consumer_owner_ref: str
    goal_ref: str
    intent_ref: str
    concern_ref: str
    context_ref: str
    information_need_ref: str
    cognitive_loop_ref: str
    a_route_execution_ref: str
    current_world_ref: str
    hypothesis_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    sufficiency_ref: str
    stop_ref: str
    provenance_refs: Tuple[str, ...]
    execution_instance_ref: str
    candidate_only: bool = True
    decision_handoff_eligible: bool = True
    task_execution: bool = False
    action_execution: bool = False


@dataclass(frozen=True)
class DecisionHandoffAttemptV1:
    """Observable readiness result for one cognition cycle."""

    cycle_index: int
    status: str
    handoff_ref: str | None = None
    rejection_reason: str | None = None
    source_execution_ref: str | None = None
    sufficiency_status: str | None = None
    stop_ref: str | None = None
    candidate_only: bool = True


__all__ = [
    "COGNITION_OWNER",
    "DECISION_OWNER",
    "CognitiveDecisionHandoffCandidateV1",
    "DecisionHandoffAttemptV1",
]

