"""Protocol for Causal Governance controlled implementation v1."""

from __future__ import annotations

from typing import Protocol

from capabilities.midplatform.core.causal_governance.causal_io_types_v1 import (
    CausalGovernanceInputV1,
    CausalGovernanceOutputV1,
)


class CausalGovernanceProtocolV1(Protocol):
    def run_case(
        self, request: CausalGovernanceInputV1
    ) -> CausalGovernanceOutputV1: ...
