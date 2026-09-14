"""Controlled multi-scenario consumer of the existing cognition chain."""

from __future__ import annotations

from typing import Any, Iterable, Tuple

from capabilities.midplatform.core.a_route_orchestration.a_route_information_need_formation_adapter_v1 import (
    ARouteInformationNeedFormationAdapterV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_engine_v1 import (
    ARouteRequiredCognitiveConditionFormationEngineV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_branch_governance_v1 import (
    govern_cognitive_branches,
)
from capabilities.midplatform.core.cognitive_flow.governed_cognitive_branch_formation_v1 import (
    form_governed_cognitive_branches,
)
from capabilities.midplatform.core.cognitive_flow.information_acquisition_strategy_candidate_formation_v1 import (
    form_information_acquisition_strategy_candidates,
)
from .cognitive_exploration_sandbox_adapter_v1 import (
    build_branch_request,
    build_current_world,
    build_governance_request,
    build_need_request,
    build_required_condition_request,
    build_strategy_request,
)
from .cognitive_exploration_sandbox_fixture_v1 import (
    build_sandbox_scenarios_v1,
)
from .cognitive_exploration_sandbox_types_v1 import (
    SandboxRoundV1,
    SandboxRunTraceV1,
    SandboxScenarioTraceV1,
    SandboxScenarioV1,
    SandboxSimulatedAcquisitionReturnV1,
)


PHASE_ID = "Phase-Controlled-Multi-Scenario-Cognitive-Exploration-Sandbox-v1-001"
SANDBOX_VERSION = "controlled-cognitive-exploration-sandbox-v1"


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))


def _run_round(
    scenario: SandboxScenarioV1,
    *,
    round_id: str,
    coverage_refs: Tuple[str, ...],
    context_ref: str,
) -> SandboxRoundV1:
    required_request = build_required_condition_request(
        scenario, coverage_refs, context_ref, round_id
    )
    required_result = ARouteRequiredCognitiveConditionFormationEngineV1().form(
        required_request
    )
    current_world = build_current_world(
        scenario, coverage_refs, context_ref, round_id
    )
    need_request = build_need_request(
        scenario, required_result, current_world, coverage_refs, context_ref
    )
    need_result = ARouteInformationNeedFormationAdapterV1().form(need_request)
    branch_request = build_branch_request(
        scenario, need_result, round_id, context_ref
    )
    branch_result = form_governed_cognitive_branches(branch_request)
    governance_request = build_governance_request(
        scenario,
        branch_result.branches,
        need_result,
        round_id,
        context_ref,
    )
    governance_result = govern_cognitive_branches(governance_request)
    strategy_request = build_strategy_request(
        scenario,
        branch_result.branches,
        governance_result.governance_decisions,
        need_result,
        round_id,
        context_ref,
    )
    strategy_result = form_information_acquisition_strategy_candidates(
        strategy_request
    )
    needs = (need_result.need,) if need_result.need else ()
    economy = {
        "required_condition_count": len(required_result.active_required_condition_refs),
        "information_need_count": len(needs),
        "branch_count": len(branch_result.branches),
        "admitted_branch_count": len(governance_result.admitted_branch_refs),
        "deferred_branch_count": len(governance_result.deferred_branch_refs),
        "rejected_branch_count": len(governance_result.rejected_branch_refs),
        "strategy_candidate_count": len(strategy_result.strategies),
        "active_strategy_candidate_count": len(strategy_result.strategies),
        "unresolved_gap_count": len(need_result.necessary_unknown_refs),
        "branches_per_need": len(branch_result.branches) / max(len(needs), 1),
        "strategies_per_admitted_branch": len(strategy_result.strategies)
        / max(len(governance_result.admitted_branch_refs), 1),
    }
    return SandboxRoundV1(
        round_id=round_id,
        problem=scenario.problem,
        required_conditions=scenario.required_conditions,
        required_condition_refs=tuple(required_result.active_required_condition_refs),
        current_cognitive_coverage_refs=tuple(
            need_result.current_cognitive_coverage_refs
        ),
        required_condition_candidates=tuple(required_result.candidates),
        information_needs=needs,
        branches=tuple(branch_result.branches),
        governance_results=(governance_result,),
        strategy_candidates=tuple(strategy_result.strategies),
        information_need_result=need_result,
        branch_formation_result=branch_result,
        governance_result=governance_result,
        strategy_formation_result=strategy_result,
        cognitive_economy=economy,
    )


