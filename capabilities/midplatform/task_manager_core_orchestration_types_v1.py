# -*- coding: utf-8 -*-
"""Task Manager Core Orchestration types v1 — candidate/planning dataclasses only."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


class OrchestrationDecisionKind(str, Enum):
    PROCEED = "proceed"
    BLOCKER = "blocker"
    DEFER = "defer"
    REJECT = "reject"
    CLOSE = "close"


class LifecycleTransitionIntent(str, Enum):
    REVIEW = "review"
    HOLD = "hold"
    DEFER = "defer"
    CLOSE_CANDIDATE = "close_candidate"


@dataclass(frozen=True)
class OrchestrationInputCandidate:
    candidate_id: str
    source_module_ref: str
    boundary_registry_ref: str
    lifecycle_state_ref: str
    alignment_rule_ref: str
    governance_constraint_ref: str
    protocol_trace_ref: str
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class OrchestrationPlanCandidate:
    candidate_id: str
    input_candidate_ref: str
    plan_stage: str
    boundary_registry_ref: str
    lifecycle_state_ref: str
    alignment_rule_ref: str
    governance_constraint_ref: str
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class CandidateRouteCandidate:
    candidate_id: str
    plan_candidate_ref: str
    route_target_module_ref: str
    route_reason: str
    boundary_registry_ref: str
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    route_execution: bool = False
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class ModuleHandoffCandidate:
    candidate_id: str
    route_candidate_ref: str
    target_module_ref: str
    handoff_reason: str
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    handoff_execution: bool = False
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class LifecycleTransitionRequestCandidate:
    candidate_id: str
    lifecycle_state_ref: str
    transition_intent: str
    reason: str
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    promotion_execution: bool = False
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class AlignmentCheckRequestCandidate:
    candidate_id: str
    alignment_rule_ref: str
    check_scope: str
    boundary_registry_ref: str
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class GovernanceCheckRequestCandidate:
    candidate_id: str
    governance_constraint_ref: str
    check_scope: str
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class TraceabilityBundleCandidate:
    candidate_id: str
    protocol_trace_ref: str
    alignment_rule_ref: str
    source_refs: Tuple[str, ...]
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class BlockerOrDeferDecisionCandidate:
    candidate_id: str
    decision_kind: str
    decision_reason: str
    source_check_refs: Tuple[str, ...]
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class OrchestrationResultCandidate:
    candidate_id: str
    plan_candidate_ref: str
    route_candidate_ref: str
    handoff_candidate_ref: str
    traceability_bundle_ref: str
    decision_candidate_ref: str
    lifecycle_request_ref: Optional[str]
    alignment_request_ref: Optional[str]
    governance_request_ref: Optional[str]
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    skeleton_pass: bool
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


ORCHESTRATION_CANDIDATE_TYPES: Tuple[str, ...] = (
    "OrchestrationInputCandidate",
    "OrchestrationPlanCandidate",
    "CandidateRouteCandidate",
    "ModuleHandoffCandidate",
    "LifecycleTransitionRequestCandidate",
    "AlignmentCheckRequestCandidate",
    "GovernanceCheckRequestCandidate",
    "TraceabilityBundleCandidate",
    "BlockerOrDeferDecisionCandidate",
    "OrchestrationResultCandidate",
)

NON_EXECUTION_FLAG_DEFAULTS: Tuple[str, ...] = (
    "candidate_only",
    "side_effect_allowed",
    "real_execution",
    "runtime_required_now",
)
