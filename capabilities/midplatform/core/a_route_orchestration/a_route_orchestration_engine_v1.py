from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_engine_v1 import (
    CognitiveStateFormationEngineV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
)
from capabilities.midplatform.core.execution_mode_v1 import (
    CONTROLLED_REPLAY_RUNTIME,
    LIVE_RUNTIME,
    validate_controlled_replay_admission,
    validate_execution_mode,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_static_validators_v1 import (
    validate_runtime_observation_admission,
)

from .a_route_orchestration_core_types_v1 import (
    ARouteHandoffRecordV1,
    ARouteCognitiveExecutionEvidenceV1,
    ARouteOrchestrationRequestV1,
    ARouteOrchestrationResultV1,
    ARouteStageResultV1,
)
from .a_route_orchestration_error_types_v1 import ARouteOrchestrationErrorV1, make_error
from .a_route_orchestration_ownership_guard_v1 import build_negative_guards
from .a_route_orchestration_protocol_v1 import (
    STAGE_PRODUCERS,
    build_handoff,
    stage_contract_ref,
)
from .a_route_orchestration_trace_types_v1 import ARouteTraceV1
from .a_route_information_need_formation_adapter_v1 import (
    ARouteInformationNeedFormationAdapterV1,
)
from .a_route_information_need_formation_types_v1 import (
    ARouteInformationNeedFormationRequestV1,
    ARouteInformationNeedFormationResultV1,
)
from .a_route_minimum_relevant_cognitive_view_engine_v1 import (
    ARouteMinimumRelevantCognitiveViewEngineV1,
)
from .a_route_minimum_relevant_cognitive_view_types_v1 import (
    ARouteMinimumRelevantCognitiveViewRequestV1,
    ARouteMinimumRelevantCognitiveViewCandidateV1,
)
from .a_route_required_cognitive_condition_formation_engine_v1 import (
    ARouteRequiredCognitiveConditionFormationEngineV1,
)
from .a_route_required_cognitive_condition_formation_types_v1 import (
    ARouteRequiredCognitiveConditionFormationRequestV1,
    ARouteRequiredCognitiveConditionFormationResultV1,
)

MAX_RECONSIDERATION_DEPTH = 2


@dataclass(frozen=True)
class _NormalizedAdmissionInformationV1:
    """Execution-mode-normalized information channels for CState."""

    required_information_refs: Tuple[str, ...]
    available_information_refs: Tuple[str, ...]
    evidence_information_refs: Tuple[Tuple[str, Tuple[str, ...]], ...]
    inherited_information_refs: Tuple[str, ...]


class ARouteOrchestrationEngineV1:
    """Deterministic lifecycle/handoff coordinator; it owns no semantic state."""

    @staticmethod
    def form_information_need(
        request: ARouteInformationNeedFormationRequestV1,
    ) -> ARouteInformationNeedFormationResultV1:
        """Expose the read-only Need formation boundary owned by A-Route."""

        return ARouteInformationNeedFormationAdapterV1().form(request)

    @staticmethod
    def form_minimum_relevant_cognitive_view(
        request: ARouteMinimumRelevantCognitiveViewRequestV1,
    ) -> ARouteMinimumRelevantCognitiveViewCandidateV1:
        """Expose the read-only common Self/External view boundary."""

        return ARouteMinimumRelevantCognitiveViewEngineV1().form(request)

    @staticmethod
    def form_required_cognitive_conditions(
        request: ARouteRequiredCognitiveConditionFormationRequestV1,
    ) -> ARouteRequiredCognitiveConditionFormationResultV1:
        """Form governed, state-sensitive conditions before Need formation."""

        return ARouteRequiredCognitiveConditionFormationEngineV1().form(request)

    @staticmethod
    def _execution_identity(request: ARouteOrchestrationRequestV1) -> str:
        return request.execution_identity_ref or request.scenario_id

    def _stage(
        self,
        request: ARouteOrchestrationRequestV1,
        stage_id: str,
        input_refs: Tuple[str, ...],
        output_refs: Tuple[str, ...],
        status: str = "READY",
        stop_reason: str = "",
        defer_reason: str = "",
        error_ref: str = "",
        reconsideration_ref: str = "",
    ) -> ARouteStageResultV1:
        producer, consumer = next(item[1:] for item in STAGE_PRODUCERS if item[0] == stage_id)
        execution_identity = self._execution_identity(request)
        trace_ref = f"trace:{execution_identity}:stage:{stage_id.lower()}"
        return ARouteStageResultV1(
            stage_id=stage_id,
            producer_owner=producer,
            consumer_owner=consumer,
            input_refs=input_refs,
            output_refs=output_refs,
            handoff_contract_ref=stage_contract_ref(stage_id),
            trace_ref=trace_ref,
            provenance_refs=(f"prov:{execution_identity}:stage:{stage_id.lower()}",),
            status=status,
            stop_reason=stop_reason,
            defer_reason=defer_reason,
            error_ref=error_ref,
            reconsideration_ref=reconsideration_ref,
        )

    def _trace(
        self,
        request: ARouteOrchestrationRequestV1,
        stages: Tuple[ARouteStageResultV1, ...],
        handoffs: Tuple[ARouteHandoffRecordV1, ...],
        errors: Tuple[ARouteOrchestrationErrorV1, ...],
        reconsideration_lineage: Tuple[str, ...] = (),
    ) -> ARouteTraceV1:
        sid = self._execution_identity(request)
        stage_refs = tuple(item.trace_ref for item in stages)
        handoff_refs = tuple(item.trace_ref for item in handoffs)
        source_refs = tuple(
            ref
            for ref in (
                *request.ingress.observation_refs,
                *request.ingress.perception_refs,
                *request.ingress.user_input_refs,
                *request.ingress.field_refs,
                *request.ingress.relation_refs,
            )
            if ref
        )
        error_refs = tuple(f"error:{sid}:{item.code}" for item in errors)
        return ARouteTraceV1(
            root_cycle_trace_id=f"root-trace:{sid}",
            cycle_id=f"cycle:{sid}",
            previous_cycle_id=request.previous_cycle_id,
            source_owner_trace_refs=source_refs,
            stage_trace_refs=stage_refs,
            handoff_trace_refs=handoff_refs,
            provenance_refs=tuple(
                ref for item in stages for ref in item.provenance_refs
            ),
            error_refs=error_refs,
            reconsideration_lineage=reconsideration_lineage,
            reverse_lookup_path=(
                f"cycle:{sid}",
                *stage_refs,
                *handoff_refs,
                *source_refs,
            ),
        )

    def _result(
        self,
        request: ARouteOrchestrationRequestV1,
        lifecycle_state: str,
        control_state: str,
        stages: List[ARouteStageResultV1],
        handoffs: List[ARouteHandoffRecordV1],
        errors: List[ARouteOrchestrationErrorV1],
        next_cycle_refs: Tuple[str, ...] = (),
        deferred_refs: Tuple[str, ...] = (),
        reconsideration_lineage: Tuple[str, ...] = (),
        cognitive_execution: ARouteCognitiveExecutionEvidenceV1 | None = None,
    ) -> ARouteOrchestrationResultV1:
        stage_tuple = tuple(stages)
        handoff_tuple = tuple(handoffs)
        error_tuple = tuple(errors)
        return ARouteOrchestrationResultV1(
            scenario_id=request.scenario_id,
            cycle_id=f"cycle:{self._execution_identity(request)}",
            lifecycle_state=lifecycle_state,
            control_state=control_state,
            stage_results=stage_tuple,
            handoffs=handoff_tuple,
            trace=self._trace(
                request, stage_tuple, handoff_tuple, error_tuple, reconsideration_lineage
            ),
            errors=error_tuple,
            negative_guards=build_negative_guards(
                execution_mode=request.execution_mode,
                synthetic_only=request.synthetic_only,
            ),
            next_cycle_ingress_refs=next_cycle_refs,
            deferred_refs=deferred_refs,
            candidate_only=request.candidate_only,
            synthetic_only=request.synthetic_only,
            execution_mode=request.execution_mode,
            cognitive_execution=cognitive_execution,
        )

    @staticmethod
    def _source_ref(
        owner: str,
        source_ref: str,
        execution_ref: str,
        index: int,
        *,
        execution_mode: str = CONTROLLED_REPLAY_RUNTIME,
    ) -> SourceRefV1:
        schema_mode = {
            CONTROLLED_REPLAY_RUNTIME: "controlled-replay",
            LIVE_RUNTIME: "live-runtime",
        }.get(execution_mode, execution_mode.lower())
        return SourceRefV1(
            owner=owner,
            source_ref=source_ref,
            schema_version=f"a-route-{schema_mode}-source-ref-v1",
            trace_ref=f"{execution_ref}:source:{index}",
            provenance_ref=f"{execution_ref}:provenance:{index}",
            read_only=True,
            reference_only=True,
            source_mutation_allowed=False,
        )

    @staticmethod
    def _normalize_admission_information(
        request: ARouteOrchestrationRequestV1,
        admission: object,
    ) -> _NormalizedAdmissionInformationV1:
        """Map each admission contract to the canonical CState channels.

        Controlled replay has only replay-level required/available
        information.  LIVE admission additionally carries evidence bindings
        and inherited information.  The distinction is explicit so a replay
        admission is not made to impersonate a LIVE admission shape.
        """

        if request.execution_mode == CONTROLLED_REPLAY_RUNTIME:
            return _NormalizedAdmissionInformationV1(
                required_information_refs=admission.required_information_refs,
                available_information_refs=admission.available_information_refs,
                evidence_information_refs=(),
                inherited_information_refs=(),
            )
        if request.execution_mode == LIVE_RUNTIME:
            return _NormalizedAdmissionInformationV1(
                required_information_refs=admission.required_information_refs,
                available_information_refs=admission.available_information_refs,
                evidence_information_refs=admission.evidence_information_refs,
                inherited_information_refs=admission.inherited_information_refs,
            )
        raise ValueError("unsupported A-Route admission normalization mode")

    def _run_admitted_runtime(
        self,
        request: ARouteOrchestrationRequestV1,
        stages: List[ARouteStageResultV1],
        handoffs: List[ARouteHandoffRecordV1],
        errors: List[ARouteOrchestrationErrorV1],
    ) -> ARouteOrchestrationResultV1:
        admission = (
            request.replay_admission
            if request.execution_mode == CONTROLLED_REPLAY_RUNTIME
            else request.runtime_admission
        )
        admission_errors = (
            validate_controlled_replay_admission(admission)
            if request.execution_mode == CONTROLLED_REPLAY_RUNTIME
            else ("runtime_admission_missing_or_invalid",)
            if not validate_runtime_observation_admission(admission)
            else ()
        )
        if admission_errors:
            return self._stop(
                request,
                stages,
                handoffs,
                errors,
                "INGRESS",
                "REPLAY_ADMISSION_FAILED",
                ";".join(admission_errors),
        )
        assert admission is not None
        normalized_information = self._normalize_admission_information(
            request, admission
        )
        input_ref = (
            admission.replay_input_ref
            if request.execution_mode == CONTROLLED_REPLAY_RUNTIME
            else admission.runtime_observation_ref
        )
        ingress_refs = tuple(
            ref
            for ref in (
                admission.gateway_admission_ref,
                input_ref,
                *request.ingress.observation_refs,
                *request.ingress.perception_refs,
                *request.ingress.field_refs,
                *request.ingress.relation_refs,
            )
            if ref
        )
        if not request.ingress.observation_refs or not request.ingress.perception_refs:
            return self._stop(
                request,
                stages,
                handoffs,
                errors,
                "INGRESS",
                "REPLAY_INGRESS_REFS_INCOMPLETE",
                "replay requires canonical observation and evidence refs",
                ingress_refs,
            )
        if tuple(request.ingress.perception_refs) != tuple(admission.evidence_refs):
            return self._stop(
                request,
                stages,
                handoffs,
                errors,
                "INGRESS",
                "REPLAY_EVIDENCE_REF_MISMATCH",
                "A-Route evidence refs must match Observation Gateway admission",
                ingress_refs,
            )

        execution_ref = f"a-route-execution:{self._execution_identity(request)}:v1"
        stages.append(
            self._stage(
                request,
                "INGRESS",
                ingress_refs,
                (execution_ref,),
                status="RUNTIME_HANDOFF_READY",
            )
        )
        handoffs.append(
            build_handoff(
                self._execution_identity(request),
                "INGRESS",
                "RUNTIME_HANDOFF_READY",
                controlled=True,
                runtime=True,
            )
        )

        state_refs = tuple(
            self._source_ref("Context Foundation", request.context_ref, execution_ref, 0, execution_mode=request.execution_mode)
            for _ in (request.context_ref,)
            if request.context_ref
        )
        pcn_refs = tuple(
            self._source_ref("Personal Cognitive Network Governance", request.pcn_ref, execution_ref, 1, execution_mode=request.execution_mode)
            for _ in (request.pcn_ref,)
            if request.pcn_ref
        )
        intent_refs = tuple(
            self._source_ref("Intent Governance", request.intent_ref, execution_ref, 2, execution_mode=request.execution_mode)
            for _ in (request.intent_ref,)
            if request.intent_ref
        )
        observation_refs = tuple(
            self._source_ref(
                "Observation Gateway Governance",
                source_ref,
                execution_ref,
                index + 3,
                execution_mode=request.execution_mode,
            )
            for index, source_ref in enumerate(
                (*request.ingress.observation_refs, *request.ingress.perception_refs)
            )
        )
        field_refs = tuple(
            self._source_ref("Field State Reducer", source_ref, execution_ref, index + 3 + len(observation_refs), execution_mode=request.execution_mode)
            for index, source_ref in enumerate(request.ingress.field_refs)
        )
        relation_refs = tuple(
            self._source_ref("Field State Reducer", source_ref, execution_ref, index + 3 + len(observation_refs) + len(field_refs), execution_mode=request.execution_mode)
            for index, source_ref in enumerate(request.ingress.relation_refs)
        )
        role_refs = tuple(
            self._source_ref("Role / Perspective Governance", source_ref, execution_ref, 120 + index, execution_mode=request.execution_mode)
            for index, source_ref in enumerate(request.role_refs)
        )
        task_refs = tuple(
            self._source_ref("Task Manager", source_ref, execution_ref, 130 + index, execution_mode=request.execution_mode)
            for index, source_ref in enumerate(request.task_refs)
        )
        goal_refs = tuple(
            self._source_ref("Goal Governance", source_ref, execution_ref, 140 + index, execution_mode=request.execution_mode)
            for index, source_ref in enumerate(request.goal_refs)
        )
        concern_refs = tuple(
            self._source_ref("Concern Governance", source_ref, execution_ref, 150 + index, execution_mode=request.execution_mode)
            for index, source_ref in enumerate(request.concern_refs)
        )
        information_need_refs = tuple(
            self._source_ref("OWNER_UNRESOLVED", source_ref, execution_ref, 160 + index, execution_mode=request.execution_mode)
            for index, source_ref in enumerate(request.information_need_refs)
        )
        current_world_ref = (
            self._source_ref(
                "Cognitive State Formation Governance",
                admission.prior_current_world_ref,
                execution_ref,
                100,
                execution_mode=request.execution_mode,
            )
            if admission.prior_current_world_ref
            else None
        )
        evidence_refs = tuple(
            self._source_ref(
                "Observation Gateway Governance",
                source_ref,
                execution_ref,
                index + 200,
                execution_mode=request.execution_mode,
            )
            for index, source_ref in enumerate(admission.evidence_refs)
        )
        state_request = CognitiveStateFormationInputV1(
            scenario_id=request.scenario_id,
            context_refs=state_refs,
            pcn_refs=pcn_refs,
            intent_refs=intent_refs,
            field_refs=field_refs,
            observation_refs=observation_refs,
            role_refs=role_refs,
            task_refs=task_refs,
            goal_refs=goal_refs,
            concern_refs=concern_refs,
            information_need_refs=information_need_refs,
            relation_refs=relation_refs,
            relation_interpretation_candidates=request.relation_interpretation_candidates,
            evidence_refs=evidence_refs,
            current_world_ref=current_world_ref,
            required_information_refs=normalized_information.required_information_refs,
            available_information_refs=normalized_information.available_information_refs,
            evidence_information_refs=normalized_information.evidence_information_refs,
            inherited_information_refs=normalized_information.inherited_information_refs,
            prior_current_world_ref=current_world_ref,
            prior_hypothesis_refs=admission.prior_hypothesis_refs,
            prior_information_gap_ref=admission.prior_information_gap_ref,
            prior_reobservation_ref=admission.prior_reobservation_ref,
            prior_next_cycle_ingress_ref=admission.prior_next_cycle_ingress_ref,
            prior_sufficiency_candidate=admission.prior_sufficiency_candidate,
            prior_information_gap_candidate=admission.prior_information_gap_candidate,
            prior_reobservation_candidate=admission.prior_reobservation_candidate,
            cycle_index=admission.cycle_index,
            synthetic_only=False,
            candidate_only=True,
            execution_mode=request.execution_mode,
            replay_input_ref=(
                admission.replay_input_ref
                if request.execution_mode == CONTROLLED_REPLAY_RUNTIME
                else None
            ),
            runtime_observation_ref=(
                admission.runtime_observation_ref
                if request.execution_mode == LIVE_RUNTIME
                else None
            ),
            execution_ref=execution_ref,
        )
        state_output = CognitiveStateFormationEngineV1().run_case(state_request)
        if not state_output.runtime_executed or not state_output.cognitive_transition_refs:
            return self._stop(
                request,
                stages,
                handoffs,
                errors,
                "COGNITIVE_STATE",
                "COGNITIVE_TRANSITION_PROOF_MISSING",
                "canonical Cognitive State Formation did not emit execution evidence",
                (execution_ref,),
                lifecycle_state="FAILED",
                control_state="FAILED",
            )

        loop_output_refs = tuple(
            ref
            for ref in (
                state_output.sufficiency_candidate.sufficiency_ref if state_output.sufficiency_candidate else None,
                state_output.information_gap_candidate.information_gap_ref if state_output.information_gap_candidate else None,
                state_output.reobservation_candidate.reobservation_ref if state_output.reobservation_candidate else None,
                state_output.next_cycle_ingress_ref,
                state_output.hypothesis_revision_candidate.hypothesis_revision_ref if state_output.hypothesis_revision_candidate else None,
                state_output.stop_candidate.stop_ref if state_output.stop_candidate else None,
            )
            if ref
        )
        output_refs = (
            state_output.current_world_candidate.current_world_id,
            *(item.hypothesis_id for item in state_output.cognitive_hypotheses),
            state_output.cognitive_state_vector_candidate.state_vector_id,
            state_output.causal_handoff_candidate.handoff_id,
            *loop_output_refs,
        )
        stages.append(
            self._stage(
                request,
                "COGNITIVE_STATE",
                (execution_ref, *request.ingress.observation_refs, *request.ingress.perception_refs),
                output_refs,
                status="RUNTIME_HANDOFF_READY",
            )
        )
        handoffs.append(
            build_handoff(
                self._execution_identity(request),
                "COGNITIVE_STATE",
                "RUNTIME_HANDOFF_READY",
                controlled=True,
                runtime=True,
            )
        )
        cognitive_execution = ARouteCognitiveExecutionEvidenceV1(
            execution_ref=execution_ref,
            execution_mode=request.execution_mode,
            owner_ref="Cognitive State Formation Governance",
            ingress_refs=ingress_refs,
            cognitive_transition_refs=state_output.cognitive_transition_refs,
            current_world_ref=state_output.current_world_candidate.current_world_id,
            hypothesis_refs=tuple(item.hypothesis_id for item in state_output.cognitive_hypotheses),
            current_world_availability="observed",
            hypothesis_availability="observed",
            sufficiency_ref=state_output.sufficiency_candidate.sufficiency_ref if state_output.sufficiency_candidate else None,
            sufficiency_availability="observed" if state_output.sufficiency_candidate else "not_observed",
            information_gap_ref=state_output.information_gap_candidate.information_gap_ref if state_output.information_gap_candidate else None,
            information_gap_availability="observed" if state_output.information_gap_candidate else "not_observed",
            stop_ref=state_output.stop_candidate.stop_ref if state_output.stop_candidate else None,
            stop_availability="observed" if state_output.stop_candidate else "not_observed",
            decision_handoff_ref=None,
            decision_handoff_availability="not_observed",
            runtime_executed=True,
            execution_proof_source="CognitiveStateFormationEngineV1.run_case",
            cognitive_cycle_index=state_output.cognitive_cycle_index,
            sufficiency_status=state_output.sufficiency_candidate.status if state_output.sufficiency_candidate else "not_observed",
            sufficiency_owner_ref=state_output.sufficiency_candidate.owner_ref if state_output.sufficiency_candidate else None,
            sufficiency_candidate=state_output.sufficiency_candidate,
            information_gap_owner_ref=state_output.information_gap_candidate.owner_ref if state_output.information_gap_candidate else None,
            information_gap_candidate=state_output.information_gap_candidate,
            reobservation_ref=state_output.reobservation_candidate.reobservation_ref if state_output.reobservation_candidate else None,
            reobservation_owner_ref=state_output.reobservation_candidate.owner_ref if state_output.reobservation_candidate else None,
            reobservation_candidate=state_output.reobservation_candidate,
            reobservation_information_gap_ref=state_output.reobservation_candidate.information_gap_ref if state_output.reobservation_candidate else None,
            next_cycle_ingress_ref=state_output.next_cycle_ingress_ref,
            prior_next_cycle_ingress_ref=admission.prior_next_cycle_ingress_ref,
            hypothesis_revision_ref=state_output.hypothesis_revision_candidate.hypothesis_revision_ref if state_output.hypothesis_revision_candidate else None,
            hypothesis_revision_owner_ref=state_output.hypothesis_revision_candidate.owner_ref if state_output.hypothesis_revision_candidate else None,
            hypothesis_revision_information_gap_ref=state_output.hypothesis_revision_candidate.information_gap_ref if state_output.hypothesis_revision_candidate else None,
            hypothesis_revision_reobservation_ref=state_output.hypothesis_revision_candidate.reobservation_ref if state_output.hypothesis_revision_candidate else None,
            stop_reason=state_output.stop_candidate.reason if state_output.stop_candidate else None,
            stop_owner_ref=state_output.stop_candidate.owner_ref if state_output.stop_candidate else None,
            role_refs=tuple(r.source_ref for r in state_request.role_refs),
            task_refs=tuple(r.source_ref for r in state_request.task_refs),
            goal_refs=tuple(r.source_ref for r in state_request.goal_refs),
            concern_refs=tuple(r.source_ref for r in state_request.concern_refs),
            information_need_refs=tuple(r.source_ref for r in state_request.information_need_refs),
            conditioned_attention_refs=tuple(
                item.attention_id for item in state_output.attention_candidates
            ),
            conditioned_evidence_relevance_refs=tuple(
                item.relevance_ref for item in state_output.evidence_relevance_candidates
            ),
            relation_interpretation_refs=tuple(
                item.relation_interpretation_ref
                for item in state_output.relation_interpretation_candidates
            ),
            conditioned_attention_priority_candidate=(
                state_output.attention_candidates[0].attention_priority_candidate
                if state_output.attention_candidates else None
            ),
            conditioned_attention_relevance_candidate=(
                state_output.attention_candidates[0].relevance_score_candidate
                if state_output.attention_candidates else None
            ),
            conditioned_hypothesis_statement=(
                state_output.cognitive_hypotheses[0].hypothesis_statement_candidate
                if state_output.cognitive_hypotheses else None
            ),
            conditioned_hypothesis_state=(
                state_output.cognitive_hypotheses[0].state
                if state_output.cognitive_hypotheses else None
            ),
            conditioned_world_kind_candidate=state_output.current_world_candidate.world_state_kind_candidate,
            conditioned_missing_information_refs=(
                state_output.sufficiency_candidate.missing_information_refs
                if state_output.sufficiency_candidate else ()
            ),
            field_refs=tuple(r.source_ref for r in state_request.field_refs),
            selected_attention_count=len(state_output.attention_selection_candidate.selected_attention_refs),
            conditioned_evidence_relevance=tuple(
                f"{item.evidence_ref}:{item.relevance_state}:{item.relevance_score_candidate}"
                for item in state_output.evidence_relevance_candidates
            ),
            relation_interpretation_candidates=tuple(
                item.interpretation_candidate
                for item in state_output.relation_interpretation_candidates
            ),
            relation_interpretation_semantic_candidates=state_output.relation_interpretation_candidates,
            current_world_relation_interpretation_refs=state_output.current_world_candidate.relation_interpretation_refs,
            conditioned_conflict_refs=state_output.current_world_candidate.conflict_refs,
        )
        if state_output.sufficiency_candidate and state_output.sufficiency_candidate.status == "SUFFICIENT":
            return self._result(
                request,
                "COGNITIVE_STATE_READY",
                "STOPPED",
                stages,
                handoffs,
                errors,
                cognitive_execution=cognitive_execution,
            )
        return self._result(
            request,
            "COGNITIVE_STATE_READY",
            "DEFERRED",
            stages,
            handoffs,
            errors,
            next_cycle_refs=(state_output.next_cycle_ingress_ref,) if state_output.next_cycle_ingress_ref else (),
            deferred_refs=("minimum_sufficient_loop_requires_next_cycle",),
            cognitive_execution=cognitive_execution,
        )

    def _stop(
        self,
        request: ARouteOrchestrationRequestV1,
        stages: List[ARouteStageResultV1],
        handoffs: List[ARouteHandoffRecordV1],
        errors: List[ARouteOrchestrationErrorV1],
        stage_id: str,
        code: str,
        message: str,
        input_refs: Tuple[str, ...] = (),
        lifecycle_state: str = "STOPPED",
        control_state: str = "STOPPED",
    ) -> ARouteOrchestrationResultV1:
        sid = self._execution_identity(request)
        error_ref = f"error:{sid}:{code}"
        errors.append(make_error(code, stage_id, message, code in {"CONTRACT_MISMATCH", "VERSION_MISMATCH", "OWNER_AUTHORITY_VIOLATION"}, input_refs, f"trace:{sid}:stage:{stage_id.lower()}"))
        stages.append(self._stage(request, stage_id, input_refs, (), "STOPPED" if control_state == "STOPPED" else control_state, message, error_ref=error_ref))
        handoffs.append(build_handoff(sid, stage_id, "BLOCKED", controlled=False))
        return self._result(request, lifecycle_state, control_state, stages, handoffs, errors)

    def run_case(self, request: ARouteOrchestrationRequestV1) -> ARouteOrchestrationResultV1:
        stages: List[ARouteStageResultV1] = []
        handoffs: List[ARouteHandoffRecordV1] = []
        errors: List[ARouteOrchestrationErrorV1] = []
        sid = self._execution_identity(request)

        mode_errors = validate_execution_mode(
            request.execution_mode,
            synthetic_only=request.synthetic_only,
        )
        if mode_errors:
            return self._stop(request, stages, handoffs, errors, "INGRESS", "INVALID_EXECUTION_MODE", ";".join(mode_errors))
        if request.execution_mode in {CONTROLLED_REPLAY_RUNTIME, LIVE_RUNTIME}:
            if not request.candidate_only:
                return self._stop(request, stages, handoffs, errors, "INGRESS", "AUTHORITY_MODE_VIOLATION", "runtime observation requires candidate-only refs")
            return self._run_admitted_runtime(request, stages, handoffs, errors)

        if not request.synthetic_only or not request.candidate_only:
            return self._stop(request, stages, handoffs, errors, "INGRESS", "AUTHORITY_MODE_VIOLATION", "controlled integration requires synthetic candidate mode")
        if request.duplicate_cycle:
            return self._stop(request, stages, handoffs, errors, "INGRESS", "DUPLICATE_CYCLE_START", "cycle start already admitted")
        if request.completed_cycle_mutation_probe:
            return self._stop(request, stages, handoffs, errors, "PERSONALITY_CONTEXT", "COMPLETED_CYCLE_IMMUTABLE", "completed cycle cannot be mutated")
        if request.contract_mismatch:
            return self._stop(request, stages, handoffs, errors, "INGRESS", "CONTRACT_MISMATCH", "orchestration contract mismatch", lifecycle_state="FAILED", control_state="FAILED")
        if request.version_mismatch:
            return self._stop(request, stages, handoffs, errors, "INGRESS", "VERSION_MISMATCH", "orchestration version mismatch", lifecycle_state="FAILED", control_state="FAILED")
        if request.owner_authority_violation:
            return self._stop(request, stages, handoffs, errors, "INGRESS", "OWNER_AUTHORITY_VIOLATION", "orchestration cannot mutate a source owner", lifecycle_state="FAILED", control_state="FAILED")
        if request.repeated_failure_signature:
            return self._stop(request, stages, handoffs, errors, "INGRESS", "REPEATED_FAILURE_SIGNATURE", "repeated failure signature is terminal for this controlled cycle")

        if request.real_ingress_unavailable:
            stages.append(self._stage(request, "INGRESS", (), (), "DEFERRED", defer_reason="DEFERRED_TO_PERCEPTION_OBSERVATION_GATEWAY"))
            handoffs.append(build_handoff(sid, "INGRESS", "DEFERRED", controlled=False))
            return self._result(request, "IDLE", "DEFERRED", stages, handoffs, errors, deferred_refs=("DEFERRED_TO_PERCEPTION_OBSERVATION_GATEWAY",))

        ingress_refs = (
            *request.ingress.observation_refs,
            *request.ingress.perception_refs,
            *request.ingress.user_input_refs,
            *request.ingress.field_refs,
        )
        if request.missing_ingress or not ingress_refs:
            return self._stop(request, stages, handoffs, errors, "INGRESS", "MISSING_STAGE_INPUT", "perception/observation ingress is incomplete")
        stages.append(self._stage(request, "INGRESS", ingress_refs, (f"observation:{sid}",)))
        handoffs.append(build_handoff(sid, "INGRESS", "CONTROLLED_HANDOFF_READY"))

        if request.duplicate_handoff:
            return self._stop(request, stages, handoffs, errors, "INGRESS", "DUPLICATE_HANDOFF", "stage handoff already consumed", ingress_refs)

        refs = f"observation:{sid}", *request.ingress.field_refs
        if request.missing_context or not request.context_ref:
            return self._stop(request, stages, handoffs, errors, "CONTEXT", "MISSING_STAGE_INPUT", "context input is incomplete", refs)
        stages.append(self._stage(request, "CONTEXT", refs, (request.context_ref,)))
        handoffs.append(build_handoff(sid, "CONTEXT", "CONTROLLED_HANDOFF_READY"))

        if request.missing_pcn or not request.pcn_ref:
            return self._stop(request, stages, handoffs, errors, "PCN", "MISSING_STAGE_INPUT", "PCN input is incomplete", (request.context_ref,))
        stages.append(self._stage(request, "PCN", (request.context_ref,), (request.pcn_ref,)))
        handoffs.append(build_handoff(sid, "PCN", "CONTROLLED_HANDOFF_READY"))

        if request.missing_intent or not request.intent_ref:
            return self._stop(request, stages, handoffs, errors, "INTENT", "MISSING_STAGE_INPUT", "intent input is incomplete", (request.pcn_ref,))
        stages.append(self._stage(request, "INTENT", (request.pcn_ref,), (request.intent_ref,)))
        handoffs.append(build_handoff(sid, "INTENT", "CONTROLLED_HANDOFF_READY"))

        if request.missing_cognitive_state or not request.cognitive_state_ref:
            return self._stop(request, stages, handoffs, errors, "COGNITIVE_STATE", "MISSING_STAGE_INPUT", "cognitive state input is incomplete", (request.intent_ref,))
        stages.append(self._stage(request, "COGNITIVE_STATE", (request.intent_ref,), (request.cognitive_state_ref,)))
        handoffs.append(build_handoff(sid, "COGNITIVE_STATE", "CONTROLLED_HANDOFF_READY"))

        if request.reconsideration_requested:
            if request.duplicate_reconsideration:
                return self._stop(request, stages, handoffs, errors, "COGNITIVE_STATE", "DUPLICATE_RECONSIDERATION", "reconsideration request already consumed")
            if request.reconsideration_depth > MAX_RECONSIDERATION_DEPTH:
                return self._stop(request, stages, handoffs, errors, "COGNITIVE_STATE", "RECONSIDERATION_DEPTH_EXCEEDED", "maximum reconsideration depth exceeded", (request.cognitive_state_ref,), "FAILED", "FAILED")
            reconsider_ref = f"reconsider:{sid}:cognitive-state"
            stages[-1] = self._stage(request, "COGNITIVE_STATE", (request.intent_ref,), (request.cognitive_state_ref,), "RECONSIDERING", reconsideration_ref=reconsider_ref)
            errors.append(make_error("RECONSIDERATION_REQUESTED", "COGNITIVE_STATE", "upstream evidence requires reconsideration", False, (request.cognitive_state_ref,), stages[-1].trace_ref))
            return self._result(request, "COGNITIVE_STATE_READY", "RECONSIDERING", stages, handoffs, errors, reconsideration_lineage=(reconsider_ref,))

        if request.missing_regulation or not request.regulation_ref:
            return self._stop(request, stages, handoffs, errors, "REGULATION", "MISSING_STAGE_INPUT", "regulation input is incomplete", (request.cognitive_state_ref,))
        stages.append(self._stage(request, "REGULATION", (request.cognitive_state_ref,), (request.regulation_ref,)))
        handoffs.append(build_handoff(sid, "REGULATION", "CONTROLLED_HANDOFF_READY"))

        if request.missing_decision or not request.decision_ref:
            code = "UPSTREAM_FAILURE_PROPAGATION" if request.upstream_failure else "MISSING_STAGE_INPUT"
            return self._stop(request, stages, handoffs, errors, "DECISION", code, "decision input is unavailable", (request.regulation_ref,))
        stages.append(self._stage(request, "DECISION", (request.regulation_ref,), (request.decision_ref,)))
        handoffs.append(build_handoff(sid, "DECISION", "CONTROLLED_HANDOFF_READY"))

        if request.defer_task or not request.task_ref:
            stages.append(self._stage(request, "TASK", (request.decision_ref,), (), "DEFERRED", defer_reason="DEFERRED_TO_TASK_MANAGER_PRODUCT_LIFECYCLE"))
            handoffs.append(build_handoff(sid, "TASK", "DEFERRED", controlled=False))
            return self._result(request, "TASK_READY", "DEFERRED", stages, handoffs, errors, deferred_refs=("task_manager_product_lifecycle",))
        stages.append(self._stage(request, "TASK", (request.decision_ref,), (request.task_ref,)))
        handoffs.append(build_handoff(sid, "TASK", "CONTROLLED_HANDOFF_READY"))

        if request.defer_action or not request.action_ref:
            stages.append(self._stage(request, "ACTION", (request.task_ref,), (), "DEFERRED", defer_reason="DEFERRED_TO_ACTION_ROUTING_PRODUCT_ADMISSION"))
            handoffs.append(build_handoff(sid, "ACTION", "DEFERRED", controlled=False))
            return self._result(request, "ACTION_READY", "DEFERRED", stages, handoffs, errors, deferred_refs=("action_routing_product_admission",))
        stages.append(self._stage(request, "ACTION", (request.task_ref,), (request.action_ref,)))
        handoffs.append(build_handoff(sid, "ACTION", "CONTROLLED_HANDOFF_READY"))

        if request.defer_runtime or not request.runtime_ref:
            stages.append(self._stage(request, "EXECUTION", (request.action_ref,), (), "DEFERRED", defer_reason="DEFERRED_TO_RUNTIME_EXECUTOR_PRODUCT_HANDOFF"))
            handoffs.append(build_handoff(sid, "EXECUTION", "DEFERRED", controlled=False))
            return self._result(request, "EXECUTION_READY", "DEFERRED", stages, handoffs, errors, deferred_refs=("runtime_executor_product_handoff",))
        stages.append(self._stage(request, "EXECUTION", (request.action_ref,), (request.runtime_ref,)))
        handoffs.append(build_handoff(sid, "EXECUTION", "CONTROLLED_HANDOFF_READY", controlled=True, runtime=False))

        if not request.result_returned or not request.result_ref:
            return self._stop(request, stages, handoffs, errors, "RESULT", "MISSING_STAGE_INPUT", "result feedback is unavailable", (request.runtime_ref,))
        stages.append(self._stage(request, "RESULT", (request.runtime_ref,), (request.result_ref,)))
        handoffs.append(build_handoff(sid, "RESULT", "CONTROLLED_HANDOFF_READY"))

        if request.duplicate_feedback:
            return self._stop(request, stages, handoffs, errors, "FEEDBACK", "DUPLICATE_RESULT_FEEDBACK", "result feedback already admitted", (request.result_ref,))
        feedback_ref = f"comparison:{sid}"
        stages.append(self._stage(request, "FEEDBACK", (request.result_ref,), (feedback_ref,)))
        handoffs.append(build_handoff(sid, "FEEDBACK", "CONTROLLED_HANDOFF_READY"))

        stages.append(self._stage(request, "MEMORY_EXPERIENCE", (feedback_ref,), (request.memory_experience_ref or f"experience:{sid}",)))
        handoffs.append(build_handoff(sid, "MEMORY_EXPERIENCE", "CONTROLLED_HANDOFF_READY"))
        stages.append(self._stage(request, "LEARNING", (request.memory_experience_ref or f"experience:{sid}",), (request.learning_ref or f"learning:{sid}",)))
        handoffs.append(build_handoff(sid, "LEARNING", "CONTROLLED_HANDOFF_READY"))
        stages.append(self._stage(request, "SELF_CONTINUITY", (request.learning_ref or f"learning:{sid}",), (request.self_ref or f"self:{sid}",)))
        handoffs.append(build_handoff(sid, "SELF_CONTINUITY", "CONTROLLED_HANDOFF_READY"))
        next_refs = (request.personality_ref or f"personality:{sid}", feedback_ref, f"cycle:{sid}:next-ingress")
        stages.append(self._stage(request, "PERSONALITY_CONTEXT", (request.self_ref or f"self:{sid}",), next_refs))
        handoffs.append(build_handoff(sid, "PERSONALITY_CONTEXT", "CONTROLLED_HANDOFF_READY"))
        deferred_refs = tuple(
            ref
            for ref, enabled in (
                ("emotion_engine", request.emotion_deferred),
                ("b_route", request.b_route_deferred),
                ("semantic_compression", request.semantic_compression_deferred),
            )
            if enabled
        )
        return self._result(request, "CYCLE_COMPLETE", "CYCLE_COMPLETE", stages, handoffs, errors, next_cycle_refs=next_refs, deferred_refs=deferred_refs)
