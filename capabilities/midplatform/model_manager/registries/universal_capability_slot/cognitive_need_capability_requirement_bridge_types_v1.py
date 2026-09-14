"""Candidate-only bridge types from cognitive need to capability requirement."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from .universal_capability_slot_types_v1 import CapabilityRequirementV1


@dataclass(frozen=True)
class CognitiveNeedCandidateV1:
    """A bounded information/evidence need formed by cognitive governance."""

    need_id: str
    source_intent_ref: Optional[str]
    source_context_ref: Optional[str]
    source_field_ref: Optional[str]
    source_hypothesis_ref: Optional[str]
    source_attention_ref: Optional[str]
    problem_description: str
    missing_information_class: str
    required_evidence_class: str
    urgency: str
    safety_relevance: str
    materialization_status: str = "CURRENT_MINIMUM_NECESSARY_NEED"
    candidate_only: bool = True
    trace_ref: Optional[str] = None
    state_version_ref: Optional[str] = None


@dataclass(frozen=True)
class CapabilityRequirementFormationCandidateV1:
    """A controlled Need -> existing CapabilityRequirement transformation."""

    formation_id: str
    source_need_ref: str
    requirement_ref: str
    requirement: CapabilityRequirementV1
    selected_problem_class: str
    requested_operation: str
    input_contract_ref: str
    output_contract_ref: str
    required_authority: str
    requirement_minimized: bool
    trace_ref: Optional[str]
    source_state_version_ref: Optional[str] = None
    candidate_only: bool = True
    technical_implementation_selected: bool = False
    model_selected: bool = False
    provider_selected: bool = False
    scope_assumed: bool = False
    authority_escalated: bool = False


@dataclass(frozen=True)
class CognitiveNeedReplanningCandidateV1:
    """Candidate-only cognitive response to bounded capability rejection."""

    replan_id: str
    source_need_ref: str
    source_requirement_ref: str
    trigger_result: str
    reason: str
    refined_need_ref: Optional[str]
    decomposed_need_refs: Tuple[str, ...]
    alternative_requirement_refs: Tuple[str, ...]
    information_insufficient: bool
    capability_gap_ref: Optional[str]
    candidate_only: bool = True
    scope_bypassed: bool = False
    authority_escalated: bool = False
    fallback_hallucination: bool = False
    automatic_acquisition: bool = False
    source_state_version_ref: Optional[str] = None
    prior_requirement_disposition: str = "REPLANNING_REQUIRED"


@dataclass(frozen=True)
class CognitiveNextStepAssessmentV1:
    """Minimal provisional next-step and sufficiency continuation boundary."""

    assessment_id: str
    source_cognitive_state_ref: str
    source_plan_ref: Optional[str]
    current_need_ref: str
    selected_next_need_ref: Optional[str]
    remaining_candidate_refs: Tuple[str, ...]
    selected_as_current_minimum_step: bool
    remaining_candidates_binding: bool
    state_version_ref: str
    sufficiency_status: str
    continuation_disposition: str
    trace_ref: Optional[str]
    candidate_only: bool = True
    stop_sufficient_not_failure: bool = True
    unexecuted_after_sufficiency_not_failure: bool = True
