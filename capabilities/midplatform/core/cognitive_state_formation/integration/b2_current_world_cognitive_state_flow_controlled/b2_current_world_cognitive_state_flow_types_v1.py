"""B2 integration-only result types.

These types are an adapter envelope around existing Cognitive State Formation,
Cognitive Flow, and Active Observation Control contracts.  They do not create
a new semantic owner.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_flow_io_types_v1 import (
    CognitiveFlowOutputV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
    CognitiveStateFormationOutputV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_active_observation_control_types_v1 import (
    ObservationControlDecisionV1,
)


@dataclass(frozen=True)
class B2ObservationNeedBridgeCandidateV1:
    """Existing FPO control decision carried as a B2 candidate handoff."""

    owner: str
    control_decision: ObservationControlDecisionV1
    source_current_world_ref: str
    candidate_only: bool = True
    provider_invocation: bool = False


@dataclass(frozen=True)
class B2CurrentWorldCognitiveFlowResultV1:
    case_id: str
    mode: str
    source_current_world: CurrentWorldCandidateV1
    state_request: CognitiveStateFormationInputV1
    state_output: CognitiveStateFormationOutputV1
    flow_output: CognitiveFlowOutputV1
    observation_need_bridge: B2ObservationNeedBridgeCandidateV1 | None
    preserved_uncertainty_refs: Tuple[str, ...]
    preserved_conflict_refs: Tuple[str, ...]
    preserved_temporal_refs: Tuple[str, ...]
    provenance_chain: Tuple[str, ...]
    current_world_read_only: bool = True
    world_truth_promoted: bool = False
    hypothesis_as_fact: bool = False
    pcn_mutation: bool = False
    intent_mutation: bool = False
    decision_mutation: bool = False
    task_mutation: bool = False
    action_execution: bool = False
    provider_invocation: bool = False
    semantic_compression: bool = False
    dynamic_cognitive_function_execution: bool = False
    candidate_only: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
