"""Protocol for the controlled Self Governance owner."""

from __future__ import annotations

from typing import Protocol

from .self_io_types_v1 import SelfGovernanceInputV1, SelfGovernanceOutputV1


class SelfGovernanceProtocolV1(Protocol):
    def run_case(self, request: SelfGovernanceInputV1) -> SelfGovernanceOutputV1: ...
