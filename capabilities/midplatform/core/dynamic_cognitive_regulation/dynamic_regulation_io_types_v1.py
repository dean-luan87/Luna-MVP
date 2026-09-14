"""Input and output envelopes for controlled Dynamic Cognitive Regulation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from capabilities.midplatform.core.dynamic_cognitive_regulation.cognitive_parameter_bounds_types_v1 import (
    CognitiveParameterBoundsV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.cognitive_parameter_genome_types_v1 import (
    CognitiveParameterGenomeCandidateV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.cognitive_parameter_types_v1 import (
    CognitiveParameterCandidateV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_core_types_v1 import (
    NegativeGuardStatusV1,
    RegulationPolicyRefV1,
    SourceRefV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_regulation_candidate_types_v1 import (
    DynamicRegulationCandidateV1,
    RegulationRevisionCandidateV1,
    RegulationRevocationCandidateV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_regulation_handoff_types_v1 import (
    DynamicRegulationHandoffCandidateV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_regulation_trace_types_v1 import (
    DynamicRegulationProvenanceV1,
    DynamicRegulationTraceV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.self_regulation_state_types_v1 import (
    SelfRegulationStateCandidateV1,
)


@dataclass(frozen=True)
class CognitiveStateVectorInputCandidateV1:
    state_vector_id: str
    attention_distribution_refs: Tuple[str, ...]
    hypothesis_state_refs: Tuple[str, ...]
    uncertainty_level_candidate: str
    conflict_level_candidate: str
    world_stability_candidate: str
    intent_pressure_candidate: str
    resource_pressure_candidate: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    stale: bool = False
    candidate_only: bool = True
    parameter_store: bool = False
    model_weight: bool = False
    long_term_memory: bool = False
    learning_result: bool = False


@dataclass(frozen=True)
class DynamicCognitiveRegulationInputV1:
    scenario_id: str
    cognitive_state_vector_candidate: CognitiveStateVectorInputCandidateV1
    context_refs: Tuple[SourceRefV1, ...]
    pcn_refs: Tuple[SourceRefV1, ...]
    intent_refs: Tuple[SourceRefV1, ...]
    hypothesis_refs: Tuple[SourceRefV1, ...]
    emotion_refs: Tuple[SourceRefV1, ...]
    resource_refs: Tuple[SourceRefV1, ...]
    learning_update_refs: Tuple[SourceRefV1, ...]
    policy_refs: Tuple[RegulationPolicyRefV1, ...]
    parameter_candidates: Tuple[CognitiveParameterCandidateV1, ...]
    parameter_bounds: Tuple[CognitiveParameterBoundsV1, ...]
    genome_candidate: Optional[CognitiveParameterGenomeCandidateV1] = None
    prior_regulation_candidate_ref: Optional[str] = None
    revision_requested: bool = False
    revocation_requested: bool = False
    source_revoked: bool = False
    synthetic_only: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class DynamicCognitiveRegulationOutputV1:
    scenario_id: str
    regulation_candidate: DynamicRegulationCandidateV1
    state_candidate: SelfRegulationStateCandidateV1
    handoff_candidate: DynamicRegulationHandoffCandidateV1
    trace: DynamicRegulationTraceV1
    provenance: DynamicRegulationProvenanceV1
    negative_guard_status: NegativeGuardStatusV1
    genome_candidate: Optional[CognitiveParameterGenomeCandidateV1] = None
    revision_candidate: Optional[RegulationRevisionCandidateV1] = None
    revocation_candidate: Optional[RegulationRevocationCandidateV1] = None
    issues: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    synthetic_only: bool = True
    runtime_executed: bool = False
    source_mutation_executed: bool = False
