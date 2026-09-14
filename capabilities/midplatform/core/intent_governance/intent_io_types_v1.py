"""Input and output envelope types for Intent Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from capabilities.midplatform.core.intent_governance.intent_core_types_v1 import (
    IntentCandidateV1,
    PotentialIntentCandidateV1,
    SourceRefV1,
)
from capabilities.midplatform.core.intent_governance.intent_handoff_types_v1 import (
    IntentToCausalHandoffCandidateV1,
)
from capabilities.midplatform.core.intent_governance.intent_interaction_types_v1 import (
    IntentInteractionCandidateV1,
)
from capabilities.midplatform.core.intent_governance.intent_trace_types_v1 import (
    IntentTraceCandidateV1,
)


@dataclass(frozen=True)
class IntentGovernanceInputV1:
    scenario_id: str
    context_refs: Tuple[SourceRefV1, ...]
    pcn_refs: Tuple[SourceRefV1, ...]
    source_refs: Tuple[SourceRefV1, ...]
    self_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    field_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    role_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    relationship_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    memory_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    experience_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    emotion_refs: Tuple[SourceRefV1, ...] = field(default_factory=tuple)
    unknowns: Tuple[str, ...] = field(default_factory=tuple)
    synthetic_only: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class IntentGovernanceOutputV1:
    scenario_id: str
    potential_intents: Tuple[PotentialIntentCandidateV1, ...]
    intent_candidates: Tuple[IntentCandidateV1, ...]
    interaction_candidates: Tuple[IntentInteractionCandidateV1, ...]
    trace_candidate: IntentTraceCandidateV1
    handoff_candidate: IntentToCausalHandoffCandidateV1
    candidate_only: bool = True
    runtime_executed: bool = False
    source_mutation_executed: bool = False
