"""Protocol for controlled implementation v1."""

from __future__ import annotations

from typing import Protocol

from capabilities.midplatform.core.cognitive_memory_experience.memory_io_types_v1 import (
    CognitiveMemoryExperienceInputV1,
    CognitiveMemoryExperienceOutputV1,
)


class CognitiveMemoryExperienceProtocolV1(Protocol):
    def run_case(
        self, request: CognitiveMemoryExperienceInputV1
    ) -> CognitiveMemoryExperienceOutputV1: ...
