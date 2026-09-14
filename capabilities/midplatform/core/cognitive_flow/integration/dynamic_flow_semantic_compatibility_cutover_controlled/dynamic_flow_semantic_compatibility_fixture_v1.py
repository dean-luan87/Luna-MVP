"""Synthetic fixture corpus for the Dynamic Flow compatibility cutover."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_types_v1 import (
    CognitiveGoalCandidateV1,
    CognitiveStateVersionCandidateV1,
    DynamicCognitiveLoopOutputV1,
    GoalSufficiencyCandidateV1,
    ProvisionalPlanCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_transition_types_v1 import (
    ReconsiderationCandidateV1,
)

from .dynamic_flow_semantic_compatibility_engine_v1 import interpret_for_a, interpretation_is_a_owned
from .dynamic_flow_semantic_compatibility_types_v1 import CompatibilityScenarioResultV1


@dataclass(frozen=True)
class CompatibilityScenarioSpecV1:
    scenario_id: str
    family: str
    final_disposition: str
    next_step: str
    sufficient: bool = False
    reconsideration: bool = False
    migrated_caller: bool = True


def build_compatibility_scenario_specs_v1() -> Tuple[CompatibilityScenarioSpecV1, ...]:
    rows = (
        ("DC-01", "NEED", "INSUFFICIENT", "CONTINUE"),
        ("DC-02", "NEED", "INSUFFICIENT", "CONTINUE"),
        ("DC-03", "NEED", "RECONSIDER", "REPLAN", False, True),
        ("DC-04", "NEED", "SUFFICIENT", "STOP_SUFFICIENT", True),
        ("DC-05", "SUFFICIENCY", "SUFFICIENT", "STOP_SUFFICIENT", True),
        ("DC-06", "SUFFICIENCY", "INSUFFICIENT", "REQUEST_MORE_EVIDENCE"),
        ("DC-07", "SUFFICIENCY", "RECONSIDER", "REQUEST_MORE_EVIDENCE", False, True),
        ("DC-08", "SUFFICIENCY", "INSUFFICIENT", "DEFER"),
        ("DC-09", "RECONSIDERATION", "RECONSIDER", "REPLAN", False, True),
        ("DC-10", "RECONSIDERATION", "INSUFFICIENT", "CONTINUE"),
        ("DC-11", "RECONSIDERATION", "SUFFICIENT", "STOP_SUFFICIENT", True),
        ("DC-12", "NEXT_STEP", "INSUFFICIENT", "CONTINUE"),
        ("DC-13", "NEXT_STEP", "INSUFFICIENT", "REQUEST_MORE_EVIDENCE"),
        ("DC-14", "NEXT_STEP", "INSUFFICIENT", "REPLAN"),
        ("DC-15", "NEXT_STEP", "SUFFICIENT", "STOP_SUFFICIENT", True),
        ("DC-16", "NEXT_STEP", "INSUFFICIENT", "WAIT"),
        ("DC-17", "NEXT_STEP", "INSUFFICIENT", "PAUSE"),
        ("DC-18", "NEXT_STEP", "INSUFFICIENT", "DEFER"),
        ("DC-19", "CALLER_CUTOVER", "INSUFFICIENT", "CONTINUE"),
        ("DC-20", "CALLER_CUTOVER", "SUFFICIENT", "STOP_SUFFICIENT", True),
        ("DC-21", "CALLER_CUTOVER", "RECONSIDER", "REPLAN", False, True),
        ("DC-22", "CALLER_CUTOVER", "INSUFFICIENT", "REQUEST_MORE_EVIDENCE"),
        ("DC-23", "REAL_CAPABILITY_RESERVATION", "INSUFFICIENT", "REQUEST_MORE_EVIDENCE"),
        ("DC-24", "REAL_CAPABILITY_RESERVATION", "SUFFICIENT", "STOP_SUFFICIENT", True),
        ("DC-25", "REAL_CAPABILITY_RESERVATION", "INSUFFICIENT", "REQUEST_MORE_EVIDENCE"),
        ("DC-26", "LEGACY_COMPATIBILITY", "INSUFFICIENT", "CONTINUE"),
        ("DC-27", "LEGACY_COMPATIBILITY", "RECONSIDER", "REPLAN", False, True),
        ("DC-28", "LEGACY_COMPATIBILITY", "SUFFICIENT", "STOP_SUFFICIENT", True),
        ("DC-29", "NEGATIVE_GUARD", "INSUFFICIENT", "CONTINUE"),
        ("DC-30", "NEGATIVE_GUARD", "SUFFICIENT", "STOP_SUFFICIENT", True),
        ("DC-31", "NEGATIVE_GUARD", "RECONSIDER", "REQUEST_MORE_EVIDENCE", False, True),
        ("DC-32", "NEGATIVE_GUARD", "INSUFFICIENT", "REPLAN"),
        ("DC-33", "CALLER_CUTOVER", "INSUFFICIENT", "CONTINUE"),
        ("DC-34", "LEGACY_COMPATIBILITY", "INSUFFICIENT", "REQUEST_MORE_EVIDENCE"),
    )
    return tuple(CompatibilityScenarioSpecV1(*row) for row in rows)


def _output(spec: CompatibilityScenarioSpecV1) -> DynamicCognitiveLoopOutputV1:
    state = CognitiveStateVersionCandidateV1(
        state_version_ref=f"state:{spec.scenario_id}:v1",
        parent_state_version_ref=None,
        evidence_update_ref=f"evidence-update:{spec.scenario_id}:1",
        current_disposition=spec.final_disposition,
        current_minimum_need_ref=f"need:{spec.scenario_id}:minimum",
        active_hypothesis_refs=(f"hypothesis:{spec.scenario_id}:active",),
        invalidated_hypothesis_refs=(f"hypothesis:{spec.scenario_id}:invalidated",) if spec.reconsideration else (),
        sufficiency_ref=f"sufficiency:{spec.scenario_id}",
        reconsideration_ref=f"reconsideration:{spec.scenario_id}" if spec.reconsideration else None,
        trace_ref=f"trace:{spec.scenario_id}:state",
    )
    goal = CognitiveGoalCandidateV1(
        goal_ref=f"goal:{spec.scenario_id}",
        goal_statement_candidate="synthetic compatibility goal",
        success_condition_refs=(f"condition:{spec.scenario_id}:sufficient",),
        context_refs=(f"context:{spec.scenario_id}",),
        intent_refs=(f"intent:{spec.scenario_id}",),
        trace_ref=f"trace:{spec.scenario_id}:goal",
    )
    plan = ProvisionalPlanCandidateV1(
        plan_ref=f"plan:{spec.scenario_id}",
        goal_ref=goal.goal_ref,
        candidate_step_refs=(f"need:{spec.scenario_id}:minimum", f"need:{spec.scenario_id}:remaining"),
        plan_completeness_status="PROVISIONAL",
        trace_ref=f"trace:{spec.scenario_id}:plan",
    )
    sufficiency = GoalSufficiencyCandidateV1(
        sufficiency_ref=f"sufficiency:{spec.scenario_id}",
        goal_ref=goal.goal_ref,
        state_version_ref=state.state_version_ref,
        status="SUFFICIENT" if spec.sufficient else "INSUFFICIENT",
        evidence_refs=(f"evidence:{spec.scenario_id}:1",),
        reason="synthetic compatibility fixture",
        stop_disposition=spec.next_step,
        terminates_remaining_plan=spec.sufficient,
    )
    return DynamicCognitiveLoopOutputV1(
        scenario_id=spec.scenario_id,
        goal=goal,
        provisional_plan=plan,
        state_versions=(state,),
        transitions=(),
        needs_materialized=(f"need:{spec.scenario_id}:minimum",),
        current_minimum_need_ref=f"need:{spec.scenario_id}:minimum",
        requirement_refs=(f"requirement:{spec.scenario_id}:minimum",),
        resolution_refs=(f"resolution:{spec.scenario_id}:minimum",),
        invocation_candidate_refs=(f"invocation:{spec.scenario_id}:minimum",),
        eligible_invocation_refs=(),
        stale_requirement_refs=(),
        capability_outcome_refs=(f"outcome:{spec.scenario_id}:minimum",),
        sufficiency_candidates=(sufficiency,),
        reconsiderations=(
            ReconsiderationCandidateV1(
                cycle_id=f"cycle:{spec.scenario_id}",
                source_stage="Dynamic Flow Compatibility",
                target_stage="A Reasoning",
                reconsideration_reason="synthetic compatibility reconsideration",
                related_refs=(f"state:{spec.scenario_id}:v1",),
                trace_ref=f"trace:{spec.scenario_id}:reconsideration",
            ),
        ) if spec.reconsideration else (),
        evidence_update_refs=(f"evidence-update:{spec.scenario_id}:1",),
        ignored_evidence_update_refs=(),
        non_materialized_plan_refs=(f"need:{spec.scenario_id}:remaining",),
        final_disposition=spec.final_disposition,
        next_step_disposition=spec.next_step,
        trace_refs=(f"trace:{spec.scenario_id}:flow",),
        provenance_refs=(f"provenance:{spec.scenario_id}:flow",),
    )


def run_compatibility_scenario(spec: CompatibilityScenarioSpecV1) -> CompatibilityScenarioResultV1:
    output = _output(spec)
    interpretation = interpret_for_a(output)
    a_owned = interpretation_is_a_owned(interpretation)
    passed = a_owned and interpretation.a_decisions.next_step_decision.next_step_disposition == spec.next_step
    failures = () if passed else ("A_INTERPRETATION_NOT_AUTHORITY_BOUNDARY",)
    return CompatibilityScenarioResultV1(
        scenario_id=spec.scenario_id,
        scenario_family=spec.family,
        compatibility_output=interpretation.compatibility_output,
        interpretation=interpretation,
        migrated_caller=spec.migrated_caller,
        direct_semantic_consumption_blocked=not interpretation.compatibility_output.semantic_authority,
        expected_disposition=spec.next_step,
        passed=passed,
        failure_refs=failures,
    )


def build_compatibility_run_v1() -> Tuple[CompatibilityScenarioResultV1, ...]:
    return tuple(run_compatibility_scenario(spec) for spec in build_compatibility_scenario_specs_v1())


__all__ = [
    "CompatibilityScenarioSpecV1",
    "build_compatibility_run_v1",
    "build_compatibility_scenario_specs_v1",
    "run_compatibility_scenario",
]
