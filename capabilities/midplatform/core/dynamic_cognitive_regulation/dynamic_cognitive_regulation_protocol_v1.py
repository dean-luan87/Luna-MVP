"""Pure protocol for deterministic candidate generation."""

from __future__ import annotations

from typing import Protocol

from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_regulation_io_types_v1 import (
    DynamicCognitiveRegulationInputV1,
    DynamicCognitiveRegulationOutputV1,
)


class DynamicCognitiveRegulationProtocolV1(Protocol):
    def evaluate(
        self, request: DynamicCognitiveRegulationInputV1
    ) -> DynamicCognitiveRegulationOutputV1: ...
