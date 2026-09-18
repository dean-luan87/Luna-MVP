"""Governed, state-sensitive Required Cognitive Condition formation."""

from __future__ import annotations

import hashlib
from dataclasses import replace
from typing import Iterable, Tuple

from .a_route_required_cognitive_condition_formation_types_v1 import (
    ACTIVE_REQUIRED,
    CONDITIONS_FORMED,
    DORMANT,
    FORMATION_OWNER,
    NO_ACTIVE_REQUIRED_CONDITIONS,
    REJECTED,
    ARouteRequiredCognitiveConditionFormationRequestV1,
    ARouteRequiredCognitiveConditionFormationResultV1,
    RequiredCognitiveConditionCandidateV1,
)


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


class ARouteRequiredCognitiveConditionFormationEngineV1:
    """Forms a minimum required set from governed rules and situation signals.

    The engine performs only exact reference-set operations supplied by
    governance: objective applicability, activation, suppression,
    satisfaction, and minimum-set choice.  It never parses semantic strings.
    """

    @staticmethod
    def _digest(
        request: ARouteRequiredCognitiveConditionFormationRequestV1,
        selected: Tuple[str, ...],
    ) -> str:
        parts = (
            request.goal_context.goal_ref,
            request.intent_ref or "",
            request.concern_ref or "",
            *selected,
        )
        return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:24]

    @staticmethod
    def _rule_applies(
        rule,
        objective_refs: set[str],
        situation_refs: set[str],
    ) -> tuple[str, str, Tuple[str, ...], str, Tuple[str, ...]]:
        if not objective_refs.intersection(rule.objective_refs):
            return DORMANT, "objective_not_active", (), "UNSATISFIED", ()
        if not set(rule.activation_all_refs).issubset(situation_refs):
            return DORMANT, "activation_all_not_satisfied", (), "UNSATISFIED", ()
        if rule.activation_any_refs and not set(rule.activation_any_refs).intersection(situation_refs):
            return DORMANT, "activation_any_not_satisfied", (), "UNSATISFIED", ()
        if set(rule.suppress_if_any_refs).intersection(situation_refs):
            return DORMANT, "suppressed_by_current_situation", (), "UNSATISFIED", ()
        if rule.alternative_satisfaction_basis_refs:
            matched_satisfaction_refs = tuple(
                ref
                for ref in rule.alternative_satisfaction_basis_refs
                if ref in situation_refs
            )
            satisfaction_status = "SATISFIED" if matched_satisfaction_refs else "UNSATISFIED"
            actual_satisfaction_coverage_refs = (
                matched_satisfaction_refs[:1] if matched_satisfaction_refs else ()
            )
        else:
            legacy_covered = (
                bool(rule.satisfaction_coverage_refs)
                and set(rule.satisfaction_coverage_refs).issubset(situation_refs)
            )
            satisfaction_status = "SATISFIED" if legacy_covered else "UNSATISFIED"
            actual_satisfaction_coverage_refs = (
                tuple(ref for ref in rule.satisfaction_coverage_refs if ref in situation_refs)
                if legacy_covered
                else ()
            )
        conditioning = _unique(
            (
                *rule.activation_all_refs,
                *(ref for ref in rule.activation_any_refs if ref in situation_refs),
                *(ref for ref in rule.suppress_if_any_refs if ref in situation_refs),
            )
        )
        reason = (
            "currently_required_and_covered_by_current_cognitive_situation"
            if satisfaction_status == "SATISFIED"
            else "currently_required_by_governed_objective_rule"
        )
        return (
            ACTIVE_REQUIRED,
            reason,
            conditioning,
            satisfaction_status,
            actual_satisfaction_coverage_refs,
        )

    def form(
        self,
        request: ARouteRequiredCognitiveConditionFormationRequestV1,
    ) -> ARouteRequiredCognitiveConditionFormationResultV1:
        situation_refs = request.current_situation.governed_refs()
        situation = set(situation_refs)
        objective_refs = set(
            _unique(
                (
                    request.goal_context.goal_ref,
                    request.intent_ref or "",
                    request.concern_ref or "",
                )
            )
        )
        trace_ref = request.formation_trace_ref or (
            f"trace:a-route:required-cognitive-condition-formation:{request.goal_context.goal_ref}"
        )
        if not request.candidate_only:
            return ARouteRequiredCognitiveConditionFormationResultV1(
                status=REJECTED,
                owner_ref=FORMATION_OWNER,
                goal_ref=request.goal_context.goal_ref,
                intent_ref=request.intent_ref,
                concern_ref=request.concern_ref,
                context_ref=request.context_ref,
                field_ref=request.field_ref,
                role_refs=tuple(request.role_refs),
                active_required_condition_refs=(),
                satisfied_condition_refs=(),
                dormant_condition_refs=(),
                candidates=(),
                current_situation_refs=situation_refs,
                trace_ref=trace_ref,
                provenance_refs=(
                    "provenance:a-route-required-cognitive-condition-formation:v1",
                    request.goal_context.trace,
                ),
                candidate_only=False,
            )
        candidates = []
        eligible = []
        for rule in request.governed_condition_rules:
            (
                status,
                reason,
                conditioning,
                satisfaction_status,
                actual_satisfaction_coverage_refs,
            ) = self._rule_applies(rule, objective_refs, situation)
            candidate = RequiredCognitiveConditionCandidateV1(
                condition_ref=rule.condition_ref,
                source_objective_refs=_unique(rule.objective_refs),
                conditioning_refs=conditioning,
                status=status,
                reason=reason,
                rule_ref=rule.rule_ref,
                satisfaction_status=satisfaction_status,
                satisfaction_coverage_refs=_unique(actual_satisfaction_coverage_refs),
                source_refs=_unique(rule.source_refs),
                provenance_refs=_unique(rule.provenance_refs),
                current_situation_refs=situation_refs,
            )
            candidates.append(candidate)
            if status == ACTIVE_REQUIRED:
                eligible.append((rule, candidate))

        selected = []
        grouped: dict[str, list[tuple[object, RequiredCognitiveConditionCandidateV1]]] = {}
        for rule, candidate in eligible:
            grouped.setdefault(rule.minimum_set_ref or rule.condition_ref, []).append((rule, candidate))
        for group in grouped.values():
            chosen_rule, chosen_candidate = min(
                group,
                key=lambda item: (item[0].selection_rank, item[1].condition_ref),
            )
            selected.append(chosen_candidate.condition_ref)

        selected_refs = _unique(selected)
        selected_set = set(selected_refs)
        candidates = tuple(
            replace(
                candidate,
                status=DORMANT,
                reason="minimum_set_alternative_not_selected",
            )
            if candidate.status == ACTIVE_REQUIRED and candidate.condition_ref not in selected_set
            else candidate
            for candidate in candidates
        )
        status = CONDITIONS_FORMED if selected_refs else NO_ACTIVE_REQUIRED_CONDITIONS
        dormant_refs = _unique(
            candidate.condition_ref
            for candidate in candidates
            if candidate.status == DORMANT
        )
        satisfied_refs = _unique(
            candidate.condition_ref
            for candidate in candidates
            if candidate.status == ACTIVE_REQUIRED
            and candidate.condition_ref in selected_set
            and candidate.satisfaction_status == "SATISFIED"
        )
        digest = self._digest(request, selected_refs)
        provenance = _unique(
            (
                "provenance:a-route-required-cognitive-condition-formation:v1",
                request.goal_context.trace,
                *(str(value) for value in request.goal_context.provenance.values()),
                *(ref for rule in request.governed_condition_rules for ref in rule.provenance_refs),
            )
        )
        return ARouteRequiredCognitiveConditionFormationResultV1(
            status=status,
            owner_ref=FORMATION_OWNER,
            goal_ref=request.goal_context.goal_ref,
            intent_ref=request.intent_ref,
            concern_ref=request.concern_ref,
            context_ref=request.context_ref,
            field_ref=request.field_ref,
            role_refs=tuple(request.role_refs),
            active_required_condition_refs=selected_refs,
            satisfied_condition_refs=satisfied_refs,
            dormant_condition_refs=dormant_refs,
            candidates=candidates,
            current_situation_refs=situation_refs,
            trace_ref=f"{trace_ref}:{digest}",
            provenance_refs=provenance,
        )


__all__ = ["ARouteRequiredCognitiveConditionFormationEngineV1"]
