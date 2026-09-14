"""Deterministic Causal Governance engine for synthetic fixtures."""

from __future__ import annotations

from typing import List, Tuple

from capabilities.midplatform.core.causal_governance.causal_confounder_types_v1 import (
    ConfounderCandidateV1,
)
from capabilities.midplatform.core.causal_governance.causal_core_types_v1 import (
    CausalHypothesisCandidateV1,
    SourceRefV1,
    UncertaintyEnvelopeV1,
)
from capabilities.midplatform.core.causal_governance.causal_counterfactual_types_v1 import (
    CounterfactualCandidateV1,
)
from capabilities.midplatform.core.causal_governance.causal_evidence_types_v1 import (
    CausalEvidenceRelationCandidateV1,
)
from capabilities.midplatform.core.causal_governance.causal_handoff_types_v1 import (
    CausalToDecisionHandoffCandidateV1,
)
from capabilities.midplatform.core.causal_governance.causal_io_types_v1 import (
    CausalGovernanceInputV1,
    CausalGovernanceOutputV1,
)
from capabilities.midplatform.core.causal_governance.causal_registry_v1 import (
    CAUSAL_OWNER,
    DECISION_CONSUMER_OWNER,
)
from capabilities.midplatform.core.causal_governance.causal_state_types_v1 import (
    StateTransitionCandidateV1,
)
from capabilities.midplatform.core.causal_governance.causal_trace_types_v1 import (
    CausalTraceCandidateV1,
)


