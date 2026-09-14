"""Fixed fixture type for Context Integration DryRun v1."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True)
class CurrentCognitiveContextIntegrationFixtureV1:
    case_id: str
    role_reference: str
    goal_reference: str
    request: Mapping[str, object]
