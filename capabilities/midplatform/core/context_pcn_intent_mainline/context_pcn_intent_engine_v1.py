from __future__ import annotations

from typing import Dict, List, Tuple

from capabilities.midplatform.core.context_foundation.context_foundation_fixture_v1 import (
    get_context_foundation_fixture_cases_v1,
)
from capabilities.midplatform.core.context_foundation.context_foundation_skeleton_v1 import (
    ContextFoundationSkeletonV1,
)
from capabilities.midplatform.core.context_foundation.context_foundation_types_v1 import (
    ContextAssemblyInputV1,
)
from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_compatibility_v1 import (
    validate_context_to_pcn_compatibility,
    validate_pcn_to_intent_compatibility,
)
from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_idempotency_v1 import (
    ContextPcnIntentIdempotencyRegistryV1,
)
from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_mainline_error_types_v1 import (
    ContextPcnIntentIntegrationErrorV1,
    make_error,
)
from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_mainline_trace_types_v1 import (
    MainlineProvenanceReversePathV1,
    MainlineTraceLinkV1,
)
from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_mainline_types_v1 import (
    IntegrationExecutionRecordV1,
    IntegrationScenarioDirectiveV1,
    IntegrationRunPayloadV1,
    IntegrationRunSummaryV1,
    NegativeGuardFlagsV1,
)
from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_static_validators_v1 import (
    validate_integration_has_no_owner,
    validate_negative_guards,
    validate_owner_preservation,
    validate_provenance_reverse_lookup,
    validate_trace_continuity,
)
from capabilities.midplatform.core.context_pcn_intent_mainline.context_to_pcn_mapping_v1 import (
    build_context_to_pcn_handoff,
    map_context_to_pcn_case,
)
from capabilities.midplatform.core.context_pcn_intent_mainline.pcn_to_intent_mapping_v1 import (
    build_pcn_to_intent_handoff,
    map_pcn_to_intent_input,
)
from capabilities.midplatform.core.intent_governance.intent_governance_skeleton_v1 import (
    IntentGovernanceSkeletonV1,
)
from capabilities.midplatform.core.personal_cognitive_network.personal_cognitive_network_skeleton_v1 import (
    PersonalCognitiveNetworkSkeletonV1,
)


