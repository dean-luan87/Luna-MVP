from __future__ import annotations

from typing import List, Tuple

from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    ActionGovernanceEngineV1,
)
from capabilities.midplatform.core.causal_governance.causal_governance_engine_v1 import (
    CausalGovernanceEngineV1,
)
from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_compatibility_v1 import (
    decide_compatibility,
    get_default_hop_version,
)
from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_error_types_v1 import (
    CognitiveExecutionChainErrorV1,
    make_error,
)
from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_handoff_mapping_v1 import (
    build_intent_input,
    map_action_to_runtime,
    map_causal_to_decision,
    map_decision_to_action,
    map_intent_to_causal,
)
from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_idempotency_v1 import (
    CrossLayerIdempotencyRegistryV1,
)
from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_reconsideration_v1 import (
    build_action_feedback_reconsideration,
    build_runtime_feedback_reconsideration,
)
from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_trace_types_v1 import (
    EndToEndTraceV1,
    ProvenanceReversePathV1,
)
from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_types_v1 import (
    DiagnosticsCandidateV1,
    HandoffEnvelopeV1,
    IntegrationExecutionRecordV1,
    IntegrationScenarioDirectiveV1,
    ReconsiderationCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_governance_engine_v1 import (
    DecisionGovernanceEngineV1,
)
from capabilities.midplatform.core.intent_governance.intent_governance_skeleton_v1 import (
    IntentGovernanceSkeletonV1,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_engine_v1 import (
    RuntimeExecutorEngineV1,
)


class CognitiveExecutionChainEngineV1:
    def __init__(self) -> None:
        self._intent_engine = IntentGovernanceSkeletonV1()
        self._causal_engine = CausalGovernanceEngineV1()
        self._decision_engine = DecisionGovernanceEngineV1()
        self._action_engine = ActionGovernanceEngineV1()
        self._runtime_engine = RuntimeExecutorEngineV1()
        self._idempotency = CrossLayerIdempotencyRegistryV1()

    def _compatibility_gate(
        self,
        directive: IntegrationScenarioDirectiveV1,
        hop_id: str,
    ):
        return decide_compatibility(
            hop_id=hop_id,
            directive_force_incompatible_hop=directive.force_version_incompatible_hop,
            directive_force_migration_required_hop=directive.force_version_migration_required_hop,
        )

    def _trace_gate(
        self,
        directive: IntegrationScenarioDirectiveV1,
        hop_id: str,
        envelope: HandoffEnvelopeV1,
    ) -> bool:
        if directive.force_missing_trace_hop == hop_id:
            return False
        return bool(envelope.trace_ref)

    def _diagnostics_candidate(
        self,
        origin_layer: str,
        error_namespace: str,
        trace_refs: Tuple[str, ...],
        failure_category: str,
        remediation_candidate_refs: Tuple[str, ...],
    ) -> DiagnosticsCandidateV1:
        return DiagnosticsCandidateV1(
            origin_layer=origin_layer,
            error_namespace=error_namespace,
            trace_refs=trace_refs,
            failure_category=failure_category,
            remediation_candidate_refs=remediation_candidate_refs,
        )

    def _make_trace(
        self,
        scenario_id: str,
        intent_trace_ref: str,
        causal_trace_ref: str,
        decision_trace_ref: str,
        action_trace_ref: str,
        execution_trace_ref: str,
    ) -> EndToEndTraceV1:
        return EndToEndTraceV1(
            root_trace_id=f"root-trace:{scenario_id}",
            intent_trace_ref=intent_trace_ref,
            causal_trace_ref=causal_trace_ref,
            decision_trace_ref=decision_trace_ref,
            action_trace_ref=action_trace_ref,
            execution_trace_ref=execution_trace_ref,
            candidate_only=True,
        )

    def _build_record(
        self,
        scenario_id: str,
        stopped_at: str,
        runtime_attempted: bool,
        handoff_path: Tuple[str, ...],
        compatibility,
        trace: EndToEndTraceV1,
        provenance: ProvenanceReversePathV1,
        reconsideration_candidates: Tuple[ReconsiderationCandidateV1, ...],
        diagnostics_candidates: Tuple[DiagnosticsCandidateV1, ...],
        errors: Tuple[CognitiveExecutionChainErrorV1, ...],
        metadata: dict[str, str],
    ) -> IntegrationExecutionRecordV1:
        return IntegrationExecutionRecordV1(
            scenario_id=scenario_id,
            stopped_at=stopped_at,
            runtime_attempted=runtime_attempted,
            runtime_side_effect=False,
            owner_bypass=False,
            runtime_bypass=False,
            handoff_path=handoff_path,
            compatibility=tuple(compatibility),
            end_to_end_trace=trace,
            provenance=provenance,
            reconsideration_candidates=reconsideration_candidates,
            diagnostics_candidates=diagnostics_candidates,
            errors=errors,
            metadata=metadata,
        )

    def run_case(
        self, directive: IntegrationScenarioDirectiveV1
    ) -> IntegrationExecutionRecordV1:
        scenario_id = directive.scenario_id
        compatibility: List = []
        errors: List[CognitiveExecutionChainErrorV1] = []
        handoff_path: List[str] = []
        diagnostics: List[DiagnosticsCandidateV1] = []
        reconsideration: List[ReconsiderationCandidateV1] = []
        metadata: dict[str, str] = {"category": directive.category}

        # L1 Intent
        intent_input = build_intent_input(scenario_id)
        intent_output = self._intent_engine.run_case(intent_input)

        # H1 Intent -> Causal
        h1_input, h1_env = map_intent_to_causal(
            scenario_id,
            intent_output,
            directive,
            get_default_hop_version("H1"),
        )
        h1_cmp = self._compatibility_gate(directive, "H1")
        compatibility.append(h1_cmp)

        if not self._trace_gate(directive, "H1", h1_env):
            errors.append(
                make_error(
                    "H1_MISSING_TRACE", "missing trace ref in H1", "trace", False
                )
            )
            return self._build_record(
                scenario_id,
                stopped_at="H1_TRACE_REJECTED",
                runtime_attempted=False,
                handoff_path=tuple(handoff_path),
                compatibility=compatibility,
                trace=self._make_trace(
                    scenario_id, intent_output.trace_candidate.trace_id, "", "", "", ""
                ),
                provenance=ProvenanceReversePathV1(
                    execution_result_ref="not-executed",
                    action_candidate_ref="not-executed",
                    decision_candidate_ref=None,
                    causal_hypothesis_refs=(),
                    intent_candidate_refs=tuple(
                        x.intent_id for x in intent_output.intent_candidates
                    ),
                    source_evidence_or_context_refs=tuple(
                        x.ref_id for x in intent_input.context_refs
                    ),
                    reverse_locatable=False,
                ),
                reconsideration_candidates=(),
                diagnostics_candidates=(),
                errors=tuple(errors),
                metadata=metadata,
            )

        if not h1_cmp.allow_handoff:
            errors.append(
                make_error("H1_COMPAT_BLOCK", h1_cmp.reason, "compatibility", False)
            )
            return self._build_record(
                scenario_id,
                stopped_at="H1_COMPATIBILITY_REJECTED",
                runtime_attempted=False,
                handoff_path=tuple(handoff_path),
                compatibility=compatibility,
                trace=self._make_trace(
                    scenario_id, intent_output.trace_candidate.trace_id, "", "", "", ""
                ),
                provenance=ProvenanceReversePathV1(
                    execution_result_ref="not-executed",
                    action_candidate_ref="not-executed",
                    decision_candidate_ref=None,
                    causal_hypothesis_refs=(),
                    intent_candidate_refs=tuple(
                        x.intent_id for x in intent_output.intent_candidates
                    ),
                    source_evidence_or_context_refs=tuple(
                        x.ref_id for x in intent_input.context_refs
                    ),
                    reverse_locatable=False,
                ),
                reconsideration_candidates=(),
                diagnostics_candidates=(),
                errors=tuple(errors),
                metadata=metadata,
            )

        if directive.duplicate_handoff_probe:
            self._idempotency.consume_handoff_once(h1_env.handoff_id)

        if not self._idempotency.consume_handoff_once(h1_env.handoff_id):
            errors.append(
                make_error(
                    "H1_DUPLICATE_HANDOFF",
                    "duplicate H1 handoff consumed",
                    "idempotency",
                    True,
                )
            )
            metadata["duplicate_handoff_guard_triggered"] = "true"
            return self._build_record(
                scenario_id,
                stopped_at="H1_DUPLICATE_GUARD_STOP",
                runtime_attempted=False,
                handoff_path=tuple(handoff_path),
                compatibility=compatibility,
                trace=self._make_trace(
                    scenario_id, intent_output.trace_candidate.trace_id, "", "", "", ""
                ),
                provenance=ProvenanceReversePathV1(
                    execution_result_ref="not-executed",
                    action_candidate_ref="not-executed",
                    decision_candidate_ref=None,
                    causal_hypothesis_refs=(),
                    intent_candidate_refs=tuple(
                        x.intent_id for x in intent_output.intent_candidates
                    ),
                    source_evidence_or_context_refs=tuple(
                        x.ref_id for x in intent_input.context_refs
                    ),
                    reverse_locatable=False,
                ),
                reconsideration_candidates=(),
                diagnostics_candidates=(),
                errors=tuple(errors),
                metadata=metadata,
            )

        handoff_path.append("H1")

        # L2 Causal
        causal_output = self._causal_engine.run_case(h1_input)

        # H2 Causal -> Decision
        h2_input, h2_env = map_causal_to_decision(
            scenario_id,
            causal_output,
            directive,
            get_default_hop_version("H2"),
        )
        h2_cmp = self._compatibility_gate(directive, "H2")
        compatibility.append(h2_cmp)

        if not self._trace_gate(directive, "H2", h2_env):
            errors.append(
                make_error(
                    "H2_MISSING_TRACE", "missing trace ref in H2", "trace", False
                )
            )
            return self._build_record(
                scenario_id,
                stopped_at="H2_TRACE_REJECTED",
                runtime_attempted=False,
                handoff_path=tuple(handoff_path),
                compatibility=compatibility,
                trace=self._make_trace(
                    scenario_id,
                    intent_output.trace_candidate.trace_id,
                    causal_output.trace_candidate.trace_id,
                    "",
                    "",
                    "",
                ),
                provenance=ProvenanceReversePathV1(
                    execution_result_ref="not-executed",
                    action_candidate_ref="not-executed",
                    decision_candidate_ref=None,
                    causal_hypothesis_refs=tuple(
                        x.hypothesis_id for x in causal_output.hypothesis_candidates
                    ),
                    intent_candidate_refs=tuple(
                        x.intent_id for x in intent_output.intent_candidates
                    ),
                    source_evidence_or_context_refs=tuple(
                        x.ref_id for x in h1_input.context_refs
                    ),
                    reverse_locatable=False,
                ),
                reconsideration_candidates=(),
                diagnostics_candidates=(),
                errors=tuple(errors),
                metadata=metadata,
            )

        if not h2_cmp.allow_handoff:
            errors.append(
                make_error(
                    "H2_COMPAT_BLOCK",
                    h2_cmp.reason,
                    "compatibility",
                    h2_cmp.hard_block is False,
                )
            )
            return self._build_record(
                scenario_id,
                stopped_at="H2_COMPATIBILITY_REJECTED",
                runtime_attempted=False,
                handoff_path=tuple(handoff_path),
                compatibility=compatibility,
                trace=self._make_trace(
                    scenario_id,
                    intent_output.trace_candidate.trace_id,
                    causal_output.trace_candidate.trace_id,
                    "",
                    "",
                    "",
                ),
                provenance=ProvenanceReversePathV1(
                    execution_result_ref="not-executed",
                    action_candidate_ref="not-executed",
                    decision_candidate_ref=None,
                    causal_hypothesis_refs=tuple(
                        x.hypothesis_id for x in causal_output.hypothesis_candidates
                    ),
                    intent_candidate_refs=tuple(
                        x.intent_id for x in intent_output.intent_candidates
                    ),
                    source_evidence_or_context_refs=tuple(
                        x.ref_id for x in h1_input.context_refs
                    ),
                    reverse_locatable=False,
                ),
                reconsideration_candidates=(),
                diagnostics_candidates=(),
                errors=tuple(errors),
                metadata=metadata,
            )

        if not self._idempotency.consume_handoff_once(h2_env.handoff_id):
            errors.append(
                make_error(
                    "H2_DUPLICATE_HANDOFF",
                    "duplicate H2 handoff consumed",
                    "idempotency",
                    True,
                )
            )
            metadata["duplicate_handoff_guard_triggered"] = "true"

        handoff_path.append("H2")

        # L3 Decision
        decision_output = self._decision_engine.run_case(h2_input)

        if decision_output.outcome_kind in {
            "DEFER",
            "ABSTAIN",
            "REQUEST_MORE_EVIDENCE",
            "CONTESTED",
            "CONSTRAINED",
        }:
            stopped_at = "DECISION_STOP_BEFORE_ACTION"
            if decision_output.outcome_kind == "DEFER":
                stopped_at = "DECISION_DEFER_STOP"
            elif decision_output.outcome_kind == "ABSTAIN":
                stopped_at = "DECISION_ABSTAIN_STOP"
            elif (
                decision_output.outcome_kind == "CONSTRAINED"
                and directive.force_decision_permission_veto
            ):
                stopped_at = "DECISION_PERMISSION_VETO_STOP"

            diagnostics.append(
                self._diagnostics_candidate(
                    origin_layer="Decision Governance",
                    error_namespace="decision_governance.controlled_implementation.v1",
                    trace_refs=(decision_output.trace_candidate.trace_id,),
                    failure_category=decision_output.outcome_kind,
                    remediation_candidate_refs=(
                        decision_output.handoff_candidate.handoff_id,
                    ),
                )
            )

            return self._build_record(
                scenario_id,
                stopped_at=stopped_at,
                runtime_attempted=False,
                handoff_path=tuple(handoff_path),
                compatibility=compatibility,
                trace=self._make_trace(
                    scenario_id,
                    intent_output.trace_candidate.trace_id,
                    causal_output.trace_candidate.trace_id,
                    decision_output.trace_candidate.trace_id,
                    "not-executed:action",
                    "not-executed:runtime",
                ),
                provenance=ProvenanceReversePathV1(
                    execution_result_ref="not-executed",
                    action_candidate_ref="not-executed",
                    decision_candidate_ref=decision_output.selection_candidate.selected_candidate_ref,
                    causal_hypothesis_refs=tuple(
                        x.hypothesis_id for x in causal_output.hypothesis_candidates
                    ),
                    intent_candidate_refs=tuple(
                        x.intent_id for x in intent_output.intent_candidates
                    ),
                    source_evidence_or_context_refs=tuple(
                        x.ref_id for x in h1_input.context_refs
                    ),
                    reverse_locatable=True,
                ),
                reconsideration_candidates=(),
                diagnostics_candidates=tuple(diagnostics),
                errors=tuple(errors),
                metadata=metadata,
            )

        # H3 Decision -> Action
        h3_input, h3_env = map_decision_to_action(
            scenario_id,
            decision_output,
            directive,
            get_default_hop_version("H3"),
        )
        h3_cmp = self._compatibility_gate(directive, "H3")
        compatibility.append(h3_cmp)

        if not self._trace_gate(directive, "H3", h3_env):
            errors.append(
                make_error(
                    "H3_MISSING_TRACE", "missing trace ref in H3", "trace", False
                )
            )
            return self._build_record(
                scenario_id,
                stopped_at="H3_TRACE_REJECTED",
                runtime_attempted=False,
                handoff_path=tuple(handoff_path),
                compatibility=compatibility,
                trace=self._make_trace(
                    scenario_id,
                    intent_output.trace_candidate.trace_id,
                    causal_output.trace_candidate.trace_id,
                    decision_output.trace_candidate.trace_id,
                    "",
                    "",
                ),
                provenance=ProvenanceReversePathV1(
                    execution_result_ref="not-executed",
                    action_candidate_ref="not-executed",
                    decision_candidate_ref=decision_output.selection_candidate.selected_candidate_ref,
                    causal_hypothesis_refs=tuple(
                        x.hypothesis_id for x in causal_output.hypothesis_candidates
                    ),
                    intent_candidate_refs=tuple(
                        x.intent_id for x in intent_output.intent_candidates
                    ),
                    source_evidence_or_context_refs=tuple(
                        x.ref_id for x in h1_input.context_refs
                    ),
                    reverse_locatable=False,
                ),
                reconsideration_candidates=(),
                diagnostics_candidates=tuple(diagnostics),
                errors=tuple(errors),
                metadata=metadata,
            )

        if not h3_cmp.allow_handoff:
            errors.append(
                make_error(
                    "H3_COMPAT_BLOCK",
                    h3_cmp.reason,
                    "compatibility",
                    h3_cmp.hard_block is False,
                )
            )
            return self._build_record(
                scenario_id,
                stopped_at="H3_COMPATIBILITY_REJECTED",
                runtime_attempted=False,
                handoff_path=tuple(handoff_path),
                compatibility=compatibility,
                trace=self._make_trace(
                    scenario_id,
                    intent_output.trace_candidate.trace_id,
                    causal_output.trace_candidate.trace_id,
                    decision_output.trace_candidate.trace_id,
                    "",
                    "",
                ),
                provenance=ProvenanceReversePathV1(
                    execution_result_ref="not-executed",
                    action_candidate_ref="not-executed",
                    decision_candidate_ref=decision_output.selection_candidate.selected_candidate_ref,
                    causal_hypothesis_refs=tuple(
                        x.hypothesis_id for x in causal_output.hypothesis_candidates
                    ),
                    intent_candidate_refs=tuple(
                        x.intent_id for x in intent_output.intent_candidates
                    ),
                    source_evidence_or_context_refs=tuple(
                        x.ref_id for x in h1_input.context_refs
                    ),
                    reverse_locatable=False,
                ),
                reconsideration_candidates=(),
                diagnostics_candidates=tuple(diagnostics),
                errors=tuple(errors),
                metadata=metadata,
            )

        if not self._idempotency.consume_handoff_once(h3_env.handoff_id):
            errors.append(
                make_error(
                    "H3_DUPLICATE_HANDOFF",
                    "duplicate H3 handoff consumed",
                    "idempotency",
                    True,
                )
            )
            metadata["duplicate_handoff_guard_triggered"] = "true"

        handoff_path.append("H3")

        # L4 Action
        action_output = self._action_engine.run_case(h3_input)

        action_not_ready = action_output.readiness.state != "candidate_ready"
        if action_not_ready:
            reconsideration.extend(
                build_action_feedback_reconsideration(
                    scenario_id,
                    action_output.action_candidate.action_state,
                    action_output.action_candidate.action_candidate_id,
                )
            )

            if directive.permission_hard_block_probe:
                metadata["terminal_stop_reason"] = "permission_permanently_denied"
                stopped_at = "LOOP_TERMINAL_STOP"
            elif action_output.action_candidate.action_state == "CANCELLED":
                stopped_at = "ACTION_CANCELLED_STOP"
            elif action_output.action_candidate.action_state == "NEEDS_PERMISSION":
                stopped_at = "ACTION_PERMISSION_REVOKED_STOP"
            elif action_output.action_candidate.action_state == "NEEDS_CONFIRMATION":
                stopped_at = "ACTION_STALE_CONFIRMATION_STOP"
            else:
                stopped_at = "ACTION_STOP_BEFORE_RUNTIME"

            return self._build_record(
                scenario_id,
                stopped_at=stopped_at,
                runtime_attempted=False,
                handoff_path=tuple(handoff_path),
                compatibility=compatibility,
                trace=self._make_trace(
                    scenario_id,
                    intent_output.trace_candidate.trace_id,
                    causal_output.trace_candidate.trace_id,
                    decision_output.trace_candidate.trace_id,
                    action_output.trace_candidate.trace_id,
                    "not-executed:runtime",
                ),
                provenance=ProvenanceReversePathV1(
                    execution_result_ref="not-executed",
                    action_candidate_ref=action_output.action_candidate.action_candidate_id,
                    decision_candidate_ref=decision_output.selection_candidate.selected_candidate_ref,
                    causal_hypothesis_refs=tuple(
                        x.hypothesis_id for x in causal_output.hypothesis_candidates
                    ),
                    intent_candidate_refs=tuple(
                        x.intent_id for x in intent_output.intent_candidates
                    ),
                    source_evidence_or_context_refs=tuple(
                        x.ref_id for x in h1_input.context_refs
                    ),
                    reverse_locatable=True,
                ),
                reconsideration_candidates=tuple(reconsideration),
                diagnostics_candidates=tuple(diagnostics),
                errors=tuple(errors),
                metadata=metadata,
            )

        # H4 Action -> Runtime
        h4_input, h4_env = map_action_to_runtime(
            scenario_id,
            action_output,
            directive,
            get_default_hop_version("H4"),
        )
        h4_cmp = self._compatibility_gate(directive, "H4")
        compatibility.append(h4_cmp)

        if not self._trace_gate(directive, "H4", h4_env):
            errors.append(
                make_error(
                    "H4_MISSING_TRACE", "missing trace ref in H4", "trace", False
                )
            )
            return self._build_record(
                scenario_id,
                stopped_at="H4_TRACE_REJECTED",
                runtime_attempted=False,
                handoff_path=tuple(handoff_path),
                compatibility=compatibility,
                trace=self._make_trace(
                    scenario_id,
                    intent_output.trace_candidate.trace_id,
                    causal_output.trace_candidate.trace_id,
                    decision_output.trace_candidate.trace_id,
                    action_output.trace_candidate.trace_id,
                    "",
                ),
                provenance=ProvenanceReversePathV1(
                    execution_result_ref="not-executed",
                    action_candidate_ref=action_output.action_candidate.action_candidate_id,
                    decision_candidate_ref=decision_output.selection_candidate.selected_candidate_ref,
                    causal_hypothesis_refs=tuple(
                        x.hypothesis_id for x in causal_output.hypothesis_candidates
                    ),
                    intent_candidate_refs=tuple(
                        x.intent_id for x in intent_output.intent_candidates
                    ),
                    source_evidence_or_context_refs=tuple(
                        x.ref_id for x in h1_input.context_refs
                    ),
                    reverse_locatable=False,
                ),
                reconsideration_candidates=tuple(reconsideration),
                diagnostics_candidates=tuple(diagnostics),
                errors=tuple(errors),
                metadata=metadata,
            )

        if not h4_cmp.allow_handoff:
            errors.append(
                make_error(
                    "H4_COMPAT_BLOCK",
                    h4_cmp.reason,
                    "compatibility",
                    h4_cmp.hard_block is False,
                )
            )
            return self._build_record(
                scenario_id,
                stopped_at="H4_COMPATIBILITY_REJECTED",
                runtime_attempted=False,
                handoff_path=tuple(handoff_path),
                compatibility=compatibility,
                trace=self._make_trace(
                    scenario_id,
                    intent_output.trace_candidate.trace_id,
                    causal_output.trace_candidate.trace_id,
                    decision_output.trace_candidate.trace_id,
                    action_output.trace_candidate.trace_id,
                    "",
                ),
                provenance=ProvenanceReversePathV1(
                    execution_result_ref="not-executed",
                    action_candidate_ref=action_output.action_candidate.action_candidate_id,
                    decision_candidate_ref=decision_output.selection_candidate.selected_candidate_ref,
                    causal_hypothesis_refs=tuple(
                        x.hypothesis_id for x in causal_output.hypothesis_candidates
                    ),
                    intent_candidate_refs=tuple(
                        x.intent_id for x in intent_output.intent_candidates
                    ),
                    source_evidence_or_context_refs=tuple(
                        x.ref_id for x in h1_input.context_refs
                    ),
                    reverse_locatable=False,
                ),
                reconsideration_candidates=tuple(reconsideration),
                diagnostics_candidates=tuple(diagnostics),
                errors=tuple(errors),
                metadata=metadata,
            )

        if directive.duplicate_action_handoff_probe:
            self._idempotency.register_execution_request(
                action_output.action_candidate.action_candidate_id,
                h4_env.handoff_id,
            )

        if not self._idempotency.register_execution_request(
            action_output.action_candidate.action_candidate_id,
            h4_env.handoff_id,
        ):
            errors.append(
                make_error(
                    "H4_DUPLICATE_EXECUTION_REQUEST",
                    "duplicate action handoff generated duplicate request",
                    "idempotency",
                    True,
                )
            )
            metadata["duplicate_execution_request_guard_triggered"] = "true"
            return self._build_record(
                scenario_id,
                stopped_at="H4_DUPLICATE_EXECUTION_REQUEST_STOP",
                runtime_attempted=False,
                handoff_path=tuple(handoff_path),
                compatibility=compatibility,
                trace=self._make_trace(
                    scenario_id,
                    intent_output.trace_candidate.trace_id,
                    causal_output.trace_candidate.trace_id,
                    decision_output.trace_candidate.trace_id,
                    action_output.trace_candidate.trace_id,
                    "",
                ),
                provenance=ProvenanceReversePathV1(
                    execution_result_ref="not-executed",
                    action_candidate_ref=action_output.action_candidate.action_candidate_id,
                    decision_candidate_ref=decision_output.selection_candidate.selected_candidate_ref,
                    causal_hypothesis_refs=tuple(
                        x.hypothesis_id for x in causal_output.hypothesis_candidates
                    ),
                    intent_candidate_refs=tuple(
                        x.intent_id for x in intent_output.intent_candidates
                    ),
                    source_evidence_or_context_refs=tuple(
                        x.ref_id for x in h1_input.context_refs
                    ),
                    reverse_locatable=False,
                ),
                reconsideration_candidates=tuple(reconsideration),
                diagnostics_candidates=tuple(diagnostics),
                errors=tuple(errors),
                metadata=metadata,
            )

        handoff_path.append("H4")

        # L5 Runtime
        runtime_output = self._runtime_engine.run_case(h4_input)

        reconsideration.extend(
            build_runtime_feedback_reconsideration(
                scenario_id,
                runtime_output.result.status,
                runtime_output.result.execution_id,
                runtime_output.result.failure_ref,
            )
        )

        if directive.duplicate_feedback_probe and reconsideration:
            sig = f"{scenario_id}:{reconsideration[0].reason}"
            self._idempotency.register_feedback(sig)

        if reconsideration:
            sig = f"{scenario_id}:{reconsideration[0].reason}"
            if not self._idempotency.register_feedback(sig):
                metadata["duplicate_feedback_guard_triggered"] = "true"
                reconsideration = [reconsideration[0]]

        if runtime_output.result.status in {"FAILED_CANDIDATE", "TIMEOUT_CANDIDATE"}:
            diagnostics.append(
                self._diagnostics_candidate(
                    origin_layer="Runtime Executor",
                    error_namespace="RuntimeExecutorErrorV1",
                    trace_refs=(runtime_output.trace.trace_id,),
                    failure_category=runtime_output.result.status,
                    remediation_candidate_refs=(runtime_output.result.execution_id,),
                )
            )

        if directive.repeat_same_failure_probe:
            metadata["terminal_stop_reason"] = "repeated_same_failure"
        if directive.no_new_evidence_probe:
            metadata["terminal_stop_reason"] = "no_new_evidence"
        if directive.retry_authority_exhausted_probe:
            metadata["terminal_stop_reason"] = "retry_authority_exhausted"

        stopped_at = "RUNTIME_COMPLETED"
        if runtime_output.result.status == "REJECTED_CANDIDATE":
            stopped_at = "RUNTIME_ADMISSION_REJECTED"
        elif runtime_output.result.status == "FAILED_CANDIDATE":
            stopped_at = "RUNTIME_FAILURE_STOP"
        elif runtime_output.result.status == "TIMEOUT_CANDIDATE":
            stopped_at = "RUNTIME_TIMEOUT_STOP"
        elif runtime_output.result.status == "PARTIAL_RESULT_CANDIDATE":
            stopped_at = "RUNTIME_PARTIAL_STOP"

        if "terminal_stop_reason" in metadata:
            stopped_at = "LOOP_TERMINAL_STOP"

        return self._build_record(
            scenario_id,
            stopped_at=stopped_at,
            runtime_attempted=True,
            handoff_path=tuple(handoff_path),
            compatibility=compatibility,
            trace=self._make_trace(
                scenario_id,
                intent_output.trace_candidate.trace_id,
                causal_output.trace_candidate.trace_id,
                decision_output.trace_candidate.trace_id,
                action_output.trace_candidate.trace_id,
                runtime_output.trace.trace_id,
            ),
            provenance=ProvenanceReversePathV1(
                execution_result_ref=runtime_output.result.execution_id,
                action_candidate_ref=action_output.action_candidate.action_candidate_id,
                decision_candidate_ref=decision_output.selection_candidate.selected_candidate_ref,
                causal_hypothesis_refs=tuple(
                    x.hypothesis_id for x in causal_output.hypothesis_candidates
                ),
                intent_candidate_refs=tuple(
                    x.intent_id for x in intent_output.intent_candidates
                ),
                source_evidence_or_context_refs=tuple(
                    x.ref_id for x in h1_input.context_refs
                ),
                reverse_locatable=True,
            ),
            reconsideration_candidates=tuple(reconsideration),
            diagnostics_candidates=tuple(diagnostics),
            errors=tuple(errors),
            metadata=metadata,
        )
