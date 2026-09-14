"""Protocol for Decision Governance controlled implementation v1."""

from __future__ import annotations

from typing import Protocol

from capabilities.midplatform.core.decision_governance.decision_io_types_v1 import (
    DecisionGovernanceInputV1,
    DecisionGovernanceOutputV1,
)


class DecisionGovernanceProtocolV1(Protocol):
    def run_case(
        self, request: DecisionGovernanceInputV1
    ) -> DecisionGovernanceOutputV1: ...
