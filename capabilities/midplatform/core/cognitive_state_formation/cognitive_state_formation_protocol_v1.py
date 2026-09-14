"""Protocol for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from typing import Protocol

from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
    CognitiveStateFormationOutputV1,
)


class CognitiveStateFormationProtocolV1(Protocol):
    def run_case(
        self, request: CognitiveStateFormationInputV1
    ) -> CognitiveStateFormationOutputV1: ...
