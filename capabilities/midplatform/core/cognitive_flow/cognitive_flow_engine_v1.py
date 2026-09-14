"""Deterministic synthetic engine for Cognitive Flow controlled implementation v1."""

from __future__ import annotations

from typing import Dict, List, Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_core_types_v1 import (
    CycleMetadataV1,
    NegativeGuardStatusV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_inheritance_types_v1 import (
    CognitiveMemoryObservationCandidateV1,
    CycleInheritanceCandidateV1,
    FutureLearningHandoffCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_interrupt_types_v1 import (
    AbortCandidateV1,
    InterruptCandidateV1,
    ResumeCandidateV1,
    SuspendCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_state_types_v1 import (
    CognitiveCycleStateCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_transition_types_v1 import (
    CognitiveCycleTransitionCandidateV1,
    ReconsiderationCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_handoff_types_v1 import (
    ModuleHandoffEnvelopeV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_io_types_v1 import (
    CognitiveFlowInputV1,
    CognitiveFlowOutputV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_registry_v1 import (
    CANONICAL_OWNER,
    CONTRACT_VERSION,
    NEGATIVE_GUARDS,
    SCHEMA_VERSION,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_trace_types_v1 import (
    CognitiveFlowProvenanceV1,
    CognitiveFlowTraceV1,
)


class CognitiveFlowEngineV1:
    def _stage_chain(self, sid: str) -> Tuple[str, ...]:
        if sid == "C15":
            return ("SUSPENDED", "INITIALIZING")
        if sid in {"C09", "C10", "C11", "C16"}:
            return ("INITIALIZING", "ABORTED")
        if sid in {"C12", "C13", "C14"}:
            return ("STATE_READY", "SUSPENDED")
        if sid in {"C03", "C04", "C05", "C07", "C22"}:
            return ("STATE_READY", "RECONSIDERING")
        return (
            "IDLE",
            "INITIALIZING",
            "CONTEXT_READY",
            "INTENT_READY",
            "STATE_FORMING",
            "STATE_READY",
            "REGULATING",
            "REGULATION_READY",
            "COMPLETED",
        )

    def _final_state(self, sid: str) -> str:
        if sid == "C15":
            return "INITIALIZING"
        if sid in {"C09", "C10", "C11", "C16"}:
            return "ABORTED"
        if sid in {"C12", "C13", "C14"}:
            return "SUSPENDED"
        if sid in {"C03", "C04", "C05", "C07", "C22"}:
            return "RECONSIDERING"
        return "COMPLETED"

    def _relationship_kind(self, sid: str) -> str:
        if sid in {"C02", "C06", "C18"}:
            return "CYCLE_INHERITANCE"
        if sid in {"C03", "C05", "C07", "C11", "C16", "C24"}:
            return "RECONSIDERATION_FEEDBACK"
        if sid in {"C04", "C13", "C14", "C22"}:
            return "READ_ONLY_PARALLEL"
        if sid in {"C08", "C12", "C21", "C23"}:
            return "OPTIONAL_REFERENCE"
        if sid in {"C19", "C20"}:
            return "DEFERRED_ASYNC_REFERENCE"
        return "STRICT_SEQUENCE"

    def _build_handoffs(
        self, request: CognitiveFlowInputV1
    ) -> Tuple[ModuleHandoffEnvelopeV1, ...]:
        sid = request.scenario_id
        envelopes = [
            (
                "Context Foundation",
                "Personal Cognitive Network Governance",
                request.context_refs[0].ref_id,
                tuple(r.ref_id for r in request.context_refs),
            ),
            (
                "Personal Cognitive Network Governance",
                "Intent Governance",
                request.pcn_refs[0].ref_id,
                tuple(r.ref_id for r in request.pcn_refs),
            ),
            (
                "Intent Governance",
                "Cognitive State Formation Governance",
                request.intent_refs[0].ref_id,
                tuple(r.ref_id for r in request.intent_refs),
            ),
        ]
        if request.cognitive_state_vector_ref is not None:
            envelopes.append(
                (
                    "Cognitive State Formation Governance",
                    "Dynamic Cognitive Regulation Governance",
                    request.cognitive_state_vector_ref.ref_id,
                    (request.cognitive_state_vector_ref.ref_id,),
                )
            )
        return tuple(
            ModuleHandoffEnvelopeV1(
                handoff_id=f"handoff:{sid}:{idx}",
                source_owner=src,
                target_owner=dst,
                source_candidate_ref=ref,
                required_refs=reqs,
                relationship_kind=self._relationship_kind(sid),
                trace_ref=f"trace:{sid}:handoff:{idx}",
                provenance_ref=f"prov:{sid}:handoff:{idx}",
                schema_version=SCHEMA_VERSION,
                contract_version=CONTRACT_VERSION,
            )
            for idx, (src, dst, ref, reqs) in enumerate(envelopes, start=1)
        )

    def _build_transitions(
        self, request: CognitiveFlowInputV1
    ) -> Tuple[CognitiveCycleTransitionCandidateV1, ...]:
        sid = request.scenario_id
        chain = self._stage_chain(sid)
        items: List[CognitiveCycleTransitionCandidateV1] = []
        for idx in range(len(chain) - 1):
            source_state = chain[idx]
            target_state = chain[idx + 1]
            items.append(
                CognitiveCycleTransitionCandidateV1(
                    cycle_id=request.cycle_snapshot.cycle_id,
                    source_state=source_state,
                    target_state=target_state,
                    transition_reason=f"{sid.lower()}_transition_{idx + 1}",
                    required_refs=request.cycle_snapshot.context_refs
                    + request.cycle_snapshot.intent_refs,
                    relationship_kind=self._relationship_kind(sid),
                    trace_ref=f"trace:{sid}:transition:{idx + 1}",
                )
            )
        return tuple(items)

    def _build_reconsiderations(
        self, request: CognitiveFlowInputV1
    ) -> Tuple[ReconsiderationCandidateV1, ...]:
        sid = request.scenario_id
        if sid not in {"C03", "C04", "C05", "C07", "C22", "C24"}:
            return ()
        return (
            ReconsiderationCandidateV1(
                cycle_id=request.cycle_snapshot.cycle_id,
                source_stage="REGULATION_READY"
                if sid in {"C07", "C24"}
                else "STATE_READY",
                target_stage="STATE_FORMING"
                if sid in {"C04", "C05", "C22"}
                else "INTENT_READY",
                reconsideration_reason=f"{sid.lower()}_reconsideration",
                related_refs=request.cycle_snapshot.intent_refs
                + request.cycle_snapshot.field_refs,
                trace_ref=f"trace:{sid}:reconsideration",
            ),
        )

    def _build_interrupts(self, request: CognitiveFlowInputV1):
        sid = request.scenario_id
        interrupt = None
        suspend = None
        resume = None
        abort = None
        if sid == "C13":
            interrupt = InterruptCandidateV1(
                request.cycle_snapshot.cycle_id,
                "safety_critical_field_event",
                request.cycle_snapshot.field_refs,
                trace_ref=f"trace:{sid}:interrupt",
            )
        if sid in {"C12", "C13", "C14"}:
            reason = {
                "C12": "required_ref_revoked",
                "C13": "safety_interrupt",
                "C14": "resource_constraint",
            }[sid]
            suspend = SuspendCandidateV1(
                request.cycle_snapshot.cycle_id,
                reason,
                request.cycle_snapshot.field_refs + request.cycle_snapshot.intent_refs,
                trace_ref=f"trace:{sid}:suspend",
            )
        if sid == "C15":
            resume = ResumeCandidateV1(
                request.cycle_snapshot.cycle_id,
                "controlled_resume",
                request.cycle_snapshot.intent_refs,
                trace_ref=f"trace:{sid}:resume",
            )
        if sid in {"C09", "C10", "C11", "C16"}:
            reason = {
                "C09": "duplicate_cycle_start",
                "C10": "duplicate_transition_request",
                "C11": "intent_cancellation",
                "C16": "invalid_evidence",
            }[sid]
            abort = AbortCandidateV1(
                request.cycle_snapshot.cycle_id,
                reason,
                request.cycle_snapshot.intent_refs + request.cycle_snapshot.field_refs,
                trace_ref=f"trace:{sid}:abort",
            )
        return interrupt, suspend, resume, abort

    def _build_inheritance(
        self, request: CognitiveFlowInputV1
    ) -> CycleInheritanceCandidateV1 | None:
        sid = request.scenario_id
        if sid not in {"C02", "C05", "C06", "C18", "C23"}:
            return None
        inherited = list(request.cycle_snapshot.intent_refs)
        if sid in {"C05", "C06", "C18"}:
            inherited.extend(request.cycle_snapshot.hypothesis_refs)
        inherited.append("uncertainty:retained")
        if request.cycle_snapshot.regulation_candidate_ref:
            inherited.append(request.cycle_snapshot.regulation_candidate_ref)
        return CycleInheritanceCandidateV1(
            cycle_id=request.cycle_snapshot.cycle_id,
            next_cycle_id=f"{request.cycle_snapshot.cycle_id}:next",
            inherited_refs=tuple(inherited),
            prohibited_refs_rejected=("mutable_runtime_state",),
            trace_ref=f"trace:{sid}:inheritance",
        )

    def _build_memory_candidate(
        self, request: CognitiveFlowInputV1
    ) -> CognitiveMemoryObservationCandidateV1 | None:
        sid = request.scenario_id
        if sid != "C19":
            return None
        return CognitiveMemoryObservationCandidateV1(
            cycle_id=request.cycle_snapshot.cycle_id,
            cycle_summary_candidate=f"summary:{sid}",
            salient_cognitive_event_candidate=f"event:{sid}",
            hypothesis_resolution_candidate=f"hypothesis_resolution:{sid}",
            intent_evolution_candidate=f"intent_evolution:{sid}",
            current_world_transition_candidate=f"world_transition:{sid}",
            regulation_outcome_candidate=f"regulation_outcome:{sid}",
            unresolved_uncertainty_candidate=f"uncertainty:{sid}",
            trace_ref=f"trace:{sid}:memory",
        )

    def _build_learning_candidate(
        self, request: CognitiveFlowInputV1
    ) -> FutureLearningHandoffCandidateV1 | None:
        sid = request.scenario_id
        if sid != "C20":
            return None
        return FutureLearningHandoffCandidateV1(
            cycle_id=request.cycle_snapshot.cycle_id,
            experience_candidate_ref=f"experience:{sid}",
            learning_candidate_ref=f"learning:{sid}",
            parameter_update_candidate_ref=f"parameter_update:{sid}",
            trace_ref=f"trace:{sid}:learning",
        )

    def _build_trace(
        self,
        request: CognitiveFlowInputV1,
        transitions: Tuple[CognitiveCycleTransitionCandidateV1, ...],
        reconsiderations: Tuple[ReconsiderationCandidateV1, ...],
        inheritance: CycleInheritanceCandidateV1 | None,
    ):
        sid = request.scenario_id
        reverse_lookup = {
            request.cycle_snapshot.cycle_id: request.cycle_snapshot.context_refs
            + request.cycle_snapshot.pcn_refs
            + request.cycle_snapshot.intent_refs
            + request.cycle_snapshot.field_refs,
        }
        return CognitiveFlowTraceV1(
            root_cycle_trace_id=f"trace:{sid}:root_cycle",
            cycle_id=request.cycle_snapshot.cycle_id,
            previous_cycle_id=request.cycle_snapshot.previous_cycle_id,
            context_refs=request.cycle_snapshot.context_refs,
            pcn_refs=request.cycle_snapshot.pcn_refs,
            intent_refs=request.cycle_snapshot.intent_refs,
            attention_refs=request.cycle_snapshot.attention_refs,
            hypothesis_refs=request.cycle_snapshot.hypothesis_refs,
            current_world_ref=request.cycle_snapshot.current_world_ref,
            cognitive_state_vector_ref=request.cycle_snapshot.cognitive_state_vector_ref,
            regulation_candidate_ref=request.cycle_snapshot.regulation_candidate_ref,
            field_refs=request.cycle_snapshot.field_refs,
            causal_refs=request.cycle_snapshot.causal_refs,
            transition_trace=tuple(t.trace_ref for t in transitions),
            interrupt_trace=(f"trace:{sid}:interrupt",) if sid == "C13" else tuple(),
            reconsideration_trace=tuple(r.trace_ref for r in reconsiderations),
            inheritance_trace=(inheritance.trace_ref,) if inheritance else tuple(),
            provenance_refs=request.cycle_snapshot.provenance_refs,
            schema_version=SCHEMA_VERSION,
            contract_version=CONTRACT_VERSION,
            reverse_lookup=reverse_lookup,
        )

    def _build_provenance(
        self, request: CognitiveFlowInputV1
    ) -> CognitiveFlowProvenanceV1:
        source_refs = (
            request.cycle_snapshot.context_refs
            + request.cycle_snapshot.pcn_refs
            + request.cycle_snapshot.intent_refs
            + request.cycle_snapshot.field_refs
            + request.cycle_snapshot.causal_refs
        )
        return CognitiveFlowProvenanceV1(
            resulting_cycle_ref=request.cycle_snapshot.cycle_id,
            previous_cycle_ref=request.cycle_snapshot.previous_cycle_id,
            source_snapshot_ref=request.cycle_snapshot.snapshot_id,
            source_refs=source_refs,
            reverse_locatable=True,
            source_owner_mutation=False,
        )

    def _guard_status(self) -> NegativeGuardStatusV1:
        return NegativeGuardStatusV1(**NEGATIVE_GUARDS)

    def _metadata(self, sid: str, transitions, reconsiderations, inheritance):
        relationship_kinds: Dict[str, str] = {
            "main": self._relationship_kind(sid),
            "field": "READ_ONLY_PARALLEL",
            "causal": "OPTIONAL_REFERENCE",
        }
        return CycleMetadataV1(
            relationship_kinds=relationship_kinds,
            transition_trace=tuple(t.trace_ref for t in transitions),
            interrupt_trace=(f"trace:{sid}:interrupt",) if sid == "C13" else tuple(),
            reconsideration_trace=tuple(r.trace_ref for r in reconsiderations),
            inheritance_trace=(inheritance.trace_ref,) if inheritance else tuple(),
        )

    def run_case(self, request: CognitiveFlowInputV1) -> CognitiveFlowOutputV1:
        sid = request.scenario_id
        transitions = self._build_transitions(request)
        reconsiderations = self._build_reconsiderations(request)
        interrupt, suspend, resume, abort = self._build_interrupts(request)
        inheritance = self._build_inheritance(request)
        memory_candidate = self._build_memory_candidate(request)
        learning_candidate = self._build_learning_candidate(request)
        handoffs = self._build_handoffs(request)

        final_state_value = self._final_state(sid)
        final_state = CognitiveCycleStateCandidateV1(
            cycle_id=request.cycle_snapshot.cycle_id,
            current_state=final_state_value,
            entry_condition=f"{sid.lower()}_entry_condition",
            allowed_source_states=(transitions[-1].source_state,)
            if transitions
            else ("IDLE",),
            allowed_next_states=("IDLE",)
            if final_state_value in {"COMPLETED", "ABORTED"}
            else ("INITIALIZING", "ABORTED"),
            transition_authorizer=CANONICAL_OWNER,
            required_refs=request.cycle_snapshot.context_refs
            + request.cycle_snapshot.intent_refs,
            forbidden_side_effects=("runtime_execution", "owner_mutation"),
            terminal=final_state_value in {"COMPLETED", "ABORTED"},
            trace_ref=f"trace:{sid}:final_state",
        )

        trace = self._build_trace(request, transitions, reconsiderations, inheritance)
        provenance = self._build_provenance(request)
        metadata = self._metadata(sid, transitions, reconsiderations, inheritance)

        return CognitiveFlowOutputV1(
            scenario_id=sid,
            final_state=final_state,
            transition_candidates=transitions,
            handoff_envelopes=handoffs,
            reconsideration_candidates=reconsiderations,
            interrupt_candidate=interrupt,
            suspend_candidate=suspend,
            resume_candidate=resume,
            abort_candidate=abort,
            inheritance_candidate=inheritance,
            memory_observation_candidate=memory_candidate,
            learning_handoff_candidate=learning_candidate,
            trace=trace,
            provenance=provenance,
            negative_guard_status=self._guard_status(),
            metadata=metadata,
            candidate_only=True,
            synthetic_only=True,
            runtime_executed=False,
            source_owner_mutation=False,
        )
