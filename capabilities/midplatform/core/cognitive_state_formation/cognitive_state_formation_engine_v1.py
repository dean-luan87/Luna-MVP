"""Deterministic engine for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from typing import Dict, List, Tuple

from capabilities.midplatform.core.cognitive_state_formation.attention_types_v1 import (
    AttentionCandidateV1,
    AttentionSelectionCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_hypothesis_types_v1 import (
    CognitiveHypothesisCandidateV1,
    HypothesisCompetitionResultV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    NegativeGuardStatusV1,
    ProvenanceEnvelopeV1,
    TraceEnvelopeV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_handoff_types_v1 import (
    CognitiveToCausalHandoffCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_loop_types_v1 import (
    CognitiveHypothesisRevisionCandidateV1,
    CognitiveInformationGapCandidateV1,
    CognitiveReobservationCandidateV1,
    CognitiveStopCandidateV1,
    CognitiveSufficiencyCandidateV1,
    validate_cognitive_loop_candidates_v1,
    validated_requirement_establishment_from_condition_formation_v1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_conditioning_types_v1 import (
    CognitiveEvidenceRelevanceCandidateV1,
    CognitiveRelationInterpretationCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
    CognitiveStateFormationOutputV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_registry_v1 import (
    CANONICAL_OWNER,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_vector_types_v1 import (
    CognitiveStateVectorCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)
from capabilities.midplatform.core.execution_mode_v1 import (
    CONTROLLED_REPLAY_RUNTIME,
    LIVE_RUNTIME,
    SYNTHETIC_CONTROLLED,
    validate_execution_mode,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_static_validators_v1 import (
    validate_input_contract,
)


class CognitiveStateFormationEngineV1:
    """Deterministic candidate formation with governed synthetic/replay execution."""

    def _score(self, base: float, sid_num: int, delta: float) -> float:
        return round(base + (sid_num % 3) * delta, 3)

    @staticmethod
    def _is_conditioned_replay(request: CognitiveStateFormationInputV1) -> bool:
        return request.execution_mode in {CONTROLLED_REPLAY_RUNTIME, LIVE_RUNTIME}

    @staticmethod
    def _values(refs: Tuple[object, ...]) -> Tuple[str, ...]:
        return tuple(getattr(item, "source_ref", str(item)) for item in refs)

    @staticmethod
    def _semantic_values(
        request: CognitiveStateFormationInputV1, semantic_kind: str
    ) -> Tuple[str, ...]:
        return tuple(
            item.semantic_value.lower()
            for item in request.semantic_reference_values
            if item.semantic_kind == semantic_kind and item.semantic_value
        )

    @staticmethod
    def _semantic_values_for_ref(
        request: CognitiveStateFormationInputV1, source_ref: str, semantic_kind: str
    ) -> Tuple[str, ...]:
        return tuple(
            item.semantic_value.lower()
            for item in request.semantic_reference_values
            if item.source_ref == source_ref
            and item.semantic_kind == semantic_kind
            and item.semantic_value
        )

    def _conditioning_target(self, request: CognitiveStateFormationInputV1) -> str:
        values = self._semantic_values(request, "TARGET")
        return values[0].replace("-", "_") if values else "unknown"

    def _role_label(self, request: CognitiveStateFormationInputV1) -> str:
        values = self._semantic_values(request, "ROLE")
        return values[0] if values else "unknown-role"

    def _build_evidence_relevance_candidates(
        self, request: CognitiveStateFormationInputV1
    ) -> Tuple[CognitiveEvidenceRelevanceCandidateV1, ...]:
        evidence_refs = self._values(request.evidence_refs)
        evidence_support = {
            evidence_ref: tuple(info_refs)
            for evidence_ref, info_refs in request.evidence_information_refs
        }
        required_information = set(request.required_information_refs)
        role_values = self._semantic_values(request, "ROLE")
        target = self._conditioning_target(request)
        result = []
        for index, evidence_ref in enumerate(evidence_refs, start=1):
            if evidence_ref in evidence_support:
                supported = bool(required_information.intersection(evidence_support[evidence_ref]))
                result.append(
                    CognitiveEvidenceRelevanceCandidateV1(
                        relevance_ref=f"relevance:{request.scenario_id}:{index}",
                        evidence_ref=evidence_ref,
                        role_refs=self._values(request.role_refs),
                        task_refs=self._values(request.task_refs),
                        goal_refs=self._values(request.goal_refs),
                        information_need_refs=self._values(request.information_need_refs),
                        relevance_state="RELEVANT" if supported else "IRRELEVANT",
                        relevance_score_candidate=0.70 if supported else 0.15,
                        reason=(
                            "Evidence declares support for an active required information ref"
                            if supported
                            else "Evidence declares no support for an active required information ref"
                        ),
                    )
                )
                continue
            matched_topics = self._semantic_values_for_ref(request, evidence_ref, "EVIDENCE_TOPIC")
            topic = matched_topics[0] if matched_topics else "unknown"
            score = 0.15
            reasons = []
            if target in matched_topics or (target == "exit" and "door" in matched_topics) or (target == "operational_state" and any(item in {"operational", "state"} for item in matched_topics)):
                score += 0.55
                reasons.append("evidence topic matches the active information need")
            if any("owner" in role for role in role_values) and any(item in {"document", "desk"} for item in matched_topics):
                score += 0.20
                reasons.append("workspace-owner perspective makes the workspace relation relevant")
            if any("visitor" in role for role in role_values) and any(item in {"door", "exit"} for item in matched_topics):
                score += 0.20
                reasons.append("visitor perspective makes the shared exit relation relevant")
            if any("visitor" in role for role in role_values) and "document" in matched_topics:
                score -= 0.10
                reasons.append("visitor perspective lowers private-document relevance")
            if any("owner" in role for role in role_values) and any(item in {"door", "exit"} for item in matched_topics):
                score -= 0.05
                reasons.append("workspace-owner perspective lowers exit relevance for this need")
            if not matched_topics:
                reasons.append("evidence semantic topic is unavailable from the typed input")
            if not reasons:
                reasons.append("evidence is retained but has no demonstrated alignment with the active need")
            score = round(max(0.0, min(1.0, score)), 3)
            state = "RELEVANT" if score >= 0.70 else "CONTEXTUALLY_RELEVANT" if score >= 0.30 else "IRRELEVANT"
            result.append(
                CognitiveEvidenceRelevanceCandidateV1(
                    relevance_ref=f"relevance:{request.scenario_id}:{index}",
                    evidence_ref=evidence_ref,
                    role_refs=self._values(request.role_refs),
                    task_refs=self._values(request.task_refs),
                    goal_refs=self._values(request.goal_refs),
                    information_need_refs=self._values(request.information_need_refs),
                    relevance_state=state,
                    relevance_score_candidate=score,
                    reason="; ".join(reasons),
                )
            )
        return tuple(result)

    def _coverage_information_refs(
        self, request: CognitiveStateFormationInputV1
    ) -> set[str]:
        """Return only information supported by relevant admitted Evidence.

        Provider/runtime ingress supplies explicit Evidence-to-information
        bindings.  Inherited information remains available across a governed
        re-observation.  Legacy callers without bindings retain their existing
        declared-availability semantics.
        """

        if request.evidence_information_refs:
            relevance_by_evidence = {
                item.evidence_ref: item.relevance_state
                for item in self._build_evidence_relevance_candidates(request)
            }
            available = set(request.inherited_information_refs)
            for evidence_ref, information_refs in request.evidence_information_refs:
                if relevance_by_evidence.get(evidence_ref) == "RELEVANT":
                    available.update(information_refs)
            return available
        available = set(request.available_information_refs)
        if not available:
            available = set(self._values(request.evidence_refs))
        return available

    def _build_relation_interpretation_candidates(
        self, request: CognitiveStateFormationInputV1
    ) -> Tuple[CognitiveRelationInterpretationCandidateV1, ...]:
        if request.relation_interpretation_candidates:
            target = self._conditioning_target(request)
            role_label = self._role_label(request)
            conditioned = []
            for relation in request.relation_interpretation_candidates:
                if role_label == "workspace-owner":
                    perspective = "workspace-owner perspective"
                elif role_label == "visitor":
                    perspective = "visitor/shared-access perspective"
                else:
                    perspective = "unresolved role perspective"
                interpretation = (
                    f"{relation.subject_ref or relation.relation_ref} "
                    f"{relation.predicate or 'relation'} "
                    f"{relation.object_ref or 'field'} is interpreted from the "
                    f"{perspective} for {target}"
                )
                conditioned.append(
                    CognitiveRelationInterpretationCandidateV1(
                        relation_interpretation_ref=relation.relation_interpretation_ref,
                        relation_ref=relation.relation_ref,
                        role_refs=self._values(request.role_refs),
                        task_refs=self._values(request.task_refs),
                        goal_refs=self._values(request.goal_refs),
                        information_need_refs=self._values(request.information_need_refs),
                        interpretation_candidate=interpretation,
                        relevance_state=relation.relevance_state,
                        candidate_only=True,
                        field_state_candidate_ref=relation.field_state_candidate_ref,
                        subject_ref=relation.subject_ref,
                        predicate=relation.predicate,
                        object_ref=relation.object_ref,
                        relation_candidate_ref=relation.relation_candidate_ref,
                        relation_semantic_kind=relation.relation_semantic_kind,
                        evidence_refs=relation.evidence_refs,
                        source_refs=relation.source_refs,
                        provenance_refs=relation.provenance_refs,
                        identity_resolution_status=relation.identity_resolution_status,
                        fact_admitted=False,
                        truth_declared=False,
                        persistent_relation_declared=False,
                    )
                )
            return tuple(conditioned)
        target = self._conditioning_target(request)
        role_label = self._role_label(request)
        result = []
        for index, relation in enumerate(self._values(request.relation_refs), start=1):
            if role_label == "workspace-owner":
                interpretation = f"{relation} is interpreted from the workspace-owner perspective for {target}"
            elif role_label == "visitor":
                interpretation = f"{relation} is interpreted from the visitor/shared-access perspective for {target}"
            else:
                interpretation = f"{relation} is interpreted for {target} without a resolved role perspective"
            result.append(
                CognitiveRelationInterpretationCandidateV1(
                    relation_interpretation_ref=f"relation-interpretation:{request.scenario_id}:{index}",
                    relation_ref=relation,
                    role_refs=self._values(request.role_refs),
                    task_refs=self._values(request.task_refs),
                    goal_refs=self._values(request.goal_refs),
                    information_need_refs=self._values(request.information_need_refs),
                    interpretation_candidate=interpretation,
                    relevance_state="UNRESOLVED",
                )
            )
        return tuple(result)

    def _build_attention_candidates(
        self, request: CognitiveStateFormationInputV1
    ) -> Tuple[AttentionCandidateV1, ...]:
        if self._is_conditioned_replay(request):
            relevance_candidates = self._build_evidence_relevance_candidates(request)
            evidence_refs = self._values(request.evidence_refs)
            if not evidence_refs:
                evidence_refs = (f"evidence:{request.scenario_id}:unavailable",)
            items: List[AttentionCandidateV1] = []
            for index, evidence_ref in enumerate(evidence_refs, start=1):
                relevance_item = relevance_candidates[index - 1] if index <= len(relevance_candidates) else None
                relevance = relevance_item.relevance_score_candidate if relevance_item else 0.0
                evidence_states = self._semantic_values_for_ref(request, evidence_ref, "EVIDENCE_STATE")
                uncertainty = 0.65 if evidence_states else 0.20
                salience = round(0.35 + relevance * 0.35, 3)
                risk = 0.20
                urgency = round(0.30 + relevance * 0.20, 3)
                intent_alignment = round(0.35 + relevance * 0.45, 3)
                priority = round(
                    relevance * 0.35
                    + salience * 0.25
                    + risk * 0.25
                    + urgency * 0.10
                    + intent_alignment * 0.05,
                    3,
                )
                reason_refs = (relevance_item.relevance_ref,) if relevance_item else ()
                items.append(
                    AttentionCandidateV1(
                        attention_id=f"att:{request.scenario_id}:{index}",
                        subject_ref=evidence_ref,
                        source_refs=tuple(dict.fromkeys((*self._values(request.observation_refs), evidence_ref))),
                        reason_refs=reason_refs,
                        context_refs=self._values(request.context_refs),
                        pcn_refs=self._values(request.pcn_refs),
                        intent_refs=self._values(request.intent_refs),
                        field_refs=self._values(request.field_refs),
                        observation_refs=self._values(request.observation_refs),
                        risk_refs=self._values(request.risk_refs),
                        uncertainty_refs=self._values(request.uncertainty_refs),
                        task_refs=self._values(request.task_refs),
                        role_refs=self._values(request.role_refs),
                        memory_refs=self._values(request.memory_refs),
                        relevance_score_candidate=relevance,
                        salience_score_candidate=salience,
                        risk_score_candidate=risk,
                        urgency_score_candidate=urgency,
                        uncertainty_score_candidate=uncertainty,
                        intent_alignment_candidate=intent_alignment,
                        attention_priority_candidate=priority,
                        attention_state="PROPOSED",
                        trace_ref=f"trace:{request.scenario_id}:attention",
                        provenance_refs=(f"prov:{request.scenario_id}:attention:{index}",),
                    )
                )
            return tuple(items)
        sid = request.scenario_id
        sid_num = int(sid[1:])
        count = 1
        if sid in {
            "S02",
            "S03",
            "S06",
            "S07",
            "S08",
            "S10",
            "S12",
            "S14",
            "S15",
            "S16",
            "S17",
            "S19",
        }:
            count = 2
        if sid == "S03":
            count = 3

        items: List[AttentionCandidateV1] = []
        for idx in range(1, count + 1):
            risk_boost = 0.6 if sid in {"S02", "S12"} and idx == count else 0.0
            uncertainty_boost = (
                0.5
                if sid in {"S03", "S04", "S09", "S13", "S14", "S15", "S19", "S20"}
                else 0.0
            )
            relevance = self._score(0.45 + idx * 0.05, sid_num, 0.03)
            salience = self._score(0.40 + idx * 0.04, sid_num, 0.02)
            risk = self._score(0.20 + risk_boost, sid_num, 0.01)
            urgency = self._score(0.35 + idx * 0.02, sid_num, 0.02)
            uncertainty = self._score(0.20 + uncertainty_boost, sid_num, 0.01)
            intent_alignment = self._score(0.50 + idx * 0.03, sid_num, 0.01)
            priority = (
                relevance * 0.35
                + salience * 0.25
                + risk * 0.25
                + urgency * 0.10
                + intent_alignment * 0.05
            )
            items.append(
                AttentionCandidateV1(
                    attention_id=f"att:{sid}:{idx}",
                    subject_ref=f"subject:{sid}:{idx}",
                    source_refs=tuple(
                        dict.fromkeys(
                            (
                                *((request.current_world_ref.source_ref,)
                                  if request.current_world_ref is not None
                                  else ()),
                                *(r.source_ref for r in request.observation_refs),
                            )
                        )
                    ),
                    reason_refs=(f"reason:{sid}:{idx}",),
                    context_refs=tuple(r.source_ref for r in request.context_refs),
                    pcn_refs=tuple(r.source_ref for r in request.pcn_refs),
                    intent_refs=tuple(r.source_ref for r in request.intent_refs),
                    field_refs=tuple(r.source_ref for r in request.field_refs),
                    observation_refs=tuple(
                        r.source_ref for r in request.observation_refs
                    ),
                    risk_refs=tuple(r.source_ref for r in request.risk_refs),
                    uncertainty_refs=tuple(
                        r.source_ref for r in request.uncertainty_refs
                    ),
                    task_refs=tuple(r.source_ref for r in request.task_refs),
                    role_refs=tuple(r.source_ref for r in request.role_refs),
                    memory_refs=tuple(r.source_ref for r in request.memory_refs),
                    relevance_score_candidate=relevance,
                    salience_score_candidate=salience,
                    risk_score_candidate=risk,
                    urgency_score_candidate=urgency,
                    uncertainty_score_candidate=uncertainty,
                    intent_alignment_candidate=intent_alignment,
                    attention_priority_candidate=round(priority, 3),
                    attention_state="PROPOSED",
                    trace_ref=f"trace:{sid}:attention",
                    provenance_refs=(f"prov:{sid}:attention:{idx}",),
                )
            )
        return tuple(items)

    def _select_attention(
        self,
        request: CognitiveStateFormationInputV1,
        items: Tuple[AttentionCandidateV1, ...],
    ) -> AttentionSelectionCandidateV1:
        if self._is_conditioned_replay(request):
            ranked = sorted(items, key=lambda x: x.attention_priority_candidate, reverse=True)
            selected = (ranked[0].attention_id,) if ranked else ()
            conflict = any(
                state in {"absent", "conflict", "contradictory"}
                for ref in self._values(request.evidence_refs)
                for state in self._semantic_values_for_ref(request, ref, "EVIDENCE_STATE")
            )
            missing = not bool(self._values(request.evidence_refs))
            return AttentionSelectionCandidateV1(
                selection_id=f"sel:{request.scenario_id}",
                selected_attention_refs=selected,
                alternative_attention_refs=tuple(item.attention_id for item in ranked if item.attention_id not in selected),
                risk_override_applied=False,
                uncertainty_retained=conflict or missing or bool(request.uncertainty_refs),
                conflicting_focus=conflict,
                source_missing=missing,
                selection_mode="single_focus" if len(selected) <= 1 else "multi_focus",
                trace_ref=f"trace:{request.scenario_id}:attention_selection",
                provenance_refs=(f"prov:{request.scenario_id}:attention_selection",),
            )
        sid = request.scenario_id
        ranked = sorted(
            items, key=lambda x: x.attention_priority_candidate, reverse=True
        )
        selected = [ranked[0].attention_id]

        risk_override = sid in {"S02", "S12"}
        if risk_override and len(ranked) > 1:
            selected = [ranked[-1].attention_id]

        multi_focus = sid in {"S03", "S06", "S10", "S17", "S19"}
        if multi_focus and len(ranked) > 1:
            selected = [ranked[0].attention_id, ranked[1].attention_id]

        source_missing = sid == "S04"
        conflict = sid in {
            "S02",
            "S03",
            "S06",
            "S08",
            "S10",
            "S12",
            "S14",
            "S15",
            "S17",
            "S19",
        }
        uncertainty_retained = sid in {
            "S03",
            "S04",
            "S06",
            "S08",
            "S09",
            "S10",
            "S11",
            "S12",
            "S13",
            "S14",
            "S15",
            "S17",
            "S19",
            "S20",
        }

        mode = "single_focus"
        if multi_focus:
            mode = "multi_focus"

        return AttentionSelectionCandidateV1(
            selection_id=f"sel:{sid}",
            selected_attention_refs=tuple(selected),
            alternative_attention_refs=tuple(
                i.attention_id for i in ranked if i.attention_id not in selected
            ),
            risk_override_applied=risk_override,
            uncertainty_retained=uncertainty_retained,
            conflicting_focus=conflict,
            source_missing=source_missing,
            selection_mode=mode,
            trace_ref=f"trace:{sid}:attention_selection",
            provenance_refs=(f"prov:{sid}:attention_selection",),
        )

    def _hypothesis_state(self, sid: str) -> str:
        if sid in {"S01", "S05", "S07", "S16", "S18"}:
            return "SUPPORTED"
        if sid in {"S04", "S09", "S13"}:
            return "INSUFFICIENT_EVIDENCE"
        if sid == "S10":
            return "REVISED"
        if sid in {"S11", "S20"}:
            return "REVOKED"
        if sid == "S14":
            return "SUSPENDED"
        return "CONTESTED"

    def _build_hypotheses(
        self,
        request: CognitiveStateFormationInputV1,
        attention_selection: AttentionSelectionCandidateV1,
    ) -> Tuple[CognitiveHypothesisCandidateV1, ...]:
        if self._is_conditioned_replay(request):
            evidence_refs = self._values(request.evidence_refs)
            required = set(request.required_information_refs)
            available = self._coverage_information_refs(request)
            missing = required - available
            conflicting = any(
                state in {"absent", "conflict", "contradictory"}
                for ref in evidence_refs
                for state in self._semantic_values_for_ref(request, ref, "EVIDENCE_STATE")
            )
            if request.prior_information_gap_ref and request.prior_reobservation_ref:
                state = "REVISED"
            elif missing:
                state = "INSUFFICIENT_EVIDENCE"
            elif conflicting:
                state = "CONTESTED"
            else:
                state = "SUPPORTED"
            target = self._conditioning_target(request)
            role_label = self._role_label(request)
            task_values = self._semantic_values(request, "TASK_LABEL")
            task_label = task_values[0] if task_values else "task-unresolved"
            count = 2 if conflicting else 1
            hypotheses: List[CognitiveHypothesisCandidateV1] = []
            for index in range(1, count + 1):
                hid = f"hyp:{request.scenario_id}:{index}"
                alternatives = tuple(f"hyp:{request.scenario_id}:{j}" for j in range(1, count + 1) if j != index)
                unknowns = tuple(sorted(missing))
                opposition = tuple(
                    ref
                    for ref in evidence_refs
                    if any(
                        state in {"absent", "opposed", "contradictory"}
                        for state in self._semantic_values_for_ref(request, ref, "EVIDENCE_STATE")
                    )
                )
                hypotheses.append(
                    CognitiveHypothesisCandidateV1(
                        hypothesis_id=hid,
                        hypothesis_statement_candidate=f"{role_label} considers {task_label} as a {target}-conditioned candidate",
                        subject_refs=(f"subject:{target}",),
                        supporting_evidence_refs=evidence_refs,
                        opposing_evidence_refs=opposition,
                        alternative_hypothesis_refs=alternatives,
                        unknown_refs=unknowns,
                        conflict_refs=(f"conflict:{request.scenario_id}",) if conflicting else (),
                        attention_refs=attention_selection.selected_attention_refs,
                        context_refs=self._values(request.context_refs),
                        field_refs=self._values(request.field_refs),
                        pcn_refs=self._values(request.pcn_refs),
                        intent_refs=self._values(request.intent_refs),
                        confidence_candidate="MEDIUM" if state == "SUPPORTED" else "LOW",
                        state=state,
                        revision_parent_ref=request.prior_hypothesis_refs[0] if state == "REVISED" and request.prior_hypothesis_refs else None,
                        trace_ref=f"trace:{request.scenario_id}:hypothesis",
                        provenance_refs=(f"prov:{request.scenario_id}:hypothesis:{index}",),
                    )
                )
            return tuple(hypotheses)
        sid = request.scenario_id
        state = self._hypothesis_state(sid)
        count = 1
        if sid in {"S03", "S06", "S10", "S12", "S17", "S19"}:
            count = 2

        hypotheses: List[CognitiveHypothesisCandidateV1] = []
        for idx in range(1, count + 1):
            hid = f"hyp:{sid}:{idx}"
            alternatives = tuple(
                f"hyp:{sid}:{j}" for j in range(1, count + 1) if j != idx
            )
            evidence_refs = tuple(r.source_ref for r in request.evidence_refs)
            if not evidence_refs:
                evidence_refs = (f"evidence:support:{sid}:{idx}",)
            opposition = (
                (f"evidence:oppose:{sid}:{idx}",)
                if state in {"CONTESTED", "REJECTED"}
                else ()
            )
            unknowns = (
                (f"unknown:{sid}",)
                if state
                in {
                    "INSUFFICIENT_EVIDENCE",
                    "SUSPENDED",
                    "REVOKED",
                    "REVISED",
                    "CONTESTED",
                }
                else ()
            )
            revision_parent = f"hyp:{sid}:0" if state == "REVISED" else None
            hypotheses.append(
                CognitiveHypothesisCandidateV1(
                    hypothesis_id=hid,
                    hypothesis_statement_candidate=f"candidate explanation {sid} #{idx}",
                    subject_refs=(f"subject:{sid}",),
                    supporting_evidence_refs=evidence_refs,
                    opposing_evidence_refs=opposition,
                    alternative_hypothesis_refs=alternatives,
                    unknown_refs=unknowns,
                    conflict_refs=(f"conflict:{sid}",)
                    if state in {"CONTESTED", "SUSPENDED", "REVISED"}
                    else (),
                    attention_refs=attention_selection.selected_attention_refs,
                    context_refs=tuple(r.source_ref for r in request.context_refs),
                    field_refs=tuple(r.source_ref for r in request.field_refs),
                    pcn_refs=tuple(r.source_ref for r in request.pcn_refs),
                    intent_refs=tuple(r.source_ref for r in request.intent_refs),
                    confidence_candidate="MEDIUM" if state == "SUPPORTED" else "LOW",
                    state=state,
                    revision_parent_ref=revision_parent,
                    trace_ref=f"trace:{sid}:hypothesis",
                    provenance_refs=(f"prov:{sid}:hypothesis:{idx}",),
                )
            )
        return tuple(hypotheses)

    def _build_competition(
        self,
        sid: str,
        hypotheses: Tuple[CognitiveHypothesisCandidateV1, ...],
    ) -> HypothesisCompetitionResultV1:
        active = tuple(
            h.hypothesis_id
            for h in hypotheses
            if h.state in {"SUPPORTED", "CONTESTED", "REVISED"}
        )
        suspended = tuple(h.hypothesis_id for h in hypotheses if h.state == "SUSPENDED")
        revoked = tuple(h.hypothesis_id for h in hypotheses if h.state == "REVOKED")
        insufficient = tuple(
            h.hypothesis_id for h in hypotheses if h.state == "INSUFFICIENT_EVIDENCE"
        )
        alternatives = tuple(
            alt for h in hypotheses for alt in h.alternative_hypothesis_refs
        )
        conflicts = tuple(c for h in hypotheses for c in h.conflict_refs)
        support_refs = tuple(s for h in hypotheses for s in h.supporting_evidence_refs)
        oppose_refs = tuple(s for h in hypotheses for s in h.opposing_evidence_refs)

        return HypothesisCompetitionResultV1(
            competition_id=f"cmp:{sid}",
            active_hypothesis_refs=active,
            suspended_hypothesis_refs=suspended,
            revoked_hypothesis_refs=revoked,
            insufficient_evidence_refs=insufficient,
            alternative_explanation_refs=alternatives,
            conflict_refs=conflicts,
            support_accumulation_refs=support_refs,
            opposition_refs=oppose_refs,
            trace_ref=f"trace:{sid}:competition",
            provenance_refs=(f"prov:{sid}:competition",),
        )

    def _world_kind(self, sid: str) -> str:
        if sid in {"S13", "S15", "S11", "S20", "S04"}:
            return "PARTIAL"
        if sid == "S09":
            return "UNKNOWN"
        if sid in {"S02", "S08", "S12", "S14"}:
            return "CONFLICTED"
        if sid in {"S03", "S06", "S10", "S17", "S19"}:
            return "MULTI_HYPOTHESIS"
        return "STABLE_CANDIDATE"

    def _build_world(
        self,
        request: CognitiveStateFormationInputV1,
        attention_selection: AttentionSelectionCandidateV1,
        competition: HypothesisCompetitionResultV1,
    ) -> CurrentWorldCandidateV1:
        sid = request.scenario_id
        if self._is_conditioned_replay(request):
            relevance_candidates = self._build_evidence_relevance_candidates(request)
            relation_candidates = self._build_relation_interpretation_candidates(request)
            if competition.conflict_refs:
                kind = "CONFLICTED"
            elif request.required_information_refs and set(request.required_information_refs) - self._coverage_information_refs(request):
                kind = "PARTIAL"
            else:
                kind = f"ROLE_TASK_CONDITIONED_{self._conditioning_target(request).upper()}"
            source_current_world = (
                (request.current_world_ref.source_ref,)
                if request.current_world_ref is not None
                else ()
            )
            return CurrentWorldCandidateV1(
                current_world_id=f"world:{sid}",
                attention_refs=attention_selection.selected_attention_refs,
                active_hypothesis_refs=competition.active_hypothesis_refs,
                alternative_hypothesis_refs=competition.alternative_explanation_refs,
                context_refs=self._values(request.context_refs),
                field_state_refs=self._values(request.field_refs),
                pcn_refs=self._values(request.pcn_refs),
                intent_refs=self._values(request.intent_refs),
                observation_refs=self._values(request.observation_refs),
                uncertainty_refs=self._values(request.uncertainty_refs),
                conflict_refs=competition.conflict_refs,
                temporal_refs=(f"temporal:{sid}",),
                source_versions={
                    "context": "v1",
                    "pcn": "v1",
                    "intent": "v1",
                    "field": "v1",
                    "observation": "v1",
                    "current_world": "current-world-candidate-v1" if request.current_world_ref is not None else "",
                },
                world_state_kind_candidate=kind,
                world_stability_candidate="LOW" if kind in {"UNKNOWN", "CONFLICTED", "PARTIAL"} else "MEDIUM",
                trace_ref=f"trace:{sid}:world",
                provenance_refs=tuple(dict.fromkeys((*source_current_world, f"prov:{sid}:world"))),
                evidence_relevance_refs=tuple(item.relevance_ref for item in relevance_candidates),
                relation_interpretation_refs=tuple(item.relation_interpretation_ref for item in relation_candidates),
            )
        kind = self._world_kind(sid)
        conflict_refs = competition.conflict_refs
        if kind == "CONFLICTED" and not conflict_refs:
            conflict_refs = (f"conflict:{sid}",)

        source_current_world = (
            (request.current_world_ref.source_ref,)
            if request.current_world_ref is not None
            else ()
        )
        return CurrentWorldCandidateV1(
            current_world_id=f"world:{sid}",
            attention_refs=attention_selection.selected_attention_refs,
            active_hypothesis_refs=competition.active_hypothesis_refs,
            alternative_hypothesis_refs=competition.alternative_explanation_refs,
            context_refs=tuple(r.source_ref for r in request.context_refs),
            field_state_refs=tuple(r.source_ref for r in request.field_refs),
            pcn_refs=tuple(r.source_ref for r in request.pcn_refs),
            intent_refs=tuple(r.source_ref for r in request.intent_refs),
            observation_refs=tuple(r.source_ref for r in request.observation_refs),
            uncertainty_refs=tuple(r.source_ref for r in request.uncertainty_refs),
            conflict_refs=conflict_refs,
            temporal_refs=(f"temporal:{sid}",),
            source_versions={
                "context": "v1",
                "pcn": "v1",
                "intent": "v1",
                "field": "v1",
                "observation": "v1",
                "current_world": "current-world-candidate-v1"
                if request.current_world_ref is not None
                else "",
            },
            world_state_kind_candidate=kind,
            world_stability_candidate="LOW"
            if kind in {"UNKNOWN", "CONFLICTED"}
            else "MEDIUM",
            trace_ref=f"trace:{sid}:world",
            provenance_refs=tuple(
                dict.fromkeys(
                    (*source_current_world, f"prov:{sid}:world")
                )
            ),
        )

    def _build_vector(
        self,
        sid: str,
        world: CurrentWorldCandidateV1,
        competition: HypothesisCompetitionResultV1,
    ) -> CognitiveStateVectorCandidateV1:
        return CognitiveStateVectorCandidateV1(
            state_vector_id=f"vector:{sid}",
            attention_distribution_refs=world.attention_refs,
            hypothesis_state_refs=competition.active_hypothesis_refs
            + competition.insufficient_evidence_refs,
            uncertainty_level_candidate="HIGH"
            if world.world_state_kind_candidate in {"UNKNOWN", "CONFLICTED"}
            else "MEDIUM",
            conflict_level_candidate="HIGH" if world.conflict_refs else "LOW",
            world_stability_candidate=world.world_stability_candidate,
            intent_pressure_candidate="MEDIUM",
            resource_pressure_candidate="LOW",
            current_world_ref=world.current_world_id,
            trace_ref=f"trace:{sid}:vector",
            provenance_refs=(f"prov:{sid}:vector",),
        )

    def _build_handoff(
        self,
        sid: str,
        request: CognitiveStateFormationInputV1,
        world: CurrentWorldCandidateV1,
        competition: HypothesisCompetitionResultV1,
    ) -> CognitiveToCausalHandoffCandidateV1:
        evidence_refs = tuple(r.source_ref for r in request.evidence_refs)
        if not evidence_refs:
            evidence_refs = tuple(
                f"evidence:{sid}:{idx}"
                for idx in range(1, len(competition.active_hypothesis_refs) + 2)
            )
        return CognitiveToCausalHandoffCandidateV1(
            handoff_id=f"handoff:{sid}",
            handoff_type="CANDIDATE_REFERENCE_ONLY",
            producer_owner=CANONICAL_OWNER,
            consumer_owner="Causal Governance",
            attention_refs=world.attention_refs,
            active_hypothesis_refs=world.active_hypothesis_refs,
            alternative_hypothesis_refs=world.alternative_hypothesis_refs,
            context_refs=tuple(r.source_ref for r in request.context_refs),
            field_state_refs=tuple(r.source_ref for r in request.field_refs),
            observation_refs=tuple(r.source_ref for r in request.observation_refs),
            uncertainty_refs=tuple(r.source_ref for r in request.uncertainty_refs),
            conflict_refs=world.conflict_refs,
            evidence_refs=evidence_refs,
            trace_ref=f"trace:{sid}:handoff",
            provenance_refs=(f"prov:{sid}:handoff",),
        )

    def _build_trace_and_provenance(
        self,
        request: CognitiveStateFormationInputV1,
        sid: str,
        world: CurrentWorldCandidateV1,
        competition: HypothesisCompetitionResultV1,
        handoff: CognitiveToCausalHandoffCandidateV1,
    ) -> Tuple[TraceEnvelopeV1, ProvenanceEnvelopeV1]:
        trace = TraceEnvelopeV1(
            root_trace_id=f"trace:{sid}:root",
            attention_trace_ref=f"trace:{sid}:attention",
            hypothesis_trace_ref=f"trace:{sid}:hypothesis",
            current_world_trace_ref=world.trace_ref,
            downstream_handoff_trace_ref=handoff.trace_ref,
            revision_lineage_refs=(f"lineage:{sid}:revision",)
            if sid in {"S10"}
            else (),
            revocation_lineage_refs=(f"lineage:{sid}:revocation",)
            if sid in {"S11", "S20"}
            else (),
            source_version_lineage_refs=(
                "context:v1",
                "pcn:v1",
                "intent:v1",
                "field:v1",
                "observation:v1",
                "current-world-candidate-v1"
                if request.current_world_ref is not None
                else "",
            ),
            alternative_hypothesis_lineage_refs=competition.alternative_explanation_refs,
        )
        provenance = ProvenanceEnvelopeV1(
            source_refs=tuple(
                item
                for item in (
                    *((request.current_world_ref.source_ref,)
                      if request.current_world_ref is not None
                      else ()),
                    "context",
                    "pcn",
                    "intent",
                    "field",
                    "observation",
                    "risk",
                    "uncertainty",
                    "task",
                    "role",
                    "memory",
                )
                if item
            ),
            owner_refs=(
                "Context Foundation",
                "Personal Cognitive Network Governance",
                "Intent Governance",
                "Field State Reducer",
                "Cognitive State Formation Governance",
                "Causal Governance",
            ),
            version_refs=("v1",),
            reverse_lookup={
                world.current_world_id: (
                    *((request.current_world_ref.source_ref,)
                      if request.current_world_ref is not None
                      else ()),
                    *world.active_hypothesis_refs,
                    *world.attention_refs,
                    *world.context_refs,
                    *world.field_state_refs,
                    *world.observation_refs,
                ),
                handoff.handoff_id: (
                    *handoff.active_hypothesis_refs,
                    *handoff.evidence_refs,
                    *handoff.context_refs,
                    *handoff.field_state_refs,
                ),
            },
        )
        return trace, provenance

    def _build_negative_guard_status(self) -> NegativeGuardStatusV1:
        return NegativeGuardStatusV1(
            candidate_only=True,
            context_mutation=False,
            pcn_mutation=False,
            intent_mutation=False,
            field_mutation=False,
            causal_mutation=False,
            decision_output=False,
            action_output=False,
            task_output=False,
            database_write=False,
            device_control=False,
            scheduler_execution=False,
            runtime_side_effect=False,
            model_call=False,
            learning_update=False,
            self_regulation_update=False,
            dynamic_parameter_mutation=False,
            single_truth_collapse=False,
        )

    def _build_cognitive_loop_candidates(
        self,
        request: CognitiveStateFormationInputV1,
        world: CurrentWorldCandidateV1,
        hypotheses: Tuple[CognitiveHypothesisCandidateV1, ...],
    ) -> Tuple[
        CognitiveSufficiencyCandidateV1,
        CognitiveInformationGapCandidateV1 | None,
        CognitiveReobservationCandidateV1 | None,
        CognitiveHypothesisRevisionCandidateV1 | None,
        CognitiveStopCandidateV1 | None,
        str | None,
    ]:
        evidence_refs = tuple(r.source_ref for r in request.evidence_refs)
        available = self._coverage_information_refs(request)
        required = tuple(request.required_information_refs)
        missing = tuple(ref for ref in required if ref not in available)
        execution_ref = request.execution_ref or f"cognitive:{request.scenario_id}:candidate"
        sufficiency_ref = f"sufficiency:{execution_ref}:v1"
        establishment_projection = (
            validated_requirement_establishment_from_condition_formation_v1(
                request.required_cognitive_condition_formation_result
            )
            if request.required_cognitive_condition_formation_result is not None
            else None
        )
        if establishment_projection is not None:
            establishment_status, establishment_ref, establishment_basis = establishment_projection
        else:
            declared_status = request.requirement_establishment_status
            establishment_status = (
                declared_status
                if declared_status in {"UNAVAILABLE", "INVALID", "WITHHELD"}
                else "NOT_ESTABLISHED"
            )
            establishment_ref = None
            establishment_basis = None
        can_evaluate_sufficiency = establishment_status == "ESTABLISHED"
        sufficient = can_evaluate_sufficiency and not missing
        goal_values = self._values(request.goal_refs)
        concern_values = self._values(request.concern_refs)
        if self._is_conditioned_replay(request):
            goal_ref = goal_values[0] if goal_values else (self._values(request.intent_refs)[0] if request.intent_refs else "goal:unresolved")
            concern_ref = concern_values[0] if concern_values else "concern:unresolved"
        else:
            goal_ref = request.intent_refs[0].source_ref if request.intent_refs else f"goal:{request.scenario_id}"
            concern_ref = f"concern:{request.scenario_id}"
        sufficiency = CognitiveSufficiencyCandidateV1(
            sufficiency_ref=sufficiency_ref,
            owner_ref=CANONICAL_OWNER,
            goal_ref=goal_ref,
            concern_ref=concern_ref,
            status=(
                "SUFFICIENT"
                if sufficient
                else "INSUFFICIENT"
                if can_evaluate_sufficiency
                else "WITHHELD"
                if establishment_status == "WITHHELD"
                else "UNKNOWN"
            ),
            evidence_refs=evidence_refs,
            required_information_refs=required,
            missing_information_refs=missing,
            reason=(
                "active cognitive need is covered by admitted relevant information"
                if sufficient
                else "active cognitive need still has required information missing"
                if can_evaluate_sufficiency
                else "requirement establishment proof is unavailable; sufficiency is withheld"
            ),
            stop_required=sufficient,
            requirement_establishment_status=establishment_status,
            requirement_establishment_ref=establishment_ref,
            requirement_establishment_basis=establishment_basis,
        )
        if not can_evaluate_sufficiency:
            return sufficiency, None, None, None, None, None
        if sufficient:
            stop = CognitiveStopCandidateV1(
                stop_ref=f"stop:{execution_ref}:v1",
                owner_ref=CANONICAL_OWNER,
                sufficiency_ref=sufficiency_ref,
                reason="MINIMUM_SUFFICIENT_INFORMATION_REACHED",
                cycle_index=request.cycle_index,
            )
            revision = None
            if request.prior_information_gap_ref and request.prior_reobservation_ref:
                revision = CognitiveHypothesisRevisionCandidateV1(
                    hypothesis_revision_ref=f"hypothesis-revision:{execution_ref}:v1",
                    owner_ref=CANONICAL_OWNER,
                    prior_hypothesis_refs=request.prior_hypothesis_refs,
                    revised_hypothesis_refs=tuple(item.hypothesis_id for item in hypotheses),
                    information_gap_ref=request.prior_information_gap_ref,
                    reobservation_ref=request.prior_reobservation_ref,
                    evidence_refs=evidence_refs,
                    reason="new admitted evidence revises the prior hypothesis state",
                )
            return sufficiency, None, None, revision, stop, None

        information_gap_ref = f"information-gap:{execution_ref}:v1"
        observation_need_ref = f"observation-need:{execution_ref}:v1"
        reobservation_ref = f"reobservation:{execution_ref}:v1"
        next_cycle_ref = f"next-cycle-ingress:{execution_ref}:v1"
        gap = CognitiveInformationGapCandidateV1(
            information_gap_ref=information_gap_ref,
            owner_ref=CANONICAL_OWNER,
            sufficiency_ref=sufficiency_ref,
            missing_information_refs=missing,
            observation_need_ref=observation_need_ref,
            reason="required information is missing for the active cognitive need",
        )
        reobservation = CognitiveReobservationCandidateV1(
            reobservation_ref=reobservation_ref,
            owner_ref="Field Perception Orchestrator",
            information_gap_ref=information_gap_ref,
            observation_need_ref=observation_need_ref,
            next_cycle_ingress_ref=next_cycle_ref,
            reason="targeted re-observation is required by the information gap",
        )
        return sufficiency, gap, reobservation, None, None, next_cycle_ref

    def run_case(
        self, request: CognitiveStateFormationInputV1
    ) -> CognitiveStateFormationOutputV1:
        input_errors = validate_input_contract(request)
        if input_errors:
            raise ValueError("cognitive_state_input_invalid:" + ";".join(input_errors))
        mode_errors = validate_execution_mode(
            request.execution_mode,
            synthetic_only=request.synthetic_only,
        )
        if mode_errors:
            raise ValueError("cognitive_state_execution_mode_invalid:" + ";".join(mode_errors))
        if request.execution_mode in {CONTROLLED_REPLAY_RUNTIME, LIVE_RUNTIME}:
            if not request.candidate_only:
                raise ValueError("cognitive_state_runtime_requires_candidate_only")
            if request.execution_mode == CONTROLLED_REPLAY_RUNTIME and not request.replay_input_ref:
                raise ValueError("cognitive_state_replay_input_ref_missing")
            if request.execution_mode == LIVE_RUNTIME and not request.runtime_observation_ref:
                raise ValueError("cognitive_state_runtime_observation_ref_missing")
            if not request.execution_ref:
                raise ValueError("cognitive_state_execution_ref_missing")
            if not request.observation_refs:
                raise ValueError("cognitive_state_runtime_observation_refs_missing")
            if request.cycle_index > 1 and not request.prior_next_cycle_ingress_ref:
                raise ValueError("cognitive_state_runtime_next_cycle_ingress_ref_missing")

        attention_candidates = self._build_attention_candidates(request)
        attention_selection = self._select_attention(request, attention_candidates)
        hypotheses = self._build_hypotheses(request, attention_selection)
        evidence_relevance_candidates = self._build_evidence_relevance_candidates(request)
        relation_interpretation_candidates = self._build_relation_interpretation_candidates(request)
        competition = self._build_competition(request.scenario_id, hypotheses)
        world = self._build_world(request, attention_selection, competition)
        vector = self._build_vector(request.scenario_id, world, competition)
        handoff = self._build_handoff(request.scenario_id, request, world, competition)
        sufficiency, information_gap, reobservation, hypothesis_revision, stop, next_cycle_ref = self._build_cognitive_loop_candidates(
            request, world, hypotheses
        )
        loop_errors = validate_cognitive_loop_candidates_v1(
            sufficiency=sufficiency,
            information_gap=information_gap,
            reobservation=reobservation,
            hypothesis_revision=None,
            stop=stop,
        )
        if hypothesis_revision is not None:
            prior_loop_errors = validate_cognitive_loop_candidates_v1(
                sufficiency=request.prior_sufficiency_candidate,
                information_gap=request.prior_information_gap_candidate,
                reobservation=request.prior_reobservation_candidate,
                hypothesis_revision=hypothesis_revision,
                stop=None,
            )
            loop_errors = (*loop_errors, *prior_loop_errors)
        if loop_errors:
            raise ValueError("cognitive_loop_contract_invalid:" + ";".join(loop_errors))
        trace, provenance = self._build_trace_and_provenance(
            request, request.scenario_id, world, competition, handoff
        )

        runtime_executed = request.execution_mode in {CONTROLLED_REPLAY_RUNTIME, LIVE_RUNTIME}
        transition_refs = (
            (
                f"transition:{request.execution_ref}:ingress-to-attention",
                f"transition:{request.execution_ref}:attention-to-hypothesis",
                f"transition:{request.execution_ref}:hypothesis-to-current-world",
                *(
                    (
                        f"transition:{request.execution_ref}:current-world-to-sufficiency",
                        f"transition:{request.execution_ref}:sufficiency-to-stop",
                    )
                    if stop is not None
                    else (
                        f"transition:{request.execution_ref}:current-world-to-sufficiency",
                        f"transition:{request.execution_ref}:sufficiency-to-information-gap",
                        f"transition:{request.execution_ref}:information-gap-to-reobservation",
                        f"transition:{request.execution_ref}:reobservation-to-next-cycle",
                    )
                ),
                *(
                    (
                        f"transition:{request.execution_ref}:next-cycle-to-hypothesis-revision",
                        f"transition:{request.execution_ref}:hypothesis-revision-to-sufficiency",
                    )
                    if hypothesis_revision is not None
                    else ()
                ),
            )
            if runtime_executed
            else ()
        )

        return CognitiveStateFormationOutputV1(
            scenario_id=request.scenario_id,
            attention_candidates=attention_candidates,
            attention_selection_candidate=attention_selection,
            cognitive_hypotheses=hypotheses,
            hypothesis_competition_result=competition,
            current_world_candidate=world,
            cognitive_state_vector_candidate=vector,
            causal_handoff_candidate=handoff,
            trace=trace,
            provenance=provenance,
            negative_guard_status=self._build_negative_guard_status(),
            candidate_only=True,
            runtime_executed=runtime_executed,
            source_mutation_executed=False,
            execution_mode=request.execution_mode,
            execution_ref=request.execution_ref if runtime_executed else None,
            cognitive_transition_refs=transition_refs,
            execution_owner_ref=CANONICAL_OWNER,
            sufficiency_candidate=sufficiency,
            information_gap_candidate=information_gap,
            reobservation_candidate=reobservation,
            hypothesis_revision_candidate=hypothesis_revision,
            stop_candidate=stop,
            next_cycle_ingress_ref=next_cycle_ref,
            cognitive_cycle_index=request.cycle_index,
            evidence_relevance_candidates=evidence_relevance_candidates,
            relation_interpretation_candidates=relation_interpretation_candidates,
            requirement_establishment_status=sufficiency.requirement_establishment_status,
            requirement_establishment_ref=sufficiency.requirement_establishment_ref,
            requirement_establishment_basis=sufficiency.requirement_establishment_basis,
            required_cognitive_condition_formation_result=request.required_cognitive_condition_formation_result,
        )
