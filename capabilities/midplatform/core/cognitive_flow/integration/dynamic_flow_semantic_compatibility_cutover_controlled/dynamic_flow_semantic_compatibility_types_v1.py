"""Candidate-only compatibility records for the Dynamic Flow authority seam."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled.a_owned_semantic_decision_types_v1 import (
    ASemanticDecisionBundleV1,
)


@dataclass(frozen=True)
class DynamicFlowCompatibilityOutputV1:
    compatibility_ref: str
    source_flow_ref: str
    source_state_version_refs: Tuple[str, ...]
    computed_need_ref: str | None
    computed_sufficiency_status: str
    computed_reconsideration_refs: Tuple[str, ...]
    computed_next_step_disposition: str
    evidence_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    source_owner_ref: str = "COGNITIVE_FLOW_GOVERNANCE"
    compatibility_only: bool = True
    semantic_authority: bool = False
    candidate_only: bool = True
    synthetic_only: bool = True
    legacy_fields_retained: bool = True


@dataclass(frozen=True)
class DynamicFlowAInterpretationV1:
    compatibility_output: DynamicFlowCompatibilityOutputV1
    a_decisions: ASemanticDecisionBundleV1
    compatibility_source_ref: str
    decision_owner_ref: str = "A_REASONING_ROLE"
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class CompatibilityScenarioResultV1:
    scenario_id: str
    scenario_family: str
    compatibility_output: DynamicFlowCompatibilityOutputV1
    interpretation: DynamicFlowAInterpretationV1
    migrated_caller: bool
    direct_semantic_consumption_blocked: bool
    expected_disposition: str
    passed: bool
    failure_refs: Tuple[str, ...] = ()
    candidate_only: bool = True
    synthetic_only: bool = True


__all__ = [
    "CompatibilityScenarioResultV1",
    "DynamicFlowAInterpretationV1",
    "DynamicFlowCompatibilityOutputV1",
]
