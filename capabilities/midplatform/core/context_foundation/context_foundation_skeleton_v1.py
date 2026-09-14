# -*- coding: utf-8 -*-
"""Controlled, non-runtime Context Foundation assembly skeleton v1."""

from __future__ import annotations

import hashlib
from typing import List, Tuple

from capabilities.midplatform.core.context_foundation.context_foundation_protocol_v1 import (
    ContextFoundationProtocolV1,
)
from capabilities.midplatform.core.context_foundation.context_foundation_static_validators_v1 import (
    projection_references,
    validate_context_envelope_boundary,
    validate_context_input,
    validate_projection_owner_exists,
    validate_projection_reference_complete,
    validate_unknown_preserved,
)
from capabilities.midplatform.core.context_foundation.context_foundation_trace_types_v1 import (
    ContextFoundationTraceV1,
)
from capabilities.midplatform.core.context_foundation.context_foundation_types_v1 import (
    ContextAssemblyInputV1,
    ContextEnvelopeCandidateV1,
    ContextValidationResultV1,
)
from capabilities.midplatform.core.context_foundation.context_projection_types_v1 import (
    ProjectionReferenceV1,
)


class ContextFoundationSkeletonV1(ContextFoundationProtocolV1):
    """Assemble immutable reference candidates without source or Runtime access."""

    skeleton_only = True
    runtime_implemented = False
    real_context_generation_allowed = False
    source_object_storage_allowed = False
    source_mutation_allowed = False
    database_access_allowed = False
    model_call_allowed = False
    external_lookup_allowed = False
    intent_output_allowed = False
    causal_output_allowed = False
    decision_output_allowed = False

    def validate_projection(
        self, projection: ProjectionReferenceV1
    ) -> ContextValidationResultV1:
        issues: List[str] = []
        for result in (
            validate_projection_owner_exists(projection),
            validate_projection_reference_complete(projection),
            validate_unknown_preserved(projection),
        ):
            issues.extend(result.issues)
        return ContextValidationResultV1(valid=not issues, issues=tuple(issues))

    def create_trace(
        self,
        request: ContextAssemblyInputV1,
        assembly_steps: Tuple[str, ...],
    ) -> ContextFoundationTraceV1:
        input_refs = tuple(
            item.projection_id for item in projection_references(request)
        )
        if request.mental_field_continuity_reference is not None:
            input_refs = input_refs + (
                request.mental_field_continuity_reference.continuity_id,
            )
        trace_material = "|".join(
            (request.context_id, request.version, request.trace_timestamp) + input_refs
        )
        trace_id = "ctx_trace_" + hashlib.sha256(
            trace_material.encode("utf-8")
        ).hexdigest()[:24]
        return ContextFoundationTraceV1(
            trace_id=trace_id,
            input_projection_refs=input_refs,
            assembly_steps=assembly_steps,
            output_context_reference=request.context_id,
            timestamp=request.trace_timestamp,
            status="CONTEXT_TRACE_CANDIDATE",
            provenance=request.provenance,
            skeleton_only=True,
            runtime_executed=False,
            state_mutation_executed=False,
        )

    def assemble_context(
        self, request: ContextAssemblyInputV1
    ) -> ContextEnvelopeCandidateV1:
        validation = validate_context_input(request)
        if not validation.valid:
            raise ValueError("context_input_invalid:" + ",".join(validation.issues))

        assembly_steps = (
            "validate_projection_references",
            "preserve_unknown_and_source_owner",
            "assemble_reference_only_envelope_candidate",
            "create_context_trace_candidate",
        )
        trace = self.create_trace(request, assembly_steps)
        envelope = ContextEnvelopeCandidateV1(
            context_id=request.context_id,
            version=request.version,
            temporal_scope=request.temporal_scope,
            field_projection_reference=request.field_projection_reference,
            observation_projection_reference=request.observation_projection_reference,
            memory_projection_reference=request.memory_projection_reference,
            self_projection_reference=request.self_projection_reference,
            role_projection_reference=request.role_projection_reference,
            relationship_projection_reference=request.relationship_projection_reference,
            emotion_projection_reference=request.emotion_projection_reference,
            mental_field_continuity_reference=request.mental_field_continuity_reference,
            provenance=request.provenance,
            trace_reference=trace.trace_id,
            status="CONTEXT_ENVELOPE_CANDIDATE",
            candidate_only=True,
            reference_only=True,
            skeleton_only=True,
            real_context_generation=False,
            runtime_executed=False,
            state_mutation=False,
            fact_write_executed=False,
            intent_output_created=False,
            causal_output_created=False,
            decision_output_created=False,
        )
        output_validation = validate_context_envelope_boundary(envelope)
        if not output_validation.valid:
            raise ValueError(
                "context_output_boundary_invalid:"
                + ",".join(output_validation.issues)
            )
        return envelope

    def get_context_snapshot(
        self, context: ContextEnvelopeCandidateV1
    ) -> ContextEnvelopeCandidateV1:
        validation = validate_context_envelope_boundary(context)
        if not validation.valid:
            raise ValueError(
                "context_snapshot_boundary_invalid:" + ",".join(validation.issues)
            )
        return context

