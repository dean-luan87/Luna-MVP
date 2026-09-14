"""Candidate-only cross-module envelopes for the real-input cognitive loop.

This is an integration envelope under the existing Cognitive Flow owner.  It
contains references to canonical B1, B2, Capability Registry, Capability
Experience, and B4 outputs; it is not a new Brain, Planner, Task, Capability,
or Outcome owner.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_types_v1 import (
    DynamicCognitiveLoopInputV1,
    DynamicCognitiveLoopOutputV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled.a_owned_semantic_decision_types_v1 import (
    ASemanticDecisionBundleV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.dynamic_flow_semantic_compatibility_cutover_controlled.dynamic_flow_semantic_compatibility_types_v1 import (
    DynamicFlowCompatibilityOutputV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.integration.b2_current_world_cognitive_state_flow_controlled.b2_current_world_cognitive_state_flow_types_v1 import (
    B2CurrentWorldCognitiveFlowResultV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_transition_types_v1 import (
    ReconsiderationCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_types_v1 import (
    CapabilityRequirementFormationCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_types_v1 import (
    CapabilityInvocationCandidateV1,
    CapabilityOutcomeAssessmentV1,
    CapabilityResolutionCandidateV1,
    CapabilityScopeAssessmentV1,
)


@dataclass(frozen=True)
class IntegratedCognitiveLoopInputV1:
    """All already-formed candidates entering one controlled integration case."""

    scenario_id: str
    input_mode: str
    source_current_world: CurrentWorldCandidateV1
    b2_result: B2CurrentWorldCognitiveFlowResultV1
    dynamic_request: DynamicCognitiveLoopInputV1
    requirement_formations: Tuple[CapabilityRequirementFormationCandidateV1, ...]
    scope_assessments: Tuple[CapabilityScopeAssessmentV1, ...]
    resolutions: Tuple[CapabilityResolutionCandidateV1, ...]
    invocations: Tuple[CapabilityInvocationCandidateV1, ...]
    capability_outcomes: Tuple[CapabilityOutcomeAssessmentV1, ...]
    b4_reconsiderations: Tuple[ReconsiderationCandidateV1, ...] = ()
    b4_reobserve_refs: Tuple[str, ...] = ()
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class IntegratedCognitiveLoopResultV1:
    """Reverse-traceable result of the cross-module candidate handoff."""

    scenario_id: str
    input_mode: str
    source_current_world_ref: str
    b2_state_world_ref: str
    b2_flow_cycle_ref: str
    dynamic_output: DynamicCognitiveLoopOutputV1
    requirement_formations: Tuple[CapabilityRequirementFormationCandidateV1, ...]
    scope_assessments: Tuple[CapabilityScopeAssessmentV1, ...]
    resolutions: Tuple[CapabilityResolutionCandidateV1, ...]
    invocations: Tuple[CapabilityInvocationCandidateV1, ...]
    capability_outcomes: Tuple[CapabilityOutcomeAssessmentV1, ...]
    requirement_dispositions: Tuple[Tuple[str, str], ...]
    b4_reconsideration_refs: Tuple[str, ...]
    b4_reobserve_refs: Tuple[str, ...]
    final_state_version_ref: str
    final_need_ref: Optional[str]
    final_disposition: str
    next_step_disposition: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    guards: Dict[str, bool] = field(default_factory=dict)
    candidate_only: bool = True
    synthetic_only: bool = True
    runtime_execution: bool = False
    provider_invocation: bool = False
    camera_activation: bool = False
    action_execution: bool = False
    learning_execution: bool = False
    memory_mutation: bool = False
    compatibility_output: Optional[DynamicFlowCompatibilityOutputV1] = None
    a_semantic_decisions: Optional[ASemanticDecisionBundleV1] = None
    dynamic_flow_semantic_consumption_migrated: bool = True


__all__ = ["IntegratedCognitiveLoopInputV1", "IntegratedCognitiveLoopResultV1"]
