"""Protocol for Intent Governance controlled implementation v1."""

from __future__ import annotations

from typing import Protocol

from capabilities.midplatform.core.intent_governance.intent_io_types_v1 import (
    IntentGovernanceInputV1,
    IntentGovernanceOutputV1,
)


class IntentGovernanceProtocolV1(Protocol):
    def run_case(
        self, request: IntentGovernanceInputV1
    ) -> IntentGovernanceOutputV1: ...