class ContextPcnIntentMainlineEngineV1:
    def __init__(self) -> None:
        self._context = ContextFoundationSkeletonV1()
        self._pcn = PersonalCognitiveNetworkSkeletonV1()
        self._intent = IntentGovernanceSkeletonV1()
        self._idempotency = ContextPcnIntentIdempotencyRegistryV1()

    def _base_context_input(self, scenario_id: str) -> ContextAssemblyInputV1:
        cases = get_context_foundation_fixture_cases_v1()
        fixture = cases[0].assembly_input
        return ContextAssemblyInputV1(
            context_id=f"context:{scenario_id}",
            version=fixture.version,
            temporal_scope=fixture.temporal_scope,
            field_projection_reference=fixture.field_projection_reference,
            observation_projection_reference=fixture.observation_projection_reference,
            memory_projection_reference=fixture.memory_projection_reference,
            self_projection_reference=fixture.self_projection_reference,
            role_projection_reference=fixture.role_projection_reference,
            relationship_projection_reference=fixture.relationship_projection_reference,
            emotion_projection_reference=fixture.emotion_projection_reference,
            mental_field_continuity_reference=fixture.mental_field_continuity_reference,
            provenance=(f"source-context:{scenario_id}",),
            trace_timestamp=fixture.trace_timestamp,
            direct_mutation_requested=False,
            skeleton_only=True,
        )

    def _build_error_record(
        self,
        directive: IntegrationScenarioDirectiveV1,
        stopped_at: str,
        errors: Tuple[ContextPcnIntentIntegrationErrorV1, ...],
        compatibility: tuple,
        context_handoff_id: str = "",
        pcn_handoff_id: str = "",
        context_candidate_ref: str = "",
        pcn_candidate_ref: str = "",
        intent_candidate_ref: str = "",
        context_trace_ref: str = "",
        pcn_trace_ref: str = "",
        intent_trace_ref: str = "",
        source_context_refs: Tuple[str, ...] = (),
        metadata: Dict[str, str] | None = None,
    ) -> IntegrationExecutionRecordV1:
        guard_flags = NegativeGuardFlagsV1()
        return IntegrationExecutionRecordV1(
            scenario_id=directive.scenario_id,
            description=directive.description,
            stopped_at=stopped_at,
            success=False,
            context_handoff_id=context_handoff_id,
            pcn_handoff_id=pcn_handoff_id,
            context_candidate_ref=context_candidate_ref,
            pcn_candidate_ref=pcn_candidate_ref,
            intent_candidate_ref=intent_candidate_ref,
            compatibility=compatibility,
            trace=MainlineTraceLinkV1(
                root_trace_id=f"root-trace:{directive.scenario_id}",
                context_trace_ref=context_trace_ref,
                pcn_trace_ref=pcn_trace_ref,
                intent_trace_ref=intent_trace_ref,
                candidate_only=True,
            ),
            provenance=MainlineProvenanceReversePathV1(
                intent_candidate_ref=intent_candidate_ref,
                pcn_projection_ref=pcn_candidate_ref,
                context_candidate_ref=context_candidate_ref,
                source_context_refs=source_context_refs,
                reverse_locatable=False,
                provenance_chain=(),
            ),
            guard_flags=guard_flags,
            errors=errors,
            diagnostics=("controlled-stop",),
            metadata=metadata or {},
        )

    def run_case(
        self, directive: IntegrationScenarioDirectiveV1
    ) -> IntegrationExecutionRecordV1:
        compatibility = []
        metadata: Dict[str, str] = {}

        # Stage 1: Context Foundation
        try:
            context_input = self._base_context_input(directive.scenario_id)
            if directive.force_context_incomplete:
                context_input = ContextAssemblyInputV1(
                    context_id=f"context:{directive.scenario_id}",
                    version="context-v1",
                    temporal_scope=context_input.temporal_scope,
                    provenance=(f"source-context:{directive.scenario_id}",),
                    trace_timestamp=context_input.trace_timestamp,
                    direct_mutation_requested=False,
                    skeleton_only=True,
                )
            context_candidate = self._context.assemble_context(context_input)
        except Exception as exc:
            return self._build_error_record(
                directive,
                stopped_at="STOP_BEFORE_PCN_CONTEXT_INCOMPLETE",
                errors=(
                    make_error(
                        "CONTEXT_INCOMPLETE",
                        "CONTEXT",
                        "context assembly failed",
                        False,
                        detail=str(exc),
                    ),
                ),
                compatibility=(),
                metadata={"category": "context_incomplete"},
            )

        h1 = build_context_to_pcn_handoff(context_candidate, directive)
        c1 = validate_context_to_pcn_compatibility(h1)
        compatibility.append(c1)

        if not c1.compatible:
            stop = (
                "HARD_BLOCK_CONTEXT_TO_PCN_VERSION_MISMATCH"
                if c1.hard_block
                else "REJECT_CONTEXT_TO_PCN_REQUIRED_REF"
            )
            return self._build_error_record(
                directive,
                stopped_at=stop,
                errors=(
                    make_error(
                        "CONTEXT_TO_PCN_REJECT",
                        "CONTEXT_TO_PCN",
                        c1.reason,
                        c1.hard_block,
                    ),
                ),
                compatibility=tuple(compatibility),
                context_handoff_id=h1.handoff_id,
                context_candidate_ref=context_candidate.context_id,
                context_trace_ref=context_candidate.trace_reference,
                source_context_refs=tuple(h1.field_context_refs),
                metadata={"gap_classification": c1.classification},
            )

        if directive.duplicate_context_handoff_probe:
            self._idempotency.consume_context_handoff_once(h1.handoff_id)
        if not self._idempotency.consume_context_handoff_once(h1.handoff_id):
            return self._build_error_record(
                directive,
                stopped_at="STOP_DUPLICATE_CONTEXT_HANDOFF",
                errors=(
                    make_error(
                        "DUPLICATE_CONTEXT_HANDOFF",
                        "CONTEXT_TO_PCN",
                        "duplicate context handoff",
                        False,
                    ),
                ),
                compatibility=tuple(compatibility),
                context_handoff_id=h1.handoff_id,
                context_candidate_ref=context_candidate.context_id,
                context_trace_ref=context_candidate.trace_reference,
                source_context_refs=tuple(h1.field_context_refs),
                metadata={"idempotency_guard": "context_handoff"},
            )

        # Stage 2: PCN
        pcn_case = map_context_to_pcn_case(context_candidate, directive)
        pcn_result = self._pcn.run_case(pcn_case)

        if directive.force_pcn_incomplete:
            return self._build_error_record(
                directive,
                stopped_at="STOP_BEFORE_INTENT_PCN_INCOMPLETE",
                errors=(
                    make_error(
                        "PCN_INCOMPLETE",
                        "PCN",
                        "pcn output incomplete",
                        False,
                    ),
                ),
                compatibility=tuple(compatibility),
                context_handoff_id=h1.handoff_id,
                context_candidate_ref=context_candidate.context_id,
                pcn_candidate_ref=pcn_result.projection.projection_id,
                context_trace_ref=context_candidate.trace_reference,
                pcn_trace_ref=pcn_result.trace.trace_id,
                source_context_refs=tuple(h1.field_context_refs),
                metadata={"category": "pcn_incomplete"},
            )

        h2 = build_pcn_to_intent_handoff(context_candidate, pcn_result, directive)
        c2 = validate_pcn_to_intent_compatibility(h2)
        compatibility.append(c2)

        if not c2.compatible:
            stop = (
                "HARD_BLOCK_PCN_TO_INTENT_VERSION_MISMATCH"
                if c2.hard_block
                else "REJECT_PCN_TO_INTENT_REQUIRED_REF"
            )
            return self._build_error_record(
                directive,
                stopped_at=stop,
                errors=(
                    make_error(
                        "PCN_TO_INTENT_REJECT",
                        "PCN_TO_INTENT",
                        c2.reason,
                        c2.hard_block,
                    ),
                ),
                compatibility=tuple(compatibility),
                context_handoff_id=h1.handoff_id,
                pcn_handoff_id=h2.handoff_id,
                context_candidate_ref=context_candidate.context_id,
                pcn_candidate_ref=pcn_result.projection.projection_id,
                context_trace_ref=context_candidate.trace_reference,
                pcn_trace_ref=pcn_result.trace.trace_id,
                source_context_refs=tuple(h1.field_context_refs),
                metadata={"gap_classification": c2.classification},
            )

        if directive.duplicate_pcn_handoff_probe:
            self._idempotency.consume_pcn_handoff_once(h2.handoff_id)
        if not self._idempotency.consume_pcn_handoff_once(h2.handoff_id):
            return self._build_error_record(
                directive,
                stopped_at="STOP_DUPLICATE_PCN_HANDOFF",
                errors=(
                    make_error(
                        "DUPLICATE_PCN_HANDOFF",
                        "PCN_TO_INTENT",
                        "duplicate pcn handoff",
                        False,
                    ),
                ),
                compatibility=tuple(compatibility),
                context_handoff_id=h1.handoff_id,
                pcn_handoff_id=h2.handoff_id,
                context_candidate_ref=context_candidate.context_id,
                pcn_candidate_ref=pcn_result.projection.projection_id,
                context_trace_ref=context_candidate.trace_reference,
                pcn_trace_ref=pcn_result.trace.trace_id,
                source_context_refs=tuple(h1.field_context_refs),
                metadata={"idempotency_guard": "pcn_handoff"},
            )

        # Stage 3: Intent Governance
        intent_input = map_pcn_to_intent_input(context_candidate, pcn_result, directive)
        if directive.force_intent_reject:
            return self._build_error_record(
                directive,
                stopped_at="REJECT_INTENT_FORMATION",
                errors=(
                    make_error(
                        "INTENT_FORMATION_REJECTED",
                        "INTENT",
                        "intent formation rejected due to missing source refs",
                        False,
                    ),
                ),
                compatibility=tuple(compatibility),
                context_handoff_id=h1.handoff_id,
                pcn_handoff_id=h2.handoff_id,
                context_candidate_ref=context_candidate.context_id,
                pcn_candidate_ref=pcn_result.projection.projection_id,
                context_trace_ref=context_candidate.trace_reference,
                pcn_trace_ref=pcn_result.trace.trace_id,
                source_context_refs=tuple(h1.field_context_refs),
                metadata={"category": "intent_reject"},
            )

        intent_output = self._intent.run_case(intent_input)
        intent_candidate_ref = intent_output.intent_candidates[0].intent_id

        guard_flags = NegativeGuardFlagsV1()
        owner_ok = validate_owner_preservation(
            context_owner=h1.source_owner,
            pcn_owner=h2.source_owner,
            intent_owner=intent_output.intent_candidates[0].owner,
        )
        no_owner_ok = validate_integration_has_no_owner(
            guard_flags.integration_has_no_owner
        )
        guard_ok = validate_negative_guards(guard_flags)

        trace = MainlineTraceLinkV1(
            root_trace_id=f"root-trace:{directive.scenario_id}",
            context_trace_ref=context_candidate.trace_reference,
            pcn_trace_ref=pcn_result.trace.trace_id,
            intent_trace_ref=intent_output.trace_candidate.trace_id,
            candidate_only=True,
        )
        trace_ok = validate_trace_continuity(
            trace.root_trace_id,
            trace.context_trace_ref,
            trace.pcn_trace_ref,
            trace.intent_trace_ref,
        )

        provenance = MainlineProvenanceReversePathV1(
            intent_candidate_ref=intent_candidate_ref,
            pcn_projection_ref=pcn_result.projection.projection_id,
            context_candidate_ref=context_candidate.context_id,
            source_context_refs=tuple(h1.field_context_refs),
            reverse_locatable=True,
            provenance_chain=(
                f"intent:{intent_candidate_ref}",
                f"pcn:{pcn_result.projection.projection_id}",
                f"context:{context_candidate.context_id}",
            ),
        )
        provenance_ok = validate_provenance_reverse_lookup(
            provenance.source_context_refs,
            provenance.reverse_locatable,
        )

        errors: List[ContextPcnIntentIntegrationErrorV1] = []
        if not owner_ok:
            errors.append(
                make_error(
                    "OWNER_PRESERVATION_FAILED",
                    "OWNER",
                    "owner preservation failed",
                    True,
                )
            )
        if not no_owner_ok:
            errors.append(
                make_error(
                    "INTEGRATION_OWNER_VIOLATION",
                    "OWNER",
                    "integration must have no owner authority",
                    True,
                )
            )
        if not guard_ok:
            errors.append(
                make_error(
                    "NEGATIVE_GUARD_VIOLATION",
                    "GUARD",
                    "negative guards violated",
                    True,
                )
            )
        if not trace_ok:
            errors.append(
                make_error(
                    "TRACE_CONTINUITY_FAILED",
                    "TRACE",
                    "trace continuity failed",
                    False,
                )
            )
        if not provenance_ok:
            errors.append(
                make_error(
                    "PROVENANCE_CONTINUITY_FAILED",
                    "PROVENANCE",
                    "provenance reverse lookup failed",
                    False,
                )
            )

        success = len(errors) == 0
        return IntegrationExecutionRecordV1(
            scenario_id=directive.scenario_id,
            description=directive.description,
            stopped_at="INTENT_CANDIDATE_READY"
            if success
            else "STOP_WITH_VALIDATION_ERRORS",
            success=success,
            context_handoff_id=h1.handoff_id,
            pcn_handoff_id=h2.handoff_id,
            context_candidate_ref=context_candidate.context_id,
            pcn_candidate_ref=pcn_result.projection.projection_id,
            intent_candidate_ref=intent_candidate_ref,
            compatibility=tuple(compatibility),
            trace=trace,
            provenance=provenance,
            guard_flags=guard_flags,
            errors=tuple(errors),
            diagnostics=("owner-preserved", "candidate-only"),
            metadata=metadata,
        )

    def run_all(
        self, directives: Tuple[IntegrationScenarioDirectiveV1, ...]
    ) -> IntegrationRunPayloadV1:
        results = [self.run_case(item) for item in directives]
        passed = sum(1 for item in results if item.success)
        summary = IntegrationRunSummaryV1(
            phase="Phase-Luna-Context-PCN-Intent-PreCognitive-Mainline-Controlled-Integration-v1-001",
            scenario_count=len(results),
            passed_scenario_count=passed,
            failed_scenario_count=len(results) - passed,
            candidate_only=True,
            synthetic_only=True,
            runtime_executed=False,
            database_write=False,
            device_control=False,
            scheduler_execution=False,
            task_mutation=False,
            source_module_mutation=False,
            model_call=False,
            status="CONTEXT_PCN_INTENT_MAINLINE_RESULT_CANDIDATE_READY",
        )
        return IntegrationRunPayloadV1(
            summary=summary, scenario_results=results, artifacts={}
        )
