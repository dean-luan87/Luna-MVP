"""Input and output types for Decision Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from capabilities.midplatform.core.decision_governance.decision_core_types_v1 import (
    DecisionCandidateV1,
    DecisionOptionCandidateV1,
    DecisionSelectionCandidateV1,
    SourceRefV1,
)
from capabilities.midplatform.core.decision_governance.decision_handoff_types_v1 import (
    DecisionToActionTaskHandoffCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_state_types_v1 import (
    DecisionStateTransitionCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_trace_types_v1 import (
    DecisionTraceCandidateV1,
)


@dataclass(frozen=True)
class DecisionGovernanceInputV1:
    scenario_id: str
    intent_refs: Tuple[SourceRefV1, ...]
    causal_refs: Tuple[SourceRefV1, ...]
    context_refs: Tuple[SourceRefV1, ...]
    field_refs: Tuple[SourceRefV1, ...]
    role_refs: Tuple[SourceRefV1, ...]
    permission_refs: Tuple[SourceRefV1, ...]
    safety_refs: Tuple[SourceRefV1, ...]
    resource_refs: Tuple[SourceRefV1, ...]
    constraint_refs: Tuple[SourceRefV1, ...]
    evidence_refs: Tuple[SourceRefV1, ...]
    options: Tuple[DecisionOptionCandidateV1, ...]
    intent_preferred_option_ids: Tuple[str, ...] = field(default_factory=tuple)
    causal_uncertainty_level: str = "LOW"
    competing_causal_hypotheses: bool = False
    resource_pressure_level: str = "NORMAL"
    human_confirmation_available: bool = False
    synthetic_only: bool = True
    candidate_only: bool = True
    working_envelope_ref: Optional[str] = None
    working_envelope_version_ref: Optional[str] = None


@dataclass(frozen=True)
class DecisionGovernanceOutputV1:
    scenario_id: str
    state: str
    outcome_kind: str
    decision_candidates: Tuple[DecisionCandidateV1, ...]
    selection_candidate: DecisionSelectionCandidateV1
    transitions: Tuple[DecisionStateTransitionCandidateV1, ...]
    trace_candidate: DecisionTraceCandidateV1
    handoff_candidate: DecisionToActionTaskHandoffCandidateV1
    candidate_only: bool = True
    decision_output: bool = False
    action_output: bool = False
    task_output: bool = False
    runtime_executed: bool = False
    database_write_executed: bool = False
    source_mutation_executed: bool = False
    fabricated_confirmation: bool = False
    working_envelope_ref: Optional[str] = None
    working_envelope_version_ref: Optional[str] = None
