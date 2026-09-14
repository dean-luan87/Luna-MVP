"""Controlled dynamic Cognitive Flow scenario inventory (36 cases).

The fixture contains references and candidate outcomes only.  It is intentionally
independent from camera, provider, model, runtime, memory, and learning paths.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Tuple

from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_types_v1 import (
    CapabilityRequirementFormationCandidateV1,
    CognitiveNeedCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_types_v1 import (
    CapabilityOutcomeAssessmentV1,
    CapabilityInvocationCandidateV1,
    CapabilityRequirementV1,
    CapabilityResolutionCandidateV1,
)

from .cognitive_dynamic_loop_types_v1 import (
    CognitiveEvidenceUpdateCandidateV1,
    CognitiveGoalCandidateV1,
    DynamicCognitiveLoopInputV1,
    ProvisionalPlanCandidateV1,
)


@dataclass(frozen=True)
class DynamicCognitiveLoopScenarioV1:
    scenario_id: str
    title: str
    request: DynamicCognitiveLoopInputV1
    expected_final_disposition: str
    expected_next_step_disposition: str
    expected_state_version_count: int
    expected_reconsideration_count: int
    expected_non_materialized_plan_count: int
    notes: str
    expected_eligible_invocation: Optional[bool] = None


def _goal(scenario_id: str) -> CognitiveGoalCandidateV1:
    return CognitiveGoalCandidateV1(
        goal_ref=f"goal:{scenario_id}",
        goal_statement_candidate="find an exit from the bounded scene",
        success_condition_refs=(f"condition:{scenario_id}:exit-located",),
        context_refs=(f"context:{scenario_id}",),
        intent_refs=(f"intent:{scenario_id}",),
        trace_ref=f"trace:{scenario_id}:goal",
    )


def _need(scenario_id: str, ref: str, state_version: str) -> CognitiveNeedCandidateV1:
    return CognitiveNeedCandidateV1(
        need_id=ref,
        source_intent_ref=f"intent:{scenario_id}",
        source_context_ref=f"context:{scenario_id}",
        source_field_ref=f"field:{scenario_id}",
        source_hypothesis_ref=f"hypothesis:{scenario_id}:exit",
        source_attention_ref=f"attention:{scenario_id}",
        problem_description=f"observe candidate point for {scenario_id}",
        missing_information_class="exit_visibility",
        required_evidence_class="visual_spatial_evidence",
        urgency="NORMAL",
        safety_relevance="RELEVANT",
        trace_ref=f"trace:{scenario_id}:{ref}",
        state_version_ref=state_version,
    )


def _event(
    scenario_id: str,
    index: int,
    source_state: str,
    *,
    sufficient: bool = False,
    invalidates: bool = False,
    replacement_need_ref: Optional[str] = None,
    availability: Optional[str] = None,
    execution_outcome: Optional[str] = None,
    requirement_satisfaction: Optional[str] = None,
    task_contribution: Optional[str] = None,
    evidence_kind: str = "OBSERVATION_EVIDENCE",
) -> CognitiveEvidenceUpdateCandidateV1:
    return CognitiveEvidenceUpdateCandidateV1(
        evidence_update_ref=f"evidence:{scenario_id}:{index}",
        source_state_version_ref=source_state,
        evidence_refs=(f"observation:{scenario_id}:{index}",),
        evidence_kind=evidence_kind,
        establishes_goal_sufficiency=sufficient,
        invalidates_hypothesis=invalidates,
        replacement_hypothesis_refs=(f"hypothesis:{scenario_id}:revised",) if invalidates else (),
        replacement_need_ref=replacement_need_ref,
        capability_result_ref=f"capability-result:{scenario_id}:{index}" if execution_outcome else None,
        execution_outcome=execution_outcome,
        requirement_satisfaction=requirement_satisfaction,
        task_contribution=task_contribution,
        capability_availability=availability,
        trace_ref=f"trace:{scenario_id}:evidence:{index}",
    )


def _formation(
    scenario_id: str,
    state_version: str,
) -> Tuple[
    CapabilityRequirementFormationCandidateV1,
    CapabilityResolutionCandidateV1,
    CapabilityInvocationCandidateV1,
]:
    requirement = CapabilityRequirementV1(
        requirement_id=f"requirement:{scenario_id}",
        requested_module_id=None,
        purpose="exit_visibility",
        task_context="bounded exit search",
        required_semantic_depth="MINIMAL",
        permission_refs=(),
        resource_refs=(),
        execution_boundary_ref="Observation Gateway -> governed capability boundary",
        requester_ref=f"intent:{scenario_id}",
        requirement_type="CAPABILITY_REQUEST",
        problem_class="exit_visibility",
        requested_operation="OBSERVE_REGION",
        input_contract_ref="observation-request-v1",
        expected_output_contract_ref="evidence-candidate-v1",
        required_authority="EVIDENCE_ONLY",
        task_context_refs=(f"context:{scenario_id}",),
        trace_ref=f"trace:{scenario_id}:requirement",
    )
    formation = CapabilityRequirementFormationCandidateV1(
        formation_id=f"formation:{scenario_id}",
        source_need_ref=f"need:{scenario_id}:1",
        requirement_ref=requirement.requirement_id,
        requirement=requirement,
        selected_problem_class="exit_visibility",
        requested_operation="OBSERVE_REGION",
        input_contract_ref="observation-request-v1",
        output_contract_ref="evidence-candidate-v1",
        required_authority="EVIDENCE_ONLY",
        requirement_minimized=True,
        trace_ref=f"trace:{scenario_id}:requirement",
        source_state_version_ref=state_version,
    )
    invocation = CapabilityInvocationCandidateV1(
        invocation_id=f"invocation:{scenario_id}",
        requirement_ref=requirement.requirement_id,
        module_ref="module:bounded-observation",
        slot_ref="slot:observation",
        execution_boundary_ref=requirement.execution_boundary_ref,
        accepted=True,
        reason="INVOCATION_HANDOFF_CANDIDATE",
        scope_assessment_ref=f"scope:{requirement.requirement_id}",
        gateway_refs=(f"gateway:{scenario_id}",),
        trace_refs=(f"trace:{scenario_id}:invocation",),
    )
    resolution = CapabilityResolutionCandidateV1(
        requirement_id=requirement.requirement_id,
        status="READY_CANDIDATE",
        module_ref="module:bounded-observation",
        slot_ref="slot:observation",
        implementation_refs=("implementation:bounded-observation",),
        model_asset_refs=(),
        provider_contract_refs=("provider-contract:evidence-only",),
        reason="GOVERNED_CAPABILITY_RESOLUTION_CANDIDATE",
        recovery_available=True,
        scope_assessment_ref=f"scope:{requirement.requirement_id}",
    )
    return formation, resolution, invocation


def _request(
    scenario_id: str,
    events: Iterable[CognitiveEvidenceUpdateCandidateV1],
    *,
    plan_count: int = 7,
    need_count: int = 7,
    extra_need_refs: Tuple[str, ...] = (),
    initial_state: str = "state:SCENARIO:v1",
    initial_need: Optional[str] = None,
    initial_disposition: str = "INSUFFICIENT",
    requirements: Tuple[CapabilityRequirementFormationCandidateV1, ...] = (),
    resolutions: Tuple[CapabilityResolutionCandidateV1, ...] = (),
    invocations: Tuple[CapabilityInvocationCandidateV1, ...] = (),
) -> DynamicCognitiveLoopInputV1:
    state = initial_state.replace("SCENARIO", scenario_id)
    event_updates = tuple(events)
    plan_refs = tuple(f"need:{scenario_id}:{index}" for index in range(1, plan_count + 1))
    needs = tuple(
        _need(scenario_id, f"need:{scenario_id}:{index}", state)
        for index in range(1, need_count + 1)
    ) + tuple(_need(scenario_id, ref, state) for ref in extra_need_refs)
    capability_outcomes = tuple(
        CapabilityOutcomeAssessmentV1(
            assessment_id=f"assessment:{scenario_id}:{index}",
            usage_ref=f"usage:{scenario_id}:{index}",
            execution_outcome=event.execution_outcome or "UNKNOWN",
            requirement_satisfaction=event.requirement_satisfaction or "UNKNOWN",
            task_contribution=event.task_contribution or "UNKNOWN",
            evidence_refs=event.evidence_refs,
            failure_pattern_refs=(),
            reason="CONTROLLED_OUTCOME_DIMENSIONS_PRESERVED",
        )
        for index, event in enumerate(event_updates, start=1)
        if event.execution_outcome is not None
    )
    return DynamicCognitiveLoopInputV1(
        scenario_id=scenario_id,
        goal=_goal(scenario_id),
        provisional_plan=ProvisionalPlanCandidateV1(
            plan_ref=f"plan:{scenario_id}",
            goal_ref=f"goal:{scenario_id}",
            candidate_step_refs=plan_refs,
            plan_completeness_status="PROVISIONAL",
            trace_ref=f"trace:{scenario_id}:plan",
        ),
        initial_state_version_ref=state,
        initial_disposition=initial_disposition,
        initial_hypothesis_refs=(f"hypothesis:{scenario_id}:exit",),
        initial_minimum_need_ref=initial_need or (plan_refs[0] if plan_refs else None),
        evidence_updates=event_updates,
        needs=needs,
        requirements=requirements,
        resolutions=resolutions,
        invocations=invocations,
        capability_outcomes=capability_outcomes,
    )


def _case(
    scenario_id: str,
    title: str,
    request: DynamicCognitiveLoopInputV1,
    final_disposition: str,
    next_step: str,
    state_count: int,
    reconsideration_count: int,
    non_materialized_count: int,
    notes: str,
    expected_eligible_invocation: Optional[bool] = None,
) -> DynamicCognitiveLoopScenarioV1:
    return DynamicCognitiveLoopScenarioV1(
        scenario_id=scenario_id,
        title=title,
        request=request,
        expected_final_disposition=final_disposition,
        expected_next_step_disposition=next_step,
        expected_state_version_count=state_count,
        expected_reconsideration_count=reconsideration_count,
        expected_non_materialized_plan_count=non_materialized_count,
        notes=notes,
        expected_eligible_invocation=expected_eligible_invocation,
    )


def build_dynamic_cognitive_loop_scenarios_v1() -> Tuple[DynamicCognitiveLoopScenarioV1, ...]:
    """Return 36 non-duplicative dynamic-state scenarios grouped A-F."""

    cases = []

    # A: seven provisional observation candidates and early sufficiency.
    cases.extend(
        (
            _case("A01", "one insufficient observation", _request("A01", (_event("A01", 1, "state:A01:v1"),)), "INSUFFICIENT", "CONTINUE", 2, 0, 5, "next minimum need only"),
            _case("A02", "two insufficient observations", _request("A02", (_event("A02", 1, "state:A02:v1"), _event("A02", 2, "state:A02:v2"))), "INSUFFICIENT", "CONTINUE", 3, 0, 4, "third candidate remains provisional"),
            _case("A03", "third observation finds exit", _request("A03", (_event("A03", 1, "state:A03:v1"), _event("A03", 2, "state:A03:v2"), _event("A03", 3, "state:A03:v3", sufficient=True))), "SUFFICIENT", "STOP_SUFFICIENT", 4, 0, 4, "candidate 4-7 do not materialize"),
            _case("A04", "first observation is sufficient", _request("A04", (_event("A04", 1, "state:A04:v1", sufficient=True),)), "SUFFICIENT", "STOP_SUFFICIENT", 2, 0, 6, "early termination"),
            _case("A05", "no evidence leaves loop deferred", _request("A05", ()), "INSUFFICIENT", "DEFER", 1, 0, 6, "no implicit invocation"),
            _case("A06", "remaining plan candidates stay non-binding", _request("A06", (_event("A06", 1, "state:A06:v1"),)), "INSUFFICIENT", "CONTINUE", 2, 0, 5, "plan completeness is not execution completeness"),
        )
    )

    # B: evidence revises the hypothesis and invalidates the old path.
    cases.extend(
        (
            _case("B01", "second evidence invalidates hypothesis", _request("B01", (_event("B01", 1, "state:B01:v1"), _event("B01", 2, "state:B01:v2", invalidates=True, replacement_need_ref="need:B01:alternative")), extra_need_refs=("need:B01:alternative",)), "RECONSIDER", "REPLAN", 3, 1, 5, "old remaining path is non-binding"),
            _case("B02", "first evidence selects alternative need", _request("B02", (_event("B02", 1, "state:B02:v1", invalidates=True, replacement_need_ref="need:B02:alternative"),), extra_need_refs=("need:B02:alternative",)), "RECONSIDER", "REPLAN", 2, 1, 6, "replacement need outranks old plan"),
            _case("B03", "hypothesis revision without explicit alternative", _request("B03", (_event("B03", 1, "state:B03:v1", invalidates=True),)), "RECONSIDER", "REPLAN", 2, 1, 5, "next plan candidate is still only a candidate"),
            _case("B04", "contradictory evidence revises state version", _request("B04", (_event("B04", 1, "state:B04:v1"), _event("B04", 2, "state:B04:v2", invalidates=True, replacement_need_ref="need:B04:alternative", evidence_kind="CONTRADICTORY_EVIDENCE")), extra_need_refs=("need:B04:alternative",)), "RECONSIDER", "REPLAN", 3, 1, 5, "state lineage retained"),
            _case("B05", "new evidence supersedes third step", _request("B05", (_event("B05", 1, "state:B05:v1"), _event("B05", 2, "state:B05:v2", invalidates=True, replacement_need_ref="need:B05:alternative")), extra_need_refs=("need:B05:alternative",)), "RECONSIDER", "REPLAN", 3, 1, 5, "remaining old candidates cannot force invocation"),
            _case("B06", "replacement hypothesis retains provenance", _request("B06", (_event("B06", 1, "state:B06:v1", invalidates=True, replacement_need_ref="need:B06:alternative"),), extra_need_refs=("need:B06:alternative",)), "RECONSIDER", "REPLAN", 2, 1, 6, "alternative hypothesis is candidate-only"),
        )
    )

    # C: unavailable/degraded capability returns to cognitive reconsideration.
    cases.extend(
        (
            _case("C01", "capability unavailable with alternative", _request("C01", (_event("C01", 1, "state:C01:v1", availability="UNAVAILABLE", replacement_need_ref="need:C01:alternative"),), extra_need_refs=("need:C01:alternative",)), "RECONSIDER", "REQUEST_MORE_EVIDENCE", 2, 1, 6, "no hallucinated evidence"),
            _case("C02", "capability degraded with alternative", _request("C02", (_event("C02", 1, "state:C02:v1", availability="DEGRADED", replacement_need_ref="need:C02:alternative"),), extra_need_refs=("need:C02:alternative",)), "RECONSIDER", "REQUEST_MORE_EVIDENCE", 2, 1, 6, "governed alternative path"),
            _case("C03", "capability unavailable without alternative", _request("C03", (_event("C03", 1, "state:C03:v1", availability="UNAVAILABLE"),), plan_count=1, need_count=1), "RECONSIDER", "DEFER", 2, 1, 0, "unavailability is not fabricated success"),
            _case("C04", "degraded capability does not bypass scope", _request("C04", (_event("C04", 1, "state:C04:v1", availability="DEGRADED", replacement_need_ref="need:C04:alternative"),), extra_need_refs=("need:C04:alternative",)), "RECONSIDER", "REQUEST_MORE_EVIDENCE", 2, 1, 6, "scope and authority remain external gates"),
            _case("C05", "unavailable capability preserves uncertainty", _request("C05", (_event("C05", 1, "state:C05:v1", availability="UNAVAILABLE", replacement_need_ref="need:C05:alternative"),), extra_need_refs=("need:C05:alternative",)), "RECONSIDER", "REQUEST_MORE_EVIDENCE", 2, 1, 6, "uncertainty is not a provider result"),
            _case("C06", "observation gateway remains handoff only", _request("C06", (_event("C06", 1, "state:C06:v1", availability="DEGRADED", replacement_need_ref="need:C06:alternative"),), extra_need_refs=("need:C06:alternative",)), "RECONSIDER", "REQUEST_MORE_EVIDENCE", 2, 1, 6, "no camera or scheduler execution"),
        )
    )

    # D: execution result, requirement satisfaction, and task contribution differ.
    cases.extend(
        (
            _case("D01", "execution success but requirement unsatisfied", _request("D01", (_event("D01", 1, "state:D01:v1", execution_outcome="SUCCESS", requirement_satisfaction="UNSATISFIED", task_contribution="NO_CONTRIBUTION", replacement_need_ref="need:D01:alternative"),), extra_need_refs=("need:D01:alternative",)), "RECONSIDER", "REQUEST_MORE_EVIDENCE", 2, 1, 6, "success is not requirement satisfaction"),
            _case("D02", "execution success with partial requirement", _request("D02", (_event("D02", 1, "state:D02:v1", execution_outcome="SUCCESS", requirement_satisfaction="PARTIAL", task_contribution="CONTRIBUTED"),)), "INSUFFICIENT", "CONTINUE", 2, 0, 5, "partial evidence continues"),
            _case("D03", "execution success with unresolved task", _request("D03", (_event("D03", 1, "state:D03:v1", execution_outcome="SUCCESS", requirement_satisfaction="SATISFIED", task_contribution="UNRESOLVED"),)), "INSUFFICIENT", "CONTINUE", 2, 0, 5, "requirement satisfaction is not goal sufficiency"),
            _case("D04", "successful capability does not close goal", _request("D04", (_event("D04", 1, "state:D04:v1", execution_outcome="SUCCESS", task_contribution="CONTRIBUTED"),)), "INSUFFICIENT", "CONTINUE", 2, 0, 5, "goal remains insufficient"),
            _case("D05", "unsatisfied result requests more evidence", _request("D05", (_event("D05", 1, "state:D05:v1", execution_outcome="SUCCESS", requirement_satisfaction="UNSATISFIED", replacement_need_ref="need:D05:alternative"),), extra_need_refs=("need:D05:alternative",)), "RECONSIDER", "REQUEST_MORE_EVIDENCE", 2, 1, 6, "reconsideration is not retry"),
            _case("D06", "later evidence can close after unsatisfied result", _request("D06", (_event("D06", 1, "state:D06:v1", execution_outcome="SUCCESS", requirement_satisfaction="UNSATISFIED", replacement_need_ref="need:D06:alternative"), _event("D06", 2, "state:D06:v2", sufficient=True)), extra_need_refs=("need:D06:alternative",)), "SUFFICIENT", "STOP_SUFFICIENT", 3, 1, 6, "goal sufficiency terminates remaining candidates"),
        )
    )

    # E: capability failure does not force continuation when the goal is sufficient.
    cases.extend(
        (
            _case("E01", "failure plus independent sufficient evidence", _request("E01", (_event("E01", 1, "state:E01:v1", sufficient=True, execution_outcome="FAILURE"),)), "SUFFICIENT", "STOP_SUFFICIENT", 2, 0, 6, "failure is not task failure"),
            _case("E02", "timeout plus sufficient evidence", _request("E02", (_event("E02", 1, "state:E02:v1", sufficient=True, execution_outcome="TIMEOUT"),)), "SUFFICIENT", "STOP_SUFFICIENT", 2, 0, 6, "stop remains successful cognitive termination"),
            _case("E03", "degraded result plus sufficient evidence", _request("E03", (_event("E03", 1, "state:E03:v1", sufficient=True, availability="DEGRADED"),)), "SUFFICIENT", "STOP_SUFFICIENT", 2, 0, 6, "no forced fallback after sufficiency"),
            _case("E04", "failure does not resume old plan", _request("E04", (_event("E04", 1, "state:E04:v1", sufficient=True, execution_outcome="FAILURE"),)), "SUFFICIENT", "STOP_SUFFICIENT", 2, 0, 6, "remaining candidates non-materialized"),
            _case("E05", "goal evidence outranks capability failure", _request("E05", (_event("E05", 1, "state:E05:v1", sufficient=True, execution_outcome="CANCELLED"),)), "SUFFICIENT", "STOP_SUFFICIENT", 2, 0, 6, "single failure cannot force original plan"),
            _case("E06", "STOP_SUFFICIENT is not a failure", _request("E06", (_event("E06", 1, "state:E06:v1", sufficient=True, execution_outcome="FAILURE"),)), "SUFFICIENT", "STOP_SUFFICIENT", 2, 0, 6, "unexecuted candidates are not failures"),
        )
    )

    # F: requirements are evaluated against the state version that generated them.
    for scenario_id, source_state, initial_state, expected_eligible, title in (
        ("F01", "state:F01:v2", "state:F01:v3", False, "old requirement from v2 is stale"),
        ("F02", "state:F02:v2", "state:F02:v3", False, "stale requirement cannot force invocation"),
        ("F03", "state:F03:v3", "state:F03:v3", True, "current requirement remains eligible"),
        ("F04", "state:F04:v2", "state:F04:v3", False, "stale invocation candidate is blocked"),
        ("F05", "state:F05:v2", "state:F05:v2", False, "refresh supersedes v2 requirement at v3"),
        ("F06", "state:F06:v2", "state:F06:v3", False, "reassess before downstream demand"),
    ):
        formation, resolution, invocation = _formation(scenario_id, source_state)
        event = () if scenario_id != "F05" else (_event("F05", 1, "state:F05:v2", evidence_kind="STATE_REFRESH"),)
        request = _request(
            scenario_id,
            event,
            initial_state=initial_state,
            requirements=(formation,),
            resolutions=(resolution,),
            invocations=(invocation,),
        )
        cases.append(
            _case(
                scenario_id,
                title,
                request,
                "INSUFFICIENT",
                "DEFER" if not event else "CONTINUE",
                1 if not event else 2,
                0,
                6 if not event else 5,
                "stale requirement is SUPERSEDED" if not expected_eligible else "requirement matches current state version",
                expected_eligible_invocation=expected_eligible,
            )
        )
    return tuple(cases)


__all__ = ["DynamicCognitiveLoopScenarioV1", "build_dynamic_cognitive_loop_scenarios_v1"]
