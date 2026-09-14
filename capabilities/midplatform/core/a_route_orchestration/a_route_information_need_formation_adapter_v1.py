"""Minimal state-sensitive Information Need formation for A-Route."""

from __future__ import annotations

import hashlib
from typing import Iterable, Tuple

from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_types_v1 import (
    CognitiveNeedCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_governance_v1 import (
    validate_cognitive_need,
)

from .a_route_information_need_formation_types_v1 import (
    ARouteInformationNeedFormationRequestV1,
    ARouteInformationNeedFormationResultV1,
    FORMATION_OWNER,
    NEED_FORMED,
    NO_ACTIVE_NEED,
    REJECTED,
)


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))


class ARouteInformationNeedFormationAdapterV1:
    """Forms a candidate from required conditions minus current coverage.

    The adapter deliberately does not parse Goal/Role/Context strings.  Goal
    semantics arrive through the existing ``GoalContextV1`` success-condition
    contract, while role/objective deltas are accepted only as explicit
    governed condition signals.  The operation is read-only and candidate-only.
    """

    @staticmethod
    def _digest(request: ARouteInformationNeedFormationRequestV1, unknown: Tuple[str, ...]) -> str:
        stable_parts = (
            request.goal_context.goal_ref,
            request.intent_ref or "",
            request.concern_ref or "",
            request.field_ref or "",
            request.current_world.current_world_id,
            *request.governed_role_condition_refs,
            *unknown,
        )
        return hashlib.sha256("|".join(stable_parts).encode("utf-8")).hexdigest()[:24]

    def form(
        self, request: ARouteInformationNeedFormationRequestV1
    ) -> ARouteInformationNeedFormationResultV1:
        world = request.current_world
        trace_ref = request.formation_trace_ref or (
            f"trace:a-route:information-need-formation:{world.current_world_id}"
        )
        required = _unique(
            (
                *request.goal_context.success_condition_refs,
                *request.governed_objective_condition_refs,
                *request.governed_role_condition_refs,
            )
        )
        coverage = set(_unique(request.current_cognitive_coverage_refs))
        unknown = tuple(ref for ref in required if ref not in coverage)
        common = dict(
            owner_ref=FORMATION_OWNER,
            goal_ref=request.goal_context.goal_ref,
            intent_ref=request.intent_ref,
            concern_ref=request.concern_ref,
            task_ref=request.task_ref,
            context_ref=request.context_ref,
            field_ref=request.field_ref,
            role_refs=tuple(request.role_refs),
            current_world_ref=world.current_world_id,
            current_world_trace_ref=world.trace_ref,
            required_cognitive_condition_refs=required,
            current_cognitive_coverage_refs=tuple(ref for ref in request.current_cognitive_coverage_refs if ref),
            necessary_unknown_refs=unknown,
            trace_ref=trace_ref,
            provenance_refs=(
                "provenance:a-route-information-need-formation:v1",
                request.goal_context.trace,
                world.trace_ref,
                *world.provenance_refs,
            ),
        )
        if not request.candidate_only or not world.candidate_only:
            return ARouteInformationNeedFormationResultV1(
                status=REJECTED,
                need=None,
                **common,
                candidate_only=False,
            )
        if world.field_mutation or world.field_truth_declaration or world.reducer_invocation_as_mutation_authority:
            return ARouteInformationNeedFormationResultV1(status=REJECTED, need=None, **common)
        if not unknown:
            return ARouteInformationNeedFormationResultV1(
                status=NO_ACTIVE_NEED,
                need=None,
                **common,
            )

        digest = self._digest(request, unknown)
        need = CognitiveNeedCandidateV1(
            need_id=f"cognitive-need:formed:{digest}",
            source_intent_ref=request.intent_ref,
            source_context_ref=request.context_ref,
            source_field_ref=request.field_ref,
            source_hypothesis_ref=request.hypothesis_ref,
            source_attention_ref=request.attention_ref,
            problem_description=(
                "the current cognitive state does not cover all governed "
                "conditions required by the active objective"
            ),
            missing_information_class="NECESSARY_COGNITIVE_CONDITION",
            required_evidence_class="EVIDENCE_FOR_REQUIRED_COGNITIVE_CONDITION",
            urgency=request.urgency,
            safety_relevance=request.safety_relevance,
            trace_ref=trace_ref,
            state_version_ref=world.current_world_id,
        )
        validation_errors = validate_cognitive_need(need)
        if validation_errors:
            return ARouteInformationNeedFormationResultV1(
                status=REJECTED,
                need=None,
                **common,
            )
        return ARouteInformationNeedFormationResultV1(
            status=NEED_FORMED,
            need=need,
            **common,
        )


__all__ = [
    "ARouteInformationNeedFormationAdapterV1",
    "ARouteInformationNeedFormationRequestV1",
    "ARouteInformationNeedFormationResultV1",
]
