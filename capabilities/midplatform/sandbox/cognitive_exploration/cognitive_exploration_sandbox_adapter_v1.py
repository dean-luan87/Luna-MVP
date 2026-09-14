"""Adapters from sandbox fixtures to existing canonical cognition contracts."""

from __future__ import annotations

from dataclasses import replace
from typing import Iterable, Tuple

from capabilities.midplatform.core.a_route_orchestration.a_route_information_need_formation_adapter_v1 import (
    ARouteInformationNeedFormationRequestV1,
    ARouteInformationNeedFormationResultV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_types_v1 import (
    ARouteRequiredCognitiveConditionFormationRequestV1,
    CurrentCognitiveSituationV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_branch_governance_v1 import (
    CognitiveBranchGovernanceInputV1,
)
from capabilities.midplatform.core.cognitive_flow.governed_cognitive_branch_formation_v1 import (
    GovernedCognitiveBranchFormationInputV1,
)
from capabilities.midplatform.core.cognitive_flow.information_acquisition_strategy_candidate_formation_v1 import (
    GovernedAcquisitionBasisV1,
    InformationAcquisitionStrategyFormationInputV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)

from .cognitive_exploration_sandbox_types_v1 import (
    SandboxScenarioV1,
    SandboxStrategyBasisSpecV1,
)


SANDBOX_INTENT_REF = "intent:sandbox:controlled-exploration:v1"
SANDBOX_FIELD_REF = "field:sandbox:controlled-exploration:v1"


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


def round_world_id(scenario: SandboxScenarioV1) -> str:
    return f"world:sandbox:{scenario.scenario_id}"


def gap_ref(scenario: SandboxScenarioV1, condition_ref: str) -> str:
    return f"gap:sandbox:{scenario.scenario_id}:{condition_ref}"


def build_situation(
    scenario: SandboxScenarioV1,
    coverage_refs: Iterable[str],
    round_context_ref: str,
) -> CurrentCognitiveSituationV1:
    return replace(
        scenario.initial_situation,
        current_cognitive_coverage_refs=tuple(coverage_refs),
        current_world_refs=(round_world_id(scenario),),
        context_condition_refs=(),
        external_information_refs=scenario.initial_situation.external_information_refs,
    )


def build_current_world(
    scenario: SandboxScenarioV1,
    coverage_refs: Iterable[str],
    round_context_ref: str,
    round_id: str,
) -> CurrentWorldCandidateV1:
    world_id = round_world_id(scenario)
    return CurrentWorldCandidateV1(
        current_world_id=world_id,
        attention_refs=(),
        active_hypothesis_refs=(),
        alternative_hypothesis_refs=(),
        context_refs=(round_context_ref,),
        field_state_refs=(SANDBOX_FIELD_REF,),
        pcn_refs=(),
        intent_refs=(SANDBOX_INTENT_REF,),
        observation_refs=(),
        uncertainty_refs=tuple(gap_ref(scenario, ref) for ref in scenario.required_conditions),
        conflict_refs=scenario.governed_conflict_refs,
        temporal_refs=(f"round:{round_id}",),
        source_versions={"sandbox": "controlled-v1"},
        world_state_kind_candidate="PARTIAL",
        world_stability_candidate="CONTROLLED",
        trace_ref=f"trace:sandbox:world:{scenario.scenario_id}:{round_id}",
        provenance_refs=(
            "provenance:controlled-cognitive-exploration-sandbox:v1",
            f"provenance:scenario:{scenario.scenario_id}",
        ),
    )


def build_required_condition_request(
    scenario: SandboxScenarioV1,
    coverage_refs: Iterable[str],
    round_context_ref: str,
    round_id: str,
) -> ARouteRequiredCognitiveConditionFormationRequestV1:
    situation = build_situation(scenario, coverage_refs, round_context_ref)
    return ARouteRequiredCognitiveConditionFormationRequestV1(
        goal_context=scenario.goal_context,
        governed_condition_rules=scenario.condition_rules,
        current_situation=situation,
        intent_ref=SANDBOX_INTENT_REF,
        concern_ref=f"concern:sandbox:{scenario.scenario_id}:v1",
        context_ref=round_context_ref,
        field_ref=SANDBOX_FIELD_REF,
        role_refs=(f"role:sandbox:{scenario.scenario_id}:v1",),
        formation_trace_ref=(
            f"trace:sandbox:required-conditions:{scenario.scenario_id}:{round_id}"
        ),
    )


def build_need_request(
    scenario: SandboxScenarioV1,
    need_result: object,
    current_world: CurrentWorldCandidateV1,
    coverage_refs: Iterable[str],
    round_context_ref: str,
) -> ARouteInformationNeedFormationRequestV1:
    required_refs = tuple(getattr(need_result, "active_required_condition_refs", ()))
    satisfied_refs = tuple(getattr(need_result, "satisfied_condition_refs", ()))
    effective_coverage_refs = _unique((*coverage_refs, *satisfied_refs))
    return ARouteInformationNeedFormationRequestV1(
        goal_context=scenario.goal_context,
        current_world=current_world,
        current_cognitive_coverage_refs=effective_coverage_refs,
        intent_ref=SANDBOX_INTENT_REF,
        concern_ref=f"concern:sandbox:{scenario.scenario_id}:v1",
        task_ref=None,
        context_ref=round_context_ref,
        field_ref=SANDBOX_FIELD_REF,
        role_refs=(f"role:sandbox:{scenario.scenario_id}:v1",),
        governed_role_condition_refs=(),
        governed_objective_condition_refs=required_refs,
        hypothesis_ref=None,
        attention_ref=None,
        formation_trace_ref=(
            f"trace:sandbox:information-need:{scenario.scenario_id}"
        ),
    )


def build_branch_request(
    scenario: SandboxScenarioV1,
    need_result: ARouteInformationNeedFormationResultV1,
    round_id: str,
    round_context_ref: str,
) -> GovernedCognitiveBranchFormationInputV1:
    need = need_result.need
    need_refs = (need.need_id,) if need else ()
    unresolved = tuple(
        (gap_ref(scenario, condition_ref), need_refs)
        for condition_ref in need_result.necessary_unknown_refs
    )
    return GovernedCognitiveBranchFormationInputV1(
        formation_ref=f"sandbox:{scenario.scenario_id}:branch:{round_id}",
        parent_cognitive_problem_ref=scenario.problem,
        source_state_ref=round_world_id(scenario),
        unresolved_gap_need_refs=unresolved,
        evidence_refs=(),
        conflict_refs=scenario.governed_conflict_refs,
        context_refs=(round_context_ref,),
        trace_ref=f"trace:sandbox:branch:{scenario.scenario_id}:{round_id}",
        provenance_refs=(
            "provenance:controlled-cognitive-exploration-sandbox:v1",
        ),
    )


def build_governance_request(
    scenario: SandboxScenarioV1,
    branches: Tuple[object, ...],
    need_result: ARouteInformationNeedFormationResultV1,
    round_id: str,
    round_context_ref: str,
) -> CognitiveBranchGovernanceInputV1:
    need = need_result.need
    rejected_gaps = {
        gap_ref(scenario, ref) for ref in scenario.rejected_condition_refs
    }
    deferred_gaps = {
        gap_ref(scenario, ref) for ref in scenario.deferred_condition_refs
    }
    current_gap_refs = tuple(
        branch.basis_ref for branch in branches if branch.basis_ref not in rejected_gaps
    )
    deferred_branch_refs = tuple(
        branch.branch_ref for branch in branches if branch.basis_ref in deferred_gaps
    )
    current_need_refs = (need.need_id,) if need else ()
    return CognitiveBranchGovernanceInputV1(
        governance_ref=f"sandbox:{scenario.scenario_id}:governance:{round_id}",
        parent_cognitive_problem_ref=scenario.problem,
        source_state_ref=round_world_id(scenario),
        branch_candidates=branches,
        current_information_need_refs=current_need_refs,
        current_information_gap_refs=current_gap_refs,
        current_conflict_refs=scenario.governed_conflict_refs,
        currently_satisfied_need_refs=(
            current_need_refs if deferred_branch_refs else ()
        ),
        currently_not_needed_branch_refs=deferred_branch_refs,
        context_refs=(round_context_ref,),
        trace_ref=f"trace:sandbox:governance:{scenario.scenario_id}:{round_id}",
        provenance_refs=(
            "provenance:controlled-cognitive-exploration-sandbox:v1",
        ),
    )


def build_strategy_bases(
    scenario: SandboxScenarioV1,
    branches: Tuple[object, ...],
    need_result: ARouteInformationNeedFormationResultV1,
) -> Tuple[GovernedAcquisitionBasisV1, ...]:
    need = need_result.need
    if need is None:
        return ()
    branch_by_condition = {branch.basis_ref: branch for branch in branches}
    bases = []
    for spec in scenario.strategy_basis_specs:
        branch = branch_by_condition.get(gap_ref(scenario, spec.condition_ref))
        if branch is None:
            continue
        bases.append(
            GovernedAcquisitionBasisV1(
                basis_ref=spec.basis_ref,
                branch_ref=branch.branch_ref,
                information_need_refs=(need.need_id,),
                information_gap_refs=(branch.basis_ref,),
                acquisition_mode_candidate=spec.acquisition_mode_candidate,
                expected_information_contribution_refs=spec.expected_information_contribution_refs,
                required_capability_class_refs=spec.required_capability_class_refs,
                opportunity_refs=spec.opportunity_refs,
                dependency_refs=spec.dependency_refs,
                provenance_refs=spec.provenance_refs,
            )
        )
    return tuple(bases)


def build_strategy_request(
    scenario: SandboxScenarioV1,
    branches: Tuple[object, ...],
    governance_decisions: Tuple[object, ...],
    need_result: ARouteInformationNeedFormationResultV1,
    round_id: str,
    round_context_ref: str,
) -> InformationAcquisitionStrategyFormationInputV1:
    return InformationAcquisitionStrategyFormationInputV1(
        formation_ref=f"sandbox:{scenario.scenario_id}:strategy",
        parent_cognitive_problem_ref=scenario.problem,
        source_state_ref=round_world_id(scenario),
        branch_candidates=branches,
        governance_decisions=governance_decisions,
        need_candidates=(need_result.need,) if need_result.need else (),
        governed_acquisition_bases=build_strategy_bases(
            scenario, branches, need_result
        ),
        current_cognitive_state_ref=round_world_id(scenario),
        context_refs=(round_context_ref,),
        trace_ref=f"trace:sandbox:strategy:{scenario.scenario_id}:{round_id}",
        provenance_refs=(
            "provenance:controlled-cognitive-exploration-sandbox:v1",
        ),
    )


__all__ = [
    "SANDBOX_FIELD_REF",
    "SANDBOX_INTENT_REF",
    "build_branch_request",
    "build_current_world",
    "build_governance_request",
    "build_need_request",
    "build_required_condition_request",
    "build_situation",
    "build_strategy_request",
    "gap_ref",
    "round_world_id",
]
