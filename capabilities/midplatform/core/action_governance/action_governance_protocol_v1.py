"""Protocol for Action Governance controlled implementation v1."""

from __future__ import annotations

from typing import Protocol

from capabilities.midplatform.core.action_governance.action_io_types_v1 import (
    ActionGovernanceInputV1,
    ActionGovernanceOutputV1,
)


class ActionGovernanceProtocolV1(Protocol):
    def run_case(
        self, request: ActionGovernanceInputV1
    ) -> ActionGovernanceOutputV1: ...
