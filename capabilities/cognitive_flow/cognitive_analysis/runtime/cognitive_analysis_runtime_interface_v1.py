"""Runtime interface declaration for the A3 controlled skeleton v1."""

from __future__ import annotations

from typing import Protocol

from .cognitive_analysis_runtime_types_v1 import (
    CognitiveAnalysisRuntimeRequestV1,
    CognitiveAnalysisRuntimeSkeletonResultV1,
)


class CognitiveAnalysisRuntimeInterfaceV1(Protocol):
    """Future Runtime shape; implementations must preserve the boundary contract."""

    def execute(
        self,
        request: CognitiveAnalysisRuntimeRequestV1,
    ) -> CognitiveAnalysisRuntimeSkeletonResultV1:
        """Return a candidate-only result without State or execution side effects."""
