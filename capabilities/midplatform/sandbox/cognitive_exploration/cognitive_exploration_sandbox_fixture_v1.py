"""Synthetic scenario catalog for the cognitive exploration sandbox."""

from __future__ import annotations

from typing import Iterable, Tuple

from capabilities.cognitive_flow.current_cognitive_context.context_inputs_v1 import (
    GoalContextV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_types_v1 import (
    CurrentCognitiveSituationV1,
    GovernedObjectiveConditionRuleV1,
)

from .cognitive_exploration_sandbox_types_v1 import (
    SandboxScenarioV1,
    SandboxStrategyBasisSpecV1,
)


FIELD_CONDITION = "condition:field:sandbox:controlled:v1"


def _rules(
    goal_ref: str,
    condition_refs: Iterable[str],
    alternative_basis_refs_by_condition: dict[str, Tuple[str, ...]] | None = None,
) -> Tuple[GovernedObjectiveConditionRuleV1, ...]:
    alternative_basis_refs_by_condition = alternative_basis_refs_by_condition or {}
    return tuple(
        GovernedObjectiveConditionRuleV1(
            rule_ref=f"rule:sandbox:{condition_ref}",
            condition_ref=condition_ref,
            objective_refs=(goal_ref,),
            activation_all_refs=(FIELD_CONDITION,),
            satisfaction_coverage_refs=(
                ()
                if alternative_basis_refs_by_condition.get(condition_ref)
                else (condition_ref,)
            ),
            alternative_satisfaction_basis_refs=alternative_basis_refs_by_condition.get(
                condition_ref, ()
            ),
            minimum_set_ref=f"minimum-set:sandbox:{condition_ref}",
            source_refs=(f"governance:sandbox:{condition_ref}",),
            provenance_refs=(f"provenance:governed:sandbox:{condition_ref}",),
        )
        for condition_ref in condition_refs
    )


def _goal(goal_ref: str) -> GoalContextV1:
    return GoalContextV1(
        goal_ref=goal_ref,
        primary_goal="controlled cognitive exploration objective",
        secondary_goal_refs=(),
        success_condition_refs=(),
        stop_condition_refs=(),
        provenance={"owner": "controlled sandbox objective governance"},
        trace=f"trace:sandbox:goal:{goal_ref}",
    )


def _situation(
    *,
    coverage_refs: Tuple[str, ...] = (),
    external_refs: Tuple[str, ...] = (),
) -> CurrentCognitiveSituationV1:
    return CurrentCognitiveSituationV1(
        current_cognitive_view_refs=("view:sandbox:minimum:v1",),
        current_cognitive_coverage_refs=coverage_refs,
        current_world_refs=("world:sandbox:initial",),
        current_world_condition_refs=(),
        self_information_refs=("self:sandbox:available:v1",),
        external_information_refs=external_refs,
        role_condition_refs=("condition:role:sandbox:operator:v1",),
        context_condition_refs=(),
        field_condition_refs=(FIELD_CONDITION,),
        intent_condition_refs=(),
        concern_condition_refs=(),
    )


def _basis(
    basis_ref: str,
    condition_ref: str,
    *,
    mode: str = "PERCEPTION",
    contribution: Tuple[str, ...] = (),
    capability_refs: Tuple[str, ...] = (),
    opportunity_refs: Tuple[str, ...] = (),
) -> SandboxStrategyBasisSpecV1:
    return SandboxStrategyBasisSpecV1(
        basis_ref=basis_ref,
        condition_ref=condition_ref,
        acquisition_mode_candidate=mode,
        expected_information_contribution_refs=contribution
        or (f"information:sandbox:{condition_ref}",),
        required_capability_class_refs=capability_refs,
        opportunity_refs=opportunity_refs,
        dependency_refs=(f"dependency:sandbox:{basis_ref}",),
        provenance_refs=(f"provenance:sandbox:basis:{basis_ref}",),
    )


def _scenario(
    scenario_id: str,
    scenario_name: str,
    problem: str,
    goal_ref: str,
    conditions: Tuple[str, ...],
    *,
    context: str = "context:sandbox:controlled:initial",
    external_refs: Tuple[str, ...] = (),
    bases: Tuple[SandboxStrategyBasisSpecV1, ...] = (),
    behavior: str = "unresolved_gap",
    simulated_return_enabled: bool = False,
    simulated_return_payload: Tuple[Tuple[str, str], ...] = (),
    simulated_return_coverage_refs: Tuple[str, ...] = (),
    round_1_context: str = "",
    deferred_condition_refs: Tuple[str, ...] = (),
    rejected_condition_refs: Tuple[str, ...] = (),
    conflict_refs: Tuple[str, ...] = (),
    alternative_basis_refs_by_condition: dict[str, Tuple[str, ...]] | None = None,
    notes: str = "synthetic controlled scenario",
) -> SandboxScenarioV1:
    return SandboxScenarioV1(
        scenario_id=scenario_id,
        scenario_name=scenario_name,
        problem=problem,
        required_conditions=conditions,
        initial_context=context,
        synthetic_inputs=("controlled-governed-rules", "controlled-basis-refs"),
        expected_behavior_class=behavior,
        simulated_return_enabled=simulated_return_enabled,
        simulated_return_payload=simulated_return_payload,
        notes=notes,
        simulated_return_coverage_refs=simulated_return_coverage_refs,
        goal_context=_goal(goal_ref),
        condition_rules=_rules(
            goal_ref, conditions, alternative_basis_refs_by_condition
        ),
        initial_situation=_situation(external_refs=external_refs),
        strategy_basis_specs=bases,
        deferred_condition_refs=deferred_condition_refs,
        rejected_condition_refs=rejected_condition_refs,
        governed_conflict_refs=conflict_refs,
        round_1_context=round_1_context,
    )


def build_sandbox_scenarios_v1() -> Tuple[SandboxScenarioV1, ...]:
    c01 = "condition:sandbox:01:clear-cue"
    c02 = ("condition:sandbox:02:exit-direction-known",)
    c03 = ("condition:sandbox:03:exit-direction-known",)
    c04 = ("condition:sandbox:04:exit-direction-known",)
    c05 = ("condition:sandbox:05:signage", "condition:sandbox:05:spatial")
    c06 = ("condition:sandbox:06:text-evidence",)
    c07 = (
        "condition:sandbox:07:exit",
        "condition:sandbox:07:passability",
        "condition:sandbox:07:destination-sign",
    )
    c08 = ("condition:sandbox:08:primary", "condition:sandbox:08:secondary")
    c09 = ("condition:sandbox:09:valid", "condition:sandbox:09:removed")
    c10 = ("condition:sandbox:10:unresolved",)
    c11 = ("condition:sandbox:11:stable",)
    c12 = ("condition:sandbox:12:exit-direction-known",)

    return (
        _scenario(
            "SCENARIO_01_SINGLE_CLEAR_CUE",
            "Single Clear Cue",
            "problem:sandbox:01:single-clear-cue",
            "goal:sandbox:01:clear-cue",
            (c01,),
            bases=(_basis("basis:sandbox:01:cue", c01),),
            behavior="single_path",
        ),
        _scenario(
            "SCENARIO_02_UNKNOWN_EXIT",
            "Unknown Exit",
            "problem:sandbox:02:unknown-exit",
            "goal:sandbox:02:find-exit",
            c02,
            bases=tuple(
                _basis(f"basis:sandbox:02:{suffix}", c02[0])
                for suffix in ("signage", "flow", "spatial")
            ),
            behavior="multi_path",
            alternative_basis_refs_by_condition={
                c02[0]: (
                    "basis:sandbox:02:signage",
                    "basis:sandbox:02:flow",
                    "basis:sandbox:02:spatial",
                )
            },
            notes="multiple explicit governed bases; sandbox does not choose a winner",
        ),
        _scenario(
            "SCENARIO_03_SIGNAGE_AND_HUMAN_FLOW_AGREE",
            "Signage and Human Flow Agree",
            "problem:sandbox:03:agreeing-cues",
            "goal:sandbox:03:find-exit",
            c03,
            bases=(
                _basis("basis:sandbox:03:signage", c03[0], contribution=("direction:left",)),
                _basis("basis:sandbox:03:flow", c03[0], contribution=("direction:left",)),
            ),
            behavior="multi_path",
            alternative_basis_refs_by_condition={
                c03[0]: ("basis:sandbox:03:signage", "basis:sandbox:03:flow")
            },
            notes="agreement is preserved as independent basis lineage; no fusion is performed",
        ),
        _scenario(
            "SCENARIO_04_SIGNAGE_AND_HUMAN_FLOW_CONFLICT",
            "Signage and Human Flow Conflict",
            "problem:sandbox:04:conflicting-cues",
            "goal:sandbox:04:find-exit",
            c04,
            bases=(
                _basis("basis:sandbox:04:signage", c04[0], contribution=("direction:a",)),
                _basis("basis:sandbox:04:flow", c04[0], contribution=("direction:b",)),
            ),
            behavior="conflict_preservation",
            conflict_refs=("conflict:sandbox:04:direction",),
            alternative_basis_refs_by_condition={
                c04[0]: ("basis:sandbox:04:signage", "basis:sandbox:04:flow")
            },
            notes="conflict remains represented; no majority, confidence or action decision",
        ),
        _scenario(
            "SCENARIO_05_SIGNAGE_NOT_VISIBLE",
            "Signage Not Visible",
            "problem:sandbox:05:signage-absent",
            "goal:sandbox:05:find-exit",
            c05,
            bases=(_basis("basis:sandbox:05:spatial", c05[1]),),
            behavior="governed_absence",
        ),
        _scenario(
            "SCENARIO_06_OCR_CONDITIONS_INSUFFICIENT",
            "OCR Conditions Insufficient",
            "problem:sandbox:06:ocr-conditions",
            "goal:sandbox:06:read-sign",
            c06,
            bases=(
                _basis(
                    "basis:sandbox:06:text",
                    c06[0],
                    mode="PERCEPTION",
                    capability_refs=("capability-class:opaque:text-evidence",),
                ),
            ),
            behavior="unresolved_gap",
            notes="capability class is a preserved ref; no OCR or capability execution",
        ),
        _scenario(
            "SCENARIO_07_MULTIPLE_UNKNOWNS",
            "Multiple Unknowns",
            "problem:sandbox:07:multiple-unknowns",
            "goal:sandbox:07:situated-navigation",
            c07,
            bases=tuple(
                _basis(f"basis:sandbox:07:{index}", condition)
                for index, condition in enumerate(c07, 1)
            ),
            behavior="multi_path",
            notes="each strategy retains its own gap and branch lineage",
        ),
        _scenario(
            "SCENARIO_08_DEFERRED_BRANCH",
            "Deferred Branch",
            "problem:sandbox:08:deferred-branch",
            "goal:sandbox:08:explore",
            c08,
            bases=tuple(
                _basis(f"basis:sandbox:08:{index}", condition)
                for index, condition in enumerate(c08, 1)
            ),
            behavior="deferred_branch",
            deferred_condition_refs=(c08[1],),
        ),
        _scenario(
            "SCENARIO_09_REJECTED_BRANCH",
            "Rejected Branch",
            "problem:sandbox:09:rejected-branch",
            "goal:sandbox:09:explore",
            c09,
            bases=tuple(
                _basis(f"basis:sandbox:09:{index}", condition)
                for index, condition in enumerate(c09, 1)
            ),
            behavior="rejected_branch",
            rejected_condition_refs=(c09[1],),
        ),
        _scenario(
            "SCENARIO_10_NO_ACQUISITION_STRATEGY_AVAILABLE",
            "No Acquisition Strategy Available",
            "problem:sandbox:10:no-acquisition-strategy",
            "goal:sandbox:10:unknown",
            c10,
            behavior="governed_absence",
            notes="Need and Branch may exist, but no governed basis is supplied",
        ),
        _scenario(
            "SCENARIO_11_IRRELEVANT_ENVIRONMENTAL_CHANGE",
            "Irrelevant Environmental Change",
            "problem:sandbox:11:irrelevant-change",
            "goal:sandbox:11:stable-cognition",
            c11,
            bases=(_basis("basis:sandbox:11:stable", c11[0]),),
            behavior="stability_under_irrelevant_change",
            simulated_return_enabled=True,
            simulated_return_payload=(("change", "opaque irrelevant environment"),),
            round_1_context="context:sandbox:controlled:irrelevant-change",
            notes="Round 1 is created by a sandbox-only return with no evidence coverage addition",
        ),
        _scenario(
            "SCENARIO_12_EVIDENCE_CHANGES_COGNITIVE_BASIS",
            "Evidence Changes Cognitive Basis",
            "problem:sandbox:12:evidence-update",
            "goal:sandbox:12:find-exit",
            c12,
            bases=(
                _basis("basis:sandbox:12:signage", c12[0], contribution=("direction:left",)),
                _basis("basis:sandbox:12:flow", c12[0], contribution=("direction:unknown",)),
            ),
            behavior="cognitive_update",
            simulated_return_enabled=True,
            simulated_return_payload=(("evidence", "synthetic signage indicates left"),),
            simulated_return_coverage_refs=("basis:sandbox:12:signage",),
            alternative_basis_refs_by_condition={
                c12[0]: ("basis:sandbox:12:signage", "basis:sandbox:12:flow")
            },
            notes="Round 1 injects only controlled synthetic coverage; no real acquisition is executed",
        ),
    )


__all__ = ["build_sandbox_scenarios_v1"]