def _identifiers(round_value: SandboxRoundV1, attribute: str) -> Tuple[str, ...]:
    values = getattr(round_value, attribute)
    if attribute == "information_needs":
        return tuple(item.need_id for item in values)
    if attribute == "branches":
        return tuple(item.branch_ref for item in values)
    return tuple(item.strategy_ref for item in values)


def _delta(
    before: SandboxRoundV1,
    after: SandboxRoundV1 | None,
) -> dict:
    if after is None:
        return {
            "needs_added": [],
            "needs_removed": [],
            "needs_retained": [],
            "branches_added": [],
            "branches_removed": [],
            "branches_retained": [],
            "strategies_added": [],
            "strategies_removed": [],
            "strategies_retained": [],
            "unresolved_gap_before": list(
                set(before.required_condition_refs)
                - set(before.current_cognitive_coverage_refs)
            ),
            "unresolved_gap_after": [],
        }

    def compare(attribute: str) -> dict:
        old = set(_identifiers(before, attribute))
        new = set(_identifiers(after, attribute))
        return {
            "added": sorted(new - old),
            "removed": sorted(old - new),
            "retained": sorted(old & new),
        }

    before_gap = set(before.required_condition_refs) - set(
        before.current_cognitive_coverage_refs
    )
    after_gap = set(after.required_condition_refs) - set(
        after.current_cognitive_coverage_refs
    )
    need_delta = compare("information_needs")
    branch_delta = compare("branches")
    strategy_delta = compare("strategy_candidates")
    return {
        "needs_added": need_delta["added"],
        "needs_removed": need_delta["removed"],
        "needs_retained": need_delta["retained"],
        "branches_added": branch_delta["added"],
        "branches_removed": branch_delta["removed"],
        "branches_retained": branch_delta["retained"],
        "strategies_added": strategy_delta["added"],
        "strategies_removed": strategy_delta["removed"],
        "strategies_retained": strategy_delta["retained"],
        "unresolved_gap_before": sorted(before_gap),
        "unresolved_gap_after": sorted(after_gap),
    }


def _simulated_return(
    scenario: SandboxScenarioV1,
    round_zero: SandboxRoundV1,
) -> SandboxSimulatedAcquisitionReturnV1 | None:
    if not scenario.simulated_return_enabled:
        return None
    strategy = round_zero.strategy_candidates[0] if round_zero.strategy_candidates else None
    branch = round_zero.branches[0] if round_zero.branches else None
    need = round_zero.information_needs[0] if round_zero.information_needs else None
    return SandboxSimulatedAcquisitionReturnV1(
        source_strategy_ref=strategy.strategy_ref if strategy else "sandbox:none",
        source_branch_ref=branch.branch_ref if branch else "sandbox:none",
        source_need_ref=need.need_id if need else "sandbox:none",
        synthetic_evidence_payload=scenario.simulated_return_payload,
        coverage_addition_refs=scenario.simulated_return_coverage_refs,
        provenance_refs=(
            "provenance:sandbox:simulated-acquisition-return:v1",
            f"provenance:scenario:{scenario.scenario_id}",
        ),
        round_id="ROUND_0_TO_ROUND_1",
    )


def _lineage_integrity(round_value: SandboxRoundV1) -> dict:
    need_refs = set(_identifiers(round_value, "information_needs"))
    branch_refs = set(_identifiers(round_value, "branches"))
    valid = True
    strategy_records = []
    for strategy in round_value.strategy_candidates:
        strategy_valid = (
            strategy.branch_ref in branch_refs
            and bool(strategy.acquisition_basis_refs)
            and set(strategy.information_need_refs).issubset(need_refs)
            and bool(strategy.provenance_refs)
            and strategy.candidate_only
        )
        valid = valid and strategy_valid
        strategy_records.append(
            {
                "strategy_ref": strategy.strategy_ref,
                "branch_ref": strategy.branch_ref,
                "information_need_refs": list(strategy.information_need_refs),
                "acquisition_basis_refs": list(strategy.acquisition_basis_refs),
                "valid": strategy_valid,
            }
        )
    return {"valid": valid, "strategies": strategy_records}


