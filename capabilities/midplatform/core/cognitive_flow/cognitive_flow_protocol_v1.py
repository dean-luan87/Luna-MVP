"""Protocol for Cognitive Flow controlled implementation v1."""

from __future__ import annotations

from typing import Protocol

from capabilities.midplatform.core.cognitive_flow.cognitive_flow_io_types_v1 import (
    CognitiveFlowInputV1,
    CognitiveFlowOutputV1,
)


class CognitiveFlowProtocolV1(Protocol):
    def run_case(self, request: CognitiveFlowInputV1) -> CognitiveFlowOutputV1: ...
