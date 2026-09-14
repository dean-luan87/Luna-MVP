# -*- coding: utf-8 -*-
"""Pure Context Foundation protocol v1; no source or Runtime calls."""

from __future__ import annotations

from typing import Protocol, Tuple

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


class ContextFoundationProtocolV1(Protocol):
    """Context assembly interface only; it owns no source object."""

    def validate_projection(
        self, projection: ProjectionReferenceV1
    ) -> ContextValidationResultV1:
        """Validate one reference-only source projection."""

    def assemble_context(
        self, request: ContextAssemblyInputV1
    ) -> ContextEnvelopeCandidateV1:
        """Assemble a Context Envelope Candidate without Runtime or mutation."""

    def create_trace(
        self,
        request: ContextAssemblyInputV1,
        assembly_steps: Tuple[str, ...],
    ) -> ContextFoundationTraceV1:
        """Create deterministic trace metadata for the candidate assembly."""

    def get_context_snapshot(
        self, context: ContextEnvelopeCandidateV1
    ) -> ContextEnvelopeCandidateV1:
        """Return the immutable candidate itself; no storage lookup is performed."""

