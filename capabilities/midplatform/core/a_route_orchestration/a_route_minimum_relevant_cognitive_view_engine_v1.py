"""Common, deterministic Self/External minimum-view selection for A-Route."""

from __future__ import annotations

import hashlib
from typing import Iterable, Tuple

from .a_route_minimum_relevant_cognitive_view_types_v1 import (
    ARouteMinimumRelevantCognitiveViewCandidateV1,
    ARouteMinimumRelevantCognitiveViewRequestV1,
    EXTERNAL_INFORMATION,
    NO_ACTIVE_RELEVANT_VIEW,
    REJECTED,
    SELF_INFORMATION,
    VIEW_FORMED,
    VIEW_OWNER,
)


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


class ARouteMinimumRelevantCognitiveViewEngineV1:
    """Selects information by declared condition coverage, not by object type."""

    @staticmethod
    def _digest(
        request: ARouteMinimumRelevantCognitiveViewRequestV1,
        selected: Tuple[str, ...],
        active_conditions: Tuple[str, ...],
    ) -> str:
        # Excluded items are intentionally absent: irrelevant additions must not
        # change the identity of the selected minimum view.
        parts = (
            request.goal_context.goal_ref,
            *active_conditions,
            *selected,
        )
        return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:24]

    @staticmethod
    def _invalid_request(
        request: ARouteMinimumRelevantCognitiveViewRequestV1,
        errors: Tuple[str, ...],
    ) -> ARouteMinimumRelevantCognitiveViewCandidateV1:
        view_ref = f"view:rejected:{request.goal_context.goal_ref}"
        return ARouteMinimumRelevantCognitiveViewCandidateV1(
            view_ref=view_ref,
            owner_ref=VIEW_OWNER,
            status=REJECTED,
            goal_ref=request.goal_context.goal_ref,
            intent_ref=request.intent_ref,
            concern_ref=request.concern_ref,
            context_ref=request.context_ref,
            field_ref=request.field_ref,
            role_refs=request.role_refs,
            current_world_ref=request.current_world_ref,
            current_cognitive_state_ref=request.current_cognitive_state_ref,
            active_condition_refs=(),
            selected_information_refs=(),
            selected_self_information_refs=(),
            selected_external_information_refs=(),
            excluded_information_refs=tuple(item.information_ref for item in request.available_information),
            recoverable_information_refs=tuple(
                item.information_ref
                for item in request.available_information
                if item.recoverable
            ),
            current_cognitive_coverage_refs=(),
            selected_source_refs=(),
            selected_provenance_refs=(),
            trace_ref=f"trace:a-route:minimum-relevant-cognitive-view:rejected:{request.goal_context.goal_ref}",
            provenance_refs=("provenance:a-route-minimum-relevant-cognitive-view:v1",),
            validation_errors=errors,
        )

    def form(
        self,
        request: ARouteMinimumRelevantCognitiveViewRequestV1,
    ) -> ARouteMinimumRelevantCognitiveViewCandidateV1:
        errors = []
        if not request.candidate_only:
            errors.append("view_request_not_candidate_only")
        refs = tuple(item.information_ref for item in request.available_information)
        if len(set(refs)) != len(refs):
            errors.append("duplicate_available_information_ref")
        if errors:
            return self._invalid_request(request, tuple(errors))

        active_conditions = _unique(
            (
                *request.goal_context.success_condition_refs,
                *request.governed_objective_condition_refs,
                *request.governed_role_condition_refs,
                *request.governed_intent_condition_refs,
                *request.governed_concern_condition_refs,
                *request.governed_context_condition_refs,
            )
        )
        active = set(active_conditions)
        selected_items = tuple(
            item
            for item in request.available_information
            if active.intersection(item.support_condition_refs)
        )
        excluded_items = tuple(
            item
            for item in request.available_information
            if item not in selected_items
        )
        selected = tuple(item.information_ref for item in selected_items)
        excluded = tuple(item.information_ref for item in excluded_items)
        recoverable = tuple(item.information_ref for item in excluded_items if item.recoverable)
        selected_self = tuple(
            item.information_ref
            for item in selected_items
            if item.object_type == SELF_INFORMATION
        )
        selected_external = tuple(
            item.information_ref
            for item in selected_items
            if item.object_type == EXTERNAL_INFORMATION
        )
        selected_sources = _unique(
            ref for item in selected_items for ref in item.source_refs
        )
        selected_provenance = _unique(
            ref for item in selected_items for ref in item.provenance_refs
        )
        digest = self._digest(request, selected, active_conditions)
        view_ref = f"minimum-relevant-cognitive-view:{digest}"
        trace_ref = f"trace:a-route:minimum-relevant-cognitive-view:{digest}"
        status = VIEW_FORMED if selected_items else NO_ACTIVE_RELEVANT_VIEW
        return ARouteMinimumRelevantCognitiveViewCandidateV1(
            view_ref=view_ref,
            owner_ref=VIEW_OWNER,
            status=status,
            goal_ref=request.goal_context.goal_ref,
            intent_ref=request.intent_ref,
            concern_ref=request.concern_ref,
            context_ref=request.context_ref,
            field_ref=request.field_ref,
            role_refs=request.role_refs,
            current_world_ref=request.current_world_ref,
            current_cognitive_state_ref=request.current_cognitive_state_ref,
            active_condition_refs=active_conditions,
            selected_information_refs=selected,
            selected_self_information_refs=selected_self,
            selected_external_information_refs=selected_external,
            excluded_information_refs=excluded,
            recoverable_information_refs=recoverable,
            current_cognitive_coverage_refs=selected,
            selected_source_refs=selected_sources,
            selected_provenance_refs=selected_provenance,
            trace_ref=trace_ref,
            provenance_refs=(
                "provenance:a-route-minimum-relevant-cognitive-view:v1",
                request.goal_context.trace,
                *selected_provenance,
            ),
        )


__all__ = ["ARouteMinimumRelevantCognitiveViewEngineV1"]
