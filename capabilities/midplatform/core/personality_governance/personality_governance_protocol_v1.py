"""Protocol for the candidate-only Personality Governance owner."""

from __future__ import annotations

from typing import Protocol

from .personality_io_types_v1 import PersonalityGovernanceInputV1, PersonalityGovernanceOutputV1


class PersonalityGovernanceProtocolV1(Protocol):
    def run_case(self, request: PersonalityGovernanceInputV1) -> PersonalityGovernanceOutputV1:
        """Produce one deterministic candidate-only output."""
