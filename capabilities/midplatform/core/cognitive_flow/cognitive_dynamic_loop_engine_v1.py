"""Deterministic candidate-only implementation of the minimum dynamic loop."""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple

from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_types_v1 import (
    CognitiveNeedCandidateV1,
)

from .cognitive_cycle_transition_types_v1 import ReconsiderationCandidateV1
from .cognitive_dynamic_loop_types_v1 import (
    COGNITIVE_DISPOSITIONS,
    CAPABILITY_AVAILABILITY,
    CognitiveEvidenceUpdateCandidateV1,
    CognitiveStateVersionCandidateV1,
    DynamicCognitiveLoopInputV1,
    DynamicCognitiveLoopOutputV1,
    DynamicCognitiveLoopTransitionCandidateV1,
    GoalSufficiencyCandidateV1,
)
from .cognitive_flow_registry_v1 import CANONICAL_OWNER


class DynamicCognitiveFlowEngineV1:
    """Builds a bounded re-entry path; it never invokes a downstream owner."""

    def _validate_input(self, request: DynamicCognitiveLoopInputV1) -> None:
        if request.initial_disposition not in COGNITIVE_DISPOSITIONS:
            raise ValueError(f"unsupported initial disposition: {request.initial_disposition}")
        if not request.goal.candidate_only or not request.provisional_plan.candidate_only:
            raise ValueError("dynamic loop inputs must remain candidate-only")
        if request.provisional_plan.execution_queue or request.provisional_plan.binding:
            raise ValueError("a provisional plan cannot be an execution queue or binding")
        for update in request.evidence_updates:
            if not update.candidate_only:
                raise ValueError("evidence updates must remain candidate-only")
            if update.capability_availability not in (None,) + CAPABILITY_AVAILABILITY:
                raise ValueError("unsupported capability availability")

    @staticmethod
    def _advance_state_version(state_ref: str, scenario_id: str) -> str:
        """Advance the explicit version suffix without creating world state."""
        prefix, marker, suffix = state_ref.rpartition(":v")
        if marker and suffix.isdigit():
            return f"{prefix}:v{int(suffix) + 1}"
        return f"state:{scenario_id}:v{state_ref.count(':') + 2}"

    @staticmethod
    def _need_map(needs: Iterable[CognitiveNeedCandidateV1]) -> Dict[str, CognitiveNeedCandidateV1]:
        return {need.need_id: need for need in needs}

    @staticmethod
    def _select_next_need(
        needs: Dict[str, CognitiveNeedCandidateV1],
        plan_refs: Tuple[str, ...],
        materialized: List[str],
        *,
        allow_non_plan_need: bool = False,
    ) -> Optional[str]:
        for ref in plan_refs:
            if ref in needs and ref not in materialized:
                return ref
        if allow_non_plan_need:
            for ref in needs:
                if ref not in materialized:
                    return ref
        return None

    @staticmethod
    def _reconsideration(
        scenario_id: str,
        reason: str,
        state_version_ref: str,
        evidence_update_ref: str,
        related_refs: Tuple[str, ...],
    ) -> ReconsiderationCandidateV1:
        return ReconsiderationCandidateV1(
            cycle_id=f"loop:{scenario_id}",
            source_stage="COGNITIVE_EVIDENCE",
            target_stage="CURRENT_MINIMUM_NEED",
            reconsideration_reason=reason,
            related_refs=(state_version_ref, evidence_update_ref) + related_refs,
            trace_ref=f"trace:{scenario_id}:reconsideration:{evidence_update_ref}",
        )

    def run_case(self, request: DynamicCognitiveLoopInputV1) -> DynamicCognitiveLoopOutputV1:
        """Process already-available candidates without performing acquisition or execution."""

        self._validate_input(request)
        need_map = self._need_map(request.needs)
        materialized: List[str] = []
        if request.initial_minimum_need_ref:
            materialized.append(request.initial_minimum_need_ref)

        current_state_ref = request.initial_state_version_ref
        current_disposition = request.initial_disposition
        current_need_ref = request.initial_minimum_need_ref
        active_hypotheses = list(request.initial_hypothesis_refs)
        state_versions: List[CognitiveStateVersionCandidateV1] = [
            CognitiveStateVersionCandidateV1(
                state_version_ref=current_state_ref,
                parent_state_version_ref=None,
                evidence_update_ref=None,
                current_disposition=current_disposition,
                current_minimum_need_ref=current_need_ref,
                active_hypothesis_refs=tuple(active_hypotheses),
                invalidated_hypothesis_refs=(),
                sufficiency_ref=None,
                reconsideration_ref=None,
                trace_ref=f"trace:{request.scenario_id}:state:0",
            )
        ]
        transitions: List[DynamicCognitiveLoopTransitionCandidateV1] = []
        sufficiency: List[GoalSufficiencyCandidateV1] = []
        reconsiderations: List[ReconsiderationCandidateV1] = []
        accepted_evidence: List[str] = []
        ignored_evidence: List[str] = []
        superseded_requirements: List[str] = []
        non_materialized_plan_refs: Tuple[str, ...] = tuple(
            ref for ref in request.provisional_plan.candidate_step_refs if ref not in materialized
        )
        next_step_disposition = (
            "STOP_SUFFICIENT" if current_disposition == "SUFFICIENT" else "CONTINUE"
        )

        for index, update in enumerate(request.evidence_updates, start=1):
            if current_disposition == "SUFFICIENT":
                ignored_evidence.append(update.evidence_update_ref)
                continue
            if update.source_state_version_ref != current_state_ref:
                ignored_evidence.append(update.evidence_update_ref)
                continue

            accepted_evidence.append(update.evidence_update_ref)
            parent_state_ref = current_state_ref
            next_state_ref = self._advance_state_version(current_state_ref, request.scenario_id)
            related_refs = update.evidence_refs
            selected_next_need: Optional[str] = None
            invalidated_refs: Tuple[str, ...] = ()
            reconsideration_ref: Optional[str] = None

            if update.establishes_goal_sufficiency:
                target_disposition = "SUFFICIENT"
                next_step_disposition = "STOP_SUFFICIENT"
                current_need_ref = None
                non_materialized_plan_refs = tuple(
                    ref for ref in request.provisional_plan.candidate_step_refs if ref not in materialized
                )
                sufficiency.append(
                    GoalSufficiencyCandidateV1(
                        sufficiency_ref=f"sufficiency:{request.scenario_id}:v{index + 1}",
                        goal_ref=request.goal.goal_ref,
                        state_version_ref=next_state_ref,
                        status="SUFFICIENT",
                        evidence_refs=update.evidence_refs,
                        reason="GOAL_CONDITION_SUPPORTED_BY_CURRENT_EVIDENCE_CANDIDATE",
                        stop_disposition="STOP_SUFFICIENT",
                        terminates_remaining_plan=True,
                    )
                )
            else:
                target_disposition = "INSUFFICIENT"
                next_step_disposition = "CONTINUE"
                reason = "CURRENT_EVIDENCE_REMAINS_INSUFFICIENT"
                allow_non_plan_need = False

                if update.invalidates_hypothesis:
                    target_disposition = "RECONSIDER"
                    next_step_disposition = "REPLAN"
                    reason = "NEW_EVIDENCE_INVALIDATES_ACTIVE_HYPOTHESIS"
                    invalidated_refs = tuple(active_hypotheses)
                    active_hypotheses = list(update.replacement_hypothesis_refs)
                    allow_non_plan_need = True
                elif update.capability_availability in {"UNAVAILABLE", "DEGRADED"}:
                    target_disposition = "RECONSIDER"
                    next_step_disposition = "REQUEST_MORE_EVIDENCE"
                    reason = (
                        "CAPABILITY_DEGRADED_REQUIRES_GOVERNED_ALTERNATIVE_EVIDENCE"
                        if update.capability_availability == "DEGRADED"
                        else "CAPABILITY_UNAVAILABLE_REQUIRES_GOVERNED_ALTERNATIVE_EVIDENCE"
                    )
                    allow_non_plan_need = True
                elif (
                    update.execution_outcome == "SUCCESS"
                    and update.requirement_satisfaction == "UNSATISFIED"
                ):
                    target_disposition = "RECONSIDER"
                    next_step_disposition = "REQUEST_MORE_EVIDENCE"
                    reason = "CAPABILITY_EXECUTION_SUCCESS_BUT_REQUIREMENT_UNSATISFIED"
                    allow_non_plan_need = True

                selected_next_need = (
                    update.replacement_need_ref
                    if update.replacement_need_ref in need_map
                    and update.replacement_need_ref not in materialized
                    else self._select_next_need(
                        need_map,
                        request.provisional_plan.candidate_step_refs,
                        materialized,
                        allow_non_plan_need=allow_non_plan_need,
                    )
                )
                if selected_next_need:
                    materialized.append(selected_next_need)
                    current_need_ref = selected_next_need
                    non_materialized_plan_refs = tuple(
                        ref
                        for ref in request.provisional_plan.candidate_step_refs
                        if ref not in materialized
                    )
                else:
                    current_need_ref = None
                    if next_step_disposition in {"CONTINUE", "REQUEST_MORE_EVIDENCE"}:
                        next_step_disposition = "DEFER"

                if target_disposition == "RECONSIDER":
                    reconsideration = self._reconsideration(
                        request.scenario_id,
                        reason,
                        next_state_ref,
                        update.evidence_update_ref,
                        related_refs,
                    )
                    reconsiderations.append(reconsideration)
                    reconsideration_ref = reconsideration.trace_ref
                    if next_step_disposition == "REPLAN":
                        non_materialized_plan_refs = tuple(
                            ref for ref in request.provisional_plan.candidate_step_refs if ref not in materialized
                        )

                sufficiency.append(
                    GoalSufficiencyCandidateV1(
                        sufficiency_ref=f"sufficiency:{request.scenario_id}:v{index + 1}",
                        goal_ref=request.goal.goal_ref,
                        state_version_ref=next_state_ref,
                        status="INSUFFICIENT",
                        evidence_refs=update.evidence_refs,
                        reason=reason,
                        stop_disposition=next_step_disposition,
                        terminates_remaining_plan=False,
                    )
                )

            state_versions.append(
                CognitiveStateVersionCandidateV1(
                    state_version_ref=next_state_ref,
                    parent_state_version_ref=parent_state_ref,
                    evidence_update_ref=update.evidence_update_ref,
                    current_disposition=target_disposition,
                    current_minimum_need_ref=current_need_ref,
                    active_hypothesis_refs=tuple(active_hypotheses),
                    invalidated_hypothesis_refs=invalidated_refs,
                    sufficiency_ref=sufficiency[-1].sufficiency_ref,
                    reconsideration_ref=reconsideration_ref,
                    trace_ref=f"trace:{request.scenario_id}:state:{index}",
                )
            )
            transitions.append(
                DynamicCognitiveLoopTransitionCandidateV1(
                    transition_ref=f"transition:{request.scenario_id}:{index}",
                    source_state_version_ref=parent_state_ref,
                    target_state_version_ref=next_state_ref,
                    source_disposition=current_disposition,
                    target_disposition=target_disposition,
                    next_step_disposition=next_step_disposition,
                    current_minimum_need_ref=(
                        materialized[-2] if len(materialized) > 1 else request.initial_minimum_need_ref
                    ),
                    selected_next_need_ref=current_need_ref,
                    superseded_requirement_refs=tuple(superseded_requirements),
                    non_materialized_plan_refs=non_materialized_plan_refs,
                    related_refs=related_refs,
                    trace_ref=f"trace:{request.scenario_id}:transition:{index}",
                )
            )
            current_state_ref = next_state_ref
            current_disposition = target_disposition

        if not request.evidence_updates and current_disposition == "INSUFFICIENT":
            next_step_disposition = "DEFER"

        final_state_ref = current_state_ref
        for formation in request.requirements:
            if formation.source_state_version_ref and formation.source_state_version_ref != final_state_ref:
                superseded_requirements.append(formation.requirement_ref)

        stale_requirement_refs = tuple(dict.fromkeys(superseded_requirements))
        stale_set = set(stale_requirement_refs)
        requirement_refs = tuple(formation.requirement_ref for formation in request.requirements)
        resolution_refs = tuple(resolution.requirement_id for resolution in request.resolutions)
        invocation_candidate_refs = tuple(
            invocation.invocation_id for invocation in request.invocations
        )
        eligible_invocations = tuple(
            invocation.invocation_id
            for invocation in request.invocations
            if invocation.accepted and invocation.requirement_ref not in stale_set
        )

        if current_disposition == "SUFFICIENT":
            non_materialized_plan_refs = tuple(
                ref for ref in request.provisional_plan.candidate_step_refs if ref not in materialized
            )

        return DynamicCognitiveLoopOutputV1(
            scenario_id=request.scenario_id,
            goal=request.goal,
            provisional_plan=request.provisional_plan,
            state_versions=tuple(state_versions),
            transitions=tuple(transitions),
            needs_materialized=tuple(materialized),
            current_minimum_need_ref=current_need_ref,
            requirement_refs=requirement_refs,
            resolution_refs=resolution_refs,
            invocation_candidate_refs=invocation_candidate_refs,
            eligible_invocation_refs=eligible_invocations,
            stale_requirement_refs=stale_requirement_refs,
            capability_outcome_refs=tuple(
                assessment.assessment_id for assessment in request.capability_outcomes
            ),
            sufficiency_candidates=tuple(sufficiency),
            reconsiderations=tuple(reconsiderations),
            evidence_update_refs=tuple(accepted_evidence),
            ignored_evidence_update_refs=tuple(ignored_evidence),
            non_materialized_plan_refs=non_materialized_plan_refs,
            final_disposition=current_disposition,
            next_step_disposition=next_step_disposition,
            trace_refs=tuple(
                [state.trace_ref for state in state_versions]
                + [transition.trace_ref for transition in transitions]
            ),
            provenance_refs=tuple(update.evidence_update_ref for update in request.evidence_updates),
        )


__all__ = ["DynamicCognitiveFlowEngineV1", "CANONICAL_OWNER"]
