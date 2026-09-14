"""Controlled skeleton assembly for Intent Governance v1."""

from __future__ import annotations

from capabilities.midplatform.core.intent_governance.intent_core_types_v1 import (
    IntentCandidateV1,
    PotentialIntentCandidateV1,
    SourceRefV1,
    UncertaintyV1,
)
from capabilities.midplatform.core.intent_governance.intent_handoff_types_v1 import (
    IntentToCausalHandoffCandidateV1,
)
from capabilities.midplatform.core.intent_governance.intent_interaction_types_v1 import (
    IntentInteractionCandidateV1,
)
from capabilities.midplatform.core.intent_governance.intent_io_types_v1 import (
    IntentGovernanceInputV1,
    IntentGovernanceOutputV1,
)
from capabilities.midplatform.core.intent_governance.intent_registry_v1 import (
    CAUSAL_OWNER,
    INTENT_OWNER,
)
from capabilities.midplatform.core.intent_governance.intent_trace_types_v1 import (
    IntentTraceCandidateV1,
)


class IntentGovernanceSkeletonV1:
    def _source_ref(
        self, owner: str, ref_id: str, ref_type: str = "REFERENCE"
    ) -> SourceRefV1:
        return SourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)

    def _build_potential(
        self, request: IntentGovernanceInputV1
    ) -> PotentialIntentCandidateV1:
        return PotentialIntentCandidateV1(
            potential_intent_id=f"potential:{request.scenario_id}",
            owner=INTENT_OWNER,
            candidate_kind="POTENTIAL_INTENT_CANDIDATE",
            source_refs=request.source_refs,
            context_refs=request.context_refs,
            pcn_refs=request.pcn_refs,
            why_candidate="source-owned evidence indicates a possible future-state tendency",
            supporting_refs=request.source_refs,
            uncertainty=UncertaintyV1(
                unknowns=request.unknowns, confidence_is_not_truth=True
            ),
            alternative_candidates=(
                self._source_ref(INTENT_OWNER, f"alt:{request.scenario_id}"),
            ),
            provenance=(
                self._source_ref(
                    INTENT_OWNER, f"prov:{request.scenario_id}", "PROVENANCE"
                ),
            ),
            formation_trace=("receive_refs", "preserve_unknown", "qualify_potential"),
            temporal_validity_observed_at="synthetic-time",
            temporal_validity_candidate="candidate-validity",
            resource_constraint_ref=self._source_ref(
                "Self Regulation / Runtime Governance",
                f"resource:{request.scenario_id}",
                "RESOURCE",
            ),
            status="POTENTIAL",
            candidate_only=True,
        )

    def _derive_future_relation(self, scenario_id: str) -> str:
        if "AVOID" in scenario_id:
            return "AVOID"
        if "UNKNOWN" in scenario_id:
            return "UNKNOWN"
        if "CARRYOVER" in scenario_id or "LONG_TERM" in scenario_id:
            return "MAINTAIN"
        return "SEEK"

    def _derive_state(self, scenario_id: str) -> str:
        if "LOW_RESOURCE" in scenario_id:
            return "SUPPRESSED"
        if "DORMANT" in scenario_id:
            return "REACTIVATED"
        if "LONG_TERM" in scenario_id:
            return "ACTIVE_CANDIDATE"
        return "FORMING"

    def _build_intent(
        self, request: IntentGovernanceInputV1, potential: PotentialIntentCandidateV1
    ) -> IntentCandidateV1:
        return IntentCandidateV1(
            intent_id=f"intent:{request.scenario_id}",
            owner=INTENT_OWNER,
            candidate_kind="INTENT_CANDIDATE",
            source_refs=request.source_refs,
            context_refs=request.context_refs,
            pcn_refs=request.pcn_refs,
            self_refs=request.self_refs,
            field_refs=request.field_refs,
            role_refs=request.role_refs,
            relationship_refs=request.relationship_refs,
            memory_refs=request.memory_refs,
            experience_refs=request.experience_refs,
            emotion_refs=request.emotion_refs,
            direction_candidate="move toward an admissible future-state direction",
            future_state_relation=self._derive_future_relation(request.scenario_id),
            strength_candidate="candidate-strength",
            confidence_candidate="candidate-confidence",
            priority_candidate="candidate-priority",
            truth_status="UNKNOWN",
            uncertainty=request.unknowns,
            alternative_candidates=potential.alternative_candidates,
            provenance=potential.provenance,
            formation_trace=potential.formation_trace + ("qualify_intent_candidate",),
            state_candidate=self._derive_state(request.scenario_id),
            interaction_refs=(
                self._source_ref(
                    INTENT_OWNER,
                    f"interaction-ref:{request.scenario_id}",
                    "INTERACTION",
                ),
            ),
            carryover_candidate=(
                "CARRYOVER" in request.scenario_id or "LONG_TERM" in request.scenario_id
            ),
            resource_constraint_ref=potential.resource_constraint_ref,
            causal_handoff_eligible=True,
            candidate_only=True,
            reference_only=True,
        )

    def _build_interaction(
        self, request: IntentGovernanceInputV1, intent: IntentCandidateV1
    ) -> IntentInteractionCandidateV1:
        interaction_type = "COEXISTENCE"
        sid = request.scenario_id
        if "DOMINANCE" in sid:
            interaction_type = "TEMPORARY_DOMINANCE"
        elif "CONFLICT" in sid or "FAMILY_FIELD" in sid or "CROSSING" in sid:
            interaction_type = "CONFLICT"
        elif "LOW_RESOURCE" in sid:
            interaction_type = "SUPPRESSION"
        elif "DORMANT" in sid:
            interaction_type = "REACTIVATION"
        return IntentInteractionCandidateV1(
            interaction_id=f"interaction:{sid}",
            interaction_type=interaction_type,
            participant_candidate_ids=(intent.intent_id,),
            source_refs=tuple(ref.ref_id for ref in request.source_refs),
            context_refs=tuple(ref.ref_id for ref in request.context_refs),
            resource_ref=f"resource:{sid}",
            uncertainty=request.unknowns,
            observed_relation="candidate_relation_only",
            provenance=(f"trace:{sid}",),
            candidate_only=True,
            decision_authority=False,
            action_authority=False,
        )

    def _build_trace(
        self,
        request: IntentGovernanceInputV1,
        potential: PotentialIntentCandidateV1,
        intent: IntentCandidateV1,
        interaction: IntentInteractionCandidateV1,
    ) -> IntentTraceCandidateV1:
        omissions = ()
        if "LOW_RESOURCE" in request.scenario_id:
            omissions = (
                "alternative_expansion_breadth_reduced",
                "historical_retrieval_breadth_reduced",
            )
        return IntentTraceCandidateV1(
            trace_id=f"trace:{request.scenario_id}",
            scenario_id=request.scenario_id,
            source_refs=tuple(ref.ref_id for ref in request.source_refs),
            potential_intent_ids=(potential.potential_intent_id,),
            intent_candidate_ids=(intent.intent_id,),
            interaction_ids=(interaction.interaction_id,),
            carryover_ids=(
                (f"carryover:{request.scenario_id}",)
                if intent.carryover_candidate
                else ()
            ),
            resource_constraint_id=f"resource:{request.scenario_id}",
            unknowns=request.unknowns,
            omissions=omissions,
            candidate_only=True,
        )

    def _build_handoff(
        self,
        request: IntentGovernanceInputV1,
        potential: PotentialIntentCandidateV1,
        intent: IntentCandidateV1,
        interaction: IntentInteractionCandidateV1,
    ) -> IntentToCausalHandoffCandidateV1:
        temporary_dominance_refs = ()
        suppression_refs = ()
        competition_refs = ()
        if interaction.interaction_type == "TEMPORARY_DOMINANCE":
            temporary_dominance_refs = (interaction.interaction_id,)
        if interaction.interaction_type == "SUPPRESSION":
            suppression_refs = (interaction.interaction_id,)
        if interaction.interaction_type == "CONFLICT":
            competition_refs = (interaction.interaction_id,)
        return IntentToCausalHandoffCandidateV1(
            handoff_id=f"handoff:{request.scenario_id}",
            producer_owner=INTENT_OWNER,
            consumer_owner=CAUSAL_OWNER,
            intent_candidate_refs=(intent.intent_id,),
            potential_intent_refs=(potential.potential_intent_id,),
            competition_refs=competition_refs,
            suppression_refs=suppression_refs,
            temporary_dominance_refs=temporary_dominance_refs,
            context_refs=tuple(ref.ref_id for ref in request.context_refs),
            pcn_refs=tuple(ref.ref_id for ref in request.pcn_refs),
            field_refs=tuple(ref.ref_id for ref in request.field_refs),
            role_refs=tuple(ref.ref_id for ref in request.role_refs),
            relationship_refs=tuple(ref.ref_id for ref in request.relationship_refs),
            resource_ref=f"resource:{request.scenario_id}",
            provenance=(f"trace:{request.scenario_id}",),
            uncertainty=request.unknowns,
            handoff_reason_candidate="candidate-only downstream causal clarification request",
            candidate_only=True,
            causal_explanation=False,
            decision_output=False,
            action_output=False,
            task_output=False,
        )

    def run_case(self, request: IntentGovernanceInputV1) -> IntentGovernanceOutputV1:
        potential = self._build_potential(request)
        intent = self._build_intent(request, potential)
        interaction = self._build_interaction(request, intent)
        trace = self._build_trace(request, potential, intent, interaction)
        handoff = self._build_handoff(request, potential, intent, interaction)
        return IntentGovernanceOutputV1(
            scenario_id=request.scenario_id,
            potential_intents=(potential,),
            intent_candidates=(intent,),
            interaction_candidates=(interaction,),
            trace_candidate=trace,
            handoff_candidate=handoff,
            candidate_only=True,
            runtime_executed=False,
            source_mutation_executed=False,
        )
