"""Deterministic Decision Governance engine for synthetic fixtures."""

from __future__ import annotations

from typing import List, Optional, Tuple

from capabilities.midplatform.core.decision_governance.decision_core_types_v1 import (
    DecisionCandidateV1,
    DecisionOptionCandidateV1,
    DecisionSelectionCandidateV1,
    SourceRefV1,
)
from capabilities.midplatform.core.decision_governance.decision_handoff_types_v1 import (
    DecisionToActionTaskHandoffCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_io_types_v1 import (
    DecisionGovernanceInputV1,
    DecisionGovernanceOutputV1,
)
from capabilities.midplatform.core.decision_governance.decision_registry_v1 import (
    ACTION_CONSUMER_OWNER,
    DECISION_OWNER,
    TASK_CONSUMER_OWNER,
)
from capabilities.midplatform.core.decision_governance.decision_state_types_v1 import (
    DecisionStateTransitionCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_trace_types_v1 import (
    DecisionTraceCandidateV1,
)


class DecisionGovernanceEngineV1:
    def _mk_ref(
        self, owner: str, ref_id: str, ref_type: str = "REFERENCE"
    ) -> SourceRefV1:
        return SourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)

    def _risk_score(self, option: DecisionOptionCandidateV1) -> int:
        return option.risk.severity * option.risk.likelihood

    def _utility_score(
        self, request: DecisionGovernanceInputV1, option: DecisionOptionCandidateV1
    ) -> int:
        preference_boost = (
            8 if option.option_id in request.intent_preferred_option_ids else 0
        )
        adjusted = (
            option.utility.expected_benefit
            + (option.intent_alignment * 3)
            + preference_boost
        )
        if request.resource_pressure_level == "DEGRADED":
            adjusted -= option.cost * 5
        elif request.resource_pressure_level == "CRITICAL":
            adjusted -= option.cost * 8
        return adjusted

    def _veto_reasons(self, option: DecisionOptionCandidateV1) -> Tuple[str, ...]:
        reasons: List[str] = []
        if not option.hard_constraints_ok:
            reasons.append("hard_constraint_veto")
        if not option.permission_allowed:
            reasons.append("permission_veto")
        if not option.safety_allowed:
            reasons.append("safety_veto")
        if not option.role_allowed:
            reasons.append("role_scope_veto")
        if not option.evidence_ready:
            reasons.append("evidence_not_ready")
        return tuple(reasons)

    def _candidate_state(self, eligible: bool, veto_reasons: Tuple[str, ...]) -> str:
        if eligible:
            return "ELIGIBLE"
        if veto_reasons:
            return "CONSTRAINED"
        return "REJECTED"

    def _build_candidates(
        self, request: DecisionGovernanceInputV1
    ) -> Tuple[DecisionCandidateV1, ...]:
        items: List[DecisionCandidateV1] = []
        for idx, option in enumerate(request.options, start=1):
            risk_score = self._risk_score(option)
            utility_score = self._utility_score(request, option)
            veto = self._veto_reasons(option)
            eligible = len(veto) == 0
            confirmation = "NO_CONFIRMATION_REQUIRED"
            if option.reversibility == "IRREVERSIBLE":
                confirmation = "CONFIRMATION_REQUIRED"

            items.append(
                DecisionCandidateV1(
                    decision_candidate_id=f"decision:{request.scenario_id}:{idx}",
                    owner=DECISION_OWNER,
                    candidate_kind="DECISION_CANDIDATE",
                    option_id=option.option_id,
                    decision_state=self._candidate_state(eligible, veto),
                    utility_score_candidate=utility_score,
                    risk_score_candidate=risk_score,
                    constraint_refs=request.constraint_refs,
                    permission_refs=request.permission_refs,
                    safety_refs=request.safety_refs,
                    resource_refs=request.resource_refs,
                    uncertainty_unknowns=(
                        "confidence_not_truth",
                        *(
                            ()
                            if request.causal_uncertainty_level == "LOW"
                            else ("causal_uncertainty",)
                        ),
                    ),
                    reversibility=option.reversibility,
                    confirmation_requirement=confirmation,
                    eligibility_candidate=eligible,
                    veto_reasons=veto,
                    provenance=(
                        self._mk_ref(
                            DECISION_OWNER,
                            f"prov:{request.scenario_id}:{option.option_id}",
                            "PROVENANCE",
                        ),
                    ),
                    trace_ref=f"trace:{request.scenario_id}",
                    revision_lineage=(
                        f"lineage:{request.scenario_id}:{option.option_id}",
                    ),
                    decision_authority=True,
                    action_authority=False,
                    task_authority=False,
                )
            )
        return tuple(items)

    def _choose_best(
        self, candidates: Tuple[DecisionCandidateV1, ...]
    ) -> Optional[DecisionCandidateV1]:
        eligible = [item for item in candidates if item.eligibility_candidate]
        if not eligible:
            return None
        eligible.sort(
            key=lambda c: (
                c.utility_score_candidate - (c.risk_score_candidate * 4),
                -c.risk_score_candidate,
                c.option_id,
            ),
            reverse=True,
        )
        return eligible[0]

    def _derive_outcome(
        self,
        request: DecisionGovernanceInputV1,
        candidates: Tuple[DecisionCandidateV1, ...],
    ) -> Tuple[str, str, DecisionSelectionCandidateV1, bool]:
        if len(request.evidence_refs) == 0:
            return (
                "NEEDS_MORE_EVIDENCE",
                "REQUEST_MORE_EVIDENCE",
                DecisionSelectionCandidateV1(
                    selected_candidate_ref=None,
                    preferred_candidate_ref=None,
                    rejected_candidate_refs=tuple(
                        c.decision_candidate_id for c in candidates
                    ),
                    defer_reason=None,
                    abstain_reason=None,
                    request_more_evidence_reason="insufficient_evidence_refs",
                    contested=False,
                    confirmation_requirement="NO_CONFIRMATION_REQUIRED",
                    execution_eligibility_candidate=False,
                ),
                False,
            )

        if request.causal_uncertainty_level == "HIGH":
            return (
                "DEFERRED",
                "DEFER",
                DecisionSelectionCandidateV1(
                    selected_candidate_ref=None,
                    preferred_candidate_ref=None,
                    rejected_candidate_refs=tuple(
                        c.decision_candidate_id for c in candidates
                    ),
                    defer_reason="causal_uncertainty_high",
                    abstain_reason=None,
                    request_more_evidence_reason=None,
                    contested=False,
                    confirmation_requirement="NO_CONFIRMATION_REQUIRED",
                    execution_eligibility_candidate=False,
                ),
                False,
            )

        eligible = [c for c in candidates if c.eligibility_candidate]
        blocked = [c for c in candidates if not c.eligibility_candidate]

        if request.competing_causal_hypotheses and len(eligible) > 1:
            return (
                "CONTESTED",
                "CONTESTED",
                DecisionSelectionCandidateV1(
                    selected_candidate_ref=None,
                    preferred_candidate_ref=None,
                    rejected_candidate_refs=tuple(
                        c.decision_candidate_id for c in blocked
                    ),
                    defer_reason="competing_hypotheses_unresolved",
                    abstain_reason=None,
                    request_more_evidence_reason=None,
                    contested=True,
                    confirmation_requirement="NO_CONFIRMATION_REQUIRED",
                    execution_eligibility_candidate=False,
                ),
                False,
            )

        best = self._choose_best(candidates)
        if best is None:
            hard_only = all("hard_constraint_veto" in c.veto_reasons for c in blocked)
            if hard_only:
                return (
                    "ABSTAINED",
                    "ABSTAIN",
                    DecisionSelectionCandidateV1(
                        selected_candidate_ref=None,
                        preferred_candidate_ref=None,
                        rejected_candidate_refs=tuple(
                            c.decision_candidate_id for c in blocked
                        ),
                        defer_reason=None,
                        abstain_reason="no_acceptable_option_under_hard_constraints",
                        request_more_evidence_reason=None,
                        contested=False,
                        confirmation_requirement="NO_CONFIRMATION_REQUIRED",
                        execution_eligibility_candidate=False,
                    ),
                    False,
                )
            return (
                "CONSTRAINED",
                "CONSTRAINED",
                DecisionSelectionCandidateV1(
                    selected_candidate_ref=None,
                    preferred_candidate_ref=None,
                    rejected_candidate_refs=tuple(
                        c.decision_candidate_id for c in blocked
                    ),
                    defer_reason=None,
                    abstain_reason="blocked_by_permission_or_safety_or_role",
                    request_more_evidence_reason=None,
                    contested=False,
                    confirmation_requirement="NO_CONFIRMATION_REQUIRED",
                    execution_eligibility_candidate=False,
                ),
                False,
            )

        pref = (
            best.decision_candidate_id
            if best.option_id in request.intent_preferred_option_ids
            else None
        )
        constrained = any(
            c.veto_reasons
            for c in candidates
            if c.decision_candidate_id != best.decision_candidate_id
        )

        if (
            best.reversibility == "IRREVERSIBLE"
            and not request.human_confirmation_available
        ):
            return (
                "NEEDS_CONFIRMATION",
                "CONFIRMATION_REQUIRED",
                DecisionSelectionCandidateV1(
                    selected_candidate_ref=best.decision_candidate_id,
                    preferred_candidate_ref=pref,
                    rejected_candidate_refs=tuple(
                        c.decision_candidate_id
                        for c in candidates
                        if c.decision_candidate_id != best.decision_candidate_id
                    ),
                    defer_reason=None,
                    abstain_reason=None,
                    request_more_evidence_reason=None,
                    contested=False,
                    confirmation_requirement="CONFIRMATION_REQUIRED",
                    execution_eligibility_candidate=False,
                ),
                False,
            )

        state = "ELIGIBLE"
        outcome = "ELIGIBLE"
        if constrained:
            state = "CONSTRAINED"
            outcome = "CONSTRAINED"
        # Auto-select only for explicit handoff or high-confidence low-risk singles.
        auto_selectable_single = (
            len(eligible) == 1
            and not constrained
            and best.reversibility != "IRREVERSIBLE"
            and best.risk_score_candidate <= 1
            and best.utility_score_candidate >= 85
        )
        if request.scenario_id.endswith("__HANDOFF") or auto_selectable_single:
            state = "SELECTED_CANDIDATE"
            outcome = "SELECTED"

        return (
            state,
            outcome,
            DecisionSelectionCandidateV1(
                selected_candidate_ref=best.decision_candidate_id,
                preferred_candidate_ref=pref,
                rejected_candidate_refs=tuple(
                    c.decision_candidate_id
                    for c in candidates
                    if c.decision_candidate_id != best.decision_candidate_id
                ),
                defer_reason=None,
                abstain_reason=None,
                request_more_evidence_reason=None,
                contested=False,
                confirmation_requirement=(
                    "NO_CONFIRMATION_REQUIRED"
                    if best.reversibility != "IRREVERSIBLE"
                    else "CONFIRMATION_REQUIRED"
                ),
                execution_eligibility_candidate=True,
            ),
            True,
        )

    def _build_transition(
        self,
        request: DecisionGovernanceInputV1,
        state: str,
        selected_candidate_ref: Optional[str],
    ) -> Tuple[DecisionStateTransitionCandidateV1, ...]:
        target = selected_candidate_ref or f"decision:{request.scenario_id}:none"
        return (
            DecisionStateTransitionCandidateV1(
                decision_candidate_id=target,
                from_state="PROPOSED",
                to_state=state,
                reason_candidate=f"deterministic_outcome:{state.lower()}",
                constraint_refs=tuple(item.ref_id for item in request.constraint_refs),
                permission_refs=tuple(item.ref_id for item in request.permission_refs),
                safety_refs=tuple(item.ref_id for item in request.safety_refs),
                provenance_ref=f"prov:{request.scenario_id}:transition",
            ),
        )

    def _build_trace(
        self,
        request: DecisionGovernanceInputV1,
        candidates: Tuple[DecisionCandidateV1, ...],
        state: str,
    ) -> DecisionTraceCandidateV1:
        rejected = tuple(c.option_id for c in candidates if not c.eligibility_candidate)
        selection_reasons = (f"reason:{request.scenario_id}:{state.lower()}",)
        return DecisionTraceCandidateV1(
            trace_id=f"trace:{request.scenario_id}",
            owner=DECISION_OWNER,
            decision_candidate_refs=tuple(c.decision_candidate_id for c in candidates),
            intent_refs=tuple(ref.ref_id for ref in request.intent_refs),
            causal_refs=tuple(ref.ref_id for ref in request.causal_refs),
            evidence_refs=tuple(ref.ref_id for ref in request.evidence_refs),
            constraint_refs=tuple(ref.ref_id for ref in request.constraint_refs),
            risk_refs=tuple(c.risk.risk_ref_id for c in request.options),
            utility_refs=tuple(c.utility.utility_ref_id for c in request.options),
            permission_refs=tuple(ref.ref_id for ref in request.permission_refs),
            safety_refs=tuple(ref.ref_id for ref in request.safety_refs),
            resource_state_refs=tuple(ref.ref_id for ref in request.resource_refs),
            alternative_option_refs=tuple(opt.option_id for opt in request.options),
            rejected_alternative_refs=rejected,
            selection_or_nonselection_reason_refs=selection_reasons,
            state_transition_refs=(
                f"transition:{request.scenario_id}:{state.lower()}",
            ),
            revision_lineage_refs=tuple(
                lineage for cand in candidates for lineage in cand.revision_lineage
            ),
            provenance=(
                f"prov:{request.scenario_id}:admission",
                f"prov:{request.scenario_id}:formation",
                f"prov:{request.scenario_id}:selection",
            ),
            candidate_only=True,
        )

    def _build_handoff(
        self,
        request: DecisionGovernanceInputV1,
        candidates: Tuple[DecisionCandidateV1, ...],
        selection: DecisionSelectionCandidateV1,
    ) -> DecisionToActionTaskHandoffCandidateV1:
        return DecisionToActionTaskHandoffCandidateV1(
            handoff_id=f"handoff:{request.scenario_id}",
            producer_owner=DECISION_OWNER,
            consumer_owners=(ACTION_CONSUMER_OWNER, TASK_CONSUMER_OWNER),
            handoff_kind="DECISION_TO_ACTION_TASK_HANDOFF_CANDIDATE",
            decision_candidate_refs=tuple(c.decision_candidate_id for c in candidates),
            selected_candidate_ref=selection.selected_candidate_ref,
            option_refs=tuple(opt.option_id for opt in request.options),
            constraint_refs=tuple(ref.ref_id for ref in request.constraint_refs),
            permission_status_refs=tuple(ref.ref_id for ref in request.permission_refs),
            safety_status_refs=tuple(ref.ref_id for ref in request.safety_refs),
            uncertainty=tuple(
                cand for c in candidates for cand in c.uncertainty_unknowns
            ),
            provenance=(f"prov:{request.scenario_id}:handoff",),
            confirmation_requirement=selection.confirmation_requirement,
            execution_eligibility_candidate=selection.execution_eligibility_candidate,
            candidate_only=True,
            decision_executed=False,
            action_triggered=False,
            task_created=False,
        )

    def run_case(
        self, request: DecisionGovernanceInputV1
    ) -> DecisionGovernanceOutputV1:
        candidates = self._build_candidates(request)
        state, outcome_kind, selection, handoff_eligible = self._derive_outcome(
            request, candidates
        )

        if not handoff_eligible:
            selection = DecisionSelectionCandidateV1(
                selected_candidate_ref=selection.selected_candidate_ref,
                preferred_candidate_ref=selection.preferred_candidate_ref,
                rejected_candidate_refs=selection.rejected_candidate_refs,
                defer_reason=selection.defer_reason,
                abstain_reason=selection.abstain_reason,
                request_more_evidence_reason=selection.request_more_evidence_reason,
                contested=selection.contested,
                confirmation_requirement=selection.confirmation_requirement,
                execution_eligibility_candidate=False,
            )

        transitions = self._build_transition(
            request, state, selection.selected_candidate_ref
        )
        trace = self._build_trace(request, candidates, state)
        handoff = self._build_handoff(request, candidates, selection)

        return DecisionGovernanceOutputV1(
            scenario_id=request.scenario_id,
            state=state,
            outcome_kind=outcome_kind,
            decision_candidates=candidates,
            selection_candidate=selection,
            transitions=transitions,
            trace_candidate=trace,
            handoff_candidate=handoff,
            candidate_only=True,
            decision_output=False,
            action_output=False,
            task_output=False,
            runtime_executed=False,
            database_write_executed=False,
            source_mutation_executed=False,
            fabricated_confirmation=False,
        )