def _scenario_trace(scenario: SandboxScenarioV1) -> SandboxScenarioTraceV1:
    round_zero = _run_round(
        scenario,
        round_id="ROUND_0",
        coverage_refs=tuple(scenario.initial_situation.current_cognitive_coverage_refs),
        context_ref=scenario.initial_context,
    )
    simulated_return = _simulated_return(scenario, round_zero)
    round_one = None
    if simulated_return is not None:
        round_one = _run_round(
            scenario,
            round_id="ROUND_1",
            coverage_refs=_unique(
                (
                    *round_zero.current_cognitive_coverage_refs,
                    *simulated_return.coverage_addition_refs,
                )
            ),
            context_ref=scenario.round_1_context or scenario.initial_context,
        )
    rounds = (round_zero, round_one) if round_one else (round_zero,)
    economy = {
        "rounds": {
            round_value.round_id: round_value.cognitive_economy
            for round_value in rounds
        },
        "max_branch_count": max(round_value.cognitive_economy["branch_count"] for round_value in rounds),
        "max_strategy_candidate_count": max(
            round_value.cognitive_economy["strategy_candidate_count"]
            for round_value in rounds
        ),
    }
    delta = _delta(round_zero, round_one)
    observations = []
    if not round_zero.strategy_candidates and round_zero.information_needs:
        observations.append("active_need_has_no_strategy_candidate")
    if round_one is not None and len(round_one.branches) > len(round_zero.branches):
        observations.append("round_1_branch_count_increased")
    if round_one is not None and not delta["strategies_removed"] and round_one.strategy_candidates:
        observations.append("round_1_strategy_candidates_remain")
    if not observations:
        observations.append("no_additional_cognitive_logic_observation")
    return SandboxScenarioTraceV1(
        scenario_id=scenario.scenario_id,
        scenario_name=scenario.scenario_name,
        expected_behavior_class=scenario.expected_behavior_class,
        scenario_metadata={
            "problem": scenario.problem,
            "required_conditions": list(scenario.required_conditions),
            "initial_context": scenario.initial_context,
            "synthetic_inputs": list(scenario.synthetic_inputs),
            "simulated_return_enabled": scenario.simulated_return_enabled,
            "notes": scenario.notes,
        },
        round_0=round_zero,
        simulated_return=simulated_return,
        round_1=round_one,
        cognitive_delta=delta,
        cognitive_economy=economy,
        lineage_integrity={
            "round_0": _lineage_integrity(round_zero),
            "round_1": _lineage_integrity(round_one) if round_one else None,
        },
        boundary_observations=(
            "sandbox_only",
            "existing_cognition_owners_invoked_without_mutation",
            "simulated_return_is_not_canonical_observation",
        ),
        cognitive_logic_observations=tuple(observations),
    )


def run_controlled_cognitive_exploration_sandbox() -> SandboxRunTraceV1:
    scenario_traces = tuple(
        _scenario_trace(scenario) for scenario in build_sandbox_scenarios_v1()
    )
    aggregate = {
        "scenario_count": len(scenario_traces),
        "round_1_scenario_count": sum(
            trace.round_1 is not None for trace in scenario_traces
        ),
        "total_round_count": sum(
            1 + (trace.round_1 is not None) for trace in scenario_traces
        ),
        "max_branch_count": max(
            trace.cognitive_economy["max_branch_count"] for trace in scenario_traces
        ),
        "max_strategy_candidate_count": max(
            trace.cognitive_economy["max_strategy_candidate_count"]
            for trace in scenario_traces
        ),
    }
    guards = {
        "synthetic_only": True,
        "provider_execution": False,
        "model_execution": False,
        "ocr_execution": False,
        "capability_execution": False,
        "observation_demand_implementation": False,
        "strategy_coordination_implementation": False,
        "decision_execution": False,
        "task_execution": False,
        "action_execution": False,
        "canonical_cognition_mutation": False,
        "canonical_ownership_transfer": False,
        "autonomous_infinite_loop": False,
        "winner_selection": False,
        "strategy_fabrication": False,
        "hidden_fallback_strategy": False,
        "synthetic_evidence_as_real": False,
    }
    return SandboxRunTraceV1(
        phase_id=PHASE_ID,
        sandbox_version=SANDBOX_VERSION,
        synthetic_only=True,
        scenario_count=len(scenario_traces),
        scenarios=scenario_traces,
        aggregate_cognitive_economy=aggregate,
        negative_guard_summary=guards,
    )


__all__ = ["run_controlled_cognitive_exploration_sandbox"]
