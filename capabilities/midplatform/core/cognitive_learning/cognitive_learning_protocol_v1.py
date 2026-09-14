"""Protocol for controlled implementation v1."""

from __future__ import annotations

from typing import Protocol

from capabilities.midplatform.core.cognitive_learning.cognitive_learning_io_types_v1 import (
    CognitiveLearningInputV1,
    CognitiveLearningOutputV1,
)


class CognitiveLearningProtocolV1(Protocol):
    def run_case(
        self, request: CognitiveLearningInputV1
    ) -> CognitiveLearningOutputV1: ...
