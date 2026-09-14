"""Contracts for the controlled multi-scenario cognitive exploration sandbox."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from capabilities.cognitive_flow.current_cognitive_context.context_inputs_v1 import (
    GoalContextV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_types_v1 import (
    CurrentCognitiveSituationV1,
    GovernedObjectiveConditionRuleV1,
)
from capabilities.midplatform.core.cognitive_flow.information_acquisition_strategy_candidate_formation_v1 import (
    GovernedAcquisitionBasisV1,
)


@dataclass(frozen=True)
class SandboxStrategyBasisSpecV1:
    """Fixture declaration for one explicit governed acquisition basis."""

    basis_ref: str
    condition_ref: str
    acquisition_mode_candidate: str = "UNKNOWN"
    expected_information_contribution_refs: Tuple[str, ...] = field(
        default_factory=tuple
    )
    required_capability_class_refs: Tuple[str, ...] = field(default_factory=tuple)
    opportunity_refs: Tuple[str, ...] = field(default_factory=tuple)
    dependency_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class SandboxSimulatedAcquisitionReturnV1:
    """Sandbox-only evidence injection; never a canonical observation result."""

    source_strategy_ref: str
    source_branch_ref: str
    source_need_ref: str
    synthetic_evidence_payload: Tuple[Tuple[str, str], ...]
    coverage_addition_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    round_id: str
    sandbox_only: bool = True
    synthetic: bool = True
    runtime_acquisition: bool = False
    provider_executed: bool = False
    capability_executed: bool = False


@dataclass(frozen=True)
class SandboxScenarioV1:
    """A synthetic scenario plus governed inputs for existing cognition owners."""

    scenario_id: str
    scenario_name: str
    problem: str
    required_conditions: Tuple[str, ...]
    initial_context: str
    synthetic_inputs: Tuple[str, ...]
    expected_behavior_class: str
    simulated_return_enabled: bool
    simulated_return_payload: Tuple[Tuple[str, str], ...]
    notes: str
    goal_context: GoalContextV1
    condition_rules: Tuple[GovernedObjectiveConditionRuleV1, ...]
    initial_situation: CurrentCognitiveSituationV1
    simulated_return_coverage_refs: Tuple[str, ...] = field(default_factory=tuple)
    strategy_basis_specs: Tuple[SandboxStrategyBasisSpecV1, ...] = field(
        default_factory=tuple
    )
    deferred_condition_refs: Tuple[str, ...] = field(default_factory=tuple)
    rejected_condition_refs: Tuple[str, ...] = field(default_factory=tuple)
    governed_conflict_refs: Tuple[str, ...] = field(default_factory=tuple)
    round_1_context: str = ""


@dataclass(frozen=True)
class SandboxRoundV1:
    round_id: str
    problem: str
    required_conditions: Tuple[str, ...]
    required_condition_refs: Tuple[str, ...]
    current_cognitive_coverage_refs: Tuple[str, ...]
    required_condition_candidates: Tuple[object, ...]
    information_needs: Tuple[object, ...]
    branches: Tuple[object, ...]
    governance_results: Tuple[object, ...]
    strategy_candidates: Tuple[object, ...]
    information_need_result: object
    branch_formation_result: object
    governance_result: object
    strategy_formation_result: object
    cognitive_economy: dict


@dataclass(frozen=True)
class SandboxScenarioTraceV1:
    scenario_id: str
    scenario_name: str
    expected_behavior_class: str
    scenario_metadata: dict
    round_0: SandboxRoundV1
    simulated_return: SandboxSimulatedAcquisitionReturnV1 | None
    round_1: SandboxRoundV1 | None
    cognitive_delta: dict
    cognitive_economy: dict
    lineage_integrity: dict
    boundary_observations: Tuple[str, ...]
    cognitive_logic_observations: Tuple[str, ...]


@dataclass(frozen=True)
class SandboxRunTraceV1:
    phase_id: str
    sandbox_version: str
    synthetic_only: bool
    scenario_count: int
    scenarios: Tuple[SandboxScenarioTraceV1, ...]
    aggregate_cognitive_economy: dict
    negative_guard_summary: dict
    status: str = "IMPLEMENTATION_READY_FOR_USER_EXECUTION"


__all__ = [
    "SandboxStrategyBasisSpecV1",
    "SandboxSimulatedAcquisitionReturnV1",
    "SandboxScenarioV1",
    "SandboxRoundV1",
    "SandboxScenarioTraceV1",
    "SandboxRunTraceV1",
]