class CausalGovernanceEngineV1:
    def _mk_ref(
        self, owner: str, ref_id: str, ref_type: str = "REFERENCE"
    ) -> SourceRefV1:
        return SourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)

    def _derive_state(self, request: CausalGovernanceInputV1) -> str:
        sid = request.scenario_id
        support = len(request.supporting_evidence_refs)
        oppose = len(request.opposing_evidence_refs)
        has_confounder = bool(request.confounder_refs)
        multi = len(request.hypothesis_candidates) > 1

        if "REVOKED" in sid:
            return "REVOKED"
        if "REVISION" in sid:
            return "REVISED"
        if support == 0:
            return "INSUFFICIENT_EVIDENCE"
        if "TEMPORAL_PRECEDENCE" in sid:
            return "INSUFFICIENT_EVIDENCE"
        if multi or oppose >= support or has_confounder:
            return "CONTESTED"
        if support > oppose:
            return "SUPPORTED"
        return "PROPOSED"

    def _build_uncertainty(
        self, request: CausalGovernanceInputV1, state: str
    ) -> UncertaintyEnvelopeV1:
        conflict = tuple(
            f"conflict:{request.scenario_id}:{idx}"
            for idx, _ in enumerate(request.hypothesis_candidates[1:], start=1)
        )
        confidence = "LOW"
        if state == "SUPPORTED":
            confidence = "MEDIUM"
        elif state in {"REVISED", "REVOKED"}:
            confidence = "LOW"
        return UncertaintyEnvelopeV1(
            unknowns=request.unknowns,
            confidence_candidate=confidence,
            confidence_not_truth=True,
            unresolved_conflicts=conflict,
            insufficient_evidence_flag=state in {"INSUFFICIENT_EVIDENCE", "SUSPENDED"},
        )

    def _build_evidence_relations(
        self,
        request: CausalGovernanceInputV1,
        hypothesis_id: str,
    ) -> Tuple[CausalEvidenceRelationCandidateV1, ...]:
        items: List[CausalEvidenceRelationCandidateV1] = []
        for ref in request.supporting_evidence_refs:
            items.append(
                CausalEvidenceRelationCandidateV1(
                    relation_id=f"relation:{hypothesis_id}:{ref.ref_id}:support",
                    hypothesis_ref=hypothesis_id,
                    evidence_ref=ref.ref_id,
                    relation_type="SUPPORT",
                    confidence_candidate="MEDIUM",
                    temporal_validity_ref=request.temporal_order_refs[0].ref_id,
                    provenance=f"prov:{request.scenario_id}:support",
                )
            )
        for ref in request.opposing_evidence_refs:
            items.append(
                CausalEvidenceRelationCandidateV1(
                    relation_id=f"relation:{hypothesis_id}:{ref.ref_id}:opposition",
                    hypothesis_ref=hypothesis_id,
                    evidence_ref=ref.ref_id,
                    relation_type="OPPOSITION",
                    confidence_candidate="MEDIUM",
                    temporal_validity_ref=request.temporal_order_refs[0].ref_id,
                    provenance=f"prov:{request.scenario_id}:opposition",
                )
            )
        return tuple(items)

    def _build_confounders(
        self, request: CausalGovernanceInputV1
    ) -> Tuple[ConfounderCandidateV1, ...]:
        output: List[ConfounderCandidateV1] = []
        for idx, ref in enumerate(request.confounder_refs, start=1):
            output.append(
                ConfounderCandidateV1(
                    confounder_id=f"confounder:{request.scenario_id}:{idx}",
                    related_hypothesis_refs=tuple(
                        f"hypothesis:{request.scenario_id}:{hid}"
                        for hid in request.hypothesis_candidates
                    ),
                    confounder_ref=ref.ref_id,
                    plausibility_candidate="CANDIDATE",
                    supporting_refs=tuple(
                        r.ref_id for r in request.supporting_evidence_refs
                    ),
                    opposing_refs=tuple(
                        r.ref_id for r in request.opposing_evidence_refs
                    ),
                    uncertainty=request.unknowns,
                    provenance=(f"prov:{request.scenario_id}:confounder",),
                )
            )
        return tuple(output)

    def _build_counterfactuals(
        self,
        request: CausalGovernanceInputV1,
        base_hypothesis: str,
    ) -> Tuple[CounterfactualCandidateV1, ...]:
        if not request.counterfactual_requested:
            return ()
        return (
            CounterfactualCandidateV1(
                counterfactual_id=f"counterfactual:{request.scenario_id}",
                base_hypothesis_ref=base_hypothesis,
                intervention_candidate="remove_or_weaken_candidate_cause",
                expected_difference_candidate="outcome_support_changes",
                required_assumptions=("intervention_isolated", "trace_preserved"),
                uncertainty=request.unknowns,
                provenance=(f"prov:{request.scenario_id}:counterfactual",),
                trace_ref=f"trace:{request.scenario_id}",
            ),
        )

    def _build_hypotheses(
        self,
        request: CausalGovernanceInputV1,
        state: str,
        uncertainty: UncertaintyEnvelopeV1,
    ) -> Tuple[CausalHypothesisCandidateV1, ...]:
        alternatives = tuple(
            self._mk_ref(
                CAUSAL_OWNER, f"alt:{request.scenario_id}:{name}", "HYPOTHESIS"
            )
            for name in request.hypothesis_candidates[1:]
        )
        result: List[CausalHypothesisCandidateV1] = []
        for idx, raw in enumerate(request.hypothesis_candidates, start=1):
            hyp_id = f"hypothesis:{request.scenario_id}:{idx}"
            result.append(
                CausalHypothesisCandidateV1(
                    hypothesis_id=hyp_id,
                    owner=CAUSAL_OWNER,
                    candidate_kind="CAUSAL_HYPOTHESIS_CANDIDATE",
                    hypothesis_statement=raw,
                    target_event_refs=request.target_event_refs,
                    cause_candidate_refs=request.cause_candidate_refs,
                    evidence_support_refs=request.supporting_evidence_refs,
                    evidence_opposition_refs=request.opposing_evidence_refs,
                    confounder_refs=request.confounder_refs,
                    temporal_order_refs=request.temporal_order_refs,
                    uncertainty=uncertainty,
                    alternative_hypothesis_refs=alternatives,
                    state_candidate=state,
                    provenance=(
                        self._mk_ref(
                            CAUSAL_OWNER,
                            f"prov:{request.scenario_id}:{idx}",
                            "PROVENANCE",
                        ),
                    ),
                    trace_ref=f"trace:{request.scenario_id}",
                )
            )
        return tuple(result)

    def _build_transitions(
        self,
        request: CausalGovernanceInputV1,
        state: str,
        first_hypothesis_id: str,
    ) -> Tuple[StateTransitionCandidateV1, ...]:
        reason = "candidate formation"
        if state == "CONTESTED":
            reason = "support-opposition-conflict or multi-hypothesis"
        elif state == "INSUFFICIENT_EVIDENCE":
            reason = "insufficient evidence or temporal-only signal"
        elif state == "REVISED":
            reason = "revision trigger observed"
        elif state == "REVOKED":
            reason = "revocation trigger observed"
        return (
            StateTransitionCandidateV1(
                hypothesis_id=first_hypothesis_id,
                from_state="PROPOSED",
                to_state=state,
                reason_candidate=reason,
                supporting_refs=tuple(
                    ref.ref_id for ref in request.supporting_evidence_refs
                ),
                opposing_refs=tuple(
                    ref.ref_id for ref in request.opposing_evidence_refs
                ),
                revision_or_revocation_trace=f"change:{request.scenario_id}:{state.lower()}",
            ),
        )

    def _build_trace(
        self,
        request: CausalGovernanceInputV1,
        hypotheses: Tuple[CausalHypothesisCandidateV1, ...],
        uncertainty: UncertaintyEnvelopeV1,
        counterfactual_refs: Tuple[str, ...],
        handoff_id: str,
    ) -> CausalTraceCandidateV1:
        conflict_refs = uncertainty.unresolved_conflicts
        revision_refs: Tuple[str, ...] = ()
        if "REVISION" in request.scenario_id:
            revision_refs = (f"change:{request.scenario_id}:revised",)
        if "REVOKED" in request.scenario_id:
            revision_refs = (f"change:{request.scenario_id}:revoked",)

        return CausalTraceCandidateV1(
            trace_id=f"trace:{request.scenario_id}",
            owner=CAUSAL_OWNER,
            hypothesis_refs=tuple(item.hypothesis_id for item in hypotheses),
            evidence_refs=tuple(ref.ref_id for ref in request.supporting_evidence_refs),
            provenance=(
                f"prov:{request.scenario_id}:ingress",
                f"prov:{request.scenario_id}:formation",
            ),
            opposition_refs=tuple(ref.ref_id for ref in request.opposing_evidence_refs),
            confounder_refs=tuple(ref.ref_id for ref in request.confounder_refs),
            temporal_order_refs=tuple(
                ref.ref_id for ref in request.temporal_order_refs
            ),
            intent_refs=tuple(ref.ref_id for ref in request.intent_refs),
            prior_refs=tuple(ref.ref_id for ref in request.prior_refs),
            context_refs=tuple(ref.ref_id for ref in request.context_refs),
            influence_refs=tuple(ref.ref_id for ref in request.influence_refs),
            uncertainty=uncertainty.unknowns,
            confidence_candidate=uncertainty.confidence_candidate,
            conflict_refs=conflict_refs,
            alternative_hypothesis_refs=tuple(
                ref.ref_id
                for item in hypotheses
                for ref in item.alternative_hypothesis_refs
            ),
            counterfactual_refs=counterfactual_refs,
            revision_chain_refs=revision_refs,
            parent_trace_refs=(f"parent:{request.scenario_id}",),
            admission_steps=(
                "admit_source_owned_refs",
                "enforce_temporal_and_correlation_guards",
                "form_hypothesis_candidates",
                "attach_support_and_opposition",
                "preserve_uncertainty_and_alternatives",
            ),
            handoff_refs=(handoff_id,),
            candidate_only=True,
        )

    def _build_handoff(
        self,
        request: CausalGovernanceInputV1,
        hypotheses: Tuple[CausalHypothesisCandidateV1, ...],
        uncertainty: UncertaintyEnvelopeV1,
        counterfactual_refs: Tuple[str, ...],
    ) -> CausalToDecisionHandoffCandidateV1:
        return CausalToDecisionHandoffCandidateV1(
            handoff_id=f"handoff:{request.scenario_id}",
            producer_owner=CAUSAL_OWNER,
            consumer_owner=DECISION_CONSUMER_OWNER,
            handoff_kind="CAUSAL_TO_DECISION_HANDOFF_CANDIDATE",
            causal_hypothesis_refs=tuple(item.hypothesis_id for item in hypotheses),
            supporting_evidence_refs=tuple(
                ref.ref_id for ref in request.supporting_evidence_refs
            ),
            opposing_evidence_refs=tuple(
                ref.ref_id for ref in request.opposing_evidence_refs
            ),
            uncertainty=uncertainty.unknowns,
            provenance=(f"prov:{request.scenario_id}:handoff",),
            alternative_hypothesis_refs=tuple(
                ref.ref_id
                for item in hypotheses
                for ref in item.alternative_hypothesis_refs
            ),
            unresolved_conflict_refs=uncertainty.unresolved_conflicts,
            counterfactual_refs=counterfactual_refs,
            trace_ref=f"trace:{request.scenario_id}",
            candidate_only=True,
            decision_executed=False,
            action_triggered=False,
            task_created=False,
        )

    def run_case(self, request: CausalGovernanceInputV1) -> CausalGovernanceOutputV1:
        state = self._derive_state(request)
        uncertainty = self._build_uncertainty(request, state)
        hypotheses = self._build_hypotheses(request, state, uncertainty)

        evidence_relations: List[CausalEvidenceRelationCandidateV1] = []
        for item in hypotheses:
            evidence_relations.extend(
                self._build_evidence_relations(request, item.hypothesis_id)
            )

        confounders = self._build_confounders(request)
        counterfactuals = self._build_counterfactuals(
            request, hypotheses[0].hypothesis_id
        )
        counterfactual_refs = tuple(item.counterfactual_id for item in counterfactuals)
        transitions = self._build_transitions(
            request, state, hypotheses[0].hypothesis_id
        )
        handoff = self._build_handoff(
            request, hypotheses, uncertainty, counterfactual_refs
        )
        trace = self._build_trace(
            request, hypotheses, uncertainty, counterfactual_refs, handoff.handoff_id
        )

        return CausalGovernanceOutputV1(
            scenario_id=request.scenario_id,
            hypothesis_candidates=hypotheses,
            evidence_relations=tuple(evidence_relations),
            confounder_candidates=confounders,
            counterfactual_candidates=counterfactuals,
            transitions=transitions,
            trace_candidate=trace,
            handoff_candidate=handoff,
            candidate_only=True,
            decision_output=False,
            action_output=False,
            task_output=False,
            runtime_executed=False,
            source_mutation_executed=False,
        )
