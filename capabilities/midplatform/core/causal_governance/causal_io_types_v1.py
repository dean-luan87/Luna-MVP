"""Input and output types for Causal Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from capabilities.midplatform.core.causal_governance.causal_confounder_types_v1 import (
    ConfounderCandidateV1,
)
from capabilities.midplatform.core.causal_governance.causal_core_types_v1 import (
    CausalHypothesisCandidateV1,
    SourceRefV1,
)
from capabilities.midplatform.core.causal_governance.causal_counterfactual_types_v1 import (
    CounterfactualCandidateV1,
)
from capabilities.midplatform.core.causal_governance.causal_evidence_types_v1 import (
    CausalEvidenceRelationCandidateV1,
)
from capabilities.midplatform.core.causal_governance.causal_handoff_types_v1 import (
    CausalToDecisionHandoffCandidateV1,
)
from capabilities.midplatform.core.causal_governance.causal_state_types_v1 import (
    StateTransitionCandidateV1,
)
from capabilities.midplatform.core.causal_governance.causal_trace_types_v1 import (
    CausalTraceCandidateV1,
)


@dataclass(frozen=True)
class CausalGovernanceInputV1:
    scenario_id: str
    hypothesis_candidates: Tuple[str, ...]
    target_event_refs: Tuple[SourceRefV1, ...]
    cause_candidate_refs: Tuple[SourceRefV1, ...]
    supporting_evidence_refs: Tuple[SourceRefV1, ...]
    opposing_evidence_refs: Tuple[SourceRefV1, ...]
    confounder_refs: Tuple[SourceRefV1, ...]
    temporal_order_refs: Tuple[SourceRefV1, ...]
    context_refs: Tuple[SourceRefV1, ...]
    prior_refs: Tuple[SourceRefV1, ...]
    intent_refs: Tuple[SourceRefV1, ...]
    influence_refs: Tuple[SourceRefV1, ...]
    correlation_signal_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    unknowns: Tuple[str, ...] = field(default_factory=tuple)
    counterfactual_requested: bool = False
    synthetic_only: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class CausalGovernanceOutputV1:
    scenario_id: str
    hypothesis_candidates: Tuple[CausalHypothesisCandidateV1, ...]
    evidence_relations: Tuple[CausalEvidenceRelationCandidateV1, ...]
    confounder_candidates: Tuple[ConfounderCandidateV1, ...]
    counterfactual_candidates: Tuple[CounterfactualCandidateV1, ...]
    transitions: Tuple[StateTransitionCandidateV1, ...]
    trace_candidate: CausalTraceCandidateV1
    handoff_candidate: CausalToDecisionHandoffCandidateV1
    candidate_only: bool = True
    decision_output: bool = False
    action_output: bool = False
    task_output: bool = False
    runtime_executed: bool = False
    source_mutation_executed: bool = False
